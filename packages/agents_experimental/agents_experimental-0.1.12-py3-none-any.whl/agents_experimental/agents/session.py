import inspect
import json
import uuid
from typing import Dict, List, Optional, Any, Union, Callable
from cognite.client import CogniteClient
from ..data_classes import AgentMessage


class AgentSession:
    """
    Represents a chat session with an agent.
    
    Args:
        cognite_client: The CogniteClient to use for authentication and API calls.
        agent_external_id: The external ID of the agent.
    """
    
    def __init__(
        self, 
        cognite_client: CogniteClient, 
        agent_external_id: str
    ):
        self._cognite_client = cognite_client
        self._agent_external_id = agent_external_id
        self._cursor = None
    
    def chat(self, message: str) -> Optional[AgentMessage]:
        """
        Send a message to the agent and get a response.
        
        Args:
            message: The message to send.
            
        Returns:
            Optional[AgentMessage]: The agent's response message, or None if the response is not a result.
        """
        # Create the user message according to the new schema
        user_message = {
            "content": {
                "type": "text",
                "text": message
            },
            "role": "user"
        }
        
        # Prepare the request with only the new message
        request: Dict[str, Any] = {
            "agentId": self._agent_external_id,
            "messages": [user_message] 
        }
        
        # Add cursor if we have one
        if self._cursor:
            request["cursor"] = self._cursor
        
        # Make the API call
        url = f"/api/v1/projects/{self._cognite_client.config.project}/ai/agents/chat"
        response = self._cognite_client.post(
            url,
            json=request,
            headers={"cdf-version": "alpha"} # Assuming alpha version, update if needed
        )
        
        response_json = response.json()
        
        # Extract the actual response based on the type ("result" or "progress")
        actual_response = response_json.get("response", {})
        
        # Store the cursor for the next request (only available in "result" type)
        self._cursor = actual_response.get("cursor")
        
        # Process the response only if it's a "result"
        if actual_response.get("type") == "result":
            agent_messages = actual_response.get("messages", [])
            if agent_messages:
                # Assuming the API returns the latest agent message as the first item
                agent_response_data = agent_messages[0]
                return AgentMessage.from_dict(agent_response_data)
        
        # Return None if it's a progress message or no message is found
        return None 