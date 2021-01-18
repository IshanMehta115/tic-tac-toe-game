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
score_font = pygame.font.SysFont('comicsans',40,False,False)
end_game_font = pygame.font.SysFont('comicsans',60,False,False)

game_name = "Tic-Tac-Toe"
game_name_text = ''
options_text = ''
play_game = "Play Game"
exit_game = "Exit Game"
restart_game = "Restart Game"
back_to_main_menu = "Back to Main Menu"
human_player='X'
computer_player='Y'
human_score = 0
computer_score = 0

buttons = []
optionButtons = []
button_number = 3
buttonWidth=200
buttonHeight=50
buttonGap=buttonHeight+30

game_grid = []
turn = ''
time=0
moves = 0

number=0
dir=''
won=False
strike_fraction = 0
levels = ['Easy','Hard']
level = 0

new_screen_ready=False
screen_selected='main menu'

def reset_game_grid():
    global game_grid
    game_grid = [[0,1,2],[3,4,5],[6,7,8]]
def restart_values():
    global game_grid,turn,time,number,dir,won,strike_fraction,new_screen_ready,moves
    reset_game_grid()
    moves=0
    if(random.randint(1,2)==1):
        turn=human_player
    else:
        turn=computer_player
    number=0
    dir=''
    won=False
    strike_fraction=0
    new_screen_ready=False

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
    global game_name_text,options_text
    game_name_text = game_name_font.render(game_name,True,pygame.Color('DarkBlue'))
    options_text = game_name_font.render("Options",True,pygame.Color('DarkBlue'))
    

    buttons.append(button(play_game,'DarkBlue','White',button_font,'normal'))
    buttons.append(button('Level : '+levels[level],'DarkBlue','White',button_font,'normal'))
    buttons.append(button(exit_game,'DarkBlue','White',button_font,'normal'))
    for i in range(button_number):
        buttons[i].set_rect(pygame.Rect(screenWidth/2-buttonWidth/2,200+i*buttonGap,buttonWidth,buttonHeight))

    optionButtons.append(button(restart_game,'DarkBlue','White',button_font,'normal'))
    optionButtons.append(button(back_to_main_menu,'DarkBlue','White',button_font,'normal'))
    for i in range(2):
        optionButtons[i].set_rect(pygame.Rect(screenWidth/2-buttonWidth/2,200+i*buttonGap,buttonWidth,buttonHeight))
                 
def check_hovering():
    mouseX,mouseY = pygame.mouse.get_pos()
    if(screen_selected=='main menu'):
        for i in buttons:
            if (i.rect.x <= mouseX <= i.rect.x+i.rect.width) and (i.rect.y <= mouseY <= i.rect.y+i.rect.height):
                i.set_mode('glow')
            else:
                i.set_mode('normal')
    elif screen_selected=='options':
        for i in optionButtons:
            if (i.rect.x <= mouseX <= i.rect.x+i.rect.width) and (i.rect.y <= mouseY <= i.rect.y+i.rect.height):
                i.set_mode('glow')
            else:
                i.set_mode('normal')

def show_main_menu():
    window.blit(game_name_text,(screenWidth/2-game_name_text.get_width()/2,30))
    for i in range(button_number):
        buttons[i].display()

def show_options():
    window.blit(options_text,(screenWidth/2-options_text.get_width()/2,30))
    for i in range(2):
        optionButtons[i].display()

def check_click():
    global screen_selected,new_screen_ready,level
    mouse_button1, mouse_button2, mouse_button3 = pygame.mouse.get_pressed()
    mouseX,mouseY = pygame.mouse.get_pos()
    if(not mouse_button1):
        return
    if(screen_selected=='main menu'):
        for i in buttons:
            if (i.rect.x <= mouseX <= i.rect.x+i.rect.width) and (i.rect.y <= mouseY <= i.rect.y+i.rect.height):
                if('Level' in i.text):
                    level=1-level
                    i.text = 'Level : '+levels[level]
                    new_screen_ready=False
                else:
                    screen_selected=i.text
                    new_screen_ready=False
    elif(screen_selected=='options'):
        for i in optionButtons:
            if (i.rect.x <= mouseX <= i.rect.x+i.rect.width) and (i.rect.y <= mouseY <= i.rect.y+i.rect.height):
                if(i.text=='Restart Game'):
                    restart_values()
                    screen_selected='Play Game'
                elif(i.text=='Back to Main Menu'):
                    restart_values()
                    screen_selected='main menu'

def position_available(r,c):
    return not (game_grid[r][c]==human_player or game_grid[r][c]==computer_player)
