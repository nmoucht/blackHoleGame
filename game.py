import pygame    
import time
import random

class gameObject:
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    x1 = 300
    y1 = 300

    dis_width = 800
    dis_height = 600
    dis = pygame.display.set_mode((dis_width, dis_height))
    game_over = False
    clock = pygame.time.Clock()

    shipPic = ""
    shipPosition = ""
    blackHolePic = ""
    blackHolePosition = ""
    blackHolexRate = 2
    blackHoleyRate = 2

    numPlanets = 10
    numPlanetsGot = 0

    planetList = []
    planetPosition = []
    planetVelocity = []

    sky = pygame.image.load("sky.jpg")

    def initGame(self):
        pygame.init()
        pygame.display.set_caption('Escape the black hole')
        self.dis.blit(self.sky, self.sky.get_rect())
        self.initShip()
        self.initBlackHole()
        self.initPlanets()

    def initShip(self):
        self.shipPic = pygame.image.load("ship.png")
        self.shipPic = pygame.transform.scale(self.shipPic, (int(342/5), int(598/5)))#342,598
        self.shipPosition = self.shipPic.get_rect()
        self.shipPosition.x = 300
        self.shipPosition.y = 300

    def initBlackHole(self):
        self.blackHolePic = pygame.image.load("bhole.png")
        self.blackHolePic = pygame.transform.scale(self.blackHolePic, (int(1000/5), int(1080/5)))#1000,1080
        self.blackHolePosition = self.blackHolePic.get_rect()
        self.blackHolePosition.x = 50
        self.blackHolePosition.y = 50
    
    def initPlanets(self):
        planetPic = pygame.image.load("earth.png")
        planetPic = pygame.transform.scale(planetPic, (int(2579/70), int(2563/70)))
        for i in range(0, self.numPlanets):
            #250,226
            planetPosition = planetPic.get_rect()
            while(planetPosition.colliderect(self.shipPosition) or planetPosition.colliderect(self.blackHolePosition) or self.checkCollideWithOtherPlanets(planetPosition)):
                planetPosition.x = random.randint(0,self.dis_width-int(250/5))
                planetPosition.y = random.randint(0,self.dis_height - int(226/5))
            self.planetPosition.append(planetPosition)
            self.planetList.append(planetPic)
            self.planetVelocity.append([0,0])
    
    def checkCollideWithOtherPlanets(self, pos):
        for elt in self.planetPosition:
            if(elt.colliderect(pos)):
                return True
        return False

    def updateShip(self,x,y):
        self.shipPosition.x += x
        self.shipPosition.y += y

    def updateBlackHole(self):
        self.blackHolePosition.x += self.blackHolexRate
        self.blackHolePosition.y += self.blackHoleyRate
        if(self.isOutsideBounds(self.blackHolePosition)):
            self.updateBlackHoleRate()
    
    def updateBlackHoleRate(self):
        if self.isPosOutsideBounds(self.blackHolePosition.x, self.dis_width, self.blackHolePosition.width):
            self.blackHolexRate *=-1
        if self.isPosOutsideBounds(self.blackHolePosition.y, self.dis_height, self.blackHolePosition.height):
            self.blackHoleyRate *=-1

    def updatePlanet(self, planet):
        self.planetPosition[planet].x += self.planetVelocity[planet][0]
        self.planetPosition[planet].y += self.planetVelocity[planet][1]
        self.planetVelocity[planet][1] /= 2
        self.planetVelocity[planet][0] /= 2

    def isOutsideBounds(self, obj):
        if self.isPosOutsideBounds(obj.x, self.dis_width, obj.width) or self.isPosOutsideBounds(obj.y, self.dis_height, obj.height):
            return True
        return False
    
    def isPosOutsideBounds(self, pos, bound, adder):
        if pos+adder >= bound or pos < 0:
            return True
        return False

    def checkGameOver(self):
        if(self.isOutsideBounds(self.shipPosition) or self.shipPosition.colliderect(self.blackHolePosition) or self.numPlanets <=5):
            self.exitGame("You Lost.", self.red)

        if(self.numPlanets == self.numPlanetsGot):
            self.exitGame("You Won!", self.green)

    def renderGame(self):
        self.updateBlackHole()
        
        # self.dis.fill(self.sky)
        self.dis.blit(self.sky, self.sky.get_rect())
        self.dis.blit(self.shipPic, self.shipPosition)
        self.dis.blit(self.blackHolePic, self.blackHolePosition)
        got_planets = []
        for i in range(0,len(self.planetPosition)):
            if(self.planetPosition[i].colliderect(self.blackHolePosition)):
                self.planetVelocity[i] = [2,2]
            self.updatePlanet(i)
            if(self.shipPosition.colliderect(self.planetPosition[i])):
                got_planets.append(i)
                self.numPlanetsGot += 1
                continue
            if(self.isOutsideBounds(self.planetPosition[i])):
                got_planets.append(i)
                self.numPlanets -= 1
            self.dis.blit(self.planetList[i], self.planetPosition[i])


        for elt in got_planets:
            del self.planetPosition[elt]
            del self.planetList[elt]
        font_style = pygame.font.SysFont(None, 20)
        mesg = font_style.render(str(self.numPlanetsGot) +"/"+str(self.numPlanets)+" planets", True, self.white)
        self.dis.blit(mesg, [self.dis_width-80, 10])  
        pygame.display.update()
        self.clock.tick(30)

    def exitGame(self, message, color):
        font_style = pygame.font.SysFont(None, 50)
        mesg = font_style.render(message, True, color)
        self.dis.blit(mesg, [self.dis_width/2, self.dis_height/2])
        pygame.display.update()
        # time.sleep(2)
        pygame.quit()
        quit()

go = gameObject()

def main():

    x1_change = 0       
    y1_change = 0
    
    go.initGame()
    
    while not go.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                go.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -5
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = 5
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -5
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = 5
                    x1_change = 0
        
        go.updateShip(x1_change, y1_change)
        go.renderGame()
        go.checkGameOver()
 
    go.exitGame()

if __name__ == '__main__':
    main()