from typing import List, Optional
from cognite.client import CogniteClient
from ..api.base import APIBase
from .agent import Agent
from ..data_classes import AgentDefinition


class AgentsAPI(APIBase):
    """
    API client for the Agents API.
    
    Args:
        cognite_client: The CogniteClient to use for authentication and API calls.
    """
    
    _RESOURCE_PATH = "/ai/agents"
    
    def __init__(self, cognite_client: CogniteClient):
        super().__init__(cognite_client)
    
    def create(self, agent: AgentDefinition) -> Agent:
        """
        Create or update an agent.
        
        Args:
            agent: The agent definition to create or update.
            
        Returns:
            Agent: The created or updated agent.
        """
        agent_dict = agent.to_dict()
        
        request = {
            "items": [agent_dict]
        }
        response = self._post("", json=request)
        return Agent(self._cognite_client, response["items"][0])
    
    def list(self, limit: Optional[int] = None) -> List[Agent]:
        """
        List agents.
        
        Args:
            limit: Maximum number of agents to return. Defaults to None (service default).
            
        Returns:
            List[Agent]: The list of agents.
        """
        params = {} if limit is None else {"limit": limit}
        response = self._get("", params=params)
        return [Agent(self._cognite_client, item) for item in response["items"]]
    
    def retrieve(self, external_id: str, ignore_unknown_ids: bool = False) -> Optional[Agent]:
        """
        Retrieve an agent by external ID.
        
        Args:
            external_id: The external ID of the agent.
            ignore_unknown_ids: If true, unknown external IDs will be ignored.
                               Defaults to False.
            
        Returns:
            Optional[Agent]: The retrieved agent, or None if not found and ignore_unknown_ids is True.
        """
        request = {
            "items": [{"externalId": external_id}],
            "ignoreUnknownIds": ignore_unknown_ids
        }
        response = self._post("/byids", json=request)
        
        if not response["items"]:
            if ignore_unknown_ids:
                return None
            else:
                raise ValueError(f"Agent with external ID {external_id} not found.")
                
        return Agent(self._cognite_client, response["items"][0])
    
    def delete(self, external_id: str, ignore_unknown_ids: bool = False) -> None:
        """
        Delete an agent by external ID.
        
        Args:
            external_id: The external ID of the agent to delete.
            ignore_unknown_ids: If true, unknown external IDs will be ignored.
                               Defaults to False.
        """
        request = {
            "items": [{"externalId": external_id}],
            "ignoreUnknownIds": ignore_unknown_ids
        }
        self._post("/delete", json=request) 