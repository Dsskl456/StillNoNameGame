import pygame, random, os, urllib.request, requests, time
from sys import exit
#from pymongo import MongoClient


resolutions=[1,1.406,1.875]
resolution_scale=1
resolution=(400,600)
floor=1000/resolution_scale
wall=1920/resolution_scale

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)  #game window settings
pygame.init() #game window
screen=pygame.display.set_mode(resolution) #game resolution
pygame.display.set_caption('StillNoNameGame') #window title
clock= pygame.time.Clock()
pygame.init()

game_active=True  # game settings
new_top=False
game_pause=False
leaderboard_status=False
new_global=False
end_screen=False
start_menu=True
#global_top_score=None
nickname_active=False

game_level=1
level=1
hp=3
score=0
start_menu_index=0
db_tops=[]
ur_global_score=0
next_level=True

pygame.mixer.init()
bg_music=pygame.mixer.Sound('game/theme.mp3')
bg_music_volume=0.15
bg_music.set_volume(bg_music_volume)
coin_sound=pygame.mixer.Sound('game/coin_sound.wav')
coin_sound.set_volume(0.25)
heal_sound=pygame.mixer.Sound('game/heal_sound.wav')
heal_sound.set_volume(0.2)
hit_sound=pygame.mixer.Sound('game/hit_sound.mp3')
hit_sound.set_volume(0.15)
start_sound=pygame.mixer.Sound('game/start_sound.wav')
start_sound.set_volume(0.25)
game_over_sound=pygame.mixer.Sound('game/game_over_sound.mp3')
game_over_sound.set_volume(0.5)


with open('game/high_score.txt') as f:
    top_score=f.read()
with open('game/nickname.txt') as f:
    nickname=f.read()


    
menu_bg_surface=pygame.image.load('game/menu_background.jpg').convert()   # font and images settings
menu_start_font=pygame.font.Font('game/manaspc.ttf',20)

title_font=pygame.font.Font('game/manaspc.ttf', 30)
button_surface=pygame.image.load('game/blank_button.png').convert_alpha()
nickname_button_surface=pygame.image.load('game/nickname_button.png').convert_alpha()
nickname_button_rect=nickname_button_surface.get_rect(center=(200,200))

little_font=pygame.font.Font('game/manaspc.ttf',int(20/resolution_scale))
score_font=pygame.font.Font('game/manaspc.ttf',int(40/resolution_scale))
score_end=pygame.font.Font('game/manaspc.ttf',int(50/resolution_scale))
    
bg_surface = pygame.image.load('game/game-background.jpg').convert()
ground_surface=pygame.image.load('game/ground.png').convert_alpha()
sun_surface=pygame.image.load('game/sun.png').convert_alpha()
skull_surface=pygame.image.load('game/skull.png').convert_alpha()
skull_global_surface=pygame.image.load('game/skull_global.png').convert_alpha()

bg_level_2_surface=pygame.image.load('game/bg_level_2.jpg').convert()


nickname_surface=menu_start_font.render(nickname,True,'Black')
nickname_rect=nickname_surface.get_rect(center=(200,200))

def main_menu():                                                          # start menu

    screen.blit(menu_bg_surface,(0,0))
    screen.blit(nickname_button_surface,nickname_button_rect)
    title_text=title_font.render('StillNoNameGame.exe',True,'Black')
    title_rect=title_text.get_rect(center=(200,50))
    screen.blit(title_text,title_rect)
    menu_text= menu_start_font.render('Choose resolution',True,'Black')
    menu_rect=menu_text.get_rect(center=(200,130))
    screen.blit(menu_text,menu_rect)
    if nickname_active==True:
        nickname_surface=menu_start_font.render(nickname,True,'Green')
    else:
        nickname_surface=menu_start_font.render(nickname,True,'White')
    nickname_rect=nickname_surface.get_rect(center=(200,200))
    screen.blit(nickname_surface,nickname_rect)
    quit_text=little_font.render('Press ESC to quit',True,'Black')
    quit_text_rect=quit_text.get_rect(center=(200,560))
    screen.blit(quit_text,quit_text_rect)
    #pygame.draw.rect(screen,(0,0,0),nickname_rect,2)


