import pygame
from pygame.locals import *
import math
import json
import spells
import random
import time 


CIRCLECOLOR = (100, 100, 255)
LINEDRAWCOLOR = (204, 115, 255)
LINECASTCOLOR = (0, 208, 255)
LINEERRORCOLOR = (255, 0, 0)
LINECONSIDEREDCOLOR = (245, 245, 66)
LINEWIDTH = 7
ADDSPELLMODE = False 


def checkspells(spells):
    for spell in spells:
        if not "offset" in spells[spell]:
            spells[spell]["offset"] = int(input(f"please input offset for spell {spells[spell]["name"]}"))
        if not "description" in spells[spell] or spells[spell]["description"] == None:
            spells[spell]["description"] = input(f"please input description for spell {spells[spell]["name"]} has no description given")
        if spells[spell]["directions"][0] != 0:
            offset = spells[spell]["directions"][0]
            spells[spell]["directions"] = [(direction-offset)%6 for direction in spells[spell]["directions"]]
            print(f"normalised {spells[spell]["name"]}")


def eval_numerical_reflection(directions, startdirection):
    num = 0
    currentdirection = startdirection
    for direction in directions:
        angle = (direction - currentdirection) % 6
        currentdirection = direction
        if angle == 0:
            num += 1
        elif angle == 1:
            num += 10
        elif angle == 2:
            num /= 2
        elif angle == 4:
            num *= 2
        elif angle == 5:
            num += 5
    return num
        

def check_numerical_reflection(directions, currentstack):
    if directions[0:5] == [0,4,3,1,5]:      
        num_directions = directions[5:]
        currentstack.append(eval_numerical_reflection(num_directions, 5))
        return True
    elif directions[0:5] == [0,2,3,5,1]:
        num_directions = directions[5:]
        currentstack.append(-1*eval_numerical_reflection(num_directions, 1))
        return True
    return False


def check_bookkeeper_gambit(directions, currentstack, gameobj):
    bookkeeper = []
    if directions[:2] == [0, 4]:
        bookkeeper.append(0)
        i = 2
        while i < len(directions):
            if directions[i] == 5:
                i += 1
                bookkeeper.append(1)
            elif directions[i:i+2] == [0, 4]:
                i += 2
                bookkeeper.append(0)
            else:
                return False
    elif directions[0] == 0:
        bookkeeper.append(1)
        i = 1
        while i < len(directions):
            if directions[i] == 0:
                i += 1
                bookkeeper.append(1)
            elif directions[i:i+2] == [1, 5]:
                i += 2
                bookkeeper.append(0)
            else:
                return False
    if len(bookkeeper) > len(currentstack):
        gameobj.spellerror = True
        return True
    bookkeepindex = 0
    stackindex = -1
    for _ in range(len(bookkeeper)):
        if bookkeeper[bookkeepindex] == 0:
            del currentstack[stackindex]
        else:
            stackindex -= 1
        bookkeepindex += 1
    return True

def renderpattern(surface, startx, starty, patternstring, maxwidth, maxheight):
    verticaldistance = round(math.sqrt(100*100+50*50)) 
    currentx = 0
    currenty = 0
    xpos = [0]
    ypos = [0]
    numbers = patternstring.replace("<", "").replace(">", "")
    for number in numbers:
        match number:
            case "0":
                currentx += 100
            case "1":
                currentx += 50
                currenty += verticaldistance
            case "2":
                currentx -= 50
                currenty += verticaldistance
            case "3":
                currentx -= 100
            case "4":
                currentx -= 50
                currenty -= verticaldistance
            case "5":
                currentx += 50
                currenty -= verticaldistance
        xpos.append(currentx)
        ypos.append(currenty)
    patternwidth = max(*xpos) - min(*xpos)
    patternheight = max(*ypos) - min(*ypos)
    xof = -1*min(*xpos)
    yof = -1*min(*ypos)
    if patternheight == 0:
        yof = maxheight/2
    widthscale = heightscale = 1
    if patternwidth > maxwidth:
        widthscale = maxwidth/patternwidth
    if patternheight > maxheight:
        heightscale = maxheight/patternheight
    scale = min(widthscale, heightscale)
    if patternheight*scale < maxheight:
        yof += (maxheight-patternheight*scale)/scale/2
    elif patternwidth*scale < maxwidth:
        xof += (maxwidth-patternwidth*scale)/scale/2
    linewidth = 2 if scale > 0.5 else 1
    for i in range(len(xpos)-1):
        pygame.draw.line(surface, LINEDRAWCOLOR, (startx+(xof+xpos[i])*scale, starty+(yof+ypos[i])*scale), (startx+(xof+xpos[i+1])*scale, starty+(yof+ypos[i+1])*scale), width=linewidth)

                



