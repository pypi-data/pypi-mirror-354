from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union, Literal


@dataclass
class DataModel:
    """
    Represents a data model in the Cognite Data Modeling knowledge graph used for
    query generation.
    """

    space: str
    external_id: str
    version: str
    view_external_ids: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation for API calls."""
        result: Dict[str, Any] = {
            "space": self.space,
            "externalId": self.external_id,
            "version": self.version,
        }
        if self.view_external_ids:
            result["viewExternalIds"] = self.view_external_ids
        return result


@dataclass
class Tool:
    """
    Base class for agent tools.
    """

    type: str
    name: str
    description: str
    configuration: Any = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation for API calls."""
        configuration = self.configuration
        if hasattr(configuration, "to_dict"):
            configuration = configuration.to_dict()
        return {
            "type": self.type,
            "name": self.name,
            "description": self.description,
            "configuration": configuration,
        }


@dataclass
class AskDocumentTool(Tool):
    """
    Tool for answering questions from documents.
    """

    # Make fields with defaults keyword-only to avoid inheritance order issues
    type: Literal["askDocument"] = field(default="askDocument", kw_only=True)
    configuration: Dict[str, Any] = field(default_factory=dict, kw_only=True)


@dataclass
class SummarizeDocumentTool(Tool):
    """
    Tool for summarizing documents.
    """

    # Make fields with defaults keyword-only
    type: Literal["summarizeDocument"] = field(
        default="summarizeDocument", kw_only=True
    )
    configuration: Dict[str, Any] = field(default_factory=dict, kw_only=True)


@dataclass
class DataModelReference:
    """
    Represents a reference to a view in the Cognite Data Modeling knowledge
    graph.
    """

    space: str
    external_id: str
    version: str
    view_external_ids: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "space": self.space,
            "externalId": self.external_id,
            "version": self.version,
        }
        if self.view_external_ids:
            result["viewExternalIds"] = self.view_external_ids
        return result


@dataclass
class QueryKnowledgeGraphToolConfiguration:
    """
    Configuration for :class:`QueryKnowledgeGraphTool` when querying the Cognite
    Data Modeling knowledge graph.
    """

    data_models: List[DataModelReference]
    instance_spaces: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "dataModels": [model.to_dict() for model in self.data_models]
        }
        if self.instance_spaces is not None:
            result["instanceSpaces"] = self.instance_spaces
        return result


@dataclass
class QueryKnowledgeGraphTool(Tool):
    """
    Tool for querying the knowledge graph (Cognite Data Modeling).
    """

    # configuration is non-default here, only type needs kw_only
    configuration: QueryKnowledgeGraphToolConfiguration
    type: Literal["queryKnowledgeGraph"] = field(
        default="queryKnowledgeGraph", kw_only=True
    )


@dataclass
class QueryTimeSeriesDatapointsTool(Tool):
    """
    Tool for querying time series datapoints.
    """

    # Make fields with defaults keyword-only
    type: Literal["queryTimeSeriesDatapoints"] = field(
        default="queryTimeSeriesDatapoints", kw_only=True
    )
    configuration: Dict[str, Any] = field(default_factory=dict, kw_only=True)


# Agent Definition using the defined tools
# Allow Union of specific tool types for better type hinting
SupportedTool = Union[
    AskDocumentTool,
    SummarizeDocumentTool,
    QueryKnowledgeGraphTool,
    QueryTimeSeriesDatapointsTool,
]


@dataclass
class AgentDefinition:
    """
    Definition for creating or updating an agent.
    Aligns with AgentCreationRequestItem in OpenAPI.
    """

    external_id: str
    name: str
    tools: List[SupportedTool] = field(default_factory=list)
    description: Optional[str] = None
    instructions: Optional[str] = None
    model: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation for API calls."""
        result: Dict[str, Any] = {
            "externalId": self.external_id,
            "name": self.name,
            "tools": [tool.to_dict() for tool in self.tools],
        }
        if self.description:
            result["description"] = self.description
        if self.instructions:
            result["instructions"] = self.instructions
        if self.model:
            result["model"] = self.model
        return result


@dataclass
class AgentContent:
    """
    Represents the content of a message (AgentContentDTO).
    """

    type: Literal["text"] = "text"
    text: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentContent":
        return cls(
            type=data.get("type", "text"),  # Should always be text for now
            text=data.get("text"),
        )

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {"type": self.type}
        if self.text:
            result["text"] = self.text
        return result


@dataclass
class Reasoning:
    """
    Represents a reasoning step from an agent.
    """

    content: List[AgentContent]  # Content is now a list of AgentContentDTO
    # type is implicitly defined by the content or other fields if added later

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Reasoning":
        content_list = data.get("content", [])
        return cls(content=[AgentContent.from_dict(c) for c in content_list])


@dataclass
class AgentData:
    """
    Represents data attached to an agent message (AgentDataDTO).
    """

    type: Literal["instances"] = "instances"
    instances: Optional[Dict[str, Any]] = (
        None  # The structure of instances isn't fully defined in the spec
    )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentData":
        return cls(type=data.get("type", "instances"), instances=data.get("instances"))


@dataclass
class AgentMessage:
    """
    Represents a message from an agent (AgentChatMessageAgentResponseDTO).
    Focuses on content, reasoning, and data, ignoring actions/tool calls.
    """

    # Role is required in the response, so no default needed.
    role: Literal["agent"]
    content: AgentContent  # Now a structured object
    # Default factories are kept for convenience when accessing the response object
    reasoning: List[Reasoning] = field(default_factory=list)
    data: List[AgentData] = field(default_factory=list)  # Use AgentData type hint

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentMessage":
        """Create an AgentMessage from a dictionary, ignoring actions."""
        content_data = data.get("content", {})

        reasoning = []
        if "reasoning" in data:
            for reasoning_data in data.get("reasoning", []):
                reasoning.append(Reasoning.from_dict(reasoning_data))

        data_items = []  # Renamed variable for clarity
        if "data" in data:
            for data_item_dict in data.get("data", []):
                data_items.append(
                    AgentData.from_dict(data_item_dict)
                )  # Use AgentData.from_dict

        return cls(
            role=data["role"],
            content=AgentContent.from_dict(content_data),
            reasoning=reasoning,
            data=data_items,  # Assign the parsed AgentData list
        )

    # Helper property for backward compatibility/ease of use if needed
    @property
    def message(self) -> Optional[str]:
        return self.content.text
