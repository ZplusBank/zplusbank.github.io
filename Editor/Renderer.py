import tkinter as tk
from tkinter import ttk, messagebox
import json
import re
import os
from datetime import datetime
import shutil

class SectionsEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Sections.js Editor")
        self.root.geometry("1000x600")
        
        self.file_path = "../engine/sections.js"
        self.data = {}
        self.selected_id = None
        
        # Create main container
        main_container = ttk.Frame(root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=1)
        
        # Top button frame
        button_frame = ttk.Frame(main_container)
        button_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(button_frame, text="➕ Add New", command=self.add_section, 
                  width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="🗑️ Delete", command=self.delete_section,
                  width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="💾 Save All", command=self.save_all,
                  width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="🔄 Reload", command=self.reload_data,
                  width=12).pack(side=tk.LEFT, padx=2)
        
        self.status_label = ttk.Label(button_frame, text="Ready", foreground="green")
        self.status_label.pack(side=tk.RIGHT, padx=5)
        
        # Create PanedWindow for table and editor
        paned = ttk.PanedWindow(main_container, orient=tk.HORIZONTAL)
        paned.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Left side - Table
        table_frame = ttk.Frame(paned)
        paned.add(table_frame, weight=1)
        
        # Table
        table_scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        table_scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        
        self.tree = ttk.Treeview(table_frame, 
                                 columns=("ID", "Name", "Description", "Link"),
                                 show="headings",
                                 yscrollcommand=table_scroll_y.set,
                                 xscrollcommand=table_scroll_x.set,
                                 selectmode="browse")
        
        table_scroll_y.config(command=self.tree.yview)
        table_scroll_x.config(command=self.tree.xview)
        
        # Configure columns
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Link", text="External Link")
        
        self.tree.column("ID", width=80, minwidth=80)
        self.tree.column("Name", width=150, minwidth=100)
        self.tree.column("Description", width=200, minwidth=150)
        self.tree.column("Link", width=250, minwidth=200)
        
        # Grid layout for table
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        table_scroll_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        table_scroll_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        # Right side - Editor
        editor_frame = ttk.LabelFrame(paned, text="Edit Section", padding="10")
        paned.add(editor_frame, weight=1)
        
        # Editor fields
        ttk.Label(editor_frame, text="ID:", font=("", 10, "bold")).grid(
            row=0, column=0, sticky=tk.W, pady=8)
        self.id_var = tk.StringVar()
        self.id_entry = ttk.Entry(editor_frame, textvariable=self.id_var, width=40)
        self.id_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=8, padx=5)
        
        ttk.Label(editor_frame, text="Name:", font=("", 10, "bold")).grid(
            row=1, column=0, sticky=tk.W, pady=8)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(editor_frame, textvariable=self.name_var, width=40)
        self.name_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=8, padx=5)
        
        ttk.Label(editor_frame, text="Description:", font=("", 10, "bold")).grid(
            row=2, column=0, sticky=tk.W, pady=8)
        self.desc_var = tk.StringVar()
        self.desc_entry = ttk.Entry(editor_frame, textvariable=self.desc_var, width=40)
        self.desc_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=8, padx=5)
        
        ttk.Label(editor_frame, text="External Link:", font=("", 10, "bold")).grid(
            row=3, column=0, sticky=tk.W, pady=8)
        self.link_var = tk.StringVar()
        self.link_entry = ttk.Entry(editor_frame, textvariable=self.link_var, width=40)
        self.link_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=8, padx=5)
        
        # Update button
        btn_frame = ttk.Frame(editor_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        self.update_btn = ttk.Button(btn_frame, text="✓ Update Section", 
                                     command=self.update_section, 
                                     state="disabled",
                                     width=20)
        self.update_btn.pack()
        
        ttk.Label(editor_frame, text="Select a section from the table to edit", 
                 foreground="gray", font=("", 9, "italic")).grid(
            row=5, column=0, columnspan=2, pady=10)
        
        editor_frame.columnconfigure(1, weight=1)
        
        # Load initial data
        self.load_data()
        
    def parse_js_file(self, content):
        """Parse the JavaScript file and extract EXAM_DATA object"""
        match = re.search(r'export\s+const\s+EXAM_DATA\s*=\s*({[\s\S]*?}\s*);', content, re.MULTILINE)
        if match:
            js_object = match.group(1)
            js_object = re.sub(r'([{,]\s*)(\w+)(\s*):', r'\1"\2"\3:', js_object)
            js_object = re.sub(r"'", '"', js_object)
            js_object = re.sub(r',(\s*[}\]])', r'\1', js_object)
            try:
                return json.loads(js_object)
            except json.JSONDecodeError as e:
                messagebox.showerror("Parse Error", f"Error parsing JS object: {e}")
                return {}
        else:
            messagebox.showerror("Parse Error", "Could not find EXAM_DATA in the file")
        return {}
    
    def load_data(self):
        """Load data from sections.js file"""
        try:
            if not os.path.exists(self.file_path):
                messagebox.showerror("Error", f"File not found: {self.file_path}")
                return
            
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.data = self.parse_js_file(content)
            self.refresh_table()
            self.update_status("Data loaded successfully", "green")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading file: {e}")
    
    def refresh_table(self):
        """Refresh the table with current data"""
        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Populate table
        for section_id, section_data in self.data.items():
            self.tree.insert("", tk.END, iid=section_id, values=(
                section_data.get('id', ''),
                section_data.get('name', ''),
                section_data.get('description', ''),
                section_data.get('externalLink', '')
            ))
    
    def on_select(self, event):
        """Handle table row selection"""
        selection = self.tree.selection()
        if selection:
            self.selected_id = selection[0]
            section_data = self.data[self.selected_id]
            
            # Populate editor fields
            self.id_var.set(section_data.get('id', ''))
            self.name_var.set(section_data.get('name', ''))
            self.desc_var.set(section_data.get('description', ''))
            self.link_var.set(section_data.get('externalLink', ''))
            
            self.update_btn.config(state="normal")
        else:
            self.selected_id = None
            self.update_btn.config(state="disabled")
    
    def update_section(self):
        """Update the selected section with editor values"""
        if not self.selected_id:
            messagebox.showwarning("Warning", "No section selected!")
            return
        
        new_id = self.id_var.get().strip()
        if not new_id:
            messagebox.showwarning("Warning", "ID cannot be empty!")
            return
        
        # Check if ID changed and new ID already exists
        if new_id != self.selected_id and new_id in self.data:
            messagebox.showwarning("Warning", "A section with this ID already exists!")
            return
        
        # Update data
        section_data = {
            'id': new_id,
            'name': self.name_var.get().strip(),
            'description': self.desc_var.get().strip(),
            'externalLink': self.link_var.get().strip()
        }
        
        # If ID changed, remove old entry
        if new_id != self.selected_id:
            del self.data[self.selected_id]
        
        self.data[new_id] = section_data
        self.selected_id = new_id
        
        self.refresh_table()
        self.tree.selection_set(new_id)
        self.update_status(f"Updated: {new_id}", "blue")
    
    def add_section(self):
        """Add a new section"""
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Section")
        dialog.geometry("450x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Section ID:", font=("", 10, "bold")).grid(
            row=0, column=0, sticky=tk.W, pady=10)
        id_entry = ttk.Entry(frame, width=35)
        id_entry.grid(row=0, column=1, pady=10, padx=10)
        id_entry.focus()
        
        ttk.Label(frame, text="Name:", font=("", 10, "bold")).grid(
            row=1, column=0, sticky=tk.W, pady=10)
        name_entry = ttk.Entry(frame, width=35)
        name_entry.grid(row=1, column=1, pady=10, padx=10)
        
        def create_section():
            section_id = id_entry.get().strip()
            section_name = name_entry.get().strip()
            
            if not section_id:
                messagebox.showwarning("Warning", "Section ID is required!")
                return
            
            if section_id in self.data:
                messagebox.showwarning("Warning", "Section ID already exists!")
                return
            
            self.data[section_id] = {
                'id': section_id,
                'name': section_name or section_id,
                'description': '',
                'externalLink': ''
            }
            
            self.refresh_table()
            self.tree.selection_set(section_id)
            self.update_status(f"Added: {section_id}", "green")
            dialog.destroy()
        
        ttk.Button(frame, text="✓ Create Section", command=create_section,
                  width=20).grid(row=2, column=0, columnspan=2, pady=20)
        
        # Bind Enter key
        dialog.bind('<Return>', lambda e: create_section())
    
    def delete_section(self):
        """Delete the selected section"""
        if not self.selected_id:
            messagebox.showwarning("Warning", "No section selected!")
            return
        
        if messagebox.askyesno("Delete", f"Delete section '{self.selected_id}'?"):
            del self.data[self.selected_id]
            self.selected_id = None
            
            # Clear editor
            self.id_var.set('')
            self.name_var.set('')
            self.desc_var.set('')
            self.link_var.set('')
            self.update_btn.config(state="disabled")
            
            self.refresh_table()
            self.update_status("Section deleted", "orange")
    
    def save_all(self):
        """Save all changes back to the file"""
        try:
            if not self.data:
                messagebox.showwarning("Warning", "No data to save!")
                return
            
            # Create backup first
            self.create_backup()
            
            # Convert to JavaScript format
            js_content = "export const EXAM_DATA = "
            js_content += json.dumps(self.data, indent=4)
            js_content += ";\n"
            
            # Write to file
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(js_content)
            
            self.update_status("✓ Saved successfully!", "green")
            messagebox.showinfo("Success", "All changes saved to file!")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving file: {e}")
    
    def reload_data(self):
        """Reload data from file"""
        if messagebox.askyesno("Reload", "Reload from file? Unsaved changes will be lost."):
            self.load_data()
            # Clear selection
            self.selected_id = None
            self.id_var.set('')
            self.name_var.set('')
            self.desc_var.set('')
            self.link_var.set('')
            self.update_btn.config(state="disabled")
    
    def create_backup(self):
        """Create a backup of the current file"""
        try:
            if os.path.exists(self.file_path):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = f"{self.file_path}.backup_{timestamp}"
                shutil.copy2(self.file_path, backup_path)
                print(f"Backup created: {backup_path}")
        except Exception as e:
            messagebox.showwarning("Backup Warning", f"Could not create backup: {e}")
    
    def update_status(self, message, color="green"):
        """Update status label"""
        self.status_label.config(text=message, foreground=color)
        self.root.after(3000, lambda: self.status_label.config(text="Ready", foreground="green"))

if __name__ == "__main__":
    root = tk.Tk()
    app = SectionsEditor(root)
    root.mainloop()