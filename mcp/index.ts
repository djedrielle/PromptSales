#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
    CallToolRequestSchema,
    ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import sql from 'mssql';

// SQL Server configuration
const dbConfig: sql.config = {
    user: process.env.DB_USER || 'sa',
    password: process.env.DB_PASS || 'PromptSales!2025',
    server: process.env.DB_HOST || 'promptsales-db',
    database: process.env.DB_NAME || 'PromptAds',
    port: 1433,
    options: {
        encrypt: false, // Para desarrollo local
        trustServerCertificate: true,
        enableArithAbort: true,
    },
    pool: {
        max: 10,
        min: 0,
        idleTimeoutMillis: 30000
    }
};

// Pool de conexiones
let pool: sql.ConnectionPool | null = null;

/**
 * Inicializa el pool de conexiones
 */
async function initializeDatabase() {
    try {
        pool = await sql.connect(dbConfig);
        console.error('✓ Connected to SQL Server successfully');
    } catch (error: any) {
        console.error('✗ Database connection failed:', error.message);
        throw error;
    }
}

/**
 * Ejecuta una consulta SQL con parámetros
 */
async function executeQuery(query: string, params: any = {}) {
    if (!pool) {
        throw new Error('Database pool not initialized');
    }

    try {
        const request = pool.request();

        // Agregar parámetros a la consulta
        if (params.campaignName) {
            request.input('campaignName', sql.NVarChar, params.campaignName);
        }
        if (params.startDate) {
            request.input('startDate', sql.DateTime, params.startDate);
        }
        if (params.endDate) {
            request.input('endDate', sql.DateTime, params.endDate);
        }
        if (params.granularity) {
            request.input('granularity', sql.NVarChar, params.granularity);
        }

        const result = await request.query(query);
        return result.recordset;
    } catch (error: any) {
        console.error('Query execution error:', error.message);
        throw error;
    }
}

const server = new Server(
    {
        name: "promptsales-analytics",
        version: "1.0.0",
    },
    {
        capabilities: {
            tools: {},
        },
    }
);

