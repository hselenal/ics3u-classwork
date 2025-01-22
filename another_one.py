import pygame
import os
import random 
import json

pygame.init()

WIDTH = 640
HEIGHT = 480
SIZE = (WIDTH, HEIGHT)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# ---------------------------
# Initialize global variables
time_run = 0
hit_time = 0

# Start variables 
state = 0 # -1 is load save files, 0 is start screen, 0.5 is tutorial, 1 is playing, 2 is dead, 3 is pause menu, 4 is store
start_playing = pygame.image.load(os.getcwd() + "\sprites\play_button.png")
start_playing_rect = pygame.Rect(217,204,208,78)
start_screen = pygame.image.load(os.getcwd() + "\sprites\Start_Screen.png")
background = pygame.image.load(os.getcwd() + "\sprites\Background.png")
walls = []
checking = 0
continue_playing_rect = (220, 280, 180, 40)

# Load Variables
load_rect = pygame.Rect(217, 300, 208, 100)
num_saves = 0 #max 2
with open("all_save_files.txt", "r") as f:
    num_saves = int(f.read())
    f.close()

save_1_rect = pygame.Rect(50, 50, WIDTH/2-75, HEIGHT-100)
save_2_rect = pygame.Rect(WIDTH/2+25, 50, WIDTH/2-75, HEIGHT-100)
save_button = pygame.Rect(WIDTH-70, HEIGHT-70, 50, 50)
enemy_save_rooms = [2, 3, 6, 8, 9, 12] #rooms with enemies in them
saving = False #variable to check if save button presssed or not
last_time_saved = 0

new_save_rect = pygame.Rect(0, 0, 0, 0)
new_save_position = [50, 50, 50, 50]
between_screen_time = 0

override_rect_1 = pygame.Rect(50, 50, WIDTH-100, 100)
override_rect_2 = pygame.Rect(50, 200, WIDTH-100, 100)

x_pic = pygame.image.load(os.getcwd() + "\sprites\X_pic.png")

#Volume variables
slider_x = 220
slider_y = 350
slider_width = 200
slider_height = 5
knob_radius = 10
min_volume = 0.0
max_volume = 1.0
current_volume = 0.5
knob_x = slider_x + int(current_volume * slider_width)
sound = pygame.mixer.Sound(os.getcwd() + "\sprites\music.wav")
sound.set_volume(current_volume)
font = pygame.font.Font(None, 36)
sound_time = 0
sound_check = 0

#Dialogue
dialogue_box = pygame.image.load(os.getcwd() + "\sprites\dialogue_box.png")

#Tutorial variables
help_image = 1 # the number of the tutorial image it is on

tutorial_1 = pygame.image.load(os.getcwd() + "\sprites\Tutorial_1.png")
tutorial_1 = pygame.transform.scale(tutorial_1, (WIDTH-60, HEIGHT-60))

tutorial_2 = pygame.image.load(os.getcwd() + "\sprites\Store_tutorial_1.png")
tutorial_2 = pygame.transform.scale(tutorial_2, (WIDTH-60, HEIGHT-60))

tutorial_3 = pygame.image.load(os.getcwd() + "\sprites\damage_tutorial_1.png")
tutorial_3 = pygame.transform.scale(tutorial_3, (WIDTH-60, HEIGHT-60))

tutorial_4 = pygame.image.load(os.getcwd() + "\sprites\damage_tutorial_2.png")
tutorial_4 = pygame.transform.scale(tutorial_4, (WIDTH-60, HEIGHT-60))

tutorial_time_pressed = 0

# Player variables
player_x = WIDTH/2
player_y = HEIGHT/2
moving = [0, 0, 0, 0]
start_player = pygame.image.load(os.getcwd() + "\sprites\Player_Up.png")
other_player = pygame.image.load(os.getcwd() + "\sprites\Other_player.png")
player = start_player
player_hitbox = pygame.Rect(player_x, player_y, 30, 25)
player_rotated = player
all_hits = []

player_hp = 100000
player_AOE = pygame.Rect(player_x, player_y, 30, 20)

font = pygame.font.Font(None, 30)
hp_text = font.render(f"Health: {player_hp}", True, (0, 0, 0)) #player hp on screen
health_potion_num = 0

w = True
a = False
s = False
d = False

#Elf
elf_image = pygame.image.load(os.getcwd() + "\sprites\Red_elf.png")
elves_rect = []
all_elves_hp = [5000 for i in range(11)] #note: elf 0 is in the elf from room 2, elves 1-end are the spawned elves from Christmas Tree
room_8_elves = []
room_8_elves_num = []

#Christmas Tree
tree_image = pygame.image.load(os.getcwd() + "\sprites\christmas_tree_mini.png")
tree_hp = 100000
tree_dialogue_done = False
tree_dialogue_time = 0
tree_dialogue_num = 0
christmas_chest_opened = False

# Snowman Chests
snowman_chest_opened = False
snowman_rewards_collected = False 

# rewards after beating tree
tree_rewards_collected = False
time_since_collected = 0

#Chests 
chest_closed = pygame.image.load(os.getcwd() + "\sprites\chest_closed.png")
chest_opened = pygame.image.load(os.getcwd() + "\sprites\chest_opened.png")

# Snowman variables 
snowman = pygame.image.load(os.getcwd() + "\sprites\snowman.png") 
snowman_x = 150
snowman_y = 150
snowman_speed = 10 
snowman_timer = 0 
snowballs = [] 
snowman_hitbox = pygame.Rect(-100, -100, 50, 50) 
snowman_hp = 200000
snowman_damage = [] 
player_damage = [] 
snowman_dialogue_done = False
snowman_dialogue_time = 0
snowman_dialogue_num = 0

# Rudolph variables
rudolph_x = 320
rudolph_y = 150
rudolph_up = pygame.image.load(os.getcwd() + "\sprites\Rudolph_up.png")
rudolph_left = pygame.image.load(os.getcwd() + "\sprites\Rudolph_left.png")
rudolph_down = pygame.image.load(os.getcwd() + "\sprites\Rudolph_down.png")
rudolph_right = pygame.image.load(os.getcwd() + "\sprites\Rudolph_right.png")
rudolph_hitbox = pygame.Rect(rudolph_x-2, rudolph_y+25, 50, 50)
rudolph_hp = 250000
rudolph_timer = 0
rudolph_charge = False
rudolph_charge_timer = 0
time_count = 0
startup_time_count = 0
rudolph_rewards_collected = False
rudolph_dialogue_num = 0
rudolph_dialogue_done = False
rudolph_dialogue_time = 0
rudolph_north = False
rudolph_west = False
rudolph_south = True
rudolph_east = False
rudolph_chest_opened = False

# Sled variables 
sled_top = pygame.image.load(os.getcwd() + "\sprites\sled_top.png")
sled_middle = pygame.image.load(os.getcwd() + "\sprites\sled_middle.png")
sled_bottom = pygame.image.load(os.getcwd() + "\sprites\sled_bottom.png")
sled_moving = [False, False, False]
sled_xy = [[200, 150], [400, 200], [100, 300]]
sled_done = [[273, 203],[290, 210], [273, 235]]
sled_pass = [False, False, False]
sled_dialogue_done = False
sled_dialogue_time = 0
sled_dialogue_num = 0
sled_chest_opened = False
sled_rewards_collected = False 

# Santa variables
santa = pygame.image.load(os.getcwd() + "\sprites\santa.png")
santa_time = 0
santa_hp = 500000

end_dialogue_done = False
end_dialogue_time = 0
end_dialogue_num = 0
end = False
grinch = pygame.image.load(os.getcwd() + "\sprites\grinch.png")
grinch = pygame.transform.scale(grinch, (54,118))
end_hitbox = pygame.Rect(295,215,50,50)

# Currency (candy cane) variables
cane = pygame.image.load(os.getcwd() + "\sprites\Candy_cane.png")
cane_list = [] 
cane_rects = [] 
for i in range(10): 
    x = random.randrange(100, 500) 
    y = random.randrange(125, 350)
    cane_list.append([x, y])
    rect = pygame.Rect(x, y + 10, 30, 20)
    cane_rects.append(rect)

candies = 0

# Pause Menu variables
settings_bar_rect = pygame.Rect(220,200,180,40)
settings = False

# Store variables 
store1 = pygame.image.load(os.getcwd() + "\sprites\store.png")
store = pygame.transform.scale(store1, (70, 75))
store_hitbox_rect = store.get_rect()
store_hitbox_rect.center = (130, 340)
sign = pygame.image.load(os.getcwd() + "\sprites\signs.png")
items_square_rect = [pygame.Rect(235,138,40,40), pygame.Rect(295,138,40,40), pygame.Rect(355,138,40,40)]
items = ['SWORD', 'BOW', 'HEALTH'] 
prices = [15,15,5] #sword, bow, health potion
confirmation = False
item_bought = 0
item_number = "Sigma"
upgrades = False

purchase_time = False #time since purchased item
fail_time = False #time since failed to purchase item (not enough candy canes)

# Inventory variables 
inventory = ['blank','blank','blank']
sword_1 = pygame.image.load(os.getcwd() + "\sprites\Sword_1.png")
bow = pygame.image.load(os.getcwd() + "\sprites\Bow.png")
initial_health_potion = pygame.image.load(os.getcwd() + "\sprites\Health_potion.png")
health_potion = pygame.transform.scale(initial_health_potion, (25,27))
health_potion_num = 0
font1 = pygame.font.Font(None, 20)
potion_text = font.render(f"{health_potion_num}", True, (0, 0, 0))
health_cooldown = 0
player_equipped = ""

# Transition variables 
door_rect = pygame.Rect(300, 100, 50, 10)
room = 0

# Bow variables
bow_cooldown = 0
arrows_up = []
arrows_left = []
arrows_down = []
arrows_right = []

bow_damage = 1000
sword_damage = 10000

#bonus powerups
dmg_bonus = 1.15 #percentage
dmg_buff_pic = pygame.image.load(os.getcwd() + "\sprites\dmg_buff.png")
dmg_buff_pic = pygame.transform.scale(dmg_buff_pic, (40, 40))
collected_4 = False #whether collected powerup in room yet
collected_4_time = 0
collected_11 = False
collected_11_time = 0
# -------------------------------------------------------------------------------------------------------------------------


# Function for text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))
text_font = pygame.font.SysFont("Nunito", 40)
text_font_small = pygame.font.SysFont("Nunito", 30)
text_font_smaller = pygame.font.SysFont("Nunito", 25)

# Function for snowman attacking
def snowman_hit(type): 
    if type == "snowman": 
        damage = random.randrange(800, 1000)
    if type == "snowball": 
        damage = random.randrange(500, 800)
    
    return damage

def snowball_direction(player_x, player_y, snowman_x, snowman_y): 
    player_pos = pygame.math.Vector2(player_x, player_y)
    snowman_pos = pygame.math.Vector2(snowman_x, snowman_y)
    direction = player_pos - snowman_pos 
    direction = direction.normalize() 
    return direction


# all Rudolph Boss Functions
def rudolph_move(player_x, player_y, rudolph_x, rudolph_y):
    player_position = pygame.math.Vector2(player_x, player_y)
    rudolph_position = pygame.math.Vector2(rudolph_x, rudolph_y)
    rudolph_direction = player_position - rudolph_position
    rudolph_direction = rudolph_direction.normalize()
    return rudolph_direction


