export const TOOLS = [
    {
        name: "get_campaign_performance",
        description: "Analyzes the overall performance of marketing campaigns. Provides key metrics such as impressions, clicks, CTR (Click-Through Rate), cost, and daily conversions. Allows filtering by campaign name and date range to obtain a detailed analysis of advertising efficiency.",
        inputSchema: {
            type: "object",
            properties: {
                campaignName: {
                    type: "string",
                    description: "Optional campaign name to filter results. If omitted, returns data for all campaigns.",
                },
                startDate: {
                    type: "string",
                    description: "Start date for metrics analysis (ISO format YYYY-MM-DD).",
                },
                endDate: {
                    type: "string",
                    description: "End date for metrics analysis (ISO format YYYY-MM-DD).",
                },
            },
        },
    },
    {
        name: "get_sales_data",
        description: "Retrieves detailed sales and conversion data attributed to specific campaigns. Provides information about sales amount, transaction date, and customer code. Ideal for calculating ROI (Return on Investment) and analyzing the direct impact of campaigns on revenue.",
        inputSchema: {
            type: "object",
            properties: {
                campaignName: {
                    type: "string",
                    description: "Optional campaign name to filter sales.",
                },
                startDate: {
                    type: "string",
                    description: "Start date for sales report (ISO format YYYY-MM-DD).",
                },
                endDate: {
                    type: "string",
                    description: "End date for sales report (ISO format YYYY-MM-DD).",
                },
            },
        },
    },
    {
        name: "get_campaign_reach",
        description: "Measures the reach and unique audience of campaigns. Provides daily data on how many unique people viewed the campaign (Reach) and unique users. Useful for evaluating market penetration and brand awareness.",
        inputSchema: {
            type: "object",
            properties: {
                campaignName: {
                    type: "string",
                    description: "Optional campaign name to filter.",
                },
            },
        },
    },
    {
        name: "get_campaign_channels",
        description: "Breaks down campaign performance by distribution channels (Social Media, Email, Web, etc.). Provides comparative metrics of impressions, clicks, CTR, and cost per platform, allowing identification of the most effective channels.",
        inputSchema: {
            type: "object",
            properties: {
                campaignName: {
                    type: "string",
                    description: "Optional campaign name to filter.",
                },
            },
        },
    },
    {
        name: "get_campaign_locations",
        description: "Analyzes the geographic distribution of campaign impact. Provides metrics of impressions, clicks, and CTR broken down by country or city. Essential for understanding in which regions the campaign performs better.",
        inputSchema: {
            type: "object",
            properties: {
                campaignName: {
                    type: "string",
                    description: "Optional campaign name to filter.",
                },
                granularity: {
                    type: "string",
                    enum: ["country", "city"],
                    description: "Level of geographic detail required. Can be 'country' or 'city'.",
                },
            },
        },
    },
];
