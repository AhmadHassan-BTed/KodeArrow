import tkinter as tk
from tkinter import ttk
import time
import pandas as pd
from keyboard import on_press_key, unhook_all
from tkinter import messagebox
from keyboard import on_press_key, unhook_all, is_pressed

# Initialize data collection variables
data = {
    'wpm': 0,
    'accuracy': 0,
    'completion_time': 0,
    'error_rate': 0,
    'finger_movement_distance': 0,
    'home_row_retention': 0,
    'correction_time': 0,
    'total_typing_time': 0,
    'navigational_key_usage': 0,
    'backspace_usage': 0,
    'pageup_pagedown_usage': 0,
    'delete_usage': 0,
    'cognitive_load': 0
}

# Key distances for different platforms
laptop_key_distances = {
    'backspace': 10,  # Shorter distance on laptop
    'delete': 11.5,     # Closer keys on laptop
    'page up': 16,    # More compact layout
    'page down': 16.5,  
    'home': 15.5,       
    'end': 17,        
    'left': 8.5,       # Closer arrow keys
    'right': 11,      
    'up': 9,         
    'down': 10,       
    'alt+i': 0.0,  # Up key
    'alt+k': 0.0,  # Down key
    'alt+l': 0.0,  # Right key
    'alt+j': 0.0,  # Left key
    'alt+;': 0.0,  # Backspace key
    'alt+p': 0.0,  # Delete key
    'alt+u': 0.0,  # Home key
    'alt+o': 0.0,  # Endline key
    'alt+\'': 0.0,  # PageUp key
    'alt+[': 0.0,  # PageDown key
}

computer_key_distances = {
    'backspace': 10.0,  # Original distances for desktop keyboard in cm
    'delete': 13.0,     
    'page up': 17.0,    
    'page down': 16.5,  
    'home': 15,       
    'end': 14.5,        
    'left': 13.0,       
    'right': 17.0,      
    'up': 16,         
    'down': 15,        
    'alt+i': 0.0,  # Up key
    'alt+k': 0.0,  # Down key
    'alt+l': 0.0,  # Right key
    'alt+j': 0.0,  # Left key
    'alt+;': 0.0,  # Backspace key
    'alt+p': 0.0,  # Delete key
    'alt+u': 0.0,  # Home key
    'alt+o': 0.0,  # Endline key
    'alt+\'': 0.0,  # PageUp key
    'alt+[': 0.0,  # PageDown key
}

# Current key distances (will be set based on platform selection)
key_distances = {}

# Track key usage statistics
start_time = None
end_time = None
correction_time = 0
finger_movement_distance = 0
total_typing_time = 0
backspace_usage = 0
navigation_key_usage = 0
pageup_pagedown_usage = 0
delete_usage = 0
home_key_usage = 0
test_active = False
platform_selected = False

expected_text = "The quick brown fox jumps over the lazy dog! Typing efficiently demands minimizing errors & maximizing speed. Every keystroke-letters, numbers (123, 0.75, 10^3), or symbols (@, #, $, %, &, , +, =, ^, ~, (, ), {, }, [, ], <, >, /, , |)-affects performance, says @AhmadHassan. Notice your spacebar, punctuation (., ,, ;, :, ?, !), and navigation keys: arrows, delete, backspace. Efficient typing, per #TypingPro, blends speed & accuracy. Keep fingers near the home row, avoiding reaches for keys like shift+@ or ~0.2% errors. Shortcuts (Ctrl+C, Alt+Tab) save time if used wisely! Pauses to fix errors, like \"teh\" to \"the,\" disrupt flow, don't they? Navigation keys -- home, end, page up/down -- can slow you down if overused. Practice steady pacing in text or code (e.g., x=2.718y; if(a<0) {return -1;}). Take breaks to avoid fatigue, as prolonged typing strains hands. For #1 goal: Build muscle memory to minimize distant key reliance (only ~3-5 cm from home row!). Consistent practice reduces errors, like mistyping 10^2 or {}. Reflect on habits: Are you overusing arrows? Efficient typing minimizes movement & maximizes precision. Use tools like keyloggers to track performance. Strive for a seamless workflow, balancing speed, accuracy, & minimal reaches. Test your skills with varied inputs, like z=3.14*(x+y), to master all keys. Success lies in fluid, error-free typing!"

def get_screen_info(window):
    """Get comprehensive screen information for adaptive layout"""
    try:
        # Get screen dimensions
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # Get DPI scaling factor
        dpi = window.winfo_fpixels('1i')  # Dots per inch
        scale_factor = dpi / 96.0  # 96 is standard DPI
        
        # Calculate effective screen size considering DPI scaling
        effective_width = screen_width / scale_factor
        effective_height = screen_height / scale_factor
        
        return {
            'screen_width': screen_width,
            'screen_height': screen_height,
            'effective_width': effective_width,
            'effective_height': effective_height,
            'dpi': dpi,
            'scale_factor': scale_factor
        }
    except:
        # Fallback values
        return {
            'screen_width': 1920,
            'screen_height': 1080,
            'effective_width': 1920,
            'effective_height': 1080,
            'dpi': 96,
            'scale_factor': 1.0
        }

