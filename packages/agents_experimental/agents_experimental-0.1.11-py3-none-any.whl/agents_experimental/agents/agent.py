from typing import Dict, List, Optional, Any
import json
from datetime import datetime

from cognite.client import CogniteClient
from .session import AgentSession



class Agent:
    """
    Represents an agent retrieved from the Cognite AI platform.
    Initialized with data typically received from API responses 
    (AgentCreationResponseItem or AgentListResponseItem).

    Args:
        cognite_client: The CogniteClient to use for authentication and API calls.
        data: The agent data dictionary from the API response.
    """
    
    def __init__(self, cognite_client: CogniteClient, data: Dict[str, Any]):
        self._cognite_client = cognite_client
        self._data = data
        # Store fields directly as private attributes
        self._external_id: str = data["externalId"]
        self._name: str = data["name"]
        self._description: Optional[str] = data.get("description")
        self._instructions: Optional[str] = data.get("instructions")
        self._model: Optional[str] = data.get("model")
        self._owner_id: Optional[str] = data.get("ownerId")
        # Convert timestamps (assuming they are Unix epoch milliseconds)
        self._created_time: Optional[datetime] = (
            datetime.fromtimestamp(data["createdTime"] / 1000)
            if "createdTime" in data else None
        )
        self._last_updated_time: Optional[datetime] = (
            datetime.fromtimestamp(data["lastUpdatedTime"] / 1000)
            if "lastUpdatedTime" in data else None
        )
        # Store raw tools list for now. Future: parse into specific Tool objects
        self._tools_data: List[Dict[str, Any]] = data.get("tools", [])
    
    @property
    def external_id(self) -> str:
        """
        Get the external ID of the agent.
        
        Returns:
            str: The external ID.
        """
        return self._external_id
    
    @property
    def name(self) -> str:
        """
        Get the name of the agent.
        
        Returns:
            str: The name.
        """
        return self._name
    
    @property
    def description(self) -> Optional[str]:
        """
        Get the description of the agent.
        
        Returns:
            Optional[str]: The description, or None if not set.
        """
        return self._description
    
    @property
    def instructions(self) -> Optional[str]:
        """
        Get the instructions of the agent.
        
        Returns:
            Optional[str]: The instructions, or None if not set.
        """
        return self._instructions
    
    @property
    def model(self) -> Optional[str]:
        """
        Get the model used by the agent.
        
        Returns:
            Optional[str]: The model name, or None if not set.
        """
        return self._model
    
    @property
    def owner_id(self) -> Optional[str]:
        """
        Get the owner ID of the agent.
        
        Returns:
            Optional[str]: The owner ID, or None if not set.
        """
        return self._owner_id
    
    @property
    def created_time(self) -> Optional[datetime]:
        """
        Get the creation time of the agent.
        
        Returns:
            Optional[datetime]: The creation time, or None if not set.
        """
        return self._created_time
    
    @property
    def last_updated_time(self) -> Optional[datetime]:
        """
        Get the last updated time of the agent.
        
        Returns:
            Optional[datetime]: The last updated time, or None if not set.
        """
        return self._last_updated_time
    
    @property
    def tools(self) -> List[Dict[str, Any]]:
        """
        Get the tools available to the agent (raw dictionary representation).
        
        Returns:
            List[Dict[str, Any]]: The list of tool dictionaries.
        """
        return self._tools_data
    
    def __str__(self) -> str:
        """
        Get a string representation of the agent.
        
        Returns:
            str: A JSON string representation of the agent data.
        """
        return json.dumps(self._data, indent=2, default=str)
    
    def __repr__(self) -> str:
        """
        Get a concise representation of the agent for debugging.
        
        Returns:
            str: A concise representation of the agent.
        """
        tool_names = [tool.get("name", f"Tool_{i}") for i, tool in enumerate(self.tools)]
        return (
            f"Agent(external_id='{self.external_id}', name='{self.name}', "
            f"model='{self.model}', tools={tool_names}, "
            f"owner='{self.owner_id}')"
        )
    
    def start_session(self) -> AgentSession:
        """
        Start a chat session with the agent.
            
        Returns:
            AgentSession: The chat session.
        """
        return AgentSession(self._cognite_client, agent_external_id=self.external_id)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the agent object back to a dictionary mirroring the API response structure.
        
        Returns:
            Dict[str, Any]: The agent data as a dictionary.
        """
        return self._data.copy()