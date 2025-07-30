from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Version(BaseModel):
    pipeline_id: str = Field(alias="pipelineId")
    major_version: int = Field(alias="majorVersion")
    minor_version: int = Field(alias="minorVersion")
    version_number: str = Field(alias="versionNumber")
    is_draft_version: bool = Field(alias="isDraftVersion")
    is_latest: bool = Field(alias="isLatest")
    steps: Optional[List[Dict[str, Any]]] = None
    alignment: str
    id: str
    tenant_id: str = Field(alias="tenantId")
    project_id: str = Field(alias="projectId")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    user_id: str = Field(alias="userId")


class ExecutionStats(BaseModel):
    success_count: int = Field(alias="successCount")
    failure_count: int = Field(alias="failureCount")


class GetPipelineConfigResponse(BaseModel):
    deployment_id: Optional[str] = Field(alias="deploymentId")
    deployment_name: Optional[str] = Field(alias="deploymentName")
    deployment_description: Optional[str] = Field(alias="deploymentDescription")
    user_keys: Dict[str, Any] = Field(alias="userKeys")
    group_keys: Dict[str, Any] = Field(alias="groupKeys")
    agent_icon: Optional[str] = Field(alias="agentIcon")
    external: bool
    active_version_id: str = Field(alias="activeVersionId")
    name: str
    execution_name: str = Field(alias="executionName")
    description: str
    video_link: Optional[str] = Field(alias="videoLink")
    agent_icon_id: Optional[str] = Field(alias="agentIconId")
    versions: List[Version]
    execution_stats: ExecutionStats = Field(alias="executionStats")
    industry: Optional[str]
    sub_industries: List[str] = Field(alias="subIndustries")
    agent_details: Dict[str, Any] = Field(alias="agentDetails")
    agent_details_tags: List[str] = Field(alias="agentDetailsTags")
    active_version: Version = Field(alias="activeVersion")
    backup_pipeline_id: Optional[str] = Field(alias="backupPipelineId")
    deployment: Optional[Any]
    library_agent_id: Optional[str] = Field(alias="libraryAgentId")
    library_imported_hash: Optional[str] = Field(alias="libraryImportedHash")
    library_imported_version: Optional[str] = Field(alias="libraryImportedVersion")
    is_deleted: Optional[bool] = Field(alias="isDeleted")
    agent_trigger: Optional[Any] = Field(alias="agentTrigger")
    api_key_id: Optional[str] = Field(alias="apiKeyId")
    is_seeded: bool = Field(alias="isSeeded")
    behaviours: List[Any]
    id: str
    tenant_id: str = Field(alias="tenantId")
    project_id: str = Field(alias="projectId")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    user_id: str = Field(alias="userId")