def calculate_adaptive_sizes(screen_info):
    """Calculate optimal sizes based on screen information"""
    width = screen_info['effective_width']
    height = screen_info['effective_height']
    scale = screen_info['scale_factor']
    
    # Determine screen category
    if width >= 2560:  # 4K+ screens
        category = "ultra_wide"
    elif width >= 1920:  # Full HD+ screens
        category = "large"
    elif width >= 1366:  # Standard laptop screens
        category = "medium"
    elif width >= 1024:  # Small laptop screens
        category = "small"
    else:  # Very small screens/tablets
        category = "tiny"
    
    # Adaptive sizing based on screen category
    size_configs = {
        "ultra_wide": {
            "window_width_ratio": 0.7,
            "window_height_ratio": 0.8,
            "min_width": 1400,
            "min_height": 900,
            "font_base": 12,
            "text_width_left": 45,
            "text_width_right": 70,
            "text_height": 30,
            "column_weight_left": 2,
            "column_weight_right": 3
        },
        "large": {
            "window_width_ratio": 0.75,
            "window_height_ratio": 0.8,
            "min_width": 1200,
            "min_height": 800,
            "font_base": 11,
            "text_width_left": 40,
            "text_width_right": 60,
            "text_height": 25,
            "column_weight_left": 2,
            "column_weight_right": 3
        },
        "medium": {
            "window_width_ratio": 0.85,
            "window_height_ratio": 0.85,
            "min_width": 1000,
            "min_height": 700,
            "font_base": 10,
            "text_width_left": 35,
            "text_width_right": 50,
            "text_height": 22,
            "column_weight_left": 1,
            "column_weight_right": 2
        },
        "small": {
            "window_width_ratio": 0.9,
            "window_height_ratio": 0.9,
            "min_width": 900,
            "min_height": 600,
            "font_base": 9,
            "text_width_left": 30,
            "text_width_right": 45,
            "text_height": 20,
            "column_weight_left": 1,
            "column_weight_right": 2
        },
        "tiny": {
            "window_width_ratio": 0.95,
            "window_height_ratio": 0.95,
            "min_width": 800,
            "min_height": 550,
            "font_base": 8,
            "text_width_left": 25,
            "text_width_right": 40,
            "text_height": 18,
            "column_weight_left": 1,
            "column_weight_right": 1
        }
    }
    
    config = size_configs[category]
    
    # Calculate actual window size
    window_width = max(int(width * config["window_width_ratio"]), config["min_width"])
    window_height = max(int(height * config["window_height_ratio"]), config["min_height"])
    
    # Ensure window fits on screen
    window_width = min(window_width, int(width * 0.95))
    window_height = min(window_height, int(height * 0.9))
    
    # Apply DPI scaling to font sizes
    font_base = max(8, int(config["font_base"] * min(scale, 1.5)))
    
    return {
        "category": category,
        "window_width": window_width,
        "window_height": window_height,
        "font_base": font_base,
        "font_title": font_base + 2,
        "font_button": font_base,
        "text_width_left": config["text_width_left"],
        "text_width_right": config["text_width_right"],
        "text_height": config["text_height"],
        "column_weight_left": config["column_weight_left"],
        "column_weight_right": config["column_weight_right"],
        "padding": max(5, int(10 * scale))
    }

def create_styled_messagebox(title, message, box_type="info"):
    """Create a custom styled message box"""
    dialog = tk.Toplevel()
    dialog.title(title)
    dialog.configure(bg='white')
    dialog.resizable(False, False)
    
    # Calculate size based on message length
    lines = message.count('\n') + 1
    width = min(max(len(max(message.split('\n'), key=len)) * 8, 400), 800)
    height = min(max(lines * 20 + 150, 200), 600)
    dialog.geometry(f"{width}x{height}")
    
    # Center the dialog
    dialog.transient()
    dialog.grab_set()
    
    # Main frame with padding
    main_frame = tk.Frame(dialog, bg='white', padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Title label
    title_label = tk.Label(main_frame, text=title, 
                          font=('Helvetica', 16, 'bold'), 
                          fg='#00207f', bg='white')
    title_label.pack(pady=(0, 15))
    
    # Create scrollable text area for long messages
    text_frame = tk.Frame(main_frame, bg='white')
    text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
    
    # Text widget with scrollbar
    text_widget = tk.Text(text_frame, wrap=tk.WORD, font=('Helvetica', 11),
                         fg='#333333', bg='#f8f9fa', relief=tk.FLAT,
                         padx=15, pady=15, height=10, cursor='arrow')
    
    scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)
    
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Insert message and make it read-only
    text_widget.insert('1.0', message)
    text_widget.configure(state='disabled')
    
    # Disable text selection and cursor
    text_widget.bind("<Button-1>", lambda e: "break")
    text_widget.bind("<Key>", lambda e: "break")
    
    # Button frame
    button_frame = tk.Frame(main_frame, bg='white')
    button_frame.pack(pady=(0, 10))
    
    # OK button with custom styling
    ok_button = tk.Button(button_frame, text="OK", 
                         font=('Helvetica', 12, 'bold'),
                         fg='white', bg='#00207f',
                         activeforeground='white', 
                         activebackground='#001a66',
                         relief=tk.FLAT, padx=30, pady=8,
                         cursor='hand2',
                         command=dialog.destroy)
    ok_button.pack()
    
    # Hover effects
    def on_enter(e):
        ok_button.configure(bg='#001a66')
    def on_leave(e):
        ok_button.configure(bg='#00207f')
    
    ok_button.bind("<Enter>", on_enter)
    ok_button.bind("<Leave>", on_leave)
    
    # Focus on OK button and bind Enter key
    ok_button.focus_set()
    dialog.bind('<Return>', lambda e: dialog.destroy())
    dialog.bind('<Escape>', lambda e: dialog.destroy())
    
    dialog.wait_window()