def rudolph_damage(rudolph_hp):
    if rudolph_hitbox.colliderect(arrow_hitbox):
        rudolph_hp -= bow_damage
    if rudolph_hitbox.colliderect(player_AOE):
        rudolph_hp -= sword_damage
    return rudolph_hp

def rudolph_hit(hit):
    if hit == "rudolph":
        damage = 1000
    elif hit == "charge":
        damage = 10000
    
    return damage


class elves(): # contains all functions for the elves (initialization, movement, drawing, collisions, and attacks)
    global player_x, player_y

    def __init__(self, x, y): #declaring all variables / vectors for elves
        self.elf_x = x
        self.elf_y = y
        self.elf_to_player = pygame.math.Vector2(player_x - self.elf_x, player_y - self.elf_y) #vector for the direction to move the elf in
        self.normalized = self.elf_to_player.normalize()
        self.AOE = 5
        self.elf_AOE = pygame.Rect(self.elf_x-self.AOE, self.elf_y-self.AOE, 60, 60) #AOE of elf attack
        self.last_attack = 0 #time since last attack (attacks at an interval)
        self.attacked = False #whether the elf has attacked the player or not (for calculating dmg, showing it on the screen, etc.)
        self.elf_hp = 5000 #max elf health
    
    def vector_calculations(self, elf_number): #calculates where the elf needs to move to
        global player_hitbox, room, tree_hp, all_elves_hp, santa_hp

        if all_elves_hp[elf_number] > 0:
            self.normalized_new = [abs(self.normalized[0]), abs(self.normalized[1])] #always positive x and y values for the vector
            if self.normalized[0] < 0.6: #because the movement in the x-direction is a bit slow
                self.normalized[0] = 0.6
            if self.elf_AOE.colliderect(player_hitbox) == False and all_elves_hp[elf_number] > 0:
                if self.elf_x > player_x + 5:
                    self.elf_x -= self.normalized_new[0] * 3
                elif self.elf_x < player_x - 5:
                    self.elf_x += self.normalized_new[0] * 3
                if self.elf_y > player_y + 5:
                    self.elf_y -= self.normalized_new[1] * 3
                elif self.elf_y < player_y - 5:
                    self.elf_y += self.normalized_new[1] * 3
        
        if all_elves_hp[elf_number] <= 0 and all_elves_hp[elf_number] > -1000000000:
            self.elf_x = -100
            self.elf_y = -100
            if room == 3:
                tree_hp -= 4000
            if room == 12:
                santa_hp -= 0
            if room == 2 or room == 3 or room == 12: #single elf room, christmas tree room, and santa room
                all_elves_hp[elf_number] = -10000000000

                return True # used for the tree when determining whether an elf has died or not
        
        return False

    def attack(self, player_hp) -> int: #the logistics behind attacking the player; returns the player's hp as well
        global time_run
        if time_run - self.last_attack > 1000:
            if (self.elf_x < player_x + self.AOE and self.elf_x > player_x - self.AOE) and (self.elf_y < player_y + self.AOE and self.elf_y > player_y - self.AOE):
                self.last_attack = time_run
                self.attacked = True

                self.dmg = random.randint(100, 200)
                self.crit_chance = random.randint(1, 50) #2% crit rate

                if self.crit_chance == 1:
                    self.dmg *= 3
                player_hp -= self.dmg
                self.attacked = True
                self.x_offset = random.randint(-10, 10)
                self.y_offset = random.randint(-10, 10)
            else:
                self.attacked = False
            
        return player_hp

    def draw_elf(self): #draws the elf and the text for dmg done to the player
        global text_font_small
        screen.blit(elf_image, (self.elf_x, self.elf_y, 30, 30))

        if self.attacked == True:
            if self.crit_chance != 1:
                draw_text(str(self.dmg), text_font_small, (255, 0, 0), player_x + self.x_offset, player_y + self.y_offset)
            else:
                draw_text(str(self.dmg), text_font, (255, 0, 0), player_x + self.x_offset, player_y + self.y_offset)
                draw_text("CRIT", text_font, (255, 0, 0), player_x + self.x_offset + 15, player_y + self.y_offset + 15)
    
    def elf_rect(self, required): #returns a lot of useful values based on what you pass into as an argument
        if required == 0:
            return self.elf_x
        elif required == 1:
            return self.elf_y


class Christmas_Tree():
    global tree_hp

    def __init__(self, x, y):
        self.summoned_elves = []
        self.x = x
        self.y = y
        self.phase = 1
        self.killed = 0 #amount of elves the player has killed that have been summoned by tree

    def summon(self):
        global all_elves_hp, player_hp, tree_dialogue_done
        if self.phase == 1 and tree_dialogue_done == True:
            if len(self.summoned_elves) < 10:
                self.elf = elves(random.randint(int(self.x) - 150, int(self.x) + 150), (random.randint(self.y - 20, self.y + 20)))
                self.summoned_elves.append((self.elf))

            if len(self.summoned_elves) == 10:
                for creature in range(len(self.summoned_elves)):
                    killed = self.summoned_elves[creature].vector_calculations(creature+1) #gets num of elves the player has killed
                    self.summoned_elves[creature].draw_elf()
                    player_hp = self.summoned_elves[creature].attack(player_hp)

                    if killed == True:
                        self.killed += 1
                if self.killed == 10:
                    self.phase = 2
                
        if self.killed == 10 and self.phase == 2: #will only go into this once
            self.phase = 2
            for i in range(16): #adds one extra (no dmg one)
                all_elves_hp.append(5000)
            self.killed = 11 #set it to be a number that is impossible during the first phase
        
        if self.killed >= 11:
            if self.phase == 2 or self.phase == 3:
                if len(self.summoned_elves) < 26:
                    self.elf = elves(random.randint(int(self.x) - 150, int(self.x) + 150), (random.randint(self.y - 20, self.y + 20)))
                    self.summoned_elves.append((self.elf))

                for creature in range(len(self.summoned_elves)):
                    killed = self.summoned_elves[creature].vector_calculations(creature+1)
                    self.summoned_elves[creature].draw_elf()
                    player_hp = self.summoned_elves[creature].attack(player_hp)

                    if killed == True:
                        self.killed += 1
        
        return self.summoned_elves
    
    def draw(self):
        tree_rect = pygame.Rect(self.x-15, self.y-15, 30, 30)
        screen.blit(tree_image, tree_rect)

        pygame.draw.rect(screen, (255, 0, 0), (WIDTH/2-20, 85, (tree_hp/100000)*40, 10))
        pygame.draw.rect(screen, (255, 255, 255), (WIDTH/2-20, 85, 40, 10), 2)

class Santa:
    global santa_hp
    def __init__(self, x, y):
        self.summoned_elves = []
        self.santa_x = x
        self.santa_y = y
        self.killed = 0 #amount of elves the player has killed that have been summoned by santa
    def summon(self):
        global all_elves_hp, player_hp, santa_time, time_run
        if time_run - santa_time > 3000:
            if len(self.summoned_elves) < 5:
                self.elf = elves(random.randint(int(self.santa_x) - 150, int(self.santa_x) + 150), (random.randint(self.santa_y - 20, self.santa_y + 20)))
                self.summoned_elves.append((self.elf))
            santa_time = time_run
        if len(self.summoned_elves) == 5:
            for creature in range(len(self.summoned_elves)):
                killed = self.summoned_elves[creature].vector_calculations(len(all_elves_hp)-1-(5-creature)) #gets num of elves the player has killed
                self.summoned_elves[creature].draw_elf()
                player_hp = self.summoned_elves[creature].attack(player_hp)
                if killed == True:
                    self.killed += 1
        
        if self.killed == 5:
            self.summoned_elves = []
            self.killed = 0
            all_elves_hp = [5000 for i in range(11)]
                
        return self.summoned_elves
    
    def santa_rectangle(self):
        return [self.santa_x, self.santa_y]

    def snowball(self):
        global snowman_timer, snowballs, direction, player_hitbox, player_hp, damage_taken, player_damage, time_run
        
        # Santa shooting 
        if snowman_timer + 1200 < time_run: 
            snowballs.append([self.santa_x + 20, self.santa_y + 20])
            snowman_timer = time_run 
        for i in range(len(snowballs)): 
            direction = snowball_direction(player_x, player_y, self.santa_x, self.santa_y)
            snowballs[i][0] += direction[0] * 20
            snowballs[i][1] += direction[1] * 20
                
        # When santa's snowballs collide with player
        for snowball in snowballs: 
            if player_hitbox.colliderect(pygame.Rect(snowball[0] - 12, snowball[1] - 12, 24, 24)): 
                damage_taken = snowman_hit("snowball")
                player_hp -= damage_taken
                player_damage.append([time_run, damage_taken, random.randrange(0, 20), random.randrange(0, 20)])
    
    def draw(self):
        santa_rect = pygame.Rect(self.santa_x-15, self.santa_y-15, 30, 30)
        screen.blit(santa, santa_rect)
            

def player_attacking(enemy_type, enemy, elf_number, hp, enemy_hitbox, w, a, s, d): #currently only works for attacking the elves
    global time_run, hit_time, player_x, player_y
    dmg_done = sword_damage
    player_crit_chance = random.randint(1, 15)
    if player_crit_chance == 1:
        dmg_done *= 4
    
    if w == True:
        player_AOE = pygame.Rect(player_x-15, player_y-20, 60, 40)

    elif a == True:
        player_AOE = pygame.Rect(player_x-25, player_y-15, 40, 60)

    elif s == True:
        player_AOE = pygame.Rect(player_x-15, player_y+20, 60, 40)

    elif d == True:
        player_AOE = pygame.Rect(player_x+15, player_y-15, 40, 60)

    if enemy_type == "elf":
        elf_hitbox = pygame.Rect(enemy.elf_rect(0), enemy.elf_rect(1), 35, 35) #slightly larger than actual elf as offset

        if event.type == pygame.MOUSEBUTTONDOWN and time_run - hit_time > 150:
            if player_AOE.colliderect(elf_hitbox) == True:
                hp[elf_number] -= dmg_done
                hit_time = time_run

                return [True, dmg_done, player_crit_chance]
            
            else:
                return [False, 0, 0]
        
        else:
            return [False, 0, 0]

    elif enemy_type == "snowman" or enemy_type == "rudolph" or enemy_type == "santa":
        if event.type == pygame.MOUSEBUTTONDOWN and time_run - hit_time > 150:
            if player_AOE.colliderect(enemy_hitbox) == True:
                dmg_done = sword_damage
                hp -= dmg_done
                hit_time = time_run

                return [True, dmg_done, player_crit_chance]
            
            else:
                return [False, 0, 0]
        else:
            return [False, 0, 0]
    
    else:
        return [False, 0, 0]