def iotatostring(iota, stacksurface, row, column):
    testtext = Game.font.render(" ", False, (0, 0, 0))
    testrect = testtext.get_rect()
    letterwidth, letterheight = testrect.width, testrect.height
    if type(iota) in [int,float]:
        return "{:.2f}".format(iota)
    elif type(iota) == bool:
        return str(iota)
    elif type(iota) == tuple:
        return "({:.2f}, {:.2f}, {:.2f})".format(*iota)
    elif type(iota) == list:
        string = "["
        drawcolumn = column + 1
        for i in range(len(iota)):
            appendstring = iotatostring(iota[i], stacksurface, row, drawcolumn)
            drawcolumn += len(appendstring)
            string += appendstring
            if i != len(iota)-1:
                if type(iota[i+1]) != str:
                    string += ", "
                    drawcolumn += 2
                else:
                    string += ","
                    drawcolumn += 1
        string += "]"
        return string
    elif type(iota) == str:
        #strings are used for patterns and other internal types
        if iota == "ERROR":
            return "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!§$%&/()=?\\ß*+-#'_.:,;", k=20))
        if iota.startswith("<"):
            patternx = column*letterwidth
            patterny = (row-1)*letterheight+0.1*letterheight
            renderpattern(stacksurface, patternx, patterny, iota, letterwidth*1.8, letterheight*0.8)
            return "  "
        return iota
    elif iota is None:
        return "Null"
    else:
        return ""


