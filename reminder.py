import schedule
import time
from plyer import notification
from datetime import datetime
import threading
import pyttsx3
import winsound
import tkinter as tk

class MedicineReminder:
    def __init__(self, database):
        self.database = database
        self.running = False
        self.mode = "normal"
        
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.setProperty('volume', 1.0)
        except:
            self.tts_engine = None
            print("Warning: Text-to-speech not available")
    
    def set_mode(self, mode):
        """Set accessibility mode"""
        self.mode = mode
        print(f"Accessibility mode set to: {mode}")
    
    def speak(self, text):
        """Speak text aloud"""
        if self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except:
                print(f"Could not speak: {text}")
    
    def play_sound_alert(self):
        """Play beep sound"""
        try:
            for _ in range(3):
                winsound.Beep(1000, 500)
                time.sleep(0.2)
        except:
            print("Could not play sound alert")
    
    def show_flash_window(self, medicine_name, dosage):
        """Create full-screen flashing alert for deaf users"""
        flash_win = tk.Tk()
        flash_win.attributes('-fullscreen', True)
        flash_win.attributes('-topmost', True)
        
        label = tk.Label(
            flash_win,
            text=f"💊 MEDICINE TIME!\n\n{medicine_name}\n{dosage}\n\nPress any key to close",
            font=('Arial', 70, 'bold'),
            fg='white'
        )
        label.pack(expand=True, fill='both')
        
        flash_count = [0]
        colors = ['#FF0000', '#FFFFFF'] * 6
        
        def flash():
            if flash_count[0] < len(colors):
                color = colors[flash_count[0]]
                flash_win.configure(bg=color)
                label.configure(bg=color)
                flash_count[0] += 1
                flash_win.after(400, flash)
            else:
                flash_win.configure(bg='#FF0000')
                label.configure(bg='#FF0000')
        
        def close_window(event=None):
            flash_win.destroy()
        
        flash_win.bind('<Key>', close_window)
        flash_win.bind('<Button-1>', close_window)
        
        flash()
        
        # Auto close after 15 seconds
        flash_win.after(15000, flash_win.destroy)
        
        flash_win.mainloop()
    
    def show_notification(self, medicine_name, dosage, notes=''):
        """Display notification based on mode"""
        title = f"💊 Medicine Reminder"
        message = f"{medicine_name}\nDosage: {dosage}"
        if notes:
            message += f"\nNote: {notes}"
        
        if self.mode == "normal":
            notification.notify(
                title=title,
                message=message,
                app_name='Medicine Reminder',
                timeout=10
            )
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Reminder: {medicine_name}")
        
        elif self.mode == "blind":
            voice_message = f"Medicine reminder. Time to take {medicine_name}, {dosage}"
            if notes:
                voice_message += f". Note: {notes}"
            self.speak(voice_message)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Voice reminder: {medicine_name}")
        
        elif self.mode == "deaf":
            notification.notify(
                title=title,
                message=message,
                app_name='Medicine Reminder',
                timeout=20
            )
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Visual reminder: {medicine_name}")
            
            # Show full-screen flash in separate thread
            flash_thread = threading.Thread(
                target=self.show_flash_window,
                args=(medicine_name, dosage),
                daemon=True
            )
            flash_thread.start()
        
        elif self.mode == "illiterate":
            self.play_sound_alert()
            voice_message = f"Medicine time! Take {medicine_name}, {dosage}"
            self.speak(voice_message)
            notification.notify(
                title="💊 MEDICINE TIME!",
                message=f"{medicine_name} - {dosage}",
                app_name='Medicine Reminder',
                timeout=15
            )
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Sound + Voice: {medicine_name}")
    
    def schedule_medicine(self, medicine):
        """Schedule reminders"""
        for time_str in medicine['times']:
            schedule.every().day.at(time_str).do(
                self.show_notification,
                medicine['name'],
                medicine['dosage'],
                medicine.get('notes', '')
            )
            print(f"Scheduled: {medicine['name']} at {time_str}")
    
    def start(self):
        """Start reminder system"""
        self.running = True
        schedule.clear()
        
        medicines = self.database.get_all_medicines()
        for medicine in medicines:
            self.schedule_medicine(medicine)
        
        print(f"\n✅ Reminder system started with {len(medicines)} medicines")
        print(f"Current mode: {self.mode.upper()}")
        
        def run_schedule():
            while self.running:
                schedule.run_pending()
                time.sleep(1)
        
        self.thread = threading.Thread(target=run_schedule, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop reminder system"""
        self.running = False
        schedule.clear()
        print("Reminder system stopped")
    
    def restart(self):
        """Restart with updated schedule"""
        self.stop()
        time.sleep(1)
        self.start()


