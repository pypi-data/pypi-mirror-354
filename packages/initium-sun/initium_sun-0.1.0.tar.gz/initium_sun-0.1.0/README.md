# Project Bootstrap

One-click generator for automation projects. This tool helps you quickly set up standardized project structures for various automation systems.

## Supported Project Types

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

## Getting Started

1. Clone this repository
2. Run the project generator:
```bash
./scripts/generate_project.sh
```

3. Follow the prompts to:
   - Enter your project name
   - Select the project type
   - Create a GitLab repository (optional)

## Project Structure

Each generated project includes:
- Standard directory structure
- CI/CD configuration
- Documentation templates
- Example implementation
- Test framework

## Requirements

- Git
- GitLab account (for remote repository creation)
- Bash shell
- Python 3.8+ (for bioreactor templates)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
