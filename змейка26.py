import tkinter as tk
from tkinter import messagebox
import random
import json
import os

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
        
        # Загрузка сохранённого рекорда
        self.load_best_score()
        
        self.create_maze()
        self.create_ui()
        self.reset_game()
        
        self.root.bind_all('<KeyPress>', self.on_key_press)
       
        self.start_btn.bind('<Button-1>', self.on_button_click)
        self.restart_btn.bind('<Button-1>', self.on_button_click)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.root.focus_set()
    
    def load_best_score(self):
        """Загрузка лучшего результата из файла snake_score.json"""
        # Получаем путь к папке, где находится скрипт
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.save_file = os.path.join(script_dir, "snake_score.json")
        
        self.best_score = 0
        
        print(f"Загрузка рекорда из: {self.save_file}")  # Отладка
        
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.best_score = data.get('best_score', 0)
                print(f"Рекорд загружен: {self.best_score}")
            except Exception as e:
                print(f"Ошибка загрузки: {e}")
                self.best_score = 0
        else:
            print("Файл с рекордом не найден, будет создан новый")
    
    def save_best_score(self):
        """Сохранение лучшего результата в файл snake_score.json"""
        data = {
            'best_score': self.best_score
        }
        try:
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Рекорд {self.best_score} сохранён в: {self.save_file}")
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
    
    def update_best_score(self):
        """Обновление лучшего результата"""
        if self.score > self.best_score:
            self.best_score = self.score
            self.save_best_score()
            return True
        return False
    
    def on_key_press(self, event):
        """Обработчик нажатия клавиш"""
        if not self.game_active:
            return
        
        keycode = event.keycode
        
        if keycode in [87, 119] and self.direction != 'Down':
            self.direction = 'Up'
        elif keycode in [83, 115] and self.direction != 'Up':
            self.direction = 'Down'
        elif keycode in [65, 97] and self.direction != 'Right':
            self.direction = 'Left'
        elif keycode in [68, 100] and self.direction != 'Left':
            self.direction = 'Right'
    
    def on_button_click(self, event):
        self.root.focus_set()
        return True
    
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
    
    def create_ui(self):
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        self.start_btn = tk.Button(btn_frame, text="Старт", command=self.start_game, width=10)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.restart_btn = tk.Button(btn_frame, text="Заново", command=self.restart_game, width=10)
        self.restart_btn.pack(side=tk.LEFT, padx=5)
        
        self.canvas = tk.Canvas(self.root, width=self.maze_w*self.cell_size, height=self.maze_h*self.cell_size,
                                bg="lightgray", highlightthickness=2)
        self.canvas.pack(pady=10)
        
        self.canvas.bind('<Button-1>', lambda e: self.root.focus_set())
    
    def reset_game(self):
        self.snake = [self.random_free_cell()]
        self.direction = "Right"
        self.food = self.random_free_cell(avoid_snake=True)
        self.score = 0
        self.apples = 0
        self.draw_game()
    
    def restart_game(self):
        self.game_active = False
        self.reset_game()
        self.root.focus_set()
    
    def random_free_cell(self, avoid_snake=False):
        while True:
            x = random.randint(2, self.maze_w-3)
            y = random.randint(2, self.maze_h-3)
            if self.maze[y][x] == '0' and (not avoid_snake or (x,y) not in self.snake):
                return (x,y)
    
    def start_game(self):
        if not self.game_active:
            self.game_active = True
            self.root.focus_set()
            self.game_loop()
    
    def game_loop(self):
        if not self.game_active:
            return
        
        head = self.snake[0]
        if self.direction == 'Left': new = (head[0]-1, head[1])
        elif self.direction == 'Right': new = (head[0]+1, head[1])
        elif self.direction == 'Up': new = (head[0], head[1]-1)
        else: new = (head[0], head[1]+1)
        
        x, y = new
        if not (0 <= x < self.maze_w and 0 <= y < self.maze_h) or self.maze[y][x] == '1' or new in self.snake[:-1]:
            self.game_active = False
            self.update_best_score()
            messagebox.showinfo("Конец игры", f"Вы проиграли!\nСчёт: {self.score}\nРекорд: {self.best_score}")
            return
        
        self.snake.insert(0, new)
        if new == self.food:
            self.score += 10
            self.apples += 1
            self.food = self.random_free_cell(avoid_snake=True)
        else:
            self.snake.pop()
        
        self.draw_game()
        speed = max(self.min_speed, self.base_speed - (self.apples // 3) * 10)
        self.root.after(speed, self.game_loop)
    
    def draw_game(self):
        self.canvas.delete("all")
        cs = self.cell_size
        for y in range(self.maze_h):
            for x in range(self.maze_w):
                x1, y1 = x*cs, y*cs
                x2, y2 = x1+cs, y1+cs
                if self.maze[y][x] == '1':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#3E2723", outline="#4E342E")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#F0F0F0", outline="#D0D0D0")
        
        for (x,y) in self.snake:
            self.canvas.create_rectangle(x*cs+2, y*cs+2, (x+1)*cs-2, (y+1)*cs-2, fill=self.snake_color, outline="#1F5E3A")
        
        fx, fy = self.food
        self.canvas.create_oval(fx*cs+4, fy*cs+4, (fx+1)*cs-4, (fy+1)*cs-4, fill="#F44336", outline="#D32F2F")
    
    def on_closing(self):
        self.save_best_score()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeMazeGame(root)
    root.mainloop()