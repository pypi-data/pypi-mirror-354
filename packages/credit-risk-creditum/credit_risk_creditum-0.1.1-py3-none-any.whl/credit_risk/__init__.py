"""
Credit Risk Assessment System

A comprehensive credit risk assessment system that evaluates both individual 
and corporate credit applications using machine learning models and economic indicators.

Basic Usage:
    >>> from credit_risk import CreditApplication
    >>> app = CreditApplication()
    >>> result = app.assess_individual(application_data)

For more examples, see: https://github.com/omoshola-o/credit-risk-creditum/examples
"""

# Version information
__version__ = "1.0.0"
__author__ = "Omoshola Owolabi"
__email__ = "your.email@example.com"
__description__ = "A comprehensive credit risk assessment system"
__url__ = "https://github.com/omoshola-o/credit-risk-creditum"

# Import core classes and functions that users will commonly use
try:
    # Core application class (MAINTAINS EXISTING IMPORT PATH)
    from .core.application import CreditApplication
    
    # Models
    from .models.individual_model import IndividualRiskModel
    from .models.corporate_model import CorporateRiskModel
    
    # Data structures - provide defaults if not yet implemented
    try:
        from .core.decision_engine import CreditDecision, RiskLevel
    except ImportError:
        # Temporary placeholder until you implement these
        class CreditDecision:
            def __init__(self, status, risk_score, confidence=None):
                self.status = status
                self.risk_score = risk_score
                self.confidence = confidence
                
        class RiskLevel:
            LOW = "low"
            MEDIUM = "medium" 
            HIGH = "high"
    
    try:
        from .core.economic_indicators import EconomicIndicators
    except ImportError:
        # Placeholder - your existing code probably has this
        class EconomicIndicators:
            def update_indicators(self, data):
                pass
    
    # Utilities - provide safe imports
    try:
        from .utils.validators import validate_individual_application, validate_corporate_application
    except ImportError:
        def validate_individual_application(data):
            return True
        def validate_corporate_application(data):
            return True
    
    try:
        from .utils.exceptions import (
            CreditRiskError,
            InvalidApplicationError,
            ModelNotTrainedError,
            InsufficientDataError
        )
    except ImportError:
        # Basic exception classes
        class CreditRiskError(Exception):
            """Base exception for credit risk assessment."""
            pass
        
        class InvalidApplicationError(CreditRiskError):
            """Raised when application data is invalid."""
            pass
        
        class ModelNotTrainedError(CreditRiskError):
            """Raised when model hasn't been trained."""
            pass
        
        class InsufficientDataError(CreditRiskError):
            """Raised when insufficient data provided."""
            pass
    
    # Configuration - provide defaults
    try:
        from .data.default_configs import DEFAULT_INDIVIDUAL_CONFIG, DEFAULT_CORPORATE_CONFIG
    except ImportError:
        DEFAULT_INDIVIDUAL_CONFIG = {
            'min_credit_score': 600,
            'max_dti': 0.43,
            'risk_thresholds': {'low': 0.2, 'medium': 0.5, 'high': 0.8}
        }
        DEFAULT_CORPORATE_CONFIG = {
            'min_revenue': 100000,
            'max_debt_ratio': 0.6,
            'risk_thresholds': {'low': 0.2, 'medium': 0.5, 'high': 0.8}
        }
    
except ImportError as e:
    # Handle import errors gracefully during development
    import warnings
    warnings.warn(f"Some modules could not be imported: {e}", ImportWarning)

# Define what gets imported with "from credit_risk import *"
__all__ = [
    # Core classes
    "CreditApplication",
    "IndividualRiskModel", 
    "CorporateRiskModel",
    "EconomicIndicators",
    
    # Data structures
    "CreditDecision",
    "RiskLevel",
    
    # Validators
    "validate_individual_application",
    "validate_corporate_application",
    
    # Exceptions
    "CreditRiskError",
    "InvalidApplicationError", 
    "ModelNotTrainedError",
    "InsufficientDataError",
    
    # Configuration
    "DEFAULT_INDIVIDUAL_CONFIG",
    "DEFAULT_CORPORATE_CONFIG",
    
    # Version info
    "__version__",
]

# BACKWARD COMPATIBILITY: Support your existing example usage patterns
def quick_individual_assessment(application_data, min_credit_score=600, max_dti=0.43):
    """
    Quick individual credit assessment with default settings.
    
    Args:
        application_data (dict): Individual application data
        min_dti (float): Maximum debt-to-income ratio
        
    Returns:
        CreditDecision: Assessment result
        
    Example:
        >>> data = {'credit_score': 720, 'monthly_income': 5000, 'monthly_debt': 1500}
        >>> result = quick_individual_assessment(data)
        >>> print(result.status)
    """
    app = CreditApplication(min_credit_score=min_credit_score, max_dti=max_dti)
    # Try new method name first, fallback to existing method
    if hasattr(app, 'assess_individual'):
        return app.assess_individual(application_data)
    elif hasattr(app, 'make_decision'):
        return app.make_decision(application_data, 'individual')
    else:
        raise AttributeError("No assessment method found")

def quick_corporate_assessment(application_data, min_revenue=100000, max_debt_ratio=0.6):
    """
    Quick corporate credit assessment with default settings.
    
    Args:
        application_data (dict): Corporate application data
        min_revenue (float): Minimum acceptable annual revenue
        max_debt_ratio (float): Maximum debt-to-equity ratio
        
    Returns:
        CreditDecision: Assessment result
    """
    app = CreditApplication(min_revenue=min_revenue, max_debt_ratio=max_debt_ratio)
    # Try new method name first, fallback to existing method
    if hasattr(app, 'assess_corporate'):
        return app.assess_corporate(application_data)
    elif hasattr(app, 'make_decision'):
        return app.make_decision(application_data, 'corporate')
    else:
        raise AttributeError("No assessment method found")

# Add convenience functions to __all__
__all__.extend(["quick_individual_assessment", "quick_corporate_assessment"])

# Module-level configuration
import logging

# Set up default logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

# Package-level constants that work with your existing code
SUPPORTED_LOAN_PURPOSES = [
    'home_purchase', 'home_improvement', 'debt_consolidation', 
    'auto', 'personal', 'business', 'education'
]

SUPPORTED_BUSINESS_TYPES = [
    'sole_proprietorship', 'partnership', 'llc', 'corporation',
    'non_profit', 'cooperative'
]

# Risk level thresholds (matches your existing usage)
RISK_THRESHOLDS = {
    'low': 0.2,
    'medium': 0.5, 
    'high': 0.8
}

__all__.extend([
    "SUPPORTED_LOAN_PURPOSES",
    "SUPPORTED_BUSINESS_TYPES", 
    "RISK_THRESHOLDS"
])

# Package metadata for programmatic access
def get_package_info():
    """Return package information as a dictionary."""
    return {
        'name': 'credit-risk-creditum',
        'version': __version__,
        'author': __author__,
        'email': __email__,
        'description': __description__,
        'url': __url__,
        'supported_python': '>=3.8',
    }

__all__.append("get_package_info")