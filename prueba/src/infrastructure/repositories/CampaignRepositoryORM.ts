import { PrismaClient, Campaign } from '@prisma/client';
import { createClient } from 'redis';

export class CampaignRepositoryORM {
    private prisma: PrismaClient;
    private cache: ReturnType<typeof createClient>;

    constructor(prismaClient: PrismaClient, redisClient: ReturnType<typeof createClient>) {
        this.prisma = prismaClient;
        this.cache = redisClient;
    }

    /**
     * Creates a new campaign using Prisma ORM.
     * Write operation.
     */
    async createCampaign(data: { name: string; budget: number; userId: string }): Promise<Campaign> {
        try {
            // ORM abstraction handles the SQL generation
            const newCampaign = await this.prisma.campaign.create({
                data: {
                    name: data.name,
                    budget: data.budget,
                    user: {
                        connect: { id: data.userId }
                    },
                    status: 'draft'
                }
            });

            // Invalidate related caches
            await this.cache.del(`user:${data.userId}:campaigns`);

            return newCampaign;
        } catch (error) {
            console.error('Prisma Error:', error);
            throw new Error('Failed to create campaign');
        }
    }

    /**
     * Retrieves a campaign by ID using Prisma ORM.
     * Read operation with Caching.
     */
    async getCampaignById(id: string): Promise<Campaign | null> {
        const cacheKey = `campaign:${id}`;

        // 1. Cache Check
        const cached = await this.cache.get(cacheKey);
        if (cached) {
            return JSON.parse(cached);
        }

        // 2. DB Query via ORM
        const campaign = await this.prisma.campaign.findUnique({
            where: { id }
        });

        if (campaign) {
            // 3. Cache Set
            await this.cache.setEx(cacheKey, 3600, JSON.stringify(campaign));
        }

        return campaign;
    }
}
