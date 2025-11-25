import { CampaignRepositorySQL } from '../../src/infrastructure/repositories/CampaignRepositorySQL';
import { Pool } from 'pg';
import { createClient } from 'redis';

// Mocks
jest.mock('pg');
jest.mock('redis');

describe('CampaignRepositorySQL Unit Tests', () => {
    let repository: CampaignRepositorySQL;
    let mockDb: any;
    let mockCache: any;

    beforeEach(() => {
        mockDb = new Pool();
        mockCache = createClient();
        repository = new CampaignRepositorySQL(mockDb, mockCache);
    });

    test('createCampaign should call stored procedure and invalidate cache', async () => {
        // Arrange
        const mockCampaign = { id: '1', name: 'Test Campaign', budget: 100 };
        mockDb.query = jest.fn().mockResolvedValue({ rows: [mockCampaign] });
        mockCache.del = jest.fn().mockResolvedValue(1);

        // Act
        const result = await repository.createCampaign('Test Campaign', 100, 'user1');

        // Assert
        expect(mockDb.query).toHaveBeenCalledWith(
            expect.stringContaining('SELECT * FROM fn_create_campaign'),
            ['Test Campaign', 100, 'user1']
        );
        expect(mockCache.del).toHaveBeenCalledWith('user:user1:campaigns');
        expect(result).toEqual(mockCampaign);
    });

    test('getCampaignById should return cached value if available', async () => {
        // Arrange
        const mockCampaign = { id: '1', name: 'Cached Campaign' };
        mockCache.get = jest.fn().mockResolvedValue(JSON.stringify(mockCampaign));
        mockDb.query = jest.fn(); // Should not be called

        // Act
        const result = await repository.getCampaignById('1');

        // Assert
        expect(mockCache.get).toHaveBeenCalledWith('campaign:1');
        expect(mockDb.query).not.toHaveBeenCalled();
        expect(result).toEqual(mockCampaign);
    });
});
