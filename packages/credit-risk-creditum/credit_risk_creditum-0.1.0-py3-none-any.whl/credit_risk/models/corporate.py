from typing import Dict, Any
from .base import BaseRiskAssessment
from ..core.economic import EconomicIndicators

class CorporateRiskAssessment(BaseRiskAssessment):
    """Handle corporate credit risk assessment"""
    
    def __init__(self, economic_indicators: EconomicIndicators):
        super().__init__(economic_indicators)
        self.weights = {
            'financial_ratios': 0.25,
            'market_position': 0.20,
            'operational_efficiency': 0.15,
            'management_quality': 0.15,
            'business_model': 0.15,
            'regulatory_compliance': 0.10
        }
    
    def calculate_risk_score(self, features: Dict[str, Any]) -> float:
        """Calculate corporate risk score with economic factors"""
        base_score = sum(features.get(k, 0) * v for k, v in self.weights.items())
        economic_factor = self.economic_indicators.calculate_economic_risk_factor(
            'corporate', 
            industry=features.get('industry')
        )
        final_score = base_score * (1 - economic_factor * 0.4)
        return min(max(final_score, 0), 1)