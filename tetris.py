import tkinter as tk
import random
import math

class TetrisGame:
    def __init__(self, root):
        self.root = root
        self.root.title("tetris")
        self.root.resizable(False, False)
        
        # Game constants
        self.GRID_WIDTH = 10
        self.GRID_HEIGHT = 20
        self.CELL_SIZE = 25
        self.WIDTH = self.GRID_WIDTH * self.CELL_SIZE
        self.HEIGHT = self.GRID_HEIGHT * self.CELL_SIZE
        self.GAME_SPEED = 500  # milliseconds
        
        # Colors (matching snake game style)
        self.BG_COLOR = "#1a1a2e"
        self.GRID_COLOR = "#16213e"
        self.TEXT_COLOR = "#ffffff"
        self.PIECE_COLORS = {
            'I': "#00ff41",  # Green (like snake)
            'O': "#ffdd00",  # Yellow
            'T': "#ff4757",  # Red (like food)
            'S': "#00d2ff",  # Cyan
            'Z': "#ff6348",  # Orange
            'J': "#5f27cd",  # Purple
            'L': "#ff9ff3"   # Pink
        }
        
        # Tetromino shapes
        self.SHAPES = {
            'I': [(0, 1), (1, 1), (2, 1), (3, 1)],
            'O': [(0, 0), (1, 0), (0, 1), (1, 1)],
            'T': [(1, 0), (0, 1), (1, 1), (2, 1)],
            'S': [(1, 0), (2, 0), (0, 1), (1, 1)],
            'Z': [(0, 0), (1, 0), (1, 1), (2, 1)],
            'J': [(0, 0), (0, 1), (1, 1), (2, 1)],
            'L': [(2, 0), (0, 1), (1, 1), (2, 1)]
        }
        
        # Canvas setup
        self.canvas = tk.Canvas(
            root,
            width=self.WIDTH,
            height=self.HEIGHT,
            bg=self.BG_COLOR,
            highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)
        
        # Info panel
        info_frame = tk.Frame(root, bg=self.BG_COLOR)
        info_frame.pack()
        
        self.score_label = tk.Label(
            info_frame,
            text="SCORE: 0",
            font=("Arial", 14, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.BG_COLOR
        )
        self.score_label.pack(side=tk.LEFT, padx=20)
        
        self.lines_label = tk.Label(
            info_frame,
            text="LINES: 0",
            font=("Arial", 14, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.BG_COLOR
        )
        self.lines_label.pack(side=tk.LEFT, padx=20)
        
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
        self.grid = [[None for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)]
        self.current_piece = None
        self.current_shape = None
        self.current_color = None
        self.current_x = 0
        self.current_y = 0
        self.score = 0
        self.lines_cleared = 0
        self.game_over = False
        self.game_started = False
        self.input_blocked = False
        
        # Animation state
        self.menu_bob = 0
        self.menu_animation_running = False
        self.fade_progress = 0
        self.is_fading = False
        
        # Menu text elements
        self.title_text = None
        self.subtitle_text = None
        self.instruction_text = None
        
        # Key bindings
        self.root.bind('<Left>', lambda e: self.move_piece(-1, 0))
        self.root.bind('<Right>', lambda e: self.move_piece(1, 0))
        self.root.bind('<Down>', lambda e: self.move_piece(0, 1))
        self.root.bind('<Up>', lambda e: self.rotate_piece())
        self.root.bind('a', lambda e: self.move_piece(-1, 0))
        self.root.bind('d', lambda e: self.move_piece(1, 0))
        self.root.bind('s', lambda e: self.move_piece(0, 1))
        self.root.bind('w', lambda e: self.rotate_piece())
        self.root.bind('<space>', lambda e: self.hard_drop())
        self.root.bind('<Escape>', lambda e: self.root.iconify())
        
        self.draw_grid()
        self.show_start_screen()
        self.animate_menu()
    
    def open_website(self, event):
        """Open spidrbot.com in browser"""
        import webbrowser
        webbrowser.open("https://spidrbot.com")
    
    def draw_grid(self):
        """Draw subtle grid lines"""
        for i in range(self.GRID_WIDTH + 1):
            x = i * self.CELL_SIZE
            self.canvas.create_line(
                x, 0, x, self.HEIGHT,
                fill=self.GRID_COLOR,
                width=1
            )
        for i in range(self.GRID_HEIGHT + 1):
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
        
        self.title_text = self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2 - 60,
            text="TETRIS",
            font=("Arial", 28, "bold"),
            fill="#00ff41",
            tags="start"
        )
        
        self.subtitle_text = self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2,
            text="Arrow Keys or WASD to move\n↑/W to rotate | Space to drop",
            font=("Arial", 11),
            fill=self.TEXT_COLOR,
            tags="start"
        )
        
        self.instruction_text = self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2 + 50,
            text="Press any key to start",
            font=("Arial", 11),
            fill="#888888",
            tags="start"
        )
    
    def animate_menu(self):
        """Animate the main menu with smooth bobbing"""
        if self.menu_animation_running:
            self.menu_bob += 0.08
            offset = math.sin(self.menu_bob) * 8
            
            try:
                self.canvas.coords(
                    self.title_text,
                    self.WIDTH // 2,
                    self.HEIGHT // 2 - 60 + offset
                )
                self.canvas.coords(
                    self.subtitle_text,
                    self.WIDTH // 2,
                    self.HEIGHT // 2 + offset
                )
                self.canvas.coords(
                    self.instruction_text,
                    self.WIDTH // 2,
                    self.HEIGHT // 2 + 50 + offset
                )
            except:
                pass
            
            self.root.after(30, self.animate_menu)
    
    def animate_fade_in(self):
        """Smooth fade-in animation for menu after death"""
        if self.is_fading and self.fade_progress < 1.0:
            self.fade_progress += 0.05
            alpha = self.fade_progress
            
            green_val = int(255 * alpha)
            title_color = f"#{0:02x}{green_val:02x}{int(65 * alpha):02x}"
            
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
            try:
                self.canvas.itemconfig(self.title_text, fill="#00ff41")
                self.canvas.itemconfig(self.subtitle_text, fill=self.TEXT_COLOR)
                self.canvas.itemconfig(self.instruction_text, fill="#888888")
            except:
                pass
    
    def start_game(self):
        """Initialize game state"""
        if self.input_blocked:
            return
            
        self.menu_animation_running = False
        self.canvas.delete("start")
        self.game_started = True
        self.game_over = False
        self.score = 0
        self.lines_cleared = 0
        self.grid = [[None for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)]
        
        self.update_score()
        self.spawn_piece()
        self.game_loop()
    
    def spawn_piece(self):
        """Spawn a new tetromino"""
        shape_type = random.choice(list(self.SHAPES.keys()))
        self.current_shape = shape_type
        self.current_piece = self.SHAPES[shape_type].copy()
        self.current_color = self.PIECE_COLORS[shape_type]
        self.current_x = self.GRID_WIDTH // 2 - 2
        self.current_y = 0
        
        # Check if spawn position is valid
        if not self.is_valid_position(self.current_piece, self.current_x, self.current_y):
            self.end_game()
    
    def is_valid_position(self, piece, x, y):
        """Check if piece position is valid"""
        for px, py in piece:
            new_x = x + px
            new_y = y + py
            
            if new_x < 0 or new_x >= self.GRID_WIDTH:
                return False
            if new_y >= self.GRID_HEIGHT:
                return False
            if new_y >= 0 and self.grid[new_y][new_x] is not None:
                return False
        
        return True
    
    def move_piece(self, dx, dy):
        """Move piece by dx, dy"""
        if not self.game_started or self.game_over or self.input_blocked:
            if not self.game_started and not self.input_blocked:
                self.start_game()
            return
        
        new_x = self.current_x + dx
        new_y = self.current_y + dy
        
        if self.is_valid_position(self.current_piece, new_x, new_y):
            self.current_x = new_x
            self.current_y = new_y
            self.draw()
        elif dy > 0:  # Moving down and can't - lock piece
            self.lock_piece()
    
    def rotate_piece(self):
        """Rotate piece 90 degrees clockwise"""
        if not self.game_started or self.game_over or self.input_blocked:
            if not self.game_started and not self.input_blocked:
                self.start_game()
            return
        
        if self.current_shape == 'O':  # O piece doesn't rotate
            return
        
        # Rotate around center
        rotated = []
        for x, y in self.current_piece:
            # Rotate 90 degrees clockwise: (x,y) -> (y, -x)
            # Adjust for piece center
            if self.current_shape == 'I':
                new_x = 2 - y
                new_y = x - 1
            else:
                new_x = 2 - y
                new_y = x
            rotated.append((new_x, new_y))
        
        # Try to place rotated piece
        if self.is_valid_position(rotated, self.current_x, self.current_y):
            self.current_piece = rotated
        # Try wall kick left
        elif self.is_valid_position(rotated, self.current_x - 1, self.current_y):
            self.current_x -= 1
            self.current_piece = rotated
        # Try wall kick right
        elif self.is_valid_position(rotated, self.current_x + 1, self.current_y):
            self.current_x += 1
            self.current_piece = rotated
        
        self.draw()
    
    def hard_drop(self):
        """Drop piece instantly"""
        if not self.game_started or self.game_over or self.input_blocked:
            return
        
        while self.is_valid_position(self.current_piece, self.current_x, self.current_y + 1):
            self.current_y += 1
        
        self.lock_piece()
        self.draw()
    
    def lock_piece(self):
        """Lock piece into grid"""
        for px, py in self.current_piece:
            grid_x = self.current_x + px
            grid_y = self.current_y + py
            if grid_y >= 0:
                self.grid[grid_y][grid_x] = self.current_color
        
        self.clear_lines()
        self.spawn_piece()
    
    def clear_lines(self):
        """Clear completed lines"""
        lines_to_clear = []
        
        for y in range(self.GRID_HEIGHT):
            if all(self.grid[y][x] is not None for x in range(self.GRID_WIDTH)):
                lines_to_clear.append(y)
        
        if lines_to_clear:
            # Remove cleared lines
            for y in sorted(lines_to_clear, reverse=True):
                del self.grid[y]
                self.grid.insert(0, [None for _ in range(self.GRID_WIDTH)])
            
            # Update score
            lines_count = len(lines_to_clear)
            self.lines_cleared += lines_count
            points = [0, 100, 300, 500, 800]  # Points for 0-4 lines
            self.score += points[min(lines_count, 4)]
            self.update_score()
    
    def game_loop(self):
        """Main game loop"""
        if self.game_over or not self.game_started:
            return
        
        # Move piece down
        if not self.is_valid_position(self.current_piece, self.current_x, self.current_y + 1):
            self.lock_piece()
        else:
            self.current_y += 1
        
        self.draw()
        
        # Speed increases with level
        speed = max(100, self.GAME_SPEED - (self.lines_cleared // 10) * 50)
        self.root.after(speed, self.game_loop)
    
    def draw(self):
        """Draw everything on canvas"""
        self.canvas.delete("game")
        
        # Draw locked pieces
        for y in range(self.GRID_HEIGHT):
            for x in range(self.GRID_WIDTH):
                if self.grid[y][x] is not None:
                    self.canvas.create_rectangle(
                        x * self.CELL_SIZE + 2,
                        y * self.CELL_SIZE + 2,
                        (x + 1) * self.CELL_SIZE - 2,
                        (y + 1) * self.CELL_SIZE - 2,
                        fill=self.grid[y][x],
                        outline="",
                        tags="game"
                    )
        
        # Draw current piece
        if self.current_piece:
            for px, py in self.current_piece:
                x = self.current_x + px
                y = self.current_y + py
                if y >= 0:
                    self.canvas.create_rectangle(
                        x * self.CELL_SIZE + 2,
                        y * self.CELL_SIZE + 2,
                        (x + 1) * self.CELL_SIZE - 2,
                        (y + 1) * self.CELL_SIZE - 2,
                        fill=self.current_color,
                        outline="",
                        tags="game"
                    )
    
    def update_score(self):
        """Update score display"""
        self.score_label.config(text=f"SCORE: {self.score}")
        self.lines_label.config(text=f"LINES: {self.lines_cleared}")
    
    def end_game(self):
        """Handle game over"""
        self.game_over = True
        self.game_started = False
        
        # Block input for 0.5 seconds
        self.input_blocked = True
        self.root.after(500, lambda: setattr(self, 'input_blocked', False))
        
        # Show menu with fade-in
        self.show_start_screen()
        self.fade_progress = 0
        self.is_fading = True
        self.animate_fade_in()
        self.animate_menu()

if __name__ == "__main__":
    root = tk.Tk()
    game = TetrisGame(root)
    root.mainloop()
