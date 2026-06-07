import tkinter as tk
from tkinter import messagebox
import random

class SnakeMazeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Змейка в лабиринте")
        self.root.geometry("600x500")
        
        self.score = 0
        self.game_active = False
        self.cell_size = 20
        self.maze_w, self.maze_h = 25, 18
        self.base_speed = 250
        self.min_speed = 150
        self.apples = 0
        self.snake_color = "#2E8B57"
        
        self.create_maze()
        self.create_ui()
        self.reset_game()
        
        # ФИКС 1: Привязываем к root и фокусируем его
        self.root.bind_all('<KeyPress>', self.key_press)  # bind_all ловит все клавиши
        self.root.focus_set()  # Устанавливаем фокус на окно
        
        # ФИКС 2: Возвращаем фокус на окно при клике по кнопкам
        for btn in self.buttons:
            btn.bind('<Button-1>', lambda e: self.root.focus_set())
    
    def create_maze(self):
        self.maze = [['0']*self.maze_w for _ in range(self.maze_h)]
        for i in range(self.maze_h):
            self.maze[i][0] = self.maze[i][self.maze_w-1] = '1'
        for j in range(self.maze_w):
            self.maze[0][j] = self.maze[self.maze_h-1][j] = '1'
        obstacles = [
            [(2,2),(2,3),(2,4),(3,2),(4,2)],
            [(2,self.maze_w-5),(2,self.maze_w-4),(2,self.maze_w-3),(3,self.maze_w-3),(4,self.maze_w-3)],
            [(self.maze_h-5,2),(self.maze_h-5,3),(self.maze_h-5,4),(self.maze_h-6,2),(self.maze_h-7,2)],
            [(self.maze_h-5,self.maze_w-5),(self.maze_h-5,self.maze_w-4),(self.maze_h-5,self.maze_w-3),
             (self.maze_h-6,self.maze_w-3),(self.maze_h-7,self.maze_w-3)],
            [(self.maze_h//2-2,5),(self.maze_h//2-1,5),(self.maze_h//2,5),(self.maze_h//2-1,6),
             (self.maze_h//2-2,7),(self.maze_h//2-1,7),(self.maze_h//2,7)],
            [(self.maze_h//2-2,self.maze_w-8),(self.maze_h//2-2,self.maze_w-7),(self.maze_h//2-2,self.maze_w-6),
             (self.maze_h//2-1,self.maze_w-7),(self.maze_h//2,self.maze_w-7)],
            [(5,self.maze_w//2-4),(5,self.maze_w//2-3),(5,self.maze_w//2-2),(6,self.maze_w//2-4),(7,self.maze_w//2-4)],
            [(5,self.maze_w//2+1),(5,self.maze_w//2+2),(5,self.maze_w//2+3),(6,self.maze_w//2+3),(7,self.maze_w//2+3)],
            [(10,6),(10,7),(11,6)],
            [(10,self.maze_w-9),(10,self.maze_w-8),(11,self.maze_w-8)],
            [(12,8),(13,9),(14,10),(13,11),(12,12)],
            [(self.maze_h//2+1,self.maze_w//2-3),(self.maze_h//2+1,self.maze_w//2-2),(self.maze_h//2+2,self.maze_w//2-3),
             (self.maze_h//2+2,self.maze_w//2-2),(self.maze_h//2+3,self.maze_w//2-4),(self.maze_h//2+3,self.maze_w//2-3),
             (self.maze_h//2+3,self.maze_w//2-2),(self.maze_h//2+3,self.maze_w//2-1),(self.maze_h//2+4,self.maze_w//2-3),
             (self.maze_h//2+4,self.maze_w//2-2)]
        ]
        for obs in obstacles:
            for y,x in obs:
                self.maze[y][x] = '1'