def create_styled_warning(title, message):
    """Create a custom styled warning dialog"""
    dialog = tk.Toplevel()
    dialog.title(title)
    dialog.configure(bg='white')
    dialog.geometry("450x200")
    dialog.resizable(False, False)
    
    # Center the dialog
    dialog.transient()
    dialog.grab_set()
    
    # Main frame
    main_frame = tk.Frame(dialog, bg='white', padx=30, pady=25)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Warning icon and title
    title_frame = tk.Frame(main_frame, bg='white')
    title_frame.pack(pady=(0, 20))
    
    # Warning symbol
    warning_label = tk.Label(title_frame, text="⚠️", font=('Helvetica', 24), bg='white')
    warning_label.pack(side=tk.LEFT, padx=(0, 10))
    
    title_label = tk.Label(title_frame, text=title, 
                          font=('Helvetica', 16, 'bold'), 
                          fg='#00207f', bg='white')
    title_label.pack(side=tk.LEFT)
    
    # Message
    message_label = tk.Label(main_frame, text=message, 
                           font=('Helvetica', 12), 
                           fg='#444444', bg='white',
                           justify=tk.CENTER, wraplength=380)
    message_label.pack(pady=(0, 25))
    
    # OK button
    ok_button = tk.Button(main_frame, text="OK", 
                         font=('Helvetica', 12, 'bold'),
                         fg='white', bg='#00207f',
                         activeforeground='white', 
                         activebackground='#001a66',
                         relief=tk.FLAT, padx=30, pady=8,
                         cursor='hand2',
                         command=dialog.destroy)
    ok_button.pack()
    
    # Hover effects
    def on_enter(e):
        ok_button.configure(bg='#001a66')
    def on_leave(e):
        ok_button.configure(bg='#00207f')
    
    ok_button.bind("<Enter>", on_enter)
    ok_button.bind("<Leave>", on_leave)
    
    ok_button.focus_set()
    dialog.bind('<Return>', lambda e: dialog.destroy())
    dialog.bind('<Escape>', lambda e: dialog.destroy())
    
    dialog.wait_window()

def on_platform_select(event):
    global key_distances, platform_selected
    selected_platform = platform_combo.get()
    
    if selected_platform == "Laptop":
        key_distances = laptop_key_distances.copy()
    elif selected_platform == "Computer":
        key_distances = computer_key_distances.copy()
    
    platform_selected = True
    start_button.config(text="Start Test", state=tk.NORMAL)

def disable_mouse_click(event):
    """Disable mouse clicks in text field"""
    return "break"

def track_custom_key_combinations(event):
    global finger_movement_distance, backspace_usage, delete_usage, navigation_key_usage, pageup_pagedown_usage, home_key_usage
    
    if is_pressed('alt') and event.name in ['i', 'k', 'l', 'j', ';', 'p', 'u', 'o', "'", '[']:
        custom_key = f"alt+{event.name}"
        
        if custom_key in key_distances:
            finger_movement_distance += key_distances[custom_key]
            
            if custom_key == 'alt+;':  # Consider this backspace
                backspace_usage += 1
            elif custom_key == 'alt+p':  # Consider this delete
                delete_usage += 1
            elif custom_key in ['alt+i', 'alt+k', 'alt+l', 'alt+j']:  # Navigational keys
                navigation_key_usage += 1
            elif custom_key in ['alt+\'', 'alt+[']:  # PageUp/PageDown
                pageup_pagedown_usage += 1
            elif custom_key in ['alt+u', 'alt+o']:  # Home/End
                home_key_usage += 1

def update_text_highlighting():
    """Update the highlighting of the expected text based on user input"""
    if not test_active:
        return
        
    typed_text = text_field.get("1.0", tk.END).rstrip('\n')
    
    # Clear existing tags
    expected_text_widget.tag_delete("correct", "incorrect", "untyped")
    
    # Get current font from the widget
    current_font = expected_text_widget.cget('font')
    if isinstance(current_font, tuple):
        font_family = current_font[0]
        font_size = current_font[1]
    else:
        font_family = 'Helvetica'
        font_size = 12
    
    # Configure tags for different states with current font
    expected_text_widget.tag_configure("correct", foreground="green", 
                                     font=(font_family, font_size, 'bold'))
    expected_text_widget.tag_configure("incorrect", foreground="red", 
                                     font=(font_family, font_size, 'bold'))
    expected_text_widget.tag_configure("untyped", foreground="black", 
                                     font=(font_family, font_size))
    
    # Apply highlighting based on comparison
    for i, char in enumerate(expected_text):
        if i < len(typed_text):
            if typed_text[i] == char:
                # Correct character
                expected_text_widget.tag_add("correct", f"1.{i}", f"1.{i+1}")
            else:
                # Incorrect character
                expected_text_widget.tag_add("incorrect", f"1.{i}", f"1.{i+1}")
        else:
            # Untyped character
            expected_text_widget.tag_add("untyped", f"1.{i}", f"1.{i+1}")

