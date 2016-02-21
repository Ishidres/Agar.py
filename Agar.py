import pygame
import random
import pickle
import easygui

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode([1920, 1080])
screen.fill([255, 255, 255])        

background = pygame.image.load("Background.png")

x_pos = random.randint(1, 1920)
y_pos = random.randint(1, 1080)
crowd = 75

x_pos_ki = random.randint(1, 1920)
y_pos_ki = random.randint(1, 1080)
crowd_ki = 75

speed = 10
speed_calculation = 0
size_withdrawal = 0

sound = True

try:
    bigfood_sound = pygame.mixer.Sound("eat_blob.ogg")   # Sound for the big green cells
    zelle_sound = pygame.mixer.Sound("eat_dot.ogg")      # Sound if you eat a small cell
    gift_sound = pygame.mixer.Sound("blob_explode.ogg")  # Sound if you're eating a virus
    lost_sound = pygame.mixer.Sound("blob_lost.ogg")     # If you were eaten by AI
    eat_sound = pygame.mixer.Sound("eat_smbh.ogg")       # If you're eating AI
except:
    print "Couldn't load sound!"
    sound = False

speed_ki = 10

moveX = 0
moveY = 0

moveX_ki = 0
moveY_ki = 0

cameraX = 0
cameraY = 0

next_aim_x = 960
next_aim_y = 540

next_aim_x_ki = 960
next_aim_y_ki = 540

spawned_cells_x = []
spawned_cells_y = []
spawned_cells = 0   

spawned_virus_x = []
spawned_virus_y = []
spawned_virus = 0

spawned_bigfood_x = []
spawned_bigfood_y = []
spawned_bigfood = 0
    
cells_must_appear = 200
virus_must_appear = 3
bigfood_must_appear = 3

time = 0
second_timer = 0

poisoning = False
poisoning_time = 240

poisoning_ki = False
poisoning_time_ki = 240

smaller_than = 10000
smaller_than_number = 0

chat = ""
normal_speed = True
ki = True
poisoning_must_stop = False
poisoning_must_stop_ki = False
special_items = True
vs_ki = False
attack = True
    
