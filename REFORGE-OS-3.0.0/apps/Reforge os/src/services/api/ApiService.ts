/**
 * Enterprise API Service Layer
 * 
 * Refactored API service using the new HTTP client and error handling
 */

import { httpClient } from '../http/HttpClient';
import type {
  DeviceProfile,
  OwnershipAttestation,
  LegalClassification,
  LanguageOutput,
  ComplianceReport,
  AuthorityRoute,
  AuditEvent,
  AuditEventsResponse,
} from '@types/api';
import type {
  TrapdoorWorkflow,
  TrapdoorWorkflowExecution,
  TrapdoorWorkflowResponse,
  TrapdoorBatchExecution,
  TrapdoorBatchResponse,
  ShadowLogsResponse,
  ShadowLogStats,
} from '@types/trapdoor';
import type {
  Solution,
  SolutionSearchParams,
  SolutionListResponse,
  SolutionResponse,
} from '@types/custodial-closet';
import { config } from '@config/environment';

const API_BASE = '/api/v1';
const TRAPDOOR_BASE = '/api/trapdoor';

/**
 * ForgeWorks Core API Service
 */
export class ForgeWorksApiService {
  /**
   * Analyzes a device
   */
  async analyzeDevice(metadata: unknown): Promise<DeviceProfile> {
    const response = await httpClient.post<DeviceProfile>(
      `${API_BASE}/device/analyze`,
      metadata
    );
    return response.data;
  }

  /**
   * Verifies device ownership
   */
  async verifyOwnership(
    deviceId: string,
    attestations: unknown
  ): Promise<OwnershipAttestation> {
    const response = await httpClient.post<OwnershipAttestation>(
      `${API_BASE}/ownership/verify`,
      { deviceId, attestations }
    );
    return response.data;
  }

  /**
   * Classifies device legally
   */
  async classifyLegal(
    deviceId: string,
    jurisdiction: string
  ): Promise<LegalClassification> {
    const response = await httpClient.post<LegalClassification>(
      `${API_BASE}/legal/classify`,
      { deviceId, jurisdiction }
    );
    return response.data;
  }

  /**
   * Shapes language output
   */
  async shapeLanguage(
    deviceContext: unknown,
    classification: unknown
  ): Promise<LanguageOutput> {
    const response = await httpClient.post<LanguageOutput>(
      `${API_BASE}/language/shape`,
      { deviceContext, classification }
    );
    return response.data;
  }

  /**
   * Gets authority routes
   */
  async getAuthorityRoutes(
    deviceId: string,
    classification: string
  ): Promise<AuthorityRoute[]> {
    const response = await httpClient.post<AuthorityRoute[]>(
      `${API_BASE}/route/authority`,
      { deviceId, classification }
    );
    return response.data;
  }

  /**
   * Gets compliance summary
   */
  async getComplianceSummary(deviceId: string): Promise<ComplianceReport> {
    const response = await httpClient.post<ComplianceReport>(
      `${API_BASE}/compliance/summary`,
      { deviceId }
    );
    return response.data;
  }

  /**
   * Performs interpretive review
   */
  async interpretiveReview(
    deviceId: string,
    ownershipConfidence: number
  ): Promise<{
    riskFraming: string;
    historicalContext: string;
    authorityPaths: AuthorityRoute[];
  }> {
    const response = await httpClient.post<{
      riskFraming: string;
      historicalContext: string;
      authorityPaths: AuthorityRoute[];
    }>(
      `${API_BASE}/interpretive/review`,
      { deviceId },
      {
        headers: {
          'X-Ownership-Confidence': ownershipConfidence.toString(),
        },
      }
    );
    return response.data;
  }

  /**
   * Generates compliance report
   */
  async generateComplianceReport(deviceId: string): Promise<ComplianceReport> {
    const response = await httpClient.post<ComplianceReport>(
      `${API_BASE}/report/compliance`,
      { deviceId }
    );
    return response.data;
  }

  /**
   * Gets audit events
   */
  async getAuditEvents(params?: {
    deviceId?: string;
    limit?: number;
    offset?: number;
  }): Promise<AuditEventsResponse> {
    const queryParams = new URLSearchParams();
    if (params?.deviceId) queryParams.append('deviceId', params.deviceId);
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    if (params?.offset) queryParams.append('offset', params.offset.toString());

    const query = queryParams.toString();
    const response = await httpClient.get<AuditEventsResponse>(
      `${API_BASE}/audit/events${query ? `?${query}` : ''}`
    );
    return response.data;
  }

  /**
   * Exports audit log
   */
  async exportAuditLog(deviceId: string): Promise<Blob> {
    const response = await httpClient.get<Blob>(
      `${API_BASE}/audit/export?deviceId=${deviceId}`,
      {
        headers: {
          'Accept': 'application/octet-stream',
        },
      }
    );
    return response.data;
  }

  /**
   * Gets certification status
   */
  async getCertificationStatus(): Promise<{
    level: string;
    requirements_met: boolean;
    next_level?: string;
  }> {
    const response = await httpClient.get<{
      level: string;
      requirements_met: boolean;
      next_level?: string;
    }>(`${API_BASE}/certification/status`);
    return response.data;
  }

  /**
   * Gets operations metrics
   */
  async getOpsMetrics(): Promise<{
    activeUnits: number;
    auditCoverage: number;
    complianceEscalations: number;
  }> {
    const response = await httpClient.get<{
      activeUnits: number;
      auditCoverage: number;
      complianceEscalations: number;
    }>(`${API_BASE}/ops/metrics`);
    return response.data;
  }
}

