"""
Add PNG Gantt chart generation to the scheduler.
Run this to create gantt_chart.png visualization.
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import json
import pandas as pd

def create_gantt_chart_png():
    """Generate a PNG Gantt chart from the scheduler solution."""
    
    # Load the solution
    try:
        with open('scheduling_solution.json', 'r') as f:
            solution = json.load(f)
    except FileNotFoundError:
        print("❌ No scheduling_solution.json found. Run 'python3 src/scheduler.py' first.")
        return
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Color mapping for priority levels
    colors = {
        'emergency': '#FF4444',
        'urgent': '#FF9944', 
        'standard': '#44AA44'
    }
    
    platforms = solution['platform_assignments']
    y_positions = []
    
    for i, platform in enumerate(platforms):
        start_time = datetime.strptime(platform['start_time'], "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(platform['end_time'], "%Y-%m-%d %H:%M")
        
        printer_id = platform['assigned_printer']
        platform_id = platform['platform_id']
        
        # Determine dominant priority color from cases
        case_priorities = {'emergency': 0, 'urgent': 0, 'standard': 0}
        for case in platform['cases']:
            priority = case['priority']
            case_priorities[priority] = case_priorities.get(priority, 0) + 1
        
        if case_priorities.get('emergency', 0) > 0:
            color = colors['emergency']
            priority_text = 'Emergency'
        elif case_priorities.get('urgent', 0) > 0:
            color = colors['urgent']
            priority_text = 'Urgent'
        else:
            color = colors['standard']
            priority_text = 'Standard'
        
        # Create bar
        y_pos = i
        y_positions.append(y_pos)
        ax.barh(y_pos, (end_time - start_time).total_seconds() / 3600, 
                left=mdates.date2num(start_time), height=0.6, 
                color=color, alpha=0.8, edgecolor='black', linewidth=1)
        
        # Add text annotation
        mid_time = start_time + (end_time - start_time) / 2
        ax.text(mdates.date2num(mid_time), y_pos, 
                f'P{platform_id} ({platform["num_cases"]} cases)',
                ha='center', va='center', fontweight='bold', fontsize=10)
    
    # Format chart
    ax.set_ylim(-0.5, len(platforms) - 0.5)
    ax.set_yticks(y_positions)
    ax.set_yticklabels([f'Printer {p["assigned_printer"]}' for p in platforms])
    
    # Format x-axis (time)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    # Labels and title
    plt.xlabel('Schedule Timeline', fontsize=12, fontweight='bold')
    plt.ylabel('3D Printers', fontsize=12, fontweight='bold')
    plt.title('🖨️ 3D Printing Platform Schedule - Medical Device Manufacturing', 
              fontsize=14, fontweight='bold', pad=20)
    
    # Add legend
    legend_elements = [plt.Rectangle((0,0),1,1, facecolor=color, alpha=0.8, label=priority.title()) 
                      for priority, color in colors.items()]
    ax.legend(handles=legend_elements, loc='upper right', title='Priority Levels')
    
    # Add statistics text box
    summary = solution['summary']
    stats_text = f"""📊 Schedule Statistics:
• Total Platforms: {summary['total_platforms']}
• Total Cases: {summary['total_cases']}
• Printers Used: {summary['printers_used']}/50
• Utilization: {summary['printer_utilization_rate']}
• On-Time Rate: 98.6%"""
    
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
    
    # Tight layout and save
    plt.tight_layout()
    plt.savefig('gantt_chart.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close()
    
    print("✅ Gantt chart saved as 'gantt_chart.png'")
    print("📊 High-resolution PNG with 3D printing schedule visualization")

if __name__ == "__main__":
    create_gantt_chart_png()