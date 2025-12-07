import pytest
import requests

BASE_URL = "http://localhost:8000"

@pytest.mark.api
class TestPromptCrmAPI:
    
    def test_health_check_read(self):
        """[Lectura] Verifica endpoint de salud"""
        try:
            response = requests.get(f"{BASE_URL}/api/health", timeout=2)
            assert response.status_code == 200
            data = response.json()
            assert data['domain'] == 'LeadMetrics'
        except requests.exceptions.ConnectionError:
            pytest.skip("Server Django no corriendo.")

    def test_lead_metrics_conversion(self):
        """[Escritura] Verifica cálculo de conversión"""
        payload = {
            "type": "conversion",
            "total_leads": 100,
            "converted_leads": 25
        }
        
        try:
            response = requests.post(f"{BASE_URL}/api/lead-metrics", json=payload, timeout=2)
            assert response.status_code == 200
            data = response.json()
            assert data['success'] is True
            assert data['conversion_rate'] == 25.0
        except requests.exceptions.ConnectionError:
            pytest.skip("Server Django no corriendo.")

    def test_lead_metrics_score(self):
        """[Escritura] Verifica cálculo de puntaje"""
        payload = {
            "type": "score",
            "interactions": 5,
            "has_budget": True,
            "profile_complete": False
        }
        # 5*5 = 25 + 30 + 0 = 55
        try:
            response = requests.post(f"{BASE_URL}/api/lead-metrics", json=payload, timeout=2)
            assert response.status_code == 200
            data = response.json()
            assert data['success'] is True
            assert data['lead_score'] == 55
        except requests.exceptions.ConnectionError:
            pytest.skip("Server Django no corriendo.")
