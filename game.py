print("loading please wait")
import pygame
import random
import os
pygame.init()
screenWidth = 500
screenHeight = 500
unitW= screenWidth/5
color_x = (205,77,157)
color_o = (0,191,255) 
unitH= screenHeight/5
window=pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption("tic-tac-toe")
run = True
# bgimg = pygame.image.load("")

base_path = os.path.dirname(__file__)
pic_path = os.path.join(base_path, "bg.png")
bgimg = pygame.image.load(pic_path)


slots = []
moves = []
chance = "player"
time = 0
winner = ""
strike = []
for i in range(3):
    for j in range(3):
        slots.append([i+1,j+1])
def draw():
    window.blit(bgimg,(0,0))
    #mx,my = pygame.mouse.get_pos()
    #pygame.draw.line(window,(0,255,0),(0,0),(x,y),4)
    pygame.draw.line(window,(0,0,0),(2*unitW,unitH),(2*unitW,screenHeight-unitH),1)
    pygame.draw.line(window,(0,0,0),(3*unitW,unitH),(3*unitW,screenHeight-unitH),1)
    pygame.draw.line(window,(0,0,0),(unitW,2*unitH),(screenWidth-unitW,2*unitH),1)
    pygame.draw.line(window,(0,0,0),(unitW,3*unitH),(screenWidth-unitW,3*unitH),1)
    if([rx,ry] in slots):
        tempx = (rx-1)*unitW+unitW
        tempy = (ry-1)*unitH+unitH
        pygame.draw.rect(window,(0,0,150),(tempx,tempy,unitW,unitH))
    font = pygame.font.SysFont("comicsans",150,False,False)
    for i in moves:
        tempx = (i[0]-1)*unitW+unitW
        tempy = (i[1]-1)*unitH+unitH
        text = font.render(i[2],True,i[3])
        window.blit(text,(tempx+unitW*(0.2),tempy))
    #pygame.draw.line(window,(0,0,0),(),(),4)
    pygame.display.update()
def turn(rx,ry,string,color):
    moves.append([rx,ry,string,color])
    slots.remove([rx,ry])
def won():
    global winner
    global strike
    for i in range(1,4):
        countx=0
        counto=0
        for j in range(1,4):
            if([i,j,"x",color_x] in moves):
                countx+=1
            elif([i,j,"o",color_o] in moves):
                counto+=1
        if(countx==3 or counto==3):
            if(countx==3):
                winner = "x"
            else:
                winner = "o"
            strike = [[i,1],[i,3]]
            return True
    for i in range(1,4):
        countx=0
        counto=0
        for j in range(1,4):
            if([j,i,"x",color_x] in moves):
                countx+=1
            elif([j,i,"o",color_o] in moves):
                counto+=1
        if(countx==3 or counto==3):
            if(countx==3):
                winner = "x"
            else:
                winner = "o"
            strike = [[1,i],[3,i]]
            return True
    countx=0
    counto=0
    for i in range(1,4):
        if([i,i,"x",color_x] in moves):
            countx+=1
        elif([i,i,"o",color_o] in moves):
            counto+=1
    if(countx==3 or counto==3):
        if(countx==3):
            winner = "x"
        else:
            winner = "o"
        strike = [[1,1],[3,3]]
        return True
    countx=0
    counto=0
    for i in range(1,4):
        if([i,4-i,"x",color_x] in moves):
            countx+=1
        elif([i,4-i,"o",color_o] in moves):
            counto+=1
    if(countx==3 or counto==3):
        if(countx==3):
            winner = "x"
        else:
            winner = "o"
        strike = [[1,3],[3,1]]
        return True
    return False
def strike_winner():
    fx,fy,sx,sy = strike[0][0],strike[0][1],strike[1][0],strike[1][1]
    fx,fy,sx,sy = fx*unitW,fy*unitH,sx*unitW,sy*unitH 
    fx,fy,sx,sy = fx+unitW/2,fy+unitH/2,sx+unitW/2,sy+unitH/2
    pygame.draw.line(window,(255,255,255),(fx,fy),(sx,sy),7)
    pygame.display.update()
while(run):
    pygame.time.delay(20)
    for events in pygame.event.get():
        if(events.type==pygame.QUIT):
            run=False
    keys = pygame.key.get_pressed()
    buttons = pygame.mouse.get_pressed()
    rx,ry = pygame.mouse.get_pos()
    rx,ry = rx//unitW,ry//unitH
    if(keys[pygame.K_q]):
        run=False
    if(won()):
        strike_winner()
        pygame.time.delay(10000)
        run=False
        break
    else:
        if(buttons[0] and chance=="player"):
            if(1<=rx<=3 and 1<=ry<=3 and [rx,ry] in slots):
                turn(rx,ry,"x",color_x)
                chance="computer"
                time = 50
        if(chance=="computer" and len(slots)!=0 and time==0):
            r = random.randint(0,len(slots)-1)
            r = slots[r]
            print(r[0],r[1])
            turn(r[0],r[1],"o",color_o)
            chance="player"
    time = max(0,time-1)
    draw()
pygame.quit()
