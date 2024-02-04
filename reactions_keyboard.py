import tkinter as tk
import random
import time

class ReactionGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Reaction Time Game")
        self.master.geometry("600x400")

        self.canvas = tk.Canvas(self.master, width=600, height=350, bg="white")
        self.canvas.pack()

        self.keys_left = ['A', 'S', 'D', 'F']
        self.keys_right = ['J', 'K', 'L', ';']

        self.highlighted_keys_left = []
        self.highlighted_keys_right = []
        self.pressed_keys_left = []
        self.pressed_keys_right = []
        self.left_pressed_at = None
        self.right_pressed_at = None

        self.reaction_time_left = None
        self.reaction_time_right = None

        self.start_button = tk.Button(self.master, text="Start Game", command=self.display_countdown)
        self.start_button.pack()
        self.started = False

        self.master.bind("<space>", self.display_countdown)
        
    def reset(self):
        self.reaction_time_left = None
        self.reaction_time_right = None
        self.pressed_keys_left = []
        self.pressed_keys_right = []
        self.left_pressed_at = None
        self.right_pressed_at = None
        
        self.highlighted_keys_left = []
        self.highlighted_keys_right = []
        self.started = False

    def start_game(self, event=None):
        self.reset()
        self.started = True
        
        self.start_button.config(state="disabled")
        self.generate_highlighted_keys()
        self.draw_keyboard()
        self.start_time_left = time.time()
        self.start_time_right = time.time()

    def generate_highlighted_keys(self):
        self.highlighted_keys_left = random.sample(self.keys_left, 3)
        for index, key in enumerate(reversed(self.keys_left)):
            if key in self.highlighted_keys_left:
                self.highlighted_keys_right.append(self.keys_right[index])


    def draw_keyboard(self):
        self.canvas.delete("all")
        key_width = 50
        key_height = 50
        x_start = 75
        y_start = 150

        for i, key in enumerate(self.keys_left):
            x = x_start + i * key_width
            y = y_start
            if key in self.highlighted_keys_left:
                color = "#FBBB62" if self.reaction_time_left else "#FFD3B6"
            else:
                color = "white"
                
            self.canvas.create_rectangle(x, y, x + key_width, y + key_height, fill=color, outline="black")
            self.canvas.create_text(x + key_width / 2, y + key_height / 2, text=key, font=("Arial", 16))

        for i, key in enumerate(self.keys_right):
            x = x_start + (i + len(self.keys_left)) * key_width
            y = y_start
            
            if key in self.highlighted_keys_right:
                color = "#8BD3E6" if self.reaction_time_right else "#B3E6FF"
            else:
                color = "white"
            
            self.canvas.create_rectangle(x, y, x + key_width, y + key_height, fill=color, outline="black")
            self.canvas.create_text(x + key_width / 2, y + key_height / 2, text=key, font=("Arial", 16))
            
    def check_keys_pressed(self, event):
        if not self.started:
            return

        pressed_key = event.char.upper()

        if pressed_key in self.keys_left:
            if self.left_pressed_at:
                if time.time() - self.left_pressed_at > 0.2 and self.reaction_time_left is None:
                    self.pressed_keys_left = []
                    self.left_pressed_at = time.time()
            else:
                self.left_pressed_at = time.time()
                
            if self.reaction_time_left is not None:
                self.reaction_time_left = None
                self.draw_keyboard()
                
            else:
                self.pressed_keys_left.append(pressed_key)

            if set(self.pressed_keys_left) == set(self.highlighted_keys_left):
                self.reaction_time_left = time.time() - self.start_time_left
                self.draw_keyboard()
                if self.reaction_time_right is not None:
                    self.display_reaction_time()

        if pressed_key in self.keys_right:
            if self.right_pressed_at:
                if time.time() - self.right_pressed_at > 0.2 and self.reaction_time_right is None:
                    self.pressed_keys_right = []
                    self.right_pressed_at = time.time()
            else:
                self.right_pressed_at = time.time()
                
            if self.reaction_time_right is not None:
                self.reaction_time_right = None
                self.draw_keyboard()
                
            else:
                self.pressed_keys_right.append(pressed_key)

            if set(self.pressed_keys_right) == set(self.highlighted_keys_right):
                self.reaction_time_right = time.time() - self.start_time_right
                self.draw_keyboard()
                if self.reaction_time_left is not None:
                    self.display_reaction_time()

            

    def display_reaction_time(self):
        self.started = False
        
        self.canvas.delete("all")
        
        self.canvas.create_text(300, 100, text=f"Left Hand Reaction Time: {self.reaction_time_left:.2f} seconds", font=("Arial", 16))
        
        self.canvas.create_text(300, 200, text=f"Right Hand Reaction Time: {self.reaction_time_right:.2f} seconds", font=("Arial", 16))
        
        self.start_button.config(text="Press Space to Restart", state="normal")

    def display_countdown(self, event=None):
        for i in range(3, 0, -1):
            self.canvas.delete("all")
            self.canvas.create_text(300, 200, text=str(i), font=("Arial", 20))
            self.master.update()
            time.sleep(1)
        self.canvas.delete("all")
        self.start_game()

def main():
    root = tk.Tk()
    game = ReactionGame(root)
    root.bind("<Key>", game.check_keys_pressed)
    root.mainloop()

if __name__ == "__main__":
    main()
