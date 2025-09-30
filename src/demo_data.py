"""
Demo data generator for 3D printing platform scheduling.
Generates realistic medical case data for testing the scheduler.
"""
import random
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any

class MedicalCaseDataGenerator:
    """Generate realistic medical case data for 3D printing scheduling."""
    
    def __init__(self):
        self.device_types = [
            "hip_replacement", "shoulder_implant", "knee_component", 
            "skull_plate", "facial_reconstruction", "spinal_implant",
            "jaw_reconstruction", "orbital_implant", "custom_prosthetic"
        ]
        
        self.priorities = ["emergency", "urgent", "standard"]
        self.priority_weights = [0.05, 0.15, 0.80]  # 5% emergency, 15% urgent, 80% standard
        
        # Sample patient names for demo
        self.first_names = [
            "John", "Jane", "Michael", "Sarah", "David", "Emily", "James", "Lisa",
            "Robert", "Maria", "William", "Jennifer", "Richard", "Linda", "Charles",
            "Patricia", "Christopher", "Barbara", "Daniel", "Elizabeth", "Matthew",
            "Susan", "Anthony", "Jessica", "Mark", "Nancy", "Donald", "Dorothy",
            "Steven", "Karen", "Paul", "Helen", "Andrew", "Sandra", "Joshua", "Donna"
        ]
        
        self.last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
            "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
            "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
            "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
            "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King"
        ]
    
    def generate_patient_name(self) -> str:
        """Generate a random patient name."""
        first = random.choice(self.first_names)
        last = random.choice(self.last_names)
        return f"{first} {last}"
    
    def generate_case_id(self, device_type: str, case_number: int) -> str:
        """Generate a case ID based on device type and number."""
        device_code = {
            "hip_replacement": "HIP",
            "shoulder_implant": "SHO", 
            "knee_component": "KNE",
            "skull_plate": "SKL",
            "facial_reconstruction": "FAC",
            "spinal_implant": "SPI",
            "jaw_reconstruction": "JAW",
            "orbital_implant": "ORB",
            "custom_prosthetic": "CUS"
        }
        code = device_code.get(device_type, "DEV")
        return f"{code}{case_number:03d}"
    
    def calculate_due_date(self, surgery_date: datetime, shipping_days: int = 10) -> datetime:
        """Calculate due date based on surgery date and shipping lead time."""
        return surgery_date - timedelta(days=shipping_days)
    
    def generate_single_case(self, case_number: int, base_date: datetime = None) -> Dict[str, Any]:
        """Generate a single medical case with realistic data."""
        if base_date is None:
            base_date = datetime.now()
        
        # Generate surgery date 5-90 days from base date (more future-focused)
        days_ahead = random.randint(5, 90)
        surgery_date = base_date + timedelta(days=days_ahead)
        
        # Select device type and priority
        device_type = random.choice(self.device_types)
        priority = random.choices(self.priorities, weights=self.priority_weights)[0]
        
        # Adjust shipping lead time based on priority
        if priority == "emergency":
            shipping_days = random.randint(1, 3)  # Rush delivery
        elif priority == "urgent":
            shipping_days = random.randint(3, 7)   # Fast delivery
        else:
            shipping_days = random.randint(7, 14)  # Standard delivery
        
        due_date = self.calculate_due_date(surgery_date, shipping_days)
        
        case = {
            "case_id": self.generate_case_id(device_type, case_number),
            "patient_name": self.generate_patient_name(),
            "device_type": device_type,
            "priority": priority,
            "surgery_date": surgery_date.strftime("%Y-%m-%d"),
            "due_date": due_date.strftime("%Y-%m-%d"),
            "shipping_days": shipping_days,
            "platform_time_hours": 16,  # Standard platform time
            "notes": f"{priority.capitalize()} {device_type.replace('_', ' ')} case"
        }
        
        return case
    
    def generate_case_batch(self, num_cases: int, base_date: datetime = None) -> List[Dict[str, Any]]:
        """Generate a batch of medical cases."""
        cases = []
        for i in range(1, num_cases + 1):
            case = self.generate_single_case(i, base_date)
            cases.append(case)
        return cases
    
    def generate_multiple_platforms(self, num_platforms: int, cases_per_platform: int = 14) -> List[Dict[str, Any]]:
        """Generate cases for multiple platforms."""
        all_cases = []
        case_counter = 1
        
        for platform in range(num_platforms):
            base_date = datetime.now() + timedelta(days=platform * 2)  # Stagger platform start dates
            platform_cases = []
            
            for case in range(cases_per_platform):
                case_data = self.generate_single_case(case_counter, base_date)
                case_data["suggested_platform"] = f"Platform_{platform + 1:02d}"
                platform_cases.append(case_data)
                case_counter += 1
            
            all_cases.extend(platform_cases)
        
        return all_cases
    
    def export_to_csv(self, cases: List[Dict[str, Any]], filename: str = "demo_medical_cases.csv"):
        """Export cases to CSV file."""
        df = pd.DataFrame(cases)
        df.to_csv(filename, index=False)
        print(f"Exported {len(cases)} cases to {filename}")
        return df
    
    def get_sample_printer_config(self, num_printers: int = 50) -> Dict[str, Any]:
        """Get sample printer configuration."""
        # Generate some fake maintenance windows
        maintenance_windows = []
        base_date = datetime.now()
        for week in range(4):  # Next 4 weeks
            maintenance_date = base_date + timedelta(weeks=week, days=6)  # Every Sunday
            start_time = maintenance_date.replace(hour=6, minute=0)
            end_time = start_time + timedelta(hours=6)  # 6-hour maintenance window
            maintenance_windows.append({
                "start": start_time.strftime("%Y-%m-%d %H:%M"),
                "end": end_time.strftime("%Y-%m-%d %H:%M"),
                "printers_affected": random.randint(1, 5)  # 1-5 printers down
            })
        
        return {
            "total_printers": num_printers,
            "cases_per_platform": 14,
            "platform_duration_hours": 16,
            "turnaround_hours": 2,
            "working_schedule": "24/7",
            "maintenance_windows": maintenance_windows,
            "printer_efficiency": 0.95,  # 95% uptime
        }

def main():
    """Demo script to generate sample data."""
    generator = MedicalCaseDataGenerator()
    
    # Generate sample cases for 5 platforms (70 cases total)
    print("Generating demo medical case data...")
    cases = generator.generate_multiple_platforms(num_platforms=5, cases_per_platform=14)
    
    # Export to CSV
    df = generator.export_to_csv(cases, "demo_medical_cases.csv")
    
    # Display summary
    print(f"\nGenerated {len(cases)} medical cases:")
    print(f"- Device types: {df['device_type'].value_counts().to_dict()}")
    print(f"- Priorities: {df['priority'].value_counts().to_dict()}")
    print(f"- Date range: {df['surgery_date'].min()} to {df['surgery_date'].max()}")
    
    # Get printer configuration
    printer_config = generator.get_sample_printer_config()
    print(f"\nPrinter Configuration:")
    print(f"- Total printers: {printer_config['total_printers']}")
    print(f"- Platform duration: {printer_config['platform_duration_hours']} hours")
    print(f"- Turnaround time: {printer_config['turnaround_hours']} hours")
    print(f"- Maintenance windows: {len(printer_config['maintenance_windows'])} scheduled")

if __name__ == "__main__":
    main()