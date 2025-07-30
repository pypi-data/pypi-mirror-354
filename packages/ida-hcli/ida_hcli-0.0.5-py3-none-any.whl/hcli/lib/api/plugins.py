"""Plugins API client."""

from typing import List, Optional, Dict

from pydantic import BaseModel

from .common import get_api_client


class PluginCategory(BaseModel):
    """Plugin category information."""
    id: str
    name: str
    description: str
    slug: str
    icon: str


class PluginCategoryInfo(BaseModel):
    """Plugin category with plugin count."""
    id: str
    name: str
    pluginCount: int


class ReleaseInfo(BaseModel):
    """Plugin release information."""
    latestRelease: str
    publishedAt: str
    url: str


class DynamicMetadata(BaseModel):
    """Dynamic metadata for plugins."""
    stars: int
    forks: int
    watchers: int
    openIssues: int
    language: str
    latestUpdate: str
    release: Optional[ReleaseInfo] = None


class Metadata(BaseModel):
    """Plugin metadata."""
    repository_name: str
    entryPoint: Optional[str] = None
    install: Optional[str] = None
    repository_description: str
    repository_owner: str
    dynamic_metadata: Optional[DynamicMetadata] = None


class Plugin(BaseModel):
    """Plugin information."""
    id: str
    owner: str
    name: str
    slug: str
    url: str
    updatedAt: Optional[str] = None
    metadata: Metadata
    categories: Optional[List[PluginCategory]] = None
    disabled: Optional[bool] = None


class SearchResult(BaseModel):
    """Search result wrapper."""
    hits: List[Plugin]
    query: str
    processingTimeMs: int
    limit: int
    offset: int
    estimatedTotalHits: int


class SearchResponse(BaseModel):
    """Full search response."""
    plugins: SearchResult
    authors: SearchResult


class PluginQuery(BaseModel):
    """Plugin search query parameters."""
    q: Optional[str] = None
    cslug: Optional[str] = None
    pslug: Optional[str] = None
    tags: Optional[str] = None
    limit: Optional[str] = None
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for URL parameters."""
        return {k: v for k, v in self.model_dump().items() if v is not None}


class PluginsAPI:
    """Plugins API client."""
    
    async def get_categories(self) -> List[PluginCategoryInfo]:
        """Get all plugin categories."""
        client = await get_api_client()
        data = await client.get_json("/plugin-repository/search/categories", auth=False)
        return [PluginCategoryInfo(**item) for item in data]
    
    async def get_plugins(self) -> SearchResult:
        """Get all plugins."""
        return await self.search(PluginQuery(limit="1000"))
    
    async def get_plugin(self, slug: str) -> Optional[Plugin]:
        """Get a specific plugin by slug."""
        client = await get_api_client()
        data = await client.get_json(f"/plugin-repository/search/plugins/{slug}", auth=False)
        search_result = SearchResult(**data)
        
        self._patch_search_result(search_result)
        
        if search_result.estimatedTotalHits == 1:
            return search_result.hits[0]
        else:
            return None
    
    async def search(self, query: Optional[PluginQuery] = None) -> SearchResult:
        """Search for plugins."""
        if query is None:
            query = PluginQuery()
        
        client = await get_api_client()
        
        # Build query string
        params = query.to_dict()
        if params:
            from urllib.parse import urlencode
            query_string = urlencode(params)
            url = f"/plugin-repository/search?{query_string}"
        else:
            url = "/plugin-repository/search"
        
        data = await client.get_json(url, auth=False)
        search_response = SearchResponse(**data)
        
        self._patch_search_result(search_response.plugins)
        
        return search_response.plugins
    
    def _patch_search_result(self, result: SearchResult):
        """Patch plugin hits with owner and name."""
        for hit in result.hits:
            self._patch_hit(hit)
    
    def _patch_hit(self, hit: Plugin):
        """Patch individual plugin with owner and name."""
        if "/" in hit.slug:
            owner, name = hit.slug.split("/", 1)
            hit.owner = owner
            hit.name = name
        hit.id = hit.slug


# Global instance
plugins = PluginsAPI()