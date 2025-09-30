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

### 3D Printing Platform Scheduling Example

```python
from src.scheduler import PlatformScheduler

# Create a new 3D printing scheduler
scheduler = PlatformScheduler(num_printers=50)

# Define medical cases for scheduling
cases = [
    {"case_id": "C001", "patient_name": "John Doe", "device_type": "hip_replacement", 
     "due_date": "2025-10-15", "platform_time": 16},
    {"case_id": "C002", "patient_name": "Jane Smith", "device_type": "shoulder_implant", 
     "due_date": "2025-10-12", "platform_time": 16}
]

# Schedule platforms with turnaround time
solution = scheduler.schedule_platforms(cases, turnaround_hours=2)

# Display optimized schedule
scheduler.display_gantt_chart(solution)
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

- **Due Date Constraints**: Surgery dates and shipping lead times
- **Platform Constraints**: 14 cases per platform, 16-hour print cycles
- **Printer Constraints**: 50 printer capacity with availability windows
- **Turnaround Constraints**: Engineer preparation time between platforms

### Optimization Objectives

- **On-Time Delivery**: Minimize late shipments for surgical procedures
- **Printer Utilization**: Maximize efficiency across 50 available printers
- **Platform Optimization**: Optimal case grouping for manufacturing efficiency
- **Emergency Handling**: Priority scheduling for urgent surgical cases

## 📊 Dependencies

- **[OR-Tools](https://developers.google.com/optimization)** `9.14.6206` - Google's optimization tools
- **[NumPy](https://numpy.org/)** `2.3.3` - Numerical computing library
- **[Pandas](https://pandas.pydata.org/)** `2.3.3` - Data manipulation and analysis
- **[Protobuf](https://developers.google.com/protocol-buffers)** `6.31.1` - Protocol buffer support

## 🚀 Usage Examples

### Example 1: Hip Replacement Platform Scheduling

```python
# Define hip replacement cases with due dates
hip_cases = [
    {"case_id": "HIP001", "patient_name": "Patient A", "due_date": "2025-10-20", "surgery_date": "2025-10-22"},
    {"case_id": "HIP002", "patient_name": "Patient B", "due_date": "2025-10-18", "surgery_date": "2025-10-20"},
    # ... up to 14 cases per platform
]

# Create and solve
scheduler = PlatformScheduler()
solution = scheduler.schedule_hip_platforms(hip_cases, num_printers=50)
```

### Example 2: Multi-Device Platform with Priorities

```python
# Define mixed device platform
mixed_cases = [
    {"case_id": "SKL001", "device_type": "skull_plate", "priority": "urgent", "due_date": "2025-10-10"},
    {"case_id": "SHO001", "device_type": "shoulder_implant", "priority": "standard", "due_date": "2025-10-25"},
    # ... additional cases
]

scheduler = PlatformScheduler()
solution = scheduler.schedule_mixed_platform(mixed_cases, turnaround_hours=2)
```

### Example 3: Printer Resource Optimization

```python
# Optimize across all 50 printers with maintenance windows
printer_schedule = {
    "available_printers": 50,
    "maintenance_windows": [("2025-10-15", "2025-10-16")],  # Printer downtime
    "platform_duration": 16,  # hours
    "turnaround_time": 2      # hours between platforms
}

scheduler = PlatformScheduler(printer_schedule)
solution = scheduler.optimize_printer_utilization(all_cases)
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

To get started with realistic scheduling scenarios:

### Sample Case Data Structure

```python
sample_cases = [
    {
        "case_id": "HIP001",
        "patient_name": "John Smith",
        "device_type": "hip_replacement",
        "due_date": "2025-10-20",
        "surgery_date": "2025-10-22",
        "priority": "standard",
        "shipping_days": 2
    },
    {
        "case_id": "SKL001", 
        "patient_name": "Jane Doe",
        "device_type": "skull_plate",
        "due_date": "2025-10-15",
        "surgery_date": "2025-10-17",
        "priority": "urgent",
        "shipping_days": 1
    }
    # ... up to 14 cases per platform
]
```

### Manufacturing Configuration

```python
manufacturing_config = {
    "total_printers": 50,
    "cases_per_platform": 14,
    "platform_duration_hours": 16,
    "turnaround_hours": 2,
    "working_hours_per_day": 24,  # Continuous operation
    "maintenance_schedule": ["Sunday 06:00-12:00"]  # Weekly maintenance
}
```

## 🛠️ Development

### Project Structure

```
ortools-scheduler/
├── src/
│   └── scheduler.py          # Main scheduler implementation
├── requirements.txt          # Python dependencies
├── README.md                # This file
└── examples/                # Usage examples (coming soon)
```

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

## ❓ Next Steps for Demo Development

To create a comprehensive demo, I'd like to clarify a few details:

1. **Shipping/Lead Time**: How many days before surgery should devices be delivered?
2. **Priority Levels**: Should we have multiple priority levels (emergency, urgent, standard)?
3. **Device Complexity**: Do different device types (hip vs skull) have different platform requirements?
4. **Maintenance Schedule**: When do the 50 printers require maintenance downtime?
5. **Work Schedule**: 24/7 operation or specific working hours?
6. **Case Grouping**: Any constraints on mixing different device types on the same platform?

With these details, I can create realistic demo data and implement the core scheduling algorithms!

## 📄 License

This project is for educational and demonstration purposes. Please check with your organization's policies for commercial use.

---

<div align="center">
  <p><strong>Built with ❤️ using Google OR-Tools and Python</strong></p>
  <p><em>Optimizing schedules, one constraint at a time</em></p>
</div>