def leaderboard():                                                           #leaderboard menu
    screen.fill('Black')
    leaderboard_title_text=score_end.render('Leaderboard',True,'Red')
    leaderboard_title_rect=leaderboard_title_text.get_rect(center=(960/resolution_scale,50/resolution_scale))
    screen.blit(leaderboard_title_text,leaderboard_title_rect)
    y=0
    for el in db_tops:
        if y==0:
            leaderboard_text=score_font.render(str(y+1)+'. '+str(el['top_score'])+' '+str(el['top_nickname']),True,'Yellow')
        else:
            leaderboard_text=score_font.render(str(y+1)+'. '+str(el['top_score'])+' '+str(el['top_nickname']),True,'White')
        leaderboard_rect=leaderboard_text.get_rect(midleft=(640/resolution_scale,(150+y*75)/resolution_scale))
        screen.blit(leaderboard_text,leaderboard_rect)
        y+=1
    leaderboard_quit_text=little_font.render('ESC/TAB = quit',True,'White')
    leaderboard_quit_rect=leaderboard_quit_text.get_rect(midleft=(10/resolution_scale,1050/resolution_scale))
    screen.blit(leaderboard_quit_text,leaderboard_quit_rect)
        
    

class Button():                                                           # buttons in start menu
    def __init__(self, image, x_pos, y_pos, text_input):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = menu_start_font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
            
            
    def update(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def changeColor(self, position,index,b_index):
        if (position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom)) or index==b_index:
            self.text = menu_start_font.render(self.text_input, True, "red")
        else:
            self.text = menu_start_font.render(self.text_input, True, "white")

button_1=Button(button_surface,200,300,'1920x1080')
button_2=Button(button_surface,200,400,'1366x768')
button_3=Button(button_surface,200,500,'1024x576')


