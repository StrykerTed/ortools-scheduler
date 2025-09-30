# 3D Printing Platform Scheduler

<div align="center">
  <img src="assets/stryker_logo_cmyk.svg" height="60" alt="Stryker" style="filter: brightness(0);">
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="assets/digitalrnd-newcolor.svg" height="70" alt="Digital R&D">
</div>

<div align="center">
  <h2>�️ Medical Implant 3D Printing Scheduler</h2>
  <p><em>Optimizing 3D printing platform schedules for medical devices using Google OR-Tools</em></p>
</div>

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge)](https://www.python.org/)
[![OR-Tools](https://img.shields.io/badge/OR--Tools-9.14-green?style=for-the-badge)](https://developers.google.com/optimization)
[![NumPy](https://img.shields.io/badge/NumPy-2.3-red?style=for-the-badge)](https://numpy.org/)
[![Medical Manufacturing](https://img.shields.io/badge/Industry-Medical%20Manufacturing-orange?style=for-the-badge)](https://en.wikipedia.org/wiki/3D_printing)

</div>

---

## 🎯 Demo Results

**Live Demo Performance** (with 70 medical cases across 5 platforms):

- **✅ 98.6% On-Time Delivery Rate** (69 of 70 cases delivered before surgery dates)
- **⚡ Ultra-Fast Solving** - Optimal solutions found in ~0.01 seconds
- **🔧 Efficient Resource Usage** - 5 of 50 printers utilized (10% utilization for this workload)
- **🏥 Complete Medical Coverage** - Hip, shoulder, skull, spinal, and facial reconstruction cases
- **📊 Priority Handling** - Emergency cases (1-3 day shipping) vs Standard (7-14 days)
- **🗓️ Smart Scheduling** - 16-hour platform cycles with 2-hour turnaround optimization

<div align="center">

![Performance](https://img.shields.io/badge/Delivery%20Rate-98.6%25-brightgreen?style=for-the-badge)
![Speed](https://img.shields.io/badge/Solve%20Time-0.01s-blue?style=for-the-badge)
![Cases](https://img.shields.io/badge/Demo%20Cases-70-orange?style=for-the-badge)
![Platforms](https://img.shields.io/badge/Platforms-5-purple?style=for-the-badge)

</div>

## 🚀 Features

**3D Printing Platform Scheduler** optimizes the production of medical implants and devices across multiple 3D printing platforms:

- **�️ Platform Scheduling** - Schedule ~14 cases per platform across 50 available printers
- **🏥 Medical Case Management** - Handle hip, shoulder, skull replacements with patient tracking
- **📅 Due Date Optimization** - Ensure timely delivery before surgery dates
- **⚡ High-Performance Solvers** - CP-SAT solver for complex manufacturing constraints
- **� Turnaround Time Management** - Account for platform refresh and engineer preparation time
- **📊 Resource Utilization** - Optimize 50 printer capacity with 16-hour platform cycles
- **🎯 Real-time Scheduling** - Dynamic adjustments for urgent cases and priority changes
- **� Production Analytics** - Track platform efficiency and delivery performance

<div align="center">

![3D Printing](https://img.shields.io/badge/3D-Printing-success?style=for-the-badge&logo=printer)
![Medical Devices](https://img.shields.io/badge/Medical-Devices-success?style=for-the-badge&logo=medical)
![Platform Scheduling](https://img.shields.io/badge/Platform-Scheduling-success?style=for-the-badge&logo=calendar)
![Due Date Management](https://img.shields.io/badge/Due%20Date-Management-success?style=for-the-badge&logo=clock)
![Resource Optimization](https://img.shields.io/badge/50%20Printers-Optimization-success?style=for-the-badge&logo=factory)

</div>

## 📦 Installation

1. **Clone or navigate to the project directory**

```bash
cd ortools-scheduler
```

2. **Create a virtual environment (recommended)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

## 🎯 Quick Start

### 🏃‍♂️ Run the Complete Demo

```bash
# Generate realistic medical case data (70 cases)
python3 src/demo_data.py

# Run the platform scheduler with visualization
python3 src/scheduler.py
```

**Expected Output:**
```
🎯 Scheduling completed successfully!
   - 5 platforms scheduled
   - 5 printers utilized  
   - 10.0% printer utilization
   - 98.6% on-time delivery rate
```

### 🧑‍💻 Custom Scheduling Example

```python
from src.scheduler import PlatformScheduler

# Create scheduler for 50 printers
scheduler = PlatformScheduler()

# Load your medical cases
cases = scheduler.load_cases_from_csv("your_cases.csv")

# Schedule platforms with constraints
solution = scheduler.schedule_platforms(cases, time_limit=60)

# Display results with Gantt chart
scheduler.display_schedule_summary(solution)
scheduler.display_gantt_chart(solution)
scheduler.export_detailed_schedule(solution)
```

## 📋 Medical Device Scheduling Scenarios

This 3D printing scheduler handles various medical manufacturing scenarios:

### 🦴 **Orthopedic Implants**

- Hip replacements with custom geometries
- Shoulder implants with patient-specific sizing
- Knee components with precise tolerances

### 🧠 **Cranial/Maxillofacial Devices**

- Skull plates and cranial implants
- Facial reconstruction components
- Custom surgical guides

### � **Platform Optimization**

- 14 cases per platform configuration
- 16-hour printing cycles per platform
- Turnaround time for platform preparation

### ⏰ **Due Date Management**

- Surgery date constraints
- Shipping time calculations
- Priority case handling for urgent surgeries

## 🔧 Core Components

### Platform Scheduler Engine

- **CP-SAT Solver**: Google's constraint programming solver optimized for manufacturing
- **Platform Builder**: Configure 14-case platforms with medical device constraints
- **Schedule Optimizer**: Balance due dates, printer availability, and turnaround times

### Medical Device Constraints

- **Due Date Constraints**: Surgery dates and shipping lead times (soft constraints with penalties)
- **Platform Constraints**: Exactly 14 cases per platform, 16-hour print cycles
- **Printer Constraints**: 50 printer capacity with no overlapping assignments
- **Turnaround Constraints**: 2-hour engineer preparation time between platforms
- **Non-Overlap Constraints**: Platforms on same printer cannot overlap in time

### Optimization Objectives

- **Primary**: Minimize maximum completion time (makespan)
- **Secondary**: Minimize weighted tardiness for priority cases
- **Tertiary**: Minimize due date violations with penalty weights
  - Emergency cases: 1000x penalty weight
  - Urgent cases: 100x penalty weight  
  - Standard cases: 10x penalty weight

## 📊 Dependencies

- **[OR-Tools](https://developers.google.com/optimization)** `9.14.6206` - Google's optimization tools
- **[NumPy](https://numpy.org/)** `2.3.3` - Numerical computing library
- **[Pandas](https://pandas.pydata.org/)** `2.3.3` - Data manipulation and analysis
- **[Protobuf](https://developers.google.com/protocol-buffers)** `6.31.1` - Protocol buffer support

## 🚀 Usage Examples

### Example 1: Generate and Schedule Medical Cases

```python
from src.demo_data import MedicalCaseDataGenerator
from src.scheduler import PlatformScheduler

# Generate realistic medical case data
generator = MedicalCaseDataGenerator()
cases = generator.generate_multiple_platforms(num_platforms=5, cases_per_platform=14)

# Export for review
generator.export_to_csv(cases, "my_medical_cases.csv")

# Schedule the cases
scheduler = PlatformScheduler()
solution = scheduler.schedule_platforms(cases, time_limit=60)

# Results: 98.6% on-time delivery, 0.01s solve time
```

### Example 2: Priority Emergency Case Handling

```python
# Define emergency cases with tight deadlines
emergency_cases = [
    {"case_id": "EMRG001", "patient_name": "John Doe", "device_type": "skull_plate", 
     "priority": "emergency", "surgery_date": "2025-10-05", "shipping_days": 1},
    {"case_id": "EMRG002", "patient_name": "Jane Smith", "device_type": "hip_replacement", 
     "priority": "emergency", "surgery_date": "2025-10-06", "shipping_days": 2}
]

# Scheduler automatically prioritizes emergency cases
scheduler = PlatformScheduler()
solution = scheduler.schedule_platforms(emergency_cases + standard_cases)

# Emergency cases get earliest platform assignments
```

### Example 3: Advanced Analytics and Visualization

```python
# Complete scheduling workflow with full analytics
scheduler = PlatformScheduler({
    "total_printers": 50,
    "cases_per_platform": 14, 
    "platform_duration_hours": 16,
    "turnaround_hours": 2
})

cases = scheduler.load_cases_from_csv("demo_medical_cases.csv")
solution = scheduler.schedule_platforms(cases)

# Multiple visualization options
scheduler.display_schedule_summary(solution)      # Text summary
scheduler.display_gantt_chart(solution)          # Visual timeline  
detailed_df = scheduler.export_detailed_schedule(solution)  # CSV analytics

# Key metrics automatically calculated:
# - 98.6% on-time delivery rate
# - 10% printer utilization (5 of 50 printers)
# - Emergency case prioritization working
```

## 📈 Manufacturing Performance Metrics

The platform provides comprehensive metrics for 3D printing production evaluation:

- **On-Time Delivery Rate**: Percentage of cases delivered before surgery dates
- **Printer Utilization**: Usage efficiency across all 50 printers
- **Platform Efficiency**: Average cases per platform (target: 14)
- **Turnaround Time**: Average time between platform completions
- **Emergency Response**: Time to schedule urgent surgical cases
- **Manufacturing Throughput**: Cases completed per day/week

## 🔬 Advanced Features

### Custom Medical Device Constraints

```python
# Add surgery date constraints with shipping buffer
scheduler.add_shipping_constraint(shipping_days=3)

# Priority handling for emergency cases
scheduler.add_priority_constraint(emergency_cases, max_delay_hours=6)
```

### Multi-Objective Platform Optimization

```python
# Balance delivery performance and printer utilization
objectives = [
    {"type": "minimize_late_deliveries", "weight": 0.7},
    {"type": "maximize_printer_utilization", "weight": 0.3}
]
scheduler.set_objectives(objectives)
```

### Production Visualization

```python
# Generate platform Gantt charts and delivery schedules
scheduler.visualize_platforms(solution, chart_type="gantt")
scheduler.export_delivery_schedule(solution, format="csv")
scheduler.generate_printer_utilization_report(solution)
```

## 📋 Demo Data Setup

The demo generates realistic medical case scenarios with the following specifications:

### Sample Case Data Structure

```python
# Actual demo data format generated by MedicalCaseDataGenerator
sample_cases = [
    {
        "case_id": "HIP001",
        "patient_name": "John Smith", 
        "device_type": "hip_replacement",
        "priority": "standard",
        "surgery_date": "2025-10-20",
        "due_date": "2025-10-10",      # 10 days before surgery
        "shipping_days": 10,
        "platform_time_hours": 16,
        "notes": "Standard hip replacement case",
        "suggested_platform": "Platform_01"
    }
    # ... 69 more realistic cases
]
```

### Device Types Generated

- **hip_replacement, shoulder_implant, knee_component** - Orthopedic devices
- **skull_plate, facial_reconstruction, orbital_implant** - Cranial/maxillofacial 
- **spinal_implant, jaw_reconstruction, custom_prosthetic** - Specialized devices

### Priority Distribution (Realistic Healthcare Ratios)

- **Emergency (5%)**: 1-3 day shipping, highest priority scheduling
- **Urgent (15%)**: 3-7 day shipping, elevated priority
- **Standard (80%)**: 7-14 day shipping, normal scheduling

### Manufacturing Configuration

```python
manufacturing_config = {
    "total_printers": 50,
    "cases_per_platform": 14,
    "platform_duration_hours": 16,
    "turnaround_hours": 2,
    "working_hours_per_day": 24,  # Continuous operation
    "shipping_lead_days": 10,     # Default before surgery
    "planning_horizon_days": 90   # 3-month scheduling window
}
```

## 🛠️ Development

### Project Structure

```
ortools-scheduler/
├── src/
│   ├── scheduler.py          # Main PlatformScheduler implementation
│   └── demo_data.py          # Medical case data generator
├── assets/                   # Company logos and branding
├── requirements.txt          # Python dependencies
├── README.md                # This comprehensive guide
└── .gitignore               # Excludes demo outputs and temp files
```

**Generated Demo Files** (excluded from git):
- `demo_medical_cases.csv` - 70 realistic medical cases
- `scheduling_solution.json` - Complete solution with assignments
- `detailed_schedule.csv` - Case-by-case delivery analysis

### Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your scheduling algorithm
4. Add tests and documentation
5. Submit a pull request

## 📚 Learning Resources

- [Google OR-Tools Documentation](https://developers.google.com/optimization)
- [Constraint Programming Guide](https://developers.google.com/optimization/cp)
- [Scheduling Optimization Techniques](<https://en.wikipedia.org/wiki/Scheduling_(computing)>)
- [Operations Research Methods](https://www.informs.org/)

## 🏷️ Medical Manufacturing Use Cases

This 3D printing platform scheduler is designed for:

- **🏥 Hospital Systems**: Coordinating implant delivery with surgical schedules
- **🏭 Medical Device Manufacturing**: Optimizing production across multiple printer farms
- **⚙️ Custom Implant Production**: Patient-specific device manufacturing workflows
- **🚑 Emergency Surgery Support**: Rapid scheduling for urgent medical cases
- **📈 Production Planning**: Long-term capacity planning and resource allocation
- **🔄 Supply Chain Integration**: Coordinating with material suppliers and shipping logistics

### ✅ **Proven Results in Demo:**
- **70 Medical Cases Scheduled** across hip, shoulder, skull, spinal, and facial devices
- **5 Platform Optimization** with perfect printer assignment
- **Emergency Priority Handling** with 1-3 day shipping for urgent cases
- **98.6% On-Time Delivery** meeting surgical schedule requirements
- **Real-Time Gantt Visualization** for production planning
- **Detailed Analytics Export** for performance tracking

## 📄 License

This project is for educational and demonstration purposes. Please check with your organization's policies for commercial use.

---

<div align="center">
  <p><strong>Built with ❤️ using Google OR-Tools and Python</strong></p>
  <p><em>Optimizing schedules, one constraint at a time</em></p>
</div>
