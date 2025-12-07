
import subprocess
import json
import sys
import time

def test_mcp_server():
    """
    Prueba de integración automática para el servidor MCP corriendo en Docker.
    Se comunica con el contenedor 'promptsales-mcp' via docker exec.
    
    Prerequisitos:
    - Docker Compose levantado: docker-compose up -d
    - Contenedor 'promptsales-mcp' corriendo
    """
    
    container_name = "promptsales-mcp"
    
    # Verificar que el contenedor está corriendo
    print(f"🔍 Verificando que el contenedor '{container_name}' está corriendo...")
    
    check_result = subprocess.run(
        ["docker", "inspect", "-f", "{{.State.Running}}", container_name],
        capture_output=True,
        text=True
    )
    
    if check_result.returncode != 0 or "true" not in check_result.stdout.lower():
        print(f"❌ El contenedor '{container_name}' no está corriendo.")
        print("💡 Tip: Ejecuta 'docker-compose up -d' desde la raíz del proyecto.")
        return False
    
    print(f"✅ Contenedor '{container_name}' está corriendo.")
    
    # Ejecutar el servidor MCP dentro del contenedor y comunicarse via stdin/stdout
    # Usamos docker exec -i para interactuar con el proceso
    print("🚀 Conectando al servidor MCP en el contenedor...")
    
    process = subprocess.Popen(
        ["docker", "exec", "-i", container_name, "node", "dist/index.js"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0
    )
    
    # Dar tiempo al servidor para inicializar
    time.sleep(2)
    
    # 1. Test: Initialize (Handshake)
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "TestClient", "version": "1.0"}
        }
    }
    
    try:
        print("📤 Enviando handshake 'initialize'...")
        process.stdin.write(json.dumps(init_request) + "\n")
        process.stdin.flush()
        
        # Esperar respuesta con timeout
        
        # Leer respuesta
        output = process.stdout.readline()
        
        if not output:
            stderr = process.stderr.read()
            print(f"❌ El servidor no respondió. Stderr: {stderr[:500] if stderr else 'vacío'}")
            return False
        
        response = json.loads(output)
        
        # Validaciones
        if response.get("id") == 1 and "result" in response:
            server_name = response["result"].get("serverInfo", {}).get("name")
            print(f"✅ Handshake exitoso! Conectado a: {server_name}")
        else:
            print(f"❌ Respuesta inválida: {response}")
            return False

        # 2. Test: List Tools
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        print("📤 Solicitando lista de herramientas (tools/list)...")
        process.stdin.write(json.dumps(tools_request) + "\n")
        process.stdin.flush()
        
        output = process.stdout.readline()
        response = json.loads(output)
        
        if response.get("id") == 2 and "result" in response:
            tools = response["result"].get("tools", [])
            tool_names = [t["name"] for t in tools]
            print(f"✅ Tools disponibles ({len(tools)}): {tool_names}")
            
            # Corroboración automática según enunciado
            if len(tools) > 0:
                print(f"✅ CORROBORACIÓN AUTOMÁTICA: El servidor MCP tiene {len(tools)} herramientas registradas.")
            else:
                print("⚠️  Advertencia: No se detectaron herramientas en el servidor.")
        else:
            print(f"❌ Fallo al listar tools: {response}")
            return False

        print("\n🎉 TEST DE MCP SERVER COMPLETADO EXITOSAMENTE 🎉")
        return True

    except json.JSONDecodeError as e:
        print(f"❌ Error parseando respuesta JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Excepción durante el test: {str(e)}")
        return False
    finally:
        process.terminate()

if __name__ == "__main__":
    success = test_mcp_server()
    sys.exit(0 if success else 1)