class Player(pygame.sprite.Sprite):                                          #player settings
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load('game/boy_stay_1.png').convert_alpha()
        self.image=pygame.transform.scale(self.image, (int(self.image.get_width()/resolution_scale),int(self.image.get_height()/resolution_scale)))
        self.rect=self.image.get_rect(midbottom=(int(80/resolution_scale),floor))
        self.gravity=0
        self.double_jump=0
        self.down=False
        self.index=1
        self.run=False
        self.turn=1
        #self.hitbox=(self.rect.x,self.rect.y,59,114)
        
    def player_input(self):
        self.run=False
        self.down=False
        keys=pygame.key.get_pressed()
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.down=True
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.x<1860 and self.down==False:
            self.rect.x+=int(10/resolution_scale)
            self.turn=1
            self.run=True
            
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.x>0 and self.down==False:
            self.rect.x-=int(10/resolution_scale)
            self.turn=2
            self.run=True
        
    def jump(self):
        if self.double_jump<2:
            self.gravity=-int(20/resolution_scale)
            self.double_jump+=1
            
    def apply_gravity(self):
        self.gravity+=1/resolution_scale
        self.rect.y+=self.gravity
        if self.rect.bottom>=floor:
            self.gravity=0
            self.rect.bottom=floor
            self.double_jump=0



    def animation_state(self):
        if self.gravity<0: #jumping
            self.image=pygame.image.load('game/boy_jump_'+str(self.turn)+'.png').convert_alpha()
            self.image=pygame.transform.scale(self.image, (int(self.image.get_width()/resolution_scale),int(self.image.get_height()/resolution_scale)))
            self.rect=self.image.get_rect(bottomleft=(self.rect.x,self.rect.bottom))
            self.index=1
        if self.gravity>0: # falling
            self.image=pygame.image.load('game/boy_fall_'+str(self.turn)+'.png').convert_alpha()
            self.image=pygame.transform.scale(self.image, (int(self.image.get_width()/resolution_scale),int(self.image.get_height()/resolution_scale)))
            self.rect=self.image.get_rect(bottomleft=(self.rect.x,self.rect.bottom))
            self.index=1
        if self.gravity==0:
            if self.run==True:
                self.index+=0.15
                if int(self.index)==7: #running
                    self.index=1 
                self.image=pygame.image.load('game/boy_run_'+str(self.turn)+'_'+str(int(self.index))+'.png').convert_alpha()
                self.image=pygame.transform.scale(self.image, (int(self.image.get_width()/resolution_scale),int(self.image.get_height()/resolution_scale)))
                self.rect=self.image.get_rect(bottomleft=(self.rect.x,self.rect.bottom))
                #self.hitbox=(self.rect.x,self.rect.y,self.rect.width,self.rect.height)
                if self.index==6:
                    self.index=1
            else:
                if self.down==True: #laying
                    self.image=pygame.image.load('game/boy_down_'+str(self.turn)+'.png').convert_alpha()
                    self.image=pygame.transform.scale(self.image, (int(self.image.get_width()/resolution_scale),int(self.image.get_height()/resolution_scale)))
                    self.rect=self.image.get_rect(bottomleft=(self.rect.x,self.rect.bottom))
                else: #staying
                    self.image=pygame.image.load('game/boy_stay_'+str(self.turn)+'.png').convert_alpha()
                    self.image=pygame.transform.scale(self.image, (int(self.image.get_width()/resolution_scale),int(self.image.get_height()/resolution_scale)))
                    self.rect=self.image.get_rect(bottomleft=(self.rect.x,self.rect.bottom))
                    self.rect=self.rect
                    #self.hitbox=(self.rect.x,self.rect.y,59,114)
                self.index=1

    def update(self):
        #pygame.draw.rect(screen,(0,255,0),self.rect,2)
        #pygame.draw.rect(screen,(0,0,0),self.hitbox,2)
        self.player_input()
        self.apply_gravity()
        self.animation_state()

player=pygame.sprite.GroupSingle()
player.add(Player())

class Obstacle(pygame.sprite.Sprite):                                                           # flying obstacle in game
    def __init__(self,level,y):
        super().__init__()
        self.level=level
        self.levels='11122333'
        self.bolt_level=self.levels[self.level-1]
        self.index=1
        self.image=pygame.image.load('game/bolt_'+str(self.bolt_level)+'_'+str(int(self.index))+'.png').convert_alpha()
        self.image=pygame.transform.scale(self.image, (int(self.image.get_width()/resolution_scale),int(self.image.get_height()/resolution_scale)))
        self.y=y
        self.rect=self.image.get_rect(bottomleft=(wall+int(100/resolution_scale),self.y))
        self.rect.x-=5/resolution_scale
    def animations(self):
        self.bolt_level==self.levels[self.level-1]
        self.image=pygame.image.load('game/bolt_'+str(self.bolt_level)+'_'+str(int(self.index))+'.png').convert_alpha()
        self.image=pygame.transform.scale(self.image, (int(self.image.get_width()/resolution_scale),int(self.image.get_height()/resolution_scale)))
        self.rect=self.image.get_rect(bottomleft=(self.rect.x,self.rect.bottom))
        self.index+=0.2
        if self.index>6:
            self.index=1
        
        
    def destroy(self):
        if self.rect.x<-100/resolution_scale or game_active==False:
            self.kill() 
    def update(self):
        #pygame.draw.rect(screen,(255,0,0),self.rect,2)
        
        self.animations()
        self.rect.x-=(5+self.level*2)/resolution_scale
        self.destroy()

obstacle_group=pygame.sprite.Group()

