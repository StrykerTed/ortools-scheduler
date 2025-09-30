"""
3D Printing Platform Scheduler for Medical Devices
Uses Google OR-Tools CP-SAT solver for optimized scheduling.
"""
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from ortools.sat.python import cp_model
import json

class PlatformScheduler:
    """
    3D Printing Platform Scheduler for medical device manufacturing.
    
    Optimizes scheduling of medical cases across multiple 3D printers with constraints:
    - 50 available printers
    - 14 cases per platform
    - 16-hour platform cycles
    - 2-hour turnaround time
    - Due date constraints with shipping lead time
    - Priority handling (emergency, urgent, standard)
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the platform scheduler.
        
        Args:
            config: Configuration dictionary with scheduling parameters
        """
        # Default configuration
        default_config = {
            "total_printers": 50,
            "cases_per_platform": 14,
            "platform_duration_hours": 16,
            "turnaround_hours": 2,
            "working_schedule": "24/7",
            "shipping_lead_days": 10,
            "planning_horizon_days": 90
        }
        
        self.config = {**default_config, **(config or {})}
        self.model = None
        self.solver = None
        self.solution = None
        
        # Decision variables
        self.platform_vars = {}      # Platform assignment variables
        self.start_time_vars = {}    # Platform start time variables
        self.printer_vars = {}       # Printer assignment variables
        
        print(f"PlatformScheduler initialized:")
        print(f"- {self.config['total_printers']} printers available")
        print(f"- {self.config['cases_per_platform']} cases per platform")
        print(f"- {self.config['platform_duration_hours']}h platform cycle + {self.config['turnaround_hours']}h turnaround")
    
    def load_cases_from_csv(self, filename: str) -> List[Dict[str, Any]]:
        """Load medical cases from CSV file."""
        df = pd.read_csv(filename)
        cases = df.to_dict('records')
        
        # Convert date strings to datetime objects
        for case in cases:
            case['surgery_date'] = datetime.strptime(case['surgery_date'], '%Y-%m-%d')
            case['due_date'] = datetime.strptime(case['due_date'], '%Y-%m-%d')
        
        print(f"Loaded {len(cases)} medical cases from {filename}")
        return cases
    
    def create_platforms(self, cases: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        """
        Group cases into platforms of optimal size.
        
        Args:
            cases: List of medical cases
            
        Returns:
            List of platforms, each containing up to cases_per_platform cases
        """
        # Sort cases by priority and due date
        priority_order = {"emergency": 0, "urgent": 1, "standard": 2}
        
        sorted_cases = sorted(cases, key=lambda x: (
            priority_order.get(x['priority'], 3),
            x['due_date']
        ))
        
        platforms = []
        cases_per_platform = self.config['cases_per_platform']
        
        for i in range(0, len(sorted_cases), cases_per_platform):
            platform_cases = sorted_cases[i:i + cases_per_platform]
            platforms.append(platform_cases)
        
        print(f"Created {len(platforms)} platforms from {len(cases)} cases")
        return platforms
    
    def build_scheduling_model(self, platforms: List[List[Dict[str, Any]]]) -> cp_model.CpModel:
        """
        Build the CP-SAT constraint programming model.
        
        Args:
            platforms: List of platforms with cases
            
        Returns:
            Configured CP-SAT model
        """
        model = cp_model.CpModel()
        
        num_platforms = len(platforms)
        num_printers = self.config['total_printers']
        platform_duration = self.config['platform_duration_hours']
        turnaround_time = self.config['turnaround_hours']
        
        # Planning horizon in hours
        horizon_hours = self.config['planning_horizon_days'] * 24
        
        print(f"Building model: {num_platforms} platforms, {num_printers} printers, {horizon_hours}h horizon")
        
        # Decision variables
        # Binary variable: platform p is assigned to printer r
        self.printer_vars = {}
        for p in range(num_platforms):
            for r in range(num_printers):
                self.printer_vars[(p, r)] = model.NewBoolVar(f'platform_{p}_printer_{r}')
        
        # Integer variable: start time of platform p (in hours from now)
        self.start_time_vars = {}
        for p in range(num_platforms):
            self.start_time_vars[p] = model.NewIntVar(0, horizon_hours, f'start_time_{p}')
        
        # CONSTRAINTS
        
        # 1. Each platform must be assigned to exactly one printer
        for p in range(num_platforms):
            model.Add(sum(self.printer_vars[(p, r)] for r in range(num_printers)) == 1)
        
        # 2. No two platforms can overlap on the same printer
        for r in range(num_printers):
            for p1 in range(num_platforms):
                for p2 in range(p1 + 1, num_platforms):
                    # If both platforms assigned to same printer, they can't overlap
                    # Platform p1 ends before p2 starts OR p2 ends before p1 starts
                    
                    # Big M constraint for non-overlapping
                    big_m = horizon_hours
                    
                    # If both assigned to printer r
                    both_assigned = model.NewBoolVar(f'both_assigned_{p1}_{p2}_{r}')
                    model.Add(self.printer_vars[(p1, r)] + self.printer_vars[(p2, r)] <= 1 + both_assigned)
                    model.Add(both_assigned <= self.printer_vars[(p1, r)])
                    model.Add(both_assigned <= self.printer_vars[(p2, r)])
                    
                    # Non-overlap constraint when both assigned to same printer
                    model.Add(
                        self.start_time_vars[p1] + platform_duration + turnaround_time <= 
                        self.start_time_vars[p2] + big_m * (1 - both_assigned)
                    ).OnlyEnforceIf(both_assigned)
                    
                    model.Add(
                        self.start_time_vars[p2] + platform_duration + turnaround_time <= 
                        self.start_time_vars[p1] + big_m * (1 - both_assigned)
                    ).OnlyEnforceIf(both_assigned)
        
        # 3. Due date constraints (soft constraints with penalties)
        due_date_penalties = []
        for p, platform_cases in enumerate(platforms):
            # Find the earliest due date in this platform
            earliest_due = min(case['due_date'] for case in platform_cases)
            hours_until_due = int((earliest_due - datetime.now()).total_seconds() / 3600)
            
            # If due date is in the past, give a reasonable buffer (24 hours)
            if hours_until_due < 0:
                hours_until_due = 24
                print(f"⚠️  Platform {p} has past due date, using 24h buffer")
            
            # Soft constraint: penalize if platform completes after due date
            completion_time = self.start_time_vars[p] + platform_duration
            lateness = model.NewIntVar(0, horizon_hours, f'lateness_{p}')
            model.Add(lateness >= completion_time - hours_until_due)
            
            # Weight penalty based on platform priority
            emergency_cases = sum(1 for case in platform_cases if case['priority'] == 'emergency')
            urgent_cases = sum(1 for case in platform_cases if case['priority'] == 'urgent')
            
            penalty_weight = emergency_cases * 1000 + urgent_cases * 100 + 10
            due_date_penalties.append(penalty_weight * lateness)
        
        # OBJECTIVES
        
        # Primary: Minimize maximum completion time (makespan)
        max_completion = model.NewIntVar(0, horizon_hours, 'max_completion')
        for p in range(num_platforms):
            completion_time = self.start_time_vars[p] + platform_duration
            model.Add(max_completion >= completion_time)
        
        # Secondary: Minimize total tardiness for priority cases
        tardiness_penalties = []
        for p, platform_cases in enumerate(platforms):
            for case in platform_cases:
                if case['priority'] in ['emergency', 'urgent']:
                    due_hours = int((case['due_date'] - datetime.now()).total_seconds() / 3600)
                    completion_time = self.start_time_vars[p] + platform_duration
                    
                    tardiness = model.NewIntVar(0, horizon_hours, f'tardiness_{p}_{case["case_id"]}')
                    model.Add(tardiness >= completion_time - due_hours)
                    
                    weight = 100 if case['priority'] == 'emergency' else 10
                    tardiness_penalties.append(weight * tardiness)
        
        # Combined objective: minimize makespan + weighted tardiness + due date penalties
        total_tardiness = sum(tardiness_penalties) if tardiness_penalties else 0
        total_due_date_penalty = sum(due_date_penalties) if due_date_penalties else 0
        model.Minimize(max_completion + total_tardiness + total_due_date_penalty)
        
        self.model = model
        print(f"Model built with {len(self.printer_vars)} printer assignment variables")
        return model
    
    def solve_schedule(self, time_limit_seconds: int = 300) -> bool:
        """
        Solve the scheduling optimization problem.
        
        Args:
            time_limit_seconds: Maximum solving time
            
        Returns:
            True if solution found, False otherwise
        """
        if not self.model:
            raise ValueError("Model not built. Call build_scheduling_model() first.")
        
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = time_limit_seconds
        solver.parameters.log_search_progress = True
        
        print(f"Solving with {time_limit_seconds}s time limit...")
        status = solver.Solve(self.model)
        
        self.solver = solver
        
        if status == cp_model.OPTIMAL:
            print("✅ Optimal solution found!")
            return True
        elif status == cp_model.FEASIBLE:
            print("✅ Feasible solution found!")
            return True
        else:
            print(f"❌ No solution found. Status: {solver.StatusName(status)}")
            return False
    
    def extract_solution(self, platforms: List[List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Extract and format the solution results.
        
        Args:
            platforms: Original platform configuration
            
        Returns:
            Formatted solution dictionary
        """
        if not self.solver:
            raise ValueError("No solution available. Call solve_schedule() first.")
        
        solution = {
            "status": "success",
            "objective_value": self.solver.ObjectiveValue(),
            "solve_time_seconds": self.solver.WallTime(),
            "platform_assignments": [],
            "printer_utilization": {},
            "summary": {}
        }
        
        # Extract platform assignments
        for p, platform_cases in enumerate(platforms):
            start_time_hours = self.solver.Value(self.start_time_vars[p])
            start_datetime = datetime.now() + timedelta(hours=start_time_hours)
            end_datetime = start_datetime + timedelta(hours=self.config['platform_duration_hours'])
            
            # Find assigned printer
            assigned_printer = None
            for r in range(self.config['total_printers']):
                if self.solver.Value(self.printer_vars[(p, r)]) == 1:
                    assigned_printer = r
                    break
            
            platform_info = {
                "platform_id": p,
                "assigned_printer": assigned_printer,
                "start_time": start_datetime.strftime("%Y-%m-%d %H:%M"),
                "end_time": end_datetime.strftime("%Y-%m-%d %H:%M"),
                "duration_hours": self.config['platform_duration_hours'],
                "num_cases": len(platform_cases),
                "cases": platform_cases,
                "priority_breakdown": {}
            }
            
            # Analyze priority breakdown
            for case in platform_cases:
                priority = case['priority']
                platform_info['priority_breakdown'][priority] = \
                    platform_info['priority_breakdown'].get(priority, 0) + 1
            
            solution["platform_assignments"].append(platform_info)
        
        # Calculate printer utilization
        printer_usage = {}
        for p, platform_info in enumerate(solution["platform_assignments"]):
            printer = platform_info["assigned_printer"]
            if printer not in printer_usage:
                printer_usage[printer] = []
            printer_usage[printer].append({
                "platform_id": p,
                "start": platform_info["start_time"],
                "end": platform_info["end_time"]
            })
        
        solution["printer_utilization"] = printer_usage
        
        # Generate summary statistics
        total_cases = sum(len(p_info["cases"]) for p_info in solution["platform_assignments"])
        printers_used = len(printer_usage)
        
        solution["summary"] = {
            "total_platforms": len(platforms),
            "total_cases": total_cases,
            "printers_used": printers_used,
            "printer_utilization_rate": f"{(printers_used / self.config['total_printers']) * 100:.1f}%",
            "avg_cases_per_platform": f"{total_cases / len(platforms):.1f}",
            "planning_horizon_hours": max([
                (datetime.strptime(p["end_time"], "%Y-%m-%d %H:%M") - datetime.now()).total_seconds() / 3600
                for p in solution["platform_assignments"]
            ])
        }
        
        self.solution = solution
        return solution
    
    def schedule_platforms(self, cases: List[Dict[str, Any]], 
                          time_limit: int = 300) -> Optional[Dict[str, Any]]:
        """
        Complete scheduling workflow: group cases, build model, solve, extract solution.
        
        Args:
            cases: List of medical cases to schedule
            time_limit: Solving time limit in seconds
            
        Returns:
            Solution dictionary or None if no solution found
        """
        try:
            # Group cases into platforms
            platforms = self.create_platforms(cases)
            
            # Build optimization model
            self.build_scheduling_model(platforms)
            
            # Solve the model
            if self.solve_schedule(time_limit):
                # Extract and return solution
                solution = self.extract_solution(platforms)
                print(f"\n🎯 Scheduling completed successfully!")
                print(f"   - {solution['summary']['total_platforms']} platforms scheduled")
                print(f"   - {solution['summary']['printers_used']} printers utilized")
                print(f"   - {solution['summary']['printer_utilization_rate']} printer utilization")
                return solution
            else:
                return None
                
        except Exception as e:
            print(f"❌ Error during scheduling: {e}")
            return None
    
    def display_schedule_summary(self, solution: Optional[Dict[str, Any]] = None):
        """Display a formatted summary of the scheduling solution."""
        if solution is None:
            solution = self.solution
        
        if not solution:
            print("No solution available to display.")
            return
        
        print("\n" + "="*80)
        print("🏥 3D PRINTING PLATFORM SCHEDULE SUMMARY")
        print("="*80)
        
        print(f"📊 Overall Statistics:")
        print(f"   • Total Platforms: {solution['summary']['total_platforms']}")
        print(f"   • Total Cases: {solution['summary']['total_cases']}")
        print(f"   • Printers Used: {solution['summary']['printers_used']}/{self.config['total_printers']}")
        print(f"   • Utilization Rate: {solution['summary']['printer_utilization_rate']}")
        print(f"   • Avg Cases/Platform: {solution['summary']['avg_cases_per_platform']}")
        print(f"   • Solve Time: {solution['solve_time_seconds']:.2f}s")
        
        print(f"\n🗓️ Platform Schedule:")
        for platform in solution['platform_assignments']:
            print(f"\n   Platform {platform['platform_id']:2d} | Printer {platform['assigned_printer']:2d} | "
                  f"{platform['start_time']} → {platform['end_time']}")
            print(f"   Cases: {platform['num_cases']:2d} | Priorities: {platform['priority_breakdown']}")
            
            # Show first few cases
            for i, case in enumerate(platform['cases'][:3]):
                print(f"      • {case['case_id']} - {case['patient_name']} - {case['device_type']} ({case['priority']})")
            if len(platform['cases']) > 3:
                print(f"      • ... and {len(platform['cases']) - 3} more cases")
        
        print("\n" + "="*80)
    
    def display_gantt_chart(self, solution: Optional[Dict[str, Any]] = None):
        """Display a simple text-based Gantt chart of the schedule."""
        if solution is None:
            solution = self.solution
        
        if not solution:
            print("No solution available to display.")
            return
        
        print("\n" + "="*100)
        print("📊 3D PRINTING PLATFORM GANTT CHART")
        print("="*100)
        
        # Sort platforms by start time
        platforms = sorted(solution['platform_assignments'], 
                          key=lambda x: x['start_time'])
        
        # Create timeline
        timeline_hours = []
        base_time = datetime.strptime(platforms[0]['start_time'], "%Y-%m-%d %H:%M")
        
        print(f"{'Printer':>8} | {'Platform':>8} | {'Timeline (Hours from Start)':^60} | {'Cases':>5}")
        print("-" * 100)
        
        for platform in platforms:
            start_dt = datetime.strptime(platform['start_time'], "%Y-%m-%d %H:%M")
            end_dt = datetime.strptime(platform['end_time'], "%Y-%m-%d %H:%M")
            
            start_offset = int((start_dt - base_time).total_seconds() / 3600)
            duration = int((end_dt - start_dt).total_seconds() / 3600)
            
            # Create visual timeline (60 chars wide)
            timeline = ['.'] * 60
            start_pos = min(start_offset, 59)
            end_pos = min(start_offset + duration, 60)
            
            # Fill timeline with platform marker
            for i in range(start_pos, end_pos):
                timeline[i] = '█'
            
            timeline_str = ''.join(timeline)
            
            # Priority indicators
            priorities = platform['priority_breakdown']
            priority_str = f"E:{priorities.get('emergency', 0)} U:{priorities.get('urgent', 0)} S:{priorities.get('standard', 0)}"
            
            print(f"   P{platform['assigned_printer']:02d}   |    P{platform['platform_id']:02d}   | {timeline_str} | {len(platform['cases']):2d}")
            print(f"        |          | {start_dt.strftime('%m/%d %H:%M'):>12} -> {end_dt.strftime('%m/%d %H:%M'):<12} | {priority_str}")
            print("-" * 100)
        
        # Legend
        print(f"\n📋 Legend:")
        print(f"   █ = Platform running  . = Idle time")
        print(f"   E = Emergency cases, U = Urgent cases, S = Standard cases")
        print(f"   Timeline shows {((datetime.strptime(platforms[-1]['end_time'], '%Y-%m-%d %H:%M') - base_time).total_seconds() / 3600):.0f} hours from start")
    
    def export_detailed_schedule(self, solution: Optional[Dict[str, Any]] = None, 
                                filename: str = "detailed_schedule.csv"):
        """Export detailed schedule to CSV for external analysis."""
        if solution is None:
            solution = self.solution
        
        if not solution:
            print("No solution available to export.")
            return
        
        # Flatten all case data with schedule information
        detailed_data = []
        
        for platform in solution['platform_assignments']:
            platform_start = datetime.strptime(platform['start_time'], "%Y-%m-%d %H:%M")
            platform_end = datetime.strptime(platform['end_time'], "%Y-%m-%d %H:%M")
            
            for case in platform['cases']:
                case_detail = {
                    'case_id': case['case_id'],
                    'patient_name': case['patient_name'],
                    'device_type': case['device_type'],
                    'priority': case['priority'],
                    'surgery_date': case['surgery_date'],
                    'due_date': case['due_date'], 
                    'shipping_days': case['shipping_days'],
                    'platform_id': platform['platform_id'],
                    'assigned_printer': platform['assigned_printer'],
                    'platform_start': platform['start_time'],
                    'platform_end': platform['end_time'],
                    'production_days_before_surgery': (
                        datetime.strptime(str(case['surgery_date']).split()[0], "%Y-%m-%d") - platform_end
                    ).days,
                    'on_time_delivery': (
                        datetime.strptime(str(case['due_date']).split()[0], "%Y-%m-%d").date() >= platform_end.date()
                    )
                }
                detailed_data.append(case_detail)
        
        # Export to CSV
        df = pd.DataFrame(detailed_data)
        df.to_csv(filename, index=False)
        
        print(f"\n📊 Detailed schedule exported to {filename}")
        print(f"   - {len(detailed_data)} cases with schedule details")
        
        # Quick analysis
        on_time_count = sum(1 for case in detailed_data if case['on_time_delivery'])
        on_time_rate = (on_time_count / len(detailed_data)) * 100
        
        print(f"   - On-time delivery rate: {on_time_rate:.1f}% ({on_time_count}/{len(detailed_data)})")
        
        return df

def main():
    """Demo script showing the platform scheduler in action."""
    print("🚀 3D Printing Platform Scheduler Demo")
    print("="*50)
    
    # Initialize scheduler
    scheduler = PlatformScheduler()
    
    # Load demo cases
    try:
        cases = scheduler.load_cases_from_csv("demo_medical_cases.csv")
    except FileNotFoundError:
        print("Demo data not found. Please run demo_data.py first to generate sample cases.")
        return
    
    # Schedule the platforms
    solution = scheduler.schedule_platforms(cases, time_limit=60)
    
    if solution:
        # Display results
        scheduler.display_schedule_summary(solution)
        
        # Show Gantt chart
        scheduler.display_gantt_chart(solution)
        
        # Export detailed analysis
        scheduler.export_detailed_schedule(solution, "detailed_schedule.csv")
        
        # Save solution to file
        with open("scheduling_solution.json", "w") as f:
            json.dump(solution, f, indent=2, default=str)
        print(f"\n💾 Solution saved to scheduling_solution.json")
    else:
        print("❌ Could not find a feasible schedule.")

if __name__ == "__main__":
    main()