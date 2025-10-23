import tkinter as tk
import random
import math

class BlockBreaker:
    def __init__(self, root):
        self.root = root
        self.root.title("block breaker")
        self.root.resizable(False, False)
        
        # Game constants
        self.WIDTH = 500
        self.HEIGHT = 600
        self.PADDLE_WIDTH = 80
        self.PADDLE_HEIGHT = 12
        self.BALL_SIZE = 10
        self.BLOCK_ROWS = 6
        self.BLOCK_COLS = 10
        self.BLOCK_WIDTH = 46
        self.BLOCK_HEIGHT = 20
        self.BLOCK_PADDING = 4
        self.BLOCK_OFFSET_TOP = 80
        self.GAME_SPEED = 16  # milliseconds
        self.POWERUP_SIZE = 20
        self.POWERUP_SPEED = 2
        
        # Colors - matching snake game theme
        self.BG_COLOR = "#1a1a2e"
        self.PADDLE_COLOR = "#4facfe"  # Clean blue
        self.BALL_COLOR = "#f5f5f5"    # Clean white
        self.TEXT_COLOR = "#ffffff"
        self.GRID_COLOR = "#16213e"
        
        # Block colors - vibrant gradient
        self.BLOCK_COLORS = [
            "#ff4757",  # Red
            "#ff6348",  # Orange-red
            "#ffa502",  # Orange
            "#ffdd59",  # Yellow
            "#26de81",  # Green
            "#20bf6b"   # Dark green
        ]
        
        # Powerup types and colors
        self.POWERUP_TYPES = {
            'EXPAND': {'color': '#4facfe', 'symbol': '⬌'},
            'MULTI': {'color': '#9b59b6', 'symbol': '●●●'},
            'SLOW': {'color': '#3498db', 'symbol': '⏱'},
            'FAST': {'color': '#e74c3c', 'symbol': '⚡'},
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
        
        # Score and lives display
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
        
        self.lives_label = tk.Label(
            info_frame,
            text="LIVES: 3",
            font=("Arial", 14, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.BG_COLOR
        )
        self.lives_label.pack(side=tk.LEFT, padx=20)
        
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
        self.paddle_x = self.WIDTH // 2 - self.PADDLE_WIDTH // 2
        self.paddle_y = self.HEIGHT - 40
        self.balls = []  # List of balls {x, y, dx, dy}
        self.score = 0
        self.lives = 3
        self.blocks = []
        self.powerups = []  # List of falling powerups
        self.game_started = False
        self.game_over = False
        self.game_won = False
        self.paddle_speed = 8
        self.base_paddle_width = 80
        self.paddle_expand_timer = 0
        self.ball_speed_modifier = 1.0
        self.speed_modifier_timer = 0
        
        # Input state
        self.keys_pressed = set()
        self.mouse_x = self.WIDTH // 2
        
        # Animation state
        self.menu_bob = 0
        self.menu_animation_running = False
        self.title_text = None
        self.subtitle_text = None
        self.instruction_text = None
        self.fade_progress = 0
        self.is_fading = False
        self.input_blocked = False
        
        # Key bindings
        self.root.bind('<Left>', lambda e: self.keys_pressed.add('LEFT'))
        self.root.bind('<Right>', lambda e: self.keys_pressed.add('RIGHT'))
        self.root.bind('<KeyRelease-Left>', lambda e: self.keys_pressed.discard('LEFT'))
        self.root.bind('<KeyRelease-Right>', lambda e: self.keys_pressed.discard('RIGHT'))
        self.root.bind('a', lambda e: self.keys_pressed.add('LEFT'))
        self.root.bind('d', lambda e: self.keys_pressed.add('RIGHT'))
        self.root.bind('<KeyRelease-a>', lambda e: self.keys_pressed.discard('LEFT'))
        self.root.bind('<KeyRelease-d>', lambda e: self.keys_pressed.discard('RIGHT'))
        self.root.bind('<space>', self.handle_space)
        self.root.bind('<Escape>', lambda e: self.root.iconify())
        
        # Mouse control
        self.canvas.bind('<Motion>', self.mouse_move)
        self.use_mouse = True
        
        self.show_start_screen()
        self.animate_menu()
    
    def open_website(self, event):
        """Open spidrbot.com in browser"""
        import webbrowser
        webbrowser.open("https://spidrbot.com")
    
    def mouse_move(self, event):
        """Track mouse position"""
        self.mouse_x = event.x
        self.use_mouse = True
    
    def show_start_screen(self):
        """Display start screen"""
        self.menu_animation_running = True
        self.canvas.delete("all")
        
        # Title
        self.title_text = self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2 - 60,
            text="BLOCK BREAKER",
            font=("Arial", 32, "bold"),
            fill=self.PADDLE_COLOR,
            tags="menu"
        )
        
        # Subtitle
        self.subtitle_text = self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2,
            text="Use Arrow Keys, WASD, or Mouse to move",
            font=("Arial", 11),
            fill=self.TEXT_COLOR,
            tags="menu"
        )
        
        # Instructions
        self.instruction_text = self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2 + 30,
            text="Press SPACE to start",
            font=("Arial", 11),
            fill="#888888",
            tags="menu"
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
                    self.HEIGHT // 2 + 30 + offset
                )
            except:
                pass
            
            self.root.after(30, self.animate_menu)
    
    def animate_fade_in(self):
        """Smooth fade-in animation for menu"""
        if self.is_fading and self.fade_progress < 1.0:
            self.fade_progress += 0.05
            alpha = self.fade_progress
            
            # Update colors with fade effect
            blue_val = int(79 * alpha)
            green_val = int(172 * alpha)
            blue2_val = int(254 * alpha)
            title_color = f"#{blue_val:02x}{green_val:02x}{blue2_val:02x}"
            
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
                self.canvas.itemconfig(self.title_text, fill=self.PADDLE_COLOR)
                self.canvas.itemconfig(self.subtitle_text, fill=self.TEXT_COLOR)
                self.canvas.itemconfig(self.instruction_text, fill="#888888")
            except:
                pass
    
    def handle_space(self, event):
        """Handle space bar press"""
        if self.input_blocked:
            return
        
        if not self.game_started:
            self.start_game()
        elif self.game_over or self.game_won:
            self.start_game()
    
    def start_game(self):
        """Initialize game state"""
        self.menu_animation_running = False
        self.canvas.delete("menu")
        self.game_started = True
        self.game_over = False
        self.game_won = False
        self.score = 0
        self.lives = 3
        self.powerups = []
        self.paddle_expand_timer = 0
        self.ball_speed_modifier = 1.0
        self.speed_modifier_timer = 0
        self.PADDLE_WIDTH = self.base_paddle_width
        
        # Reset paddle
        self.paddle_x = self.WIDTH // 2 - self.PADDLE_WIDTH // 2
        
        # Create initial ball and launch it immediately
        angle = random.uniform(-45, 45)
        speed = 5
        self.balls = [{
            'x': self.WIDTH // 2,
            'y': self.paddle_y - self.BALL_SIZE - 10,
            'dx': speed * math.sin(math.radians(angle)),
            'dy': -speed * math.cos(math.radians(angle)),
            'trail': []
        }]
        
        # Create blocks
        self.create_blocks()
        
        self.update_score()
        self.update_lives()
        self.game_loop()
    
    def create_blocks(self):
        """Create block grid"""
        self.blocks = []
        for row in range(self.BLOCK_ROWS):
            for col in range(self.BLOCK_COLS):
                x = col * (self.BLOCK_WIDTH + self.BLOCK_PADDING) + self.BLOCK_PADDING + 5
                y = row * (self.BLOCK_HEIGHT + self.BLOCK_PADDING) + self.BLOCK_OFFSET_TOP
                color = self.BLOCK_COLORS[row % len(self.BLOCK_COLORS)]
                points = (row + 1) * 10
                
                # 15% chance of powerup
                has_powerup = random.random() < 0.15
                powerup_type = random.choice(list(self.POWERUP_TYPES.keys())) if has_powerup else None
                
                self.blocks.append({
                    'x': x,
                    'y': y,
                    'color': color,
                    'points': points,
                    'visible': True,
                    'has_powerup': has_powerup,
                    'powerup_type': powerup_type
                })
    
    def game_loop(self):
        """Main game loop"""
        if self.game_over or self.game_won:
            return
        
        self.update_paddle()
        self.update_balls()
        self.update_powerups()
        self.update_timers()
        self.check_collisions()
        self.draw()
        
        self.root.after(self.GAME_SPEED, self.game_loop)
    
    def update_timers(self):
        """Update powerup timers"""
        if self.paddle_expand_timer > 0:
            self.paddle_expand_timer -= 1
            if self.paddle_expand_timer == 0:
                self.PADDLE_WIDTH = self.base_paddle_width
        
        if self.speed_modifier_timer > 0:
            self.speed_modifier_timer -= 1
            if self.speed_modifier_timer == 0:
                self.ball_speed_modifier = 1.0
                # Reset ball speeds
                for ball in self.balls:
                    speed = math.sqrt(ball['dx']**2 + ball['dy']**2)
                    if speed > 0:
                        ball['dx'] = ball['dx'] / abs(ball['dx']) * 5 if ball['dx'] != 0 else 0
                        ball['dy'] = ball['dy'] / abs(ball['dy']) * 5 if ball['dy'] != 0 else -5
    
    def update_paddle(self):
        """Update paddle position"""
        if self.use_mouse:
            self.paddle_x = self.mouse_x - self.PADDLE_WIDTH // 2
        else:
            if 'LEFT' in self.keys_pressed:
                self.paddle_x -= self.paddle_speed
            if 'RIGHT' in self.keys_pressed:
                self.paddle_x += self.paddle_speed
        
        if 'LEFT' in self.keys_pressed or 'RIGHT' in self.keys_pressed:
            self.use_mouse = False
        
        self.paddle_x = max(0, min(self.paddle_x, self.WIDTH - self.PADDLE_WIDTH))
    
    def update_balls(self):
        """Update all balls"""
        balls_to_remove = []
        
        for i, ball in enumerate(self.balls):
            # Add to trail
            ball['trail'].append((ball['x'], ball['y']))
            if len(ball['trail']) > 5:
                ball['trail'].pop(0)
            
            # Move ball
            ball['x'] += ball['dx'] * self.ball_speed_modifier
            ball['y'] += ball['dy'] * self.ball_speed_modifier
            
            # Wall collisions
            if ball['x'] <= 0 or ball['x'] >= self.WIDTH - self.BALL_SIZE:
                ball['dx'] = -ball['dx']
                ball['x'] = max(0, min(ball['x'], self.WIDTH - self.BALL_SIZE))
            
            if ball['y'] <= 0:
                ball['dy'] = -ball['dy']
                ball['y'] = 0
            
            # Bottom wall - remove ball
            if ball['y'] >= self.HEIGHT:
                balls_to_remove.append(i)
        
        # Remove balls that fell
        for i in reversed(balls_to_remove):
            self.balls.pop(i)
        
        # If no balls left, lose life
        if len(self.balls) == 0:
            self.lose_life()
    
    def update_powerups(self):
        """Update falling powerups"""
        powerups_to_remove = []
        
        for i, powerup in enumerate(self.powerups):
            powerup['y'] += self.POWERUP_SPEED
            
            # Check paddle collision
            if (powerup['y'] + self.POWERUP_SIZE >= self.paddle_y and
                powerup['y'] <= self.paddle_y + self.PADDLE_HEIGHT and
                powerup['x'] + self.POWERUP_SIZE >= self.paddle_x and
                powerup['x'] <= self.paddle_x + self.PADDLE_WIDTH):
                
                self.activate_powerup(powerup['type'])
                powerups_to_remove.append(i)
            
            # Remove if off screen
            elif powerup['y'] > self.HEIGHT:
                powerups_to_remove.append(i)
        
        for i in reversed(powerups_to_remove):
            self.powerups.pop(i)
    
    def activate_powerup(self, powerup_type):
        """Activate a powerup effect"""
        if powerup_type == 'EXPAND':
            self.PADDLE_WIDTH = self.base_paddle_width * 1.5
            self.paddle_expand_timer = 300  # ~5 seconds
        
        elif powerup_type == 'MULTI':
            # Add 2 more balls
            if len(self.balls) > 0:
                original = self.balls[0]
                for _ in range(2):
                    angle = random.uniform(-60, 60)
                    speed = 5
                    self.balls.append({
                        'x': original['x'],
                        'y': original['y'],
                        'dx': speed * math.sin(math.radians(angle)),
                        'dy': -speed * math.cos(math.radians(angle)),
                        'trail': []
                    })
        
        elif powerup_type == 'SLOW':
            self.ball_speed_modifier = 0.6
            self.speed_modifier_timer = 300
        
        elif powerup_type == 'FAST':
            self.ball_speed_modifier = 1.5
            self.speed_modifier_timer = 300
    
    def check_collisions(self):
        """Check for ball collisions"""
        for ball in self.balls:
            # Paddle collision
            if (ball['y'] + self.BALL_SIZE >= self.paddle_y and
                ball['y'] <= self.paddle_y + self.PADDLE_HEIGHT and
                ball['x'] + self.BALL_SIZE >= self.paddle_x and
                ball['x'] <= self.paddle_x + self.PADDLE_WIDTH):
                
                if ball['dy'] > 0:
                    hit_pos = ((ball['x'] + self.BALL_SIZE/2) - (self.paddle_x + self.PADDLE_WIDTH/2)) / (self.PADDLE_WIDTH/2)
                    angle = hit_pos * 60
                    speed = 5  # Reset to base speed
                    
                    ball['dx'] = speed * math.sin(math.radians(angle))
                    ball['dy'] = -speed * math.cos(math.radians(angle))
                    
                    if abs(ball['dy']) < 2:
                        ball['dy'] = -2 if ball['dy'] < 0 else 2
                    
                    ball['y'] = self.paddle_y - self.BALL_SIZE
            
            # Block collisions - check all edges properly
            ball_left = ball['x']
            ball_right = ball['x'] + self.BALL_SIZE
            ball_top = ball['y']
            ball_bottom = ball['y'] + self.BALL_SIZE
            ball_center_x = ball['x'] + self.BALL_SIZE / 2
            ball_center_y = ball['y'] + self.BALL_SIZE / 2
            
            for block in self.blocks:
                if not block['visible']:
                    continue
                
                block_left = block['x']
                block_right = block['x'] + self.BLOCK_WIDTH
                block_top = block['y']
                block_bottom = block['y'] + self.BLOCK_HEIGHT
                
                # Check if ball overlaps with block
                if (ball_right > block_left and ball_left < block_right and
                    ball_bottom > block_top and ball_top < block_bottom):
                    
                    block['visible'] = False
                    self.score += block['points']
                    self.update_score()
                    
                    # Spawn powerup
                    if block['has_powerup']:
                        self.powerups.append({
                            'x': block['x'] + self.BLOCK_WIDTH // 2 - self.POWERUP_SIZE // 2,
                            'y': block['y'],
                            'type': block['powerup_type']
                        })
                    
                    # Calculate collision side more accurately
                    prev_ball_left = ball_left - ball['dx'] * self.ball_speed_modifier
                    prev_ball_right = ball_right - ball['dx'] * self.ball_speed_modifier
                    prev_ball_top = ball_top - ball['dy'] * self.ball_speed_modifier
                    prev_ball_bottom = ball_bottom - ball['dy'] * self.ball_speed_modifier
                    
                    # Determine which side was hit
                    hit_from_left = prev_ball_right <= block_left
                    hit_from_right = prev_ball_left >= block_right
                    hit_from_top = prev_ball_bottom <= block_top
                    hit_from_bottom = prev_ball_top >= block_bottom
                    
                    if hit_from_left or hit_from_right:
                        ball['dx'] = -ball['dx']
                    elif hit_from_top or hit_from_bottom:
                        ball['dy'] = -ball['dy']
                    else:
                        # Corner hit - bounce both directions
                        ball['dx'] = -ball['dx']
                        ball['dy'] = -ball['dy']
                    
                    # Check win condition
                    if all(not b['visible'] for b in self.blocks):
                        self.win_game()
                    
                    break
    
    def lose_life(self):
        """Handle losing a life"""
        self.lives -= 1
        self.update_lives()
        
        if self.lives <= 0:
            self.end_game()
        else:
            # Reset ball
            angle = random.uniform(-45, 45)
            speed = 5
            self.balls = [{
                'x': self.WIDTH // 2,
                'y': self.paddle_y - self.BALL_SIZE - 10,
                'dx': speed * math.sin(math.radians(angle)),
                'dy': -speed * math.cos(math.radians(angle)),
                'trail': []
            }]
    
    def win_game(self):
        """Handle winning the game"""
        self.game_won = True
        self.game_started = False
        
        self.input_blocked = True
        self.root.after(500, lambda: setattr(self, 'input_blocked', False))
        
        self.show_win_screen()
    
    def show_win_screen(self):
        """Display win screen"""
        self.menu_animation_running = True
        self.canvas.delete("all")
        
        self.title_text = self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2 - 60,
            text="YOU WIN!",
            font=("Arial", 36, "bold"),
            fill=self.PADDLE_COLOR,
            tags="menu"
        )
        
        self.subtitle_text = self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2,
            text=f"Final Score: {self.score}",
            font=("Arial", 14),
            fill=self.TEXT_COLOR,
            tags="menu"
        )
        
        self.instruction_text = self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2 + 30,
            text="Press SPACE to play again",
            font=("Arial", 11),
            fill="#888888",
            tags="menu"
        )
        
        self.fade_progress = 0
        self.is_fading = True
        self.animate_fade_in()
        self.animate_menu()
    
    def end_game(self):
        """Handle game over"""
        self.game_over = True
        self.game_started = False
        
        self.input_blocked = True
        self.root.after(500, lambda: setattr(self, 'input_blocked', False))
        
        self.show_game_over_screen()
    
    def show_game_over_screen(self):
        """Display game over screen"""
        self.menu_animation_running = True
        self.canvas.delete("all")
        
        self.title_text = self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2 - 60,
            text="GAME OVER",
            font=("Arial", 36, "bold"),
            fill="#ff4757",
            tags="menu"
        )
        
        self.subtitle_text = self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2,
            text=f"Final Score: {self.score}",
            font=("Arial", 14),
            fill=self.TEXT_COLOR,
            tags="menu"
        )
        
        self.instruction_text = self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2 + 30,
            text="Press SPACE to try again",
            font=("Arial", 11),
            fill="#888888",
            tags="menu"
        )
        
        self.fade_progress = 0
        self.is_fading = True
        self.animate_fade_in()
        self.animate_menu()
    
    def draw(self):
        """Draw everything on canvas"""
        self.canvas.delete("game")
        
        # Draw blocks
        for block in self.blocks:
            if block['visible']:
                self.canvas.create_rectangle(
                    block['x'], block['y'],
                    block['x'] + self.BLOCK_WIDTH,
                    block['y'] + self.BLOCK_HEIGHT,
                    fill=block['color'],
                    outline="",
                    tags="game"
                )
                
                # Draw powerup indicator
                if block['has_powerup']:
                    powerup_info = self.POWERUP_TYPES[block['powerup_type']]
                    self.canvas.create_text(
                        block['x'] + self.BLOCK_WIDTH // 2,
                        block['y'] + self.BLOCK_HEIGHT // 2,
                        text=powerup_info['symbol'],
                        font=("Arial", 10, "bold"),
                        fill="#ffffff",
                        tags="game"
                    )
        
        # Draw falling powerups
        for powerup in self.powerups:
            powerup_info = self.POWERUP_TYPES[powerup['type']]
            self.canvas.create_rectangle(
                powerup['x'], powerup['y'],
                powerup['x'] + self.POWERUP_SIZE,
                powerup['y'] + self.POWERUP_SIZE,
                fill=powerup_info['color'],
                outline="",
                tags="game"
            )
            self.canvas.create_text(
                powerup['x'] + self.POWERUP_SIZE // 2,
                powerup['y'] + self.POWERUP_SIZE // 2,
                text=powerup_info['symbol'],
                font=("Arial", 8, "bold"),
                fill="#ffffff",
                tags="game"
            )
        
        # Draw paddle with glow effect
        self.canvas.create_rectangle(
            self.paddle_x - 1, self.paddle_y - 1,
            self.paddle_x + self.PADDLE_WIDTH + 1,
            self.paddle_y + self.PADDLE_HEIGHT + 1,
            fill="#3a8fd9",
            outline="",
            tags="game"
        )
        self.canvas.create_rectangle(
            self.paddle_x, self.paddle_y,
            self.paddle_x + self.PADDLE_WIDTH,
            self.paddle_y + self.PADDLE_HEIGHT,
            fill=self.PADDLE_COLOR,
            outline="",
            tags="game"
        )
        
        # Draw all balls
        for ball in self.balls:
            # Draw ball trail
            for i, (tx, ty) in enumerate(ball['trail']):
                alpha = (i + 1) / len(ball['trail']) * 0.5
                brightness = int(200 * alpha)
                trail_color = f"#{brightness:02x}{brightness:02x}{brightness:02x}"
                size = self.BALL_SIZE * (0.6 + 0.4 * alpha)
                offset = (self.BALL_SIZE - size) / 2
                self.canvas.create_oval(
                    tx + offset, ty + offset,
                    tx + size + offset, ty + size + offset,
                    fill=trail_color,
                    outline="",
                    tags="game"
                )
            
            # Draw ball
            self.canvas.create_oval(
                ball['x'], ball['y'],
                ball['x'] + self.BALL_SIZE,
                ball['y'] + self.BALL_SIZE,
                fill=self.BALL_COLOR,
                outline="",
                tags="game"
            )
    
    def update_score(self):
        """Update score display"""
        self.score_label.config(text=f"SCORE: {self.score}")
    
    def update_lives(self):
        """Update lives display"""
        self.lives_label.config(text=f"LIVES: {self.lives}")

if __name__ == "__main__":
    root = tk.Tk()
    game = BlockBreaker(root)
    root.mainloop()
