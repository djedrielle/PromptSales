# 🐳 Stress Testing con Locust + Docker

## 🎯 Arquitectura

```
┌─────────────────┐
│   Tu PC         │
│  (Master)       │ ← Interfaz Web (localhost:8089)
│  localhost:8089 │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼────┐
│Worker1│ │Worker2│  ← Contenedores Docker
│Docker │ │Docker │     (Generan carga HTTP)
└───┬───┘ └──┬────┘
    │        │
    └────┬───┘
         │
    ┌────▼────────┐
    │  Django API │ ← Tu servidor en localhost:8000
    │localhost:8000│
    └─────────────┘
```

---

## 🚀 Configuración: Master en tu PC, Workers en Docker

### **Paso 1: Iniciar Master en tu PC**

```bash
cd c:\Users\djedr\OneDrive\Documentos\TEC\Sem4\Diseño\caso2\PromptSales
python -m locust -f tests/stress/locustfile.py --master
```

### **Paso 2: Obtener tu IP local**

```powershell
ipconfig
```

Busca tu IPv4 Address (ej: `192.168.1.100`)

### **Paso 3: Crear Worker(s) en Docker**

**Comando único (sin Dockerfile):**

```bash
docker run --rm \
  -v ${PWD}/tests/stress:/locust \
  locustio/locust:latest \
  -f /locust/locustfile.py \
  --worker \
  --master-host=192.168.1.100
```

**Reemplaza** `192.168.1.100` con tu IP real del Paso 2.

### **Para múltiples workers:**

Ejecuta el comando en terminales diferentes:

```bash
# Worker 1
docker run --rm -v ${PWD}/tests/stress:/locust locustio/locust:latest -f /locust/locustfile.py --worker --master-host=192.168.1.100

# Worker 2
docker run --rm -v ${PWD}/tests/stress:/locust locustio/locust:latest -f /locust/locustfile.py --worker --master-host=192.168.1.100

# Worker 3
docker run --rm -v ${PWD}/tests/stress:/locust locustio/locust:latest -f /locust/locustfile.py --worker --master-host=192.168.1.100
```

### **Paso 4: Verificar conexión**

En la interfaz web (http://localhost:8089), verás:
```
Workers: X connected
```

---

## � Workers en Otra Computadora

**Para cumplir con:** *"una computadora ejecutando el test y otra computadora mínimo soportando la infraestructura"*

### **PC 1 (Tu PC):**
- Master de Locust (interfaz web)
- Servidor Django (localhost:8000)

### **PC 2 (Otra PC con Docker):**

```bash
docker run --rm \
  -v /ruta/a/tests/stress:/locust \
  locustio/locust:latest \
  -f /locust/locustfile.py \
  --worker \
  --master-host=<IP_DE_PC1>
```

---

## 🔍 Troubleshooting

**Workers no se conectan:**
1. Verifica firewall (puerto 5557)
2. Usa IP correcta (no `localhost`)
3. Ambas PCs en la misma red

**Django no responde desde Docker:**
- Windows/Mac: `http://host.docker.internal:8000`
- Linux: `http://172.17.0.1:8000`


Comando para crear workers

docker run --rm -v ${PWD}/tests/stress:/locust locustio/locust:latest -f /locust/locustfile.py --worker --master-host=<IP_DE_PC1>