def drawstack(currentstack, gamesurface, stacksurface):
    stacksurface.fill((0, 0, 0, 0))
    stacksurface.fill((0, 0, 0, 100))
    i = len(currentstack)-1
    while i >= 0 and i > len(currentstack)-20:
        string = iotatostring(currentstack[i], stacksurface, len(currentstack)-i, 0)
        color = LINEDRAWCOLOR
        if currentstack[i] == "ERROR":
            color = LINEERRORCOLOR
        text = Game.font.render(string, False, color)
        textRect = text.get_rect()
        textRect.center = (textRect.width//2, round(textRect.height*(len(currentstack)-i-0.5)))
        stacksurface.blit(text, textRect)
        i -= 1
    gamesurface.blit(stacksurface, (32, 32))



def newspell(currentspells, spelldirections, offset):
    spellname = input("What is the Spell called?")
    id = input("What should the Spell ID be?")
    if id == "":
        id = spellname.lower().replace(" ", "_")
        id = id.replace("'", "")
    description = input("What does it do?")
    currentspells[id] = {
        "name": spellname,
        "directions": spelldirections,
        "offset": offset,
        "description": description
    }
    with open(f'spells.py', 'a') as f:
        f.write(f'#{spellname}\n#{description}\ndef {id}(currentstack, gameobj):\n    pass\n\n\n')

def setconnectionsstate(state, gameobj, staffcast):
    if not staffcast:
        print("not cast by staff, skipping")
        if len(gameobj.castspells[-1]) == 0:
            print("nothing to set anyway")
        return
    if len(gameobj.castspells) > 0:
        print("jup, that one works alright")
        if len(gameobj.castspells[-1]) == 0:
            print("nothing to set though")
        for connection in gameobj.castspells[-1]:
            if connection.state == "Drawing":
                connection.state = state


def executespell(currentspell, currentstack, gameobj, staffcast=True):
    gameobj.castspells.append(gameobj.currentconnections)
    gameobj.currentconnections = []
    gameobj.spellerror = False
    offset = currentspell[0]
    normalspell = [(direction-offset)%6 for direction in currentspell]
    if gameobj.consideration:
        if gameobj.introspectionlevel > 0:
            gameobj.introspectionlist.append(f"<{"".join([str(direction) for direction in currentspell])}>")
        else:
            currentstack.append(f"<{"".join([str(direction) for direction in currentspell])}>")
        gameobj.consideration = False
        setconnectionsstate("Considered", gameobj, staffcast)
        return
    tocast = None 
    for spell in gameobj.spells:
        if gameobj.spells[spell]["directions"] == normalspell:
            tocast = spell
    #Certain spells which need Game Object
    if tocast == "consideration":
        gameobj.consideration = True
        setconnectionsstate("Cast", gameobj, staffcast)
        return
    elif tocast == "evanition":
        if len(gameobj.introspectionlist) > 0:
            gameobj.introspectionlist.pop()
            setconnectionsstate("Considered", gameobj, staffcast)
            return
    elif tocast == "introspection":
        if gameobj.introspectionlevel > 0:
            gameobj.introspectionlist.append(f"<{''.join([str(direction) for direction in currentspell])}>")
            setconnectionsstate("Considered", gameobj, staffcast)
        else:
            setconnectionsstate("Cast", gameobj, staffcast)
        gameobj.introspectionlevel += 1
        return
    elif tocast == "retrospection":
        gameobj.introspectionlevel -= 1
        if gameobj.introspectionlevel > 0:
            gameobj.introspectionlist.append(f"<{''.join([str(direction) for direction in currentspell])}>")
            setconnectionsstate("Considered", gameobj, staffcast) 
        else:
            currentstack.append(gameobj.introspectionlist)
            gameobj.introspectionlist = []
            setconnectionsstate("Cast", gameobj, staffcast)
        return
    elif gameobj.introspectionlevel > 0:
        gameobj.introspectionlist.append(f"<{''.join([str(direction) for direction in currentspell])}>")
        setconnectionsstate("Considered", gameobj, staffcast)
        return
    elif tocast is not None: 
        spellfunction = getattr(spells, tocast)
        spellfunction(currentstack, gameobj)
    else:
        if check_numerical_reflection(normalspell, currentstack):
            setconnectionsstate("Cast", gameobj, staffcast)
            return
        if check_bookkeeper_gambit(normalspell, currentstack, gameobj):
            setconnectionsstate("Cast", gameobj, staffcast)
            return

    if tocast is None or gameobj.spellerror:
        if ADDSPELLMODE and not gameobj.spellerror:
            newspell(gameobj.spells, normalspell, offset)
            gameobj.currentconnections = []
        else:
            print("there was an error or it was a wrong spell :<")
            setconnectionsstate("Error", gameobj, staffcast)
    else:
        setconnectionsstate("Cast", gameobj, staffcast)

        

def connectionexists(currentconnections, castspells, startpoint, endpoint):
    for connection in currentconnections:
        if (    connection.startpoint == startpoint and connection.endpoint == endpoint 
                or connection.endpoint == startpoint and connection.startpoint == endpoint
            ):
            return connection
    for spell in castspells:
        for connection in spell:
            if (    connection.startpoint == startpoint and connection.endpoint == endpoint 
                    or connection.endpoint == startpoint and connection.startpoint == endpoint
                ):
                return connection

def pointhasconnection(currentconnections, castspells, point):
    for connection in currentconnections:
        if (    connection.startpoint == point 
                or connection.endpoint == point
            ):
            return True
    for spell in castspells:
        for connection in spell:
            if (    connection.startpoint == point
                    or connection.endpoint == point
                ):
                return True
    return False


def generatepoints():
    points = []
    y = 0
    while Game.pointdistance/2+y*math.sqrt(Game.pointdistance**2-(Game.pointdistance/2)**2) < Game.height:
        x = 0
        if y%2 == 0:
            while Game.pointdistance/2+Game.pointdistance*x < Game.width:
                points.append(Point(y, x))
                x += 1
        else:
            while Game.pointdistance*(x+1) < Game.width:
                points.append(Point(y, x))
                x += 1
        y += 1
    return points

def getpoints(points, row, column):
    for point in points:
        if point.row == row and point.column == column:
            return Point
    return None

def gethoveredpoint(points, mousex, mousey):
    for point in points:
        if math.sqrt((point.xpos - mousex)**2 + (point.ypos - mousey)**2) < Game.pointdistance*0.4:
            return point

def pointsadjacent(point1, point2):
    x1 = point1.column
    y1 = point1.row
    x2 = point2.column
    y2 = point2.row
    if abs(y1 - y2) == 1: #above to each other
        if (    y1%2 == 0 and x1 - x2 == 1
                or y1%2 == 1 and x1 - x2 == -1
                or x1 == x2
            ):
            return True
    elif y1 == y2 and abs(x1 - x2) == 1:
            return True
    return False

def isbacktrack(connections, currentpoint, newpoint):
        if len(connections) == 0:
            return False
        lastconnect = connections[-1]
        if lastconnect.startpoint == newpoint and lastconnect.endpoint == currentpoint:
            return True
    
class Point:
    def __init__(self, row, column):
        self.position = (column, row)
        self.row = row
        self.column = column
        self.xpos = Game.pointdistance/4+Game.pointdistance*column if row%2== 0 else Game.pointdistance*3/4+Game.pointdistance*column
        self.ypos = Game.pointdistance/4+row*math.sqrt(Game.pointdistance**2-(Game.pointdistance/2)**2)

    def draw(self, surface):
        mousex, mousey = pygame.mouse.get_pos()
        distance = math.sqrt((self.xpos - mousex)**2 + (self.ypos - mousey)**2)
        circlesize = math.floor(7-distance/60)
        if circlesize > 0:
            pygame.draw.circle(surface, CIRCLECOLOR, [self.xpos, self.ypos], circlesize)


class Connection:
    def __init__(self, startpoint, endpoint):
        self.startpoint = startpoint
        self.endpoint = endpoint
        self.startpos = self.startx, self.starty = startpoint.xpos, startpoint.ypos
        self.endpos = self.endx, self.endy = endpoint.xpos, endpoint.ypos
        self.state = "Drawing"
        self.direction = 0
        strow = startpoint.row
        stcol = startpoint.column
        enrow = endpoint.row
        encol = endpoint.column
        if strow == enrow:
            if encol - stcol == 1:
                self.direction = 0
            else:
                self.direction = 3
        elif strow%2 == 0:
            if enrow > strow:
                if encol == stcol:
                    self.direction = 1
                else:
                    self.direction = 2
            else:
                if encol == stcol:
                    self.direction = 5
                else:
                    self.direction = 4
        else:
            if enrow > strow:
                if encol == stcol:
                    self.direction = 2
                else:
                    self.direction = 1
            else:
                if encol == stcol:
                    self.direction = 4
                else:
                    self.direction = 5

    def draw(self, surface, length, index):
        if self.state == "Drawing":
            color = LINEDRAWCOLOR
        elif self.state == "Cast":
            color = LINECASTCOLOR
        elif self.state == "Error":
            color = LINEERRORCOLOR
        elif self.state == "Considered":
            color = LINECONSIDEREDCOLOR
        else:
            color = (150, 150, 150)
        if Game.directionrender:
            color = tuple([value*(1-index/length)+(255*0.75+value*0.25)*(index/length) for value in color])
        pygame.draw.line(surface, color, self.startpos, self.endpos, width=LINEWIDTH) 
        if Game.directionrender:
            drawnumber = math.floor(Game.time/5e+8)%min(length, 8)
            if drawnumber == index%8:
                portion = Game.time/5e+8%1
                blinkpos = (self.endx*portion+self.startx*(1-portion), self.endy*portion+self.starty*(1-portion))
                pygame.draw.circle(surface, (255, 255, 255), blinkpos, LINEWIDTH) 

            

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
 
    def on_init(self):
        pygame.init()
        if ADDSPELLMODE:
            self._display_surf = pygame.display.set_mode((600,400))
        else:
            self._display_surf = pygame.display.set_mode((0,0))
        self.size = self.width, self.height = self._display_surf.get_size()
        self._running = True
        self.stacksurf = pygame.Surface((self.width*0.2, self.height-64), pygame.SRCALPHA)
        self.font = pygame.font.Font('font.ttf', 40)
        self.state = "Idle"
        self.pointdistance = self.height//16
        self.points: list[Point]  = generatepoints()
        self.currentpoint = None
        self.currentconnections: list[Connection] = []
        self.castspells: list[list[Connection]] = []
        print("loading spells")
        with open("spells.json", "r") as f:
            self.spells = json.load(f)
        checkspells(self.spells)
        self.starttime = time.time_ns()
        self.time = 0
        self.currentstack = []
        self.spellerror = False
        self.directionrender = False
        self.consideration = False
        self.introspectionlevel = 0
        self.introspectionlist = []
        self.levelinputs = []
        self.leveloutputs = []
        self.expectedoutputs = []
        self.writtenspell = []
        self.ravenmind = []
        self.executiondepth = 0
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
            with open("spells.json", "w") as f:
                f.write(json.dumps(self.spells, indent=4))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            if event.button == 1 and self.state == "Idle" and gethoveredpoint(self.points, mousex, mousey):
                self.state = "Casting"
                self.currentpoint = gethoveredpoint(self.points, mousex, mousey)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.spellerror = False
            if event.button == 1 and self.state == "Casting":
                currentspell = []
                for connection in self.currentconnections:
                    if connection.state == "Drawing":
                        currentspell.append(connection.direction)
                if len(currentspell) > 0:
                    self.writtenspell.append(currentspell)
                    executespell(currentspell, self.currentstack, self) 
                self.state = "Idle"

        elif event.type == pygame.MOUSEMOTION:
            mousex, mousey = event.pos
            if self.state == "Casting":
                newpoint = gethoveredpoint(self.points, mousex, mousey)
                if newpoint != self.currentpoint and newpoint != None:
                    if pointsadjacent(self.currentpoint, newpoint):
                        if isbacktrack(self.currentconnections, self.currentpoint, newpoint):
                            self.currentconnections.pop()
                            self.currentpoint = newpoint
                        elif not connectionexists(self.currentconnections, self.castspells, self.currentpoint, newpoint):
                            self.currentconnections.append(Connection(self.currentpoint, newpoint))
                            self.currentpoint = newpoint

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                self.directionrender = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                self.directionrender = False

                

            
    def on_loop(self):
        self.time = time.time_ns() - self.starttime
    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        mousex, mousey = pygame.mouse.get_pos()
        if self.currentpoint != None and self.state == "Casting":
            pygame.draw.line(self._display_surf, LINEDRAWCOLOR, (self.currentpoint.xpos, self.currentpoint.ypos), (mousex, mousey), width=7)
        
        for point in self.points:
            point.draw(self._display_surf)

        for i, connection in enumerate(self.currentconnections):
            connection.draw(self._display_surf, len(self.currentconnections), i)
        for spell in self.castspells:
            for i, connection in enumerate(spell):
                connection.draw(self._display_surf, len(spell), i)
        if len(self.currentstack) > 0:
               drawstack(self.currentstack, self._display_surf, self.stacksurf)
        pygame.display.flip()
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__" :
    Game = App()
    Game.on_execute()
    

