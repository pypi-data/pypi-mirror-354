import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from ..core.economic import EconomicIndicators

class BaseRiskAssessment:
    """Base class for risk assessment with common functionality"""
    def __init__(self, economic_indicators: EconomicIndicators):
        self.economic_indicators = economic_indicators
        self.scaler = StandardScaler()
        self.model = None
        self.risk_thresholds = {
            'low': 0.3,
            'medium': 0.6,
            'high': 0.8
        }
    
    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preprocess raw credit data"""
        processed_df = df.copy()
        
        numeric_columns = processed_df.select_dtypes(include=['float64', 'int64']).columns
        categorical_columns = processed_df.select_dtypes(include=['object']).columns
        
        for col in numeric_columns:
            processed_df[col].fillna(processed_df[col].median(), inplace=True)
        
        for col in categorical_columns:
            processed_df[col].fillna(processed_df[col].mode()[0], inplace=True)
        
        processed_df = pd.get_dummies(processed_df, columns=categorical_columns)
        
        return processed_df
    
    def train_model(self, X, y, model_type: str = 'random_forest'):
        """Train risk prediction model"""
        X_scaled = self.scaler.fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )
        
        self.model = (
            RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
            if model_type == 'random_forest'
            else LogisticRegression(random_state=42, max_iter=1000)
        )
        
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        print("\nModel Performance:")
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        return self.model
    
    def predict_risk(self, features):
        """Predict risk using trained model"""
        if self.model is None:
            raise ValueError("Model not trained. Please train the model first.")
        
        features_scaled = self.scaler.transform(features)
        return self.model.predict_proba(features_scaled)