class Hearts(pygame.sprite.Sprite):                                                                #flying hearts in game
    def __init__(self,y):
        super().__init__()
        self.image=pygame.image.load('game/hp.png').convert_alpha()
        self.image=pygame.transform.scale(self.image, (int(self.image.get_width()/resolution_scale),int(self.image.get_height()/resolution_scale)))
        self.y=y
        self.rect=self.image.get_rect(midbottom=(-100/resolution_scale,self.y))
        self.rect.x+=5/resolution_scale

    def destroy(self):
        if self.rect.x>wall+100/resolution_scale or game_active==False:
            self.kill() 
    def update(self):

        self.rect.x+=5/resolution_scale
        self.destroy()

hearts_group=pygame.sprite.Group()

def collision_sprite(hp):                                                                          #getting hit during game
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,True):
        hit_sound.play()
        hp-=1
    return hp


def heal_sprite(hp):                                                                               #catching hearts during game
    if hp<5:
        if pygame.sprite.spritecollide(player.sprite,hearts_group,True):
            heal_sound.play()
            hp+=1
    return hp


hp_surface=pygame.image.load('game/hp.png').convert_alpha()
def display_hp():                                                                                   # display hp in game
    for el in range(0,hp):
        hp_rect=hp_surface.get_rect(midright=((1900-el*35)/resolution_scale,100/resolution_scale))
        screen.blit(hp_surface,hp_rect)

def display_score(color):                                                                               #display score in game
    score_surface=score_font.render('Score: '+str(score),True,color)
    score_rect=score_surface.get_rect(midright=(wall-20/resolution_scale, 50/resolution_scale))
    screen.blit(score_surface,score_rect)


coin_rectxy=(random.randint(120/resolution_scale,1500/resolution_scale),random.randint(520/resolution_scale,980/resolution_scale))
def display_coin(coin_rectxy):                                                                       #display coin in game
    coin_surface=pygame.image.load('game/coin.png').convert_alpha()
    coin_surface=pygame.transform.scale(coin_surface, (int(coin_surface.get_width()/resolution_scale),int(coin_surface.get_height()/resolution_scale)))
    coin_rect=coin_surface.get_rect(midbottom=coin_rectxy)
    screen.blit(coin_surface,(coin_rect))
    return coin_rect

def resize_window(size):                                                                             #scaling game window and resolution
    resolution_scale=resolutions[size]
    resolution=(int(1920/resolution_scale),int(1080/resolution_scale))
    screen=pygame.display.set_mode(resolution)
    floor=int(1000/resolution_scale)
    wall=int(1920/resolution_scale)
    coin_rectxy=(random.randint(int(120/resolution_scale),int(1500/resolution_scale)),random.randint(int(520/resolution_scale),int(980/resolution_scale)))
    start_sound.play()
    bg_music.play(loops=-1)
    with open('game/nickname.txt', 'w') as f:
        f.write(str(nickname))
    return resolution_scale, floor, wall, coin_rectxy


