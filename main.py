import pygame
from pygame.locals import *
import math
import json
import os
import spells


CIRCLECOLOR = (100, 100, 255)
LINEDRAWCOLOR = (204, 115, 255)
LINECASTCOLOR = (66, 224, 245)
LINEERRORCOLOR = (255, 0, 0)
LINEWIDTH = 7
ADDSPELLMODE = True


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


def check_bookkeeper_gambit(directions, currentstack):
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
        Game.spellerror = True
        return True
    newstack = currentstack[:-len(bookkeeper)]
    affected = currentstack[-len(bookkeeper):]
    for i in range(len(bookkeeper)):
        if bookkeeper[i] == 1:
            newstack.append(affected[i])
    Game.currentstack = newstack 
    return True


def drawstack(currentstack, gamesurface, stacksurface):
    dimensions = width, height = stacksurface.get_size()
    stacksurface.fill((0, 0, 0, 0))
    stacksurface.fill((0, 0, 0, 100))
    i = len(currentstack)-1
    while i >= 0 and i > len(currentstack)-20:
        if type(currentstack[i]) in [int,float]:
            string = str(currentstack[i])
        elif type(currentstack[i]) == tuple: 
            string = "({}, {}, {})".format(*["{:.3f}".format(element) if type(element) == float else element for element in list(currentstack[i])])
        text = Game.font.render(string, False, LINEDRAWCOLOR)
        textRect = text.get_rect()
        textRect.center = (min(textRect.width//2, width/2), textRect.height*(len(currentstack)-i-0.5))
        stacksurface.blit(text, textRect)
        i -= 1
    gamesurface.blit(stacksurface, (0, 0))



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
        f.write(f'#{spellname}\n#{description}\ndef {id}(currentstack):\n    pass\n\n\n')


def executespell(spellid, currentstack):
    spellfunction = getattr(spells, spellid)
    spellfunction(currentstack)



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

       
class Point:
    def __init__(self, row, column):
        self.position = (column, row)
        self.row = row
        self.column = column
        self.xpos = Game.pointdistance/4+Game.pointdistance*column if row%2== 0 else Game.pointdistance*3/4+Game.pointdistance*column
        self.ypos = Game.pointdistance/4+row*math.sqrt(Game.pointdistance**2-(Game.pointdistance/2)**2)

    def draw(self, surface):
        pygame.draw.circle(surface, CIRCLECOLOR, [self.xpos, self.ypos], 5)

    def get(points, row, column):
        for point in points:
            if point.row == row and point.column == column:
                return Point
        return None

    def gethovered(points, mousex, mousey):
        for point in points:
            if math.sqrt((point.xpos - mousex)**2 + (point.ypos - mousey)**2) < 20:
                return point

    def isadjacent(point1, point2):
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
        pygame.draw.line(surface, color, self.startpos, self.endpos, width=LINEWIDTH) 


    def exists(connections, startpoint, endpoint):
        for connection in connections:
            if (    connection.startpoint == startpoint and connection.endpoint == endpoint 
                 or connection.endpoint == startpoint and connection.startpoint == endpoint
               ):
                return connection

    def isbacktrack(connections, currentpoint, newpoint):
        if len(connections) == 0:
            return False
        lastconnect = connections[-1]
        if lastconnect.startpoint == newpoint and lastconnect.endpoint == currentpoint:
            return True


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((0,0))
        self.size = self.width, self.height = self._display_surf.get_size()
        self._running = True
        self.stacksurf = pygame.Surface((self.width*0.2, self.height), pygame.SRCALPHA)
        self.font = pygame.font.Font('font.ttf', 32)
        self.state = "Idle"
        self.pointdistance = self.height//11
        self.points = generatepoints()
        self.currentpoint = None
        self.connections = []
        print("loading spells")
        with open("spells.json", "r") as f:
            self.spells = json.load(f)
        self.currentstack = []
        self.spellerror = False
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
            with open("spells.json", "w") as f:
                f.write(json.dumps(self.spells, indent=4))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            if event.button == 1 and self.state == "Idle" and Point.gethovered(self.points, mousex, mousey):
                self.state = "Casting"
                self.currentpoint = Point.gethovered(self.points, mousex, mousey)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.spellerror = False
            if event.button == 1 and self.state == "Casting":
                currentspell = []
                for connection in self.connections:
                    if connection.state == "Drawing":
                        currentspell.append(connection.direction)
                if len(currentspell) > 0:
                    offset = currentspell[0]
                    currentspell = [(direction-offset)%6 for direction in currentspell]
                    validspell = True
                    if not check_numerical_reflection(currentspell, self.currentstack):
                        if not check_bookkeeper_gambit(currentspell, self.currentstack):
                            validspell = False
                            for spell in self.spells:
                                if self.spells[spell]["directions"] == currentspell:
                                    validspell = True
                                    executespell(spell, self.currentstack)
                    if not validspell or self.spellerror:
                        if ADDSPELLMODE and not self.spellerror:
                            newspell(self.spells, currentspell, offset)
                            self.connections = []
                        else:
                            print("there was an error or it was a wrong spell :<")
                            for connection in self.connections:
                                if connection.state == "Drawing":
                                    connection.state = "Error"
                    else:
                        for connection in self.connections:
                                if connection.state == "Drawing":
                                    connection.state = "Cast"      


                                
                self.state = "Idle"

        elif event.type == pygame.MOUSEMOTION:
            mousex, mousey = event.pos
            if self.state == "Casting":
                newpoint = Point.gethovered(self.points, mousex, mousey)
                if newpoint != self.currentpoint and newpoint != None:
                    if Point.isadjacent(self.currentpoint, newpoint):
                        if Connection.isbacktrack(self.connections, self.currentpoint, newpoint):
                            self.connections.pop()
                            self.currentpoint = newpoint
                        elif not Connection.exists(self.connections, self.currentpoint, newpoint):
                            self.connections.append(Connection(self.currentpoint, newpoint))
                            self.currentpoint = newpoint

                

            
    def on_loop(self):
        mousex, mousey = pygame.mouse.get_pos()
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
    

