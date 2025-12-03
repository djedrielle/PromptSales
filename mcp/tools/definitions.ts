export const TOOLS = [
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
];