def on_text_change(event):
    """Called whenever text in the input field changes"""
    if test_active:
        update_text_highlighting()

def start_test():
    global start_time, test_active
    
    if not platform_selected:
        create_styled_warning("Platform Not Selected", "Please select a platform first!")
        return
    
    start_time = time.time()
    test_active = True

    # Enable the text input field
    text_field.config(state=tk.NORMAL)
    text_field.focus_set()
    
    # Clear any existing text
    text_field.delete("1.0", tk.END)
    
    # Bind text change events
    text_field.bind('<KeyRelease>', on_text_change)
    text_field.bind('<Button-1>', lambda e: "break")  # Disable mouse clicks
    
    # Initial highlighting update
    update_text_highlighting()
    
    # Disable platform selection during test
    platform_combo.config(state='disabled')

    # Hook key press events for both standard keys and custom Alt+key combinations
    on_press_key('backspace', track_backspace)
    on_press_key('left', track_navigation_key)
    on_press_key('right', track_navigation_key)
    on_press_key('up', track_navigation_key)
    on_press_key('down', track_navigation_key)
    on_press_key('page up', track_pageup)
    on_press_key('page down', track_pagedown)
    on_press_key('delete', track_delete)
    on_press_key('home', track_home_key)
    on_press_key('end', track_home_key)
    
    # Hook custom Alt+key combinations
    for key in ['i', 'k', 'l', 'j', ';', 'p', 'u', 'o', "'", '[']:
        on_press_key(key, track_custom_key_combinations)

    # Hide start button and show restart option
    start_button.configure(text="Restart Test", command=restart_test)

def restart_test():
    """Restart the test by resetting all variables and UI state"""
    global start_time, test_active, backspace_usage, navigation_key_usage, delete_usage
    global pageup_pagedown_usage, home_key_usage, finger_movement_distance, correction_time
    
    # Reset all tracking variables
    start_time = None
    test_active = False
    backspace_usage = 0
    navigation_key_usage = 0
    delete_usage = 0
    pageup_pagedown_usage = 0
    home_key_usage = 0
    finger_movement_distance = 0
    correction_time = 0
    
    # Reset data dictionary
    for key in data:
        data[key] = 0
    
    # Clear text field and disable it
    text_field.delete("1.0", tk.END)
    text_field.config(state=tk.DISABLED)
    
    # Re-enable platform selection
    platform_combo.config(state='readonly')
    
    # Reset text highlighting
    expected_text_widget.tag_delete("correct", "incorrect", "untyped")
    
    # Unhook all key tracking
    unhook_all()
    
    # Reset button text
    start_button.configure(text="Start Test", command=start_test)

def track_backspace(event):
    global backspace_usage, finger_movement_distance
    if test_active:
        backspace_usage += 1
        finger_movement_distance += key_distances['backspace']

def track_delete(event):
    global delete_usage, finger_movement_distance
    if test_active:
        delete_usage += 1
        finger_movement_distance += key_distances['delete'] 

def track_navigation_key(event):
    global navigation_key_usage, finger_movement_distance
    if test_active:
        navigation_key_usage += 1
        finger_movement_distance += key_distances[event.name]

def track_pageup(event):
    global pageup_pagedown_usage, finger_movement_distance
    if test_active:
        pageup_pagedown_usage += 1
        finger_movement_distance += key_distances['page up']

def track_pagedown(event):
    global pageup_pagedown_usage, finger_movement_distance
    if test_active:
        pageup_pagedown_usage += 1
        finger_movement_distance += key_distances['page down']

def track_home_key(event):
    global home_key_usage, finger_movement_distance
    if test_active:
        home_key_usage += 1
        finger_movement_distance += key_distances[event.name]

def end_test():
    global end_time, test_active
    if test_active is True:
        end_time = time.time()
    test_active = False  # Stop the test
    
    # Disable the text input field
    text_field.config(state=tk.DISABLED)
    
    # Unbind text change events
    text_field.unbind('<KeyRelease>')
    
    # Re-enable platform selection
    platform_combo.config(state='readonly')
    
    # Reset text highlighting
    expected_text_widget.tag_delete("correct", "incorrect", "untyped")
    
    # Reset start button
    start_button.configure(text="Start Test", command=start_test)
    
    unhook_all()  # Unhook all key tracking when the test ends
    calculate_results()
    show_guessing_dialog()  # Show guessing dialog instead of direct results

