"""
Test de Seguridad - Validación de Permisos Grant/Deny

Este módulo implementa pruebas de seguridad para validar:
1. Acceso DENEGADO sin autenticación (401)
2. Acceso DENEGADO con API key inválida (403)
3. Acceso DENEGADO con permisos insuficientes (403)
4. Acceso PERMITIDO con API key válida y permisos correctos (200)
"""

import pytest
import requests

BASE_URL = "http://localhost:8000"
PROTECTED_ENDPOINT = f"{BASE_URL}/api/admin/stats"

# API Keys de prueba (deben coincidir con las definidas en views.py)
ADMIN_KEY = "admin-key-12345"
READONLY_KEY = "readonly-key-67890"
INVALID_KEY = "fake-key-99999"


def server_is_running():
    """Verifica si el servidor Django está corriendo."""
    try:
        requests.get(f"{BASE_URL}/api/health", timeout=2)
        return True
    except requests.exceptions.ConnectionError:
        return False


@pytest.mark.security
class TestSecurityPermissions:
    """
    Suite de pruebas de seguridad para validar autenticación y autorización.
    """
    
    @pytest.fixture(autouse=True)
    def check_server(self):
        """Skip tests si el servidor no está corriendo."""
        if not server_is_running():
            pytest.skip("Server Django no corriendo. Ejecuta: cd src/PromptCrmDomain && python manage.py runserver")

    def test_access_denied_no_auth(self):
        """
        TEST 1: Acceso DENEGADO sin header Authorization.
        Esperado: 401 Unauthorized
        """
        response = requests.get(PROTECTED_ENDPOINT)
        
        assert response.status_code == 401, f"Esperado 401, recibido {response.status_code}"
        
        data = response.json()
        assert 'error' in data
        assert 'Missing Authorization' in data['error']
        
        print("✅ TEST PASSED: Sin auth -> 401 (acceso denegado)")

    def test_access_denied_invalid_key(self):
        """
        TEST 2: Acceso DENEGADO con API key inválida.
        Esperado: 403 Forbidden
        """
        headers = {"Authorization": f"Bearer {INVALID_KEY}"}
        response = requests.get(PROTECTED_ENDPOINT, headers=headers)
        
        assert response.status_code == 403, f"Esperado 403, recibido {response.status_code}"
        
        data = response.json()
        assert 'error' in data
        assert 'Invalid API key' in data['error']
        
        print("✅ TEST PASSED: Key inválida -> 403 (acceso denegado)")

    def test_access_denied_insufficient_permissions(self):
        """
        TEST 3: Acceso DENEGADO con permisos insuficientes.
        El usuario 'readonly' tiene solo permiso 'read', pero el endpoint requiere 'write'.
        Esperado: 403 Forbidden
        """
        headers = {"Authorization": f"Bearer {READONLY_KEY}"}
        response = requests.get(PROTECTED_ENDPOINT, headers=headers)
        
        assert response.status_code == 403, f"Esperado 403, recibido {response.status_code}"
        
        data = response.json()
        assert 'error' in data
        assert 'insufficient permissions' in data['error']
        assert data.get('required') == 'write'
        assert 'read' in data.get('your_permissions', [])
        
        print("✅ TEST PASSED: Permisos insuficientes -> 403 (acceso denegado)")

    def test_access_granted_valid_admin(self):
        """
        TEST 4: Acceso PERMITIDO con API key de admin válida.
        El admin tiene permisos ['read', 'write', 'delete'].
        Esperado: 200 OK con datos
        """
        headers = {"Authorization": f"Bearer {ADMIN_KEY}"}
        response = requests.get(PROTECTED_ENDPOINT, headers=headers)
        
        assert response.status_code == 200, f"Esperado 200, recibido {response.status_code}"
        
        data = response.json()
        assert data.get('success') is True
        assert data.get('user_role') == 'admin'
        assert 'stats' in data
        assert data['stats'].get('total_leads') == 1250
        
        print("✅ TEST PASSED: Admin válido -> 200 (acceso permitido)")

    def test_invalid_auth_format(self):
        """
        TEST 5: Acceso DENEGADO con formato de Authorization incorrecto.
        Esperado: 401 Unauthorized
        """
        # Sin prefijo 'Bearer'
        headers = {"Authorization": ADMIN_KEY}
        response = requests.get(PROTECTED_ENDPOINT, headers=headers)
        
        assert response.status_code == 401, f"Esperado 401, recibido {response.status_code}"
        
        data = response.json()
        assert 'Invalid Authorization format' in data['error']
        
        print("✅ TEST PASSED: Formato inválido -> 401 (acceso denegado)")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🔐 EJECUTANDO TESTS DE SEGURIDAD")
    print("=" * 60)
    
    if not server_is_running():
        print("❌ Error: El servidor Django no está corriendo.")
        print("💡 Ejecuta: cd src/PromptCrmDomain && python manage.py runserver")
        exit(1)
    
    # Ejecutar tests manualmente
    test_suite = TestSecurityPermissions()
    test_suite.check_server = lambda: None  # Skip fixture
    
    tests = [
        ("Sin autenticación", test_suite.test_access_denied_no_auth),
        ("API key inválida", test_suite.test_access_denied_invalid_key),
        ("Permisos insuficientes", test_suite.test_access_denied_insufficient_permissions),
        ("Admin válido (GRANT)", test_suite.test_access_granted_valid_admin),
        ("Formato inválido", test_suite.test_invalid_auth_format),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            print(f"\n📋 Test: {name}")
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"❌ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ ERROR: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"🔐 RESULTADOS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    exit(0 if failed == 0 else 1)
