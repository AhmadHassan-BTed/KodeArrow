import platform
import os
import subprocess

# Path for the file to store data
user_usage_data = "kodearrow_data.txt"

# Function to remove the hidden attribute before writing
def remove_hidden_attribute(file_path):
    try:
        # For Windows: Use subprocess to remove the hidden attribute
        subprocess.check_call(["attrib", "-H", file_path])
        print(f"Hidden attribute removed for '{file_path}'")
    except subprocess.CalledProcessError as e:
        print(f"Failed to remove hidden attribute: {e}")

# Function to reapply the hidden attribute after writing
def add_hidden_attribute(file_path):
    try:
        # For Windows: Use subprocess to add the hidden attribute
        subprocess.check_call(["attrib", "+H", file_path])
        print(f"Hidden attribute added for '{file_path}'")
    except subprocess.CalledProcessError as e:
        print(f"Failed to add hidden attribute: {e}")

# Function to create a hidden file with initial values (if the file doesn't exist)
def create_hidden_file(file_path, total_words=0, total_shortcuts=0, total_runtime=0):
    if not os.path.exists(file_path):
        # Initialize content with default values
        content = f"{total_words}\n{total_shortcuts}\n{total_runtime}\n"
        
        try:
            with open(file_path, "w") as file:
                file.write(content)
            
            # Set the file as hidden based on the platform (Windows only)
            if platform.system() == "Windows":
                add_hidden_attribute(file_path)
            elif platform.system() in ["Darwin", "Linux"]:
                # For macOS and Linux: Prefix file name with a dot to hide it
                os.rename(file_path, f".{file_path}")
            else:
                raise NotImplementedError(f"Unsupported platform: {platform.system()}")
            
            print(f"Hidden file '{file_path}' created successfully.")
        
        except Exception as e:
            print(f"Failed to create hidden file '{file_path}': {e}")

# Function to write variables to the file
def write_to_file(file_path, total_words, total_shortcuts, total_runtime):
    try:
        remove_hidden_attribute(file_path)
        
        with open(file_path, "w") as file:
            file.write(f"{total_words}\n{total_shortcuts}\n{total_runtime}\n")
            
        add_hidden_attribute(file_path)
        
    except Exception as e:
        print(f"Failed to write to file '{file_path}': {e}")

# Function to read variables from the file
def read_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            # Read lines and convert each line to an integer
            total_words = int(file.readline().strip())
            total_shortcuts = int(file.readline().strip())
            total_runtime = int(file.readline().strip())
        return total_words, total_shortcuts, total_runtime
    except FileNotFoundError:
        print("File not found. Initializing values to 0.")
        return 0, 0, 0
    except ValueError:
        print("Invalid data in file. Reinitializing values to 0.")
        return 0, 0, 0

# Initialize hidden file with default values (if it doesn't exist)
create_hidden_file(user_usage_data)

# Example usage
# Initialize values by reading from the file
total_words, total_shortcuts, total_runtime = read_from_file(user_usage_data)

# Modify values (example updates)
total_words += 10
total_shortcuts += 2
total_runtime += 5

# Write updated values to the file
write_to_file(user_usage_data, total_words, total_shortcuts, total_runtime)

# Read back to verify
total_words, total_shortcuts, total_runtime = read_from_file(user_usage_data)
print("Total words typed:", total_words)
print("Total shortcuts used:", total_shortcuts)
print("Total runtime:", total_runtime)
