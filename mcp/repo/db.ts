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
export async function initializeDatabase() {
    const maxRetries = 10;
    const retryDelay = 5000;

    for (let i = 0; i < maxRetries; i++) {
        try {
            pool = await sql.connect(dbConfig);
            console.error('✓ Connected to SQL Server successfully');
            return;
        } catch (error: any) {
            console.error(`✗ Database connection failed (attempt ${i + 1}/${maxRetries}):`, error.message);
            if (i === maxRetries - 1) throw error;
            await new Promise(resolve => setTimeout(resolve, retryDelay));
        }
    }
}

/**
 * Cierra el pool de conexiones
 */
export async function closeDatabase() {
    if (pool) {
        await pool.close();
    }
}

/**
 * Ejecuta una consulta SQL con parámetros
 */
export async function executeQuery(query: string, params: any = {}) {
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
