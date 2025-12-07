from locust import HttpUser, task, between, constant
import random

class PromptSalesUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://localhost:8000"

    @task(3)
    def check_health(self):
        self.client.get("/api/health")

    @task(1)
    def calculate_lead_score(self):
        """Simula cálculo de score de leads"""
        payload = {
            "type": "score",
            "interactions": random.randint(1, 15),
            "has_budget": random.choice([True, False]),
            "profile_complete": random.choice([True, False])
        }
        
        with self.client.post("/api/lead-metrics", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                if response.json().get("success"):
                    response.success()
                else:
                    response.failure("Success false")
            else:
                response.failure(f"Status {response.status_code}")

class AggressiveBot(HttpUser):
    wait_time = constant(0.1)
    
    @task
    def spam_metrics(self):
        self.client.post("/api/lead-metrics", json={
            "type": "conversion",
            "total_leads": 1000,
            "converted_leads": 500
        })
