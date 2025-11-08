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
    'alt+[': 0.8,  # PageDown key
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
    
    # Configure tags for different states
    expected_text_widget.tag_configure("correct", foreground="green", font=('Helvetica', 12, 'bold'))
    expected_text_widget.tag_configure("incorrect", foreground="red", font=('Helvetica', 12, 'bold'))
    expected_text_widget.tag_configure("untyped", foreground="black", font=('Helvetica', 12))
    
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

    start_button.pack_forget()

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
    
    unhook_all()  # Unhook all key tracking when the test ends
    calculate_results()
    show_guessing_dialog()  # Show guessing dialog instead of direct results

def calculate_results():
    global total_typing_time
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
    window = tk.Tk()
    window.title("Typing Test")
    
    # Make window resizable
    window.geometry("1200x800")  # Initial size
    window.minsize(800, 600)    # Minimum size to prevent excessive shrinking
    
    # Configure window to expand with resizing
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

    # Set up main frame for layout
    main_frame = tk.Frame(window)
    main_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(1, weight=1)

    # Platform selection frame (at the top)
    platform_frame = tk.Frame(main_frame)
    platform_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")
    platform_frame.columnconfigure(1, weight=1)

    platform_label = tk.Label(platform_frame, text="Select Platform:", font=('Helvetica', 12, 'bold'))
    platform_label.pack(side=tk.LEFT, padx=5)

    platform_combo = ttk.Combobox(platform_frame, values=["Laptop", "Computer"], state="readonly", width=15)
    platform_combo.pack(side=tk.LEFT, padx=5)
    platform_combo.bind('<<ComboboxSelected>>', on_platform_select)

    # Create left and right frames for text display and input
    left_frame = tk.Frame(main_frame)
    left_frame.grid(row=1, column=0, padx=10, sticky="nsew")  # Left frame for typing area
    left_frame.columnconfigure(0, weight=1)
    left_frame.rowconfigure(0, weight=1)

    right_frame = tk.Frame(main_frame)
    right_frame.grid(row=1, column=1, padx=10, sticky="nsew")  # Right frame for text to type
    right_frame.columnconfigure(0, weight=1)
    right_frame.rowconfigure(1, weight=1)

    # Typing input field (on the left side)
    text_field = tk.Text(left_frame, font=('Helvetica', 12))
    text_field.config(state=tk.DISABLED)  # Disable typing field initially
    text_field.pack(fill=tk.BOTH, expand=True, pady=10)
    
    # Disable mouse clicks in text field
    text_field.bind("<Button-1>", disable_mouse_click)
    text_field.bind("<Button-2>", disable_mouse_click)
    text_field.bind("<Button-3>", disable_mouse_click)
    text_field.bind("<Double-Button-1>", disable_mouse_click)
    text_field.bind("<Triple-Button-1>", disable_mouse_click)
    
    # Button frame for start and end buttons (below typing area)
    button_frame = tk.Frame(left_frame)
    button_frame.pack(fill=tk.X, pady=5)
    
    start_button = tk.Button(button_frame, text="Select platform first", command=start_test, state=tk.DISABLED)
    start_button.pack(side=tk.LEFT, padx=5)
    
    end_button = tk.Button(button_frame, text="End Test", command=end_test)
    end_button.pack(side=tk.LEFT, padx=5)

    # Text display (on the right side)
    task_label = tk.Label(right_frame, text="Text to Type:", font=('Helvetica', 14, 'bold'))
    task_label.pack(fill=tk.X, pady=(0, 10))

    # Use Text widget with dynamic height and width
    expected_text_widget = tk.Text(right_frame, wrap=tk.WORD, 
                                  font=('Helvetica', 12), state=tk.DISABLED,
                                  cursor="arrow", relief=tk.SUNKEN, bd=1)
    expected_text_widget.pack(fill=tk.BOTH, expand=True, pady=10)
    
    # Insert the expected text
    expected_text_widget.config(state=tk.NORMAL)
    expected_text_widget.insert("1.0", expected_text)
    expected_text_widget.config(state=tk.DISABLED)
    
    # Disable all interactions with the expected text widget
    expected_text_widget.bind("<Button-1>", lambda e: "break")
    expected_text_widget.bind("<Button-2>", lambda e: "break")
    expected_text_widget.bind("<Button-3>", lambda e: "break")
    expected_text_widget.bind("<Key>", lambda e: "break")

    # Update widget sizes based on window resize
    def on_resize(event):
        # Calculate relative font size based on window width
        width = event.width
        base_font_size = max(10, min(14, width // 80))  # Adjust font size dynamically
        text_font = ('Helvetica', base_font_size)
        
        # Update fonts
        task_label.config(font=('Helvetica', base_font_size + 2, 'bold'))
        expected_text_widget.config(font=text_font)
        text_field.config(font=text_font)
        platform_label.config(font=('Helvetica', base_font_size, 'bold'))
        start_button.config(font=('Helvetica', base_font_size))
        end_button.config(font=('Helvetica', base_font_size))
        
        # Adjust text widget height based on window height
        height = event.height
        text_lines = max(20, min(40, height // 20))  # Dynamic height for text widgets
        expected_text_widget.config(height=text_lines)
        text_field.config(height=text_lines)

    window.bind("<Configure>", on_resize)

    window.mainloop()

if __name__ == "__main__":
    main()