def resize_surfaces(resolution_scale):                                                               #scaling texts and images
    
    global score_font, score_end, bg_surface, ground_surface, sun_surface, skull_surface,skull_global_surface, hp_surface, little_font, bg_level_2_surface
    
    score_font=pygame.font.Font('game/manaspc.ttf',int(40/resolution_scale))
    score_end=pygame.font.Font('game/manaspc.ttf',int(50/resolution_scale))
    little_font=pygame.font.Font('game/manaspc.ttf',int(20/resolution_scale))
    
    bg_surface = pygame.image.load('game/game-background.jpg').convert()
    bg_surface=pygame.transform.scale(bg_surface, (int(bg_surface.get_width()/resolution_scale),int(bg_surface.get_height()/resolution_scale)))
    ground_surface=pygame.image.load('game/ground.png').convert_alpha()
    ground_surface=pygame.transform.scale(ground_surface, (int(ground_surface.get_width()/resolution_scale),int(ground_surface.get_height()/resolution_scale)))
    sun_surface=pygame.image.load('game/sun.png').convert_alpha()
    sun_surface=pygame.transform.scale(sun_surface, (int(sun_surface.get_width()/resolution_scale),int(sun_surface.get_height()/resolution_scale)))
    skull_surface=pygame.image.load('game/skull.png').convert_alpha()
    skull_surface=pygame.transform.scale(skull_surface, (int(skull_surface.get_width()/resolution_scale),int(skull_surface.get_height()/resolution_scale)))
    skull_global_surface=pygame.image.load('game/skull_global.png').convert_alpha()
    skull_global_surface=pygame.transform.scale(skull_global_surface, (int(skull_global_surface.get_width()/resolution_scale),int(skull_global_surface.get_height()/resolution_scale)))
    hp_surface=pygame.image.load('game/hp.png').convert_alpha()
    hp_surface=pygame.transform.scale(hp_surface, (int(hp_surface.get_width()/resolution_scale),int(hp_surface.get_height()/resolution_scale)))

    bg_level_2_surface = pygame.image.load('game/bg_level_2.jpg').convert()
    bg_level_2_surface=pygame.transform.scale(bg_level_2_surface, (int(bg_level_2_surface.get_width()/resolution_scale),int(bg_level_2_surface.get_height()/resolution_scale)))

#cluster='mongodb+srv://Player:1234@highscore.bhspl4x.mongodb.net/?retryWrites=true&w=majority'
#client=MongoClient(cluster)
#db=client.game
#db_score=db.db_score

def read_global_score():                                                                            #reading global top score
    try:
        global ur_global_score
        Tops=[]
        myresult = db_score.find().limit(10)
        for x in myresult:
            Tops.append({'top_score':x['Score'],'top_nickname':x['Nickname']})
            if x['Nickname']==nickname:
                ur_global_score=x['Score']
        #if ur_global_score==0:
        #    ur_global_score=Tops[-1]['top_score']
        global_top_score=Tops[0]['top_score']
        global_top_nickname=Tops[0]['top_nickname']
        #print('global scores readed')
        return global_top_score, global_top_nickname, ur_global_score, Tops
    except Exception as e:
        print(e)
        return None, None, None, None

#global_top_score, global_top_nickname, ur_global_score, db_tops=read_global_score()

def myFunc(e):
    return e['top_score']

def write_global_score():                                                                           #writing new global top score
    try:
        db_tops.append({'top_score':score,'top_nickname':nickname})
        for el in db_tops[:-1]:
            if el['top_nickname']==nickname:
                db_tops.remove(el)
        db_tops.sort(reverse=True,key=myFunc)
        db_tops.pop()
        x=1
        for el in db_tops:
            db_score.update_one({'Top':x}, {"$set": { "Score": el['top_score'],'Nickname': el['top_nickname']}})
            x+=1
        #print("\nYour message has successfully been sent!")    
    except Exception as e:
        print(e)


obstacle_timer=pygame.USEREVENT +1                                                                  #user events
pygame.time.set_timer(obstacle_timer, 1500)

def Level_1(coin_rectxy):
    screen.blit(bg_surface,(0,0))
    screen.blit(ground_surface,(0,floor))
    screen.blit(sun_surface,(0,0))
    coin_rect=display_coin(coin_rectxy)
    player.draw(screen)
    obstacle_group.draw(screen)
    hearts_group.draw(screen)
    return coin_rect

def Level_2(coin_rectxy):
    screen.blit(bg_level_2_surface,(0,0))
    coin_rect=display_coin(coin_rectxy)
    player.draw(screen)
    hearts_group.draw(screen)
    return coin_rect

def New_level():
    global hp
    hp=3
    screen.fill('Black')
    player.sprite.rect.x=80/resolution_scale
    player.sprite.rect.y=floor
    #obstacle_group.kill()


