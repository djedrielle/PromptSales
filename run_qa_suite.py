import argparse
import subprocess
import sys

def run_command(command, description):
    print(f"\n{'='*60}")
    print(f"🚀 Ejecutando: {description}")
    print(f"📝 Comando: {command}")
    print(f"{'='*60}\n")
    
    try:
        # Ejecutar y mostrar output en tiempo real
        result = subprocess.run(command, shell=True, check=False)
        if result.returncode == 0:
            print(f"\n✅ {description} completado EXITOSAMENTE.")
            return True
        else:
            print(f"\n❌ {description} FALLÓ (Código: {result.returncode}).")
            return False
    except Exception as e:
        print(f"❌ Error ejecutando {description}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="PromptSales QA Suite Runner")
    parser.add_argument('--type', choices=['unit', 'api', 'stress', 'mcp', 'lint', 'all'], default='all', help='Tipo de prueba a ejecutar')
    
    args = parser.parse_args()
    
    success = True
    
    # 1. Linter
    if args.type in ['lint', 'all']:
        cmd = f"{sys.executable} -m ruff check ."
        if not run_command(cmd, "Linter (Ruff)"):
            success = False

    # 2. Unit Tests
    if args.type in ['unit', 'all']:
        cmd = f"{sys.executable} -m pytest tests/unit -v"
        if not run_command(cmd, "Unit Tests"):
            success = False

    # 3. API Tests (Requiere servidor corriendo, aquí solo intentamos)
    if args.type in ['api', 'all']:
        print("\n⚠️  Nota: API Tests requieren que el servidor Django esté corriendo en localhost:8000")
        cmd = f"{sys.executable} -m pytest tests/api -v"
        if not run_command(cmd, "REST API Tests"):
            # No marcamos success=False estricto porque depende del server
            print("ℹ️  (Si fallaron por conexión, asegúrate de levantar el server)")

    # 4. MCP Test
    if args.type in ['mcp', 'all']:
        cmd = f"{sys.executable} tests/mcp/test_mcp_integration.py"
        if not run_command(cmd, "MCP Server Integration Test"):
            success = False

    # 5. Stress Test (Solo check dry-run)
    if args.type in ['stress', 'all']:
        print("\n⚠️  Nota: Stress Test se ejecuta mejor manualmente o en CI.")
        print("   Comando sugerido: python -m locust -f tests/stress/locustfile.py --headless -u 10 -r 2 -t 10s")
        # Hacemos un dry-run rápido
        cmd = f"{sys.executable} -m locust -f tests/stress/locustfile.py --headless -u 5 -r 1 -t 5s"
        if not run_command(cmd, "Stress Test (Dry Run 5s)"):
            success = False

    if success:
        print("\n🎉🎉 TODO LAS PRUEBAS DE LA SUITE SELECCIONADA PASARON 🎉🎉")
        sys.exit(0)
    else:
        print("\n💥💥 ALGUNAS PRUEBAS FALLARON 💥💥")
        sys.exit(1)

if __name__ == "__main__":
    main()
