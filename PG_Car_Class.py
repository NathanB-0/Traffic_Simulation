import pygame
import numpy as np
import math
# Can make this class its own file, improves readability of the code
class Car:
    def __init__(self, number, x0, y0, v0, a0, angle0, car_size, max_speed, max_neg_acc, max_pos_acc, too_close, too_far, car_color):
        self.number = number
        self.x = x0
        self.y = y0
        self.v = v0
        self.a = a0
        self.size = car_size
        self.max_speed = max_speed
        self.max_neg_acc = max_neg_acc
        self.max_pos_acc = max_pos_acc
        self.color = car_color
        self.angle = angle0
        self.close = too_close
        self.far = too_far


    def get_xpos(self):
        return self.x

    def get_ypos(self):
        return self.y

    def get_velo(self):
        return self.v
    
    def get_acc(self):
        return self.a

    def get_size(self):
        return self.size

    def get_angle(self):
        return self.angle


    def print_summary(self):
        # Originally used when I had a 1D simulation, not corrected for a circular track
        print(f"Car #{self.number}, size {self.size}, is at x = {self.x} m and y = {self.y} m with a speed of {self.v} m/s and an acceleration of {self.a} m/s^2.")

    def draw_car(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.size)

    # Checks if two circle cars are intersecting by 
    # finding the distance between the center of both the circles and 
    # comparing it to both radii added together. If the distance is less than 
    # the added radii, then the two cars are intersecting.
    def check_collision(self, Car):
        return math.sqrt((self.x - Car.get_xpos())**2 + (self.y - Car.get_ypos())**2) < self.size + Car.get_size()

    # Makes the car speed up, slow down, or maintain the same velocity depending on
    # the cars distance from the car in front of it
    def move(self, Car, track_radius, screen_width, screen_height):
        if (math.sqrt((self.x - Car.get_xpos())**2 + (self.y - Car.get_ypos())**2)) < self.close and self.v > .5:
            self.v -= self.a*np.pi/180
            self.angle += self.v*np.pi/180
        elif (math.sqrt((self.x - Car.get_xpos())**2 + (self.y - Car.get_ypos())**2)) > self.far:
            if self.v >= self.max_speed:
                self.v = self.max_speed
                self.angle += self.v*np.pi/180
            else:
                self.v += self.a*np.pi/180
                self.angle += self.v*np.pi/180
        else:
            self.angle += self.v*np.pi/180
        


        # Will convert this to % for update 2 
        if self.angle >= 2*np.pi:
            self.angle -= 2*np.pi

        self.x = np.cos(self.angle)*track_radius + screen_width/2
        self.y = np.sin(self.angle)*track_radius + screen_height/2

