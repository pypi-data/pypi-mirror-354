"""Cloud API client."""

from typing import List, Dict, Any, Optional

from pydantic import BaseModel

from .common import get_api_client


class Session(BaseModel):
    """Cloud session information."""
    jobId: Optional[str] = None
    sessionId: str
    url: Optional[str] = None
    createdAt: int
    lastActivity: int


class CloudAPI:
    """Cloud API client."""
    
    async def get_sessions(self) -> List[Session]:
        """Get all cloud sessions."""
        client = await get_api_client()
        # Use cloud URL instead of API URL
        from hcli.env import ENV
        old_base_url = client.client.base_url
        client.client.base_url = ENV.HCLI_CLOUD_URL
        
        try:
            data = await client.get_json("/sessions")
            return [Session(**item) for item in data]
        finally:
            # Restore original base URL
            client.client.base_url = old_base_url
    
    async def delete_session(self, session_id: str) -> None:
        """Delete a cloud session."""
        client = await get_api_client()
        # Use cloud URL instead of API URL
        from hcli.env import ENV
        old_base_url = client.client.base_url
        client.client.base_url = ENV.HCLI_CLOUD_URL
        
        try:
            await client.delete_json(f"/sessions/{session_id}")
        finally:
            # Restore original base URL
            client.client.base_url = old_base_url
    
    async def create_session(self, tool: str, metadata: Dict[str, str]) -> Any:
        """Create a new cloud session."""
        client = await get_api_client()
        # Use cloud URL instead of API URL
        from hcli.env import ENV
        old_base_url = client.client.base_url
        client.client.base_url = ENV.HCLI_CLOUD_URL
        
        try:
            return await client.post_json("/sessions", {
                "tool": tool,
                "metadata": metadata
            })
        finally:
            # Restore original base URL
            client.client.base_url = old_base_url


# Global instance
cloud = CloudAPI()