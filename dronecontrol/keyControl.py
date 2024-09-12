import cv2
import numpy as np
import time
import random
from matplotlib.pyplot import show
from djitellopy import Tello
from datetime import datetime
from os import mkdir
import pygame as pg

# https://djitellopy.readthedocs.io/en/latest/tello/

class KeyController():
    def __init__(self):
        self.tello = Tello()
        self.mode = -1
        
    def startup(self):
        self.tello.connect()

    def key_control(self):
        self.tello.streamoff()  # Ends the current stream, in case it's still opened
        self.tello.streamon()  # Starts a new stream
        command = 'no command'
        
        while True:

            frame_read = self.tello.get_frame_read()  # Stores the current streamed frame
            image = frame_read.frame

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_w:
                        command = 'frw'
                        self.tello.move_forward(20) # in cm
                    if event.key == pg.K_a:
                        command = 'left'
                        self.tello.move_left(20)
                    if event.key == pg.K_s:
                        command = 'back'
                        self.tello.move_back(20)
                    if event.key == pg.K_d:
                        command = 'right'
                        self.tello.move_right(20)
                    if event.key == pg.K_q:
                        command = 'rotate left'
                        self.tello.rotate_counter_clockwise(20) # in degrees
                    if event.key == pg.K_e:
                        command = 'rotate right'
                        self.tello.rotate_clockwise(20)
                    if event.key == pg.K_SPACE:
                        command = 'up'
                        self.tello.move_up(20)
                    if event.key == pg.K_LCTRL:
                        command = 'down'
                        self.tello.move_down(20)
                    if event.key == pg.K_b:
                        print("Bateria: ", self.tello.get_battery(), "%")
                    if event.key == pg.K_l:
                        command = 'land'
                        print("landing...")
                        self.tello.land()
                    if event.key == pg.K_m:
                        self.tello.land()
                        return 0
            cv2.putText(image, command, (450, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.imshow("image", image)
            if cv2.waitKey(5) & 0xFF == 27:
                break
    def main_interface(self):
        self.startup()
        pg.init()
        #self.mode = 1
        telloMode = -1
        win = pg.display.set_mode((500,500))
        pg.display.set_caption("Control window")
        print("Para controlar pelo teclado, digite 1")
        print("Para sair, digite 0")

        self.tello.streamoff()  # Ends the current stream, in case it's still opened
        self.tello.streamon()  # Starts a new stream
        while telloMode != 0:
            frame_read = self.tello.get_frame_read()  # Stores the current streamed frame
            image = frame_read.frame
            """
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  
            """
            
            
            cv2.imshow("image", image)
            if cv2.waitKey(5) & 0xFF == 27:
                break

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        print("telloMode 1")
                        telloMode = 1
                        self.mode = 1
                    if event.key == pg.K_0:
                        telloMode = 0
                        self.mode = 0
                        print("telloMode 0")
                    if event.key == pg.K_l:
                        print("landing...")
                        self.tello.land()
                    if event.key == pg.K_t:
                        print("takeoff")
                        self.tello.takeoff()
                        telloMode = 1
                    if event.key == pg.K_b:
                        print("A bateria esta em ", self.tello.get_battery(), "%")
            
                if telloMode == 1:
                    print("key control selected")
                    self.key_control()
                    telloMode = -1
                    
                elif telloMode == 0:
                    self.tello.land()
                    telloMode = -1
                    print("Obrigado por voar hoje")
                elif telloMode != -1 and telloMode != 1 and telloMode != 2:
                    print("Valor invalido!")

# img_array = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)  # Example array
# cv2.imshow('Image', img_array)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
if __name__ == "__main__":
    
    while True:
        keycontroller = KeyController()
        keycontroller.main_interface()
