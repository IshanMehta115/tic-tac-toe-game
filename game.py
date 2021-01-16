import pygame
import os
import random
pygame.init()
screenWidth=500
screenHeight=500
unitLength = 500/5
strike_width=6
line_width=6
window = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption("Tic-Tac-Toe")

base_path = os.path.dirname(__file__)
bg_img = pygame.image.load(os.path.join(base_path,"bg.png"))

game_name_font = pygame.font.SysFont("comicsans",100,False,False)
button_font = pygame.font.SysFont("comicsans",50,False,False)
marker_font = pygame.font.SysFont('comicsans',30,True,False)

game_name = "Tic-Tac-Toe"
game_name_text = ''
play_game = "Play Game"
exit_game = "Exit Game"

buttons = []
button_number = 2
buttonWidth=200
buttonHeight=50
buttonGap=buttonHeight+30

game_grid = []
turn = 'player'
time=0

number=0
dir=''
won=False
strike_fraction = 0

screen_selected='main menu'

class button:
    def __init__(self,text,normal_text_color,glow_text_color,text_font,mode):
        self.text = text
        self.normal_text_color = normal_text_color
        self.glow_text_color = glow_text_color
        self.text_font = text_font
        self.mode = mode
    def set_rect(self,rect):
        self.rect = rect
    def display(self):
        if(self.mode=='normal'):
            display_text = self.text_font.render(self.text,True,pygame.Color(self.normal_text_color))
            window.blit(display_text,(self.rect.x+self.rect.width/2 - display_text.get_width()/2,self.rect.y+self.rect.height/2 - display_text.get_height()/2))
        elif(self.mode=='glow'):
            display_text = self.text_font.render(self.text,True,pygame.Color(self.glow_text_color))
            window.blit(display_text,(self.rect.x+self.rect.width/2 - display_text.get_width()/2,self.rect.y+self.rect.height/2 - display_text.get_height()/2))
    def set_mode(self,new_mode):
        self.mode = new_mode

def set_main_menu():
    global game_name_text
    game_name_text = game_name_font.render(game_name,True,pygame.Color('DarkBlue'))
    

    buttons.append(button(play_game,'DarkBlue','White',button_font,'normal'))
    buttons.append(button(exit_game,'DarkBlue','White',button_font,'normal'))
    for i in range(button_number):
        buttons[i].set_rect(pygame.Rect(screenWidth/2-buttonWidth/2,200+i*buttonGap,buttonWidth,buttonHeight))

        
def check_hovering():
    mouseX,mouseY = pygame.mouse.get_pos()
    for i in buttons:
        if (i.rect.x <= mouseX <= i.rect.x+i.rect.width) and (i.rect.y <= mouseY <= i.rect.y+i.rect.height):
            i.set_mode('glow')
        else:
            i.set_mode('normal')

def show_main_menu():
    window.blit(game_name_text,(screenWidth/2-game_name_text.get_width()/2,30))
    for i in range(button_number):
        buttons[i].display()

def check_click():
    global screen_selected
    mouse_button1, mouse_button2, mouse_button3 = pygame.mouse.get_pressed(3)
    mouseX,mouseY = pygame.mouse.get_pos()
    if(not mouse_button1):
        return
    for i in buttons:
        if (i.rect.x <= mouseX <= i.rect.x+i.rect.width) and (i.rect.y <= mouseY <= i.rect.y+i.rect.height):
            screen_selected=i.text

def check_position(r,c):
    for i in game_grid:
        if i[0]==r and i[1]==c:
            return False
    return True
def strike(a,b):
    global strike_fraction
    if(b=='row'):
        pygame.draw.line(window,(255,255,255),(unitLength+unitLength/5,a*unitLength+unitLength/2),(unitLength+unitLength/5+strike_fraction*(3*unitLength-2*unitLength/5),(a*unitLength+unitLength/2)),strike_width)
    if(b=='col'):
        pygame.draw.line(window,(255,255,255),(a*unitLength+unitLength/2,unitLength+unitLength/5),(a*unitLength+unitLength/2,unitLength+unitLength/5+strike_fraction*(3*unitLength-2*unitLength/5)),strike_width)
    if(b=='dia' and a==1):
        pygame.draw.line(window,(255,255,255),(unitLength+unitLength/5,unitLength+unitLength/5),(unitLength+unitLength/5+strike_fraction*(3*unitLength-2*unitLength/5),unitLength+unitLength/5+strike_fraction*(3*unitLength-2*unitLength/5),strike_width))
    if(b=='dia' and a==2):
         pygame.draw.line(window,(255,255,255),(unitLength+unitLength/5,3*unitLength+unitLength-unitLength/5),(unitLength+unitLength/5+strike_fraction*(3*unitLength-2*unitLength/5),3*unitLength+unitLength-unitLength/5-strike_fraction*(3*unitLength-2*unitLength/5)),strike_width)

    strike_fraction+=0.0625


