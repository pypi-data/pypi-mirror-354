# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .shared.subject import Subject

__all__ = ["EnvironmentMetadata"]


class EnvironmentMetadata(BaseModel):
    annotations: Optional[Dict[str, str]] = None
    """
    annotations are key/value pairs that gets attached to the environment.
    +internal - not yet implemented
    """

    archived_at: Optional[datetime] = FieldInfo(alias="archivedAt", default=None)
    """Time when the Environment was archived.

    If not set, the environment is not archived.
    """

    created_at: Optional[datetime] = FieldInfo(alias="createdAt", default=None)
    """Time when the Environment was created."""

    creator: Optional[Subject] = None
    """creator is the identity of the creator of the environment"""

    last_started_at: Optional[datetime] = FieldInfo(alias="lastStartedAt", default=None)
    """Time when the Environment was last started (i.e.

    CreateEnvironment or StartEnvironment were called).
    """

    name: Optional[str] = None
    """name is the name of the environment as specified by the user"""

    organization_id: Optional[str] = FieldInfo(alias="organizationId", default=None)
    """organization_id is the ID of the organization that contains the environment"""

    original_context_url: Optional[str] = FieldInfo(alias="originalContextUrl", default=None)
    """
    original_context_url is the normalized URL from which the environment was
    created
    """

    project_id: Optional[str] = FieldInfo(alias="projectId", default=None)
    """
    If the Environment was started from a project, the project_id will reference the
    project.
    """

    runner_id: Optional[str] = FieldInfo(alias="runnerId", default=None)
    """Runner is the ID of the runner that runs this environment."""