def strike(a,b):
    global strike_fraction
    if(b=='row'):
        pygame.draw.line(window,(255,255,255),(unitLength+unitLength/5,a*unitLength+unitLength/2),(unitLength+unitLength/5+strike_fraction*(3*unitLength-2*unitLength/5),(a*unitLength+unitLength/2)),strike_width)
    if(b=='col'):
        pygame.draw.line(window,(255,255,255),(a*unitLength+unitLength/2,unitLength+unitLength/5),(a*unitLength+unitLength/2,unitLength+unitLength/5+strike_fraction*(3*unitLength-2*unitLength/5)),strike_width)
    if(b=='dia' and a==1):
        pygame.draw.line(window,(255,255,255),(unitLength+unitLength/5,unitLength+unitLength/5),(unitLength+unitLength/5+strike_fraction*(3*unitLength-2*unitLength/5),unitLength+unitLength/5+strike_fraction*(3*unitLength-2*unitLength/5)),strike_width)
    if(b=='dia' and a==2):
         pygame.draw.line(window,(255,255,255),(unitLength+unitLength/5,3*unitLength+unitLength-unitLength/5),(unitLength+unitLength/5+strike_fraction*(3*unitLength-2*unitLength/5),3*unitLength+unitLength-unitLength/5-strike_fraction*(3*unitLength-2*unitLength/5)),strike_width)

    strike_fraction+=0.0625

def check_win():

    for i in range(3):
        if game_grid[i][0]==game_grid[i][1] and game_grid[i][1]==game_grid[i][2]:
            return i+1,'row', True, game_grid[i][0]

    for j in range(3):
        if game_grid[0][j]==game_grid[1][j] and game_grid[1][j]==game_grid[2][j]:
            return j+1,'col', True, game_grid[0][j]
    
    
    if game_grid[0][0]==game_grid[1][1] and game_grid[1][1]==game_grid[2][2]:
        return 1,'dia', True, game_grid[0][0]

    if game_grid[2][0]==game_grid[1][1] and game_grid[1][1]==game_grid[0][2]:
        return 2,'dia',True,game_grid[1][1]    
    count = 0
    for i in range(3):
        for j in range(3):
            if game_grid[i][j]==human_player or game_grid[i][j]==computer_player:
                count+=1
    if(count==9):
        return 0,'',True,'tie'
    return 0,'',False,''
        
def randomMove():
    i=random.randint(0,2)
    j=random.randint(0,2)
    while(not position_available(i,j)):
        i=random.randint(0,2)
        j=random.randint(0,2)
    return i,j
def minimax(isMaximizingTurn):
    number,dir,won,player_type = check_win()
    if(won):
        if player_type==computer_player:
            return 1
        elif player_type==human_player:
            return -1
        elif player_type=='tie':
            return 0
    if(isMaximizingTurn):
        bestScore = -100
        for i in range(3):
            for j in range(3):
                if game_grid[i][j]!=human_player and game_grid[i][j]!=computer_player:
                    original_value = game_grid[i][j]
                    game_grid[i][j]=computer_player
                    score = minimax(False)
                    game_grid[i][j]=original_value
                    if(bestScore<score):
                        bestScore=score
        return bestScore
    else:
        bestScore = 100
        for i in range(3):
            for j in range(3):
                if game_grid[i][j]!=human_player and game_grid[i][j]!=computer_player:
                    original_value = game_grid[i][j]
                    game_grid[i][j]=human_player
                    score = minimax(True)
                    game_grid[i][j]=original_value
                    if(score<bestScore):
                        bestScore=score
        return bestScore

def MiniMax_Algo():
    positions = ''
    best_score = -100
    for i in range(3):
        for j in range(3):
            if game_grid[i][j]!=human_player and game_grid[i][j]!=computer_player:
                original_value = game_grid[i][j]
                game_grid[i][j]=computer_player
                score = minimax(False)
                game_grid[i][j]=original_value
                if(best_score<score):
                    best_score=score
                    positions = [i,j]
    return positions[0],positions[1]
