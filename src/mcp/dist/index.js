#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema, } from "@modelcontextprotocol/sdk/types.js";
import { initializeDatabase, closeDatabase } from './repo/db.js';
import { handleListTools, handleCallTool } from './handlers/index.js';
const server = new Server({
    name: "promptsales-analytics",
    version: "1.0.0",
}, {
    capabilities: {
        tools: {},
    },
});
// Configurar handlers usando el patrón moderno
server.setRequestHandler(ListToolsRequestSchema, handleListTools);
server.setRequestHandler(CallToolRequestSchema, handleCallTool);
async function run() {
    try {
        // Inicializar la base de datos antes de iniciar el servidor
        await initializeDatabase();
        const transport = new StdioServerTransport();
        await server.connect(transport);
        console.error("PromptSales Analytics MCP Server running on stdio");
    }
    catch (error) {
        console.error("Failed to start server:", error);
        process.exit(1);
    }
}
// Manejar cierre graceful
process.on('SIGINT', async () => {
    console.error('Shutting down gracefully...');
    await closeDatabase();
    process.exit(0);
});
run().catch((error) => {
    console.error("Fatal error running server:", error);
    process.exit(1);
});
