import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .domain.lead_metrics import LeadMetrics

@csrf_exempt
def lead_metrics_api(request):
    """
    Endpoint para calcular métricas de leads.
    Soporta POST.
    Ruta esperada: /api/lead-metrics
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            metric_type = data.get('type')
            
            metrics = LeadMetrics()
            
            if metric_type == 'conversion':
                total = data.get('total_leads')
                converted = data.get('converted_leads')
                if total is None or converted is None:
                    return JsonResponse({'error': 'Faltan parámetros total_leads o converted_leads'}, status=400)
                
                result = metrics.calculate_conversion_rate(int(total), int(converted))
                return JsonResponse({'success': True, 'conversion_rate': result})
                
            elif metric_type == 'score':
                interactions = data.get('interactions', 0)
                has_budget = data.get('has_budget', False)
                profile_complete = data.get('profile_complete', False)
                
                score = metrics.calculate_lead_score(int(interactions), bool(has_budget), bool(profile_complete))
                return JsonResponse({'success': True, 'lead_score': score})
            
            else:
                return JsonResponse({'error': 'Tipo de métrica no válido (conversion/score)'}, status=400)

        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception:
            return JsonResponse({'error': 'Error interno'}, status=500)
            
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def health_check(request):
    """Check simple para ver si la API responde"""
    return JsonResponse({'status': 'ok', 'service': 'PromptSales CRM', 'domain': 'LeadMetrics'})
