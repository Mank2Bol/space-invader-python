# -*- coding: utf-8 -*-
"""
Created on Sun Dec 19 13:09:42 2021

@author: Hp
"""
import threading as th
import tkinter as tk
from time import sleep,time
import keyboard.keyboard as kb
import random as rd

active = True

class Delta():
    def __init__(self,root):
        self.actif = True
        self.tick = 1/50
        self.tps_normal = 0
        self.root = root
        
        self.tps = time()
        self.der_tps = None
    
    def start(self):

        while self.actif:
            self.der_tps = self.tps
            self.tps = time()
            delta = self.tps - self.der_tps - self.tick
            sleep(self.tick)
            print(delta/self.tick)
            
            if kb.is_pressed('d'):
                self.root.can.move(ide,10,0)
            
            if kb.is_pressed('q'):
                self.root.can.move(ide,-10,0)
            
            if rd.random()<0.02:
                sleep(0.1)
                
    def stop(self):
        print('DESACTIVE')
        self.actif = False





root = tk.Tk()
root.can = tk.Canvas(root, width=1000, height=200, bg='black') # cannevas
root.can.pack()
ide = root.can.create_rectangle(30, 80, 30+100, 80+40, fill='red')

delta = Delta(root)
        
thread1 = th.Thread(target=delta.start, daemon=True)

thread1.start()

root.mainloop()


delta.stop()

root.destroy()