def calculate_results():
    global total_typing_time
    
    # Ensure we have valid end_time
    if end_time is None or start_time is None:
        return
        
    total_time = end_time - start_time
    total_typing_time = total_time - correction_time

    # Calculate WPM (Words per minute)
    words_typed = len(text_field.get("1.0", tk.END).split())
    wpm = (words_typed / total_typing_time) * 60 if total_typing_time > 0 else 0

    # Accuracy calculation
    typed_text = text_field.get("1.0", tk.END).strip()
    correct_characters = sum(1 for a, b in zip(expected_text, typed_text) if a == b)
    accuracy = (correct_characters / len(expected_text)) * 100 if len(expected_text) > 0 else 0

    # Error rate
    total_errors = len(expected_text) - correct_characters
    error_rate = total_errors / len(expected_text) if len(expected_text) > 0 else 0

    # Home row retention percentage (more usage of navigational keys leads to lower retention)
    total_navigation_usage = navigation_key_usage + backspace_usage + delete_usage + pageup_pagedown_usage + home_key_usage
    home_row_retention_percentage = 100 - (total_navigation_usage / (total_navigation_usage + words_typed)) * 100 if words_typed > 0 else 0

    # Add results to the data dictionary
    data.update({
        'wpm': wpm,
        'accuracy': accuracy,
        'completion_time': total_time,
        'error_rate': error_rate,
        'finger_movement_distance': finger_movement_distance,
        'home_row_retention': home_row_retention_percentage,
        'correction_time': correction_time,
        'total_typing_time': total_typing_time,
        'navigational_key_usage': navigation_key_usage,
        'backspace_usage': backspace_usage,
        'pageup_pagedown_usage': pageup_pagedown_usage,
        'delete_usage': delete_usage
    })

def show_guessing_dialog():
    """Show a styled dialog asking user to guess their key usage statistics"""
    dialog = tk.Toplevel()
    dialog.title("Guess Your Statistics!")
    dialog.configure(bg='white')
    dialog.geometry("500x550")
    dialog.resizable(False, False)
    dialog.grab_set()
    
    # Center the dialog
    dialog.transient()
    
    # Main frame with padding
    main_frame = tk.Frame(dialog, bg='white', padx=30, pady=25)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Header section
    header_frame = tk.Frame(main_frame, bg='white')
    header_frame.pack(fill=tk.X, pady=(0, 20))
    
    # Emoji and title
    emoji_label = tk.Label(header_frame, text="🤔", font=('Helvetica', 28), bg='white')
    emoji_label.pack()
    
    title_label = tk.Label(header_frame, text="Before seeing your results...", 
                          font=('Helvetica', 18, 'bold'), 
                          fg='#00207f', bg='white')
    title_label.pack(pady=(5, 0))
    
    subtitle_label = tk.Label(header_frame, text="Can you guess how many times you pressed:", 
                             font=('Helvetica', 12), 
                             fg='#444444', bg='white')
    subtitle_label.pack(pady=(5, 0))
    
    # Dictionary to store user guesses
    guesses = {}
    
    # Create entry fields for each statistic
    stats_to_guess = [
        ("Backspace", "backspace_usage"),
        ("Arrow Keys", "navigational_key_usage"),
        ("Delete Key", "delete_usage"),
        ("PageUp/PageDown", "pageup_pagedown_usage"),
        ("Home/End Keys", "home_key_usage")
    ]
    
    entries = {}
    
    # Stats container
    stats_frame = tk.Frame(main_frame, bg='white')
    stats_frame.pack(fill=tk.X, pady=(10, 20))
    
    for i, (stat_name, stat_key) in enumerate(stats_to_guess):
        # Create a styled frame for each stat
        stat_frame = tk.Frame(stats_frame, bg='#f8f9fa', relief=tk.FLAT, bd=1)
        stat_frame.pack(fill=tk.X, pady=3, padx=5)
        
        inner_frame = tk.Frame(stat_frame, bg='#f8f9fa')
        inner_frame.pack(fill=tk.X, padx=15, pady=12)
        
        # Label
        label = tk.Label(inner_frame, text=f"{stat_name}:", 
                        font=('Helvetica', 11, 'bold'),
                        fg='#00207f', bg='#f8f9fa',
                        width=18, anchor='w')
        label.pack(side=tk.LEFT)
        
        # Entry with custom styling
        entry_frame = tk.Frame(inner_frame, bg='#f8f9fa')
        entry_frame.pack(side=tk.RIGHT)
        
        entry = tk.Entry(entry_frame, width=8, justify='center',
                        font=('Helvetica', 11, 'bold'),
                        fg='#00207f', bg='white',
                        relief=tk.FLAT, bd=1,
                        highlightthickness=2,
                        highlightcolor='#00207f',
                        highlightbackground='#cccccc')
        entry.pack(padx=5)
        
        entries[stat_key] = entry
        entry.insert(0, "0")
    
    def submit_guesses():
        try:
            for stat_key, entry in entries.items():
                guesses[stat_key] = int(entry.get()) if entry.get().isdigit() else 0
        except:
            for stat_key in entries.keys():
                guesses[stat_key] = 0
        
        dialog.destroy()
        show_results_with_guesses(guesses)
    
    # Button section
    button_frame = tk.Frame(main_frame, bg='white')
    button_frame.pack(pady=(10, 0))
    
    submit_button = tk.Button(button_frame, text="Submit Guesses", 
                             command=submit_guesses,
                             font=('Helvetica', 14, 'bold'),
                             fg='white', bg='#00207f',
                             activeforeground='white', 
                             activebackground='#001a66',
                             relief=tk.FLAT, 
                             padx=40, pady=12,
                             cursor='hand2')
    submit_button.pack()
    
    # Hover effects for submit button
    def on_enter(e):
        submit_button.configure(bg='#001a66')
    def on_leave(e):
        submit_button.configure(bg='#00207f')
    
    submit_button.bind("<Enter>", on_enter)
    submit_button.bind("<Leave>", on_leave)
    
    # Instructions
    instruction_frame = tk.Frame(main_frame, bg='white')
    instruction_frame.pack(pady=(15, 0))
    
    instruction1 = tk.Label(instruction_frame, text="Enter your best guess for each category", 
                           font=('Helvetica', 10, 'italic'), 
                           fg='#666666', bg='white')
    instruction1.pack()
    
    instruction2 = tk.Label(instruction_frame, text="(This helps you understand your typing awareness)", 
                           font=('Helvetica', 10, 'italic'), 
                           fg='#00207f', bg='white')
    instruction2.pack(pady=(2, 0))
    
    # Focus and key bindings
    list(entries.values())[0].focus_set()
    dialog.bind('<Return>', lambda e: submit_guesses())
    dialog.bind('<Escape>', lambda e: dialog.destroy())

