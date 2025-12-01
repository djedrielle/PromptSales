-- PromptAds Simplified Database Creation Script
-- This script creates only the tables needed by the MCP Analytics Server

USE [master]
GO

-- Create the database
CREATE DATABASE [PromptAds]
GO

USE [PromptAds]
GO

-- ===================================
-- Supporting Tables (Catalogs)
-- ===================================

-- Campaign Statuses
CREATE TABLE [dbo].[PCRCampaignStatuses](
    [IdStatus] INT IDENTITY(1,1) NOT NULL,
    [StatusDescription] VARCHAR(20) NOT NULL,
    CONSTRAINT [PK_PCRCampaignStatuses] PRIMARY KEY ([IdStatus])
)
GO

-- Organizations
CREATE TABLE [dbo].[PCROrganizations](
    [IdOrganization] INT IDENTITY(1,1) NOT NULL,
    [OrganizationName] VARCHAR(50) NOT NULL,
    [Website] VARCHAR(50) NULL,
    [Industry] VARCHAR(30) NOT NULL,
    [CreatedAt] DATETIME NOT NULL DEFAULT GETDATE(),
    [UpdatedAt] DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT [PK_PCROrganizations] PRIMARY KEY ([IdOrganization])
)
GO

-- Geographic Tables
CREATE TABLE [dbo].[PCRCountries](
    [IdCountry] INT IDENTITY(1,1) NOT NULL,
    [CountryName] VARCHAR(30) NOT NULL,
    CONSTRAINT [PK_PCRCountries] PRIMARY KEY ([IdCountry])
)
GO

CREATE TABLE [dbo].[PCRStates](
    [IdState] INT IDENTITY(1,1) NOT NULL,
    [StateName] VARCHAR(30) NOT NULL,
    [IdCountry] INT NOT NULL,
    CONSTRAINT [PK_PCRStates] PRIMARY KEY ([IdState]),
    CONSTRAINT [FK_PCRStates_PCRCountries] FOREIGN KEY([IdCountry])
        REFERENCES [dbo].[PCRCountries] ([IdCountry])
)
GO

CREATE TABLE [dbo].[PCRCities](
    [IdCity] INT IDENTITY(1,1) NOT NULL,
    [CityName] VARCHAR(50) NOT NULL,
    [IdState] INT NOT NULL,
    CONSTRAINT [PK_PCRCities] PRIMARY KEY ([IdCity]),
    CONSTRAINT [FK_PCRCities_PCRStates] FOREIGN KEY([IdState])
        REFERENCES [dbo].[PCRStates] ([IdState])
)
GO

-- Client Statuses
CREATE TABLE [dbo].[PCRClientStatuses](
    [IdStatus] INT IDENTITY(1,1) NOT NULL,
    [StatusDescription] VARCHAR(20) NOT NULL,
    CONSTRAINT [PK_PCRClientStatuses] PRIMARY KEY ([IdStatus])
)
GO

-- Clients
CREATE TABLE [dbo].[PCRClients](
    [IdClient] INT IDENTITY(1,1) NOT NULL,
    [ClientCode] VARCHAR(30) NOT NULL,
    [IdStatus] INT NOT NULL,
    [CreatedAt] DATETIME NOT NULL DEFAULT GETDATE(),
    [UpdatedAt] DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT [PK_PCRClients] PRIMARY KEY ([IdClient]),
    CONSTRAINT [FK_PCRClients_PCRClientStatuses] FOREIGN KEY([IdStatus])
        REFERENCES [dbo].[PCRClientStatuses] ([IdStatus])
)
GO

-- ===================================
-- Core Campaign Table
-- ===================================

CREATE TABLE [dbo].[PCRCampaigns](
    [IdCampaign] INT IDENTITY(1,1) NOT NULL,
    [CampaignCode] VARCHAR(20) NOT NULL,
    [CampaignName] VARCHAR(100) NOT NULL,
    [IdOrganization] INT NOT NULL,
    [IdStatus] INT NOT NULL,
    [CreatedAt] DATETIME NOT NULL DEFAULT GETDATE(),
    [UpdatedAt] DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT [PK_PCRCampaigns] PRIMARY KEY ([IdCampaign]),
    CONSTRAINT [FK_PCRCampaigns_PCRCampaignStatuses] FOREIGN KEY([IdStatus])
        REFERENCES [dbo].[PCRCampaignStatuses] ([IdStatus]),
    CONSTRAINT [FK_PCRCampaigns_PCROrganizations] FOREIGN KEY([IdOrganization])
        REFERENCES [dbo].[PCROrganizations] ([IdOrganization])
)
GO

