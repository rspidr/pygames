import tkinter as tk
import random
import math

class WordleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("wordle")
        self.root.resizable(False, False)
        
        # Word list - common 5-letter words
        self.WORD_LIST = [
            "about", "above", "abuse", "actor", "acute", "admit", "adopt", "adult", "after", "again",
            "agent", "agree", "ahead", "alarm", "album", "alert", "alike", "alive", "allow", "alone",
            "along", "alter", "among", "anger", "angle", "angry", "apart", "apple", "apply", "arena",
            "argue", "arise", "array", "aside", "asset", "audio", "avoid", "award", "aware", "badly",
            "baker", "bases", "basic", "basis", "beach", "began", "begin", "begun", "being", "below",
            "bench", "billy", "birth", "black", "blade", "blame", "blind", "block", "blood", "board",
            "boost", "booth", "bound", "brain", "brand", "bread", "break", "breed", "brief", "bring",
            "broad", "broke", "brown", "build", "built", "buyer", "cable", "calif", "carry", "catch",
            "cause", "chain", "chair", "chart", "chase", "cheap", "check", "chest", "chief", "child",
            "china", "chose", "civil", "claim", "class", "clean", "clear", "click", "clock", "close",
            "coach", "coast", "could", "count", "court", "cover", "crack", "craft", "crash", "crazy",
            "cream", "crime", "cross", "crowd", "crown", "crude", "curve", "cycle", "daily", "dance",
            "dated", "dealt", "death", "debut", "delay", "depth", "doing", "doubt", "dozen", "draft",
            "drama", "drank", "drawn", "dream", "dress", "drill", "drink", "drive", "drove", "dying",
            "eager", "early", "earth", "eight", "elite", "empty", "enemy", "enjoy", "enter", "entry",
            "equal", "error", "event", "every", "exact", "exist", "extra", "faith", "false", "fault",
            "fiber", "field", "fifth", "fifty", "fight", "final", "first", "fixed", "flash", "fleet",
            "floor", "fluid", "focus", "force", "forth", "forty", "forum", "found", "frame", "frank",
            "fraud", "fresh", "front", "fruit", "fully", "funny", "giant", "given", "glass", "globe",
            "going", "grace", "grade", "grand", "grant", "grass", "great", "green", "gross", "group",
            "grown", "guard", "guess", "guest", "guide", "happy", "harry", "heart", "heavy", "hence",
            "henry", "horse", "hotel", "house", "human", "ideal", "image", "imply", "index", "inner",
            "input", "issue", "japan", "jimmy", "joint", "jones", "judge", "known", "label", "large",
            "laser", "later", "laugh", "layer", "learn", "lease", "least", "leave", "legal", "lemon",
            "level", "lewis", "light", "limit", "links", "lives", "local", "logic", "loose", "lower",
            "lucky", "lunch", "lying", "magic", "major", "maker", "march", "maria", "match", "maybe",
            "mayor", "meant", "media", "metal", "might", "minor", "minus", "mixed", "model", "money",
            "month", "moral", "motor", "mount", "mouse", "mouth", "movie", "music", "needs", "never",
            "newly", "night", "noise", "north", "noted", "novel", "nurse", "occur", "ocean", "offer",
            "often", "order", "other", "ought", "paint", "panel", "paper", "party", "peace", "peter",
            "phase", "phone", "photo", "piece", "pilot", "pitch", "place", "plain", "plane", "plant",
            "plate", "point", "pound", "power", "press", "price", "pride", "prime", "print", "prior",
            "prize", "proof", "proud", "prove", "queen", "quick", "quiet", "quite", "radio", "raise",
            "range", "rapid", "ratio", "reach", "ready", "refer", "right", "rival", "river", "robin",
            "roger", "roman", "rough", "round", "route", "royal", "rural", "scale", "scene", "scope",
            "score", "sense", "serve", "seven", "shall", "shape", "share", "sharp", "sheet", "shelf",
            "shell", "shift", "shine", "shirt", "shock", "shoot", "short", "shown", "sight", "since",
            "sixth", "sixty", "sized", "skill", "sleep", "slide", "small", "smart", "smile", "smith",
            "smoke", "solid", "solve", "sorry", "sound", "south", "space", "spare", "speak", "speed",
            "spend", "spent", "split", "spoke", "sport", "staff", "stage", "stake", "stand", "start",
            "state", "steam", "steel", "stick", "still", "stock", "stone", "stood", "store", "storm",
            "story", "strip", "stuck", "study", "stuff", "style", "sugar", "suite", "super", "sweet",
            "table", "taken", "taste", "taxes", "teach", "terry", "texas", "thank", "theft", "their",
            "theme", "there", "these", "thick", "thing", "think", "third", "those", "three", "threw",
            "throw", "tight", "times", "tired", "title", "today", "topic", "total", "touch", "tough",
            "tower", "track", "trade", "train", "treat", "trend", "trial", "tribe", "trick", "tried",
            "tries", "truck", "truly", "trust", "truth", "twice", "under", "undue", "union", "unity",
            "until", "upper", "upset", "urban", "usage", "usual", "valid", "value", "video", "virus",
            "visit", "vital", "vocal", "voice", "waste", "watch", "water", "wheel", "where", "which",
            "while", "white", "whole", "whose", "woman", "women", "world", "worry", "worse", "worst",
            "worth", "would", "wound", "write", "wrong", "wrote", "yield", "young", "youth"
        ]
        
        # Game constants
        self.MAX_GUESSES = 6
        self.WORD_LENGTH = 5
        self.CELL_SIZE = 70
        self.CELL_GAP = 8
        self.KEYBOARD_CELL_WIDTH = 43
        self.KEYBOARD_CELL_HEIGHT = 58
        
        # Colors (matching snake game)
        self.BG_COLOR = "#1a1a2e"
        self.CORRECT_COLOR = "#00ff41"
        self.PRESENT_COLOR = "#ffcc00"
        self.ABSENT_COLOR = "#3a3a52"
        self.UNUSED_COLOR = "#16213e"  # Darker for unused keys
        self.EMPTY_COLOR = "#16213e"
        self.TEXT_COLOR = "#ffffff"
        self.BORDER_COLOR = "#3a3a52"
        
        # Calculate window dimensions
        self.WIDTH = 530
        self.HEIGHT = 820
        
        # Canvas setup
        self.canvas = tk.Canvas(
            root,
            width=self.WIDTH,
            height=self.HEIGHT,
            bg=self.BG_COLOR,
            highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)
        
        # Title
        self.title_label = tk.Label(
            root,
            text="WORDLE",
            font=("Arial", 24, "bold"),
            fg=self.CORRECT_COLOR,
            bg=self.BG_COLOR
        )
        self.canvas.create_window(self.WIDTH // 2, 30, window=self.title_label)
        
        # Watermark (clickable)
        self.watermark_label = tk.Label(
            root,
            text="spidrbot.com",
            font=("Arial", 9),
            fg="#888888",
            bg=self.BG_COLOR,
            cursor="hand2"
        )
        self.watermark_label.pack(pady=(0, 5))
        self.watermark_label.bind("<Button-1>", self.open_website)
        
        # Game state
        self.target_word = ""
        self.current_guess = ""
        self.guesses = []
        self.current_row = 0
        self.game_over = False
        self.keyboard_state = {}  # Track key colors
        self.animating = False
        
        # Animation
        self.shake_offset = 0
        self.title_bob = 0
        self.message_bob = 0
        self.message_scale = 0
        self.showing_message = False
        
        # Keyboard layout
        self.keyboard_rows = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['ENTER', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '⌫']
        ]
        
        # Store keyboard button positions for click detection
        self.keyboard_buttons = {}
        
        # Key bindings
        self.root.bind('<Key>', self.handle_key)
        self.root.bind('<Escape>', lambda e: self.root.iconify())
        self.canvas.bind('<Button-1>', self.handle_click)
        
        self.start_game()
        self.draw_board()
        self.draw_keyboard()
        self.animate_title()
    
    def open_website(self, event):
        """Open spidrbot.com in browser"""
        import webbrowser
        webbrowser.open("https://spidrbot.com")
    
    def start_game(self):
        """Initialize new game"""
        self.target_word = random.choice(self.WORD_LIST).upper()
        self.current_guess = ""
        self.guesses = []
        self.current_row = 0
        self.game_over = False
        self.keyboard_state = {}
        self.animating = False
    
    def animate_title(self):
        """Animate title bobbing"""
        self.title_bob += 0.08
        offset = math.sin(self.title_bob) * 3
        try:
            self.canvas.coords(
                self.canvas.find_withtag("title")[0] if self.canvas.find_withtag("title") else 1,
                self.WIDTH // 2,
                30 + offset
            )
        except:
            pass
        self.root.after(30, self.animate_title)
    
    def handle_click(self, event):
        """Handle mouse clicks on keyboard"""
        if self.game_over or self.animating:
            return
        
        for key, (x1, y1, x2, y2) in self.keyboard_buttons.items():
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                if key == 'ENTER':
                    self.submit_guess()
                elif key == '⌫':
                    self.delete_letter()
                else:
                    self.add_letter(key)
                break
    
    def handle_key(self, event):
        """Handle keyboard input"""
        if self.animating:
            return
            
        if self.game_over:
            if event.keysym == 'Return':
                self.reset_game()
            return
        
        key = event.char.upper()
        
        if event.keysym == 'Return':
            self.submit_guess()
        elif event.keysym == 'BackSpace':
            self.delete_letter()
        elif key.isalpha() and len(key) == 1:
            self.add_letter(key)
    
    def add_letter(self, letter):
        """Add letter to current guess"""
        if len(self.current_guess) < self.WORD_LENGTH and not self.animating:
            self.current_guess += letter
            self.draw_board()
        elif len(self.current_guess) == self.WORD_LENGTH and not self.animating:
            # Replace last letter if at word limit (hidden rule)
            self.current_guess = self.current_guess[:-1] + letter
            self.draw_board()
    
    def delete_letter(self):
        """Delete last letter from current guess"""
        if len(self.current_guess) > 0 and not self.animating:
            self.current_guess = self.current_guess[:-1]
            self.draw_board()
    
    def submit_guess(self):
        """Submit current guess"""
        if self.animating:
            return
            
        if len(self.current_guess) != self.WORD_LENGTH:
            self.shake_row()
            return
        
        if self.current_guess.lower() not in self.WORD_LIST:
            self.shake_row()
            return
        
        # Check guess
        result = self.check_guess(self.current_guess)
        self.guesses.append((self.current_guess, result))
        
        # Update keyboard state
        for i, letter in enumerate(self.current_guess):
            color = result[i]
            if letter not in self.keyboard_state:
                self.keyboard_state[letter] = color
            elif color == 'correct':
                self.keyboard_state[letter] = color
            elif color == 'present' and self.keyboard_state[letter] != 'correct':
                self.keyboard_state[letter] = color
            elif color == 'absent' and self.keyboard_state[letter] not in ['correct', 'present']:
                self.keyboard_state[letter] = color
        
        # Redraw immediately without animation
        self.draw_board()
        self.draw_keyboard()
        
        # Check win/loss
        if self.current_guess == self.target_word:
            self.game_over = True
            self.root.after(300, self.show_win_message)
        elif self.current_row >= self.MAX_GUESSES - 1:
            self.game_over = True
            self.root.after(300, self.show_loss_message)
        else:
            self.current_row += 1
            self.current_guess = ""
    
    def check_guess(self, guess):
        """Check guess against target word"""
        result = ['absent'] * self.WORD_LENGTH
        target_letters = list(self.target_word)
        
        # First pass: mark correct letters
        for i in range(self.WORD_LENGTH):
            if guess[i] == self.target_word[i]:
                result[i] = 'correct'
                target_letters[i] = None
        
        # Second pass: mark present letters
        for i in range(self.WORD_LENGTH):
            if result[i] == 'absent' and guess[i] in target_letters:
                result[i] = 'present'
                target_letters[target_letters.index(guess[i])] = None
        
        return result
    
    def shake_row(self):
        """Animate row shake for invalid guess"""
        offsets = [10, -10, 8, -8, 5, -5, 0]
        
        def shake_step(idx=0):
            if idx < len(offsets):
                self.shake_offset = offsets[idx]
                self.draw_board()
                self.root.after(50, lambda: shake_step(idx + 1))
            else:
                self.shake_offset = 0
                self.draw_board()
        
        shake_step()
    
    def animate_flip_row(self, row, result):
        """Animate entire row flipping"""
        def flip_tiles(col=0):
            if col < self.WORD_LENGTH:
                self.flip_single_tile(row, col, result[col], lambda: flip_tiles(col + 1))
            else:
                # Animation complete
                self.draw_keyboard()
                self.animating = False
                
                # Check win/loss
                if self.current_guess == self.target_word:
                    self.game_over = True
                    self.root.after(500, self.show_win_message)
                elif self.current_row >= self.MAX_GUESSES - 1:
                    self.game_over = True
                    self.root.after(500, self.show_loss_message)
                else:
                    self.current_row += 1
                    self.current_guess = ""
        
        flip_tiles()
    
    def flip_single_tile(self, row, col, color_state, callback):
        """Flip a single tile with smooth animation"""
        letter = self.guesses[row][0][col]
        color = self.get_color_for_state(color_state)
        
        start_x = (self.WIDTH - (self.WORD_LENGTH * self.CELL_SIZE + (self.WORD_LENGTH - 1) * self.CELL_GAP)) // 2
        start_y = 70
        x = start_x + col * (self.CELL_SIZE + self.CELL_GAP)
        y = start_y + row * (self.CELL_SIZE + self.CELL_GAP)
        
        # Create animation in 10 steps
        def animate_step(step=0):
            if step <= 10:
                self.canvas.delete(f"tile_{row}_{col}")
                
                # Calculate scale (shrink then grow)
                if step <= 5:
                    scale = 1 - (step / 5) * 0.95
                    current_color = self.EMPTY_COLOR
                    show_letter = True
                else:
                    scale = 0.05 + ((step - 5) / 5) * 0.95
                    current_color = color
                    show_letter = True
                
                cell_height = self.CELL_SIZE * scale
                y_offset = (self.CELL_SIZE - cell_height) / 2
                
                # Draw tile
                self.canvas.create_rectangle(
                    x + 2, y + y_offset + 2,
                    x + self.CELL_SIZE - 2, y + y_offset + cell_height - 2,
                    fill=current_color,
                    outline=current_color if step > 5 else self.BORDER_COLOR,
                    width=2,
                    tags=f"tile_{row}_{col}"
                )
                
                # Draw letter (hide at middle of flip)
                if show_letter and scale > 0.1:
                    self.canvas.create_text(
                        x + self.CELL_SIZE // 2,
                        y + self.CELL_SIZE // 2,
                        text=letter,
                        font=("Arial", int(32 * scale), "bold"),
                        fill=self.TEXT_COLOR,
                        tags=f"tile_{row}_{col}"
                    )
                
                self.root.after(25, lambda: animate_step(step + 1))
            else:
                # Clean up and redraw board
                self.canvas.delete(f"tile_{row}_{col}")
                self.draw_board()
                callback()
        
        animate_step()
    
    def draw_board(self):
        """Draw the game board"""
        self.canvas.delete("board")
        
        start_x = (self.WIDTH - (self.WORD_LENGTH * self.CELL_SIZE + (self.WORD_LENGTH - 1) * self.CELL_GAP)) // 2
        start_y = 70
        
        for row in range(self.MAX_GUESSES):
            for col in range(self.WORD_LENGTH):
                # Skip if tile is being animated
                if self.canvas.find_withtag(f"tile_{row}_{col}"):
                    continue
                
                x = start_x + col * (self.CELL_SIZE + self.CELL_GAP)
                y = start_y + row * (self.CELL_SIZE + self.CELL_GAP)
                
                # Apply shake offset to current row
                if row == self.current_row:
                    x += self.shake_offset
                
                # Determine cell color and letter
                if row < len(self.guesses):
                    letter = self.guesses[row][0][col]
                    color_state = self.guesses[row][1][col]
                    color = self.get_color_for_state(color_state)
                    border = color
                elif row == self.current_row and col < len(self.current_guess):
                    letter = self.current_guess[col]
                    color = self.EMPTY_COLOR
                    border = self.BORDER_COLOR
                else:
                    letter = ""
                    color = self.EMPTY_COLOR
                    border = self.BORDER_COLOR
                
                # Draw cell
                self.canvas.create_rectangle(
                    x + 2, y + 2,
                    x + self.CELL_SIZE - 2, y + self.CELL_SIZE - 2,
                    fill=color,
                    outline=border,
                    width=2,
                    tags="board"
                )
                
                if letter:
                    self.canvas.create_text(
                        x + self.CELL_SIZE // 2,
                        y + self.CELL_SIZE // 2,
                        text=letter,
                        font=("Arial", 32, "bold"),
                        fill=self.TEXT_COLOR,
                        tags="board"
                    )
    
    def draw_keyboard(self):
        """Draw on-screen keyboard"""
        self.canvas.delete("keyboard")
        self.keyboard_buttons.clear()
        
        start_y = 570
        
        for row_idx, row in enumerate(self.keyboard_rows):
            # Calculate row width for centering
            row_width = 0
            for key in row:
                if key in ['ENTER', '⌫']:
                    row_width += self.KEYBOARD_CELL_WIDTH * 1.5
                else:
                    row_width += self.KEYBOARD_CELL_WIDTH
                row_width += 6  # gap
            row_width -= 6  # remove last gap
            
            start_x = (self.WIDTH - row_width) // 2
            x = start_x
            
            for key in row:
                width = self.KEYBOARD_CELL_WIDTH * 1.5 if key in ['ENTER', '⌫'] else self.KEYBOARD_CELL_WIDTH
                
                # Determine key color
                if key in ['ENTER', '⌫']:
                    color = self.BORDER_COLOR
                elif key in self.keyboard_state:
                    color = self.get_color_for_state(self.keyboard_state[key])
                else:
                    color = self.UNUSED_COLOR  # Darker for unused keys
                
                y = start_y + row_idx * 64
                
                # Store button position for click detection
                self.keyboard_buttons[key] = (x, y, x + width, y + self.KEYBOARD_CELL_HEIGHT)
                
                # Draw key
                self.canvas.create_rectangle(
                    x, y,
                    x + width, y + self.KEYBOARD_CELL_HEIGHT,
                    fill=color,
                    outline="",
                    tags="keyboard"
                )
                
                # Draw key letter
                font_size = 11 if key in ['ENTER', '⌫'] else 15
                self.canvas.create_text(
                    x + width // 2,
                    y + self.KEYBOARD_CELL_HEIGHT // 2,
                    text=key,
                    font=("Arial", font_size, "bold"),
                    fill=self.TEXT_COLOR,
                    tags="keyboard"
                )
                
                x += width + 6
    
    def get_color_for_state(self, state):
        """Get color for tile state"""
        if state == 'correct':
            return self.CORRECT_COLOR
        elif state == 'present':
            return self.PRESENT_COLOR
        elif state == 'absent':
            return self.ABSENT_COLOR
        elif state == 'unused':
            return self.UNUSED_COLOR
        return self.EMPTY_COLOR
    
    def show_win_message(self):
        """Show win message with animation"""
        self.showing_message = True
        self.message_scale = 0
        self.message_bob = 0
        self.animate_message_popup(True)
    
    def show_loss_message(self):
        """Show loss message with animation"""
        self.showing_message = True
        self.message_scale = 0
        self.message_bob = 0
        self.animate_message_popup(False)
    
    def animate_message_popup(self, is_win):
        """Animate message box with scale and bob"""
        def animate_step():
            if self.message_scale < 1.0:
                # Scale up animation
                self.message_scale = min(1.0, self.message_scale + 0.1)
                self.draw_message_box(is_win)
                self.root.after(20, animate_step)
            else:
                # Start bobbing animation
                self.animate_message_bob(is_win)
        animate_step()
    
    def animate_message_bob(self, is_win):
        """Continuous bobbing animation for message"""
        if self.showing_message:
            self.message_bob += 0.08
            self.draw_message_box(is_win)
            self.root.after(30, lambda: self.animate_message_bob(is_win))
    
    def draw_message_box(self, is_win):
        """Draw the message box with current animation state"""
        self.canvas.delete("message")
        
        # Calculate bob offset
        bob_offset = math.sin(self.message_bob) * 5 if self.message_scale >= 1.0 else 0
        
        # Box dimensions
        base_width = 240 if not is_win else 200
        base_height = 90 if not is_win else 70
        width = base_width * self.message_scale
        height = base_height * self.message_scale
        
        center_x = self.WIDTH // 2
        center_y = 280 + bob_offset
        
        # Shadow effect
        shadow_offset = 4
        self.canvas.create_rectangle(
            center_x - width // 2 + shadow_offset,
            center_y - height // 2 + shadow_offset,
            center_x + width // 2 + shadow_offset,
            center_y + height // 2 + shadow_offset,
            fill="#0d0d1a",
            outline="",
            tags="message"
        )
        
        # Main box
        box_color = self.CORRECT_COLOR if is_win else "#ff4757"
        self.canvas.create_rectangle(
            center_x - width // 2,
            center_y - height // 2,
            center_x + width // 2,
            center_y + height // 2,
            fill=self.BG_COLOR,
            outline=box_color,
            width=3,
            tags="message"
        )
        
        if self.message_scale >= 0.5:  # Only show text after half scaled
            # Main message
            main_text = "YOU WIN!" if is_win else "GAME OVER"
            font_size = int(18 * self.message_scale)
            self.canvas.create_text(
                center_x,
                center_y - 20 if not is_win else center_y - 10,
                text=main_text,
                font=("Arial", max(font_size, 1), "bold"),
                fill=box_color,
                tags="message"
            )
            
            if not is_win:
                # Show the answer
                small_font = int(12 * self.message_scale)
                self.canvas.create_text(
                    center_x,
                    center_y + 5,
                    text=f"The word was: {self.target_word}",
                    font=("Arial", max(small_font, 1)),
                    fill=self.TEXT_COLOR,
                    tags="message"
                )
            
            # Instructions
            tiny_font = int(10 * self.message_scale)
            self.canvas.create_text(
                center_x,
                center_y + (30 if not is_win else 15),
                text="Press ENTER to play again",
                font=("Arial", max(tiny_font, 1)),
                fill=self.TEXT_COLOR,
                tags="message"
            )
    
    def reset_game(self):
        """Reset game for new round"""
        self.showing_message = False
        self.canvas.delete("message")
        self.start_game()
        self.draw_board()
        self.draw_keyboard()

if __name__ == "__main__":
    root = tk.Tk()
    game = WordleGame(root)
    root.mainloop()
