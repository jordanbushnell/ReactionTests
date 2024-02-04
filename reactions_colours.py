import tkinter as tk
import random
import time

class ReactionTimeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Reaction Time Test")

        self.canvas = tk.Canvas(self.master, width=800, height=600, bg="#FFFFFF")  # White
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        self.canvas.bind("<Button-1>", self.on_click)

        self.reaction_label = tk.Label(self.master, text="", font=("Arial", 24))
        self.reaction_label.pack()

        self.start_test_button = tk.Button(self.master, text="Start Test", font=("Arial", 16), command=self.display_countdown)
        self.start_test_button.pack()
        
        self.master.bind("<space>", self.on_space_press)
        
        self.started = False
        
        # Initialize variables
        self.reaction_time = 0
        self.clicked = False
        self.green = "#98FB98"
    
    def display_countdown(self, event=None):
        for i in range(3, 0, -1):
            self.canvas.delete("all")
            self.canvas.create_text(400, 300, text=str(i), font=("Arial", 20))
            self.master.update()
            time.sleep(1)
        self.canvas.delete("all")
        
        self.start_test()
    
    def on_space_press(self, event):
        if not self.started:
            self.display_countdown()
        else:
            self.clicked = True

    def start_test(self):
        self.started = True
        
        self.reaction_label.config(text="")
        self.reaction_time = 0
        self.clicked = False
        start_time = time.time()
        pastel_colors = ["#FFB6C1", "#FFD700", "#FFA07A", "#9370DB", "#87CEEB",] * 3  # Pastel pink, Gold, Light salmon, Medium purple, Sky blue
        colors_sequence = pastel_colors + [self.green]  # Add green color to the end of the sequence
        current_color_index = 0
        self.canvas.config(bg=colors_sequence[current_color_index])
        last_color_change_time = start_time
        green_was_shown = False
        while not self.clicked:
            next_color_delay = random.uniform(0.5, 3.0)  # Random delay between 0.5 and 2.0 seconds
            self.canvas.update()
            current_time = time.time()
            if not green_was_shown and current_time - last_color_change_time >= next_color_delay:  # Change color after random delay
                current_color_index = random.randint(0, len(colors_sequence) - 1)
                self.canvas.config(bg=colors_sequence[current_color_index])
                last_color_change_time = current_time
                if colors_sequence[current_color_index] == self.green:  # Green color
                    start_time = time.time()  # Start time when green is shown
                    green_was_shown = True
            if self.clicked:
                if colors_sequence[current_color_index] == self.green:  # Green color
                    self.reaction_time = time.time() - start_time
                    self.show_reaction_time()
                else:
                    self.reaction_label.config(text="You clicked too soon!")
                break

    def show_reaction_time(self):
        self.reaction_label.config(text=f"Reaction Time: {self.reaction_time:.3f} seconds")
        self.started = False

    def on_click(self, event):
        if event.widget == self.canvas and event.x < self.canvas.winfo_width() and event.y < self.canvas.winfo_height():
            self.clicked = True

root = tk.Tk()
game = ReactionTimeGame(root)
root.mainloop()