while True:                                                                             #main game loop

    for event in pygame.event.get():                                                        #game events 
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if start_menu==True:                                                                    #start menu events
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if len(nickname)>0 and nickname!='Nickname':
                    if button_1.checkForInput(MENU_MOUSE_POS):
                        resolution_scale, floor, wall, coin_rectxy=resize_window(0)
                        resize_surfaces(resolution_scale)
                        start_menu=False
                    if button_2.checkForInput(MENU_MOUSE_POS):
                        resolution_scale, floor, wall, coin_rectxy=resize_window(1)
                        resize_surfaces(resolution_scale)
                        start_menu=False
                    if button_3.checkForInput(MENU_MOUSE_POS):
                        resolution_scale, floor, wall, coin_rectxy=resize_window(2)
                        resize_surfaces(resolution_scale)
                        start_menu=False
                if nickname_rect.collidepoint(event.pos):
                    nickname_active=True
                    start_menu_index=4
                else:
                    nickname_active=False
            if event.type ==pygame.KEYDOWN:                                                         #nickname input settings
                if nickname_active==True:
                    if event.key == pygame.K_BACKSPACE:
                        nickname=nickname[:-1]
                    elif event.key==pygame.K_COMMA or event.key==pygame.K_DELETE or event.key==pygame.K_TAB:
                        pass
                    
                    elif event.key==pygame.K_RETURN or event.key==pygame.K_KP_ENTER or event.key==pygame.K_DOWN:
                        if len(nickname)>0:
                            nickname_active=False
                            start_menu_index=3
                    elif event.key==pygame.K_UP:
                        if len(nickname)>0:
                            nickname_active=False
                            start_menu_index=1                        
                    else:
                        if len(nickname)<16:
                            nickname+=event.unicode
                else:                                                                                #menu movement
                    if event.key==pygame.K_UP:
                        if start_menu_index>=4:
                            start_menu_index=1
                        else:
                            start_menu_index+=1
                    if event.key==pygame.K_DOWN:
                        if start_menu_index<=1:
                            start_menu_index=4
                        else:
                            start_menu_index-=1
                    if start_menu_index==4:
                        nickname_active=True
                    if start_menu_index in [1,2,3]:
                        if len(nickname)>0 and nickname!='Nickname':
                            if event.key==pygame.K_RETURN or event.key==pygame.K_KP_ENTER:
                                resolution_scale, floor, wall, coin_rectxy=resize_window(3-start_menu_index)
                                resize_surfaces(resolution_scale)
                                start_menu=False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                        
        if start_menu==False:                                                                    
            if game_active==True:
                #if score==5 and next_level==True:
                    #level=2
                    #New_level()
                    #next_level=False
                    
                if game_pause==False:                                                           #game events
                    if event.type==pygame.KEYDOWN:                                                  #player jump
                        if event.key==pygame.K_w or event.key==pygame.K_UP or event.key==pygame.K_SPACE:
                            player.sprite.jump()
                        if event.key==pygame.K_ESCAPE:                                              #pause
                            game_pause=True
                            pygame.mixer.pause()

                        if event.key==pygame.K_EQUALS or event.key==pygame.K_PLUS:                  #volume settings input
                            if bg_music_volume<1:
                                bg_music_volume+=0.05
                                bg_music.set_volume(bg_music_volume)
                        if event.key==pygame.K_UNDERSCORE or event.key==pygame.K_MINUS:
                            if bg_music_volume>0:
                                bg_music_volume-=0.05
                                bg_music.set_volume(bg_music_volume)

                    if event.type==obstacle_timer and level==1:                                                   #obstacle respawn
                        obstacle_group.add(Obstacle(game_level,random.randint(int(500/resolution_scale),int(1000/resolution_scale))))
                        pygame.time.set_timer(obstacle_timer, 1500-game_level*200)
                else:
                    if event.type==pygame.KEYDOWN:                                                     #unpause
                        if leaderboard_status==False:
                            if event.key==pygame.K_ESCAPE:
                                game_pause=False
                                pygame.mixer.unpause()
                            if event.key==pygame.K_q:
                                pygame.quit()
                                exit()
                            if event.key==pygame.K_TAB:
                                leaderboard_status=True
                                #global_top_score,global_top_nickname, ur_global_score, db_tops=read_global_score()
                        else:
                            if event.key==pygame.K_TAB or event.key==pygame.K_ESCAPE:
                                leaderboard_status=False


            if game_active==False:
                if end_screen==False:                                                           #endscreen showup
                    pygame.mixer.stop()
                    game_over_sound.play()
                    #global_top_score,global_top_nickname, ur_global_score, db_tops=read_global_score() 
                    #if global_top_score!=None:
                    #    if score>global_top_score:
                    #       new_global=True
                    #    if score>ur_global_score:
                    #       write_global_score()
                            
                    end_screen=True
                                                                                              #endscreen input
                if leaderboard_status==False:
                    if event.type==pygame.KEYDOWN:
                        if (event.key==pygame.K_RETURN or event.key==pygame.K_KP_ENTER):
                            end_screen=False
                            score=0
                            New_level()
                            game_level=1
                            new_top=False
                            new_global=False
                            game_active=True
                            coin_rectxy=(random.randint(int(120/resolution_scale),int(1500/resolution_scale)),random.randint(int(520/resolution_scale),int(980/resolution_scale)))
                            start_sound.play()
                            bg_music.play(loops=-1)
                        if event.key==pygame.K_TAB:
                            leaderboard_status=True
                            #global_top_score,global_top_nickname, ur_global_score, db_tops=read_global_score()
                else:
                    if event.type==pygame.KEYDOWN: 
                        if event.key==pygame.K_TAB or event.key==pygame.K_ESCAPE:
                            leaderboard_status=False
                        

    if start_menu==True:                                                          # menu screen
        main_menu()

        MENU_MOUSE_POS=pygame.mouse.get_pos()
        button_1.update()
        button_1.changeColor(MENU_MOUSE_POS,start_menu_index,3)
        button_2.update()
        button_2.changeColor(MENU_MOUSE_POS,start_menu_index,2)
        button_3.update()
        button_3.changeColor(MENU_MOUSE_POS,start_menu_index,1)


    if start_menu==False:                                                         # game screen
        if game_active==True:
            #print(game_pause)
            if level==1:
                coin_rect=Level_1(coin_rectxy)
                display_score('Black')
            if level==2:
                coin_rect=Level_2(coin_rectxy)
                display_score('White') 
            if hp==0:
                game_active=False
            display_hp()
            if game_pause==False:
                player.update()

                if score>int(top_score):
                    top_score=score
                    new_top=True

                hp=collision_sprite(hp)
                game_level=int(score/10) +1

                obstacle_group.update()

                hp=heal_sprite(hp)
                hearts_group.update()

                if coin_rect.colliderect(player.sprite.rect):                               #Collecting coin
                    coin_sound.play()
                    score+=1
                    coin_rectxy=(random.randint(int(120/resolution_scale),int(1400/resolution_scale)),random.randint(int(520/resolution_scale),int(980/resolution_scale)))
                    if random.randint(1,10)==7:
                        hearts_group.add(Hearts(random.randint(int(500/resolution_scale),floor)))

            else:                                                                           #game paused
                if leaderboard_status==True:
                    leaderboard()
                else:
                    pause_surface=score_end.render('PAUSE',True,'Black')
                    pause_rect=pause_surface.get_rect(center=(960/resolution_scale,400/resolution_scale))
                    screen.blit(pause_surface,pause_rect)
                    resume_game_surface=little_font.render('ESC = Resume',True,'Black')
                    resume_game_rect=resume_game_surface.get_rect(center=(960/resolution_scale, 450/resolution_scale))
                    screen.blit(resume_game_surface,resume_game_rect)
                    quit_game_surface=little_font.render('Q = Quit game',True,'Black')
                    quit_game_rect=quit_game_surface.get_rect(center=(960/resolution_scale, 475/resolution_scale))
                    screen.blit(quit_game_surface,quit_game_rect)
                    leaderboard_game_surface=little_font.render('TAB = Leaderboard',True,'Black')
                    leaderboard_game_rect=leaderboard_game_surface.get_rect(center=(960/resolution_scale, 500/resolution_scale))
                    screen.blit(leaderboard_game_surface,leaderboard_game_rect)
        else:                                                                        #end screen
            if leaderboard_status==True:
                leaderboard()
            else:
                screen.fill('Black')
                top_score_surface=score_end.render('Score: '+str(score), True,'White')
                top_score_rect=top_score_surface.get_rect(center=(960/resolution_scale, 600/resolution_scale))
                screen.blit(top_score_surface,top_score_rect)

                if new_top==True:                                                               #top score
                    score_end_surface=score_end.render('New Top Score:'+str(top_score),True,'Red')
                    score_end_rect=score_end_surface.get_rect(center=(960/resolution_scale, 700/resolution_scale))
                    screen.blit(score_end_surface,score_end_rect)
                    with open('game/high_score.txt', 'w') as f:
                        f.write(str(score))

                else:
                    score_end_surface=score_end.render('Top score:'+str(top_score),True,'White')
                    score_end_rect=score_end_surface.get_rect(center=(960/resolution_scale, 700/resolution_scale))
                    screen.blit(score_end_surface,score_end_rect)
                #if global_top_score!=None:                                                     #global score
                #    if new_global==True:
                #        skull_global_rect=skull_global_surface.get_rect(center=(960/resolution_scale,300/resolution_scale))
                #        screen.blit(skull_global_surface,skull_global_rect)
                #        global_end_surface=score_end.render('New Global top score: '+str(score),True,'Red')
                #        global_end_rect=global_end_surface.get_rect(center=(960/resolution_scale,800/resolution_scale))
                #        screen.blit(global_end_surface,global_end_rect)
                #    else:
                #        global_end_surface=score_end.render('Global top score: '+str(global_top_score)+' by '+str(global_top_nickname),True,'White')
                #        global_end_rect=global_end_surface.get_rect(center=(960/resolution_scale,800/resolution_scale))
                #        screen.blit(global_end_surface,global_end_rect)
                #        skull_rect=skull_surface.get_rect(center=(960/resolution_scale,300/resolution_scale))
                #        screen.blit(skull_surface,skull_rect)
                #else:
                #    skull_rect=skull_surface.get_rect(center=(960/resolution_scale,300/resolution_scale))
                #    screen.blit(skull_surface,skull_rect)
                enter_end_surface=score_end.render('Press ENTER to start new game',True,'White') #continue
                enter_end_rect=enter_end_surface.get_rect(center=(960/resolution_scale,900/resolution_scale))
                screen.blit(enter_end_surface,enter_end_rect)
                leaderboard_end_surface=score_end.render('TAB = Leaderboard',True, 'White')
                leaderboard_end_rect=leaderboard_end_surface.get_rect(center=(960/resolution_scale,975/resolution_scale))
                screen.blit(leaderboard_end_surface,leaderboard_end_rect)
                
                #if score >60:                                                                    #easter egg
                #    level2_font=pygame.font.Font('game/manaspc.ttf',int(20/resolution_scale))
                #    level2_surface=level2_font.render('Level 2 soon...',True,'Dimgrey')
                #    level2_rect=level2_surface.get_rect(center=(960/resolution_scale,1050/resolution_scale))
                #    screen.blit(level2_surface,level2_rect)
            

    pygame.display.update()
    clock.tick(60)
