import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .domain.lead_metrics import LeadMetrics

# API Key válida para autenticación (en producción esto estaría en variables de entorno)
VALID_API_KEYS = {
    "admin-key-12345": {"role": "admin", "permissions": ["read", "write", "delete"]},
    "readonly-key-67890": {"role": "viewer", "permissions": ["read"]},
}


def check_api_key(request):
    """
    Verifica la API key en el header Authorization.
    Retorna (is_valid, user_info, error_response)
    """
    auth_header = request.headers.get('Authorization', '')
    
    if not auth_header:
        return False, None, JsonResponse(
            {'error': 'Missing Authorization header'}, 
            status=401
        )
    
    # Formato esperado: "Bearer <api_key>"
    parts = auth_header.split(' ')
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return False, None, JsonResponse(
            {'error': 'Invalid Authorization format. Use: Bearer <api_key>'}, 
            status=401
        )
    
    api_key = parts[1]
    
    if api_key not in VALID_API_KEYS:
        return False, None, JsonResponse(
            {'error': 'Invalid API key'}, 
            status=403
        )
    
    return True, VALID_API_KEYS[api_key], None


def check_permission(user_info, required_permission):
    """Verifica si el usuario tiene el permiso requerido."""
    return required_permission in user_info.get('permissions', [])


@csrf_exempt
def admin_stats(request):
    """
    Endpoint PROTEGIDO que requiere autenticación y permisos de admin.
    Ruta: /api/admin/stats
    
    - Requiere header: Authorization: Bearer <api_key>
    - Requiere permiso: 'write' (solo admins)
    
    Este endpoint demuestra validación de permisos grant/deny.
    """
    # 1. Verificar autenticación (API key válida)
    is_valid, user_info, error_response = check_api_key(request)
    if not is_valid:
        return error_response
    
    # 2. Verificar autorización (permiso 'write' requerido)
    if not check_permission(user_info, 'write'):
        return JsonResponse(
            {
                'error': 'Forbidden: insufficient permissions',
                'required': 'write',
                'your_permissions': user_info.get('permissions', [])
            }, 
            status=403
        )
    
    # 3. Si pasa autenticación y autorización, retornar datos
    return JsonResponse({
        'success': True,
        'message': 'Access granted to admin stats',
        'user_role': user_info.get('role'),
        'stats': {
            'total_leads': 1250,
            'active_campaigns': 15,
            'conversion_rate': 23.5
        }
    })


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

