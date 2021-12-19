import numpy as np
import random
import pygame
from PG_Car_Class import Car


"""
Variables needed:
current pos
Size of car
current speed
current acc
max speed
max acceleration (not necessarily symmetric)
reaction time
Chicken factor? (don't like people behind you, don't like being close, or want to get as close as possible)

functions
setters
getters
update v, a, etc.
checks
check of crash
check of distance in front
"""

# Setting basic variables
background_color = "black"

track_radius = 250 # Radius to the center of the track

# Initializes pygame
pygame.init()

# Setting Font For Printouts
font_color=(255,255,255)
font_obj=pygame.font.SysFont("arial.ttc",15)

# Screen size generated with pygame
screen_width = 750
screen_height = 750
(width, height) = (screen_width, screen_height)

# Infinite loop variable that'll be used later when actually running the simulation
running = True


# Function to draw track that'll be called every loop
def draw_track():
    pygame.draw.circle(screen, "gray", (screen_width/2, screen_height/2), 300)
    pygame.draw.circle(screen, "black", (screen_width/2, screen_height/2), 200)



number_of_cars = 5
my_cars = []

color_list = ["blue", "red", "green", "purple", "white"]

prevAngle = 0
# Generating all of the cars at random positions
for n in range(number_of_cars):
    possible_angle = (2*np.pi/number_of_cars)
    dtheta = random.random()*possible_angle + .3
    starting_angle = prevAngle + dtheta
    starting_x = np.cos(starting_angle)*track_radius + screen_width/2
    starting_y = np.sin(starting_angle)*track_radius + screen_height/2
    # Only the acceleration is random, other properties can also be set to random
    # for different variations with the exception of initial velocity
    car = Car(1, starting_x, starting_y, 0.5, random.randint(2, 5), starting_angle, 20, 40, -20, 10, 100, 200, color_list[n])
    my_cars.append(car)
    prevAngle = starting_angle

    

# Printing the stats
def draw_text(current_time):
    # Render the objects
    time_obj=font_obj.render(f"Current Time: {current_time//60} min {current_time%60} s",True,font_color)
    screen.blit(time_obj,(450,0))
    num_car_obj=font_obj.render(f"Number of cars: {number_of_cars}",True,font_color)
    screen.blit(num_car_obj,(450,20))

    sum_velos = 0
    for i in my_cars:
        sum_velos += i.get_velo()
    av_velos = round(sum_velos/number_of_cars,2)

    av_velo_obj=font_obj.render(f"Average Rot. Velo: {av_velos} deg/s",True,font_color)
    screen.blit(av_velo_obj,(450,40))


    




# Setting up the pygame window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Traffic Simulation")
screen.fill(background_color)

# Time counter
time = 0

# Drawing the initial position
draw_track()

draw_text(time)

for car in my_cars:
    car.draw_car(screen)

pygame.display.flip()



# Running the simulation
while running:
    
    for event in pygame.event.get():
        # Allows the code to be quit
        if event.type == pygame.QUIT:
            running = False
        
        # Keyboard presses advance the simulation
        elif event.type == pygame.KEYDOWN:
            time += 1

            screen.fill(background_color)
            draw_track()
            draw_text(time)

            # A double linked list is probably a more elegant way of checking collisions
            # and updating the movements of the cars
            for i in range(len(my_cars)):
                if (i == len(my_cars) - 1):
                    my_cars[i].move(my_cars[0], track_radius, screen_width, screen_height)
                    my_cars[i].draw_car(screen)
                else:
                    my_cars[i].move(my_cars[i + 1], track_radius, screen_width, screen_height)
                    my_cars[i].draw_car(screen)

            for i in range(len(my_cars)):
                if (i == len(my_cars) - 1):
                    if (my_cars[i].check_collision(my_cars[0])):
                        running = False
                elif (my_cars[i].check_collision(my_cars[i + 1])):
                    running = False

            

            
            
            pygame.display.flip()

