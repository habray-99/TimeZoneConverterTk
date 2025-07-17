# import json
# import os
# from datetime import datetime
# import pytz
# import re

# class MeetingTimeConverter:
#     def __init__(self, json_file='team_timezones.json'):
#         self.json_file = json_file
#         self.timezone_data = self.load_timezone_data()
        
#         # Common timezone mappings
#         self.timezone_map = {
#             'IST': 'Asia/Kolkata',
#             'AEST': 'Australia/Sydney',
#             'GMT+4': 'Asia/Dubai',  # UAE timezone
#             'EST': 'America/New_York',
#             'PST': 'America/Los_Angeles',
#             'GMT': 'Europe/London',
#             'CET': 'Europe/Paris',
#             'JST': 'Asia/Tokyo',
#             'CST': 'America/Chicago'
#         }
    
#     def load_timezone_data(self):
#         """Load timezone data from JSON file, create if doesn't exist"""
#         if os.path.exists(self.json_file):
#             try:
#                 with open(self.json_file, 'r') as f:
#                     return json.load(f)
#             except (json.JSONDecodeError, FileNotFoundError):
#                 print(f"Error reading {self.json_file}, creating new file...")
        
#         # Default data structure - simplified to just track timezones
#         default_data = {
#             "timezones": {
#                 "AEST": [],
#                 "IST": [],
#                 "GMT+4": []
#             }
#         }
#         self.save_timezone_data(default_data)
#         return default_data
    
#     def save_timezone_data(self, data=None):
#         """Save timezone data to JSON file"""
#         if data is None:
#             data = self.timezone_data
        
#         with open(self.json_file, 'w') as f:
#             json.dump(data, f, indent=2)
#         print(f"Timezone data saved to {self.json_file}")
    
#     def add_timezone(self, timezone):
#         """Add a new timezone to track"""
#         if timezone not in self.timezone_data["timezones"]:
#             self.timezone_data["timezones"][timezone] = []
#             self.save_timezone_data()
#             print(f"Added timezone: {timezone}")
#         else:
#             print(f"Timezone {timezone} already exists")
    
#     def remove_timezone(self, timezone):
#         """Remove a timezone from tracking"""
#         if timezone in self.timezone_data["timezones"]:
#             del self.timezone_data["timezones"][timezone]
#             self.save_timezone_data()
#             print(f"Removed timezone: {timezone}")
#         else:
#             print(f"Timezone {timezone} not found")
    
#     def list_timezones(self):
#         """Display all tracked timezones"""
#         print("\nCurrently Tracked Timezones:")
#         print("-" * 30)
#         for timezone in self.timezone_data["timezones"].keys():
#             print(f"• {timezone}")
    
#     # Keep these methods for backward compatibility but simplify them
#     def add_person_to_timezone(self, person_name, timezone):
#         """Add a timezone (person names no longer used)"""
#         self.add_timezone(timezone)
    
#     def remove_person_from_timezone(self, person_name, timezone):
#         """Remove a timezone (person names no longer used)"""
#         if timezone in self.timezone_data["timezones"]:
#             # Only remove if user confirms
#             confirm = input(f"Remove entire timezone {timezone}? (y/n): ").lower()
#             if confirm == 'y':
#                 self.remove_timezone(timezone)
    
#     def list_team_members(self):
#         """Display all tracked timezones (replaces team member listing)"""
#         self.list_timezones()
    
#     def parse_time_input(self, time_input):
#         """Parse time input in format 'start_time am/pm end_time am/pm timezone'"""
#         # Regex pattern to match the expected format
#         pattern = r'(\d{1,2}):?(\d{2})?\s*(am|pm)\s+(\d{1,2}):?(\d{2})?\s*(am|pm)\s+(\w+(?:\+\d)?)'
        
#         match = re.match(pattern, time_input.strip(), re.IGNORECASE)
#         if not match:
#             raise ValueError("Invalid time format. Expected: 'start_time am/pm end_time am/pm timezone'")
        
#         start_hour, start_min, start_ampm, end_hour, end_min, end_ampm, timezone = match.groups()
        
