from database import MedicineDatabase
from reminder import MedicineReminder
from gui import MedicineReminderGUI

def main():
    """Main application entry point"""
    print("="*50)
    print("Medicine Reminder System Starting...")
    print("="*50)
    
    # Initialize database
    db = MedicineDatabase()
    
    # Initialize reminder system
    reminder = MedicineReminder(db)
    reminder.start()
    
    # Initialize and run GUI
    app = MedicineReminderGUI(db, reminder)
    app.run()
    
    # Cleanup on exit
    reminder.stop()
    print("\nApplication closed. Thank you!")

if __name__ == "__main__":
    main()
