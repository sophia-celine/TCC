import cv2,time,random
from matplotlib.pyplot import show
from djitellopy import Tello
from datetime import datetime
from os import mkdir
import pygame as pg

# https://djitellopy.readthedocs.io/en/latest/tello/

class KeyController():
    def __init__(self):
        self.tello = Tello()
        
    def startup(self):
        self.tello.connect()

    def key_control(self):
        self.tello.streamoff()  # Ends the current stream, in case it's still opened
        self.tello.streamon()  # Starts a new stream
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
                        self.tello.move_forward(20) # in cm
                    if event.key == pg.K_a:
                        self.tello.move_left(20)
                    if event.key == pg.K_s:
                        self.tello.move_back(20)
                    if event.key == pg.K_d:
                        self.tello.move_right(20)
                    if event.key == pg.K_q:
                        self.tello.rotate_counter_clockwise(20) # in degrees
                    if event.key == pg.K_e:
                        self.tello.rotate_clockwise(20)
                    if event.key == pg.K_SPACE:
                        self.tello.move_up(20)
                    if event.key == pg.K_LCTRL:
                        self.tello.move_down(20)
                    if event.key == pg.K_b:
                        print("Bateria: ", self.tello.get_battery(), "%")
                    if event.key == pg.K_m:
                        return 0
    
            cv2.imshow("image", image)
            if cv2.waitKey(5) & 0xFF == 27:
                break
    def main_interface(self):
        self.startup()
        pg.init()
        win = pg.display.set_mode((500,500))
        pg.display.set_caption("Test")
        self.tello.streamoff()  
        self.tello.streamon()
        telloMode = -1

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    telloMode = 1
                if event.key == pg.K_0:
                    telloMode = 0
                if event.key == pg.K_l:
                    self.tello.land()
                if event.key == pg.K_t:
                    self.tello.takeoff()
                if event.key == pg.K_b:
                    print("A bateria esta em ", self.tello.get_battery(), "%")
        
            if telloMode == 1:
                self.key_control()
                telloMode = -1
                print("Para controlar pelo teclado, digite 1")
                print("Para sair, digite 0")
            elif telloMode == 0:
                self.tello.land()
                telloMode = -1
                print("Obrigado por voar hoje")
            elif telloMode != -1 and telloMode != 1 and telloMode != 2:
                print("Valor invalido!")

if __name__ == "__main__":

    keycontroller = KeyController()
    keycontroller.main_interface()