#         # Convert to 24-hour format
#         start_hour = int(start_hour)
#         end_hour = int(end_hour)
#         start_min = int(start_min) if start_min else 0
#         end_min = int(end_min) if end_min else 0
        
#         if start_ampm.lower() == 'pm' and start_hour != 12:
#             start_hour += 12
#         elif start_ampm.lower() == 'am' and start_hour == 12:
#             start_hour = 0
            
#         if end_ampm.lower() == 'pm' and end_hour != 12:
#             end_hour += 12
#         elif end_ampm.lower() == 'am' and end_hour == 12:
#             end_hour = 0
        
#         return start_hour, start_min, end_hour, end_min, timezone.upper()
    
#     def convert_time_to_timezone(self, dt, from_tz, to_tz):
#         """Convert datetime from one timezone to another"""
#         from_timezone = pytz.timezone(self.timezone_map.get(from_tz, from_tz))
#         to_timezone = pytz.timezone(self.timezone_map.get(to_tz, to_tz))
        
#         # Localize the datetime to the source timezone
#         localized_dt = from_timezone.localize(dt)
        
#         # Convert to target timezone
#         converted_dt = localized_dt.astimezone(to_timezone)
        
#         return converted_dt
    
#     def format_time_12hour(self, dt):
#         """Format datetime to 12-hour format"""
#         return dt.strftime("%I:%M %p").lstrip('0')
    
#     def convert_meeting_time(self, time_input):
#         """Convert meeting time to all registered timezones"""
#         try:
#             start_hour, start_min, end_hour, end_min, source_timezone = self.parse_time_input(time_input)
            
#             # Create datetime objects (using today's date)
#             today = datetime.now().date()
#             start_dt = datetime.combine(today, datetime.min.time().replace(hour=start_hour, minute=start_min))
#             end_dt = datetime.combine(today, datetime.min.time().replace(hour=end_hour, minute=end_min))
            
#             # Handle case where end time is next day
#             if end_dt <= start_dt:
#                 end_dt = end_dt.replace(day=end_dt.day + 1)
            
#             result_parts = []
            
#             # Convert to all registered timezones
#             for timezone in self.timezone_data["timezones"]:
#                 if timezone in self.timezone_map:
#                     # Convert times
#                     converted_start = self.convert_time_to_timezone(start_dt, source_timezone, timezone)
#                     converted_end = self.convert_time_to_timezone(end_dt, source_timezone, timezone)
                    
#                     # Format times
#                     start_str = self.format_time_12hour(converted_start)
#                     end_str = self.format_time_12hour(converted_end)
                    
#                     # Format: "TIMEZONE: start_time - end_time"
#                     result_parts.append(f"{timezone}: {start_str} - {end_str}")
#                 else:
#                     print(f"Warning: Timezone mapping not found for {timezone}")
            
#             # Join all parts with newlines for better readability
#             return "Meeting Time:\n" + "\n".join(result_parts)
            
#         except Exception as e:
#             return f"Error: {str(e)}"
    
#     def add_timezone_mapping(self, short_name, pytz_name):
#         """Add a new timezone mapping"""
#         self.timezone_map[short_name] = pytz_name
#         print(f"Added timezone mapping: {short_name} -> {pytz_name}")
    
#     def interactive_menu(self):
#         """Interactive menu for managing the converter"""
#         while True:
#             print("\n" + "="*50)
#             print("Global Meeting Time Converter")
#             print("="*50)
#             print("1. Convert meeting time")
#             print("2. Add timezone")
#             print("3. Remove timezone")
#             print("4. List timezones")
#             print("5. Add timezone mapping")
#             print("6. Exit")
#             print("-"*50)
            
#             choice = input("Enter your choice (1-6): ").strip()
            
#             if choice == '1':
#                 time_input = input("\nEnter meeting time (e.g., '2:00 PM 4:00 PM IST'): ")
#                 result = self.convert_meeting_time(time_input)
#                 print(f"\n{result}")
                
