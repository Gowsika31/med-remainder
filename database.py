import json
import os
from datetime import datetime

class MedicineDatabase:
    def __init__(self, filename='medicines.json'):
        self.filename = filename
        self.medicines = self.load_medicines()
    
    def load_medicines(self):
        """Load medicines from JSON file"""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return []
    
    def save_medicines(self):
        """Save medicines to JSON file"""
        with open(self.filename, 'w') as f:
            json.dump(self.medicines, f, indent=4)
    
    def add_medicine(self, name, dosage, times, notes=''):
        """Add new medicine"""
        medicine = {
            'id': len(self.medicines) + 1,
            'name': name,
            'dosage': dosage,
            'times': times,
            'notes': notes,
            'active': True,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.medicines.append(medicine)
        self.save_medicines()
        return True
    
    def get_all_medicines(self):
        """Get all active medicines"""
        return [m for m in self.medicines if m['active']]
    
    def delete_medicine(self, medicine_id):
        """Mark medicine as inactive"""
        for medicine in self.medicines:
            if medicine['id'] == medicine_id:
                medicine['active'] = False
                self.save_medicines()
                return True
        return False