while True:
    if x_pos > 1920: x_pos = 1920
    if x_pos < 0: x_pos = 0
    if y_pos > 1080: y_pos = 1080
    if y_pos < 0: y_pos = 0
    
    if cells_must_appear > 2000: cells_must_appear = 2000
    
    size_withdrawal = crowd / 15
    size_withdrawal_ki = crowd_ki / 15
    
    time = time + 1
    second_timer = second_timer + 1
    
    if poisoning_must_stop:
        poisoning_must_stop = False
        poisoning = False
    
    if poisoning == True:
        poisoning_time = poisoning_time - 1
    
    if poisoning_time > 0 and poisoning:
        crowd = crowd - 1
    
    if poisoning_time == 0:
        poisoning = False
        poisoning_time = 300

    # KI
    
    if poisoning_must_stop_ki:
        poisoning_must_stop_ki = False
        poisoning_ki = False
    
    if poisoning == True:
        poisoning_time_ki = poisoning_time_ki - 1
    
    if poisoning_time_ki > 0 and poisoning_ki:
        crowd_ki = crowd_ki - 1
    
    if poisoning_time_ki == 0:
        poisoning_ki = False
        poisoning_time_ki = 300
    
    if time >= 120:
        time = 0      
        crowd = crowd - size_withdrawal
        crowd_ki = crowd_ki - size_withdrawal_ki
    
    if second_timer >= 300:
        if random.randint(1, 3) == 3:
            attack = True
        else:
            attack = False
    
    if crowd < crowd_ki / 4:
        attack = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:           
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                moveY = -1
            if event.key == pygame.K_DOWN: 
                moveY = 1
            if event.key == pygame.K_LEFT:
                moveX = -1
            if event.key == pygame.K_RIGHT:
                moveX = 1
                
            if event.key == pygame.K_F1:                 
                new_crowd = easygui.enterbox("Size:", default = crowd)
                crowd = int(new_crowd)
                    
            if event.key == pygame.K_F2:   
                new_speed = easygui.enterbox("Speed:", default = speed)
                speed = int(new_speed)                                       
                normal_speed = False
            
            if event.key == pygame.K_F3:   
                new_cells_must_appear = easygui.enterbox("How much Cells have to appear?", default = cells_must_appear)
                cells_must_appear = int(new_cells_must_appear)                                                  
            
            if event.key == pygame.K_F4:                 
                normal_speed = True
                poisoning = False
                poisoning_time = 0
                cells_must_appear = 200
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                moveY = 0
            if event.key == pygame.K_DOWN: 
                moveY = 0
            if event.key == pygame.K_LEFT:
                moveX = 0
            if event.key == pygame.K_RIGHT:
                moveX = 0
     
    if normal_speed: 
        speed = crowd / 100
        speed = 10-speed
    
        speed_ki = crowd_ki / 100
        speed_ki = 10-speed_ki
    
    if crowd < 60:
        crowd = 60
        
    if crowd_ki < 60:
        crowd_ki = 60
    print crowd
    if speed < 1:
        speed = 1
                        
    if spawned_cells < cells_must_appear:
        spawned_cells_x.append(random.randint(0, 1920)) 
        spawned_cells_y.append(random.randint(0, 1080))
        spawned_cells = spawned_cells + 1
        
    if special_items:
        if spawned_virus < virus_must_appear:
            spawned_virus_x.append(random.randint(0, 1920)) 
            spawned_virus_y.append(random.randint(0, 1080))
            spawned_virus = spawned_virus + 1 
            
    if special_items:        
        if spawned_bigfood < bigfood_must_appear:
            spawned_bigfood_x.append(random.randint(0, 1920)) 
            spawned_bigfood_y.append(random.randint(0, 1080))
            spawned_bigfood = spawned_bigfood + 1 
    

    if spawned_cells == cells_must_appear:
        for i in range(cells_must_appear):
            
            differenz_x_distance = x_pos - spawned_cells_x[i-1]
            differenz_y_distance = y_pos - spawned_cells_y[i-1]
            
            distance = differenz_x_distance**2 + differenz_y_distance**2
            distance = distance**(1/2.0) # Wurzel
            
            if distance < crowd/2:
                del spawned_cells_x[i-1]
                del spawned_cells_y[i-1]
                
                spawned_cells = spawned_cells - 1
                crowd = crowd + 1
                if sound: zelle_sound.play()

            
            # KI
            
            differenz_x_distance = x_pos_ki - spawned_cells_x[i-1]
            differenz_y_distance = y_pos_ki - spawned_cells_y[i-1]
            
            distance = differenz_x_distance**2 + differenz_y_distance**2
            distance = distance**(1/2.0) # Wurzel
            
            if distance < crowd_ki/2:
                del spawned_cells_x[i-1]
                del spawned_cells_y[i-1]
                
                spawned_cells = spawned_cells - 1
                crowd = crowd + 1
                if sound: zelle_sound.play()                   
            
            for i in range (2):
                if spawned_cells < cells_must_appear:
                    spawned_cells_x.append(random.randint(0, 1920)) 
                    spawned_cells_y.append(random.randint(0, 1080))
                    spawned_cells = spawned_cells + 1
            
    if special_items:
        if spawned_virus == virus_must_appear:
            for i in range(0, virus_must_appear):
                differenz_x_distance = x_pos - spawned_virus_x[i-1]
                differenz_y_distance = y_pos - spawned_virus_y[i-1]
                
                distance = differenz_x_distance**2 + differenz_y_distance**2
                distance = distance**(1/2.0) # Wurzel
                
                if distance < crowd/2:
                    del spawned_virus_x[i-1]
                    del spawned_virus_y[i-1]
                    
                    spawned_virus = spawned_virus - 1
                    poisoning = True
                    if sound: gift_sound.play()

                
                # KI
                
                differenz_x_distance = x_pos_ki - spawned_virus_x[i-1]
                differenz_y_distance = y_pos_ki - spawned_virus_y[i-1]
                
                distance = differenz_x_distance**2 + differenz_y_distance**2
                distance = distance**(1/2.0) # Wurzel
                
                if distance < crowd_ki/2:
                    del spawned_virus_x[i-1]
                    del spawned_virus_y[i-1]
                    
                    spawned_virus = spawned_virus - 1
                    poisoning_ki = True
                    if sound: gift_sound.play()     
                
                for i in range (2):
                     if spawned_virus < virus_must_appear:
                        spawned_virus_x.append(random.randint(0, 1920)) 
                        spawned_virus_y.append(random.randint(0, 1080))
                        spawned_virus = spawned_virus + 1 
                
    if special_items:                
        if spawned_bigfood == bigfood_must_appear:
            for i in range(0, bigfood_must_appear):
                differenz_x_distance = x_pos - spawned_bigfood_x[i-1]
                differenz_y_distance = y_pos - spawned_bigfood_y[i-1]
                
                distance = differenz_x_distance**2 + differenz_y_distance**2
                distance = distance**(1/2.0) # Wurzel
                
                if distance < crowd/2:
                    del spawned_bigfood_x[i-1]
                    del spawned_bigfood_y[i-1]
                    
                    spawned_bigfood = spawned_bigfood - 1
                    
                    if crowd < 150:
                        crowd = crowd + 80
                        if sound: bigfood_sound.play()
                    else:
                        poisoning = True
                        crowd = crowd + 30
                        if sound: gift_sound.play()
                
                # KI
                
                differenz_x_distance = x_pos_ki - spawned_bigfood_x[i-1]
                differenz_y_distance = y_pos_ki - spawned_bigfood_y[i-1]
                
                distance = differenz_x_distance**2 + differenz_y_distance**2
                distance = distance**(1/2.0) # Wurzel
                
                if distance < crowd_ki/2:
                    del spawned_bigfood_x[i-1]
                    del spawned_bigfood_y[i-1]
                    
                    spawned_bigfood = spawned_bigfood - 1
                    
                    if crowd_ki < 150:
                        crowd_ki = crowd_ki + 80
                        if sound: bigfood_sound.play()
                    else:
                        poisoning_ki = True
                        crowd_ki = crowd_ki + 30
                        if sound: gift_sound.play()         
                
                for i in range (2):
                    if spawned_bigfood < bigfood_must_appear:
                        spawned_bigfood_x.append(random.randint(0, 1920)) 
                        spawned_bigfood_y.append(random.randint(0, 1080))
                        spawned_bigfood = spawned_bigfood + 1 
    
    if ki:   
        differenz_x_distance = x_pos_ki - x_pos
        differenz_y_distance = y_pos_ki - y_pos
        
        distance = differenz_x_distance**2 + differenz_y_distance**2
        distance = distance**(1/2.0) # Wurzel 
        
        if distance < crowd_ki/2:
            if crowd_ki > crowd + crowd / 10:
                lost_sound.play()
                
                crowd_ki += crowd/2
                crowd = 0
                
                x_pos = random.randint(1, 1920)
                y_pos = random.randint(1, 1080)
        
        if distance < crowd/2:
            if crowd > crowd_ki + crowd_ki / 10:
                eat_sound.play()
                
                crowd += crowd_ki/2
                crowd_ki = 0
                
                x_pos_ki = random.randint(1, 1920)
                y_pos_ki = random.randint(1, 1080)
        
        for i in range(spawned_cells):
            differenz_x_distance = x_pos_ki - spawned_cells_x[i-1]
            differenz_y_distance = y_pos_ki - spawned_cells_y[i-1]
            
            distance = differenz_x_distance**2 + differenz_y_distance**2
            distance = distance**(1/2.0)
            
            if distance < smaller_than:
                smaller_than = distance    
                smaller_than_number = i
                
            next_aim_x_ki = spawned_cells_x[smaller_than_number]
            next_aim_y_ki = spawned_cells_y[smaller_than_number]
        
        if special_items:            
            if crowd_ki < 150:
                for i in range(spawned_bigfood):
                    differenz_x_distance = x_pos_ki - spawned_bigfood_x[i-1]
                    differenz_y_distance = y_pos_ki - spawned_bigfood_y[i-1]
                    
                    distance = differenz_x_distance**2 + differenz_y_distance**2
                    distance = distance**(1/2.0)
                        
                    next_aim_x_ki = spawned_bigfood_x[i-1]
                    next_aim_y_ki = spawned_bigfood_y[i-1]
        
        if crowd_ki > crowd + crowd / 10:
            if attack == True:
                next_aim_x_ki = x_pos
                next_aim_y_ki = y_pos
        
    if ki:
        if x_pos_ki < next_aim_x_ki:
            moveX_ki = 1
        if x_pos_ki > next_aim_x_ki:
            moveX_ki = -1
        if y_pos_ki < next_aim_y_ki:
            moveY_ki = 1
        if y_pos_ki > next_aim_y_ki:
            moveY_ki = -1    
    
    x_pos += moveX * speed
    y_pos += moveY * speed
    
    x_pos_ki += moveX_ki * speed_ki
    y_pos_ki += moveY_ki * speed_ki
    
    screen.fill([255, 255, 255])    
    screen.blit(background, (0 -cameraX, 0 -cameraY))
    
    for i in range(spawned_cells):
        new_object = pygame.draw.circle(screen, [100, 150, 200], [spawned_cells_x[i-1], spawned_cells_y[i-1]], 10, 0)
        
    for i in range(spawned_bigfood):
        new_object = pygame.draw.circle(screen, [0, 255, 150], [spawned_bigfood_x[i-1], spawned_bigfood_y[i-1]], 75, 0)
        
    for i in range(spawned_virus):
        new_object = pygame.draw.circle(screen, [0, 192, 0], [spawned_virus_x[i-1], spawned_virus_y[i-1]], 30, 0)     
    
    if crowd_ki > crowd:
        pygame.draw.circle(screen, [192, 0, 0], [x_pos -cameraX, y_pos -cameraY], crowd/2, 0)               # You
        pygame.draw.circle(screen, [0, 192, 192], [x_pos_ki - cameraX, y_pos_ki - cameraY], crowd_ki/2, 0)    # Computer
    
    if crowd > crowd_ki:
        pygame.draw.circle(screen, [0, 192, 192], [x_pos_ki - cameraX, y_pos_ki - cameraY], crowd_ki/2, 0)    # Computer
        pygame.draw.circle(screen, [192, 0, 0], [x_pos -cameraX, y_pos -cameraY], crowd/2, 0)               # You
    
    if crowd == crowd_ki:
        pygame.draw.circle(screen, [0, 192, 192], [x_pos_ki - cameraX, y_pos_ki - cameraY], crowd_ki/2, 0)    # Computer
        pygame.draw.circle(screen, [192, 0, 0], [x_pos -cameraX, y_pos -cameraY], crowd/2, 0)               # You
        
    if poisoning:
        pygame.draw.circle(screen, [0, 102, 0], [x_pos -cameraX, y_pos -cameraY], crowd/2, 0)
    if poisoning_ki:
        pygame.draw.circle(screen, [0, 102, 102], [x_pos_ki -cameraX, y_pos_ki -cameraY], crowd_ki/2, 0)
        
    chat_text = chat
    chat_font = pygame.font.Font(None, 40)
    chat_surf = chat_font.render(chat_text, 1, (0, 0, 0))
    screen.blit(chat_surf, [10, 10])
    
    generated_cells_text = "Generating Cells: " + str (spawned_cells) + "/" + str (cells_must_appear)
    gc_text_font = pygame.font.Font(None, 40)
    gc_text_surf = chat_font.render(generated_cells_text, 1, (0, 0, 0))
    
    if spawned_cells < cells_must_appear:
        screen.blit(gc_text_surf, [1550, 10])
    
    pygame.display.flip()