server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
        tools: [
            {
                name: "get_campaign_performance",
                description: "Retrieves general performance metrics for campaigns (impressions, clicks, CTR, etc.).",
                inputSchema: {
                    type: "object",
                    properties: {
                        campaignName: {
                            type: "string",
                            description: "Optional name of the campaign to filter by.",
                        },
                        startDate: {
                            type: "string",
                            description: "Start date for the metrics (ISO format).",
                        },
                        endDate: {
                            type: "string",
                            description: "End date for the metrics (ISO format).",
                        },
                    },
                },
            },
            {
                name: "get_sales_data",
                description: "Retrieves sales and conversion data attributed to marketing campaigns.",
                inputSchema: {
                    type: "object",
                    properties: {
                        campaignName: {
                            type: "string",
                            description: "Optional name of the campaign to filter by.",
                        },
                        startDate: {
                            type: "string",
                            description: "Start date for the sales data (ISO format).",
                        },
                        endDate: {
                            type: "string",
                            description: "End date for the sales data (ISO format).",
                        },
                    },
                },
            },
            {
                name: "get_campaign_reach",
                description: "Retrieves the reach and unique audience metrics for campaigns.",
                inputSchema: {
                    type: "object",
                    properties: {
                        campaignName: {
                            type: "string",
                            description: "Optional name of the campaign to filter by.",
                        },
                    },
                },
            },
            {
                name: "get_campaign_channels",
                description: "Retrieves the list of channels (Social Media, Email, Web, etc.) where campaigns are published.",
                inputSchema: {
                    type: "object",
                    properties: {
                        campaignName: {
                            type: "string",
                            description: "Optional name of the campaign to filter by.",
                        },
                    },
                },
            },
            {
                name: "get_campaign_locations",
                description: "Retrieves geographic distribution data (cities, countries) for campaign delivery.",
                inputSchema: {
                    type: "object",
                    properties: {
                        campaignName: {
                            type: "string",
                            description: "Optional name of the campaign to filter by.",
                        },
                        granularity: {
                            type: "string",
                            enum: ["country", "city"],
                            description: "Level of geographic detail required.",
                        },
                    },
                },
            },
        ],
    };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name } = request.params;
    const args = (request.params.arguments || {}) as any;

    console.error(`[MCP] Received request for tool: ${name} with args:`, JSON.stringify(args));

    try {
        let result;
        let query: string;

        switch (name) {
            case "get_campaign_performance": {
                query = `
                    SELECT 
                        c.CampaignCode,
                        c.CampaignName as CampaignName,
                        m.Date,
                        m.Impressions,
                        m.Clicks,
                        CASE WHEN m.Impressions > 0 
                            THEN CAST(m.Clicks AS FLOAT) / m.Impressions * 100 
                            ELSE 0 
                        END as CTR,
                        m.Spend as Cost,
                        m.Conversions
                    FROM PACampaignDailyMetrics m
                    INNER JOIN PCRCampaigns c ON m.IdCampaign = c.IdCampaign
                    WHERE 1=1
                    ${args.campaignName ? "AND c.CampaignCode = @campaignName" : ""}
                    ${args.startDate ? "AND m.Date >= @startDate" : ""}
                    ${args.endDate ? "AND m.Date <= @endDate" : ""}
                    ORDER BY m.Date DESC
                `;
                result = await executeQuery(query, args);
                break;
            }

            case "get_sales_data": {
                query = `
                    SELECT 
                        c.CampaignCode,
                        c.CampaignName as CampaignName,
                        s.CreatedAt,
                        s.SaleTotal as SaleAmount,
                        cl.ClientCode as CustomerCode
                    FROM PASalesHistory s
                    INNER JOIN PCRCampaigns c ON s.IdCampaign = c.IdCampaign
                    INNER JOIN PCRClients cl ON s.IdClient = cl.IdClient
                    WHERE 1=1
                    ${args.campaignName ? "AND c.CampaignCode = @campaignName" : ""}
                    ${args.startDate ? "AND s.CreatedAt >= @startDate" : ""}
                    ${args.endDate ? "AND s.CreatedAt <= @endDate" : ""}
                    ORDER BY s.CreatedAt DESC
                `;
                result = await executeQuery(query, args);
                break;
            }

            case "get_campaign_reach": {
                query = `
                    SELECT 
                        c.CampaignCode,
                        c.CampaignName as CampaignName,
                        m.Date,
                        m.Reach,
                        m.UniqueUsers
                    FROM PACampaignDailyMetrics m
                    INNER JOIN PCRCampaigns c ON m.IdCampaign = c.IdCampaign
                    WHERE 1=1
                    ${args.campaignName ? "AND c.CampaignCode = @campaignName" : ""}
                    ORDER BY m.Date DESC
                `;
                result = await executeQuery(query, args);
                break;
            }

            case "get_campaign_channels": {
                query = `
                    SELECT 
                        c.CampaignCode,
                        c.CampaignName as CampaignName,
                        ch.ChannelName,
                        ch.Platform,
                        ch.Impressions,
                        ch.Clicks,
                        CASE WHEN ch.Impressions > 0 
                            THEN CAST(ch.Clicks AS FLOAT) / ch.Impressions * 100 
                            ELSE 0 
                        END as CTR,
                        ch.Spend as Cost
                    FROM PACampaignChannelMetrics ch
                    INNER JOIN PCRCampaigns c ON ch.IdCampaign = c.IdCampaign
                    WHERE 1=1
                    ${args.campaignName ? "AND c.CampaignCode = @campaignName" : ""}
                `;
                result = await executeQuery(query, args);
                break;
            }

            case "get_campaign_locations": {
                query = `
                    SELECT 
                        c.CampaignCode,
                        c.CampaignName as CampaignName,
                        co.CountryName as Country,
                        ${args.granularity === 'city' ? 'ci.CityName as City,' : ''}
                        g.Impressions,
                        g.Clicks,
                        CASE WHEN g.Impressions > 0 
                            THEN CAST(g.Clicks AS FLOAT) / g.Impressions * 100 
                            ELSE 0 
                        END as CTR
                    FROM PACampaignGeoMetrics g
                    INNER JOIN PCRCampaigns c ON g.IdCampaign = c.IdCampaign
                    LEFT JOIN PCRCountries co ON g.IdCountry = co.IdCountry
                    LEFT JOIN PCRCities ci ON g.IdCity = ci.IdCity
                    WHERE 1=1
                    ${args.campaignName ? "AND c.CampaignCode = @campaignName" : ""}
                    ORDER BY g.Impressions DESC
                `;
                result = await executeQuery(query, args);
                break;
            }

            default:
                throw new Error(`Tool not found: ${name}`);
        }

        return {
            content: [
                {
                    type: "text",
                    text: JSON.stringify(result, null, 2),
                },
            ],
        };

    } catch (error: any) {
        console.error(`[MCP] Error executing tool ${name}:`, error);
        return {
            content: [
                {
                    type: "text",
                    text: `Error executing tool ${name}: ${error.message}`,
                },
            ],
            isError: true,
        };
    }
});

async function run() {
    try {
        // Inicializar la base de datos antes de iniciar el servidor
        await initializeDatabase();

        const transport = new StdioServerTransport();
        await server.connect(transport);
        console.error("PromptSales Analytics MCP Server running on stdio");
    } catch (error) {
        console.error("Failed to start server:", error);
        process.exit(1);
    }
}

// Manejar cierre graceful
process.on('SIGINT', async () => {
    console.error('Shutting down gracefully...');
    if (pool) {
        await pool.close();
    }
    process.exit(0);
});

run().catch((error) => {
    console.error("Fatal error running server:", error);
    process.exit(1);
});