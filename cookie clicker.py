import tkinter as tk
from tkinter import ttk
import math
import webbrowser

class CookieClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("cookie clicker")
        self.root.resizable(False, False)
        
        # Game constants
        self.WIDTH = 500
        self.HEIGHT = 500
        
        # Colors (matching snake game)
        self.BG_COLOR = "#1a1a2e"
        self.ACCENT_COLOR = "#00ff41"
        self.SECONDARY_COLOR = "#00cc33"
        self.BUTTON_COLOR = "#16213e"
        self.TEXT_COLOR = "#ffffff"
        self.COOKIE_BASE = "#d4a574"
        self.COOKIE_DARK = "#b8935f"
        self.COOKIE_LIGHT = "#e6c89f"
        
        # Main frame
        main_frame = tk.Frame(root, bg=self.BG_COLOR)
        main_frame.pack(padx=10, pady=10)
        
        # Canvas setup
        self.canvas = tk.Canvas(
            main_frame,
            width=self.WIDTH,
            height=280,
            bg=self.BG_COLOR,
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Game state
        self.cookies = 0
        self.cookies_per_click = 1
        self.cookies_per_second = 0
        self.total_cookies = 0
        
        # Upgrades
        self.upgrades = {
            'cursor': {'cost': 15, 'cps': 0.1, 'cpc': 0, 'count': 0, 'name': 'Cursor', 'desc': '+0.1 cookies/sec'},
            'reinforced_cursor': {'cost': 100, 'cps': 0, 'cpc': 1, 'count': 0, 'name': 'Reinforced Cursor', 'desc': '+1 cookies/click'},
            'grandma': {'cost': 100, 'cps': 1, 'cpc': 0, 'count': 0, 'name': 'Grandma', 'desc': '+1 cookie/sec'},
            'farm': {'cost': 500, 'cps': 8, 'cpc': 0, 'count': 0, 'name': 'Farm', 'desc': '+8 cookies/sec'},
            'steel_clicker': {'cost': 500, 'cps': 0, 'cpc': 5, 'count': 0, 'name': 'Steel Clicker', 'desc': '+5 cookies/click'},
            'mine': {'cost': 3000, 'cps': 47, 'cpc': 0, 'count': 0, 'name': 'Mine', 'desc': '+47 cookies/sec'},
            'diamond_fingers': {'cost': 5000, 'cps': 0, 'cpc': 25, 'count': 0, 'name': 'Diamond Fingers', 'desc': '+25 cookies/click'},
            'factory': {'cost': 10000, 'cps': 260, 'cpc': 0, 'count': 0, 'name': 'Factory', 'desc': '+260 cookies/sec'},
            'bank': {'cost': 40000, 'cps': 1400, 'cpc': 0, 'count': 0, 'name': 'Bank', 'desc': '+1400 cookies/sec'},
            'titan_hand': {'cost': 50000, 'cps': 0, 'cpc': 100, 'count': 0, 'name': 'Titan Hand', 'desc': '+100 cookies/click'}
        }
        
        # Animation state
        self.cookie_scale = 1.0
        self.cookie_rotation = 0
        self.pulse_direction = 1
        self.click_particles = []
        self.cursor_rotation = 0
        
        # Tooltip
        self.tooltip = None
        
        # Cookie stats display
        self.stats_label = tk.Label(
            main_frame,
            text="COOKIES: 0",
            font=("Arial", 16, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.BG_COLOR
        )
        self.stats_label.pack()
        
        self.cpc_label = tk.Label(
            main_frame,
            text="per click: 1",
            font=("Arial", 10),
            fg="#888888",
            bg=self.BG_COLOR
        )
        self.cpc_label.pack()
        
        self.cps_label = tk.Label(
            main_frame,
            text="per second: 0.0",
            font=("Arial", 10),
            fg="#888888",
            bg=self.BG_COLOR
        )
        self.cps_label.pack()
        
        # Shop frame with scrollbar
        shop_frame = tk.Frame(main_frame, bg=self.BG_COLOR)
        shop_frame.pack(pady=(5, 0))
        
        # Shop title
        shop_title = tk.Label(
            shop_frame,
            text="SHOP",
            font=("Arial", 14, "bold"),
            fg=self.TEXT_COLOR,
            bg=self.BG_COLOR
        )
        shop_title.pack()
        
        # Create canvas for scrollable area
        self.shop_canvas = tk.Canvas(
            shop_frame,
            width=480,
            height=150,
            bg=self.BG_COLOR,
            highlightthickness=0
        )
        self.shop_canvas.pack(side=tk.LEFT)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(
            shop_frame,
            orient=tk.VERTICAL,
            command=self.shop_canvas.yview,
            bg=self.BUTTON_COLOR,
            troughcolor=self.BG_COLOR,
            activebackground=self.ACCENT_COLOR
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.shop_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create frame inside canvas
        self.shop_inner_frame = tk.Frame(self.shop_canvas, bg=self.BG_COLOR)
        self.shop_canvas_window = self.shop_canvas.create_window(
            (0, 0),
            window=self.shop_inner_frame,
            anchor='nw'
        )
        
        # Watermark (clickable)
        self.watermark_label = tk.Label(
            main_frame,
            text="spidrbot.com",
            font=("Arial", 9),
            fg="#888888",
            bg=self.BG_COLOR,
            cursor="hand2"
        )
        self.watermark_label.pack(pady=(5, 5))
        self.watermark_label.bind("<Button-1>", self.open_website)
        
        # Key bindings
        self.root.bind('<Escape>', lambda e: self.root.iconify())
        self.root.bind('<space>', lambda e: self.root.destroy())
        
        # Cookie button area (circle)
        self.cookie_center_x = self.WIDTH // 2
        self.cookie_center_y = 140
        self.cookie_radius = 60
        
        # Bind click to cookie area
        self.canvas.bind("<Button-1>", self.handle_click)
        
        # Bind mousewheel to shop scrolling
        self.shop_canvas.bind("<Enter>", self._bind_mousewheel)
        self.shop_canvas.bind("<Leave>", self._unbind_mousewheel)
        
        # Draw UI
        self.draw_ui()
        self.create_shop_buttons()
        self.animate()
        self.passive_income()
    
    def _bind_mousewheel(self, event):
        """Bind mousewheel to scrolling"""
        self.shop_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.shop_canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.shop_canvas.bind_all("<Button-5>", self._on_mousewheel)
    
    def _unbind_mousewheel(self, event):
        """Unbind mousewheel"""
        self.shop_canvas.unbind_all("<MouseWheel>")
        self.shop_canvas.unbind_all("<Button-4>")
        self.shop_canvas.unbind_all("<Button-5>")
    
    def _on_mousewheel(self, event):
        """Handle mousewheel scrolling"""
        if event.num == 5 or event.delta < 0:
            self.shop_canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.shop_canvas.yview_scroll(-1, "units")
    
    def open_website(self, event):
        """Open spidrbot.com in browser"""
        webbrowser.open("https://spidrbot.com")
    
    def draw_ui(self):
        """Draw the game interface"""
        # Title
        self.canvas.create_text(
            self.WIDTH // 2,
            30,
            text="COOKIE CLICKER",
            font=("Arial", 24, "bold"),
            fill=self.ACCENT_COLOR,
            tags="static"
        )
    
    def show_tooltip(self, event, text):
        """Show tooltip on hover"""
        if self.tooltip:
            self.tooltip.destroy()
        
        self.tooltip = tk.Toplevel(self.root)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        
        label = tk.Label(
            self.tooltip,
            text=text,
            font=("Arial", 9),
            bg="#2a2a3e",
            fg=self.TEXT_COLOR,
            relief="solid",
            borderwidth=1,
            padx=8,
            pady=4
        )
        label.pack()
    
    def hide_tooltip(self, event):
        """Hide tooltip"""
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
    
    def create_shop_buttons(self):
        """Create upgrade buttons in scrollable frame, sorted by cost"""
        self.upgrade_buttons = []
        button_height = 30
        button_spacing = 5
        
        # Sort upgrades by cost
        upgrade_keys = sorted(self.upgrades.keys(), key=lambda k: self.upgrades[k]['cost'])
        
        for i, key in enumerate(upgrade_keys):
            upgrade = self.upgrades[key]
            
            # Create frame for each button
            btn_frame = tk.Frame(
                self.shop_inner_frame,
                bg=self.BUTTON_COLOR,
                highlightbackground=self.ACCENT_COLOR,
                highlightthickness=2,
                height=button_height,
                width=460
            )
            btn_frame.pack(pady=button_spacing, padx=10)
            btn_frame.pack_propagate(False)
            
            # Name and count label
            name_label = tk.Label(
                btn_frame,
                text=f"{upgrade['name']} (0)",
                font=("Arial", 9, "bold"),
                fg=self.TEXT_COLOR,
                bg=self.BUTTON_COLOR,
                anchor="w"
            )
            name_label.pack(side=tk.LEFT, padx=10)
            
            # Cost label
            cost_label = tk.Label(
                btn_frame,
                text=f"{upgrade['cost']} 🍪",
                font=("Arial", 9),
                fg=self.COOKIE_BASE,
                bg=self.BUTTON_COLOR,
                anchor="e"
            )
            cost_label.pack(side=tk.RIGHT, padx=10)
            
            # Bind click event
            btn_frame.bind("<Button-1>", lambda e, k=key: self.buy_upgrade(k))
            name_label.bind("<Button-1>", lambda e, k=key: self.buy_upgrade(k))
            cost_label.bind("<Button-1>", lambda e, k=key: self.buy_upgrade(k))
            
            # Bind hover events for tooltip
            tooltip_text = upgrade['desc']
            btn_frame.bind("<Enter>", lambda e, t=tooltip_text, f=btn_frame: [
                f.config(cursor="hand2"),
                self.show_tooltip(e, t)
            ])
            btn_frame.bind("<Leave>", lambda e, f=btn_frame: [
                f.config(cursor=""),
                self.hide_tooltip(e)
            ])
            name_label.bind("<Enter>", lambda e, t=tooltip_text: self.show_tooltip(e, t))
            name_label.bind("<Leave>", self.hide_tooltip)
            cost_label.bind("<Enter>", lambda e, t=tooltip_text: self.show_tooltip(e, t))
            cost_label.bind("<Leave>", self.hide_tooltip)
            
            self.upgrade_buttons.append({
                'key': key,
                'frame': btn_frame,
                'name_label': name_label,
                'cost_label': cost_label
            })
        
        # Update scroll region
        self.shop_inner_frame.update_idletasks()
        self.shop_canvas.config(scrollregion=self.shop_canvas.bbox("all"))
    
    def draw_cookie(self):
        """Draw the clickable cookie with realistic appearance"""
        self.canvas.delete("cookie")
        self.canvas.delete("cursors")
        
        # Apply scale
        radius = self.cookie_radius * self.cookie_scale
        
        # Cookie base circle
        self.canvas.create_oval(
            self.cookie_center_x - radius,
            self.cookie_center_y - radius,
            self.cookie_center_x + radius,
            self.cookie_center_y + radius,
            fill=self.COOKIE_BASE,
            outline=self.COOKIE_DARK,
            width=3,
            tags="cookie"
        )
        
        # Add cookie texture (bumpy edges)
        num_bumps = 12
        for i in range(num_bumps):
            angle = (i / num_bumps) * 2 * math.pi
            bump_x = self.cookie_center_x + math.cos(angle) * radius * 0.85
            bump_y = self.cookie_center_y + math.sin(angle) * radius * 0.85
            bump_size = radius * 0.12
            
            self.canvas.create_oval(
                bump_x - bump_size,
                bump_y - bump_size,
                bump_x + bump_size,
                bump_y + bump_size,
                fill=self.COOKIE_LIGHT,
                outline="",
                tags="cookie"
            )
        
        # Chocolate chips with varied sizes
        chip_positions = [
            (-0.4, -0.3, 0.13), (0.35, -0.25, 0.15), (-0.25, 0.35, 0.12),
            (0.4, 0.3, 0.14), (0.1, -0.45, 0.11), (-0.35, 0.1, 0.13),
            (0.15, 0.15, 0.12), (-0.15, -0.15, 0.14), (0.05, 0.4, 0.11),
            (-0.5, -0.1, 0.12), (0.2, -0.1, 0.13)
        ]
        
        for dx, dy, size_mult in chip_positions:
            chip_x = self.cookie_center_x + dx * radius
            chip_y = self.cookie_center_y + dy * radius
            chip_size = radius * size_mult
            
            # Dark chocolate chip
            self.canvas.create_oval(
                chip_x - chip_size,
                chip_y - chip_size,
                chip_x + chip_size,
                chip_y + chip_size,
                fill="#3d2817",
                outline="#2a1a0f",
                width=1,
                tags="cookie"
            )
            
            # Highlight on chip
            highlight_offset = chip_size * 0.3
            self.canvas.create_oval(
                chip_x - highlight_offset,
                chip_y - highlight_offset,
                chip_x - highlight_offset + chip_size * 0.4,
                chip_y - highlight_offset + chip_size * 0.4,
                fill="#5c3d2e",
                outline="",
                tags="cookie"
            )
        
        # Cookie highlight/shine
        shine_radius = radius * 0.3
        self.canvas.create_oval(
            self.cookie_center_x - radius * 0.35 - shine_radius,
            self.cookie_center_y - radius * 0.35 - shine_radius,
            self.cookie_center_x - radius * 0.35 + shine_radius,
            self.cookie_center_y - radius * 0.35 + shine_radius,
            fill=self.COOKIE_LIGHT,
            outline="",
            tags="cookie"
        )
        
        # Draw cursors orbiting the cookie
        cursor_count = self.upgrades['cursor']['count']
        if cursor_count > 0:
            # Limit visible cursors to 10 for visual clarity
            visible_cursors = min(cursor_count, 10)
            cursor_orbit_radius = radius + 30
            
            for i in range(visible_cursors):
                angle = self.cursor_rotation + (i / visible_cursors) * 2 * math.pi
                cursor_x = self.cookie_center_x + math.cos(angle) * cursor_orbit_radius
                cursor_y = self.cookie_center_y + math.sin(angle) * cursor_orbit_radius
                
                # Draw cursor pointer
                # Cursor body (pointing toward cookie)
                cursor_angle = angle + math.pi  # Point toward center
                cursor_size = 15
                
                # Calculate cursor triangle points
                tip_x = cursor_x + math.cos(cursor_angle) * cursor_size
                tip_y = cursor_y + math.sin(cursor_angle) * cursor_size
                
                left_x = cursor_x + math.cos(cursor_angle + 2.5) * cursor_size * 0.6
                left_y = cursor_y + math.sin(cursor_angle + 2.5) * cursor_size * 0.6
                
                right_x = cursor_x + math.cos(cursor_angle - 2.5) * cursor_size * 0.6
                right_y = cursor_y + math.sin(cursor_angle - 2.5) * cursor_size * 0.6
                
                # Draw cursor shape
                self.canvas.create_polygon(
                    tip_x, tip_y,
                    left_x, left_y,
                    right_x, right_y,
                    fill=self.ACCENT_COLOR,
                    outline=self.SECONDARY_COLOR,
                    width=2,
                    tags="cursors"
                )
        
        # Draw click particles
        self.canvas.delete("particle")
        for particle in self.click_particles[:]:
            particle['life'] -= 1
            particle['y'] -= 2
            particle['size'] -= 0.2
            
            if particle['life'] <= 0 or particle['size'] <= 0:
                self.click_particles.remove(particle)
            else:
                alpha = particle['life'] / 20
                self.canvas.create_text(
                    particle['x'],
                    particle['y'],
                    text=f"+{particle['value']}",
                    font=("Arial", int(10 + particle['size']), "bold"),
                    fill=self.ACCENT_COLOR,
                    tags="particle"
                )
    
    def handle_click(self, event):
        """Handle mouse clicks"""
        x, y = event.x, event.y
        
        # Check if clicked on cookie
        distance = math.sqrt((x - self.cookie_center_x)**2 + (y - self.cookie_center_y)**2)
        if distance <= self.cookie_radius * self.cookie_scale:
            self.click_cookie(x, y)
    
    def click_cookie(self, x, y):
        """Handle cookie click"""
        self.cookies += self.cookies_per_click
        self.total_cookies += self.cookies_per_click
        
        # Cookie click animation
        self.cookie_scale = 1.15
        
        # Add particle effect
        self.click_particles.append({
            'x': x,
            'y': y,
            'life': 20,
            'size': 5,
            'value': self.cookies_per_click
        })
        
        self.update_display()
    
    def buy_upgrade(self, upgrade_key):
        """Purchase an upgrade"""
        upgrade = self.upgrades[upgrade_key]
        
        if self.cookies >= upgrade['cost']:
            self.cookies -= upgrade['cost']
            upgrade['count'] += 1
            self.cookies_per_second += upgrade['cps']
            self.cookies_per_click += upgrade['cpc']
            
            # Increase cost (1.15x multiplier)
            upgrade['cost'] = int(upgrade['cost'] * 1.15)
            
            self.update_display()
            self.update_shop()
    
    def update_display(self):
        """Update cookie count display"""
        self.stats_label.config(text=f"COOKIES: {int(self.cookies)}")
        self.cpc_label.config(text=f"per click: {self.cookies_per_click}")
        self.cps_label.config(text=f"per second: {self.cookies_per_second:.1f}")
    
    def update_shop(self):
        """Update shop button displays"""
        for btn in self.upgrade_buttons:
            key = btn['key']
            upgrade = self.upgrades[key]
            
            # Update count
            btn['name_label'].config(text=f"{upgrade['name']} ({upgrade['count']})")
            
            # Update cost
            btn['cost_label'].config(text=f"{upgrade['cost']} 🍪")
            
            # Update button color based on affordability
            if self.cookies >= upgrade['cost']:
                btn['frame'].config(highlightbackground=self.ACCENT_COLOR, highlightthickness=2)
            else:
                btn['frame'].config(highlightbackground="#888888", highlightthickness=1)
    
    def animate(self):
        """Main animation loop"""
        # Idle cookie pulse
        self.cookie_scale += self.pulse_direction * 0.002
        if self.cookie_scale > 1.05:
            self.pulse_direction = -1
        elif self.cookie_scale < 0.95:
            self.pulse_direction = 1
        
        # Return to normal size after click
        if self.cookie_scale > 1.05:
            self.cookie_scale *= 0.95
        
        # Rotate cursors
        self.cursor_rotation += 0.02
        if self.cursor_rotation >= 2 * math.pi:
            self.cursor_rotation = 0
        
        self.draw_cookie()
        self.update_shop()
        
        self.root.after(30, self.animate)
    
    def passive_income(self):
        """Add cookies from passive income"""
        if self.cookies_per_second > 0:
            income = self.cookies_per_second / 10  # Called every 100ms
            self.cookies += income
            self.total_cookies += income
            self.update_display()
        
        self.root.after(100, self.passive_income)

if __name__ == "__main__":
    root = tk.Tk()
    game = CookieClicker(root)
    root.mainloop()