def main_loop():
    run = True
    global turn,time,screen_selected,number,dir,won,new_screen_ready,moves,human_score,computer_score,computer_player,human_player
    while(run):
        pygame.time.delay(100)
        time = max(-1,time-100)
        for events in pygame.event.get():
            if(events.type==pygame.QUIT):
                run=False
        if(screen_selected=='Exit Game'):
            run = False
        elif(screen_selected=='Play Game'):
            if moves==9:
                pygame.time.delay(1000)
                restart_values()
                screen_selected='main menu'
            else:
                if new_screen_ready:
                    window.blit(bg_img,(0,0))
                    pygame.draw.line(window,(0,0,0),(2*unitLength,unitLength),(2*unitLength,screenHeight-unitLength),line_width)
                    pygame.draw.line(window,(0,0,0),(3*unitLength,unitLength),(3*unitLength,screenHeight-unitLength),line_width)
                    pygame.draw.line(window,(0,0,0),(unitLength,2*unitLength),(screenWidth-unitLength,2*unitLength),line_width)
                    pygame.draw.line(window,(0,0,0),(unitLength,3*unitLength),(screenWidth-unitLength,3*unitLength),line_width)
                    human_score_text = score_font.render('You : '+(str)(human_score),True,pygame.Color('DarkBlue'))
                    window.blit(human_score_text,(screenWidth-human_score_text.get_width()-10,20))
                    computer_score_text = score_font.render('Computer : '+(str)(computer_score),True,pygame.Color('DarkBlue'))
                    window.blit(computer_score_text,(10,20))

                    mousex,mousey = pygame.mouse.get_pos()
                    mousex = mousex//unitLength
                    mousey = mousey//unitLength
                    mousex-=1
                    mousey-=1
                    mousex=(int)(mousex)
                    mousey=(int)(mousey)
                    mouseBtn1,mouseBtn2,mouseBtn3 = pygame.mouse.get_pressed()

                    if(turn==human_player):
                        if(0<=mousex<=2 and 0<=mousey<=2):
                            if(position_available(mousey,mousex)):
                                if(mouseBtn1):
                                    game_grid[mousey][mousex]=human_player
                                    moves=moves+1
                                    turn=computer_player
                                    time = 1000
                                else:
                                    gap = 10
                                    pygame.draw.rect(window,(179, 179, 255),(unitLength*(mousex+1)+gap,unitLength*(mousey+1)+gap,unitLength-2*gap,unitLength-2*gap))
                    elif(turn==computer_player and moves<9 and time<0):
                        nextBestMove=0
                        if(level==0):
                            nextBestMove = randomMove()
                        else:
                            nextBestMove = MiniMax_Algo()
                        game_grid[nextBestMove[0]][nextBestMove[1]]=computer_player
                        moves+=1
                        turn=human_player
                    
                    for i in range(3):
                        for j in range(3):
                            if game_grid[i][j]==human_player or game_grid[i][j]==computer_player:
                                text = game_name_font.render(game_grid[i][j],True,pygame.Color('DarkBlue'))
                                window.blit(text,(unitLength*(j+1)+unitLength/2-text.get_width()/2,unitLength*(i+1)+unitLength/2-text.get_height()/2))
                    pygame.display.update()
                    number,dir,won,player_type = check_win()
                    if(won):
                        screen_selected='won'
                        pygame.time.delay(500)
                        if(player_type==human_player):
                            human_score+=1
                        elif(player_type==computer_player):
                            computer_score+=1
                else:
                    mouseBtn1,mouseBtn2,mouseBtn3 = pygame.mouse.get_pressed()
                    if(not mouseBtn1):
                        new_screen_ready=True
        elif(screen_selected=='main menu'):
            if(new_screen_ready):
                check_click()
                check_hovering()
            else:
                mouseBtn1,mouseBtn2,mouseBtn3 = pygame.mouse.get_pressed()
                if(not mouseBtn1):
                    new_screen_ready=True
            window.blit(bg_img,(0,0))
            show_main_menu()
            pygame.display.update()
        elif(screen_selected=='won'):
            window.blit(bg_img,(0,0))
            pygame.draw.line(window,(0,0,0),(2*unitLength,unitLength),(2*unitLength,screenHeight-unitLength),line_width)
            pygame.draw.line(window,(0,0,0),(3*unitLength,unitLength),(3*unitLength,screenHeight-unitLength),line_width)
            pygame.draw.line(window,(0,0,0),(unitLength,2*unitLength),(screenWidth-unitLength,2*unitLength),line_width)
            pygame.draw.line(window,(0,0,0),(unitLength,3*unitLength),(screenWidth-unitLength,3*unitLength),line_width)
            human_score_text = score_font.render('You : '+(str)(human_score),True,pygame.Color('DarkBlue'))
            window.blit(human_score_text,(screenWidth-human_score_text.get_width()-10,20))
            computer_score_text = score_font.render('Computer : '+(str)(computer_score),True,pygame.Color('DarkBlue'))
            window.blit(computer_score_text,(10,20))

            end_game = ''
            if(player_type==human_player):
                end_game = 'You Won'
            elif(player_type==computer_player):
                end_game = 'You Lose'
            elif(player_type=='tie'):
                end_game = 'Draw'
            winner_text = end_game_font.render(end_game,True,pygame.Color('DarkBlue'))
            window.blit(winner_text,(screenWidth/2-winner_text.get_width()/2,screenHeight-winner_text.get_height()-30))
           
            for i in range(3):
                for j in range(3):
                    if game_grid[i][j]==human_player or game_grid[i][j]==computer_player:
                        text = game_name_font.render(game_grid[i][j],True,pygame.Color("DarkBlue"))
                        window.blit(text,(unitLength*(j+1)+unitLength/2-text.get_width()/2,unitLength*(i+1)+unitLength/2-text.get_height()/2))
            strike(number,dir)
            pygame.display.update()
            if(strike_fraction>1):
                pygame.time.delay(1000)
                screen_selected='options'
        elif(screen_selected=='options'):
            if(new_screen_ready):
                check_click()
                check_hovering()  
            else:
                mouseBtn1,mouseBtn2,mouseBtn3 = pygame.mouse.get_pressed()
                if(not mouseBtn1):
                    new_screen_ready=True
                pass
            window.blit(bg_img,(0,0)) 
            show_options()
            pygame.display.update()

restart_values()
set_main_menu()
main_loop()
