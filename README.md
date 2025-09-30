# OR-Tools Scheduling Practice Demo

<div align="center">
  <img src="assets/stryker_logo_cmyk.svg" height="60" alt="Stryker" style="filter: brightness(0);">
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="assets/digitalrnd-newcolor.svg" height="70" alt="Digital R&D">
</div>

<div align="center">
  <h2>🗓️ Advanced Scheduling Optimization Platform</h2>
  <p><em>High-performance Python scheduler using Google OR-Tools for complex scheduling problems</em></p>
</div>

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge)](https://www.python.org/)
[![OR-Tools](https://img.shields.io/badge/OR--Tools-9.14-green?style=for-the-badge)](https://developers.google.com/optimization)
[![NumPy](https://img.shields.io/badge/NumPy-2.3-red?style=for-the-badge)](https://numpy.org/)
[![Optimization](https://img.shields.io/badge/Industry-Operations%20Research-orange?style=for-the-badge)](https://en.wikipedia.org/wiki/Operations_research)

</div>

---

## 🚀 Features

**OR-Tools Scheduling Practice Demo** provides comprehensive capabilities for solving complex scheduling optimization problems:

- **🔧 OR-Tools Integration** - Leverage Google's powerful optimization library
- **📅 Multi-Objective Scheduling** - Handle complex scheduling constraints and objectives
- **⚡ High-Performance Solvers** - CP-SAT solver for constraint programming problems
- **📊 Resource Management** - Optimize resource allocation and utilization
- **🎯 Real-time Optimization** - Fast solving for dynamic scheduling requirements
- **📈 Analytics & Reporting** - Detailed analysis of scheduling solutions
- **🔄 Flexible Constraints** - Support for various scheduling constraints
- **🧮 Mathematical Modeling** - Advanced constraint programming techniques

<div align="center">

![Constraint Programming](https://img.shields.io/badge/CP--SAT-Solver-success?style=for-the-badge&logo=google)
![Resource Optimization](https://img.shields.io/badge/Resource-Optimization-success?style=for-the-badge&logo=calendar)
![Mathematical Modeling](https://img.shields.io/badge/Mathematical-Modeling-success?style=for-the-badge&logo=calculator)
![Multi-Objective](https://img.shields.io/badge/Multi--Objective-Optimization-success?style=for-the-badge&logo=target)
![Real-time](https://img.shields.io/badge/Real--time-Scheduling-success?style=for-the-badge&logo=clock)

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

### Basic Scheduling Example

```python
from src.scheduler import Scheduler

# Create a new scheduler instance
scheduler = Scheduler()

# Define your scheduling problem
scheduler.add_jobs(jobs_data)
scheduler.add_resources(resources_data)
scheduler.add_constraints(constraints_data)

# Solve the scheduling problem
solution = scheduler.solve()

# Display results
scheduler.display_solution(solution)
```

## 📋 Scheduling Problem Types

This demo platform supports various scheduling scenarios:

### 🏭 **Job Shop Scheduling**

- Multiple jobs with sequential operations
- Resource constraints and dependencies
- Minimizing makespan and tardiness

### 👥 **Employee Scheduling**

- Shift assignments and preferences
- Skill-based task allocation
- Fair workload distribution

### 🚛 **Vehicle Routing with Time Windows**

- Delivery route optimization
- Time window constraints
- Capacity and distance optimization

### 🏥 **Healthcare Scheduling**

- Patient appointment scheduling
- Staff allocation optimization
- Equipment and room management

## 🔧 Core Components

### Scheduler Engine

- **CP-SAT Solver**: Google's constraint programming solver
- **Model Builder**: Flexible constraint model creation
- **Solution Parser**: Extract and format optimization results

### Constraint Types

- **Time Constraints**: Start/end times, deadlines, durations
- **Resource Constraints**: Capacity limits, availability windows
- **Precedence Constraints**: Task dependencies and sequences
- **Assignment Constraints**: Resource-task allocations

### Optimization Objectives

- **Makespan Minimization**: Reduce total completion time
- **Cost Optimization**: Minimize operational costs
- **Resource Utilization**: Maximize efficiency
- **Customer Satisfaction**: Minimize delays and violations

## 📊 Dependencies

- **[OR-Tools](https://developers.google.com/optimization)** `9.14.6206` - Google's optimization tools
- **[NumPy](https://numpy.org/)** `2.3.3` - Numerical computing library
- **[Pandas](https://pandas.pydata.org/)** `2.3.3` - Data manipulation and analysis
- **[Protobuf](https://developers.google.com/protocol-buffers)** `6.31.1` - Protocol buffer support

## 🚀 Usage Examples

### Example 1: Simple Job Scheduling

```python
# Define jobs with processing times
jobs = [
    {"id": 1, "duration": 3, "deadline": 10},
    {"id": 2, "duration": 2, "deadline": 8},
    {"id": 3, "duration": 4, "deadline": 12}
]

# Create and solve
scheduler = Scheduler()
solution = scheduler.schedule_jobs(jobs)
```

### Example 2: Resource-Constrained Scheduling

```python
# Define resources and jobs
resources = [{"id": "machine_1", "capacity": 1}, {"id": "machine_2", "capacity": 1}]
jobs = [
    {"id": 1, "duration": 5, "required_resource": "machine_1"},
    {"id": 2, "duration": 3, "required_resource": "machine_2"}
]

scheduler = Scheduler()
solution = scheduler.schedule_with_resources(jobs, resources)
```

## 📈 Performance Metrics

The platform provides comprehensive metrics for solution evaluation:

- **Makespan**: Total completion time
- **Resource Utilization**: Percentage of resource usage
- **Tardiness**: Total delay beyond deadlines
- **Solution Quality**: Objective function value
- **Solving Time**: Computational performance

## 🔬 Advanced Features

### Custom Constraints

```python
# Add custom constraint functions
scheduler.add_custom_constraint(lambda x, y: x.start + x.duration <= y.start)
```

### Multi-Objective Optimization

```python
# Define multiple objectives with weights
objectives = [
    {"type": "minimize_makespan", "weight": 0.6},
    {"type": "minimize_cost", "weight": 0.4}
]
scheduler.set_objectives(objectives)
```

### Solution Visualization

```python
# Generate Gantt charts and schedules
scheduler.visualize_solution(solution, chart_type="gantt")
scheduler.export_schedule(solution, format="csv")
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

## 🏷️ Use Cases

This scheduling platform is ideal for:

- **Manufacturing**: Production line scheduling and optimization
- **Healthcare**: Patient and staff scheduling systems
- **Transportation**: Vehicle routing and logistics
- **Education**: Course and exam scheduling
- **Service Industry**: Appointment and resource management

## 📄 License

This project is for educational and demonstration purposes. Please check with your organization's policies for commercial use.

---

<div align="center">
  <p><strong>Built with ❤️ using Google OR-Tools and Python</strong></p>
  <p><em>Optimizing schedules, one constraint at a time</em></p>
</div>
