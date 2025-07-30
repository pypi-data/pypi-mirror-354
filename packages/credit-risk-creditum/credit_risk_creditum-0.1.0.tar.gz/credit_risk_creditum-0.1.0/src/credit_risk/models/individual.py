from typing import Dict, Any
from .base import BaseRiskAssessment
from ..core.economic import EconomicIndicators

class IndividualRiskAssessment(BaseRiskAssessment):
    """Handle individual credit risk assessment"""
    
    def __init__(self, economic_indicators: EconomicIndicators):
        super().__init__(economic_indicators)
        self.weights = {
            'payment_history': 0.30,
            'credit_utilization': 0.25,
            'credit_history_length': 0.15,
            'income_stability': 0.15,
            'debt_to_income': 0.15
        }
    
    def calculate_risk_score(self, features: Dict[str, Any]) -> float:
        """Calculate individual risk score with economic factors"""
        base_score = sum(features.get(k, 0) * v for k, v in self.weights.items())
        economic_factor = self.economic_indicators.calculate_economic_risk_factor('individual')
        final_score = base_score * (1 - economic_factor * 0.3)
        return min(max(final_score, 0), 1)