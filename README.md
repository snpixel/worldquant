# WorldQuant Alpha Generator

A powerful tool for generating, optimizing, and validating alpha expressions for WorldQuant's Alpha Factory platform.

## Overview

The WorldQuant Alpha Generator is a Python-based tool designed to help quantitative researchers and algorithmic traders create and optimize alpha expressions. This tool automates the process of generating alpha strategies that can be submitted to WorldQuant's platform.

## Features

- **Alpha Expression Generation**: Create alpha expressions using different complexity modes:
  - Basic: Simple pattern-based expressions
  - Creative: Complex, multi-factor expressions
  - Optimize: Sophisticated expressions with industry neutralization and normalization
  
- **Alpha Optimization**: Refine expressions to improve performance metrics

- **Alpha Validation**: Verify expressions against WorldQuant's requirements before submission

- **Results Display**: Visualize and export generated alphas

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd worldquant-alpha
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your WorldQuant credentials in `data/credentials.json`:
   ```json
   {
     "username": "your_username",
     "password": "your_password"
   }
   ```

## Usage

### Basic Command

```bash
python generate_alphas.py
```

This will generate 5 alpha expressions in creative mode.

### Command Line Arguments

- `--credentials`: Path to credentials file (default: ./data/credentials.json)
- `--output-dir`: Directory to save results (default: ./data/generated_alphas)
- `--count`: Number of alpha expressions to generate (default: 5)
- `--mode`: Generation mode: 'basic', 'creative', or 'optimize' (default: 'creative')
- `--optimize`: Optimize generated alphas before display

### Examples

Generate 10 basic alpha expressions:
```bash
python generate_alphas.py --count 10 --mode basic
```

Generate and optimize 20 creative expressions:
```bash
python generate_alphas.py --count 20 --mode creative --optimize
```

## Project Structure

```
worldquant-alpha/
├── generate_alphas.py       # Main script
├── requirements.txt         # Dependencies
├── alpha_engine/            # Core alpha generation logic
│   ├── generator.py         # Alpha expression generator
│   ├── optimizer.py         # Expression optimization
│   └── validator.py         # Validation against WorldQuant requirements
├── config/                  # Configuration settings
├── data/                    # Data storage
│   ├── credentials.json     # WorldQuant credentials
│   └── generated_alphas/    # Output directory for generated alphas
├── ui/                      # User interface components
│   └── display.py           # Results display
└── utils/                   # Utility functions
    ├── api_client.py        # WorldQuant API client
    └── helpers.py           # Helper functions
```

## Dependencies

- requests >= 2.25.0
- tabulate >= 0.8.9
- colorama >= 0.4.4

## License

[License information]

## Contributing

[Contribution guidelines]

## Disclaimer

This tool is not affiliated with WorldQuant. Use at your own risk and ensure compliance with WorldQuant's terms of service when submitting generated alphas.