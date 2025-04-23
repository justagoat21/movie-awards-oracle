import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
from typing import Callable, Dict, List, Any, Optional

from database import Database
import utils

class OscarsAppGUI:
    """Main GUI class for the Oscars App"""
    
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.current_user = None
        
        # Set up the main window
        self.root.title("Movie Awards Oracle")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Set color scheme
        self.bg_color = "#FFFFFF"
        self.accent_color = "#D4AF37"  # Gold
        self.text_color = "#333333"
        self.button_bg = "#800020"  # Burgundy
        self.button_fg = "#FFFFFF"  # White
        
        self.root.configure(bg=self.bg_color)
        
        # Create styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("Gold.TLabel", background=self.bg_color, foreground=self.accent_color, font=("Arial", 16, "bold"))
        self.style.configure("TLabel", background=self.bg_color, foreground=self.text_color, font=("Arial", 12))
        self.style.configure("TButton", 
                            background=self.button_bg, 
                            foreground=self.button_fg, 
                            font=("Arial", 11, "bold"),
                            borderwidth=1)
        self.style.map("TButton",
                    background=[('active', self.accent_color)],
                    foreground=[('active', self.text_color)])
        
        # Create main frames
        self.create_header_frame()
        self.create_main_frame()
        self.create_status_bar()
        
        # Initialize database connection
        self.check_database_connection()
        
    def create_header_frame(self):
        """Create the header frame with title and user info"""
        self.header_frame = ttk.Frame(self.root)
        self.header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # App title
        self.title_label = ttk.Label(
            self.header_frame, 
            text="🏆 Movie Awards Oracle", 
            style="Gold.TLabel", 
            font=("Arial", 24, "bold")
        )
        self.title_label.pack(side=tk.LEFT, pady=10)
        
        # User info/login
        self.user_frame = ttk.Frame(self.header_frame)
        self.user_frame.pack(side=tk.RIGHT, pady=10)
        
        self.login_button = tk.Button(
            self.user_frame,
            text="Login/Register",
            bg=self.button_bg,
            fg=self.button_fg,
            font=("Arial", 10),
            command=self.show_login_dialog
        )
        self.login_button.pack(side=tk.RIGHT)
        
        self.user_label = ttk.Label(self.user_frame, text="Not logged in")
        self.user_label.pack(side=tk.RIGHT, padx=10)
        
    def create_main_frame(self):
        """Create the main content frame with feature buttons and results area"""
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left side - Feature buttons
        self.buttons_frame = ttk.Frame(self.main_frame, width=300)
        self.buttons_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), pady=10)
        
        # Buttons frame title
        ttk.Label(self.buttons_frame, text="Features", style="Gold.TLabel").pack(anchor=tk.W, pady=(0, 10))
        
        # Create feature buttons
        self.create_feature_buttons()
        
        # Right side - Results area
        self.results_frame = ttk.Frame(self.main_frame)
        self.results_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, pady=10)
        
        # Results area title
        ttk.Label(self.results_frame, text="Results", style="Gold.TLabel").pack(anchor=tk.W, pady=(0, 10))
        
        # Results display (Treeview)
        self.results_tree = ttk.Treeview(self.results_frame, show="headings")
        self.results_tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars for the treeview
        treescroll_y = ttk.Scrollbar(self.results_tree, orient=tk.VERTICAL, command=self.results_tree.yview)
        treescroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_tree.configure(yscrollcommand=treescroll_y.set)
        
        treescroll_x = ttk.Scrollbar(self.results_tree, orient=tk.HORIZONTAL, command=self.results_tree.xview)
        treescroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.results_tree.configure(xscrollcommand=treescroll_x.set)
        
        # Results text for more detailed output
        self.results_text = tk.Text(self.results_frame, height=10, width=50, wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Text area scrollbar
        text_scroll = ttk.Scrollbar(self.results_text, orient=tk.VERTICAL, command=self.results_text.yview)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.configure(yscrollcommand=text_scroll.set)
        
    def create_feature_buttons(self):
        """Create buttons for each feature"""
        features = [
            ("✅ Register a user", self.register_user),
            ("🎬 Add Nomination", self.add_nomination),
            ("📜 View My Nominations", self.view_user_nominations),
            ("🏆 Top Nominated Movies", self.view_top_nominated_movies),
            ("🎭 Staff Stats", self.view_staff_stats),
            ("🌍 Top Actor Birth Countries", self.view_top_actor_countries),
            ("🗺️ Staff by Country", self.view_staff_by_country),
            ("🎥 Dream Team", self.view_dream_team),
            ("🏢 Top Production Companies", self.view_top_production_companies),
            ("🌐 Non-English Oscar Winners", self.view_non_english_winners),
            ("👥 Staff List", self.view_staff_list)  # New feature button
        ]
        
        for text, command in features:
            btn = tk.Button(
                self.buttons_frame,
                text=text,
                bg=self.button_bg,
                fg=self.button_fg,
                font=("Arial", 11),
                width=25,
                height=2,
                command=command,
                relief=tk.RAISED,
                cursor="hand2"
            )
            btn.pack(fill=tk.X, pady=5)
            
            # Add hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.accent_color, fg=self.text_color))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.button_bg, fg=self.button_fg))
    
    def create_status_bar(self):
        """Create status bar at the bottom of the window"""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = ttk.Label(self.status_bar, text="Ready", anchor=tk.W)
        self.status_label.pack(fill=tk.X, padx=10, pady=5)
        
    def update_status(self, message):
        """Update the status bar message"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def clear_results(self):
        """Clear the results area"""
        # Clear the treeview
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Reset the columns
        for col in self.results_tree["columns"]:
            self.results_tree.heading(col, text="")
        
        self.results_tree["columns"] = ()
        
        # Clear the text area
        self.results_text.delete(1.0, tk.END)
    
    def display_results_in_tree(self, data, columns):
        """Display results in the treeview"""
        self.clear_results()
        
        if not data:
            self.results_text.insert(tk.END, "No results found.")
            return
        
        # Configure columns
        self.results_tree["columns"] = columns
        for col in columns:
            self.results_tree.heading(col, text=col.capitalize())
            self.results_tree.column(col, width=100, anchor=tk.CENTER)
        
        # Insert data
        for i, item in enumerate(data):
            values = [item.get(col, "") for col in columns]
            self.results_tree.insert("", tk.END, iid=i, values=values)
    
    def display_text_results(self, text):
        """Display results in the text area"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, text)
    
    def check_database_connection(self):
        """Check and establish database connection"""
        self.update_status("Connecting to database...")
        
        def connection_thread():
            success = self.db.connect()
            if success:
                self.update_status("Connected to database.")
            else:
                self.update_status("Database connection failed!")
                messagebox.showerror("Connection Error", 
                                    "Failed to connect to the database. Check your internet connection and try again.")
        
        # Run connection in a separate thread to avoid freezing the UI
        threading.Thread(target=connection_thread).start()
    
    def show_login_dialog(self):
        """Show login/register dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Login/Register")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Username:").pack(pady=(10, 5))
        username_entry = ttk.Entry(dialog, width=30)
        username_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Password:").pack(pady=5)
        password_entry = ttk.Entry(dialog, width=30, show="*")
        password_entry.pack(pady=5)
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        def on_register():
            username = username_entry.get()
            password = password_entry.get()
            
            if not username or not password:
                messagebox.showerror("Error", "Please enter both username and password")
                return
            
            # For now, just close the dialog
            messagebox.showinfo("Registration", "Registration feature will be implemented in the next phase")
            dialog.destroy()
        
        def on_login():
            username = username_entry.get()
            password = password_entry.get()
            
            if not username or not password:
                messagebox.showerror("Error", "Please enter both username and password")
                return
            
            # For now, simulate login
            self.current_user = {"id": 1, "username": username}
            self.user_label.config(text=f"Logged in as: {username}")
            dialog.destroy()
        
        ttk.Button(btn_frame, text="Login", command=on_login).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Register", command=on_register).pack(side=tk.LEFT, padx=5)
        
    # Feature button callback functions
    def register_user(self):
        """Register a new user"""
        if self.current_user:
            messagebox.showinfo("Already Logged In", "You are already logged in. Log out to register a new user.")
            return
            
        dialog = tk.Toplevel(self.root)
        dialog.title("Register User")
        dialog.geometry("350x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Username:").pack(pady=(10, 5))
        username_entry = ttk.Entry(dialog, width=30)
        username_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Email:").pack(pady=5)
        email_entry = ttk.Entry(dialog, width=30)
        email_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Password:").pack(pady=5)
        password_entry = ttk.Entry(dialog, width=30, show="*")
        password_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Confirm Password:").pack(pady=5)
        confirm_entry = ttk.Entry(dialog, width=30, show="*")
        confirm_entry.pack(pady=5)
        
        def on_submit():
            username = username_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            confirm = confirm_entry.get()
            
            if not username or not email or not password or not confirm:
                messagebox.showerror("Error", "All fields are required")
                return
                
            if password != confirm:
                messagebox.showerror("Error", "Passwords do not match")
                return
                
            if not utils.validate_email(email):
                messagebox.showerror("Error", "Invalid email format")
                return
                
            if not utils.validate_password_strength(password):
                messagebox.showerror("Error", "Password must be at least 8 characters with 1 uppercase, 1 lowercase, and 1 number")
                return
            
            # Register the user
            success = self.db.register_user(username, password, email)
            
            if success:
                messagebox.showinfo("Success", "User registered successfully. You can now log in.")
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to register user. Please try again.")
        
        ttk.Button(dialog, text="Register", command=on_submit).pack(pady=10)
    
    def add_nomination(self):
        """Add a new user nomination for a staff member for a movie"""
        if not self.current_user:
            messagebox.showinfo("Login Required", "Please login to add a nomination")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Nomination")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Staff Name:").pack(pady=(10, 5))
        staff_entry = ttk.Entry(dialog, width=30)
        staff_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Movie Title:").pack(pady=5)
        movie_entry = ttk.Entry(dialog, width=30)
        movie_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Award Category:").pack(pady=5)
        categories = [
            "Best Picture", "Best Director", "Best Actor", 
            "Best Actress", "Best Supporting Actor", "Best Supporting Actress",
            "Best Original Screenplay", "Best Adapted Screenplay", 
            "Best Cinematography", "Best Original Score"
        ]
        category_var = tk.StringVar(dialog)
        category_var.set(categories[0])
        category_menu = ttk.Combobox(dialog, textvariable=category_var, values=categories, width=30)
        category_menu.pack(pady=5)
        
        def on_submit():
            staff = staff_entry.get()
            movie = movie_entry.get()
            category = category_var.get()
            
            if not staff or not movie or not category:
                messagebox.showerror("Error", "All fields are required")
                return
            
            # In actual implementation, we would search for staff_id and movie_id
            # For now, just show a success message
            messagebox.showinfo("Success", f"Nomination recorded: {staff} for {movie} in category {category}")
            self.update_status(f"Nomination added: {staff} for {movie}")
            dialog.destroy()
        
        ttk.Button(dialog, text="Submit Nomination", command=on_submit).pack(pady=10)
    
    def view_user_nominations(self):
        """View existing nominations for the user"""
        if not self.current_user:
            messagebox.showinfo("Login Required", "Please login to view your nominations")
            return
        
        self.update_status("Fetching your nominations...")
        
        def fetch_thread():
            nominations = self.db.get_user_nominations(self.current_user.get('id', 0))
            
            # Update UI in the main thread
            self.root.after(0, lambda: self.display_user_nominations(nominations))
        
        threading.Thread(target=fetch_thread).start()
    
    def display_user_nominations(self, nominations):
        """Display user nominations in the results area"""
        if not nominations:
            self.clear_results()
            self.display_text_results("You haven't made any nominations yet.")
            self.update_status("No nominations found.")
            return
        
        columns = ["id", "staff_name", "movie_title", "category"]
        self.display_results_in_tree(nominations, columns)
        self.update_status(f"Found {len(nominations)} nomination(s).")
    
    def view_top_nominated_movies(self):
        """View top nominated movies by system users"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Top Nominated Movies")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Filter by Category (optional):").pack(pady=(10, 5))
        categories = ["", "Best Picture", "Best Director", "Best Actor", "Best Actress"]
        category_var = tk.StringVar(dialog)
        category_menu = ttk.Combobox(dialog, textvariable=category_var, values=categories, width=25)
        category_menu.pack(pady=5)
        
        ttk.Label(dialog, text="Filter by Year (optional):").pack(pady=5)
        year_entry = ttk.Entry(dialog, width=25)
        year_entry.pack(pady=5)
        
        def on_search():
            category = category_var.get() or None
            year_text = year_entry.get()
            year = int(year_text) if year_text.isdigit() else None
            
            self.update_status("Searching for top nominated movies...")
            dialog.destroy()
            
            def fetch_thread():
                movies = self.db.get_top_nominated_movies(category, year)
                
                # Update UI in the main thread
                self.root.after(0, lambda: self.display_top_movies(movies, category, year))
            
            threading.Thread(target=fetch_thread).start()
        
        ttk.Button(dialog, text="Search", command=on_search).pack(pady=10)
    
    def display_top_movies(self, movies, category=None, year=None):
        """Display top nominated movies in the results area"""
        if not movies:
            self.clear_results()
            self.display_text_results("No movies found matching your criteria.")
            self.update_status("No movies found.")
            return
        
        columns = ["title", "nomination_count"]
        self.display_results_in_tree(movies, columns)
        
        filter_text = ""
        if category:
            filter_text += f" in category '{category}'"
        if year:
            filter_text += f" from year {year}"
        
        self.update_status(f"Found {len(movies)} top nominated movies{filter_text}.")
    
    def view_staff_stats(self):
        """Show total nominations and Oscars for a given staff member"""
        staff_name = simpledialog.askstring("Staff Stats", "Enter staff member name:")
        if not staff_name:
            return
        
        self.update_status(f"Searching for stats on {staff_name}...")
        
        # In a real implementation, we would search for staff_id by name
        # For demonstration, use a dummy staff_id
        staff_id = 1
        
        def fetch_thread():
            stats = self.db.get_staff_stats(staff_id)
            
            # Update UI in the main thread
            self.root.after(0, lambda: self.display_staff_stats(stats, staff_name))
        
        threading.Thread(target=fetch_thread).start()
    
    def display_staff_stats(self, stats, staff_name):
        """Display staff statistics in the results area"""
        self.clear_results()
        
        if not stats:
            self.display_text_results(f"No information found for '{staff_name}'.")
            self.update_status(f"No information found for '{staff_name}'.")
            return
        
        formatted_stats = utils.format_staff_stats(stats)
        self.display_text_results(formatted_stats)
        self.update_status(f"Displaying statistics for {staff_name}")
    
    def view_top_actor_countries(self):
        """Show top 5 birth countries for actors who won Best Actor"""
        self.update_status("Fetching top actor birth countries...")
        
        def fetch_thread():
            countries = self.db.get_top_actor_birth_countries()
            
            # Update UI in the main thread
            self.root.after(0, lambda: self.display_top_countries(countries))
        
        threading.Thread(target=fetch_thread).start()
    
    def display_top_countries(self, countries):
        """Display top actor birth countries in the results area"""
        if not countries:
            self.clear_results()
            self.display_text_results("No data available for actor birth countries.")
            self.update_status("No data available.")
            return
        
        columns = ["birth_country", "winner_count"]
        self.display_results_in_tree(countries, columns)
        self.update_status("Displaying top actor birth countries.")
    
    def view_staff_by_country(self):
        """Show all nominated staff from a given country"""
        country = simpledialog.askstring("Staff by Country", "Enter country name:")
        if not country:
            return
        
        self.update_status(f"Searching for staff from {country}...")
        
        def fetch_thread():
            staff_list = self.db.get_staff_by_country(country)
            
            # Update UI in the main thread
            self.root.after(0, lambda: self.display_staff_by_country(staff_list, country))
        
        threading.Thread(target=fetch_thread).start()
    
    def display_staff_by_country(self, staff_list, country):
        """Display staff by country in the results area"""
        if not staff_list:
            self.clear_results()
            self.display_text_results(f"No nominated staff found from {country}.")
            self.update_status(f"No staff found from {country}.")
            return
        
        columns = ["name", "categories", "nomination_count", "oscar_count"]
        self.display_results_in_tree(staff_list, columns)
        self.update_status(f"Found {len(staff_list)} staff members from {country}.")
    
    def view_dream_team(self):
        """Show Best living cast (director, actors, producer, singer)"""
        self.update_status("Calculating dream team...")
        
        def fetch_thread():
            dream_team = self.db.get_dream_team()
            
            # Update UI in the main thread
            self.root.after(0, lambda: self.display_dream_team(dream_team))
        
        threading.Thread(target=fetch_thread).start()
    
    def display_dream_team(self, dream_team):
        """Display dream team in the results area"""
        self.clear_results()
        
        if not dream_team:
            self.display_text_results("Could not determine dream team.")
            self.update_status("Dream team calculation failed.")
            return
        
        formatted_team = utils.format_dream_team(dream_team)
        
        result_text = "🌟 THE DREAM TEAM 🌟\n\n"
        for role, person in formatted_team.items():
            result_text += f"🎬 {role.capitalize()}: {person}\n"
        
        self.display_text_results(result_text)
        self.update_status("Dream team calculated successfully.")
    
    def view_top_production_companies(self):
        """Show top 5 production companies by Oscars won"""
        self.update_status("Fetching top production companies...")
        
        def fetch_thread():
            companies = self.db.get_top_production_companies()
            
            # Update UI in the main thread
            self.root.after(0, lambda: self.display_top_companies(companies))
        
        threading.Thread(target=fetch_thread).start()
    
    def display_top_companies(self, companies):
        """Display top production companies in the results area"""
        if not companies:
            self.clear_results()
            self.display_text_results("No data available for production companies.")
            self.update_status("No data available.")
            return
        
        columns = ["name", "oscar_count"]
        self.display_results_in_tree(companies, columns)
        self.update_status("Displaying top production companies by Oscar wins.")
    
    def view_non_english_winners(self):
        """List all non-English speaking Oscar-winning movies"""
        self.update_status("Fetching non-English Oscar winners...")
        
        def fetch_thread():
            movies = self.db.get_non_english_oscar_winners()
            
            # Update UI in the main thread
            self.root.after(0, lambda: self.display_non_english_winners(movies))
        
        threading.Thread(target=fetch_thread).start()
    
    def display_non_english_winners(self, movies):
        """Display non-English Oscar winners in the results area"""
        if not movies:
            self.clear_results()
            self.display_text_results("No non-English Oscar winners found.")
            self.update_status("No non-English winners found.")
            return
        
        columns = ["title", "language", "year", "category"]
        self.display_results_in_tree(movies, columns)
        self.update_status(f"Found {len(movies)} non-English Oscar-winning movies.")
    
    def view_staff_list(self):
        """View list of staff members"""
        self.update_status("Fetching staff list...")
        
        def fetch_thread():
            staff_list = self.db.get_staff_list()
            
            # Update UI in the main thread
            self.root.after(0, lambda: self.display_staff_list(staff_list))
        
        threading.Thread(target=fetch_thread).start()
    
    def display_staff_list(self, staff_list):
        """Display staff list in the results area"""
        if not staff_list:
            self.clear_results()
            self.display_text_results("No staff members found.")
            self.update_status("No staff found.")
            return
        
        columns = list(staff_list[0].keys())
        self.display_results_in_tree(staff_list, columns)
        self.update_status(f"Found {len(staff_list)} staff members.")