-- ===================================
-- Analytics Tables (Used by MCP Server)
-- ===================================

-- Daily Performance Metrics
CREATE TABLE [dbo].[PACampaignDailyMetrics](
    [IdMetric] INT IDENTITY(1,1) NOT NULL,
    [IdCampaign] INT NOT NULL,
    [Date] DATE NOT NULL,
    [Impressions] INT NOT NULL DEFAULT 0,
    [Clicks] INT NOT NULL DEFAULT 0,
    [Spend] DECIMAL(18, 2) NOT NULL DEFAULT 0,
    [Conversions] INT NOT NULL DEFAULT 0,
    [Reach] INT NOT NULL DEFAULT 0,
    [UniqueUsers] INT NOT NULL DEFAULT 0,
    CONSTRAINT [PK_PACampaignDailyMetrics] PRIMARY KEY ([IdMetric]),
    CONSTRAINT [FK_PACampaignDailyMetrics_PCRCampaigns] FOREIGN KEY([IdCampaign])
        REFERENCES [dbo].[PCRCampaigns] ([IdCampaign])
)
GO

-- Channel Metrics
CREATE TABLE [dbo].[PACampaignChannelMetrics](
    [IdChannelMetric] INT IDENTITY(1,1) NOT NULL,
    [IdCampaign] INT NOT NULL,
    [Date] DATE NOT NULL,
    [ChannelName] VARCHAR(50) NOT NULL,
    [Platform] VARCHAR(50) NOT NULL,
    [Impressions] INT NOT NULL DEFAULT 0,
    [Clicks] INT NOT NULL DEFAULT 0,
    [Spend] DECIMAL(18, 2) NOT NULL DEFAULT 0,
    CONSTRAINT [PK_PACampaignChannelMetrics] PRIMARY KEY ([IdChannelMetric]),
    CONSTRAINT [FK_PACampaignChannelMetrics_PCRCampaigns] FOREIGN KEY([IdCampaign])
        REFERENCES [dbo].[PCRCampaigns] ([IdCampaign])
)
GO

-- Geographic Metrics
CREATE TABLE [dbo].[PACampaignGeoMetrics](
    [IdGeoMetric] INT IDENTITY(1,1) NOT NULL,
    [IdCampaign] INT NOT NULL,
    [Date] DATE NOT NULL,
    [IdCity] INT NULL,
    [IdCountry] INT NULL,
    [Impressions] INT NOT NULL DEFAULT 0,
    [Clicks] INT NOT NULL DEFAULT 0,
    CONSTRAINT [PK_PACampaignGeoMetrics] PRIMARY KEY ([IdGeoMetric]),
    CONSTRAINT [FK_PACampaignGeoMetrics_PCRCampaigns] FOREIGN KEY([IdCampaign])
        REFERENCES [dbo].[PCRCampaigns] ([IdCampaign]),
    CONSTRAINT [FK_PACampaignGeoMetrics_PCRCities] FOREIGN KEY([IdCity])
        REFERENCES [dbo].[PCRCities] ([IdCity]),
    CONSTRAINT [FK_PACampaignGeoMetrics_PCRCountries] FOREIGN KEY([IdCountry])
        REFERENCES [dbo].[PCRCountries] ([IdCountry])
)
GO

-- Sales History
CREATE TABLE [dbo].[PASalesHistory](
    [IdSale] INT IDENTITY(1,1) NOT NULL,
    [IdClient] INT NOT NULL,
    [IdCampaign] INT NULL,
    [SaleTotal] DECIMAL(16, 2) NOT NULL,
    [CreatedAt] DATETIME NOT NULL DEFAULT GETDATE(),
    [UpdatedAt] DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT [PK_PASalesHistory] PRIMARY KEY ([IdSale]),
    CONSTRAINT [FK_PASalesHistory_PCRClients] FOREIGN KEY([IdClient])
        REFERENCES [dbo].[PCRClients] ([IdClient]),
    CONSTRAINT [FK_PASalesHistory_PCRCampaigns] FOREIGN KEY([IdCampaign])
        REFERENCES [dbo].[PCRCampaigns] ([IdCampaign])
)
GO