/**
 * Trapdoor API Service (Admin/Secret Room)
 */
export class TrapdoorApiService {
  /**
   * Executes FRP bypass workflow
   */
  async executeFRP(
    deviceSerial: string,
    authorization: { confirmed: boolean; userInput: string }
  ): Promise<TrapdoorWorkflowResponse> {
    if (!config.trapdoor.enabled) {
      throw new Error('Trapdoor API is not enabled');
    }

    const response = await httpClient.post<TrapdoorWorkflowResponse>(
      `${TRAPDOOR_BASE}/frp`,
      { deviceSerial, authorization }
    );
    return response.data;
  }

  /**
   * Executes bootloader unlock
   */
  async executeUnlock(
    deviceSerial: string,
    authorization: { confirmed: boolean; userInput: string }
  ): Promise<TrapdoorWorkflowResponse> {
    if (!config.trapdoor.enabled) {
      throw new Error('Trapdoor API is not enabled');
    }

    const response = await httpClient.post<TrapdoorWorkflowResponse>(
      `${TRAPDOOR_BASE}/unlock`,
      { deviceSerial, authorization }
    );
    return response.data;
  }

  /**
   * Executes custom workflow
   */
  async executeWorkflow(
    execution: TrapdoorWorkflowExecution
  ): Promise<TrapdoorWorkflowResponse> {
    if (!config.trapdoor.enabled) {
      throw new Error('Trapdoor API is not enabled');
    }

    const response = await httpClient.post<TrapdoorWorkflowResponse>(
      `${TRAPDOOR_BASE}/workflow/execute`,
      execution
    );
    return response.data;
  }

  /**
   * Lists available workflows
   */
  async listWorkflows(): Promise<{
    success: boolean;
    workflows: TrapdoorWorkflow[];
  }> {
    if (!config.trapdoor.enabled) {
      throw new Error('Trapdoor API is not enabled');
    }

    const response = await httpClient.get<{
      success: boolean;
      workflows: TrapdoorWorkflow[];
    }>(`${TRAPDOOR_BASE}/workflows`);
    return response.data;
  }

  /**
   * Executes batch commands
   */
  async executeBatch(
    batch: TrapdoorBatchExecution
  ): Promise<TrapdoorBatchResponse> {
    if (!config.trapdoor.enabled) {
      throw new Error('Trapdoor API is not enabled');
    }

    const response = await httpClient.post<TrapdoorBatchResponse>(
      `${TRAPDOOR_BASE}/batch/execute`,
      batch
    );
    return response.data;
  }

  /**
   * Gets shadow logs
   */
  async getShadowLogs(date?: string): Promise<ShadowLogsResponse> {
    if (!config.trapdoor.enabled) {
      throw new Error('Trapdoor API is not enabled');
    }

    const query = date ? `?date=${date}` : '';
    const response = await httpClient.get<ShadowLogsResponse>(
      `${TRAPDOOR_BASE}/logs/shadow${query}`
    );
    return response.data;
  }

  /**
   * Gets shadow log statistics
   */
  async getShadowLogStats(): Promise<{
    success: boolean;
    stats: ShadowLogStats;
  }> {
    if (!config.trapdoor.enabled) {
      throw new Error('Trapdoor API is not enabled');
    }

    const response = await httpClient.get<{
      success: boolean;
      stats: ShadowLogStats;
    }>(`${TRAPDOOR_BASE}/logs/stats`);
    return response.data;
  }

  /**
   * Rotates shadow logs
   */
  async rotateShadowLogs(): Promise<{
    success: boolean;
    message: string;
  }> {
    if (!config.trapdoor.enabled) {
      throw new Error('Trapdoor API is not enabled');
    }

    const response = await httpClient.post<{
      success: boolean;
      message: string;
    }>(`${TRAPDOOR_BASE}/logs/rotate`);
    return response.data;
  }
}

/**
 * Custodial Closet API Service (Solutions Database)
 */
export class CustodialClosetApiService {
  /**
   * Lists solutions
   */
  async listSolutions(
    params?: SolutionSearchParams
  ): Promise<SolutionListResponse> {
    const queryParams = new URLSearchParams();
    if (params?.device_type) queryParams.append('device_type', params.device_type);
    if (params?.category) queryParams.append('category', params.category);
    if (params?.search) queryParams.append('search', params.search);
    if (params?.difficulty) queryParams.append('difficulty', params.difficulty);
    if (params?.tags) params.tags.forEach(tag => queryParams.append('tags', tag));
    if (params?.limit) queryParams.append('limit', params.limit.toString());
    if (params?.offset) queryParams.append('offset', params.offset.toString());

    const query = queryParams.toString();
    const response = await httpClient.get<SolutionListResponse>(
      `${API_BASE}/solutions${query ? `?${query}` : ''}`
    );
    return response.data;
  }

  /**
   * Gets solution by ID
   */
  async getSolution(solutionId: string): Promise<SolutionResponse> {
    const response = await httpClient.get<SolutionResponse>(
      `${API_BASE}/solutions/${solutionId}`
    );
    return response.data;
  }

  /**
   * Gets solutions by device type
   */
  async getSolutionsByDeviceType(
    deviceType: string
  ): Promise<SolutionListResponse> {
    const response = await httpClient.get<SolutionListResponse>(
      `${API_BASE}/solutions/device-types/${deviceType}`
    );
    return response.data;
  }
}

/**
 * Default service instances
 */
export const forgeWorksApi = new ForgeWorksApiService();
export const trapdoorApi = new TrapdoorApiService();
export const custodialClosetApi = new CustodialClosetApiService();