def player_attacking_bow(elf, arrow, elf_number): #currently only works for attacking the elves
    global all_elves_hp
    global all_elves_hp, snowman_hp

    for pos in arrow:
        arrow_hitbox = pygame.Rect(pos[0], pos[1], 5, 10)
        elf_x = elf.elf_rect(0)
        elf_y = elf.elf_rect(1)
        elf_hitbox = pygame.Rect(elf_x, elf_y, 40, 40)
        arrow_hitbox = pygame.Rect(pos[0], pos[1], 5, 10) 

        if arrow_hitbox.colliderect(elf_hitbox):
            all_elves_hp[elf_number] -= bow_damage
            draw_text(f"{bow_damage}", text_font_small, (0, 0, 0), elf_x, elf_y)         


def player_draw_dmg(enemy_type, enemy, elf_number, enemy_x, enemy_y, hp): #only works for sword
    if enemy_type == "elf":
        hit = player_attacking("elf", enemy, elf_number, hp, 0, w, a, s, d)
        if hit[0] == True:
            if hit[2] == 1:
                all_hits.append([hit[1], time_run, 1, random.randint(-10, 10), random.randint(-10, 10), enemy])
                hp[elf_number] -= hit[1]
            else:
                all_hits.append([hit[1], time_run, 0, random.randint(-10, 10), random.randint(-10, 10), enemy])
                hp[elf_number] -= hit[1]
    
    elif enemy_type == "snowman":
        hit = player_attacking("snowman", enemy, 0, hp, pygame.Rect(enemy_x-25, enemy_y-25, 50, 50), w, a, s, d)
    
    elif enemy_type == "rudolph":
        hit = player_attacking("rudolph", enemy, 0, hp, pygame.Rect(enemy_x-25, enemy_y-25, 50, 50), w, a, s, d)
    
    elif enemy_type == "santa":
        hit = player_attacking("santa", enemy, 0, hp, pygame.Rect(enemy_x-25, enemy_y-25, 50, 50), w, a, s, d)
        
    if enemy_type == "snowman" or enemy_type == "rudolph" or enemy_type == "santa": 
        if hit[0] == True:
            if hit[2] == 1:
                all_hits.append([hit[1], time_run, 1, random.randint(-10, 10), random.randint(-10, 10), enemy])
                hp -= hit[1]
            else:
                all_hits.append([hit[1], time_run, 0, random.randint(-10, 10), random.randint(-10, 10), enemy])
                hp -= hit[1]
            

    for hit, time, crit, x_offset, y_offset, prev_enemy in all_hits:
        if time_run - time < 500 and prev_enemy == enemy:
            draw_text(str(hit), text_font_small, (0, 0, 0), enemy_x-x_offset, enemy_y-y_offset)
            
            if crit == 1:
                draw_text("CRIT", text_font, (0, 0, 0), enemy_x-x_offset, enemy_y-y_offset)

    return hp

def saving_new_file(file, room, enemy_max_hp, enemy_dead, player_x, player_y, candies, chest, player_hp, inventory, health_potion_num):
    global num_saves
    lines = {
        "room" : room,
        "enemy" : enemy_max_hp,
        "dead" : enemy_dead,
        "player_x": player_x,
        "player_y": player_y,
        "candies" : candies,
        "chest_opened" : chest,
        "player_hp" : player_hp,
        "inventory" : inventory,
        "health_potions" : health_potion_num
    }

    with open(file, "w") as f:
        json.dump(lines, f)
        f.close()

def load_old_save(file):
    with open(file, "r") as f:
        lines = json.load(f)
        f.close()

        room = lines["room"]
        enemy_max_hp = lines["enemy"]
        enemy_dead = lines["dead"]
        player_x = lines["player_x"]
        player_y = lines["player_y"]
        candies = lines["candies"]
        chest_opened = lines["chest_opened"]
        player_hp = lines["player_hp"]
        inventory = lines["inventory"]
        health_potion = lines["health_potions"]

    return [room, enemy_max_hp, enemy_dead, player_x, player_y, candies, chest_opened, player_hp, inventory, health_potion]