def show_results_with_guesses(guesses):
    """Show results comparing guesses with actual values, with reward at the bottom"""
    # Calculate accuracy of guesses
    actual_values = {
        'backspace_usage': backspace_usage,
        'navigational_key_usage': navigation_key_usage,
        'delete_usage': delete_usage,
        'pageup_pagedown_usage': pageup_pagedown_usage,
        'home_key_usage': home_key_usage
    }

    

    result_message = (
        f"Platform: {platform_combo.get()}\n"
        f"WPM: {data['wpm']:.2f}\n"
        f"Accuracy: {data['accuracy']:.2f}%\n"
        f"Completion Time: {data['completion_time']:.2f}s\n"
        f"Error Rate: {data['error_rate']:.2f}\n"
        f"Finger Movement Distance: {data['finger_movement_distance']:.2f}\n"
        f"Home Row Retention: {data['home_row_retention']:.2f}%\n"
        f"Navigational Key Usage: {data['navigational_key_usage']}\n"
        f"Backspace Usage: {data['backspace_usage']}\n"
        f"Delete Usage: {data['delete_usage']}\n"
        f"PageUp/PageDown Usage: {data['pageup_pagedown_usage']}\n"
        f"Home/End Key Usage: {home_key_usage}\n\n\n"
    )
    

    result_message += "=== YOUR GUESSES vs ACTUAL ===\n"
    
    stat_names = {
        'backspace_usage': 'Backspace',
        'navigational_key_usage': 'Arrow Keys',
        'delete_usage': 'Delete Key',
        'pageup_pagedown_usage': 'PgUp/PgDn',
        'home_key_usage': 'Home/End Keys'
    }
    
    total_accuracy = 0
    guess_count = 0
    
    for stat_key, actual_value in actual_values.items():
        guessed_value = guesses.get(stat_key, 0)
        difference = abs(actual_value - guessed_value)
        accuracy_percent = max(0, 100 - (difference * 10)) if actual_value > 0 else (100 if guessed_value == 0 else 0)
        
        result_message += f"{stat_names[stat_key]}: Guessed {guessed_value} | Actual {actual_value}"
        
        if difference == 0:
            result_message += " ✓ Perfect!\n"
        elif difference <= 2:
            result_message += " ✓ Very close!\n"
        elif difference <= 5:
            result_message += " ~ Close\n"
        else:
            result_message += " ✗ Off by quite a bit\n"
        
        total_accuracy += accuracy_percent
        guess_count += 1
    
    overall_guess_accuracy = total_accuracy / guess_count if guess_count > 0 else 0
    result_message += f"\nOverall Guess Accuracy: {overall_guess_accuracy:.1f}%\n\n"
    
    create_styled_messagebox("🏆 Test Results & Your Guesses", result_message)

