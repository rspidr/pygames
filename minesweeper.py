import tkinter as tk
import random
import math

class MinesweeperGame:
    def __init__(self, root):
        self.root = root
        self.root.title("minesweeper")
        self.root.resizable(False, False)
        
        # Game constants
        self.CELL_SIZE = 30
        self.PADDING = 10
        
        # Colors matching snake game
        self.BG_COLOR = "#1a1a2e"
        self.CELL_COLOR = "#16213e"
        self.CELL_REVEALED = "#0f3460"
        self.MINE_COLOR = "#ff4757"
        self.FLAG_COLOR = "#ffa502"
        self.TEXT_COLOR = "#ffffff"
        self.GRID_COLOR = "#2d4059"
        self.BUTTON_COLOR = "#00ff41"
        self.BUTTON_HOVER = "#00cc33"
        
        # Number colors
        self.NUMBER_COLORS = {
            1: "#00d2ff",
            2: "#00ff41",
            3: "#ff4757",
            4: "#5f27cd",
            5: "#ff6348",
            6: "#1dd1a1",
            7: "#000000",
            8: "#808080"
        }
        
        # Game state
        self.game_started = False
        self.game_over = False
        self.grid_size = 10
        self.mine_count = 10
        self.grid = []
        self.mines = set()
        self.revealed = set()
        self.flags = set()
        self.first_click = True
        
        # Animation state
        self.menu_bob = 0
        self.menu_animation_running = False
        self.button_hover_state = {}
        
        # UI elements
        self.canvas = None
        self.info_frame = None
        self.time_label = None
        self.mines_label = None
        self.game_time = 0
        self.timer_running = False
        
        self.show_main_menu()
    
    def show_main_menu(self):
        """Display main menu with difficulty options"""
        self.timer_running = False  # Stop timer when returning to menu
        self.clear_window()
        self.menu_animation_running = True
        
        # Menu canvas
        menu_width = 400
        menu_height = 450
        self.canvas = tk.Canvas(
            self.root,
            width=menu_width,
            height=menu_height,
            bg=self.BG_COLOR,
            highlightthickness=0
        )
        self.canvas.pack(padx=20, pady=20)
        
        # Title
        self.title_text = self.canvas.create_text(
            menu_width // 2,
            80,
            text="MINESWEEPER",
            font=("Arial", 32, "bold"),
            fill=self.BUTTON_COLOR
        )
        
        # Subtitle
        self.subtitle_text = self.canvas.create_text(
            menu_width // 2,
            130,
            text="Select Difficulty",
            font=("Arial", 14),
            fill=self.TEXT_COLOR
        )
        
        # Difficulty buttons
        difficulties = [
            ("Easy", 8, 10, 180),
            ("Medium", 14, 30, 240),
            ("Hard", 16, 40, 300),
            ("Expert", 20, 70, 360)
        ]
        
        self.menu_buttons = []
        for name, size, mines, y_pos in difficulties:
            btn_id = self.create_menu_button(
                menu_width // 2, y_pos,
                f"{name}\n{size}x{size} grid, {mines} mines",
                lambda s=size, m=mines: self.start_game(s, m)
            )
            self.menu_buttons.append(btn_id)
        
        # Watermark
        self.watermark = tk.Label(
            self.root,
            text="spidrbot.com",
            font=("Arial", 9),
            fg="#888888",
            bg=self.BG_COLOR,
            cursor="hand2"
        )
        self.watermark.pack(pady=(0, 10))
        self.watermark.bind("<Button-1>", self.open_website)
        
        # Bind keyboard shortcuts
        self.root.bind('<Escape>', lambda e: self.root.iconify())  # Minimize on ESC
        self.root.bind('<space>', lambda e: self.root.destroy())  # Close on SPACE
        
        self.animate_menu()
    
    def create_menu_button(self, x, y, text, command):
        """Create an animated menu button"""
        btn_width = 280
        btn_height = 50
        
        # Button background
        rect = self.canvas.create_rectangle(
            x - btn_width//2, y - btn_height//2,
            x + btn_width//2, y + btn_height//2,
            fill=self.CELL_COLOR,
            outline=self.BUTTON_COLOR,
            width=2,
            tags="button"
        )
        
        # Button text
        txt = self.canvas.create_text(
            x, y,
            text=text,
            font=("Arial", 12, "bold"),
            fill=self.TEXT_COLOR,
            tags="button"
        )
        
        # Bind hover and click events
        btn_group = (rect, txt)
        self.button_hover_state[btn_group] = False
        
        self.canvas.tag_bind(rect, "<Enter>", lambda e, b=btn_group: self.on_button_hover(b, True))
        self.canvas.tag_bind(rect, "<Leave>", lambda e, b=btn_group: self.on_button_hover(b, False))
        self.canvas.tag_bind(rect, "<Button-1>", lambda e: command())
        self.canvas.tag_bind(txt, "<Enter>", lambda e, b=btn_group: self.on_button_hover(b, True))
        self.canvas.tag_bind(txt, "<Leave>", lambda e, b=btn_group: self.on_button_hover(b, False))
        self.canvas.tag_bind(txt, "<Button-1>", lambda e: command())
        
        return btn_group
    
    def on_button_hover(self, button_group, hover):
        """Handle button hover effect"""
        rect, txt = button_group
        self.button_hover_state[button_group] = hover
        if hover:
            self.canvas.itemconfig(rect, fill=self.BUTTON_COLOR, outline=self.BUTTON_HOVER, width=3)
            self.canvas.itemconfig(txt, fill=self.BG_COLOR)
        else:
            self.canvas.itemconfig(rect, fill=self.CELL_COLOR, outline=self.BUTTON_COLOR, width=2)
            self.canvas.itemconfig(txt, fill=self.TEXT_COLOR)
    
    def animate_menu(self):
        """Animate the main menu with smooth bobbing"""
        if self.menu_animation_running:
            self.menu_bob += 0.08
            offset = math.sin(self.menu_bob) * 6
            
            try:
                # Bob title and subtitle
                self.canvas.coords(self.title_text, 200, 80 + offset)
                self.canvas.coords(self.subtitle_text, 200, 130 + offset)
                
                # Bob buttons slightly with fixed positions
                y_positions = [180, 240, 300, 360]
                for i, btn_group in enumerate(self.menu_buttons):
                    rect, txt = btn_group
                    base_y = y_positions[i]
                    btn_offset = math.sin(self.menu_bob + i * 0.3) * 3
                    
                    # Fixed button dimensions
                    btn_width = 280
                    btn_height = 50
                    
                    self.canvas.coords(rect,
                        200 - btn_width//2, base_y - btn_height//2 + btn_offset,
                        200 + btn_width//2, base_y + btn_height//2 + btn_offset)
                    self.canvas.coords(txt, 200, base_y + btn_offset)
            except:
                pass
            
            self.root.after(30, self.animate_menu)
    
    def start_game(self, size, mines):
        """Initialize game with selected difficulty"""
        self.menu_animation_running = False
        self.timer_running = False  # Stop timer before switching screens
        self.grid_size = size
        self.mine_count = mines
        self.game_started = True
        self.game_over = False
        self.first_click = True
        self.revealed = set()
        self.flags = set()
        self.mines = set()
        self.game_time = 0
        
        self.setup_game_ui()
    
    def setup_game_ui(self):
        """Setup game UI"""
        self.clear_window()
        
        # Info frame with better styling
        self.info_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        self.info_frame.pack(pady=(15, 10))
        
        # Container for timer (for animation)
        timer_container = tk.Frame(self.info_frame, bg=self.CELL_COLOR, relief=tk.FLAT, bd=0)
        timer_container.pack(side=tk.LEFT, padx=8)
        
        self.time_label = tk.Label(
            timer_container,
            text="TIME: 0",
            font=("Arial", 13, "bold"),
            fg=self.BUTTON_COLOR,
            bg=self.CELL_COLOR,
            padx=20,
            pady=8,
            width=10
        )
        self.time_label.pack()
        
        # Container for mines
        mines_container = tk.Frame(self.info_frame, bg=self.CELL_COLOR, relief=tk.FLAT, bd=0)
        mines_container.pack(side=tk.LEFT, padx=8)
        
        self.mines_label = tk.Label(
            mines_container,
            text=f"MINES: {self.mine_count}",
            font=("Arial", 13, "bold"),
            fg=self.FLAG_COLOR,
            bg=self.CELL_COLOR,
            padx=20,
            pady=8
        )
        self.mines_label.pack()
        
        # Back button with hover effect
        self.back_button = tk.Button(
            self.info_frame,
            text="◄ MENU",
            font=("Arial", 11, "bold"),
            fg=self.BG_COLOR,
            bg=self.BUTTON_COLOR,
            activebackground=self.BUTTON_HOVER,
            activeforeground=self.BG_COLOR,
            command=self.show_main_menu,
            cursor="hand2",
            relief=tk.FLAT,
            padx=18,
            pady=8,
            borderwidth=0
        )
        self.back_button.pack(side=tk.LEFT, padx=8)
        
        # Bind hover effects to button
        self.back_button.bind("<Enter>", lambda e: self.back_button.config(bg=self.BUTTON_HOVER))
        self.back_button.bind("<Leave>", lambda e: self.back_button.config(bg=self.BUTTON_COLOR))
        
        # Game canvas
        canvas_size = self.grid_size * self.CELL_SIZE
        self.canvas = tk.Canvas(
            self.root,
            width=canvas_size,
            height=canvas_size,
            bg=self.BG_COLOR,
            highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)
        
        # Watermark
        self.watermark = tk.Label(
            self.root,
            text="spidrbot.com",
            font=("Arial", 9),
            fg="#888888",
            bg=self.BG_COLOR,
            cursor="hand2"
        )
        self.watermark.pack(pady=(0, 10))
        self.watermark.bind("<Button-1>", self.open_website)
        
        # Bind mouse events
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        
        # Bind keyboard shortcuts
        self.root.bind('<Escape>', lambda e: self.root.iconify())  # Minimize on ESC
        self.root.bind('<space>', lambda e: self.root.destroy())  # Close on SPACE
        
        self.draw_grid()
    
    def draw_grid(self):
        """Draw the minesweeper grid"""
        self.canvas.delete("all")
        
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x1 = col * self.CELL_SIZE
                y1 = row * self.CELL_SIZE
                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE
                
                pos = (row, col)
                
                if pos in self.revealed:
                    # Revealed cell
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill=self.CELL_REVEALED,
                        outline=self.GRID_COLOR,
                        width=2
                    )
                    
                    if pos in self.mines:
                        # Draw mine
                        self.canvas.create_oval(
                            x1 + 8, y1 + 8, x2 - 8, y2 - 8,
                            fill=self.MINE_COLOR,
                            outline=""
                        )
                    else:
                        # Draw number
                        count = self.count_adjacent_mines(row, col)
                        if count > 0:
                            self.canvas.create_text(
                                (x1 + x2) // 2, (y1 + y2) // 2,
                                text=str(count),
                                font=("Arial", 14, "bold"),
                                fill=self.NUMBER_COLORS.get(count, self.TEXT_COLOR)
                            )
                else:
                    # Unrevealed cell
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill=self.CELL_COLOR,
                        outline=self.GRID_COLOR,
                        width=2
                    )
                    
                    if pos in self.flags:
                        # Draw flag
                        cx = (x1 + x2) // 2
                        cy = (y1 + y2) // 2
                        self.canvas.create_polygon(
                            cx - 6, cy - 6,
                            cx + 6, cy,
                            cx - 6, cy + 6,
                            fill=self.FLAG_COLOR,
                            outline=""
                        )
    
    def on_left_click(self, event):
        """Handle left click (reveal cell)"""
        if self.game_over:
            return
        
        col = event.x // self.CELL_SIZE
        row = event.y // self.CELL_SIZE
        
        if row < 0 or row >= self.grid_size or col < 0 or col >= self.grid_size:
            return
        
        pos = (row, col)
        
        if pos in self.flags or pos in self.revealed:
            return
        
        if self.first_click:
            self.generate_mines(pos)
            self.first_click = False
            self.timer_running = True
            self.update_timer()
        
        self.reveal_cell(pos)
    
    def on_right_click(self, event):
        """Handle right click (flag cell)"""
        if self.game_over or self.first_click:
            return
        
        col = event.x // self.CELL_SIZE
        row = event.y // self.CELL_SIZE
        
        if row < 0 or row >= self.grid_size or col < 0 or col >= self.grid_size:
            return
        
        pos = (row, col)
        
        if pos in self.revealed:
            return
        
        if pos in self.flags:
            self.flags.remove(pos)
        else:
            self.flags.add(pos)
        
        self.update_mines_label()
        self.draw_grid()
    
    def generate_mines(self, safe_pos):
        """Generate mines, avoiding the first clicked position"""
        self.mines = set()
        
        # Generate safe positions (clicked cell and its neighbors)
        safe_positions = {safe_pos}
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = safe_pos[0] + dr, safe_pos[1] + dc
                if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                    safe_positions.add((nr, nc))
        
        # Generate mines
        available_positions = [
            (r, c) for r in range(self.grid_size) for c in range(self.grid_size)
            if (r, c) not in safe_positions
        ]
        
        self.mines = set(random.sample(available_positions, min(self.mine_count, len(available_positions))))
    
    def reveal_cell(self, pos):
        """Reveal a cell and check win/lose conditions"""
        if pos in self.revealed or pos in self.flags:
            return
        
        self.revealed.add(pos)
        
        if pos in self.mines:
            self.game_over = True
            self.timer_running = False
            self.reveal_all_mines()
            self.show_game_over(False)
            return
        
        # Auto-reveal adjacent cells if no adjacent mines
        if self.count_adjacent_mines(pos[0], pos[1]) == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = pos[0] + dr, pos[1] + dc
                    if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                        new_pos = (nr, nc)
                        if new_pos not in self.revealed:
                            self.reveal_cell(new_pos)
        
        self.draw_grid()
        self.check_win()
    
    def count_adjacent_mines(self, row, col):
        """Count mines adjacent to a cell"""
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                    if (nr, nc) in self.mines:
                        count += 1
        return count
    
    def reveal_all_mines(self):
        """Reveal all mines when game is lost"""
        for mine in self.mines:
            self.revealed.add(mine)
        self.draw_grid()
    
    def check_win(self):
        """Check if player has won"""
        total_cells = self.grid_size * self.grid_size
        if len(self.revealed) == total_cells - len(self.mines):
            self.game_over = True
            self.timer_running = False
            self.show_game_over(True)
    
    def show_game_over(self, won):
        """Display game over message"""
        canvas_size = self.grid_size * self.CELL_SIZE
        
        # Semi-transparent overlay
        self.canvas.create_rectangle(
            0, 0, canvas_size, canvas_size,
            fill=self.BG_COLOR,
            stipple="gray50"
        )
        
        # Message
        message = "YOU WIN!" if won else "GAME OVER"
        color = self.BUTTON_COLOR if won else self.MINE_COLOR
        
        self.canvas.create_text(
            canvas_size // 2, canvas_size // 2 - 20,
            text=message,
            font=("Arial", 28, "bold"),
            fill=color
        )
        
        self.canvas.create_text(
            canvas_size // 2, canvas_size // 2 + 20,
            text=f"Time: {self.game_time}s",
            font=("Arial", 14),
            fill=self.TEXT_COLOR
        )
    
    def update_timer(self):
        """Update game timer"""
        if self.timer_running:
            self.game_time += 1
            self.time_label.config(text=f"TIME: {self.game_time}")
            self.root.after(1000, self.update_timer)
    
    def update_mines_label(self):
        """Update mines remaining counter"""
        remaining = self.mine_count - len(self.flags)
        self.mines_label.config(text=f"MINES: {remaining}")
    
    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def open_website(self, event):
        """Open spidrbot.com in browser"""
        import webbrowser
        webbrowser.open("https://spidrbot.com")

if __name__ == "__main__":
    root = tk.Tk()
    game = MinesweeperGame(root)
    root.mainloop()
