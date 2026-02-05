import tkinter as tk
from tkinter import ttk
import time
import pandas as pd
from keyboard import on_press_key, unhook_all
from tkinter import messagebox
import math
from keyboard import on_press_key, unhook_all, is_pressed
import webbrowser
import urllib.parse

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
    'backspace': 3.8,  # Shorter distance on laptop
    'delete': 4.2,     # Closer keys on laptop
    'page up': 5.2,    # More compact layout
    'page down': 5.2,  
    'home': 4.8,       
    'end': 4.8,        
    'left': 3.5,       # Closer arrow keys
    'right': 3.5,      
    'up': 3.8,         
    'down': 3.8,       

    'alt+i': 0.8,  # Up key
    'alt+k': 0.0,  # Down key
    'alt+l': 0.0,  # Right key
    'alt+j': 0.0,  # Left key
    'alt+;': 0.0,  # Backspace key
    'alt+p': 1.0,  # Delete key
    'alt+u': 1.0,  # Home key
    'alt+o': 1.0,  # Endline key
    'alt+\'': 0.8,  # PageUp key
    'alt+[': 1.8,  # PageDown key
}

computer_key_distances = {
    'backspace': 4.42,  # Original distances for desktop keyboard
    'delete': 5.0,     
    'page up': 6.0,    
    'page down': 6.0,  
    'home': 5.5,       
    'end': 5.5,        
    'left': 4.0,       
    'right': 4.0,      
    'up': 4.5,         
    'down': 4.5,        

    'alt+i': 1.0,  # Up key
    'alt+k': 0.0,  # Down key
    'alt+l': 0.0,  # Right key
    'alt+j': 0.0,  # Left key
    'alt+;': 0.0,  # Backspace key
    'alt+p': 1.2,  # Delete key
    'alt+u': 1.2,  # Home key
    'alt+o': 1.2,  # Endline key
    'alt+\'': 1.0,  # PageUp key
    'alt+[': 2.23,  # PageDown key
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
            elif custom_key in ['alt+u', 'alt+o']:  # Home/Endline keys
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
        messagebox.showwarning("Platform Not Selected", "Please select a platform first!")
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
    """Show a dialog asking user to guess their key usage statistics"""
    dialog = tk.Toplevel()
    dialog.title("Guess Your Statistics!")
    dialog.geometry("400x500")
    dialog.grab_set()  # Make it modal
    
    # Center the dialog
    dialog.transient()
    
    tk.Label(dialog, text="Before seeing your results...", font=('Helvetica', 16, 'bold')).pack(pady=10)
    tk.Label(dialog, text="Can you guess how many times you pressed:", font=('Helvetica', 12)).pack(pady=5)
    
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
    
    for stat_name, stat_key in stats_to_guess:
        frame = tk.Frame(dialog)
        frame.pack(pady=5, padx=20, fill=tk.X)
        
        tk.Label(frame, text=f"{stat_name}:", width=15, anchor='w').pack(side=tk.LEFT)
        entry = tk.Entry(frame, width=10, justify='center')
        entry.pack(side=tk.RIGHT)
        entries[stat_key] = entry
        
        # Set default value to 0
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
    
    def skip_guessing():
        dialog.destroy()
        show_results()
    
    # Buttons
    button_frame = tk.Frame(dialog)
    button_frame.pack(pady=20)
    
    tk.Button(button_frame, text="Submit Guesses", command=submit_guesses, 
              bg='lightgreen', font=('Helvetica', 12, 'bold')).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Skip", command=skip_guessing,
              bg='lightgray', font=('Helvetica', 12)).pack(side=tk.LEFT, padx=10)
    
    # Instructions
    tk.Label(dialog, text="Enter your best guess for each category", 
             font=('Helvetica', 10, 'italic'), fg='gray').pack(pady=(20, 0))

