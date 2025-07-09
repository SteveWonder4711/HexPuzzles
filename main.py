import pygame
from pygame.locals import *
import math
import json
import spells
import random


CIRCLECOLOR = (100, 100, 255)
LINEDRAWCOLOR = (204, 115, 255)
LINECASTCOLOR = (66, 224, 245)
LINEERRORCOLOR = (255, 0, 0)
LINECONSIDEREDCOLOR = (245, 245, 66)
LINEWIDTH = 7
ADDSPELLMODE = False


def checkspells(spells):
    for spell in spells:
        if not "offset" in spells[spell]:
            print("spell without offset")
        if not "description" in spells[spell]:
            print(f"spell {spells[spell]["name"]} has no description given")
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
    newstack = currentstack[:-len(bookkeeper)]
    affected = currentstack[-len(bookkeeper):]
    for i in range(len(bookkeeper)):
        if bookkeeper[i] == 1:
            newstack.append(affected[i])
    gameobj.currentstack = newstack 
    return True

def iotatostring(iota):
    if type(iota) in [int,float,bool]:
        return str(iota)
    elif type(iota) == tuple: 
        return "({}, {}, {})".format(*[math.floor(element*1000)/1000 for element in list(iota)])
    elif type(iota) == list:
        string = "["
        for i in range(len(iota)):
            string += iotatostring(iota[i])
            if i != len(iota)-1:
                string += ", "
        string += "]"
        return string
    elif type(iota) == str:
        #strings are used for patterns and other internal types
        if iota == "ERROR":
            return "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!§$%&/()=?\\ß*+-#'_.:,;", k=20))
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
        string = iotatostring(currentstack[i])
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

def setconnectionsstate(state, gameobj):
    for connection in gameobj.connections:
            if connection.state == "Drawing":
                connection.state = state


def executespell(currentspell, currentstack, gameobj):
    gameobj.spellerror = False
    offset = currentspell[0]
    normalspell = [(direction-offset)%6 for direction in currentspell]
    if gameobj.consideration:
        if gameobj.introspectionlevel > 0:
            gameobj.introspectionlist.append(f"<{"".join([str(direction) for direction in currentspell])}>")
        else:
            currentstack.append(f"<{"".join([str(direction) for direction in currentspell])}>")
        gameobj.consideration = False
        setconnectionsstate("Considered", gameobj)
        return
    tocast = None
    for spell in gameobj.spells:
        if gameobj.spells[spell]["directions"] == normalspell:
            tocast = spell
    #Certain spells which need Game Object
    if tocast == "consideration":
        gameobj.consideration = True
        setconnectionsstate("Cast", gameobj)
        return
    elif tocast == "evanition":
        if len(gameobj.introspectionlist) > 0:
            gameobj.introspectionlist.pop()
            setconnectionsstate("Considered", gameobj)
            return
    elif tocast == "introspection":
        if gameobj.introspectionlevel > 0:
            gameobj.introspectionlist.append(f"<{''.join([str(direction) for direction in currentspell])}>")
            setconnectionsstate("Considered", gameobj)
        else:
            setconnectionsstate("Cast", gameobj)
        gameobj.introspectionlevel += 1
        return
    elif tocast == "retrospection":
        gameobj.introspectionlevel -= 1
        if gameobj.introspectionlevel > 0:
            gameobj.introspectionlist.append(f"<{''.join([str(direction) for direction in currentspell])}>")
            setconnectionsstate("Considered", gameobj) 
        else:
            currentstack.append(gameobj.introspectionlist)
            gameobj.introspectionlist = []
            setconnectionsstate("Cast", gameobj)
        return
    elif gameobj.introspectionlevel > 0:
        gameobj.introspectionlist.append(f"<{''.join([str(direction) for direction in currentspell])}>")
        setconnectionsstate("Considered", gameobj)
        return
    elif tocast is not None: 
        spellfunction = getattr(spells, tocast)
        spellfunction(currentstack, gameobj)
    else:
        if check_numerical_reflection(normalspell, currentstack):
            setconnectionsstate("Cast", gameobj)
            return
        if check_bookkeeper_gambit(normalspell, currentstack, gameobj):
            setconnectionsstate("Cast", gameobj)
            return

    if tocast is None or gameobj.spellerror:
        if ADDSPELLMODE and not gameobj.spellerror:
            newspell(gameobj.spells, normalspell, offset)
            gameobj.connections = []
        else:
            print("there was an error or it was a wrong spell :<")
            setconnectionsstate("Error", gameobj)
    else:
        setconnectionsstate("Cast", gameobj)      

    

def connectionexists(connections, startpoint, endpoint):
        for connection in connections:
            if (    connection.startpoint == startpoint and connection.endpoint == endpoint 
                 or connection.endpoint == startpoint and connection.startpoint == endpoint
               ):
                return connection



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
        circlesize = math.floor(7-distance/40)
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

    def draw(self, surface):
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
        pygame.draw.line(surface, color, self.startpos, self.endpos, width=LINEWIDTH) 


        

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
        self.font = pygame.font.Font('font.ttf', 32)
        self.state = "Idle"
        self.pointdistance = self.height//16
        self.points: list[Point]  = generatepoints()
        self.currentpoint = None
        self.connections: list[Connection] = []
        print("loading spells")
        with open("spells.json", "r") as f:
            self.spells = json.load(f)
        #checkspells(self.spells)
        self.currentstack = []
        self.spellerror = False
        self.consideration = False
        self.introspectionlevel = 0
        self.introspectionlist = []
        self.levelinputs = []
        self.leveloutputs = []
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
                for connection in self.connections:
                    if connection.state == "Drawing":
                        currentspell.append(connection.direction)
                if len(currentspell) > 0:
                   executespell(currentspell, self.currentstack, self) 
                self.state = "Idle"

        elif event.type == pygame.MOUSEMOTION:
            mousex, mousey = event.pos
            if self.state == "Casting":
                newpoint = gethoveredpoint(self.points, mousex, mousey)
                if newpoint != self.currentpoint and newpoint != None:
                    if pointsadjacent(self.currentpoint, newpoint):
                        if isbacktrack(self.connections, self.currentpoint, newpoint):
                            self.connections.pop()
                            self.currentpoint = newpoint
                        elif not connectionexists(self.connections, self.currentpoint, newpoint):
                            self.connections.append(Connection(self.currentpoint, newpoint))
                            self.currentpoint = newpoint

                

            
    def on_loop(self):
        pass
    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        mousex, mousey = pygame.mouse.get_pos()
        if self.currentpoint != None and self.state == "Casting":
            pygame.draw.line(self._display_surf, LINEDRAWCOLOR, (self.currentpoint.xpos, self.currentpoint.ypos), (mousex, mousey), width=7)
        
        for point in self.points:
            point.draw(self._display_surf)
        for connection in self.connections:
            connection.draw(self._display_surf)
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
    

