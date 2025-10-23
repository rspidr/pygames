import tkinter as tk
import random
from collections import deque
import math

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("snake")
        self.root.resizable(False, False)
        
        # Game constants
        self.GRID_SIZE = 20
        self.CELL_SIZE = 25
        self.WIDTH = self.GRID_SIZE * self.CELL_SIZE
        self.HEIGHT = self.GRID_SIZE * self.CELL_SIZE
        self.GAME_SPEED = 100  # milliseconds
        
        # Colors
        self.BG_COLOR = "#1a1a2e"
        self.SNAKE_COLOR = "#00ff41"
        self.SNAKE_HEAD_COLOR = "#00cc33"
        self.FOOD_COLOR = "#ff4757"
        self.GRID_COLOR = "#16213e"
        self.TEXT_COLOR = "#ffffff"
        
        # Canvas setup
        self.canvas = tk.Canvas(
            root, 
            width=self.WIDTH, 
            height=self.HEIGHT,
            bg=self.BG_COLOR,
            highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)
        
        # Score display
        self.score_label = tk.Label(
            root,
            text="SCORE: 0",
            font=("Arial", 14, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.BG_COLOR
        )
        self.score_label.pack()
        
        # Watermark (clickable)
        self.watermark_label = tk.Label(
            root,
            text="spidrbot.com",
            font=("Arial", 9),
            fg="#888888",
            bg=self.BG_COLOR,
            cursor="hand2"
        )
        self.watermark_label.pack(pady=(5, 5))
        self.watermark_label.bind("<Button-1>", self.open_website)
        
        # Game state
        self.snake = deque()
        self.direction = None
        self.next_direction = None
        self.food = None
        self.score = 0
        self.game_over = False
        self.game_started = False
        
        # Input queue for responsive controls
        self.direction_queue = deque(maxlen=3)
        
        # Animation state
        self.food_pulse = 0
        self.food_pulse_direction = 1
        self.menu_bob = 0
        self.menu_animation_running = False
        self.fade_progress = 0
        self.is_fading = False
        self.input_blocked = False
        
        # Menu text elements
        self.title_text = None
        self.subtitle_text = None
        self.instruction_text = None
        
        # Key bindings - using both arrow keys and WASD
        self.root.bind('<Up>', lambda e: self.queue_direction('UP'))
        self.root.bind('<Down>', lambda e: self.queue_direction('DOWN'))
        self.root.bind('<Left>', lambda e: self.queue_direction('LEFT'))
        self.root.bind('<Right>', lambda e: self.queue_direction('RIGHT'))
        self.root.bind('w', lambda e: self.queue_direction('UP'))
        self.root.bind('s', lambda e: self.queue_direction('DOWN'))
        self.root.bind('a', lambda e: self.queue_direction('LEFT'))
        self.root.bind('d', lambda e: self.queue_direction('RIGHT'))
        self.root.bind('<Escape>', lambda e: self.root.iconify())  # Minimize on ESC
        self.root.bind('<space>', lambda e: self.root.destroy())  # Close on SPACE
        
        self.draw_grid()
        self.show_start_screen()
        self.animate_menu()
    
    def open_website(self, event):
        """Open spidrbot.com in browser"""
        import webbrowser
        webbrowser.open("https://spidrbot.com")
    
    def draw_grid(self):
        """Draw subtle grid lines"""
        for i in range(self.GRID_SIZE + 1):
            # Vertical lines
            x = i * self.CELL_SIZE
            self.canvas.create_line(
                x, 0, x, self.HEIGHT,
                fill=self.GRID_COLOR,
                width=1
            )
            # Horizontal lines
            y = i * self.CELL_SIZE
            self.canvas.create_line(
                0, y, self.WIDTH, y,
                fill=self.GRID_COLOR,
                width=1
            )
    
    def show_start_screen(self):
        """Display start screen"""
        self.menu_animation_running = True
        self.canvas.delete("game")
        self.canvas.delete("start")
        
        # Title (will be animated)
        self.title_text = self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2 - 50,
            text="SNAKE",
            font=("Arial", 28, "bold"),
            fill=self.SNAKE_COLOR,
            tags="start"
        )
        
        # Subtitle (will also bob)
        self.subtitle_text = self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2 + 10,
            text="Use Arrow Keys or WASD to move",
            font=("Arial", 11),
            fill=self.TEXT_COLOR,
            tags="start"
        )
        
        # Instructions (will also bob)
        self.instruction_text = self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2 + 35,
            text="Press any direction key to start",
            font=("Arial", 11),
            fill="#888888",
            tags="start"
        )
    
    def animate_menu(self):
        """Animate the main menu with smooth bobbing"""
        if self.menu_animation_running:
            # Create smooth bobbing motion using sine wave
            self.menu_bob += 0.08
            offset = math.sin(self.menu_bob) * 8
            
            # Move all menu text elements together
            try:
                self.canvas.coords(
                    self.title_text,
                    self.WIDTH // 2,
                    self.HEIGHT // 2 - 50 + offset
                )
                self.canvas.coords(
                    self.subtitle_text,
                    self.WIDTH // 2,
                    self.HEIGHT // 2 + 10 + offset
                )
                self.canvas.coords(
                    self.instruction_text,
                    self.WIDTH // 2,
                    self.HEIGHT // 2 + 35 + offset
                )
            except:
                pass
            
            self.root.after(30, self.animate_menu)
    
    def animate_fade_in(self):
        """Smooth fade-in animation for menu after death"""
        if self.is_fading and self.fade_progress < 1.0:
            self.fade_progress += 0.05
            
            # Calculate alpha-like effect by adjusting colors
            # Start from dark and fade to full brightness
            alpha = self.fade_progress
            
            # Update title color
            green_val = int(255 * alpha)
            title_color = f"#{0:02x}{green_val:02x}{int(65 * alpha):02x}"
            
            # Update text colors
            text_brightness = int(255 * alpha)
            text_color = f"#{text_brightness:02x}{text_brightness:02x}{text_brightness:02x}"
            
            gray_brightness = int(136 * alpha)
            gray_color = f"#{gray_brightness:02x}{gray_brightness:02x}{gray_brightness:02x}"
            
            try:
                self.canvas.itemconfig(self.title_text, fill=title_color)
                self.canvas.itemconfig(self.subtitle_text, fill=text_color)
                self.canvas.itemconfig(self.instruction_text, fill=gray_color)
            except:
                pass
            
            self.root.after(20, self.animate_fade_in)
        else:
            self.is_fading = False
            # Reset to final colors
            try:
                self.canvas.itemconfig(self.title_text, fill=self.SNAKE_COLOR)
                self.canvas.itemconfig(self.subtitle_text, fill=self.TEXT_COLOR)
                self.canvas.itemconfig(self.instruction_text, fill="#888888")
            except:
                pass
    
    def queue_direction(self, new_direction):
        """Queue direction changes for responsive input"""
        # Block input if disabled
        if self.input_blocked:
            return
            
        if not self.game_started:
            self.start_game()
            self.direction_queue.append(new_direction)
            return
        
        if self.game_over:
            return
        
        # Get the last direction in queue or current direction
        last_dir = self.direction_queue[-1] if self.direction_queue else self.direction
        
        # Prevent 180-degree turns
        opposite = {
            'UP': 'DOWN', 'DOWN': 'UP',
            'LEFT': 'RIGHT', 'RIGHT': 'LEFT'
        }
        
        if last_dir and new_direction == opposite.get(last_dir):
            return
        
        # Only queue if different from last queued direction
        if not self.direction_queue or new_direction != self.direction_queue[-1]:
            self.direction_queue.append(new_direction)
    
    def start_game(self):
        """Initialize game state"""
        self.menu_animation_running = False
        self.canvas.delete("start")
        self.game_started = True
        self.game_over = False
        self.score = 0
        self.direction = None
        self.direction_queue.clear()
        
        # Initialize snake in center
        center = self.GRID_SIZE // 2
        self.snake = deque([
            (center, center),
            (center, center + 1),
            (center, center + 2)
        ])
        
        self.spawn_food()
        self.update_score()
        self.game_loop()
    
    def spawn_food(self):
        """Spawn food at random empty location"""
        while True:
            x = random.randint(0, self.GRID_SIZE - 1)
            y = random.randint(0, self.GRID_SIZE - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break
    
    def game_loop(self):
        """Main game loop"""
        if self.game_over:
            return
        
        # Process next direction from queue
        if self.direction_queue:
            self.next_direction = self.direction_queue.popleft()
            
            # Validate direction change
            opposite = {
                'UP': 'DOWN', 'DOWN': 'UP',
                'LEFT': 'RIGHT', 'RIGHT': 'LEFT'
            }
            if not self.direction or self.next_direction != opposite.get(self.direction):
                self.direction = self.next_direction
        
        if self.direction:
            self.move_snake()
            self.check_collision()
            self.check_food()
        
        self.draw()
        self.root.after(self.GAME_SPEED, self.game_loop)
    
    def move_snake(self):
        """Move snake in current direction"""
        head_x, head_y = self.snake[0]
        
        if self.direction == 'UP':
            head_y -= 1
        elif self.direction == 'DOWN':
            head_y += 1
        elif self.direction == 'LEFT':
            head_x -= 1
        elif self.direction == 'RIGHT':
            head_x += 1
        
        self.snake.appendleft((head_x, head_y))
        self.snake.pop()
    
    def check_collision(self):
        """Check for collisions with walls or self"""
        head_x, head_y = self.snake[0]
        
        # Wall collision
        if head_x < 0 or head_x >= self.GRID_SIZE or head_y < 0 or head_y >= self.GRID_SIZE:
            self.end_game()
            return
        
        # Self collision
        if self.snake[0] in list(self.snake)[1:]:
            self.end_game()
            return
    
    def check_food(self):
        """Check if snake ate food"""
        if self.snake[0] == self.food:
            self.score += 1
            self.update_score()
            
            # Grow snake
            tail = self.snake[-1]
            self.snake.append(tail)
            
            self.spawn_food()
    
    def draw(self):
        """Draw everything on canvas"""
        self.canvas.delete("game")
        
        # Animate food pulse
        self.food_pulse += self.food_pulse_direction * 0.3
        if self.food_pulse > 3:
            self.food_pulse_direction = -1
        elif self.food_pulse < 0:
            self.food_pulse_direction = 1
        
        # Draw food with pulsing animation
        if self.food:
            fx, fy = self.food
            pulse_offset = int(self.food_pulse)
            self.canvas.create_oval(
                fx * self.CELL_SIZE + 3 + pulse_offset,
                fy * self.CELL_SIZE + 3 + pulse_offset,
                (fx + 1) * self.CELL_SIZE - 3 - pulse_offset,
                (fy + 1) * self.CELL_SIZE - 3 - pulse_offset,
                fill=self.FOOD_COLOR,
                outline="",
                tags="game"
            )
        
        # Draw snake with rounded effect
        for i, (x, y) in enumerate(self.snake):
            color = self.SNAKE_HEAD_COLOR if i == 0 else self.SNAKE_COLOR
            offset = 1 if i == 0 else 2
            self.canvas.create_rectangle(
                x * self.CELL_SIZE + offset,
                y * self.CELL_SIZE + offset,
                (x + 1) * self.CELL_SIZE - offset,
                (y + 1) * self.CELL_SIZE - offset,
                fill=color,
                outline="",
                tags="game"
            )
            
            # Add eye to head
            if i == 0:
                # Determine eye position based on direction
                eye_offset = 8
                if self.direction == 'UP':
                    eye_y = y * self.CELL_SIZE + 7
                    eye_x1 = x * self.CELL_SIZE + 7
                    eye_x2 = x * self.CELL_SIZE + 16
                elif self.direction == 'DOWN':
                    eye_y = (y + 1) * self.CELL_SIZE - 7
                    eye_x1 = x * self.CELL_SIZE + 7
                    eye_x2 = x * self.CELL_SIZE + 16
                elif self.direction == 'LEFT':
                    eye_x = x * self.CELL_SIZE + 7
                    eye_y1 = y * self.CELL_SIZE + 7
                    eye_y2 = y * self.CELL_SIZE + 16
                elif self.direction == 'RIGHT':
                    eye_x = (x + 1) * self.CELL_SIZE - 7
                    eye_y1 = y * self.CELL_SIZE + 7
                    eye_y2 = y * self.CELL_SIZE + 16
                else:
                    # Default right-facing eyes
                    eye_x = (x + 1) * self.CELL_SIZE - 7
                    eye_y1 = y * self.CELL_SIZE + 7
                    eye_y2 = y * self.CELL_SIZE + 16
                
                # Draw eyes
                if self.direction in ['UP', 'DOWN']:
                    self.canvas.create_oval(eye_x1, eye_y, eye_x1 + 3, eye_y + 3,
                                           fill="#000000", outline="", tags="game")
                    self.canvas.create_oval(eye_x2, eye_y, eye_x2 + 3, eye_y + 3,
                                           fill="#000000", outline="", tags="game")
                else:
                    self.canvas.create_oval(eye_x, eye_y1, eye_x + 3, eye_y1 + 3,
                                           fill="#000000", outline="", tags="game")
                    self.canvas.create_oval(eye_x, eye_y2, eye_x + 3, eye_y2 + 3,
                                           fill="#000000", outline="", tags="game")
    
    def update_score(self):
        """Update score display"""
        self.score_label.config(text=f"SCORE: {self.score}")
    
    def end_game(self):
        """Handle game over - smoothly fade in main menu"""
        self.game_over = True
        self.game_started = False
        
        # Block input for 0.5 seconds to prevent glitching
        self.input_blocked = True
        self.root.after(500, lambda: setattr(self, 'input_blocked', False))
        
        # Show menu immediately with fade-in animation
        self.show_start_screen()
        self.fade_progress = 0
        self.is_fading = True
        self.animate_fade_in()
        self.animate_menu()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
