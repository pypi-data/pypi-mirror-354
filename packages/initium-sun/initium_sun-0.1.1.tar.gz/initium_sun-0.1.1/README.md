# Initium Project Bootstrap

One-click generator for automation projects. This tool helps you quickly set up standardized project structures for various automation systems.

## Installation

### Option 1: Using pip (recommended)

```bash
pip install initium-sun
```

### Option 2: From source (developer mode)

1. Clone the repository:
   ```bash
   git clone https://gitlab.com/autowerk/initium.git
   cd initium
   ```

2. Make the script executable (Linux/macOS):
   ```bash
   chmod +x scripts/generate_project.sh
   ```

3. Run directly from source:
   ```bash
   ./scripts/generate_project.sh
   ```

   Or install in development mode:
   ```bash
   pip install -e .
   ```

## Usage

### Option 1: Using the Python module (after pip install)

```bash
python -m initium.cli <project_name> <project_type> [--remote]
```

### Option 2: Using the interactive script (from source)

```bash
./scripts/generate_project.sh
```

Then follow the interactive prompts to:
1. Enter your project name
2. Select project type (plc/hmi/ros/bioreactor)
3. Optionally create a remote GitLab repository

### Supported Project Types

- **PLC Templates**
  - Standard PLC project structure
  - Common PLC libraries and configurations
  - Example programs and documentation

- **HMI Templates**
  - Modern HMI interface templates
  - Common visualization components
  - Standard communication protocols

- **ROS Templates**
  - ROS 2 project structure
  - Common ROS nodes and messages
  - Integration with hardware

- **Bioreactor Templates**
  - Complete bioreactor control system
  - Simulation environment
  - Visualization dashboard
  - PID control implementation

## Examples

### Using Python module:
```bash
# Create a new PLC project
python -m initium.cli my_plc_project plc

# Create an HMI project with a remote GitLab repository
python -m initium.cli my_hmi_project hmi --remote

# Create a bioreactor project
python -m initium.cli my_bioreactor_project bioreactor
```

### Using the interactive script:
```bash
./scripts/generate_project.sh
# Then follow the prompts to:
# 1. Enter project name
# 2. Select project type
# 3. Optionally create a remote GitLab repository
```

## Getting Started

1. Install the package as shown above
2. Run the command with your desired project name and type
3. If using `--remote`, make sure you have GitLab access configured

## Project Structure

Each generated project includes:
- Standard directory structure
- CI/CD configuration
- Documentation templates
- Example implementation
- Test framework

## Requirements

- Python 3.6+
- Git (for version control)
- GitLab account (if using `--remote` flag)
- `requests` Python package (automatically installed with the package)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
