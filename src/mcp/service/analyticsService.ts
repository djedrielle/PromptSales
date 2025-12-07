import { executeQuery } from '../repo/db.js';

export async function getCampaignPerformance(args: any) {
    const query = `
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
    return await executeQuery(query, args);
}

export async function getSalesData(args: any) {
    const query = `
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
    return await executeQuery(query, args);
}

export async function getCampaignReach(args: any) {
    const query = `
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
    return await executeQuery(query, args);
}

export async function getCampaignChannels(args: any) {
    const query = `
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
    return await executeQuery(query, args);
}

export async function getCampaignLocations(args: any) {
    const query = `
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
    return await executeQuery(query, args);
}
