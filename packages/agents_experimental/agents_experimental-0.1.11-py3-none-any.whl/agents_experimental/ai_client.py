from cognite.client import CogniteClient
from .agents import AgentsAPI


class AIClient:
    """
    Client for interacting with Cognite AI services.
    
    Args:
        cognite_client: The CogniteClient to use for authentication and API calls.
    """
    
    def __init__(self, cognite_client: CogniteClient):
        self._cognite_client = cognite_client
        self._agents = AgentsAPI(self._cognite_client)
    
    @property
    def agents(self) -> AgentsAPI:
        """
        Access the Agents API.
        
        Returns:
            AgentsAPI: The Agents API client.
        """
        return self._agents 