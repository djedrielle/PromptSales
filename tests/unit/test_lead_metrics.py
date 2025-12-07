import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/PromptCrmDomain')))

from crm.domain.lead_metrics import LeadMetrics

class TestLeadMetrics:
    
    def setup_method(self):
        self.metrics = LeadMetrics()
        
    def test_conversion_rate_basic(self):
        """Prueba cálculo de conversión normal"""
        rate = self.metrics.calculate_conversion_rate(100, 20)
        assert rate == 20.0

    def test_conversion_rate_zero_leads(self):
        """Si hay 0 leads, la conversión es 0"""
        rate = self.metrics.calculate_conversion_rate(0, 0)
        assert rate == 0.0

    def test_conversion_rate_invalid(self):
        """Error si convertidos > total"""
        with pytest.raises(ValueError):
            self.metrics.calculate_conversion_rate(10, 20)

    def test_lead_score_max(self):
        """Puntaje máximo con muchas interacciones"""
        # 20 interacciones * 5 = 100 (cap en 50) + 30 + 20 = 100
        score = self.metrics.calculate_lead_score(20, True, True)
        assert score == 100

    def test_lead_score_partial(self):
        """Puntaje con pocas interacciones y sin presupuesto"""
        # 2 interacciones * 5 = 10 + 0 + 20 = 30
        score = self.metrics.calculate_lead_score(2, False, True)
        assert score == 30

    def test_negative_values(self):
        """Validar error con negativos"""
        with pytest.raises(ValueError):
            self.metrics.calculate_lead_score(-1, True, True)