def main():
    global text_field, start_button, platform_combo, expected_text_widget
    
    # Create window first to get screen info
    window = tk.Tk()
    window.title("Typing Test - Adaptive Layout")
    
    # Withdraw window temporarily to calculate proper size
    window.withdraw()
    window.update_idletasks()  # Ensure window is ready for measurements
    
    # Get screen information and calculate adaptive sizes
    screen_info = get_screen_info(window)
    sizes = calculate_adaptive_sizes(screen_info)
    
    print(f"Screen Category: {sizes['category']}")
    print(f"Window Size: {sizes['window_width']}x{sizes['window_height']}")
    print(f"Base Font Size: {sizes['font_base']}")
    
    # Configure window with calculated sizes
    window.geometry(f"{sizes['window_width']}x{sizes['window_height']}")
    window.minsize(sizes['window_width'] // 2, sizes['window_height'] // 2)
    
    # Center window on screen
    x = (screen_info['screen_width'] - sizes['window_width']) // 2
    y = (screen_info['screen_height'] - sizes['window_height']) // 2
    window.geometry(f"{sizes['window_width']}x{sizes['window_height']}+{x}+{y}")
    
    # Show window
    window.deiconify()
    
    # Configure window grid
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    # Main container
    main_frame = tk.Frame(window, bg='#f5f5f5')
    main_frame.pack(fill=tk.BOTH, expand=True, padx=sizes['padding'], pady=sizes['padding'])
    
    # Configure main frame grid with adaptive weights
    main_frame.columnconfigure(0, weight=sizes['column_weight_left'])
    main_frame.columnconfigure(1, weight=sizes['column_weight_right'])
    main_frame.rowconfigure(2, weight=1)  # Text areas get all the space

    # ===================
    # TOP SECTION: Platform Selection (Row 0)
    # ===================
    platform_frame = tk.LabelFrame(main_frame, text="Setup", font=('Helvetica', sizes['font_title'], 'bold'),
                                   bg='white', fg='#00207f', padx=sizes['padding'], pady=sizes['padding'])
    platform_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, sizes['padding']))

    # Platform selection
    platform_container = tk.Frame(platform_frame, bg='white')
    platform_container.pack(fill=tk.X)
    
    platform_label = tk.Label(platform_container, text="Select Platform:", 
                             font=('Helvetica', sizes['font_base'], 'bold'),
                             bg='white', fg='#333')
    platform_label.pack(side=tk.LEFT, padx=(0, 10))

    platform_combo = ttk.Combobox(platform_container, values=["Laptop", "Computer"], 
                                 state="readonly", font=('Helvetica', sizes['font_base']),
                                 width=15)
    platform_combo.pack(side=tk.LEFT, padx=5)
    platform_combo.bind('<<ComboboxSelected>>', on_platform_select)

    # ===================
    # MIDDLE SECTION: Control Buttons (Row 1)
    # ===================
    control_frame = tk.LabelFrame(main_frame, text="Controls", font=('Helvetica', sizes['font_title'], 'bold'),
                                 bg='white', fg='#00207f', padx=sizes['padding'], pady=sizes['padding'])
    control_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, sizes['padding']))

    button_container = tk.Frame(control_frame, bg='white')
    button_container.pack(fill=tk.X)
    
    # Create styled buttons
    button_style = {
        'font': ('Helvetica', sizes['font_button'], 'bold'),
        'relief': tk.FLAT,
        'padx': sizes['padding'] * 2,
        'pady': sizes['padding'],
        'cursor': 'hand2'
    }
    
    start_button = tk.Button(button_container, text="Select platform first", 
                           command=start_test, state=tk.DISABLED,
                           bg='#cccccc', fg='#666666', **button_style)
    start_button.pack(side=tk.LEFT, padx=(0, 10))
    
    end_button = tk.Button(button_container, text="End Test", command=end_test,
                          bg='#dc3545', fg='white', 
                          activebackground='#c82333', activeforeground='white',
                          **button_style)
    end_button.pack(side=tk.LEFT, padx=5)
    
    # Add hover effects for buttons
    def create_hover_effect(button, normal_bg, hover_bg):
        def on_enter(e):
            if button['state'] != 'disabled':
                button.configure(bg=hover_bg)
        def on_leave(e):
            if button['state'] != 'disabled':
                button.configure(bg=normal_bg)
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    create_hover_effect(end_button, '#dc3545', '#c82333')

    # ===================
    # BOTTOM SECTION: Text Areas (Row 2)
    # ===================
    
    # Left side: Typing area
    left_frame = tk.LabelFrame(main_frame, text="Your Typing", font=('Helvetica', sizes['font_title'], 'bold'),
                              bg='white', fg='#00207f', padx=sizes['padding'], pady=sizes['padding'])
    left_frame.grid(row=2, column=0, sticky="nsew", padx=(0, sizes['padding']//2))
    left_frame.columnconfigure(0, weight=1)
    left_frame.rowconfigure(0, weight=1)

    # Typing input field with scrollbar
    text_frame_left = tk.Frame(left_frame, bg='white')
    text_frame_left.pack(fill=tk.BOTH, expand=True)
    text_frame_left.columnconfigure(0, weight=1)
    text_frame_left.rowconfigure(0, weight=1)
    
    text_field = tk.Text(text_frame_left, 
                        font=('Helvetica', sizes['font_base']),
                        width=sizes['text_width_left'], 
                        height=sizes['text_height'],
                        wrap=tk.WORD, 
                        bg='#f8f9fa', 
                        fg='#333333',
                        insertbackground='#00207f',
                        selectbackground='#00207f',
                        selectforeground='white',
                        padx=10, pady=10,
                        relief=tk.FLAT, bd=1)
    text_field.grid(row=0, column=0, sticky="nsew")
    text_field.config(state=tk.DISABLED)
    
    # Scrollbar for typing field
    scrollbar_left = ttk.Scrollbar(text_frame_left, orient=tk.VERTICAL, command=text_field.yview)
    scrollbar_left.grid(row=0, column=1, sticky="ns")
    text_field.configure(yscrollcommand=scrollbar_left.set)
    
    # Disable mouse interactions
    for event in ["<Button-1>", "<Button-2>", "<Button-3>", "<Double-Button-1>", "<Triple-Button-1>"]:
        text_field.bind(event, disable_mouse_click)

    # Right side: Text to type
    right_frame = tk.LabelFrame(main_frame, text="Text to Type", font=('Helvetica', sizes['font_title'], 'bold'),
                               bg='white', fg='#00207f', padx=sizes['padding'], pady=sizes['padding'])
    right_frame.grid(row=2, column=1, sticky="nsew", padx=(sizes['padding']//2, 0))
    right_frame.columnconfigure(0, weight=1)
    right_frame.rowconfigure(0, weight=1)

    # Expected text display with scrollbar
    text_frame_right = tk.Frame(right_frame, bg='white')
    text_frame_right.pack(fill=tk.BOTH, expand=True)
    text_frame_right.columnconfigure(0, weight=1)
    text_frame_right.rowconfigure(0, weight=1)
    
    expected_text_widget = tk.Text(text_frame_right, 
                                  wrap=tk.WORD, 
                                  font=('Helvetica', sizes['font_base']),
                                  width=sizes['text_width_right'],
                                  height=sizes['text_height'],
                                  state=tk.DISABLED,
                                  cursor="arrow", 
                                  bg='#ffffff',
                                  fg='#333333',
                                  padx=10, pady=10,
                                  relief=tk.FLAT, bd=1)
    expected_text_widget.grid(row=0, column=0, sticky="nsew")
    
    # Scrollbar for expected text
    scrollbar_right = ttk.Scrollbar(text_frame_right, orient=tk.VERTICAL, command=expected_text_widget.yview)
    scrollbar_right.grid(row=0, column=1, sticky="ns")
    expected_text_widget.configure(yscrollcommand=scrollbar_right.set)
    
    # Insert expected text
    expected_text_widget.config(state=tk.NORMAL)
    expected_text_widget.insert("1.0", expected_text)
    expected_text_widget.config(state=tk.DISABLED)
    
    # Disable interactions with expected text
    for event in ["<Button-1>", "<Button-2>", "<Button-3>", "<Key>"]:
        expected_text_widget.bind(event, lambda e: "break")

    # ===================
    # ADAPTIVE RESIZE HANDLING
    # ===================
    
    last_resize_time = 0
    resize_timer = None
    
    def delayed_resize():
        """Handle resize with debouncing to prevent flickering"""
        nonlocal last_resize_time
        current_time = time.time()
        
        if current_time - last_resize_time > 0.3:  # Only resize after 300ms of no activity
            try:
                # Get current window size
                current_width = window.winfo_width()
                current_height = window.winfo_height()
                
                if current_width > 100 and current_height > 100:  # Valid size
                    # Recalculate optimal settings
                    new_screen_info = get_screen_info(window)
                    new_screen_info['effective_width'] = current_width
                    new_screen_info['effective_height'] = current_height
                    
                    new_sizes = calculate_adaptive_sizes(new_screen_info)
                    
                    # Update fonts if window size changed significantly
                    font_size = max(8, min(16, new_sizes['font_base']))
                    
                    # Apply new font sizes
                    new_font = ('Helvetica', font_size)
                    title_font = ('Helvetica', font_size + 2, 'bold')
                    
                    # Update all text widgets
                    text_field.configure(font=new_font)
                    expected_text_widget.configure(font=new_font)
                    
                    # Update labels
                    platform_label.configure(font=('Helvetica', font_size, 'bold'))
                    
                    # Update button fonts
                    button_font = ('Helvetica', font_size, 'bold')
                    start_button.configure(font=button_font)
                    end_button.configure(font=button_font)
                    
            except Exception as e:
                print(f"Resize error: {e}")
    
    def on_window_resize(event):
        nonlocal last_resize_time, resize_timer
        
        if event.widget == window:
            last_resize_time = time.time()
            
            # Cancel previous timer
            if resize_timer:
                window.after_cancel(resize_timer)
            
            # Schedule new resize
            resize_timer = window.after(300, delayed_resize)
    
    # Bind resize event
    window.bind("<Configure>", on_window_resize)
    
    # ===================
    # FINAL SETUP
    # ===================
    
    # Update start button styling when enabled
    def update_start_button():
        if platform_combo.get():
            start_button.configure(
                text="Start Test",
                state=tk.NORMAL,
                bg='#28a745',
                fg='white',
                activebackground='#218838',
                activeforeground='white'
            )
            create_hover_effect(start_button, '#28a745', '#218838')
    
    # Bind platform selection to button update
    original_on_platform_select = platform_combo.bind('<<ComboboxSelected>>')
    def enhanced_platform_select(event):
        on_platform_select(event)
        update_start_button()
    
    platform_combo.bind('<<ComboboxSelected>>', enhanced_platform_select)
    
    # Set initial focus
    platform_combo.focus_set()
    
    # Force initial layout update
    window.update_idletasks()
    delayed_resize()
    
    print(f"Layout initialized for {sizes['category']} screen")
    print(f"Window: {sizes['window_width']}x{sizes['window_height']}")
    
    window.mainloop()

    
if __name__ == "__main__":
    main()