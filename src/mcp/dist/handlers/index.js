import { TOOLS } from '../tools/definitions.js';
import * as analyticsService from '../service/analyticsService.js';
export async function handleListTools() {
    return {
        tools: TOOLS,
    };
}
export async function handleCallTool(request) {
    const { name } = request.params;
    const args = (request.params.arguments || {});
    console.error(`[MCP] Received request for tool: ${name} with args:`, JSON.stringify(args));
    try {
        let result;
        switch (name) {
            case "get_campaign_performance":
                result = await analyticsService.getCampaignPerformance(args);
                break;
            case "get_sales_data":
                result = await analyticsService.getSalesData(args);
                break;
            case "get_campaign_reach":
                result = await analyticsService.getCampaignReach(args);
                break;
            case "get_campaign_channels":
                result = await analyticsService.getCampaignChannels(args);
                break;
            case "get_campaign_locations":
                result = await analyticsService.getCampaignLocations(args);
                break;
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
    }
    catch (error) {
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
}