-- ===================================
-- Sample Data for Testing
-- ===================================

-- Insert sample statuses
INSERT INTO [dbo].[PCRCampaignStatuses] ([StatusDescription]) VALUES 
    ('Active'),
    ('Paused'),
    ('Completed'),
    ('Draft')
GO

INSERT INTO [dbo].[PCRClientStatuses] ([StatusDescription]) VALUES 
    ('Active'),
    ('Inactive'),
    ('Lead')
GO

-- Insert sample organization
INSERT INTO [dbo].[PCROrganizations] ([OrganizationName], [Website], [Industry], [CreatedAt], [UpdatedAt]) VALUES 
    ('Demo Company', 'www.democompany.com', 'Technology', GETDATE(), GETDATE())
GO

-- Insert sample geography
INSERT INTO [dbo].[PCRCountries] ([CountryName]) VALUES ('Costa Rica'), ('United States')
GO

INSERT INTO [dbo].[PCRStates] ([StateName], [IdCountry]) VALUES 
    ('San Jose', 1),
    ('California', 2)
GO

INSERT INTO [dbo].[PCRCities] ([CityName], [IdState]) VALUES 
    ('San Jose Centro', 1),
    ('Los Angeles', 2)
GO

-- Insert sample campaign
INSERT INTO [dbo].[PCRCampaigns] ([CampaignCode], [CampaignName], [IdOrganization], [IdStatus], [CreatedAt], [UpdatedAt]) VALUES 
    ('CAMP-001', 'Summer Sale 2025', 1, 1, GETDATE(), GETDATE())
GO

-- Insert sample client
INSERT INTO [dbo].[PCRClients] ([ClientCode], [IdStatus], [CreatedAt], [UpdatedAt]) VALUES 
    ('CLIENT-001', 1, GETDATE(), GETDATE())
GO

-- Insert sample metrics
DECLARE @CampaignId INT = (SELECT TOP 1 IdCampaign FROM [dbo].[PCRCampaigns])

INSERT INTO [dbo].[PACampaignDailyMetrics] ([IdCampaign], [Date], [Impressions], [Clicks], [Spend], [Conversions], [Reach], [UniqueUsers])
VALUES 
    (@CampaignId, '2025-11-01', 15000, 450, 500.00, 20, 12000, 9500),
    (@CampaignId, '2025-11-02', 18000, 520, 600.00, 25, 14000, 11000)
GO

DECLARE @CampaignId INT = (SELECT TOP 1 IdCampaign FROM [dbo].[PCRCampaigns])
INSERT INTO [dbo].[PACampaignChannelMetrics] ([IdCampaign], [Date], [ChannelName], [Platform], [Impressions], [Clicks], [Spend])
VALUES 
    (@CampaignId, '2025-11-01', 'Social Media', 'Facebook', 8000, 240, 250.00),
    (@CampaignId, '2025-11-01', 'Search', 'Google Ads', 7000, 210, 250.00)
GO

DECLARE @CampaignId INT = (SELECT TOP 1 IdCampaign FROM [dbo].[PCRCampaigns])
DECLARE @CityId INT = (SELECT TOP 1 IdCity FROM [dbo].[PCRCities])
DECLARE @CountryId INT = (SELECT TOP 1 IdCountry FROM [dbo].[PCRCountries])

INSERT INTO [dbo].[PACampaignGeoMetrics] ([IdCampaign], [Date], [IdCity], [IdCountry], [Impressions], [Clicks])
VALUES 
    (@CampaignId, '2025-11-01', @CityId, @CountryId, 10000, 300)
GO

DECLARE @CampaignId INT = (SELECT TOP 1 IdCampaign FROM [dbo].[PCRCampaigns])
DECLARE @ClientId INT = (SELECT TOP 1 IdClient FROM [dbo].[PCRClients])

INSERT INTO [dbo].[PASalesHistory] ([IdClient], [IdCampaign], [SaleTotal], [CreatedAt], [UpdatedAt])
VALUES 
    (@ClientId, @CampaignId, 2500.00, GETDATE(), GETDATE()),
    (@ClientId, @CampaignId, 1800.00, GETDATE(), GETDATE())
GO

PRINT 'Database PromptAds created successfully with sample data!'
GO
