import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class MedicineReminderGUI:
    def __init__(self, database, reminder_system):
        self.database = database
        self.reminder = reminder_system
        
        self.root = tk.Tk()
        self.root.title("Medicine Reminder System - Accessible")
        self.root.geometry("950x650")
        self.root.configure(bg='#f0f0f0')
        
        self.setup_ui()
        self.refresh_medicine_list()
    
    def flash_screen(self):
        """Flash screen for deaf users"""
        original_bg = self.root.cget('bg')
        for _ in range(5):
            self.root.configure(bg='#ff0000')
            self.root.update()
            self.root.after(200)
            self.root.configure(bg='#ffffff')
            self.root.update()
            self.root.after(200)
        self.root.configure(bg=original_bg)
    
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_label = tk.Label(
            self.root,
            text="💊 Medicine Reminder System",
            font=('Arial', 20, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=15)
        
        # Accessibility Mode Selector
        mode_frame = tk.Frame(self.root, bg='#f0f0f0')
        mode_frame.pack(pady=5)
        
        tk.Label(
            mode_frame,
            text="Accessibility Mode:",
            font=('Arial', 11, 'bold'),
            bg='#f0f0f0'
        ).pack(side='left', padx=5)
        
        self.mode_var = tk.StringVar(value="normal")
        mode_options = [
            "Normal Mode",
            "Blind Mode (Voice)",
            "Deaf Mode (Visual Flash)",
            "Illiterate Mode (Sound + Voice)"
        ]
        
        mode_dropdown = ttk.Combobox(
            mode_frame,
            textvariable=self.mode_var,
            values=mode_options,
            state='readonly',
            width=30,
            font=('Arial', 10)
        )
        mode_dropdown.current(0)
        mode_dropdown.pack(side='left', padx=5)
        mode_dropdown.bind('<<ComboboxSelected>>', self.change_mode)
        
        # Input Frame
        input_frame = tk.LabelFrame(
            self.root,
            text="Add New Medicine",
            font=('Arial', 12, 'bold'),
            bg='#ecf0f1',
            padx=20,
            pady=15
        )
        input_frame.pack(padx=20, pady=10, fill='x')
        
        tk.Label(input_frame, text="Medicine Name:", bg='#ecf0f1').grid(row=0, column=0, sticky='w', pady=5)
        self.name_entry = tk.Entry(input_frame, width=30, font=('Arial', 10))
        self.name_entry.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(input_frame, text="Dosage:", bg='#ecf0f1').grid(row=0, column=2, sticky='w', pady=5)
        self.dosage_entry = tk.Entry(input_frame, width=20, font=('Arial', 10))
        self.dosage_entry.grid(row=0, column=3, pady=5, padx=10)
        
        tk.Label(input_frame, text="Times (HH:MM):", bg='#ecf0f1').grid(row=1, column=0, sticky='w', pady=5)
        self.times_entry = tk.Entry(input_frame, width=30, font=('Arial', 10))
        self.times_entry.grid(row=1, column=1, pady=5, padx=10)
        tk.Label(input_frame, text="(comma-separated: 08:00,14:00,20:00)", bg='#ecf0f1', font=('Arial', 8)).grid(row=1, column=2, columnspan=2, sticky='w')
        
        tk.Label(input_frame, text="Notes:", bg='#ecf0f1').grid(row=2, column=0, sticky='w', pady=5)
        self.notes_entry = tk.Entry(input_frame, width=50, font=('Arial', 10))
        self.notes_entry.grid(row=2, column=1, columnspan=3, pady=5, padx=10)
        
        add_btn = tk.Button(
            input_frame,
            text="➕ Add Medicine",
            command=self.add_medicine,
            bg='#27ae60',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=5,
            cursor='hand2'
        )
        add_btn.grid(row=3, column=0, columnspan=4, pady=10)
        
        # Medicine List Frame
        list_frame = tk.LabelFrame(
            self.root,
            text="Active Medicines",
            font=('Arial', 12, 'bold'),
            bg='#ecf0f1',
            padx=10,
            pady=10
        )
        list_frame.pack(padx=20, pady=10, fill='both', expand=True)
        
        columns = ('ID', 'Name', 'Dosage', 'Times', 'Notes')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=8)
        
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Medicine Name')
        self.tree.heading('Dosage', text='Dosage')
        self.tree.heading('Times', text='Reminder Times')
        self.tree.heading('Notes', text='Notes')
        
        self.tree.column('ID', width=50)
        self.tree.column('Name', width=150)
        self.tree.column('Dosage', width=100)
        self.tree.column('Times', width=200)
        self.tree.column('Notes', width=300)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Buttons Frame
        btn_frame = tk.Frame(self.root, bg='#f0f0f0')
        btn_frame.pack(pady=10)
        
        delete_btn = tk.Button(
            btn_frame,
            text="🗑️ Delete Selected",
            command=self.delete_medicine,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=5,
            cursor='hand2'
        )
        delete_btn.pack(side='left', padx=5)
        
        refresh_btn = tk.Button(
            btn_frame,
            text="🔄 Refresh",
            command=self.refresh_medicine_list,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=5,
            cursor='hand2'
        )
        refresh_btn.pack(side='left', padx=5)
        
        test_btn = tk.Button(
            btn_frame,
            text="🔔 Test Alert",
            command=self.test_alert,
            bg='#9b59b6',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=5,
            cursor='hand2'
        )
        test_btn.pack(side='left', padx=5)
    
    def change_mode(self, event=None):
        """Change accessibility mode"""
        mode_text = self.mode_var.get()
        
        if "Normal" in mode_text:
            self.reminder.set_mode("normal")
        elif "Blind" in mode_text:
            self.reminder.set_mode("blind")
        elif "Deaf" in mode_text:
            self.reminder.set_mode("deaf")
        elif "Illiterate" in mode_text:
            self.reminder.set_mode("illiterate")
        
        messagebox.showinfo("Mode Changed", f"Accessibility mode set to: {mode_text}")
    
    def test_alert(self):
        """Test current accessibility mode"""
        self.reminder.show_notification("Test Medicine", "100mg", "This is a test alert")
        
        if self.reminder.mode == "deaf":
            self.flash_screen()
    
    def add_medicine(self):
        """Add new medicine"""
        name = self.name_entry.get().strip()
        dosage = self.dosage_entry.get().strip()
        times_str = self.times_entry.get().strip()
        notes = self.notes_entry.get().strip()
        
        if not name or not dosage or not times_str:
            messagebox.showerror("Error", "Please fill in all required fields!")
            return
        
        times = [t.strip() for t in times_str.split(',')]
        
        for time_str in times:
            try:
                datetime.strptime(time_str, '%H:%M')
            except ValueError:
                messagebox.showerror("Error", f"Invalid time format: {time_str}\nUse HH:MM format (e.g., 08:00)")
                return
        
        self.database.add_medicine(name, dosage, times, notes)
        
        self.name_entry.delete(0, tk.END)
        self.dosage_entry.delete(0, tk.END)
        self.times_entry.delete(0, tk.END)
        self.notes_entry.delete(0, tk.END)
        
        self.refresh_medicine_list()
        self.reminder.restart()
        
        messagebox.showinfo("Success", f"Medicine '{name}' added successfully!")
    
    def delete_medicine(self):
        """Delete selected medicine"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a medicine to delete!")
            return
        
        item = self.tree.item(selected[0])
        medicine_id = int(item['values'][0])
        medicine_name = item['values'][1]
        
        confirm = messagebox.askyesno("Confirm Delete", f"Delete '{medicine_name}'?")
        if confirm:
            self.database.delete_medicine(medicine_id)
            self.refresh_medicine_list()
            self.reminder.restart()
            messagebox.showinfo("Success", f"Medicine '{medicine_name}' deleted!")
    
    def refresh_medicine_list(self):
        """Refresh the medicine list display"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        medicines = self.database.get_all_medicines()
        for med in medicines:
            times_str = ', '.join(med['times'])
            self.tree.insert('', 'end', values=(
                med['id'],
                med['name'],
                med['dosage'],
                times_str,
                med.get('notes', '')
            ))
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

