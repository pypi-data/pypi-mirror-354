from typing import Dict, Optional, Any, List
from cognite.client import CogniteClient
from ..data_classes import AgentMessage
from ..tools import FunctionTool
import json


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
        agent_external_id: str,
        *,
        tools: Optional[List[FunctionTool]] = None,
    ) -> None:
        self._cognite_client = cognite_client
        self._agent_external_id = agent_external_id
        self._cursor = None
        self._tools = {tool.name: tool for tool in tools or []}
        self._use_internal = bool(self._tools)
        self._actions = []
        self.raw_responses: List[Dict[str, Any]] = []
        for t in self._tools.values():
            schema = dict(t.params_json_schema)
            schema.pop("title", None)
            self._actions.append(
                {
                    "type": "clientTool",
                    "clientTool": {
                        "name": t.name,
                        "description": t.description,
                        "parameters": schema,
                    },
                }
            )

    def chat(self, message: str) -> Optional[AgentMessage]:
        """
        Send a message to the agent and get a response.

        Args:
            message: The message to send.

        Returns:
            Optional[AgentMessage]: The agent's response message, or None if the response is not a result.
        """
        user_message = {"content": {"type": "text", "text": message}, "role": "user"}

        return self._send_messages([user_message])

    def _send_messages(self, messages: List[Dict[str, Any]]) -> Optional[AgentMessage]:
        request: Dict[str, Any] = {
            "agentId": self._agent_external_id,
            "messages": messages,
        }
        if self._cursor:
            request["cursor"] = self._cursor
        if self._use_internal and self._actions:
            request["actions"] = self._actions

        path = "/ai/internal/agents/chat" if self._use_internal else "/ai/agents/chat"
        url = f"/api/v1/projects/{self._cognite_client.config.project}{path}"

        response = self._cognite_client.post(
            url, json=request, headers={"cdf-version": "alpha"}
        )

        response_json = response.json()
        self.raw_responses.append(response_json)
        actual_response = response_json.get("response", {})
        self._cursor = actual_response.get("cursor")

        if actual_response.get("type") != "result":
            return None

        agent_messages = actual_response.get("messages", [])
        if not agent_messages:
            return None

        agent_response_data = agent_messages[0]

        actions = agent_response_data.get("actions")
        if actions and self._use_internal:
            action_messages = []
            for action in actions:
                if action.get("type") != "clientTool":
                    continue
                tool_name = action["clientTool"]["name"]
                args_str = action["clientTool"].get("arguments", "{}")
                args = json.loads(args_str) if args_str else {}
                tool = self._tools.get(tool_name)
                if tool is None:
                    raise ValueError(f"No tool registered with name {tool_name}")
                result = tool.run(**args)
                action_messages.append(
                    {
                        "actionId": action["id"],
                        "role": "action",
                        "type": "clientTool",
                        "content": {"type": "text", "text": str(result)},
                    }
                )

            if action_messages:
                return self._send_messages(action_messages)

        return AgentMessage.from_dict(agent_response_data)
