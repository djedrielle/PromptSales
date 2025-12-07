class LeadMetrics:
    """
    Calculadora de métricas para Leads en el CRM.
    Permite evaluar la calidad y rendimiento de los leads.
    """
    
    def calculate_conversion_rate(self, total_leads: int, converted_leads: int) -> float:
        """
        Calcula la tasa de conversión como porcentaje.
        """
        if total_leads < 0 or converted_leads < 0:
            raise ValueError("Los valores no pueden ser negativos")
            
        if total_leads == 0:
            return 0.0
            
        if converted_leads > total_leads:
            raise ValueError("Los leads convertidos no pueden ser mayores al total")
            
        return round((converted_leads / total_leads) * 100, 2)

    def calculate_lead_score(self, interactions: int, has_budget: bool, profile_complete: bool) -> int:
        """
        Calcula un puntaje (0-100) para un lead basado en su comportamiento y perfil.
        """
        if interactions < 0:
            raise ValueError("Las interacciones no pueden ser negativas")
            
        score = 0
        
        # 1. Puntos por interacciones (max 50)
        interaction_points = interactions * 5
        score += min(interaction_points, 50)
        
        # 2. Presupuesto confirmado (30 puntos)
        if has_budget:
            score += 30
            
        # 3. Perfil completo (20 puntos)
        if profile_complete:
            score += 20
            
        return score
