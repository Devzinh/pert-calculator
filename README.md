# PERT Calculator

Command-line tool for project time estimation using the PERT (Program Evaluation Review Technique) method.

## What is PERT?

PERT calculates weighted time estimates based on three scenarios:
- **Optimistic (O)**: Best-case scenario
- **Most Likely (M)**: Realistic scenario  
- **Pessimistic (P)**: Worst-case scenario

**Formula:** `PERT = (O + 4M + P) / 6`

The standard deviation `σ = (P - O) / 6` indicates the uncertainty level.

## Features

- Input validation with retry loop
- Decimal support (both `.` and `,` formats)
- Animated output with interpretation
- Standard deviation calculation
- 68% confidence interval display

## Usage

```bash
python main.py
