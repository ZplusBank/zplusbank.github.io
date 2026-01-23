#!/usr/bin/env python3
"""
Exam Data JavaScript Editor
A tkinter GUI application to edit EXAM_DATA directly in renderer.js file
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import re
import os

class ExamDataJSEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Exam Data JS Editor")
        self.root.geometry("900x650")
        
        # Data structure
        self.exam_data = {}
        self.current_subject = None
        self.js_file_path = None
        self.js_file_content = None
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title and File selector
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(title_frame, text="Exam Data JS Editor", 
                 font=('Arial', 16, 'bold')).pack(side=tk.LEFT)
        
        ttk.Button(title_frame, text="Open renderer.js", 
                  command=self.open_js_file).pack(side=tk.RIGHT, padx=5)
        
        # File path display
        self.file_path_label = ttk.Label(main_frame, text="No file loaded", 
                                         foreground="gray")
        self.file_path_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Left panel - Subject list
        left_frame = ttk.LabelFrame(main_frame, text="Subjects", padding="5")
        left_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Listbox with scrollbar
        list_scroll = ttk.Scrollbar(left_frame)
        list_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.subject_listbox = tk.Listbox(left_frame, yscrollcommand=list_scroll.set,
                                          width=20, font=('Arial', 10))
        self.subject_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        list_scroll.config(command=self.subject_listbox.yview)
        self.subject_listbox.bind('<<ListboxSelect>>', self.on_subject_select)
        
        # Left panel buttons
        left_btn_frame = ttk.Frame(left_frame)
        left_btn_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(left_btn_frame, text="Add Subject", 
                  command=self.add_subject).pack(fill=tk.X, pady=2)
        ttk.Button(left_btn_frame, text="Delete Subject", 
                  command=self.delete_subject).pack(fill=tk.X, pady=2)
        
        # Right panel - Subject editor
        right_frame = ttk.LabelFrame(main_frame, text="Subject Details", padding="10")
        right_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Subject ID
        ttk.Label(right_frame, text="Subject ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.id_entry = ttk.Entry(right_frame, width=40)
        self.id_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Subject Name
        ttk.Label(right_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(right_frame, width=40)
        self.name_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Description
        ttk.Label(right_frame, text="Description:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.desc_entry = ttk.Entry(right_frame, width=40)
        self.desc_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # External Link
        ttk.Label(right_frame, text="External Link:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.link_entry = ttk.Entry(right_frame, width=40)
        self.link_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        
        right_frame.columnconfigure(1, weight=1)
        
        # Save button for current subject
        ttk.Button(right_frame, text="Save Changes", 
                  command=self.save_current_subject).grid(row=4, column=0, columnspan=2, pady=10)
        
        # JSON Preview
        preview_frame = ttk.LabelFrame(right_frame, text="Current EXAM_DATA", padding="5")
        preview_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        preview_scroll = ttk.Scrollbar(preview_frame)
        preview_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.json_text = tk.Text(preview_frame, height=10, width=50, 
                                yscrollcommand=preview_scroll.set,
                                font=('Courier', 9))
        self.json_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        preview_scroll.config(command=self.json_text.yview)
        
        right_frame.rowconfigure(5, weight=1)
        
        # Bottom buttons
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=3, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(bottom_frame, text="Save to renderer.js", 
                  command=self.save_to_js_file, 
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="Reload from File", 
                  command=self.reload_from_file).pack(side=tk.LEFT, padx=5)
        
        # Style for accent button
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Arial', 10, 'bold'))
    
    def open_js_file(self):
        """Open and parse renderer.js file"""
        filename = filedialog.askopenfilename(
            title="Open renderer.js",
            filetypes=[("JavaScript files", "*.js"), ("All files", "*.*")],
            initialfile="renderer.js"
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    self.js_file_content = f.read()
                
                self.js_file_path = filename
                self.extract_exam_data()
                self.refresh_subject_list()
                self.update_json_preview()
                
                # Update file path display
                display_path = filename
                if len(display_path) > 60:
                    display_path = "..." + display_path[-57:]
                self.file_path_label.config(text=f"Loaded: {display_path}", 
                                           foreground="green")
                
                messagebox.showinfo("Success", "JavaScript file loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
    
    def extract_exam_data(self):
        """Extract EXAM_DATA object from JavaScript file"""
        # Pattern to match: const EXAM_DATA = { ... };
        pattern = r'const\s+EXAM_DATA\s*=\s*(\{.*?\n\};)'
        match = re.search(pattern, self.js_file_content, re.DOTALL)
        
        if not match:
            messagebox.showerror("Error", "Could not find EXAM_DATA in the file!")
            return
        
        exam_data_str = match.group(1)
        
        # Convert JavaScript object to JSON-parseable format
        # Remove comments
        exam_data_str = re.sub(r'//.*?
    
    def save_to_js_file(self):
        """Save modified EXAM_DATA back to renderer.js"""
        if not self.js_file_path:
            messagebox.showwarning("No File", "Please open a renderer.js file first!")
            return
        
        if not self.js_file_content:
            messagebox.showerror("Error", "No file content loaded!")
            return
        
        # Convert exam_data to formatted JavaScript object
        js_object = self.dict_to_js_object(self.exam_data, indent=4)
        new_exam_data = f"const EXAM_DATA = {js_object};"
        
        # Replace EXAM_DATA in the file
        pattern = r'const\s+EXAM_DATA\s*=\s*\{[^;]*\};'
        
        if not re.search(pattern, self.js_file_content, re.DOTALL):
            messagebox.showerror("Error", "Could not find EXAM_DATA declaration in file!")
            return
        
        new_content = re.sub(pattern, new_exam_data, self.js_file_content, 
                            count=1, flags=re.DOTALL)
        
        try:
            # Create backup
            backup_path = self.js_file_path + '.backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(self.js_file_content)
            
            # Write new content
            with open(self.js_file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            self.js_file_content = new_content
            
            messagebox.showinfo("Success", 
                              f"File saved successfully!\n\n"
                              f"Backup created at:\n{backup_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
    
    def dict_to_js_object(self, obj, indent=4, level=0):
        """Convert Python dict to JavaScript object string"""
        if isinstance(obj, dict):
            if not obj:
                return "{}"
            
            indent_str = " " * (indent * level)
            inner_indent = " " * (indent * (level + 1))
            
            items = []
            for key, value in obj.items():
                js_value = self.dict_to_js_object(value, indent, level + 1)
                items.append(f'{inner_indent}{key}: {js_value}')
            
            return "{\n" + ",\n".join(items) + f"\n{indent_str}}}"
        
        elif isinstance(obj, str):
            # Escape quotes and special characters
            escaped = obj.replace('\\', '\\\\').replace('"', '\\"')
            return f'"{escaped}"'
        
        elif isinstance(obj, (int, float)):
            return str(obj)
        
        elif isinstance(obj, bool):
            return "true" if obj else "false"
        
        elif obj is None:
            return "null"
        
        elif isinstance(obj, list):
            if not obj:
                return "[]"
            items = [self.dict_to_js_object(item, indent, level + 1) for item in obj]
            return "[" + ", ".join(items) + "]"
        
        return str(obj)
    
    def reload_from_file(self):
        """Reload data from the currently open file"""
        if not self.js_file_path:
            messagebox.showwarning("No File", "No file is currently open!")
            return
        
        try:
            with open(self.js_file_path, 'r', encoding='utf-8') as f:
                self.js_file_content = f.read()
            
            self.extract_exam_data()
            self.refresh_subject_list()
            self.update_json_preview()
            self.clear_form()
            
            messagebox.showinfo("Success", "Data reloaded from file!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reload file:\n{str(e)}")
    
    def refresh_subject_list(self):
        """Refresh the listbox with current subjects"""
        self.subject_listbox.delete(0, tk.END)
        for subject_id in sorted(self.exam_data.keys()):
            self.subject_listbox.insert(tk.END, subject_id)
    
    def on_subject_select(self, event):
        """Handle subject selection from listbox"""
        selection = self.subject_listbox.curselection()
        if not selection:
            return
        
        subject_id = self.subject_listbox.get(selection[0])
        self.current_subject = subject_id
        self.load_subject_to_form(subject_id)
    
    def load_subject_to_form(self, subject_id):
        """Load subject data into form fields"""
        if subject_id not in self.exam_data:
            return
        
        data = self.exam_data[subject_id]
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, data.get('id', ''))
        
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, data.get('name', ''))
        
        self.desc_entry.delete(0, tk.END)
        self.desc_entry.insert(0, data.get('description', ''))
        
        self.link_entry.delete(0, tk.END)
        self.link_entry.insert(0, data.get('externalLink', ''))
    
    def add_subject(self):
        """Add a new subject"""
        if not self.js_file_path:
            messagebox.showwarning("No File", "Please open a renderer.js file first!")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Subject")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Enter Subject ID:").pack(pady=10)
        id_entry = ttk.Entry(dialog, width=30)
        id_entry.pack(pady=5)
        id_entry.focus()
        
        def create():
            subject_id = id_entry.get().strip()
            if not subject_id:
                messagebox.showwarning("Invalid Input", "Subject ID cannot be empty!")
                return
            
            if subject_id in self.exam_data:
                messagebox.showwarning("Duplicate ID", "This subject ID already exists!")
                return
            
            self.exam_data[subject_id] = {
                "id": subject_id,
                "name": "",
                "description": "",
                "externalLink": ""
            }
            self.refresh_subject_list()
            self.update_json_preview()
            dialog.destroy()
            
            # Select the new subject
            items = list(self.subject_listbox.get(0, tk.END))
            if subject_id in items:
                self.subject_listbox.selection_clear(0, tk.END)
                self.subject_listbox.selection_set(items.index(subject_id))
                self.load_subject_to_form(subject_id)
        
        ttk.Button(dialog, text="Create", command=create).pack(pady=10)
        dialog.bind('<Return>', lambda e: create())
    
    def delete_subject(self):
        """Delete selected subject"""
        if not self.current_subject:
            messagebox.showwarning("No Selection", "Please select a subject to delete!")
            return
        
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete '{self.current_subject}'?"):
            del self.exam_data[self.current_subject]
            self.current_subject = None
            self.refresh_subject_list()
            self.update_json_preview()
            self.clear_form()
    
    def save_current_subject(self):
        """Save current form data to the subject"""
        if not self.js_file_path:
            messagebox.showwarning("No File", "Please open a renderer.js file first!")
            return
        
        if not self.current_subject:
            messagebox.showwarning("No Selection", "Please select a subject first!")
            return
        
        new_id = self.id_entry.get().strip()
        if not new_id:
            messagebox.showwarning("Invalid Input", "Subject ID cannot be empty!")
            return
        
        # If ID changed, update the dictionary key
        if new_id != self.current_subject:
            if new_id in self.exam_data:
                messagebox.showwarning("Duplicate ID", "This subject ID already exists!")
                return
            self.exam_data[new_id] = self.exam_data.pop(self.current_subject)
            self.current_subject = new_id
        
        # Update data
        self.exam_data[self.current_subject] = {
            "id": self.id_entry.get().strip(),
            "name": self.name_entry.get().strip(),
            "description": self.desc_entry.get().strip(),
            "externalLink": self.link_entry.get().strip()
        }
        
        self.refresh_subject_list()
        self.update_json_preview()
        messagebox.showinfo("Success", "Subject saved! Don't forget to click 'Save to renderer.js'")
    
    def clear_form(self):
        """Clear all form fields"""
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.link_entry.delete(0, tk.END)
    
    def update_json_preview(self):
        """Update the JSON preview text"""
        self.json_text.delete('1.0', tk.END)
        if self.exam_data:
            json_str = json.dumps(self.exam_data, indent=4)
            self.json_text.insert('1.0', json_str)
        else:
            self.json_text.insert('1.0', '// No data loaded')

def main():
    root = tk.Tk()
    app = ExamDataJSEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
, '', exam_data_str, flags=re.MULTILINE)
        exam_data_str = re.sub(r'/\*.*?\*/', '', exam_data_str, flags=re.DOTALL)
        
        # Add quotes around unquoted property names
        # Match property names like: propertyName: or propertyName :
        exam_data_str = re.sub(r'(\n\s*)([a-zA-Z_$][a-zA-Z0-9_$]*)\s*:', r'\1"\2":', exam_data_str)
        
        # Convert single quotes to double quotes
        # But be careful not to convert quotes inside strings
        exam_data_str = self.convert_quotes(exam_data_str)
        
        # Remove trailing commas before closing braces/brackets
        exam_data_str = re.sub(r',(\s*[}\]])', r'\1', exam_data_str)
        
        try:
            self.exam_data = json.loads(exam_data_str)
            if not self.exam_data:
                # If empty, load default
                self.exam_data = {
                    "java": {
                        "id": "java",
                        "name": "OOP2",
                        "description": "Chapter 17 questions",
                        "externalLink": "https://ibdx.github.io/javaOOP17/"
                    }
                }
        except json.JSONDecodeError as e:
            messagebox.showerror("Parse Error", 
                               f"Could not parse EXAM_DATA object:\n{str(e)}\n\n"
                               "Loading default data instead.")
            # Load default data
            self.exam_data = {
                "java": {
                    "id": "java",
                    "name": "OOP2",
                    "description": "Chapter 17 questions",
                    "externalLink": "https://ibdx.github.io/javaOOP17/"
                }
            }
    
    def convert_quotes(self, js_str):
        """Convert single quotes to double quotes while preserving strings"""
        result = []
        in_string = False
        string_char = None
        escaped = False
        
        for i, char in enumerate(js_str):
            if escaped:
                result.append(char)
                escaped = False
                continue
            
            if char == '\\':
                escaped = True
                result.append(char)
                continue
            
            if char in ('"', "'"):
                if not in_string:
                    in_string = True
                    string_char = char
                    result.append('"')  # Always use double quotes
                elif char == string_char:
                    in_string = False
                    string_char = None
                    result.append('"')  # Always use double quotes
                else:
                    result.append(char)
            else:
                result.append(char)
        
        return ''.join(result)
    
    def save_to_js_file(self):
        """Save modified EXAM_DATA back to renderer.js"""
        if not self.js_file_path:
            messagebox.showwarning("No File", "Please open a renderer.js file first!")
            return
        
        if not self.js_file_content:
            messagebox.showerror("Error", "No file content loaded!")
            return
        
        # Convert exam_data to formatted JavaScript object
        js_object = self.dict_to_js_object(self.exam_data, indent=4)
        new_exam_data = f"const EXAM_DATA = {js_object};"
        
        # Replace EXAM_DATA in the file
        pattern = r'const\s+EXAM_DATA\s*=\s*\{[^;]*\};'
        
        if not re.search(pattern, self.js_file_content, re.DOTALL):
            messagebox.showerror("Error", "Could not find EXAM_DATA declaration in file!")
            return
        
        new_content = re.sub(pattern, new_exam_data, self.js_file_content, 
                            count=1, flags=re.DOTALL)
        
        try:
            # Create backup
            backup_path = self.js_file_path + '.backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(self.js_file_content)
            
            # Write new content
            with open(self.js_file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            self.js_file_content = new_content
            
            messagebox.showinfo("Success", 
                              f"File saved successfully!\n\n"
                              f"Backup created at:\n{backup_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
    
    def dict_to_js_object(self, obj, indent=4, level=0):
        """Convert Python dict to JavaScript object string"""
        if isinstance(obj, dict):
            if not obj:
                return "{}"
            
            indent_str = " " * (indent * level)
            inner_indent = " " * (indent * (level + 1))
            
            items = []
            for key, value in obj.items():
                js_value = self.dict_to_js_object(value, indent, level + 1)
                items.append(f'{inner_indent}{key}: {js_value}')
            
            return "{\n" + ",\n".join(items) + f"\n{indent_str}}}"
        
        elif isinstance(obj, str):
            # Escape quotes and special characters
            escaped = obj.replace('\\', '\\\\').replace('"', '\\"')
            return f'"{escaped}"'
        
        elif isinstance(obj, (int, float)):
            return str(obj)
        
        elif isinstance(obj, bool):
            return "true" if obj else "false"
        
        elif obj is None:
            return "null"
        
        elif isinstance(obj, list):
            if not obj:
                return "[]"
            items = [self.dict_to_js_object(item, indent, level + 1) for item in obj]
            return "[" + ", ".join(items) + "]"
        
        return str(obj)
    
    def reload_from_file(self):
        """Reload data from the currently open file"""
        if not self.js_file_path:
            messagebox.showwarning("No File", "No file is currently open!")
            return
        
        try:
            with open(self.js_file_path, 'r', encoding='utf-8') as f:
                self.js_file_content = f.read()
            
            self.extract_exam_data()
            self.refresh_subject_list()
            self.update_json_preview()
            self.clear_form()
            
            messagebox.showinfo("Success", "Data reloaded from file!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reload file:\n{str(e)}")
    
    def refresh_subject_list(self):
        """Refresh the listbox with current subjects"""
        self.subject_listbox.delete(0, tk.END)
        for subject_id in sorted(self.exam_data.keys()):
            self.subject_listbox.insert(tk.END, subject_id)
    
    def on_subject_select(self, event):
        """Handle subject selection from listbox"""
        selection = self.subject_listbox.curselection()
        if not selection:
            return
        
        subject_id = self.subject_listbox.get(selection[0])
        self.current_subject = subject_id
        self.load_subject_to_form(subject_id)
    
    def load_subject_to_form(self, subject_id):
        """Load subject data into form fields"""
        if subject_id not in self.exam_data:
            return
        
        data = self.exam_data[subject_id]
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, data.get('id', ''))
        
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, data.get('name', ''))
        
        self.desc_entry.delete(0, tk.END)
        self.desc_entry.insert(0, data.get('description', ''))
        
        self.link_entry.delete(0, tk.END)
        self.link_entry.insert(0, data.get('externalLink', ''))
    
    def add_subject(self):
        """Add a new subject"""
        if not self.js_file_path:
            messagebox.showwarning("No File", "Please open a renderer.js file first!")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Subject")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Enter Subject ID:").pack(pady=10)
        id_entry = ttk.Entry(dialog, width=30)
        id_entry.pack(pady=5)
        id_entry.focus()
        
        def create():
            subject_id = id_entry.get().strip()
            if not subject_id:
                messagebox.showwarning("Invalid Input", "Subject ID cannot be empty!")
                return
            
            if subject_id in self.exam_data:
                messagebox.showwarning("Duplicate ID", "This subject ID already exists!")
                return
            
            self.exam_data[subject_id] = {
                "id": subject_id,
                "name": "",
                "description": "",
                "externalLink": ""
            }
            self.refresh_subject_list()
            self.update_json_preview()
            dialog.destroy()
            
            # Select the new subject
            items = list(self.subject_listbox.get(0, tk.END))
            if subject_id in items:
                self.subject_listbox.selection_clear(0, tk.END)
                self.subject_listbox.selection_set(items.index(subject_id))
                self.load_subject_to_form(subject_id)
        
        ttk.Button(dialog, text="Create", command=create).pack(pady=10)
        dialog.bind('<Return>', lambda e: create())
    
    def delete_subject(self):
        """Delete selected subject"""
        if not self.current_subject:
            messagebox.showwarning("No Selection", "Please select a subject to delete!")
            return
        
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete '{self.current_subject}'?"):
            del self.exam_data[self.current_subject]
            self.current_subject = None
            self.refresh_subject_list()
            self.update_json_preview()
            self.clear_form()
    
    def save_current_subject(self):
        """Save current form data to the subject"""
        if not self.js_file_path:
            messagebox.showwarning("No File", "Please open a renderer.js file first!")
            return
        
        if not self.current_subject:
            messagebox.showwarning("No Selection", "Please select a subject first!")
            return
        
        new_id = self.id_entry.get().strip()
        if not new_id:
            messagebox.showwarning("Invalid Input", "Subject ID cannot be empty!")
            return
        
        # If ID changed, update the dictionary key
        if new_id != self.current_subject:
            if new_id in self.exam_data:
                messagebox.showwarning("Duplicate ID", "This subject ID already exists!")
                return
            self.exam_data[new_id] = self.exam_data.pop(self.current_subject)
            self.current_subject = new_id
        
        # Update data
        self.exam_data[self.current_subject] = {
            "id": self.id_entry.get().strip(),
            "name": self.name_entry.get().strip(),
            "description": self.desc_entry.get().strip(),
            "externalLink": self.link_entry.get().strip()
        }
        
        self.refresh_subject_list()
        self.update_json_preview()
        messagebox.showinfo("Success", "Subject saved! Don't forget to click 'Save to renderer.js'")
    
    def clear_form(self):
        """Clear all form fields"""
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.link_entry.delete(0, tk.END)
    
    def update_json_preview(self):
        """Update the JSON preview text"""
        self.json_text.delete('1.0', tk.END)
        if self.exam_data:
            json_str = json.dumps(self.exam_data, indent=4)
            self.json_text.insert('1.0', json_str)
        else:
            self.json_text.insert('1.0', '// No data loaded')

def main():
    root = tk.Tk()
    app = ExamDataJSEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()