import pygame    

class gameObject:
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    x1 = 300
    y1 = 300

    dis_width = 800
    dis_height = 600
    dis = pygame.display.set_mode((dis_width, dis_height))
    game_over = False
    shipPic = ""
    shipPosition = ""
    clock = pygame.time.Clock()

    def initGame(self):
        pygame.init()
        pygame.display.set_caption('Escape the black hole')
        self.initShip()

    def initShip(self):
        self.shipPic = pygame.image.load("ship.png")
        self.shipPic = pygame.transform.scale(self.shipPic, (int(342/5), int(598/5)))#342,598
        self.shipPosition = self.shipPic.get_rect()
        self.shipPosition.x = 300
        self.shipPosition.y = 300

    def updateShip(self,x,y):
        self.shipPosition.x += x
        self.shipPosition.y += y

    def checkGameOver(self):
        if self.shipPosition.x >= self.dis_width or self.shipPosition.x < 0 or self.shipPosition.y >= self.dis_height or self.shipPosition.y < 0:
            self.exitGame()

    def renderGame(self):
        self.dis.fill(self.white)
        self.dis.blit(self.shipPic, self.shipPosition)
        # pygame.display.flip()
    
        pygame.display.update()
        self.clock.tick(30)

    def exitGame(self):
        font_style = pygame.font.SysFont(None, 50)
        mesg = font_style.render("you lost", True, self.black)
        self.dis.blit(mesg, [self.dis_width/2, self.dis_height/2])
        pygame.display.update()
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
                    x1_change = -10
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = 10
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -10
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = 10
                    x1_change = 0
        
        go.updateShip(x1_change, y1_change)
        go.checkGameOver()
        go.renderGame()
 
    go.exitGame()

if __name__ == '__main__':
    main()