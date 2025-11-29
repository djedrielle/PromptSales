# PromptSales Analytics MCP Server

Este servidor implementa el **Model Context Protocol (MCP)** para proveer capacidades de analítica de marketing a agentes de IA. Actúa como una interfaz entre el LLM y los datos de rendimiento de campañas de PromptSales.

## 1. Ubicación de Configuración

*   **Directorio Raíz**: `prueba/mcp-servers/analytics-server/`
*   **Punto de Entrada**: [`index.ts`](./index.ts) - Contiene toda la lógica del servidor, definición de herramientas y manejo de peticiones.
*   **Gestión de Paquetes**: [`package.json`](./package.json) - Define las dependencias, específicamente el SDK de MCP (`@modelcontextprotocol/sdk`).
*   **Configuración de Ejecución**: El servidor está diseñado para ejecutarse sobre `stdio` (entrada/salida estándar), lo que permite su integración fácil con cualquier cliente MCP (como Claude Desktop o IDEs).

## 2. Reglas y Principios de Diseño

*   **Transporte Stdio**: Se utiliza `StdioServerTransport` para la comunicación. Esto significa que el servidor lee JSON-RPC de `stdin` y escribe en `stdout`. Los logs de depuración deben ir siempre a `stderr` para no romper el protocolo.
*   **Statelessness (Sin Estado)**: El servidor procesa cada petición de forma independiente. No mantiene estado de sesión entre llamadas a herramientas.
*   **Preparado para Producción**: Aunque actualmente usa un placeholder para la base de datos (`executeQuery`), la estructura de las herramientas y las consultas SQL simuladas están diseñadas para conectarse directamente a una base de datos relacional (como PostgreSQL) sin cambiar la interfaz de las herramientas.
*   **Tipado Fuerte**: Se utiliza TypeScript para definir los esquemas de entrada y garantizar la seguridad de tipos en los argumentos.

## 3. Código de Implementación

La implementación en `index.ts` sigue este flujo:

1.  **Inicialización**: Se importa la clase `Server` y se instancia con el nombre `promptsales-analytics`.
2.  **Definición de Herramientas (`ListToolsRequestSchema`)**: Se expone un JSON Schema para cada herramienta, detallando qué argumentos acepta (ej. `campaignId`, `startDate`). Esto permite al LLM entender *cómo* usar la herramienta.
3.  **Ejecución de Herramientas (`CallToolRequestSchema`)**: Un `switch` maneja las llamadas. Cada caso construye una consulta SQL (actualmente simulada) y retorna los resultados en formato JSON.
4.  **Manejo de Errores**: Se envuelven las ejecuciones en bloques `try-catch` para devolver errores formateados al cliente MCP en lugar de crashear el servidor.

## 4. Tools Disponibles

El servidor expone 5 herramientas especializadas:

| Tool | Descripción | Argumentos Clave |
| :--- | :--- | :--- |
| **`get_campaign_performance`** | Métricas generales de rendimiento (impresiones, clicks, CTR, gasto). | `campaignId`, `startDate`, `endDate` |
| **`get_sales_data`** | Datos financieros, ventas totales y conversiones atribuidas. | `campaignId`, `startDate`, `endDate` |
| **`get_campaign_reach`** | Métricas de alcance de audiencia y usuarios únicos. | `campaignId` |
| **`get_campaign_channels`** | Lista de canales (redes sociales, email, web) donde se publicó. | `campaignId` |
| **`get_campaign_locations`** | Desglose geográfico (países, ciudades) del impacto de la campaña. | `campaignId`, `granularity` |

## 5. Prompts de Ejemplo

A continuación, ejemplos de cómo un usuario interactuaría con el agente y qué herramienta se activaría internamente:

### Ejemplo 1: Rendimiento General
**Usuario**: "¿Cómo le fue a la campaña de 'Verano 2025' el mes pasado?"
**Tool Call**:
```json
{
  "name": "get_campaign_performance",
  "arguments": {
    "campaignId": "summer-2025-id", // (El LLM inferiría el ID si tiene contexto)
    "startDate": "2025-10-01",
    "endDate": "2025-10-31"
  }
}
```

### Ejemplo 2: Análisis de Ventas
**Usuario**: "Muéstrame cuánto dinero generó la campaña de Black Friday."
**Tool Call**:
```json
{
  "name": "get_sales_data",
  "arguments": {
    "campaignId": "black-friday-id"
  }
}
```

### Ejemplo 3: Distribución Geográfica
**Usuario**: "¿En qué ciudades estamos teniendo más impacto con la nueva campaña?"
**Tool Call**:
```json
{
  "name": "get_campaign_locations",
  "arguments": {
    "campaignId": "new-campaign-id",
    "granularity": "city"
  }
}
```

### Ejemplo 4: Auditoría de Canales
**Usuario**: "¿En qué redes sociales se publicó el anuncio de lanzamiento?"
**Tool Call**:
```json
{
  "name": "get_campaign_channels",
  "arguments": {
    "campaignId": "launch-campaign-id"
  }
}
```
