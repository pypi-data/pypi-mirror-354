from typing import Dict, Any, Optional, List

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
        # Only update with non-None values
        for key, value in indicator_data.items():
            if value is not None:
                self.indicators[key] = value
    
    def calculate_economic_risk_factor(self, entity_type: str = 'individual', 
                                     industry: Optional[str] = None) -> float:
        """
        Calculate economic risk factor based on entity type and industry.
        
        Args:
            entity_type (str): Type of entity ('individual' or 'corporate')
            industry (Optional[str]): Industry sector for corporate assessment
            
        Returns:
            float: Economic risk factor between 0 and 1
        """
        weights = self._get_economic_weights(entity_type)
        
        risk_factor = 0.0
        for indicator, weight in weights.items():
            if indicator == 'industry_growth' and industry:
                # Handle industry-specific growth
                industry_data = self.indicators.get('industry_growth', {})
                if isinstance(industry_data, dict):
                    value = industry_data.get(industry, 0.5)
                else:
                    value = 0.5
            else:
                # Get the indicator value, with proper default handling
                value = self.indicators.get(indicator, 0.5)
            
            # Ensure value is not None before multiplication
            if value is not None:
                risk_factor += float(value) * weight
            else:
                # Use default neutral value if indicator is missing
                risk_factor += 0.5 * weight
                
        return min(max(risk_factor, 0), 1)
    
    def _get_economic_weights(self, entity_type: str) -> Dict[str, float]:
        """
        Get economic factor weights based on entity type.
        
        Args:
            entity_type (str): Type of entity ('individual' or 'corporate')
            
        Returns:
            Dict[str, float]: Dictionary of indicator weights
        """
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
    
    def debug_indicators(self, entity_type: str = 'individual') -> None:
        """
        Debug method to check indicator status and help troubleshoot issues.
        
        Args:
            entity_type (str): Type of entity to debug ('individual' or 'corporate')
        """
        print(f"\n=== DEBUG: Economic Indicators for {entity_type.upper()} ===")
        
        weights = self._get_economic_weights(entity_type)
        print(f"Required indicators for {entity_type}:")
        
        missing_indicators = []
        none_indicators = []
        
        for indicator, weight in weights.items():
            value = self.indicators.get(indicator, "MISSING")
            status = "✓" if value != "MISSING" and value is not None else "✗"
            
            if value == "MISSING":
                missing_indicators.append(indicator)
            elif value is None:
                none_indicators.append(indicator)
                
            print(f"  {status} {indicator}: {value} (weight: {weight})")
        
        print(f"\nSummary:")
        print(f"  Total indicators stored: {len(self.indicators)}")
        print(f"  Stored indicators: {list(self.indicators.keys())}")
        print(f"  Required indicators: {list(weights.keys())}")
        
        if missing_indicators:
            print(f"  ⚠️  Missing indicators: {missing_indicators}")
        if none_indicators:
            print(f"  ⚠️  None value indicators: {none_indicators}")
            
        if not missing_indicators and not none_indicators:
            print(f"  ✅ All indicators properly set!")
            
        # Test calculation
        try:
            risk_factor = self.calculate_economic_risk_factor(entity_type)
            print(f"  ✅ Risk factor calculation successful: {risk_factor:.3f}")
        except Exception as e:
            print(f"  ❌ Risk factor calculation failed: {e}")
        
        print("=" * 50)
    
    def get_indicator_value(self, indicator: str, default: Any = None) -> Any:
        """
        Get a specific indicator value.
        
        Args:
            indicator (str): Name of the indicator
            default (Any): Default value if indicator not found
            
        Returns:
            Any: Indicator value or default
        """
        return self.indicators.get(indicator, default)
    
    def list_available_indicators(self) -> List[str]:
        """
        Get list of all available indicators.
        
        Returns:
            List[str]: List of indicator names
        """
        return list(self.indicators.keys())
    
    def clear_indicators(self) -> None:
        """Clear all stored indicators."""
        self.indicators.clear()
    
    def get_indicators_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all indicators.
        
        Returns:
            Dict[str, Any]: Summary information
        """
        return {
            'total_indicators': len(self.indicators),
            'indicator_names': list(self.indicators.keys()),
            'individual_required': list(self._get_economic_weights('individual').keys()),
            'corporate_required': list(self._get_economic_weights('corporate').keys()),
            'indicators': dict(self.indicators)  # Copy of current indicators
        }