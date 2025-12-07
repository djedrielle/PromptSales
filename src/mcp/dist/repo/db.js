import sql from 'mssql';
// SQL Server configuration
const dbConfig = {
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
let pool = null;
/**
 * Inicializa el pool de conexiones
 */
export async function initializeDatabase() {
    try {
        pool = await sql.connect(dbConfig);
        console.error('✓ Connected to SQL Server successfully');
    }
    catch (error) {
        console.error('✗ Database connection failed:', error.message);
        throw error;
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
export async function executeQuery(query, params = {}) {
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
    }
    catch (error) {
        console.error('Query execution error:', error.message);
        throw error;
    }
}
