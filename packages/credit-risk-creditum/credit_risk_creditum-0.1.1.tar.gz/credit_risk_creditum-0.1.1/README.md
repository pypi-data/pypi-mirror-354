# Credit Risk Assessment System

A comprehensive credit risk assessment system that evaluates both individual and corporate credit applications, taking into account economic indicators and various risk factors.

## Features

- Individual credit risk assessment
- Corporate credit risk assessment
- Economic indicators integration
- Machine learning model integration (Random Forest and Logistic Regression)
- Configurable risk thresholds and weights

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/credit-risk-assessment.git
cd credit-risk-assessment
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the package:
```bash
pip install -e .
```

## Usage

Check the `examples/example_usage.py` file for a complete example of how to use the system. Here's a quick example:

```python
from credit_risk.core.application import CreditApplication

# Initialize application processor
credit_app = CreditApplication(min_credit_score=600, max_dti=0.43)

# Update economic indicators
economic_data = {
    'cpi': 0.02,
    'gdp_growth': 0.03,
    'unemployment_rate': 0.05,
    # ... other indicators
}
credit_app.economic_indicators.update_indicators(economic_data)

# Process an individual application
individual_application = {
    'credit_score': 720,
    'monthly_income': 5000,
    'monthly_debt': 1500,
    'loan_amount': 20000,
    'loan_purpose': 'home_improvement',
    # ... other features
}

decision = credit_app.make_decision(individual_application, 'individual')
print(decision)
```

## Project Structure

```
credit_risk_assessment/
├── src/
│   └── credit_risk/
│       ├── models/           # Risk assessment models
│       ├── core/            # Core functionality
│       └── utils/           # Utility functions
└── examples/               # Usage examples
```

## Requirements

- Python 3.7+
- NumPy
- Pandas
- scikit-learn
- typing

## License

This project is licensed under the MIT License - see the LICENSE file for details.