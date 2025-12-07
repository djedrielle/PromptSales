from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT
from pymongo.errors import CollectionInvalid
import sys

MONGO_URL = "mongodb://localhost:27017/promptcontent"
DATABASE_NAME = "promptcontent"

def create_database_and_collections():
    try:
        client = MongoClient(MONGO_URL)
        db = client[DATABASE_NAME]
        
        print("Conectado a MongoDB")
        print(f"Base de datos: {DATABASE_NAME}")
        print("-" * 60)
        
        try:
            db.create_collection("Usuarios", validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["userId", "email", "name", "role", "createdAt", "authMethod"],
                    "properties": {
                        "userId": {"bsonType": "string"},
                        "email": {"bsonType": "string"},
                        "name": {"bsonType": "string"},
                        "role": {"bsonType": "string", "enum": ["admin", "marketer", "agent", "client"]},
                        "passwordHash": {"bsonType": "string"},
                        "authMethod": {"bsonType": "string", "enum": ["local", "oauth_google", "oauth_microsoft", "sso"]},
                        "lastPasswordChange": {"bsonType": "date"},
                        "twoFactorEnabled": {"bsonType": "bool"},
                        "createdAt": {"bsonType": "date"},
                        "lastLogin": {"bsonType": "date"},
                        "status": {"bsonType": "string", "enum": ["active", "inactive", "suspended"]}
                    }
                }
            })
            print("Colección 'Usuarios' creada")
        except CollectionInvalid:
            print("Colección 'Usuarios' ya existe")
        
        db.Usuarios.create_index([("userId", ASCENDING)], unique=True)
        db.Usuarios.create_index([("email", ASCENDING)], unique=True)
        db.Usuarios.create_index([("role", ASCENDING)])
        print("  → Índices creados para 'Usuarios'")
        
        try:
            db.create_collection("Servicios_Externos", validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["serviceId", "name", "baseUrl", "configuration", "authMethod", "createdAt"],
                    "properties": {
                        "serviceId": {"bsonType": "string"},
                        "name": {"bsonType": "string"},
                        "baseUrl": {"bsonType": "string"},
                        "authMethod": {"bsonType": "string"},
                        "encryptedCredentials": {"bsonType": "string"},
                        "secretKey": {"bsonType": "string"},
                        "apiKey": {"bsonType": "string"},
                        "status": {"bsonType": "string", "enum": ["active", "inactive", "testing"]},
                        "lastTestedAt": {"bsonType": "date"},
                        "createdAt": {"bsonType": "date"},
                        "updatedAt": {"bsonType": "date"},
                        "configuration": {"bsonType": "object"}
                    }
                }
            })
            print("Colección 'Servicios_Externos' creada")
        except CollectionInvalid:
            print("Colección 'Servicios_Externos' ya existe")
        
        db.Servicios_Externos.create_index([("serviceId", ASCENDING)], unique=True)
        db.Servicios_Externos.create_index([("name", ASCENDING)])
        print("  → Índices creados para 'Servicios_Externos'")
        
        try:
            db.create_collection("Registros_Llamadas_API", validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["logId", "serviceId", "timestamp", "request", "response",
                                 "statusCode", "userId", "platform", "ipAddress"],
                    "properties": {
                        "logId": {"bsonType": "string"},
                        "serviceId": {"bsonType": "string"},
                        "endpoint": {"bsonType": "string"},
                        "method": {"bsonType": "string"},
                        "request": {"bsonType": "object"},
                        "response": {"bsonType": "object"},
                        "statusCode": {"bsonType": "int"},
                        "responseTime": {"bsonType": "int"},
                        "result": {"bsonType": "string"},
                        "userId": {"bsonType": "string"},
                        "platform": {"bsonType": "string"},
                        "ipAddress": {"bsonType": "string"},
                        "processType": {"bsonType": "string"},
                        "timestamp": {"bsonType": "date"},
                        "processedAt": {"bsonType": "date"},
                        "errorDetails": {"bsonType": "string"}
                    }
                }
            })
            print("Colección 'Registros_Llamadas_API' creada")
        except CollectionInvalid:
            print("Colección 'Registros_Llamadas_API' ya existe")
        
        db.Registros_Llamadas_API.create_index([("logId", ASCENDING)], unique=True)
        db.Registros_Llamadas_API.create_index([("serviceId", ASCENDING)])
        db.Registros_Llamadas_API.create_index([("timestamp", DESCENDING)])
        db.Registros_Llamadas_API.create_index([("userId", ASCENDING)])
        print("  → Índices creados para 'Registros_Llamadas_API'")
        
        try:
            db.create_collection("Catalogo_Modelos_IA", validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["modelId", "name", "provider", "modelEndpoint", "version", "createdAt"],
                    "properties": {
                        "modelId": {"bsonType": "string"},
                        "name": {"bsonType": "string"},
                        "description": {"bsonType": "string"},
                        "provider": {
                            "bsonType": "string",
                            "enum": ["openai", "anthropic", "google", "huggingface", "aws_bedrock", "azure_openai", "custom"]
                        },
                        "baseModel": {"bsonType": "string"},
                        "modelEndpoint": {"bsonType": "string"},
                        "isFineTuned": {"bsonType": "bool"},
                        "fineTunedModelId": {"bsonType": "string"},
                        "fineTunedAt": {"bsonType": "date"},
                        "status": {"bsonType": "string", "enum": ["active", "inactive", "testing"]},
                        "createdAt": {"bsonType": "date"},
                        "updatedAt": {"bsonType": "date"}
                    }
                }
            })
            print("Colección 'Catalogo_Modelos_IA' creada")
        except CollectionInvalid:
            print("Colección 'Catalogo_Modelos_IA' ya existe")
        
        db.Catalogo_Modelos_IA.create_index([("modelId", ASCENDING)], unique=True)
        db.Catalogo_Modelos_IA.create_index([("name", ASCENDING)])
        print("  → Índices creados para 'Catalogo_Modelos_IA'")
        
        try:
            db.create_collection("Registros_Modelos_IA", validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["logId", "modelId", "timestamp", "input", "output", "userId", "status", "ipAddress"],
                    "properties": {
                        "logId": {"bsonType": "string"},
                        "modelId": {"bsonType": "string"},
                        "versionId": {"bsonType": "string"},
                        "input": {"bsonType": "string"},
                        "output": {"bsonType": "object"},
                        "parameters": {"bsonType": "object"},
                        "userId": {"bsonType": "string"},
                        "ipAddress": {"bsonType": "string"},
                        "processType": {"bsonType": "string"},
                        "timestamp": {"bsonType": "date"},
                        "processingTime": {"bsonType": "int"},
                        "status": {"bsonType": "string"},
                        "mcpServerUsed": {"bsonType": "bool"},
                        "mcpServerName": {"bsonType": "string"}
                    }
                }
            })
            print("Colección 'Registros_Modelos_IA' creada")
        except CollectionInvalid:
            print("Colección 'Registros_Modelos_IA' ya existe")
        
        db.Registros_Modelos_IA.create_index([("logId", ASCENDING)], unique=True)
        db.Registros_Modelos_IA.create_index([("modelId", ASCENDING)])
        db.Registros_Modelos_IA.create_index([("timestamp", DESCENDING)])
        print("  → Índices creados para 'Registros_Modelos_IA'")
        
        try:
            db.create_collection("Tipos_Contenido", validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["contentTypeId", "name", "createdAt"],
                    "properties": {
                        "contentTypeId": {"bsonType": "string"},
                        "name": {"bsonType": "string", "enum": ["text", "image", "video", "audio", "carousel", "story"]},
                        "description": {"bsonType": "string"},
                        "supportedPlatforms": {"bsonType": "array"},
                        "createdAt": {"bsonType": "date"}
                    }
                }
            })
            print("Colección 'Tipos_Contenido' creada")
        except CollectionInvalid:
            print("Colección 'Tipos_Contenido' ya existe")
        
        db.Tipos_Contenido.create_index([("contentTypeId", ASCENDING)], unique=True)
        db.Tipos_Contenido.create_index([("name", ASCENDING)])
        print("  → Índices creados para 'Tipos_Contenido'")
        
        try:
            db.create_collection("Medios", validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["clientId", "requestDescription", "hashtags", "deliveryStatus", "format"],
                    "properties": {
                        "mediaId": {"bsonType": "string"},
                        "mediaUrl": {"bsonType": "string"},
                        "fileName": {"bsonType": "string"},
                        "format": {"bsonType": "string"},
                        "size": {"bsonType": "int"},
                        "description": {"bsonType": "string"},
                        "hashtags": {"bsonType": "array"},
                        "category": {"bsonType": "string", "enum": ["social", "ads", "web", "other"]},
                        "platform": {"bsonType": "string", "enum": ["Youtube", "Instagram", "Facebook", "Tiktok", "other"]},
                        "vectorEmbedding": {"bsonType": "array"},
                        "userId": {"bsonType": "string"},
                        "clientId": {"bsonType": "string"},
                        "requestId": {"bsonType": "string"},
                        "requestDescription": {"bsonType": "string"},
                        "campaignId": {"bsonType": "string"},
                        "adId": {"bsonType": "string"},
                        "strategyId": {"bsonType": "string"},
                        "deliveryStatus": {"bsonType": "string", "enum": ["Pending", "Delivered", "Processing"]},
                        "createdAt": {"bsonType": "date"},
                        "updatedAt": {"bsonType": "date"},
                        "usageCount": {"bsonType": "int"},
                        "rights": {"bsonType": "string"}
                    }
                }
            })
            print("Colección 'Medios' creada")
        except CollectionInvalid:
            print("Colección 'Medios' ya existe")
        
        db.Medios.create_index([("mediaId", ASCENDING)], unique=True)
        db.Medios.create_index([("hashtags", ASCENDING)])
        db.Medios.create_index([("description", TEXT)])
        db.Medios.create_index([("createdAt", DESCENDING)])
        db.Medios.create_index([("status", ASCENDING)])
        db.Medios.create_index([("clientId", ASCENDING)])
        db.Medios.create_index([("campaignId", ASCENDING)])
        print("  → Índices creados para 'Medios'")
        
        try:
            db.create_collection("Solicitudes_Contenido", validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["requestId", "clientId", "contentType", "createdAt", "status", "ipAddress", "httpMethod", "requestHeaders", "requestBody"],
                    "properties": {
                        "requestId": {"bsonType": "string"},
                        "clientId": {"bsonType": "string"},
                        "contentType": {"bsonType": "string"},
                        "description": {"bsonType": "string"},
                        "targetAudience": {"bsonType": "string"},
                        "campaignDescription": {"bsonType": "string"},
                        "httpMethod": {"bsonType": "string", "enum": ["GET", "POST", "PUT", "DELETE", "PATCH"]},
                        "requestHeaders": {"bsonType": "object"},
                        "requestBody": {"bsonType": "object"},
                        "ipAddress": {"bsonType": "string"},
                        "generatedContent": {
                            "bsonType": "array",
                            "items": {
                                "bsonType": "object",
                                "properties": {
                                    "contentId": {"bsonType": "string"},
                                    "contentType": {"bsonType": "string"},
                                    "url": {"bsonType": "string"},
                                    "metadata": {"bsonType": "object"}
                                }
                            }
                        },
                        "status": {"bsonType": "string", "enum": ["pending", "processing", "completed", "failed"]},
                        "createdAt": {"bsonType": "date"},
                        "completedAt": {"bsonType": "date"},
                        "processingTime": {"bsonType": "int"}
                    }
                }
            })
            print("Colección 'Solicitudes_Contenido' creada")
        except CollectionInvalid:
            print("Colección 'Solicitudes_Contenido' ya existe")
        
        db.Solicitudes_Contenido.create_index([("requestId", ASCENDING)], unique=True)
        db.Solicitudes_Contenido.create_index([("clientId", ASCENDING)])
        db.Solicitudes_Contenido.create_index([("userId", ASCENDING)])
        db.Solicitudes_Contenido.create_index([("createdAt", DESCENDING)])
        db.Solicitudes_Contenido.create_index([("status", ASCENDING)])
        db.Solicitudes_Contenido.create_index([("contentType", ASCENDING)])
        db.Solicitudes_Contenido.create_index([("ipAddress", ASCENDING)])
        print("  → Índices creados para 'Solicitudes_Contenido'")
        
        try:
            db.create_collection("Clientes", validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["clientId", "email", "name", "createdAt", "status"],
                    "properties": {
                        "clientId": {"bsonType": "string"},
                        "email": {"bsonType": "string"},
                        "name": {"bsonType": "string"},
                        "company": {"bsonType": "string"},
                        "phone": {"bsonType": "string"},
                        "createdAt": {"bsonType": "date"},
                        "updatedAt": {"bsonType": "date"},
                        "status": {"bsonType": "string", "enum": ["active", "inactive", "suspended"]},
                        "subscriptions": {
                            "bsonType": "array",
                            "items": {
                                "bsonType": "object",
                                "properties": {
                                    "subscriptionId": {"bsonType": "string"},
                                    "planId": {"bsonType": "string"},
                                    "planName": {"bsonType": "string"},
                                    "status": {"bsonType": "string", "enum": ["active", "paused", "cancelled"]},
                                    "startDate": {"bsonType": "date"},
                                    "endDate": {"bsonType": "date"},
                                    "renewalDate": {"bsonType": "date"},
                                    "paymentStatus": {"bsonType": "string", "enum": ["paid", "pending", "failed"]},
                                    "usageTracking": {
                                        "bsonType": "object",
                                        "additionalProperties": {
                                            "bsonType": "object",
                                            "properties": {
                                                "used": {"bsonType": "int"},
                                                "limit": {"bsonType": "int"},
                                                "resetDate": {"bsonType": "date"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            })
            print("Colección 'Clientes' creada")
        except CollectionInvalid:
            print("Colección 'Clientes' ya existe")
        
        db.Clientes.create_index([("clientId", ASCENDING)], unique=True)
        db.Clientes.create_index([("email", ASCENDING)], unique=True)
        db.Clientes.create_index([("status", ASCENDING)])
        print("  → Índices creados para 'Clientes'")
        
        try:
            db.create_collection("Planes_Suscripcion", validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["planId", "name", "price", "createdAt"],
                    "properties": {
                        "planId": {"bsonType": "string"},
                        "name": {"bsonType": "string"},
                        "description": {"bsonType": "string"},
                        "price": {"bsonType": "double"},
                        "currency": {"bsonType": "string"},
                        "billingCycle": {"bsonType": "string", "enum": ["monthly", "quarterly", "annual"]},
                        "status": {"bsonType": "string", "enum": ["active", "discontinued"]},
                        "features": {
                            "bsonType": "array",
                            "items": {
                                "bsonType": "object",
                                "required": ["featureId", "limit"],
                                "properties": {
                                    "featureId": {"bsonType": "string"},
                                    "featureName": {"bsonType": "string"},
                                    "limit": {"bsonType": "int"}
                                }
                            }
                        },
                        "createdAt": {"bsonType": "date"},
                        "updatedAt": {"bsonType": "date"}
                    }
                }
            })
            print("Colección 'Planes_Suscripcion' creada")
        except CollectionInvalid:
            print("Colección 'Planes_Suscripcion' ya existe")
        
        db.Planes_Suscripcion.create_index([("planId", ASCENDING)], unique=True)
        db.Planes_Suscripcion.create_index([("name", ASCENDING)])
        db.Planes_Suscripcion.create_index([("status", ASCENDING)])
        print("  → Índices creados para 'Planes_Suscripcion'")
        
        try:
            db.create_collection("Funciones", validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["featureId", "name", "createdAt"],
                    "properties": {
                        "featureId": {"bsonType": "string"},
                        "name": {"bsonType": "string"},
                        "description": {"bsonType": "string"},
                        "createdAt": {"bsonType": "date"}
                    }
                }
            })
            print("Colección 'Funciones' creada")
        except CollectionInvalid:
            print("Colección 'Funciones' ya existe")
        
        db.Funciones.create_index([("featureId", ASCENDING)], unique=True)
        print("  → Índices creados para 'Funciones'")
        
        try:
            db.create_collection("Metodos_Pago", validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["methodId", "name", "type", "createdAt"],
                    "properties": {
                        "methodId": {"bsonType": "string"},
                        "name": {"bsonType": "string", "enum": ["credit_card", "debit_card", "paypal", "wire_transfer"]},
                        "type": {"bsonType": "string"},
                        "description": {"bsonType": "string"},
                        "isActive": {"bsonType": "bool"},
                        "createdAt": {"bsonType": "date"}
                    }
                }
            })
            print("Colección 'Metodos_Pago' creada")
        except CollectionInvalid:
            print("Colección 'Metodos_Pago' ya existe")
        
        db.Metodos_Pago.create_index([("methodId", ASCENDING)], unique=True)
        print("  → Índices creados para 'Metodos_Pago'")
        
        try:
            db.create_collection("Calendarios_Pago", validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["scheduleId", "subscriptionId", "amount", "dueDate"],
                    "properties": {
                        "scheduleId": {"bsonType": "string"},
                        "subscriptionId": {"bsonType": "string"},
                        "amount": {"bsonType": "double"},
                        "currency": {"bsonType": "string"},
                        "dueDate": {"bsonType": "date"},
                        "status": {"bsonType": "string", "enum": ["pending", "paid", "overdue", "cancelled"]},
                        "paymentMethodId": {"bsonType": "string"},
                        "createdAt": {"bsonType": "date"}
                    }
                }
            })
            print("Colección 'Calendarios_Pago' creada")
        except CollectionInvalid:
            print("Colección 'Calendarios_Pago' ya existe")
        
        db.Calendarios_Pago.create_index([("scheduleId", ASCENDING)], unique=True)
        db.Calendarios_Pago.create_index([("subscriptionId", ASCENDING)])
        db.Calendarios_Pago.create_index([("dueDate", ASCENDING)])
        print("  → Índices creados para 'Calendarios_Pago'")
        
        try:
            db.create_collection("Transacciones_Pago", validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["transactionId", "subscriptionId", "clientId", "amount", "timestamp"],
                    "properties": {
                        "transactionId": {"bsonType": "string"},
                        "subscriptionId": {"bsonType": "string"},
                        "clientId": {"bsonType": "string"},
                        "amount": {"bsonType": "double"},
                        "currency": {"bsonType": "string"},
                        "paymentMethodId": {"bsonType": "string"},
                        "status": {"bsonType": "string", "enum": ["success", "failed", "pending", "refunded"]},
                        "externalTransactionId": {"bsonType": "string"},
                        "details": {"bsonType": "object"},
                        "timestamp": {"bsonType": "date"},
                        "processedAt": {"bsonType": "date"},
                        "errorMessage": {"bsonType": "string"}
                    }
                }
            })
            print("Colección 'Transacciones_Pago' creada")
        except CollectionInvalid:
            print("Colección 'Transacciones_Pago' ya existe")
        
        db.Transacciones_Pago.create_index([("transactionId", ASCENDING)], unique=True)
        db.Transacciones_Pago.create_index([("subscriptionId", ASCENDING)])
        db.Transacciones_Pago.create_index([("clientId", ASCENDING)])
        db.Transacciones_Pago.create_index([("timestamp", DESCENDING)])
        print("  → Índices creados para 'Transacciones_Pago'")
        
        try:
            db.create_collection("Campanas", validator={
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["campaignId", "name", "description", "createdAt"],
                    "properties": {
                        "campaignId": {"bsonType": "string"},
                        "name": {"bsonType": "string"},
                        "description": {"bsonType": "string"},
                        "targetAudience": {"bsonType": "string"},
                        "campaignMessage": {"bsonType": "string"},
                        "contentVersions": {"bsonType": "array"},
                        "usedImages": {"bsonType": "array"},
                        "status": {"bsonType": "string", "enum": ["draft", "active", "completed", "archived"]},
                        "startDate": {"bsonType": "date"},
                        "endDate": {"bsonType": "date"},
                        "createdAt": {"bsonType": "date"},
                        "updatedAt": {"bsonType": "date"}
                    }
                }
            })
            print("Colección 'Campanas' creada")
        except CollectionInvalid:
            print("Colección 'Campanas' ya existe")
        
        db.Campanas.create_index([("campaignId", ASCENDING)], unique=True)
        db.Campanas.create_index([("createdAt", DESCENDING)])
        db.Campanas.create_index([("status", ASCENDING)])
        print("  → Índices creados para 'Campanas'")
        
        print("-" * 60)
        print(f" Base de datos '{DATABASE_NAME}' configurada exitosamente")
        print(" Total de colecciones creadas: 15")
        
        collections = db.list_collection_names()
        print("\nColecciones disponibles:")
        for i, col in enumerate(collections, 1):
            print(f"  {i}. {col}")
        
        client.close()
        print("\n Conexión cerrada")
        
    except Exception as e:
        print(f"\n Error: {e}")
        sys.exit(1)

if 1 == 1:
    print("=" * 60)
    print("CREACIÓN DE BASE DE DATOS - promptcontent")
    print("=" * 60)
    create_database_and_collections()
    print("\n¡Script completado exitosamente!")
