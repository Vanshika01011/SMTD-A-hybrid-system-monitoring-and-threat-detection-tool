# SMTD: A Hybrid System Monitoring and Threat Detection Tool

## Project Overview

SMTD is a modern Python-based tool that provides comprehensive system monitoring and basic threat detection capabilities in a single application. It offers real-time visualization of system resources while identifying potentially suspicious processes, all through a clean and intuitive interface.

## Team Information

**Team Name:** SyncOS (SE(OS)-VI-T117)

- **Vanshika Pundir** (Team Lead) - 220221977 - vanshikapundir555@gmail.com
- **Abhijeet Singh** - 220111211 - abhijeetsinghs264@gmail.com
- **Jessica Dass** - 22022581 - jessicadass08@gmail.com
- **Aman Kumar** - 22011964 - amank756195@gmail.com

## Features

### System Monitoring
- Real-time tracking of CPU usage
- Memory (RAM) consumption monitoring
- Disk activity tracking
- Network traffic analysis
- Detailed process viewer with sortable columns

### Threat Detection
- Identification of unusual or suspicious processes
- Flagging of potentially harmful system activities
- Rule-based detection system
- Whitelist mechanism to reduce false positives

### User Interface
- Clean, modern interface with smooth graphs
- Dark/light mode support
- Tab-based navigation
- Interactive, real-time visualization
- Search functionality for filtering processes

## Technical Architecture

### Frontend (User Interface)
- Built with Tkinter and ttk for a modern appearance
- Features interactive elements like dropdown menus and sortable tables
- Supports dark mode throughout the application

### Backend (Monitoring Engine)
- Powered by psutil to collect system information
- Uses "rolling buffers" for efficient data management
- Updates regularly without freezing the application

### Data Visualization
- Matplotlib creates professional, interactive graphs
- Export capabilities to CSV files or SQLite database
- Historical data analysis for identifying trends


## Project Status

Current completion: **85%**

| Component | Status | Completion % |
|-----------|--------|--------------|
| Core Application | Completed | 100% |
| Monitoring Capabilities | Completed | 100% |
| Security Features | In Progress | 70-80% |
| User Experience | In Progress | 90% |

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/SMTD.git

# Navigate to the project directory
cd SMTD

# Install required dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Requirements

- Python 3.7+
- psutil
- matplotlib
- Tkinter/ttk

## Challenges Overcome

- Resolved UI freezing using non-blocking updates with root.after()
- Fixed graph rendering issues for extended monitoring
- Implemented proper exception handling for process termination
- Reduced false positives in threat detection with intelligent whitelisting

## Pending Tasks

- Refinement of network anomaly detection
- Implementation of behavioral pattern analysis
- Optimization of SQLite database schema
- Accessibility improvements (colorblind-friendly schemes, keyboard shortcuts)
- Final cross-platform testing and validation

## Contact

For questions or feedback, please contact the team lead: vanshikapundir555@gmail.com