def draw_slider(screen, x, y, width, height, knob_x):
    # Draw the track
    pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height))
    # Draw the knob
    pygame.draw.circle(screen, (50, 150, 255), (knob_x, y + height // 2), knob_radius)
def get_volume_from_position(knob_x, slider_x, slider_width, min_volume, max_volume):
    relative_position = (knob_x - slider_x) / slider_width
    return min_volume + (max_volume - min_volume) * relative_position

# Christmas tree and elf initiation --- the single elf in room 2, not the ones summoned by the tree
tree = Christmas_Tree(WIDTH/2- 20, 100)
satan = Santa(320, 100)
elf = elves(WIDTH/2, 100)

def player_attack_bow(satan, arrow): #currently only works for attacking the elves
    global santa_hp

    for pos in arrow:
        arrow_hitbox = pygame.Rect(pos[0], pos[1], 5, 10)
        santa_x = satan.santa_rectangle()[0]
        santa_y = satan.santa_rectangle()[1]
        santa_hitbox = pygame.Rect(santa_x, santa_y, 40, 40)
        arrow_hitbox = pygame.Rect(pos[0], pos[1], 5, 10) 

        if arrow_hitbox.colliderect(santa_hitbox):
            santa_hp -= bow_damage
            draw_text(f"{bow_damage}", text_font_small, (0, 0, 0), santa_x, santa_y)
    
    return santa_hp


running = True
dragging = False

#GAME LOOP
while running:
    new_save_rect = pygame.Rect(0, 0, 0, 0)
    time_run = pygame.time.get_ticks()
    mouse_x, mouse_y = pygame.mouse.get_pos() # get the mouse position for the clicking of play button
    left_M_pressed, middle_M_pressed, right_M_pressed = pygame.mouse.get_pressed() # get state of mouse (pressed or not)
    volume_text = font.render(f"Volume: {current_volume:.2f}", True, (255, 255, 255))

    # EVENT HANDLING 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        # Pause Menu events 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and state == 3 and settings == False:
                state = 1
            elif event.key == pygame.K_ESCAPE and state == 3 and settings == True:
                settings = False
            elif event.key == pygame.K_ESCAPE and state == 1:
                state = 3
        
        #Settings events
        if settings == True and state == 3:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Change character settings
                if start_player_choice.collidepoint(mouse_x, mouse_y): 
                    player = start_player 
                    player_rotated = player 
                if other_player_choice.collidepoint(mouse_x, mouse_y): 
                    player = other_player
                    player_rotated = player
                # Volume Slider Effects
                if event.button == 1:
                # Check if the user clicked on the knob
                    mouse_x, mouse_y = event.pos
                    if abs(mouse_x - knob_x) <= knob_radius and abs(mouse_y - (slider_y + slider_height // 2)) <= knob_radius:
                        dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                # Move the knob with the mouse
                    mouse_x, _ = event.pos
                    knob_x = max(slider_x, min(mouse_x, slider_x + slider_width))
                    current_volume = get_volume_from_position(knob_x, slider_x, slider_width, min_volume, max_volume)
                    sound.set_volume(current_volume)

        if state == 1 and sound_time == 0:
            sound.play(-1)
            sound_time += 1
    
        # Store events 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and state == 1 and player_hitbox.colliderect(store_hitbox_rect): 
                if room in [1, 5, 7, 10]:
                    state = 4
                    item_bought = 0
            elif event.key == pygame.K_ESCAPE and state == 4 and confirmation == True:
                confirmation = False
            elif event.key == pygame.K_ESCAPE and state == 4: 
                state = 1
            # Purchase Confirmation
            if confirmation == False and upgrades == True and event.key == pygame.K_y:
                if item_number == 0 and candies >= prices[item_number]:
                    sword_damage += 2500
                    upgrades = False
                    candies -= prices[item_number]
                    item_bought = 1
                elif item_number == 1 and candies >= prices[item_number]:
                    bow_damage += 500
                    upgrades = False
                    candies -= prices[item_number]
                    item_bought = 1
                else:
                    upgrades = False
                    item_bought = 2
                    state = 1
            # Purchase Confirmation (NON-UPGRADES)           
            elif confirmation == True and event.key == pygame.K_y and upgrades == False:
                if candies >= prices[item_number]:
                    inventory[item_number] = items[item_number]
                    candies -= prices[item_number]
                    if inventory[2] == items[2]:
                        health_potion_num += 1
                    confirmation = False
                    item_bought = 1
                else:
                    state = 1
                    confirmation = False
                    item_bought = 2
        
        # Inventory events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 and inventory[0] == "SWORD":
                player_equipped = "sword"
            elif event.key == pygame.K_2 and inventory[1] == "BOW": #can only equip one at a time
                player_equipped = "bow"
            if event.key == pygame.K_3 and inventory[2] == "HEALTH":
                player_equipped = "healthpot"
            
        # Player attacking events - resets all variables / initiates them always to 0 repeatedly
        player_to_mouse_norm = [0, 0] #resets vector for attacking direction with a sword
        player_x_offset = 0 #for the dmg number on screen
        player_y_offset = 0 #for the dmg number on screen

        # changes tutorial screen when clicked
        if state == 0.5:
            if event.type == pygame.MOUSEBUTTONDOWN and time_run - tutorial_time_pressed >= 150:
                help_image += 1
                tutorial_time_pressed = time_run
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    state = 1
        
        if state == 1:
            sound.play(-1)
            if room == 3 and tree_dialogue_done == False:
                if event.type == pygame.MOUSEBUTTONDOWN and time_run - tree_dialogue_time >= 150:
                    tree_dialogue_num += 1
                    tree_dialogue_time = time_run
            
            if room == 6 and snowman_dialogue_done == False: 
                if event.type == pygame.MOUSEBUTTONDOWN and time_run - snowman_dialogue_time >= 150: 
                    snowman_dialogue_num += 1 
                    snowman_dialogue_time = time_run
            
            if room == 9 and rudolph_dialogue_done == False:
                if event.type == pygame.MOUSEBUTTONDOWN and time_run - rudolph_dialogue_time >= 150: 
                        rudolph_dialogue_num += 1 
                        rudolph_dialogue_time = time_run
            
            if room == 11: 
                if event.type == pygame.MOUSEBUTTONDOWN and time_run - sled_dialogue_time >= 150: 
                    sled_dialogue_num += 1 
                    sled_dialogue_time = time_run
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and sled_dialogue_done == True: 
                    if player_hitbox.colliderect(pygame.Rect(sled_xy[0][0], sled_xy[0][1], 124, 15)) and sled_xy[0] != sled_done[0]: 
                        sled_moving[0] = True 
                    if player_hitbox.colliderect(pygame.Rect(sled_xy[1][0], sled_xy[1][1], 65, 36)) and sled_xy[1] != sled_done[1]: 
                        sled_moving[1] = True 
                    if player_hitbox.colliderect(pygame.Rect(sled_xy[2][0], sled_xy[2][1], 124, 15)) and sled_xy[2] != sled_done[2]: 
                        sled_moving[2] = True 
                
            if room == 13 and end_dialogue_done == False:
                if event.type == pygame.MOUSEBUTTONDOWN and time_run - end_dialogue_time >= 150: 
                    end_dialogue_num += 1 
                    end_dialogue_time = time_run
            
            if end == True:
                player_equipped = ""
                if event.type == pygame.MOUSEBUTTONDOWN:
                    end = False
                    pygame.quit()


        # handling keys for movement (can run multiple at a time)
        if state == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player_rotated = pygame.transform.rotate(player, 0) #rotates according to the original image, not the current
                    moving[0] = 1
                    w = True #the variables for which way the bow will shoot
                    a = False
                    s = False
                    d = False

                if event.key == pygame.K_a:
                    player_rotated = pygame.transform.rotate(player, 90)
                    moving[1] = 1
                    w = False
                    a = True
                    s = False
                    d = False

                if event.key == pygame.K_s:
                    player_rotated = pygame.transform.rotate(player, 180)
                    moving[2] = 1
                    w = False
                    a = False
                    s = True
                    d = False
                    
                if event.key == pygame.K_d:
                    player_rotated = pygame.transform.rotate(player, -90)
                    moving[3] = 1
                    w = False
                    a = False
                    s = False
                    d = True
            
            elif event.type == pygame.KEYUP: 
                if event.key == pygame.K_w:
                    moving[0] = 0
                if event.key == pygame.K_a:
                    moving[1] = 0
                if event.key == pygame.K_s:
                    moving[2] = 0
                if event.key == pygame.K_d:
                    moving[3] = 0
            
            if event.type == pygame.MOUSEBUTTONDOWN: # can do at same time as moving
                player_x_offset = random.randint(-10, 10)
                player_y_offset = random.randint(-10, 10)
            
            # save button pressed
            if ((event.type == pygame.KEYDOWN and event.key == pygame.K_h) or 
                (save_button.collidepoint(mouse_x, mouse_y) == True and left_M_pressed == True) and 
                saving == False 
                and state == 1):
                saving = True
            
            #x out of loading / saving screen
            if saving == True and event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                saving = False
            
        if state == -1 and event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            state = 0
                    
             
    font = pygame.font.Font(None, 30)
    font1 = pygame.font.Font(None, 20)
    hp_text = font.render(f"Health: {player_hp}", True, (0, 0, 0))
    potion_text = font.render(f"{health_potion_num}", True, (255, 255, 255))

    # does the continuous moving
    if moving[0] == 1: #W: up
        new_player_y = player_y - 5
        new_player_rect = pygame.Rect(player_x, player_y - 5, 30, 25) #creates imaginary player rect after moving
        for wall in walls:
            if new_player_rect.colliderect(pygame.Rect(wall)): #checks if imaginary player rect hits wall
                new_player_y = player_y #if it hits, don't move the player
                break
        player_y = new_player_y #doesn't change if does hit, but changes if it hits
            
    if moving[1] == 1: #A: left
        new_player_x = player_x - 5
        new_player_rect = pygame.Rect(player_x - 5, player_y, 30, 25)
        for wall in walls:
            if new_player_rect.colliderect(pygame.Rect(wall)):
                new_player_x = player_x
                break
        player_x = new_player_x
        
    if moving[2] == 1: #S: down
        new_player_y = player_y + 5
        new_player_rect = pygame.Rect(player_x, player_y + 5, 30, 25)
        for wall in walls:
            if new_player_rect.colliderect(pygame.Rect(wall)):
                new_player_y = player_y
                break
        player_y = new_player_y
            
    if moving[3] == 1: #D: right
        new_player_x = player_x + 5
        new_player_rect = pygame.Rect(player_x + 5, player_y, 30, 25)
        for wall in walls:
            if new_player_rect.colliderect(pygame.Rect(wall)):
                new_player_x = player_x
                break
        player_x = new_player_x


    # GAME STATE UPDATES -----------------------------------------------------------------------------------------------------------------
    
    if state == 1: 
        # Update player hitbox 
        player_hitbox = pygame.Rect(player_x, player_y + 5, 30, 25)
        santa_hitbox = santa.get_rect()

        if room == 2:
            elf.vector_calculations(0)
            player_hp = elf.attack(player_hp)
        
        if room == 4:
            if collected_4 == False:
                dmg_buff_rect = pygame.Rect(105, 310, 40, 40)

            if player_hitbox.colliderect(dmg_buff_rect):
                dmg_buff_rect = pygame.Rect(50, 50, 10, 10)
                collected_4 = True
                sword_damage *= dmg_bonus
                bow_damage *= dmg_bonus
                collected_4_time = time_run

        
        if room == 6: 
            if snowman_hp > 0: 
                # Snowman moving 
                snowman_x += snowman_speed 
                if snowman_x < 150 or snowman_x > 500: 
                    snowman_speed *= -1 

                if snowman_dialogue_done == True: 
                    snowman_hitbox = pygame.Rect(snowman_x - 25, snowman_y - 25, 50, 50)

                 # When player collides with snowman
                if player_hitbox.colliderect(snowman_hitbox): 
                    damage_taken = snowman_hit("snowman")
                    player_hp -= damage_taken
                    player_damage.append([time_run, damage_taken, random.randrange(0, 20), random.randrange(0, 20)])
            
                
                # Snowman shooting 
                if snowman_timer + 1200 < time_run: 
                    snowballs.append([snowman_x, snowman_y])
                    snowman_timer = time_run 
                for i in range(len(snowballs)): 
                    direction = snowball_direction(player_x, player_y, snowman_x, snowman_y)
                    snowballs[i][0] += direction[0] * 20
                    snowballs[i][1] += direction[1] * 20
                    if snowballs[i][1] > 360 or snowballs[i][1] < 130 or snowballs[i][0] < 100 or snowballs[i][0] > 530:
                        snowballs.pop(0)
                # When snowballs collide with player
                for snowball in snowballs: 
                    if player_hitbox.colliderect(pygame.Rect(snowball[0] - 12, snowball[1] - 12, 24, 24)): 
                        damage_taken = snowman_hit("snowball")
                        player_hp -= damage_taken
                        player_damage.append([time_run, damage_taken, random.randrange(0, 20), random.randrange(0, 20)])
                    
                    else: 
                        snowman_hitbox = pygame.Rect(-1000, -1000, 50, 50)


        if room == 8:
            if len(room_8_elves) < 5:
                all_elves_hp.append(5000)
                room_8_elves.append(elves(random.randint(200, 400), random.randint(100, 150)))
                room_8_elves_num.append(len(all_elves_hp)-1)
            
            if len(room_8_elves) == 5:
                for i in range(len(room_8_elves)):
                    elf = room_8_elves[i]
                    elf.vector_calculations(room_8_elves_num[i])
                    player_hp = elf.attack(player_hp)
            
        if room == 9:
        # Rudolph
            if rudolph_dialogue_done == False:
                player_x = 320
                player_y = 320
            if rudolph_hp > 0 and rudolph_dialogue_done == True:
                rudolph_hitbox = pygame.Rect(rudolph_x-25, rudolph_y-25, 50, 50)
                time_count += 1
                if time_count == 1:
                    rudolph_timer = time_run
                    # Rudolph Charge
                if time_run - rudolph_timer >= 2000:
                    startup_time_count += 1
                    if startup_time_count == 1:
                        rudolph_charge_timer = time_run
                        rudolph_charge = True
                if rudolph_charge == True and time_run - rudolph_charge_timer < 1500:
                    rudolph_direction = rudolph_move(player_x, player_y, rudolph_x, rudolph_y)
                    rudolph_x += rudolph_direction[0] * 0
                    rudolph_y += rudolph_direction[1] * 0
                    rudolph_direction = rudolph_move(player_x, player_y, rudolph_x, rudolph_y)
                if rudolph_charge == True and time_run - rudolph_charge_timer >= 1500:
                    rudolph_x += rudolph_direction[0] * 20
                    rudolph_y += rudolph_direction[1] * 20
                    if rudolph_hitbox.colliderect(player_hitbox):
                        player_hp -= rudolph_hit("charge")
                    if time_run - rudolph_charge_timer >= 2000:
                        rudolph_charge = False
                        time_count = 0
                        startup_time_count = 0
                    # Base movement
                if rudolph_charge == False:
                    rudolph_direction = rudolph_move(player_x, player_y, rudolph_x, rudolph_y)
                    rudolph_x += rudolph_direction[0] * 4
                    rudolph_y += rudolph_direction[1] * 4
                    if rudolph_hitbox.colliderect(player_hitbox):
                        player_hp -= rudolph_hit("rudolph")
                rudolph_hp = player_draw_dmg("rudolph", 69, 420, rudolph_x, rudolph_y, rudolph_hp)
                    
                    # Sprite Updating
                if rudolph_direction[0] > -0.5 and rudolph_direction[0] < 0 and rudolph_direction[1] < -0.5: #Up Up left 
                    rudolph_north = True
                    rudolph_west = False
                    rudolph_south = False
                    rudolph_east = False
                elif rudolph_direction[0] > 0 and rudolph_direction[0] < 0.5 and rudolph_direction[1] < -0.5: #Up Up right 
                    rudolph_north = True
                    rudolph_west = False
                    rudolph_south = False
                    rudolph_east = False
                elif rudolph_direction[0] < -0.5 and rudolph_direction[1] < 0 and rudolph_direction[1] > -0.5: #Left Left up  
                    rudolph_north = False
                    rudolph_west = True
                    rudolph_south = False
                    rudolph_east = False
                elif rudolph_direction[0] < -0.5 and rudolph_direction[1] > 0 and rudolph_direction[1] < 0.5: #Left Left down  
                    rudolph_north = False
                    rudolph_west = True
                    rudolph_south = False
                    rudolph_east = False
                elif rudolph_direction[0] > -0.5 and rudolph_direction[0] < 0 and rudolph_direction[1] > 0.5: #Down Down left  
                    rudolph_north = False
                    rudolph_west = False
                    rudolph_south = True
                    rudolph_east = False
                elif rudolph_direction[0] > 0 and rudolph_direction[0] < 0.5 and rudolph_direction[1] > 0.5: #Down Down right  
                    rudolph_north = False
                    rudolph_west = False
                    rudolph_south = True
                    rudolph_east = False
                elif rudolph_direction[0] > 0.5 and rudolph_direction[1] > 0 and rudolph_direction[1] < 0.5: #Right Right down  
                    rudolph_north = False
                    rudolph_west = False
                    rudolph_south = False
                    rudolph_east = True
                elif rudolph_direction[0] > 0.5 and rudolph_direction[1] < 0 and rudolph_direction[1] > -0.5: #Right Right up  
                    rudolph_north = False
                    rudolph_west = False
                    rudolph_south = False
                    rudolph_east = True
            elif rudolph_hp <= 0:
                rudolph_x = -1000000
        
        if room == 11: 
            for i in range(3): 
                if sled_moving[i] == True: 
                    sled_direction = snowball_direction(sled_done[i][0], sled_done[i][1], sled_xy[i][0], sled_xy[i][1])
                    sled_xy[i][0] += sled_direction[0] * 5 
                    sled_xy[i][1] += sled_direction[1] * 5
    
            if sled_moving[0] == True: 
                if sled_xy[0][0] > sled_done[0][0] or sled_xy[0][1] > sled_done[0][1]: 
                    sled_xy[0][0] = sled_done[0][0]
                    sled_xy[0][1] = sled_done[0][1]
                    sled_moving[0] = False 
                    sled_pass[0] = True 
            if sled_moving[1] == True: 
                if sled_xy[1][0] < sled_done[1][0] or sled_xy[1][1] > sled_done[1][1]: 
                    sled_xy[1][0] = sled_done[1][0]
                    sled_xy[1][1] = sled_done[1][1]
                    sled_moving[1] = False 
                    sled_pass [1] = True 
            if sled_moving[2] == True: 
                if sled_xy[2][0] > sled_done[2][0] or sled_xy[2][1] < sled_done[2][1]: 
                    sled_xy[2][0] = sled_done[2][0]
                    sled_xy[2][1] = sled_done[2][1]
                    sled_moving[2] = False 
                    sled_pass[2] = True


        
        if room == 13:
            if end_dialogue_done == False:
                player_x = 320
                player_y = 320
            elif end_dialogue_done == True:
                if player_hitbox.colliderect(end_hitbox):
                    end = True
    

    # Settings Button in Pause Menu
    if settings_bar_rect.collidepoint(mouse_x, mouse_y) and left_M_pressed == True and state == 3 and settings == False:
        settings = True
    
    player_hitbox = pygame.Rect(player_x, player_y + 5, 30, 25) 
    
    # Collect candy canes 
    for i in range(len(cane_rects)): 
        if player_hitbox.colliderect(cane_rects[i]): 
            candies += 1 
            cane_rects[i] = pygame.Rect(-100, -100, 30, 20)
            cane_list[i] = [-100, -100]
    
    # Go through doors and change rooms 
    if (player_hitbox.colliderect(door_rect) and 
    (room != 3 or (room == 3 and tree_hp <= 0)) and # Christmas tree room 
    (room != 2 or (room == 2 and all_elves_hp[0] <= 0)) and # Elf room 
    (room != 9 or (room == 9 and rudolph_hp <= 0)) and # Rudolph room 
    (room != 6 or (room == 6 and snowman_hp <= 0)) and # Snowman room 
    (room != 11 or (room == 11 and sled_pass == [True, True, True]))): # Sled room 
        room += 1 
        player_x = WIDTH/2
        player_y = 340
        elves_rect = []
        for i in range(10): 
            x = random.randrange(100, 500) 
            y = random.randrange(125, 350)
            cane_list[i] = [x, y]
            rect = pygame.Rect(x, y + 10, 30, 20)
            cane_rects[i] = rect
        pygame.time.wait(250)

        if room == 12:
            for i in range(5): #creates new elves for Santa
                all_elves_hp.append(5000)
    
    # Buying store items 
    if state == 4:
        if items_square_rect[0].collidepoint(mouse_x,mouse_y) and left_M_pressed == True and confirmation == False:
            item_number = 0
            if inventory[0] == items[0]:
                upgrades = True
            else:
                confirmation = True
        elif items_square_rect[1].collidepoint(mouse_x,mouse_y) and left_M_pressed == True and confirmation == False:
            item_number = 1
            if inventory[1] == items[1]:
                upgrades = True
            else:
                confirmation = True
        elif items_square_rect[2].collidepoint(mouse_x,mouse_y) and left_M_pressed == True and confirmation == False:
            item_number = 2
            confirmation = True
 
    # Start screen 
    if state == 0:
        screen.blit(start_screen, pygame.Rect(0, 0, WIDTH, HEIGHT))
        screen.blit(start_playing, (0, 0, WIDTH, HEIGHT))
        pygame.draw.rect(screen, (0, 0, 0), (217, 300, 208, 100))
        draw_text("LOAD", text_font, (255, 255, 255), 280, 340)
    
        if start_playing_rect.collidepoint(mouse_x, mouse_y) and left_M_pressed == True:
            state = 0.5 #tutorial state
        
        if load_rect.collidepoint(mouse_x, mouse_y) and left_M_pressed == True and time_run - between_screen_time >= 200:
            state = -1
            between_screen_time = time_run
    
    if state == -1 and time_run - between_screen_time >= 500:
        if num_saves >= 1:
            if save_1_rect.collidepoint(mouse_x, mouse_y) == True and left_M_pressed == True:
                all_info = load_old_save("save_1.json") 
                #returns [room, enemy_max_hp, enemy_dead, player_x, player_y, candies, chest_opened, player_hp, inventory, health_potions]
                room = all_info[0]
                player_x = all_info[3]
                player_y = all_info[4]
                candies = all_info[5]
                player_hp = all_info[7]
                inventory = all_info[8]
                health_potion_num = all_info[9]
                state = 1

                if room == 2:
                    if all_info[2] == False: #if the enemy is alive when saved
                        all_elves_hp[0] = all_info[1]
                    if all_info[2] == True:
                        all_elves_hp[0] = 0
                if room == 3:
                    if all_info[2] == False:
                        tree_hp = all_info[1]
                    if all_info[2] == True:
                        tree_hp = 0
                if room == 6:
                    if all_info[2] == False:
                        snowman_hp = all_info[1]
                    if all_info[2] == True:
                        snowman_hp = 0
                if room == 8:
                    if all_info[2] == False:
                        pass #make if elves dead variable for here
                    if all_info[2] == True:
                        pass
                if room == 9:
                    if all_info[2] == False:
                        rudolph_hp = all_info[1]
                    if all_info[2] == True:
                        rudolph_hp = 0
                if room == 12:
                    if all_info[2] == False:
                        santa_hp = all_info[1]
                    if all_info[2] == True:
                        santa_hp = 0

                
                if all_info[6] == False:
                    if room == 3:
                        christmas_chest_opened = False
                    else:
                        christmas_chest_opened = True

                    if room == 6:
                        snowman_chest_opened = False
                    else:
                        snowman_chest_opened = True

                    if room == 9:
                        rudolph_chest_opened = False
                    else:
                        rudolph_chest_opened = True
                
                
        if num_saves == 2:
            if save_2_rect.collidepoint(mouse_x, mouse_y) == True and left_M_pressed == True:
                all_info = load_old_save("save_2.json") 
                #returns [room, enemy_max_hp, enemy_dead, player_x, player_y, candies, chest_opened, player_hp]
                room = all_info[0]
                player_x = all_info[3]
                player_y = all_info[4]
                candies = all_info[5]
                player_hp = all_info[7]
                inventory = all_info[8]
                health_potion_num = all_info[9]
                state = 1

                if room == 2:
                    if all_info[2] == False: #if the enemy is alive when saved
                        all_elves_hp[0] = all_info[1]
                    if all_info[2] == True:
                        all_elves_hp[0] = 0
                if room == 3:
                    if all_info[2] == False:
                        tree_hp = all_info[1]
                    if all_info[2] == True:
                        tree_hp = 0
                if room == 6:
                    if all_info[2] == False:
                        snowman_hp = all_info[1]
                    if all_info[2] == True:
                        snowman_hp = 0
                if room == 8:
                    if all_info[2] == False:
                        pass #make if elves dead variable for here
                    if all_info[2] == True:
                        pass
                if room == 9:
                    if all_info[2] == False:
                        rudolph_hp = all_info[1]
                    if all_info[2] == True:
                        rudolph_hp = 0
                if room == 12:
                    if all_info[2] == False:
                        santa_hp = all_info[1]
                    if all_info[2] == True:
                        santa_hp = 0

                
                if all_info[6] == False:
                    if room == 3:
                        christmas_chest_opened = False
                    else:
                        christmas_chest_opened = True

                    if room == 6:
                        snowman_chest_opened = False
                    else:
                        snowman_chest_opened = True

                    if room == 9:
                        rudolph_chest_opened = False
                    else:
                        rudolph_chest_opened = True

    
    # resets to start playing screen but keeps the game running in the background still (for if player wants to load in prev run)
    if state == 3 and settings == False:
        playing_rect = pygame.Rect(continue_playing_rect)

        if playing_rect.collidepoint(mouse_x, mouse_y) == True and left_M_pressed == True and time_run - between_screen_time >= 200:
            state = 0
            between_screen_time = time_run
                    

    #the floor the player is able to move on (87, 100) -> (525, 350)
    if player_x < 87:
        player_x += 5
    if player_x > 525:
        player_x -= 5
    if player_y < 100:
        player_y += 5
    if player_y > 350:
        player_y -= 5
    
    # Bow
    if player_equipped == "bow" and left_M_pressed == True and time_run - bow_cooldown >= 50:
        if w == True: #WASD
            arrow_up = [player_x,player_y-5]
            arrows_up.append(arrow_up)
        if a == True:
            arrow_left = [player_x-5,player_y]
            arrows_left.append(arrow_left)
        if s == True:
            arrow_down = [player_x,player_y+10]
            arrows_down.append(arrow_down)
        if d == True:
            arrow_right = [player_x+10,player_y]
            arrows_right.append(arrow_right)
        bow_cooldown = time_run

    
    # Health Potion
    if player_equipped == "healthpot" and left_M_pressed == True and time_run - health_cooldown >= 1000:
        if health_potion_num > 0:
            player_hp += 20000
            if player_hp > 100000:
                player_hp = 100000
            health_potion_num -= 1
            health_cooldown = time_run
    
    #saving and loading
    if saving == True:
        if num_saves == 0:
            new_save_rect = pygame.Rect(50, 50, WIDTH-100, 100)
            new_save_position = [50, 50, WIDTH-100, 100]

        if num_saves >= 1:
            new_save_rect = pygame.Rect(50, 200, WIDTH-100, 100)
            new_save_position = [50, 200, WIDTH-100, 100]

        if num_saves == 2:
            new_save_rect = pygame.Rect(50, 350, WIDTH-100, 100)
            new_save_position = [50, 350, WIDTH-100, 100]
    
    #setting up info to save
    if saving == True:
        if ((new_save_rect.collidepoint(mouse_x, mouse_y) or 
        (num_saves == 2 and override_rect_1.collidepoint(mouse_x, mouse_y) == True) or
        (num_saves == 2 and override_rect_2.collidepoint(mouse_x, mouse_y) == True)) and left_M_pressed == True
        ):
            if time_run - last_time_saved >= 200:
                enemy_max_hp = None
                enemy_dead = None
                chest = None
                enemy_dead_prob = None
                if room == 2:
                    enemy_max_hp = 5000
                    enemy_dead = all_elves_hp[0]
                elif room == 3:
                    enemy_max_hp = 100000
                    enemy_dead = tree_hp
                    chest = christmas_chest_opened
                elif room == 6:
                    enemy_max_hp = 200000
                    enemy_dead = snowman_hp
                    chest = snowman_chest_opened
                elif room == 8:
                    enemy_max_hp = 5000
                    enemy_dead_prob = all_elves_hp[len(all_elves_hp)-5:-1]
                elif room == 9:
                    enemy_max_hp = 250000
                    enemy_dead = rudolph_hp
                    chest = rudolph_chest_opened
                elif room == 12:
                    enemy_max_hp = 500000
                    enemy_dead = santa_hp
                    #need santa chest to be made still
                
                if enemy_dead != None:
                    if enemy_dead <= 0:
                        enemy_dead = True
                    else:
                        enemy_dead = False
                
                if room == 8:
                    for hp in enemy_dead_prob:
                        if hp <= 0:
                            enemy_dead = True

                if (num_saves == 0 or 
                    (num_saves == 2 and override_rect_1.collidepoint(mouse_x, mouse_y) == True)):
                    saving_new_file("save_1.json", room, enemy_max_hp, enemy_dead, player_x, player_y, candies, chest, player_hp, inventory, health_potion_num)
                    if num_saves == 0:
                        num_saves += 1
                        with open("all_save_files.txt", "w") as f: #save number of save files to txt
                            f.write(str(num_saves))
                            f.close()
                elif (num_saves == 1 or 
                    (num_saves == 2 and override_rect_2.collidepoint(mouse_x, mouse_y) == True)):
                    saving_new_file("save_2.json", room, enemy_max_hp, enemy_dead, player_x, player_y, candies, chest, player_hp, inventory, health_potion_num)
                    if num_saves == 1:
                        num_saves += 1
                        with open("all_save_files.txt", "w") as f: #save number of save files to txt
                            f.write(str(num_saves))
                            f.close()
                
                last_time_saved = time_run
    
    # x-ing out of window for loading and saving files
    if state == -1 or saving == True:
        x_rect = pygame.Rect(10, 10, 40, 40)
    if state == -1:
        if x_rect.collidepoint(mouse_x, mouse_y) and left_M_pressed == True:
            state = 0
    
    if saving == True:
        if x_rect.collidepoint(mouse_x, mouse_y) and left_M_pressed == True:
            saving = False


    # DRAWING -----------------------------------------------------------------------------------------------------------------------

    #drawing the save files (at beginning of game)
    if state == -1:
        screen.fill((230, 200, 190))
        if num_saves == 0:
            draw_text("No save files", text_font, (0, 0, 0), WIDTH/2-90, HEIGHT/2-20)

        if num_saves >= 1:
            pygame.draw.rect(screen, (0, 0, 0), (50, 50, WIDTH/2-75, HEIGHT-100))
        
        if num_saves == 2:
            pygame.draw.rect(screen, (0, 0, 0), (WIDTH/2+25, 50, WIDTH/2-75, HEIGHT-100))

    # draws the tutorial images
    if state == 0.5:
        screen.fill((0, 0, 0))
        draw_text("press Q to quit tutorial and start playing", text_font_small, (255, 255, 255), 5, 5)

        if help_image == 1:
            screen.blit(tutorial_1, (30, 30))
            pygame.draw.rect(screen, (255, 0, 0), (60, 41, 220-60, 98-41), 3)
            pygame.draw.line(screen, (255, 0, 0), (178, 99), (246, 156), 3)
            draw_text("health and owned currency", text_font_small, (0, 0, 0), 140, 160)
            draw_text("1/4", text_font_small, (255, 255, 255), WIDTH-30, 5)

            pygame.draw.rect(screen, (255, 0, 0), (131, 313, 256-223, 316-290), 3)
            pygame.draw.line(screen, (255, 0, 0), (140, 313), (150, 270), 3)
            draw_text("store (press e to open)", text_font_smaller, (0, 0, 0), 140, 250)

            pygame.draw.rect(screen, (255, 0, 0), (453, 33, 608-453, 78-33), 3)
            pygame.draw.line(screen, (255, 0, 0), (569, 78), (569, 128), 3)
            draw_text("inventory (press 1, 2 or", text_font_smaller, (0, 0, 0), 420, 134)
            draw_text("3 to equip;", text_font_smaller, (0, 0, 0), 470, 148)
            draw_text("click to use)", text_font_smaller, (0, 0, 0), 465, 163)

            pygame.draw.rect(screen, (255, 0, 0), (372, 215, 464-416, 184-148), 3)
            pygame.draw.line(screen, (255, 0, 0), (417, 226), (430, 240), 3)
            draw_text("collect as currency", text_font_small, (0, 0, 0), 370, 245)
        
        if help_image == 2:
            screen.blit(tutorial_2, (30, 30))
            pygame.draw.rect(screen, (255, 0, 0), (347, 143, 386-330, 251-202), 3)
            pygame.draw.line(screen, (255, 0, 0), (347, 143+(251-202)), (312, 295), 3)
            draw_text("in the store click squares", text_font_small, (0, 0, 0), 220, 190)
            draw_text("to open buy prompt", text_font_small, (0, 0, 0), 250, 210)
            draw_text("/ see information on items", text_font_small, (0, 0, 0), 220, 230)
            draw_text("2/4", text_font_small, (0, 0, 0), WIDTH-30, 5)
        
        if help_image == 3:
            screen.blit(tutorial_3, (30, 30))
            pygame.draw.rect(screen, (255, 0, 0), (301, 120, 363-301, 145-120), 3)
            pygame.draw.line(screen, (255, 0, 0), (336, 145), (336, 193), 3)
            draw_text("damage done by the player is black coloured", text_font_small, (0, 0, 0), 150, 198)
            draw_text("left click to attack", text_font_small, (0, 0, 0), 190, 220)
            draw_text("3/4", text_font_small, (255, 255, 255), WIDTH-30, 5)
            
        
        if help_image == 4:
            screen.blit(tutorial_4, (30, 30))
            pygame.draw.rect(screen, (255, 0, 0), (254, 126, 311-254, 152-254), 3)
            pygame.draw.line(screen, (255, 0, 0), (313, 144), (380, 170), 3)
            draw_text("damage done by the enemies is red coloured", text_font_small, (0, 0, 0), 120, 175)
            draw_text("4/4", text_font_small, (255, 255, 255), WIDTH-30, 5)


        if help_image == 5:
            state = 1

    
    # Playing the actual game 
    if state == 1:
        screen.fill((255,255,255))
        screen.blit(background, (0, 0))
        screen.blit(player_rotated, (player_x, player_y))
        screen.blit(hp_text, (50, 20))
        draw_text(str(candies), text_font, (0, 0, 0), 80, 45)
        screen.blit(cane, (50, 40))


        # Specific rooms to draw candy canes in 
        if room in [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11]: 
            for candy in cane_list: 
                screen.blit(cane, (candy[0], candy[1]))
        else: 
            for i in range(10): 
                cane_rects[i] = pygame.Rect(-100, -100, 30, 20)
        
        # Bow
        if player_equipped == "bow":
            for i in arrows_up:
                pygame.draw.ellipse(screen, (0,0,0), (i[0],i[1],5,10))
            for i in arrows_left:
                pygame.draw.ellipse(screen, (0,0,0), (i[0],i[1],5,10))
            for i in arrows_down:
                pygame.draw.ellipse(screen, (0,0,0), (i[0],i[1],5,10))
            for i in arrows_right:
                pygame.draw.ellipse(screen, (0,0,0), (i[0],i[1],5,10))
        
        
        if player_equipped == "bow":
            for pos in arrows_up:
                pos[1] -= 30
                arrow_hitbox = pygame.Rect(pos[0],pos[1],5,10)

                if room == 2:
                    elf_hitbox = pygame.Rect(elf.elf_rect(0), elf.elf_rect(1), 35,35)
                    if arrow_hitbox.colliderect(elf_hitbox):
                        all_elves_hp[0] -= bow_damage
                        draw_text(f"{bow_damage}", text_font_small, (0, 0, 0), elf.elf_rect(0), elf.elf_rect(1))
                
                if room == 6: 
                    if arrow_hitbox.colliderect(snowman_hitbox): 
                        snowman_hp -= bow_damage
                        snowman_damage.append([time_run, random.randrange(-50, 0), random.randrange(-30, 20), bow_damage])
                
                if room == 9:
                    if arrow_hitbox.colliderect(rudolph_hitbox) and rudolph_dialogue_done == True:
                        rudolph_hp -= bow_damage
                        draw_text(f"{bow_damage}", text_font_small, (0, 0, 0), rudolph_x, rudolph_y)

                if room == 12:
                    if arrow_hitbox.colliderect(santa_hitbox):
                        santa_hp -= bow_damage
                        draw_text(f"{bow_damage}", text_font_small, (0, 0, 0), santa)
                    
            for pos in arrows_left:
                pos[0] -= 30
                arrow_hitbox = pygame.Rect(pos[0],pos[1],5,10)

                if room == 2:
                    elf_hitbox = pygame.Rect(elf.elf_rect(0), elf.elf_rect(1), 35,35)
                    if arrow_hitbox.colliderect(elf_hitbox):
                        all_elves_hp[0] -= bow_damage
                        draw_text(f"{bow_damage}", text_font_small, (0, 0, 0), elf.elf_rect(0), elf.elf_rect(1))
                
                if room == 6: 
                    if arrow_hitbox.colliderect(snowman_hitbox): 
                        snowman_hp -= bow_damage
                        snowman_damage.append([time_run, random.randrange(-50, 0), random.randrange(-30, 20), bow_damage])
                    
                
                if room == 9:
                    if arrow_hitbox.colliderect(rudolph_hitbox) and rudolph_dialogue_done == True:
                        rudolph_hp -= bow_damage
                        draw_text(str(bow_damage), text_font_small, (0, 0, 0), rudolph_x, rudolph_y)
                    
            for pos in arrows_down:
                pos[1] += 30
                arrow_hitbox = pygame.Rect(pos[0],pos[1],5,10)

                if room == 2:
                    elf_hitbox = pygame.Rect(elf.elf_rect(0), elf.elf_rect(1), 35,35)
                    if arrow_hitbox.colliderect(elf_hitbox):
                        all_elves_hp[0] -= bow_damage
                        draw_text(f"{bow_damage}", text_font_small, (0, 0, 0), elf.elf_rect(0), elf.elf_rect(1))

                if room == 6: 
                    if arrow_hitbox.colliderect(snowman_hitbox): 
                        snowman_hp -= bow_damage
                        snowman_damage.append([time_run, random.randrange(-50, 0), random.randrange(-30, 20), bow_damage])
                
                if room == 9:
                    if arrow_hitbox.colliderect(rudolph_hitbox) and rudolph_dialogue_done == True:
                        rudolph_hp -= bow_damage
                        draw_text(f"{bow_damage}", text_font_small, (0, 0, 0), rudolph_x, rudolph_y)

            for pos in arrows_right:
                pos[0] += 30
                arrow_hitbox = pygame.Rect(pos[0],pos[1],5,10)

                if room == 2:
                    elf_hitbox = pygame.Rect(elf.elf_rect(0), elf.elf_rect(1), 35,35)
                    if arrow_hitbox.colliderect(elf_hitbox):
                        all_elves_hp[0] -= bow_damage
                        draw_text(f"{bow_damage}", text_font_small, (0, 0, 0), elf.elf_rect(0), elf.elf_rect(1))

                if room == 6: 
                    if arrow_hitbox.colliderect(snowman_hitbox): 
                        snowman_hp -= bow_damage
                        snowman_damage.append([time_run, random.randrange(-50, 0), random.randrange(-30, 20), bow_damage])
                
                if room == 9:
                    if arrow_hitbox.colliderect(rudolph_hitbox) and rudolph_dialogue_done == True:
                        rudolph_hp -= bow_damage
                        draw_text(f"{bow_damage}", text_font_small, (0, 0, 0), rudolph_x, rudolph_y)

        # Store room 
        if room in [1, 5, 7, 10]:
             screen.blit(store, store_hitbox_rect)

        # Room with an elf 
        if room == 2: 
            elf.draw_elf()

            if player_equipped == "sword":
                player_draw_dmg("elf", elf, 0, elf.elf_rect(0), elf.elf_rect(1), all_elves_hp)
        
        # Room with Christmas Tree
        if room == 3:
            if tree_hp > 0:
                all_creatures = tree.summon() # this needs to be shifted over
                tree.draw()
                for i in range(len(all_creatures)):
                    if player_equipped == "sword":
                        player_draw_dmg("elf", all_creatures[i], i+1, all_creatures[i].elf_rect(0), all_creatures[i].elf_rect(1), all_elves_hp)
                        
                    if player_equipped == "bow":
                        player_attacking_bow(all_creatures[i], arrows_up, i+1)
                        player_attacking_bow(all_creatures[i], arrows_right, i+1)
                        player_attacking_bow(all_creatures[i], arrows_down, i+1)
                        player_attacking_bow(all_creatures[i], arrows_left, i+1)

                if tree_dialogue_done == False:
                    screen.blit(dialogue_box, (20, HEIGHT/2))
                    if tree_dialogue_num == 0:
                        draw_text("AARRRGGHGHGHGHGHHHHH!!!", text_font, (0, 0, 0), 50, 3*HEIGHT/4-20)
                    elif tree_dialogue_num == 1:
                        draw_text("YOU CANNOT PASS!!!", text_font, (0, 0, 0), 50, 3*HEIGHT/4-20)
                    elif tree_dialogue_num == 2:
                        draw_text("Go my minions!!!", text_font, (0, 0, 0), 50, 3*HEIGHT/4-20)
                    else:
                        tree_dialogue_done = True
                
            
            if tree_hp <= 0: #draws chest for tree after tree is defeated
                chest_rect = pygame.Rect(WIDTH/2-20, 190, 60, 50)

                # conditional makes it only go into this once
                if (player_hitbox.colliderect(chest_rect or christmas_chest_opened == True) and tree_rewards_collected == False):
                    time_since_collected = time_run
                    christmas_chest_opened = True
                    tree_rewards_collected = True
                    candies += 10
                    health_potion_num += 1
                    
                if time_run - time_since_collected <= 2000:
                    screen.blit(chest_opened, (WIDTH/2-10, 200))
                    draw_text("Rewards moved to inventory", text_font_small, (0, 0, 0), 160, 150)

                if christmas_chest_opened == False:
                    screen.blit(chest_closed, (WIDTH/2-10, 200))

               
        # Maze room 
        if room == 4:
            walls = [(265, 285, 30, 85), (240, 285, 245, 30), (460, 115, 30, 65), 
                     (380, 215, 110, 32), (150, 150, 330, 30), (235, 150, 30, 100), 
                     (305, 215, 30, 70), (380, 150, 30, 90), (155, 215, 30, 150)]
            for wall in walls:
                pygame.draw.rect(screen, (100, 200, 255), wall)

            if collected_4 == False:
                screen.blit(dmg_buff_pic, (105, 310))
            
            if time_run - collected_4_time <= 1000:
                draw_text("Damage +15%", text_font, (0, 0, 0), 100, 290)
        else: 
            for i in range(len(walls)): 
                walls[i] = (-1000, -1000, 100, 100)

        if room == 6:
            if snowman_hp > 0: 
                screen.blit(snowman, (snowman_x - 30, snowman_y - 30))
                if snowman_dialogue_done == True: 
                    for snowball in snowballs: 
                        pygame.draw.circle(screen, (225, 225, 225), (snowball[0], snowball[1]), 15)
                    pygame.draw.rect(screen, (255, 255, 255), (snowman_x - 52, snowman_y - 31, 104, 12))
                    pygame.draw.rect(screen, (0, 255, 0), (snowman_x - 50, snowman_y - 30, snowman_hp/2000, 10))
                    
                    for damage in snowman_damage: 
                        if time_run - damage[0] < 500: 
                            draw_text(str(damage[3]), text_font_small, (0, 0, 0), snowman_x + damage[1], snowman_y + damage[2])
                    for damage in player_damage: 
                        if time_run - damage[0] < 500: 
                            draw_text(str(damage[1]), text_font_small, (255, 0, 0), player_x + damage[2], player_y + damage[3])
                
                else:
                    screen.blit(dialogue_box, (20, HEIGHT/2))
                    if snowman_dialogue_num == 0:
                        draw_text("NOOOOOOOOOOOOOO!!!", text_font, (0, 0, 0), 50, 3*HEIGHT/4-20)
                    elif snowman_dialogue_num == 1:
                        draw_text("YOU MUST NOT PASS!!!", text_font, (0, 0, 0), 50, 3*HEIGHT/4-20)
                    elif snowman_dialogue_num == 2:
                        draw_text("My snowballs will keep you away!!!", text_font, (0, 0, 0), 50, 3*HEIGHT/4-20)
                    else:
                        snowman_dialogue_done = True

            else: 
                chest_rect = pygame.Rect(WIDTH/2-20, 190, 60, 50)
                
                if (player_hitbox.colliderect(chest_rect) or snowman_chest_opened == True) and snowman_rewards_collected == False:  
                    time_since_collected = time_run 
                    snowman_chest_opened = True 
                    snowman_rewards_collected = True 
                    candies += 10

                if time_run - time_since_collected <= 2000:
                    screen.blit(chest_opened, (WIDTH/2-10, 200))
                    draw_text("Candy cane reward moved to inventory", text_font_small, (0, 0, 0), 150, 150)

                if snowman_chest_opened == False:
                    screen.blit(chest_closed, (WIDTH/2-10, 200))
            
            #draw sword dmg on screen
            if player_equipped == "sword":
                snowman_hp = player_draw_dmg("snowman", 0, 0, snowman_x, snowman_y, snowman_hp)
        
        if room == 8:
            if len(room_8_elves) == 5:
                for i in range(len(room_8_elves)):
                    elf = room_8_elves[i]
                    elf.draw_elf()
            
                    if player_equipped == "sword":
                        player_draw_dmg("elf", elf, room_8_elves_num[i], elf.elf_rect(0), elf.elf_rect(1), all_elves_hp)
                    
                    if player_equipped == "bow":
                        player_attacking_bow(room_8_elves[i], arrows_up, room_8_elves_num[i])
                        player_attacking_bow(room_8_elves[i], arrows_down, room_8_elves_num[i])
                        player_attacking_bow(room_8_elves[i], arrows_right, room_8_elves_num[i])
                        player_attacking_bow(room_8_elves[i], arrows_left, room_8_elves_num[i])
        if room == 9:
            if rudolph_hp > 0:
                pygame.draw.rect(screen, (255, 255, 255), (0,418,640,34))
                pygame.draw.rect(screen, (255, 0, 0), (0, 420, rudolph_hp/390.625, 30))
                if rudolph_dialogue_done == False:
                    screen.blit(dialogue_box, (20, HEIGHT/2))
                    if rudolph_dialogue_num == 0:
                        draw_text("YOU WILL NOT REACH SANTA", text_font, (0, 0, 0), 50, 3*HEIGHT/4-20)
                    elif rudolph_dialogue_num == 1:
                        draw_text("NOW BE THE DUST UNDER MY HOOVES", text_font, (0, 0, 0), 50, 3*HEIGHT/4-20)
                    else:
                        rudolph_dialogue_done = True
                if rudolph_north == True:
                    screen.blit(rudolph_up, (rudolph_x-30, rudolph_y-40))
                if rudolph_west == True:
                    screen.blit(rudolph_left, (rudolph_x-40, rudolph_y-40))
                if rudolph_south == True:
                    screen.blit(rudolph_down, (rudolph_x-22, rudolph_y-40))
                if rudolph_east == True:
                    screen.blit(rudolph_right, (rudolph_x-40, rudolph_y-40))
                
            if rudolph_hp <= 0:
                chest_rect = pygame.Rect(WIDTH/2-20, 190, 60, 50)
                if player_hitbox.colliderect(chest_rect) and rudolph_rewards_collected == False:
                    time_since_collected = time_run
                    rudolph_chest_opened = True
                    rudolph_rewards_collected = True
                    candies += 25
                    
                if time_run - time_since_collected <= 2000:
                    screen.blit(chest_opened, (WIDTH/2-10, 200))
                    draw_text("Candy cane reward moved to inventory", text_font_small, (0, 0, 0), 150, 150)
                if rudolph_chest_opened == False:
                    screen.blit(chest_closed, (WIDTH/2-10, 200))


        if room == 11: 
            screen.blit(sled_top, sled_xy[0])
            screen.blit(sled_middle, sled_xy[1])
            screen.blit(sled_bottom, sled_xy[2])
            if sled_dialogue_done == False: 
                screen.blit(dialogue_box, (20, HEIGHT/2))
            if sled_dialogue_num == 0:
                draw_text("HELPPPPP!!!", text_font, (0, 0, 0), 50, 3*HEIGHT/4-20)
            elif sled_dialogue_num == 1:
                draw_text("I'M A BROKEN SLED!!!", text_font, (0, 0, 0), 50, 3*HEIGHT/4-20)
            elif sled_dialogue_num == 2:
                draw_text("Please fix me!!!", text_font, (0, 0, 0), 50, 3*HEIGHT/4-20)
            else:
                sled_dialogue_done = True

            if sled_pass == [True, True, True]: 
                chest_rect = pygame.Rect(WIDTH/2-20, 190, 60, 50)
                
                if (player_hitbox.colliderect(chest_rect) or snowman_chest_opened == True) and snowman_rewards_collected == False:  
                    time_since_collected = time_run 
                    snowman_chest_opened = True 
                    snowman_rewards_collected = True 
                    candies += 10 
                if time_run - time_since_collected <= 2000:
                    screen.blit(chest_opened, (WIDTH/2-10, 200))
                    draw_text("Candy cane reward moved to inventory", text_font_small, (0, 0, 0), 150, 150)
                if snowman_chest_opened == False:
                    screen.blit(chest_closed, (WIDTH/2-10, 200))
            
                if collected_11 == False:
                    dmg_buff_rect = pygame.Rect(200, 200, 40, 40)
                    screen.blit(dmg_buff_pic, (200, 200))

                if player_hitbox.colliderect(dmg_buff_rect) == True:
                    collected_11 = True
                    collected_11_time = time_run
                    dmg_buff_rect = pygame.Rect(50, 50, 20, 20)
                    sword_damage *= 1.30
                    bow_damage *= 1.30
                
                if time_run - collected_11_time <= 2000 and collected_11 == True:
                    draw_text("Damage +30%", text_font, (0, 0, 0), 170, 150)
        
        if room == 13:
            screen.blit(grinch, (200, HEIGHT/2-40))
            pygame.draw.circle(screen, (255,0,0), (WIDTH/2 -9, HEIGHT/2 -30), 10)
            pygame.draw.circle(screen, (255,0,0), (WIDTH/2 + 9, HEIGHT/2 -30), 10)
            pygame.draw.rect(screen, (0,255,50), end_hitbox)
            pygame.draw.rect(screen, (255,0,0), (295,238.5,50,5))
            pygame.draw.rect(screen, (255,0,0), (317.5,215,5,50))
            if end_dialogue_done == False:
                screen.blit(dialogue_box, (20, HEIGHT/2))
            if end_dialogue_num == 0:
                draw_text("My son, I am so proud of you..", text_font, (0, 0, 0), 50, 3*HEIGHT/4-20)
            elif end_dialogue_num == 1:
                draw_text("You've conquered Santa's dungeon!!", text_font, (0, 0, 0), 50, 3*HEIGHT/4-20)
            elif end_dialogue_num == 2:
                draw_text("You destroyed the Tree, Frosty", text_font, (0, 0, 0), 50, 3*HEIGHT/4-30)
                draw_text("and Rudolph!", text_font, (0, 0, 0), 50, 3*HEIGHT/4)
            elif end_dialogue_num == 3:
                draw_text("All that's left is to destroy the", text_font, (0, 0, 0), 50, 3*HEIGHT/4-30)
                draw_text("presents and Ruin Christmas!", text_font, (0, 0, 0), 50, 3*HEIGHT/4)
            elif end_dialogue_num == 4:
                draw_text("Go out and conquer the world, my son!", text_font, (0, 0, 0), 50, 3*HEIGHT/4-20)
            else:
                end_dialogue_done = True     
        
        if end == True:
            pygame.draw.rect(screen, (0,0,0), (0,0,640,480))
            draw_text("Congratulations!", text_font, (255, 255, 255), WIDTH/2 -120, HEIGHT/2)
            draw_text("You Ruined Christmas!", text_font, (255, 255, 255), WIDTH/2 -160, HEIGHT/2 - 30)
        
        # room with santa
        if room == 12:
            if santa_hp > 0:
                pygame.draw.rect(screen, (255, 255, 255), (0,418,640,34))
                pygame.draw.rect(screen, (255, 0, 0), (0, 420, santa_hp/781.25, 30))
                all_creatures = satan.summon()
                satan.draw()
                satan.snowball()
                for i in range(len(all_creatures)):
                    if player_equipped == "sword":
                        player_draw_dmg("elf", all_creatures[i], len(all_elves_hp)-1-(5-i), all_creatures[i].elf_rect(0), all_creatures[i].elf_rect(1), all_elves_hp)
                        
                    if player_equipped == "bow":
                        player_attacking_bow(all_creatures[i], arrows_up, len(all_elves_hp)-1-(5-i))
                        player_attacking_bow(all_creatures[i], arrows_right, len(all_elves_hp)-1-(5-i))
                        player_attacking_bow(all_creatures[i], arrows_left, len(all_elves_hp)-1-(5-i))
                        player_attacking_bow(all_creatures[i], arrows_down, len(all_elves_hp)-1-(5-i))

                        player_attack_bow(satan, arrows_up)
                        player_attack_bow(satan, arrows_right)
                        player_attack_bow(satan, arrows_down)
                        player_attack_bow(satan, arrows_left)
            
            for snowball in snowballs: 
                pygame.draw.circle(screen, (225, 225, 225), (snowball[0], snowball[1]), 15)
            for damage in player_damage: 
                if time_run - damage[0] < 500: 
                    draw_text(str(damage[1]), text_font_small, (255, 0, 0), player_x + damage[2], player_y + damage[3])

        # room after beating the game
        if room == 13:
            pass


        #drawing the player's attacks (don't do damage but is visible there); function for dmg calc is only where rooms have enemies
        if event.type == pygame.MOUSEBUTTONDOWN and player_equipped == "sword":
            if w == True:
                pygame.draw.arc(screen, (0, 0, 0), (player_x-10, player_y, 60, 20), 0, 3.14, 3)
                pygame.draw.arc(screen, (0, 0, 0), (player_x-10, player_y-20, 60, 20), 0, 3.14, 3)
            elif a == True:
                pygame.draw.arc(screen, (0, 0, 0), (player_x, player_y-10, 20, 60), 1.57, 4.71, 3)
                pygame.draw.arc(screen, (0, 0, 0), (player_x-20, player_y-10, 20, 60), 1.57, 4.71, 3)
            elif s == True:
                pygame.draw.arc(screen, (0, 0, 0), (player_x-10, player_y+10, 60, 20), 3.14, 0, 3)
                pygame.draw.arc(screen, (0, 0, 0), (player_x-10, player_y+30, 60, 20), 3.14, 0, 3)
            elif d == True:
                pygame.draw.arc(screen, (0, 0, 0), (player_x+8, player_y-10, 20, 60), 4.71, 1.57, 3)
                pygame.draw.arc(screen, (0, 0, 0), (player_x+28, player_y-10, 20, 60), 4.71, 1.57, 3)
                

        # Inventory
        if player_equipped == "sword":
            pygame.draw.rect(screen, (255,204,203), (480,10,40,40))
        elif player_equipped == "bow":
            pygame.draw.rect(screen, (255,204,203), (530,10,40,40))
        elif player_equipped == "healthpot":
            pygame.draw.rect(screen, (255,204,203), (580,10,40,40))
        pygame.draw.rect(screen, (0,0,0), (480,10,40,40), width=3)
        pygame.draw.rect(screen, (0,0,0), (530,10,40,40), width=3)     
        pygame.draw.rect(screen, (0,0,0), (580,10,40,40), width=3)
        draw_text("1", text_font, (0, 0, 0), 495, 50)
        draw_text("2", text_font, (0, 0, 0), 545, 50)
        draw_text("3", text_font, (0, 0, 0), 595, 50)
        
        for i in range(len(inventory)):
            if inventory[i] == "SWORD":
                screen.blit(sword_1, (485,15))
            elif inventory[i] == "BOW":
                screen.blit(bow, (540, 13))
            elif health_potion_num > 0:
                screen.blit(health_potion, (587, 15))
                while health_potion_num >= 1 and health_potion_num <= 9 and time_run - checking >= 1:
                    screen.blit(potion_text, (605, 26))
                    checking = time_run
                while health_potion_num >= 10 and time_run - checking >= 1:
                    screen.blit(potion_text, (595, 26))
                    checking = time_run
        
        if player_hp <= 0:
            state = 2
        
        #save button
        pygame.draw.rect(screen, (0, 0, 0), (WIDTH-70, HEIGHT-70, 50, 50))
        draw_text("H", text_font, (255, 255, 255), WIDTH-55, HEIGHT-55)
    
        #saving files
        if saving == True:
            screen.fill((230, 200, 150))

            #drawing rectangles for saves depending on how many current saves there are
            if num_saves == 0:
                pygame.draw.rect(screen, (0, 0, 0), (50, 50, WIDTH-100, 100))
                draw_text("NEW SAVE FILE", text_font, (230, 200, 150), 200, 100)
            
            if num_saves == 1:
                pygame.draw.rect(screen, (0, 0, 0), (50, 50, WIDTH-100, 100))

                pygame.draw.rect(screen, (0, 0, 0), (50, 200, WIDTH-100, 100))
                draw_text("NEW SAVE FILE", text_font, (230, 200, 150), 200, 250)
            
            if num_saves == 2:
                pygame.draw.rect(screen, (0, 0, 0), (50, 50, WIDTH-100, 100))
                pygame.draw.rect(screen, (0, 0, 0), (50, 200, WIDTH-100, 100))

                pygame.draw.rect(screen, (0, 0, 0), (50, 350, WIDTH-100, 100))
                draw_text("MAX REACHED: OVERRIDE A PREVIOUS SAVE", text_font_small, (230, 200, 150), 95, 395)
                draw_text("OVERRIDE", text_font, (230, 200, 150), 240, 250)
                draw_text("OVERRIDE", text_font, (230, 200, 150), 240, 100)

                if override_rect_1.collidepoint(mouse_x, mouse_y) == True and left_M_pressed == True:
                    draw_text("Override Completed", text_font, (230, 200, 150), 70, 70)
                if override_rect_2.collidepoint(mouse_x, mouse_y) == True and left_M_pressed == True:
                    draw_text("Override Completed", text_font, (230, 200, 150), 70, 220)
        
            #checks if pressed new rect or not
            if new_save_rect.collidepoint(mouse_x, mouse_y) and left_M_pressed == True:
                if time_run - last_time_saved < 500 and num_saves < 2:
                    draw_text("SAVED!!!", text_font, (255, 255, 255), new_save_position[0]+5, new_save_position[1]+5)
        
    if state == -1 or saving == True:
        screen.blit(x_pic, (10, 10))
    
    if state == 2:
        screen.fill((0, 0, 0))
        draw_text("You have died!", text_font, (255, 255, 255), WIDTH/2 - 120, HEIGHT/2 - 20)

    # Pause menu 
    if state == 3: 
        screen.fill((255,255,255))
        pygame.draw.rect(screen, (0,0,0), (50,50,540,380))
        draw_text("GAME PAUSED", text_font, (255,255,255), 220, 60)
        pygame.draw.rect(screen, (255,255,255), settings_bar_rect, width=1)
        draw_text("SETTINGS", text_font, (255,255,255), 240,210)
        pygame.draw.rect(screen, (255,255,255), continue_playing_rect, width=1)
        draw_text("START SCREEN", text_font_small, (255,255,255), 235, 295)
        saving = False

    # Settings 
    if settings == True:
        pygame.draw.rect(screen, (0,0,0), (50,50,540,380))
        draw_text("SETTINGS", text_font, (255,255,255), 260, 60)

        #Volume Slider Appearance
        draw_slider(screen, slider_x, slider_y, slider_width, slider_height, knob_x)
        screen.blit(volume_text, (slider_x, slider_y - 50))

        draw_text("Choose your character:", text_font, (255, 255, 255), 150, 125)
        start_player_choice = pygame.Rect(225, 170, 50, 50)
        other_player_choice = pygame.Rect(375, 170, 50, 50)
        if player == start_player: 
            pygame.draw.rect(screen, (255, 225, 225), start_player_choice)
        elif player == other_player: 
            pygame.draw.rect(screen, (255, 225, 225), other_player_choice)
        pygame.draw.rect(screen, (255, 255, 255), start_player_choice, 2)
        pygame.draw.rect(screen, (255, 255, 255), other_player_choice, 2)
        screen.blit(start_player, (235, 175))
        screen.blit(other_player, (385, 183))
    
    # Store 
    if state == 4: 
        screen.blit(sign, (75, 30))
        draw_text("STORE", text_font, (255,255,255), 270,65)
        pygame.draw.rect(screen, (255,255,255), items_square_rect[0], width=1)
        screen.blit(sword_1, (239,142))
        pygame.draw.rect(screen, (255,255,255), items_square_rect[1], width=1)
        screen.blit(bow, (307,140))
        pygame.draw.rect(screen, (255,255,255), items_square_rect[2], width=1)
        screen.blit(health_potion, (362,143))
        
        if confirmation == True:
            draw_text(f"PURCHASE {items[item_number]}? Y/ESC", text_font, (255,255,255), 130,200)
        if upgrades == True:
            draw_text(f"UPGRADE {items[item_number]}? Y/ESC", text_font, (255,255,255), 130,200)
    
    if item_bought == 1:
        purchase_time = time_run
    elif item_bought == 2:
        fail_time = time_run
    
    item_bought = 0

    if time_run - purchase_time < 1000 and time_run > 1000:
        draw_text("PURCHASE SUCCESSFUL", text_font, (255, 255, 255), WIDTH/2 - 180, HEIGHT/2 - 50)
    
    if time_run - fail_time < 1000 and time_run > 1000:
        draw_text("NOT ENOUGH CANDY CANES", text_font, (0,0,0), WIDTH/2 - 200, HEIGHT/2 - 50)
            
    pygame.display.flip()
    clock.tick(30)
    #---------------------------


pygame.quit()
