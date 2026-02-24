import type { ElementType } from 'react';
import { BarChart3, Brain, Database, FileText, Mail, Zap } from 'lucide-react';

export type TemplateCategory = 'data' | 'ai' | 'integration' | 'reporting' | 'automation';

export interface PipelineTemplate {
    id: string;
    name: string;
    description: string;
    icon: ElementType;
    category: TemplateCategory;
    isOfficial: boolean;
    stageNames: string[];
}

export const templatesCatalog: PipelineTemplate[] = [
    {
        id: 'tpl-001',
        name: 'ETL Data Pipeline',
        description: 'Extract, Transform, Load data from multiple sources to a data warehouse',
        icon: Database,
        category: 'data',
        isOfficial: true,
        stageNames: ['Extract Source Data', 'Validate & Clean', 'Transform Dataset', 'Load to Warehouse'],
    },
    {
        id: 'tpl-002',
        name: 'ML Model Training',
        description: 'Complete pipeline for training and deploying ML models',
        icon: Brain,
        category: 'ai',
        isOfficial: true,
        stageNames: ['Ingest Training Data', 'Feature Engineering', 'Train Model', 'Evaluate Performance', 'Deploy Model'],
    },
    {
        id: 'tpl-003',
        name: 'Daily Report Generator',
        description: 'Generate and email daily business reports automatically',
        icon: FileText,
        category: 'reporting',
        isOfficial: true,
        stageNames: ['Collect Metrics', 'Generate Report', 'Email Stakeholders'],
    },
    {
        id: 'tpl-004',
        name: 'API Data Sync',
        description: 'Sync data between APIs and databases periodically',
        icon: Zap,
        category: 'integration',
        isOfficial: true,
        stageNames: ['Fetch API Payload', 'Normalize Records', 'Upsert to Database', 'Publish Sync Summary'],
    },
    {
        id: 'tpl-005',
        name: 'Log Analyzer',
        description: 'Process and analyze application logs for insights',
        icon: BarChart3,
        category: 'data',
        isOfficial: true,
        stageNames: ['Collect Logs', 'Parse Events', 'Aggregate Metrics'],
    },
    {
        id: 'tpl-006',
        name: 'Email Notifications',
        description: 'Send email notifications based on triggers and events',
        icon: Mail,
        category: 'automation',
        isOfficial: true,
        stageNames: ['Detect Trigger', 'Send Notification'],
    },
];

export const categoryLabels: Record<TemplateCategory, string> = {
    data: 'Data Processing',
    ai: 'AI & ML',
    integration: 'Integrations',
    reporting: 'Reporting',
    automation: 'Automation',
};
