# 🧪 PromptSales QA Suite

Esta carpeta contiene la batería de pruebas moderna para el proyecto PromptSales, diseñada con prácticas de última generación (QA powered by AI & Code).

## 📂 Estructura

```
tests/
├── unit/       # Pruebas de lógica de negocio pura (PricingCalculator)
├── api/        # Pruebas de integración REST API (Requests)
├── stress/     # Pruebas de carga y estrés distribuidas (Locust)
└── mcp/        # Pruebas automáticas del servidor MCP (JSON-RPC)
```

## 🚀 Inicio Rápido

### 1. Requisitos Previos

Asegúrate de instalar las herramientas necesarias:
```bash
pip install pytest requests locust ruff django
```

Para las pruebas de integración MCP necesitas tener el servidor Node.js compilado:
```bash
cd src/mcp
npm install
npm run build
```

### 2. Ejecutar Todas las Pruebas

Hemos creado un script maestro para facilitar la ejecución:

```bash
# Ejecuta unit tests, linter, integración MCP y API (si server corre)
python run_qa_suite.py --type all
```

### 3. Ejecución por Tipo

#### 🏗️ Unit Testing (Pytest)
Pruebas rápidas de la clase `LeadMetrics`.
```bash
python run_qa_suite.py --type unit
# O directamente:
python -m pytest tests/unit/test_lead_metrics.py -v
```

#### 🌐 REST API Testing
Prueba los endpoints `/api/health` y `/api/lead-metrics`.
Requiere que el servidor Django esté corriendo (`python manage.py runserver`).
```bash
python run_qa_suite.py --type api
```

#### 🦗 Stress Testing (Locust)
Prueba la capacidad del sistema bajo carga.
```bash
# Modo gráfico (abre localhost:8089)
python -m locust -f tests/stress/locustfile.py

# Modo Headless (CLI)
python -m locust -f tests/stress/locustfile.py --headless -u 50 -r 5 -t 1m
```
- `-u 50`: 50 usuarios concurrentes
- `-r 5`: 5 usuarios nuevos por segundo
- `-t 1m`: Ejecutar por 1 minuto

#### 🤖 MCP Server Testing
Prueba de caja negra que verifica que el servidor MCP responde al protocolo JSON-RPC correctamente.
```bash
python run_qa_suite.py --type mcp
```

## 🛠️ Linter & Calidad (Ruff)

Usamos **Ruff** para mantener el código limpio. Es compatible con las reglas de Flake8, Isort y PyUpgrade.
```bash
# Revisar código
python -m ruff check .

# Corregir automáticamente
python -m ruff check --fix .
```
