#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
    CallToolRequestSchema,
    ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// Mock Data for Analytics
const CAMPAIGN_DATA = [
    { id: "c1", name: "Summer Sale", impressions: 15000, clicks: 450, conversions: 20, spend: 500 },
    { id: "c2", name: "Tech Launch", impressions: 50000, clicks: 1200, conversions: 85, spend: 2000 },
    { id: "c3", name: "Brand Awareness", impressions: 100000, clicks: 300, conversions: 5, spend: 1000 },
];

// Create the MCP Server
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

/**
 * Tool: query_analytics
 * Description: Retrieves campaign performance metrics based on parameters.
 * In a real scenario, this would parse natural language or SQL.
 */
server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
        tools: [
            {
                name: "get_campaign_performance",
                description: "Get performance metrics for campaigns. Can filter by name or get all.",
                inputSchema: {
                    type: "object",
                    properties: {
                        campaignName: {
                            type: "string",
                            description: "Optional name of the campaign to filter by",
                        },
                        metric: {
                            type: "string",
                            description: "Specific metric to retrieve (impressions, clicks, conversions, spend)",
                        },
                    },
                },
            },
            {
                name: "analyze_roi",
                description: "Calculates ROI for a specific campaign.",
                inputSchema: {
                    type: "object",
                    properties: {
                        campaignId: {
                            type: "string",
                            description: "ID of the campaign",
                        },
                    },
                    required: ["campaignId"],
                },
            },
        ],
    };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;

    if (name === "get_campaign_performance") {
        const campaignName = args?.campaignName as string | undefined;

        let results = CAMPAIGN_DATA;
        if (campaignName) {
            results = results.filter(c => c.name.toLowerCase().includes(campaignName.toLowerCase()));
        }

        return {
            content: [
                {
                    type: "text",
                    text: JSON.stringify(results, null, 2),
                },
            ],
        };
    }

    if (name === "analyze_roi") {
        const campaignId = args?.campaignId as string;
        const campaign = CAMPAIGN_DATA.find(c => c.id === campaignId);

        if (!campaign) {
            return {
                content: [{ type: "text", text: `Campaign ${campaignId} not found.` }],
                isError: true,
            };
        }

        // Simple ROI: (Revenue - Cost) / Cost. Assuming Conversion Value = $100 for demo.
        const revenue = campaign.conversions * 100;
        const roi = ((revenue - campaign.spend) / campaign.spend) * 100;

        return {
            content: [
                {
                    type: "text",
                    text: `ROI Analysis for ${campaign.name}:\nSpend: $${campaign.spend}\nRevenue (est): $${revenue}\nROI: ${roi.toFixed(2)}%`,
                },
            ],
        };
    }

    throw new Error(`Tool not found: ${name}`);
});

// Start the server
async function run() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("PromptSales Analytics MCP Server running on stdio");
}

run().catch((error) => {
    console.error("Fatal error running server:", error);
    process.exit(1);
});
