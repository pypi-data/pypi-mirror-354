from typing import Dict, Any, Optional

class EconomicIndicators:
    """
    Handle economic indicators and their impact on credit risk assessment.

    This class manages various economic indicators such as CPI, GDP growth,
    unemployment rate, etc., and calculates their impact on credit risk.

    Attributes:
        indicators (dict): Dictionary storing current economic indicators.
    """
    
    def __init__(self):
        self.indicators = {}

    def update_indicators(self, indicator_data: Dict[str, Any]) -> None:
        """
        Update economic indicators with current data.

        Args:
            indicator_data (Dict[str, Any]): Dictionary containing economic indicators.
                Expected keys:
                - cpi (float): Consumer Price Index
                - gdp_growth (float): GDP growth rate
                - unemployment_rate (float): Unemployment rate
                - interest_rate (float): Current interest rate
                - inflation_rate (float): Inflation rate
                - industry_growth (Dict[str, float]): Growth rates by industry
                - market_volatility (float): Market volatility index
                - currency_stability (float): Currency stability index

        Example:
            >>> economic = EconomicIndicators()
            >>> data = {
            ...     'cpi': 0.02,
            ...     'gdp_growth': 0.03,
            ...     'unemployment_rate': 0.05
            ... }
            >>> economic.update_indicators(data)
        """
        self.indicators.update({
            'cpi': indicator_data.get('cpi', None),
            'gdp_growth': indicator_data.get('gdp_growth', None),
            'unemployment_rate': indicator_data.get('unemployment_rate', None),
            'interest_rate': indicator_data.get('interest_rate', None),
            'inflation_rate': indicator_data.get('inflation_rate', None),
            'industry_growth': indicator_data.get('industry_growth', {}),
            'market_volatility': indicator_data.get('market_volatility', None),
            'currency_stability': indicator_data.get('currency_stability', None)
        })
    
    def calculate_economic_risk_factor(self, entity_type: str = 'individual', 
                                     industry: Optional[str] = None) -> float:
        """Calculate economic risk factor based on entity type and industry"""
        weights = self._get_economic_weights(entity_type)
        
        risk_factor = 0.0
        for indicator, weight in weights.items():
            if indicator == 'industry_growth' and industry:
                value = self.indicators.get(indicator, {}).get(industry, 0.5)
            else:
                value = self.indicators.get(indicator, 0.5)
            risk_factor += value * weight
            
        return min(max(risk_factor, 0), 1)
    
    def _get_economic_weights(self, entity_type: str) -> Dict[str, float]:
        """Get economic factor weights based on entity type"""
        if entity_type == 'individual':
            return {
                'cpi': 0.3,
                'unemployment_rate': 0.3,
                'interest_rate': 0.2,
                'inflation_rate': 0.2
            }
        return {
            'gdp_growth': 0.2,
            'industry_growth': 0.3,
            'interest_rate': 0.2,
            'market_volatility': 0.15,
            'currency_stability': 0.15
        }


class CreditApplication:
    """
    Handle credit applications and make approval decisions.

    This class processes both individual and corporate credit applications,
    incorporating economic factors and risk assessments to make lending decisions.

    Args:
        min_credit_score (int): Minimum required credit score. Defaults to 600.
        max_dti (float): Maximum allowed debt-to-income ratio. Defaults to 0.43.

    Attributes:
        economic_indicators (EconomicIndicators): Economic data manager
        individual_assessment (IndividualRiskAssessment): Individual risk calculator
        corporate_assessment (CorporateRiskAssessment): Corporate risk calculator
    """

    def make_decision(self, application_data: Dict[str, Any], 
                     entity_type: str = 'individual') -> Dict[str, Any]:
        """
        Make credit approval decision based on application data.

        Args:
            application_data (Dict[str, Any]): Application information including:
                For individuals:
                    - credit_score (int)
                    - monthly_income (float)
                    - monthly_debt (float)
                    - loan_amount (float)
                    - loan_purpose (str)
                For corporations:
                    - years_in_business (int)
                    - annual_revenue (float)
                    - industry (str)
                    - loan_amount (float)
                    - loan_purpose (str)
            entity_type (str): Type of entity ('individual' or 'corporate').
                Defaults to 'individual'.

        Returns:
            Dict[str, Any]: Decision result containing:
                - decision (str): 'approved' or 'rejected'
                - risk_score (float): Calculated risk score
                - risk_category (str): 'low', 'medium', or 'high'
                - max_loan_amount (float): Maximum approved loan amount
                - economic_factor (float): Impact of economic conditions

        Example:
            >>> app = CreditApplication()
            >>> data = {
            ...     'credit_score': 720,
            ...     'monthly_income': 5000,
            ...     'monthly_debt': 1500,
            ...     'loan_amount': 20000,
            ...     'loan_purpose': 'home_improvement'
            ... }
            >>> result = app.make_decision(data, 'individual')
        """
        # Implementation would go here
        pass