#                 # Option to copy to clipboard (if available)
#                 try:
#                     import pyperclip
#                     copy_choice = input("\nCopy to clipboard? (y/n): ").lower()
#                     if copy_choice == 'y':
#                         pyperclip.copy(result)
#                         print("Copied to clipboard!")
#                 except ImportError:
#                     print("(Install pyperclip for clipboard functionality)")
            
#             elif choice == '2':
#                 timezone = input("Enter timezone (e.g., AEST, IST, GMT+4): ").strip().upper()
#                 self.add_timezone(timezone)
            
#             elif choice == '3':
#                 timezone = input("Enter timezone to remove: ").strip().upper()
#                 self.remove_timezone(timezone)
            
#             elif choice == '4':
#                 self.list_timezones()
            
#             elif choice == '5':
#                 short_name = input("Enter short timezone name (e.g., GMT+4): ").strip().upper()
#                 pytz_name = input("Enter pytz timezone name (e.g., Asia/Dubai): ").strip()
#                 self.add_timezone_mapping(short_name, pytz_name)
            
#             elif choice == '6':
#                 print("Goodbye!")
#                 break
            
#             else:
#                 print("Invalid choice. Please try again.")

# def main():
#     """Main function to run the converter"""
#     converter = MeetingTimeConverter()
    
#     # Example usage
#     # print("Global Meeting Time Converter")
#     # print("Example usage:")
#     # print("Input: '2:00 PM 4:00 PM IST'")
#     # print("Output:")
#     # print("Meeting Time:")
#     # print("AEST: 7:30 PM - 9:30 PM")
#     # print("IST: 2:00 PM - 4:00 PM")
#     # print("GMT+4: 10:30 AM - 12:30 PM")
#     # print("\nClean format - just times for each timezone, perfect for Teams messages!")
    
#     # Run interactive menu
#     converter.interactive_menu()

# if __name__ == "__main__":
#     main()

import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import pytz
import re

class MeetingTimeConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Global Meeting Time Converter")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        self.json_file = 'team_timezones.json'
        self.timezone_data = self.load_timezone_data()
        
        # Common timezone mappings
        self.timezone_map = {
            'IST': 'Asia/Kolkata',
            'AEST': 'Australia/Sydney',
            'GMT+4': 'Asia/Dubai',  # UAE timezone
            'EST': 'America/New_York',
            'PST': 'America/Los_Angeles',
            'GMT': 'Europe/London',
            'CET': 'Europe/Paris',
            'JST': 'Asia/Tokyo',
            'CST': 'America/Chicago',
            'MST': 'America/Denver',
            'BST': 'Europe/London',
            'CEST': 'Europe/Paris'
        }
        
        self.setup_ui()
        self.refresh_timezone_list()
    
    def load_timezone_data(self):
        """Load timezone data from JSON file, create if doesn't exist"""
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        # Default data structure
        default_data = {
            "timezones": {
                "AEST": [],
                "IST": [],
                "GMT+4": []
            }
        }
        self.save_timezone_data(default_data)
        return default_data
    
    def save_timezone_data(self, data=None):
        """Save timezone data to JSON file"""
        if data is None:
            data = self.timezone_data
        
        with open(self.json_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def setup_ui(self):
        """Setup the main UI"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Global Meeting Time Converter", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Time Input Section
        time_frame = ttk.LabelFrame(main_frame, text="Time Conversion", padding="10")
        time_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        time_frame.columnconfigure(1, weight=1)
        
        ttk.Label(time_frame, text="Meeting Time:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        self.time_entry = ttk.Entry(time_frame, width=30)
        self.time_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        self.time_entry.insert(0, "2:00 PM 4:00 PM IST")
        
        convert_btn = ttk.Button(time_frame, text="Convert", command=self.convert_time)
        convert_btn.grid(row=0, column=2, padx=(5, 0))
        
        # Example label
        example_label = ttk.Label(time_frame, text="Example: 2:00 PM 4:00 PM IST", 
                                 font=('Arial', 8), foreground='gray')
        example_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(5, 0))
        
        # Results Section
        results_frame = ttk.LabelFrame(main_frame, text="Converted Times", padding="10")
        results_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=10, width=50)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Copy button
        copy_btn = ttk.Button(results_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        copy_btn.grid(row=1, column=0, pady=(10, 0))
        
        # Timezone Management Section
        tz_frame = ttk.LabelFrame(main_frame, text="Timezone Management", padding="10")
        tz_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        tz_frame.columnconfigure(1, weight=1)
        
        # Add timezone
        ttk.Label(tz_frame, text="Add Timezone:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        self.tz_entry = ttk.Entry(tz_frame, width=20)
        self.tz_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        add_btn = ttk.Button(tz_frame, text="Add", command=self.add_timezone)
        add_btn.grid(row=0, column=2, padx=(5, 0))
        
        # Timezone list
        ttk.Label(tz_frame, text="Active Timezones:").grid(row=1, column=0, sticky=tk.W, pady=(10, 5))
        
        # Listbox with scrollbar
        list_frame = ttk.Frame(tz_frame)
        list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        
        self.tz_listbox = tk.Listbox(list_frame, height=6)
        self.tz_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        tz_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tz_listbox.yview)
        tz_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tz_listbox.configure(yscrollcommand=tz_scrollbar.set)
        
        # Remove button
        remove_btn = ttk.Button(tz_frame, text="Remove Selected", command=self.remove_timezone)
        remove_btn.grid(row=3, column=0, columnspan=3, pady=(5, 0))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                                font=('Arial', 8), foreground='blue')
        status_label.grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=(10, 0))
        
        # Configure main frame grid weights
        main_frame.rowconfigure(2, weight=1)
    
    def refresh_timezone_list(self):
        """Refresh the timezone listbox"""
        self.tz_listbox.delete(0, tk.END)
        for timezone in sorted(self.timezone_data["timezones"].keys()):
            self.tz_listbox.insert(tk.END, timezone)
    
    def add_timezone(self):
        """Add a new timezone"""
        timezone = self.tz_entry.get().strip().upper()
        if not timezone:
            messagebox.showwarning("Warning", "Please enter a timezone")
            return
        
        if timezone in self.timezone_data["timezones"]:
            messagebox.showinfo("Info", f"Timezone {timezone} already exists")
            return
        
        # Check if timezone mapping exists
        if timezone not in self.timezone_map:
            # Ask user for pytz timezone name
            pytz_name = self.ask_pytz_name(timezone)
            if pytz_name:
                try:
                    # Validate timezone
                    pytz.timezone(pytz_name)
                    self.timezone_map[timezone] = pytz_name
                except pytz.UnknownTimeZoneError:
                    messagebox.showerror("Error", f"Invalid timezone: {pytz_name}")
                    return
            else:
                return
        
        self.timezone_data["timezones"][timezone] = []
        self.save_timezone_data()
        self.refresh_timezone_list()
        self.tz_entry.delete(0, tk.END)
        self.status_var.set(f"Added timezone: {timezone}")
    
    def ask_pytz_name(self, timezone):
        """Ask user for pytz timezone name"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Timezone Mapping")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text=f"Enter pytz timezone name for {timezone}:").pack(pady=10)
        ttk.Label(dialog, text="(e.g., Asia/Dubai, America/New_York)", 
                 font=('Arial', 8), foreground='gray').pack()
        
        entry = ttk.Entry(dialog, width=40)
        entry.pack(pady=10)
        entry.focus()
        
        result = [None]
        
        def ok_clicked():
            result[0] = entry.get().strip()
            dialog.destroy()
        
        def cancel_clicked():
            dialog.destroy()
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="OK", command=ok_clicked).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=cancel_clicked).pack(side=tk.LEFT, padx=5)
        
        dialog.bind('<Return>', lambda e: ok_clicked())
        dialog.bind('<Escape>', lambda e: cancel_clicked())
        
        dialog.wait_window()
        return result[0]
    
    def remove_timezone(self):
        """Remove selected timezone"""
        selection = self.tz_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a timezone to remove")
            return
        
        timezone = self.tz_listbox.get(selection[0])
        
        if messagebox.askyesno("Confirm", f"Remove timezone {timezone}?"):
            del self.timezone_data["timezones"][timezone]
            self.save_timezone_data()
            self.refresh_timezone_list()
            self.status_var.set(f"Removed timezone: {timezone}")
    
    def parse_time_input(self, time_input):
        """Parse time input in format 'start_time am/pm end_time am/pm timezone'"""
        # Regex pattern to match the expected format
        pattern = r'(\d{1,2}):?(\d{2})?\s*(am|pm)\s+(\d{1,2}):?(\d{2})?\s*(am|pm)\s+(\w+(?:\+\d)?)'
        
        match = re.match(pattern, time_input.strip(), re.IGNORECASE)
        if not match:
            raise ValueError("Invalid time format. Expected: 'start_time am/pm end_time am/pm timezone'")
        
        start_hour, start_min, start_ampm, end_hour, end_min, end_ampm, timezone = match.groups()
        
        # Convert to 24-hour format
        start_hour = int(start_hour)
        end_hour = int(end_hour)
        start_min = int(start_min) if start_min else 0
        end_min = int(end_min) if end_min else 0
        
        if start_ampm.lower() == 'pm' and start_hour != 12:
            start_hour += 12
        elif start_ampm.lower() == 'am' and start_hour == 12:
            start_hour = 0
            
        if end_ampm.lower() == 'pm' and end_hour != 12:
            end_hour += 12
        elif end_ampm.lower() == 'am' and end_hour == 12:
            end_hour = 0
        
        return start_hour, start_min, end_hour, end_min, timezone.upper()
    
    def convert_time_to_timezone(self, dt, from_tz, to_tz):
        """Convert datetime from one timezone to another"""
        from_timezone = pytz.timezone(self.timezone_map.get(from_tz, from_tz))
        to_timezone = pytz.timezone(self.timezone_map.get(to_tz, to_tz))
        
        # Localize the datetime to the source timezone
        localized_dt = from_timezone.localize(dt)
        
        # Convert to target timezone
        converted_dt = localized_dt.astimezone(to_timezone)
        
        return converted_dt
    
    def format_time_12hour(self, dt):
        """Format datetime to 12-hour format"""
        return dt.strftime("%I:%M %p").lstrip('0')
    
    def convert_time(self):
        """Convert meeting time to all registered timezones"""
        time_input = self.time_entry.get().strip()
        if not time_input:
            messagebox.showwarning("Warning", "Please enter a meeting time")
            return
        
        try:
            start_hour, start_min, end_hour, end_min, source_timezone = self.parse_time_input(time_input)
            
            # Create datetime objects (using today's date)
            today = datetime.now().date()
            start_dt = datetime.combine(today, datetime.min.time().replace(hour=start_hour, minute=start_min))
            end_dt = datetime.combine(today, datetime.min.time().replace(hour=end_hour, minute=end_min))
            
            # Handle case where end time is next day
            if end_dt <= start_dt:
                end_dt = end_dt.replace(day=end_dt.day + 1)
            
            result_parts = []
            
            # Convert to all registered timezones
            for timezone in sorted(self.timezone_data["timezones"].keys()):
                if timezone in self.timezone_map:
                    # Convert times
                    converted_start = self.convert_time_to_timezone(start_dt, source_timezone, timezone)
                    converted_end = self.convert_time_to_timezone(end_dt, source_timezone, timezone)
                    
                    # Format times
                    start_str = self.format_time_12hour(converted_start)
                    end_str = self.format_time_12hour(converted_end)
                    
                    # Format: "TIMEZONE: start_time - end_time"
                    result_parts.append(f"{timezone}: {start_str} - {end_str}")
                else:
                    result_parts.append(f"{timezone}: [Timezone mapping not found]")
            
            # Display results
            result_text = "Meeting Time:\n" + "\n".join(result_parts)
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(1.0, result_text)
            
            self.status_var.set("Time conversion completed")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error converting time: {str(e)}")
            self.status_var.set("Error in conversion")
    
    def copy_to_clipboard(self):
        """Copy results to clipboard"""
        content = self.results_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "No content to copy")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        self.root.update()  # Required for clipboard to work
        
        messagebox.showinfo("Success", "Meeting times copied to clipboard!")
        self.status_var.set("Copied to clipboard")

def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = MeetingTimeConverterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()