def show_results_with_guesses(guesses):
    """Show results comparing guesses with actual values"""
    # Calculate accuracy of guesses
    actual_values = {
        'backspace_usage': backspace_usage,
        'navigational_key_usage': navigation_key_usage,
        'delete_usage': delete_usage,
        'pageup_pagedown_usage': pageup_pagedown_usage,
        'home_key_usage': home_key_usage
    }
    
    result_message = f"Platform: {platform_combo.get()}\n"
    result_message += f"WPM: {data['wpm']:.2f}\n"
    result_message += f"Accuracy: {data['accuracy']:.2f}%\n"
    result_message += f"Completion Time: {data['completion_time']:.2f}s\n"
    result_message += f"Error Rate: {data['error_rate']:.2f}\n"
    result_message += f"Finger Movement Distance: {data['finger_movement_distance']:.2f}\n"
    result_message += f"Home Row Retention: {data['home_row_retention']:.2f}%\n"
    result_message += f"Correction Time: {data['correction_time']:.2f}s\n\n"
    
    result_message += "=== YOUR GUESSES vs ACTUAL ===\n"
    
    stat_names = {
        'backspace_usage': 'Backspace',
        'navigational_key_usage': 'Arrow Keys',
        'delete_usage': 'Delete Key',
        'pageup_pagedown_usage': 'PageUp/PageDown',
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
    result_message += f"\nOverall Guess Accuracy: {overall_guess_accuracy:.1f}%"
    
    messagebox.showinfo("Test Results with Your Guesses", result_message)
    
    # Save to Excel with guess data
    enhanced_data = data.copy()
    enhanced_data.update({
        'guessed_backspace': guesses.get('backspace_usage', 0),
        'actual_backspace': backspace_usage,
        'guessed_arrows': guesses.get('navigational_key_usage', 0),
        'actual_arrows': navigation_key_usage,
        'guessed_delete': guesses.get('delete_usage', 0),
        'actual_delete': delete_usage,
        'guessed_pageup_pagedown': guesses.get('pageup_pagedown_usage', 0),
        'actual_pageup_pagedown': pageup_pagedown_usage,
        'guessed_home_end': guesses.get('home_key_usage', 0),
        'actual_home_end': home_key_usage,
        'guess_accuracy': overall_guess_accuracy
    })
    
def show_results():
    """Show basic results without guessing game"""
    result_message = (
        f"Platform: {platform_combo.get()}\n"
        f"WPM: {data['wpm']:.2f}\n"
        f"Accuracy: {data['accuracy']:.2f}%\n"
        f"Completion Time: {data['completion_time']:.2f}s\n"
        f"Error Rate: {data['error_rate']:.2f}\n"
        f"Finger Movement Distance: {data['finger_movement_distance']:.2f}\n"
        f"Home Row Retention: {data['home_row_retention']:.2f}%\n"
        f"Correction Time: {data['correction_time']:.2f}s\n"
        f"Navigational Key Usage: {data['navigational_key_usage']}\n"
        f"Backspace Usage: {data['backspace_usage']}\n"
        f"Delete Usage: {data['delete_usage']}\n"
        f"PageUp/PageDown Usage: {data['pageup_pagedown_usage']}\n"
        f"Home/End Key Usage: {home_key_usage}\n"
    )
    messagebox.showinfo("Test Results", result_message)
    
    # Optionally save to Excel or CSV
    df = pd.DataFrame([data])
    df.to_excel('typing_test_results.xlsx', index=False)

def main():
    global text_field, start_button, platform_combo, expected_text_widget
    window = tk.Tk()
    window.title("Typing Test")

    # Set up frames for layout
    main_frame = tk.Frame(window)
    main_frame.pack(pady=10, padx=10)

    # Platform selection frame (at the top)
    platform_frame = tk.Frame(main_frame)
    platform_frame.grid(row=0, column=0, columnspan=2, pady=10)

    platform_label = tk.Label(platform_frame, text="Select Platform:", font=('Helvetica', 12, 'bold'))
    platform_label.pack(side=tk.LEFT, padx=5)

    platform_combo = ttk.Combobox(platform_frame, values=["Laptop", "Computer"], state="readonly", width=15)
    platform_combo.pack(side=tk.LEFT, padx=5)
    platform_combo.bind('<<ComboboxSelected>>', on_platform_select)

    right_frame = tk.Frame(main_frame)
    right_frame.grid(row=1, column=0, padx=10)

    left_frame = tk.Frame(main_frame)
    left_frame.grid(row=1, column=1, padx=10)

    # Text display (on the left side)
    task_label = tk.Label(left_frame, text="Text to Type:", font=('Helvetica', 14, 'bold'))
    task_label.pack()

    # Use Text widget instead of Label for highlighting capability
    expected_text_widget = tk.Text(left_frame, wrap=tk.WORD, width=50, height=30, 
                                 font=('Helvetica', 12), state=tk.DISABLED,
                                 cursor="arrow", relief=tk.SUNKEN, bd=1)
    expected_text_widget.pack(pady=26, fill=tk.BOTH, expand=False)
    
    # Insert the expected text
    expected_text_widget.config(state=tk.NORMAL)
    expected_text_widget.insert("1.0", expected_text)
    expected_text_widget.config(state=tk.DISABLED)
    
    # Disable all interactions with the expected text widget
    expected_text_widget.bind("<Button-1>", lambda e: "break")
    expected_text_widget.bind("<Button-2>", lambda e: "break")
    expected_text_widget.bind("<Button-3>", lambda e: "break")
    expected_text_widget.bind("<Key>", lambda e: "break")

    # Typing input field (on the right side)
    text_field = tk.Text(right_frame, height=55, width=170)
    text_field.config(state=tk.DISABLED)  # Disable typing field initially
    
    # Disable mouse clicks in text field
    text_field.bind("<Button-1>", disable_mouse_click)
    text_field.bind("<Button-2>", disable_mouse_click)
    text_field.bind("<Button-3>", disable_mouse_click)
    text_field.bind("<Double-Button-1>", disable_mouse_click)
    text_field.bind("<Triple-Button-1>", disable_mouse_click)
    
    text_field.pack()

    start_button = tk.Button(right_frame, text="Select platform first", command=start_test, state=tk.DISABLED)
    start_button.pack()

    end_button = tk.Button(right_frame, text="End Test", command=end_test)
    end_button.pack()

    window.mainloop()

if __name__ == "__main__":
    main()