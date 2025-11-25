# PromptSales Architecture

## 1. High-Level Architecture

This diagram illustrates the interaction between the central PromptSales Portal and its sub-companies (PromptContent, PromptAds, PromptCrm), along with their integration with external services.

```mermaid
graph TD
    subgraph "PromptSales Ecosystem"
        Portal["PromptSales Portal (Web/Vercel)"]
        
        subgraph "Sub-Companies"
            Content["PromptContent System"]
            Ads["PromptAds System"]
            CRM["PromptCrm System"]
        end
        
        Portal -->|HTTP/REST/MCP| Content
        Portal -->|HTTP/REST/MCP| Ads
        Portal -->|HTTP/REST/MCP| CRM
        
        Content <-->|MCP| Ads
        Ads <-->|MCP| CRM
        CRM <-->|MCP| Content
    end

    subgraph "External Services"
        AI_Models["AI Models (OpenAI, etc.)"]
        Social_Media["Social Media (Meta, TikTok)"]
        Ad_Platforms["Ad Platforms (Google Ads)"]
        Ext_CRM["External CRMs (HubSpot, Salesforce)"]
    end

    Content -->|API| AI_Models
    Content -->|API| Social_Media
    Ads -->|API| Ad_Platforms
    Ads -->|API| Social_Media
    CRM -->|API| Ext_CRM
    CRM -->|API| Social_Media
```

## 2. Infrastructure Architecture

This diagram details the deployment strategy using Kubernetes for backend services and Vercel for frontends, ensuring scalability and high availability.

```mermaid
graph TD
    subgraph "Client Layer"
        User["User / Browser"]
    end

    subgraph "Frontend Layer (Vercel)"
        NextApp["Next.js App (PromptSales Portal)"]
        AdminPanel["Admin Panels"]
    end

    subgraph "Cloud Infrastructure (AWS)"
        LB["Load Balancer (ALB)"]
        
        subgraph "Kubernetes Cluster (EKS)"
            subgraph "Services Namespace"
                API_Gateway["API Gateway / Ingress"]
                Auth_Service["Auth Service (OAuth 2.0)"]
                
                Content_Svc["PromptContent Service"]
                Ads_Svc["PromptAds Service"]
                CRM_Svc["PromptCrm Service"]
                
                MCP_Orchestrator["MCP Orchestrator"]
            end
            
            subgraph "Workers Namespace"
                Job_Queue["Job Queue Workers"]
            end
        end
        
        subgraph "Data Layer"
            Redis[("Redis Cache - ElastiCache")]
            Postgres[("PostgreSQL - Aurora")]
            Mongo[("MongoDB - Atlas")]
        end
    end

    User -->|HTTPS| NextApp
    User -->|HTTPS| AdminPanel
    
    NextApp -->|API Calls| LB
    AdminPanel -->|API Calls| LB
    
    LB --> API_Gateway
    
    API_Gateway --> Auth_Service
    API_Gateway --> Content_Svc
    API_Gateway --> Ads_Svc
    API_Gateway --> CRM_Svc
    API_Gateway --> MCP_Orchestrator
    
    Content_Svc --> Redis
    Ads_Svc --> Redis
    CRM_Svc --> Redis
    
    Content_Svc --> Mongo
    Ads_Svc --> Postgres
    CRM_Svc --> Postgres
    
    Content_Svc -->|Async| Job_Queue
    Ads_Svc -->|Async| Job_Queue
```

## 3. MCP (Model Context Protocol) Integration

This diagram focuses on how MCP servers are used to interconnect the sub-companies and provide a unified interface for AI agents and the portal.

```mermaid
graph LR
    subgraph "MCP Clients"
        Portal_Agent["Portal AI Agent"]
        Dev_Tool["Developer Tooling"]
    end

    subgraph "MCP Layer"
        Analytics_MCP["Analytics MCP Server"]
        Content_MCP["Content MCP Server"]
        Ads_MCP["Ads MCP Server"]
        CRM_MCP["CRM MCP Server"]
    end

    subgraph "Backend Systems"
        Content_DB[("Content DB")]
        Ads_DB[("Ads DB")]
        CRM_DB[("CRM DB")]
    end

    Portal_Agent -->|Query| Analytics_MCP
    Portal_Agent -->|Action| Content_MCP
    Portal_Agent -->|Action| Ads_MCP
    
    Analytics_MCP -->|Read| Content_DB
    Analytics_MCP -->|Read| Ads_DB
    Analytics_MCP -->|Read| CRM_DB
    
    Content_MCP -->|Read/Write| Content_DB
    Ads_MCP -->|Read/Write| Ads_DB
    CRM_MCP -->|Read/Write| CRM_DB
    
    Content_MCP -.->|Context Sharing| Ads_MCP
```
