import request from 'supertest';
import express from 'express';

// Mock App Setup
const app = express();
app.use(express.json());
app.get('/api/v1/campaigns/:id', (req, res) => {
    if (req.params.id === '1') {
        res.json({ id: '1', name: 'Integration Test Campaign' });
    } else {
        res.status(404).send('Not Found');
    }
});
app.post('/api/v1/campaigns', (req, res) => {
    if (!req.headers.authorization) {
        return res.status(401).send('Unauthorized');
    }
    res.status(201).json({ id: '2', ...req.body });
});

describe('REST API Integration Tests', () => {
    test('GET /api/v1/campaigns/:id should return 200 for existing campaign', async () => {
        const response = await request(app).get('/api/v1/campaigns/1');
        expect(response.status).toBe(200);
        expect(response.body.name).toBe('Integration Test Campaign');
    });

    test('POST /api/v1/campaigns should return 401 if no auth token', async () => {
        const response = await request(app).post('/api/v1/campaigns').send({ name: 'New' });
        expect(response.status).toBe(401);
    });

    test('POST /api/v1/campaigns should create campaign with valid auth', async () => {
        const response = await request(app)
            .post('/api/v1/campaigns')
            .set('Authorization', 'Bearer valid-token')
            .send({ name: 'New Campaign', budget: 500 });

        expect(response.status).toBe(201);
        expect(response.body.name).toBe('New Campaign');
    });
});