def check_win():
    for i in range(1,4):
        this_row_player=0
        this_row_computer=0
        for g in game_grid:
            if(g[0]==i):
                if g[2]=='X':
                    this_row_player+=1
                elif g[2]=='O':
                    this_row_computer+=1
        if this_row_player==3 or this_row_computer==3:
            return i,'col',True
    
    for j in range(1,4):
        this_col_player = 0
        this_col_computer=0
        for g in game_grid:
            if(g[1]==j):
                if g[2]=='X':
                    this_col_player+=1
                elif g[2]=='O':
                    this_col_computer+=1
        if this_col_computer==3 or this_col_player==3:
            return j,'row',True
    
    temp_player = 0
    temp_computer = 0
    for g in game_grid:
        if(g[0]==g[1]):
            if g[2]=='X':
                temp_player+=1
            elif g[2]=='O':
                temp_computer+=1
    if temp_player==3 or temp_computer==3:
        return 1,'dia',True

    temp_player = 0
    temp_computer = 0
    for g in game_grid:
        if g[0]+g[1]==4:
            if g[2]=='X':
                temp_player+=1
            elif g[2]=='O':
                temp_computer+=1
    if temp_player==3 or temp_computer==3:
        return 2,'dia',True
    return 0,'',False
        

def main_loop():
    run = True
    game_ready=False
    global turn,time,screen_selected,number,dir,won
    while(run):
        pygame.time.delay(50)
        time = max(-1,time-100)
        for events in pygame.event.get():
            if(events.type==pygame.QUIT):
                run=False
        if(screen_selected=='Exit Game'):
            run = False
        elif(screen_selected=='Play Game'):
            if game_ready:
                window.blit(bg_img,(0,0))
                pygame.draw.line(window,(0,0,0),(2*unitLength,unitLength),(2*unitLength,screenHeight-unitLength),line_width)
                pygame.draw.line(window,(0,0,0),(3*unitLength,unitLength),(3*unitLength,screenHeight-unitLength),line_width)
                pygame.draw.line(window,(0,0,0),(unitLength,2*unitLength),(screenWidth-unitLength,2*unitLength),line_width)
                pygame.draw.line(window,(0,0,0),(unitLength,3*unitLength),(screenWidth-unitLength,3*unitLength),line_width)

                mousex,mousey = pygame.mouse.get_pos()
                mousex = mousex//unitLength
                mousey = mousey//unitLength

                mouseBtn1,mouseBtn2,mouseBtn3 = pygame.mouse.get_pressed()

                if(turn=='player'):
                    if(1<=mousex<=3 and 1<=mousey<=3):
                        if(check_position(mousex,mousey)):
                            if(mouseBtn1):
                                game_grid.append((mousex,mousey,'X'))
                                turn='computer'
                                time = 1000
                            else:
                                gap = 10
                                pygame.draw.rect(window,(179, 179, 255),(unitLength*mousex+gap,unitLength*mousey+gap,unitLength-2*gap,unitLength-2*gap))
                elif(turn=='computer' and len(game_grid)<9 and time<0):
                    mousex=random.randint(1,3)
                    mousey=random.randint(1,3)
                    while(not check_position(mousex,mousey)):
                        mousex=random.randint(1,3)
                        mousey=random.randint(1,3)
                    game_grid.append((mousex,mousey,'O'))
                    turn='player'
                for i in game_grid:
                    text = game_name_font.render(i[2],True,pygame.Color('DarkBlue'))
                    window.blit(text,(unitLength*i[0]+unitLength/2-text.get_width()/2,unitLength*i[1]+unitLength/2-text.get_height()/2))
                pygame.display.update()
                number,dir,won = check_win()
                if(won):
                    screen_selected='won'
                    pygame.time.delay(500)
            else:
                mouseBtn1,mouseBtn2,mouseBtn3 = pygame.mouse.get_pressed()
                if(not mouseBtn1):
                    game_ready=True
        elif(screen_selected=='main menu'):
            check_click()
            check_hovering()
            window.blit(bg_img,(0,0))
            show_main_menu()
            pygame.display.update()
        elif(screen_selected=='won'):
            print("won section")
            window.blit(bg_img,(0,0))
            pygame.draw.line(window,(0,0,0),(2*unitLength,unitLength),(2*unitLength,screenHeight-unitLength),line_width)
            pygame.draw.line(window,(0,0,0),(3*unitLength,unitLength),(3*unitLength,screenHeight-unitLength),line_width)
            pygame.draw.line(window,(0,0,0),(unitLength,2*unitLength),(screenWidth-unitLength,2*unitLength),line_width)
            pygame.draw.line(window,(0,0,0),(unitLength,3*unitLength),(screenWidth-unitLength,3*unitLength),line_width)
            for i in game_grid:
                    text = game_name_font.render(i[2],True,pygame.Color('DarkBlue'))
                    window.blit(text,(unitLength*i[0]+unitLength/2-text.get_width()/2,unitLength*i[1]+unitLength/2-text.get_height()/2))
            strike(number,dir)
            pygame.display.update()
            if(strike_fraction>1):
                pygame.time.delay(1000)
                run=False

set_main_menu()
main_loop()
