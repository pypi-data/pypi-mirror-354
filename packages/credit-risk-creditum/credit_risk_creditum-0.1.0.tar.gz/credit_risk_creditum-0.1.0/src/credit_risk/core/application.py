import numpy as np
from typing import Dict, Any, Tuple

from ..core.economic import EconomicIndicators
from ..models.individual import IndividualRiskAssessment
from ..models.corporate import CorporateRiskAssessment

class CreditApplication:
    """Handle credit applications and make approval decisions"""
    
    def __init__(self, min_credit_score: int = 600, max_dti: float = 0.43):
        self.min_credit_score = min_credit_score
        self.max_dti = max_dti
        self.economic_indicators = EconomicIndicators()
        self.individual_assessment = IndividualRiskAssessment(self.economic_indicators)
        self.corporate_assessment = CorporateRiskAssessment(self.economic_indicators)
    
    def validate_application(self, application_data: Dict[str, Any], 
                           entity_type: str = 'individual') -> Tuple[bool, str]:
        """Validate credit application data"""
        required_fields = self._get_required_fields(entity_type)
        
        for field in required_fields:
            if field not in application_data:
                return False, f"Missing required field: {field}"
        
        if entity_type == 'individual':
            return self._validate_individual(application_data)
        return self._validate_corporate(application_data)
    
    def _validate_individual(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate individual application"""
        if data['credit_score'] < self.min_credit_score:
            return False, "Credit score below minimum requirement"
        
        dti = self._calculate_dti(data['monthly_debt'], data['monthly_income'])
        if dti > self.max_dti:
            return False, "Debt-to-income ratio too high"
        
        return True, "Application valid"
    
    def _validate_corporate(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate corporate application"""
        if data['years_in_business'] < 2:
            return False, "Minimum 2 years in business required"
        
        if data['annual_revenue'] < 100000:
            return False, "Minimum annual revenue requirement not met"
        
        return True, "Application valid"
    
    @staticmethod
    def _get_required_fields(entity_type: str) -> list:
        """Get required fields based on entity type"""
        if entity_type == 'individual':
            return [
                'credit_score',
                'monthly_income',
                'monthly_debt',
                'loan_amount',
                'loan_purpose'
            ]
        return [
            'years_in_business',
            'annual_revenue',
            'industry',
            'loan_amount',
            'loan_purpose'
        ]
    
    @staticmethod
    def _calculate_dti(monthly_debt: float, monthly_income: float) -> float:
        """Calculate Debt-to-Income ratio"""
        return np.where(monthly_income > 0, monthly_debt / monthly_income, np.inf)
    
    def make_decision(self, application_data: Dict[str, Any], 
                     entity_type: str = 'individual') -> Dict[str, Any]:
        """Make credit approval decision"""
        is_valid, message = self.validate_application(application_data, entity_type)
        if not is_valid:
            return {
                'decision': 'rejected',
                'reason': message,
                'risk_score': None
            }
        
        # Calculate risk score based on entity type
        if entity_type == 'individual':
            risk_score = self.individual_assessment.calculate_risk_score(application_data)
            assessor = self.individual_assessment
        else:
            risk_score = self.corporate_assessment.calculate_risk_score(application_data)
            assessor = self.corporate_assessment
        
        risk_category = self._get_risk_category(risk_score)
        
        return {
            'decision': 'approved' if risk_category != 'high' else 'rejected',
            'risk_score': risk_score,
            'risk_category': risk_category,
            'max_loan_amount': self._calculate_max_loan_amount(
                application_data,
                risk_score,
                entity_type
            ) if risk_category != 'high' else 0,
            'economic_factor': self.economic_indicators.calculate_economic_risk_factor(
                entity_type,
                industry=application_data.get('industry')
            )
        }
    
    def _calculate_max_loan_amount(self, application_data: Dict[str, Any],
                                risk_score: float, entity_type: str) -> float:
        """Calculate maximum loan amount"""
        if entity_type == 'individual':
            base_max = application_data['monthly_income'] * 36
        else:
            base_max = application_data['annual_revenue'] * 0.5
        
        risk_multiplier = 1 - risk_score
        return base_max * risk_multiplier
    
    def _get_risk_category(self, risk_score: float) -> str:
        """Determine risk category based on risk score"""
        if risk_score <= 0.3:
            return 'low'
        elif risk_score <= 0.6:
            return 'medium'
        return 'high'