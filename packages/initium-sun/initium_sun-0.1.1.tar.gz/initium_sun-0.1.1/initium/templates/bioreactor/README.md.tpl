# $PROJECT_NAME - Festo Bioreactor System

## Overview
This project implements a bioreactor control and simulation system using Festo components.

## System Configuration
- Reactor Volume: $REACTOR_VOLUME L
- Target Temperature: $TEMP_C °C
- Target pH: $PH
- Agitation Speed: $AGITATION RPM
- Microorganism: $MICROORGANISM
- Control Strategy: $CONTROL_STRATEGY

## Project Structure
```
.
├── control/         # Control algorithms and PID implementation
├── modeling/        # Bioreactor mathematical models
├── simulation/      # Simulation scripts and test cases
└── visualization/   # Dashboard and visualization components
```

## Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure the system:
```bash
cp config.yml config.local.yml
# Edit config.local.yml with your settings
```

## Running Simulations
```bash
# Run simulation
python simulation/main.py --config config.local.yml

# Start visualization dashboard
python visualization/dashboard.py