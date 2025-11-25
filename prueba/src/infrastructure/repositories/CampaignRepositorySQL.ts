import { Pool } from 'pg';
import { createClient } from 'redis';

// Interface for the Campaign entity
interface Campaign {
  id: string;
  name: string;
  budget: number;
  status: string;
}

export class CampaignRepositorySQL {
  private db: Pool;
  private cache: ReturnType<typeof createClient>;

  constructor(dbPool: Pool, redisClient: ReturnType<typeof createClient>) {
    this.db = dbPool;
    this.cache = redisClient;
  }

  /**
   * Creates a new campaign using a Stored Procedure.
   * Write operation - invalidates cache if necessary.
   */
  async createCampaign(name: string, budget: number, userId: string): Promise<Campaign> {
    try {
      // Calling Stored Procedure: sp_create_campaign(name, budget, user_id)
      const query = 'CALL sp_create_campaign($1, $2, $3, $4)';
      // Note: In PG, CALL is for procedures. RETURNING might need a function or output param.
      // For this example, we assume the procedure returns the created row or we query it back.
      // Alternatively, using SELECT * FROM fn_create_campaign(...) if it's a function.
      
      // Let's assume a function that returns the new ID
      const result = await this.db.query(
        'SELECT * FROM fn_create_campaign($1, $2, $3)',
        [name, budget, userId]
      );

      const newCampaign = result.rows[0];
      
      // Invalidate list cache if exists
      await this.cache.del(`user:${userId}:campaigns`);

      return newCampaign;
    } catch (error) {
      console.error('Error creating campaign via SP:', error);
      throw new Error('Database transaction failed');
    }
  }

  /**
   * Retrieves a campaign by ID.
   * Read operation - implements Cache-Aside pattern.
   */
  async getCampaignById(id: string): Promise<Campaign | null> {
    const cacheKey = `campaign:${id}`;

    // 1. Try to get from Cache
    try {
      const cachedData = await this.cache.get(cacheKey);
      if (cachedData) {
        console.log('Cache Hit');
        return JSON.parse(cachedData);
      }
    } catch (err) {
      console.warn('Redis error:', err);
    }

    // 2. If missing, get from DB
    try {
      const result = await this.db.query('SELECT * FROM campaigns WHERE id = $1', [id]);
      
      if (result.rows.length === 0) return null;

      const campaign = result.rows[0];

      // 3. Save to Cache (TTL 1 hour)
      await this.cache.setEx(cacheKey, 3600, JSON.stringify(campaign));
      console.log('Cache Miss - Loaded from DB');

      return campaign;
    } catch (error) {
      console.error('Error fetching campaign:', error);
      throw error;
    }
  }
}
