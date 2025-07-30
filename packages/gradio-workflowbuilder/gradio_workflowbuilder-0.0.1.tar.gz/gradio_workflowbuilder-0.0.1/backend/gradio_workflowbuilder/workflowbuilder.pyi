from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any

from gradio.components.base import Component, FormComponent
from gradio.events import Events
from gradio.i18n import I18nData

if TYPE_CHECKING:
    from gradio.components import Timer


class WorkflowBuilder(Component):
    """
    Professional Workflow Builder component with support for 25+ node types
    inspired by n8n and Langflow for AI agent development and MCP integration.
    """
    
    EVENTS = [Events.change, Events.input]

    def __init__(
        self,
        value: Optional[Dict[str, Any]] = None,
        label: Optional[str] = None,
        info: Optional[str] = None,
        show_label: Optional[bool] = None,
        container: bool = True,
        scale: Optional[int] = None,
        min_width: int = 160,
        visible: bool = True,
        elem_id: Optional[str] = None,
        elem_classes: Optional[List[str]] = None,
        render: bool = True,
        **kwargs,
    ):
        """
        Parameters:
            value: Default workflow data with nodes and edges
            label: Component label
            info: Additional component information
            show_label: Whether to show the label
            container: Whether to use container styling
            scale: Relative width scale
            min_width: Minimum width in pixels
            visible: Whether component is visible
            elem_id: HTML element ID
            elem_classes: CSS classes
            render: Whether to render immediately
        """
        
        # Initialize with empty workflow if no value provided
        if value is None:
            value = {"nodes": [], "edges": []}
        
        # Validate the workflow data
        if not isinstance(value, dict):
            raise ValueError("Workflow value must be a dictionary")
        
        if "nodes" not in value:
            value["nodes"] = []
        if "edges" not in value:
            value["edges"] = []
            
        super().__init__(
            label=label,
            info=info,
            show_label=show_label,
            container=container,
            scale=scale,
            min_width=min_width,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=render,
            value=value,
            **kwargs,
        )

    def preprocess(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process workflow data from frontend
        """
        if payload is None:
            return {"nodes": [], "edges": []}
        
        # Validate and clean the workflow data
        workflow = self._validate_workflow(payload)
        return workflow
    
    def postprocess(self, value: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process workflow data for frontend
        """
        if value is None:
            return {"nodes": [], "edges": []}
            
        # Ensure proper structure
        if not isinstance(value, dict):
            return {"nodes": [], "edges": []}
            
        return {
            "nodes": value.get("nodes", []),
            "edges": value.get("edges", [])
        }

    def _validate_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate workflow structure and node configurations
        """
        if not isinstance(workflow, dict):
            return {"nodes": [], "edges": []}
        
        nodes = workflow.get("nodes", [])
        edges = workflow.get("edges", [])
        
        # Validate each node
        validated_nodes = []
        for node in nodes:
            if self._validate_node(node):
                validated_nodes.append(node)
        
        # Validate each edge
        validated_edges = []
        node_ids = {node["id"] for node in validated_nodes}
        for edge in edges:
            if self._validate_edge(edge, node_ids):
                validated_edges.append(edge)
        
        return {
            "nodes": validated_nodes,
            "edges": validated_edges
        }
    
    def _validate_node(self, node: Dict[str, Any]) -> bool:
        """
        Validate individual node structure and properties
        """
        required_fields = ["id", "type", "position", "data"]
        
        # Check required fields
        if not all(field in node for field in required_fields):
            return False
        
        # Validate node type
        if not self._is_valid_node_type(node["type"]):
            return False
        
        # Validate position
        position = node["position"]
        if not isinstance(position, dict) or "x" not in position or "y" not in position:
            return False
        
        # Validate node data based on type
        return self._validate_node_data(node["type"], node["data"])
    
    def _validate_edge(self, edge: Dict[str, Any], valid_node_ids: set) -> bool:
        """
        Validate edge connections
        """
        required_fields = ["id", "source", "target"]
        
        if not all(field in edge for field in required_fields):
            return False
        
        # Check if source and target nodes exist
        return (edge["source"] in valid_node_ids and 
                edge["target"] in valid_node_ids)
    
    def _is_valid_node_type(self, node_type: str) -> bool:
        """
        Check if node type is supported
        """
        # All the node types from your frontend
        supported_types = {
            # Input/Output Nodes
            "ChatInput", "ChatOutput", "Input", "Output",
            
            # AI & Language Models
            "OpenAIModel", "ChatModel", "Prompt", "HFTextGeneration",
            
            # API & Web
            "APIRequest", "WebSearch",
            
            # Data Processing
            "ExecutePython", "ConditionalLogic", "Wait",
            
            # RAG & Knowledge
            "KnowledgeBase", "RAGQuery",
            
            # Speech & Vision
            "HFSpeechToText", "HFTextToSpeech", "HFVisionModel",
            
            # Image Generation
            "HFImageGeneration", "NebiusImage",
            
            # MCP Integration
            "MCPConnection", "MCPAgent",
            
            # Legacy types (for backward compatibility)
            "textInput", "fileInput", "numberInput", "llm", "textProcessor", 
            "conditional", "textOutput", "fileOutput", "chartOutput", 
            "apiCall", "dataTransform", "webhook", "schedule", "manualTrigger",
            "emailTrigger", "httpRequest", "googleSheets", "database", "csvFile",
            "openaiChat", "claudeChat", "huggingFace", "textEmbedding",
            "codeNode", "functionNode", "setNode", "jsonParse",
            "ifCondition", "switchNode", "merge", "waitNode",
            "email", "slack", "discord", "telegram",
            "fileUpload", "awsS3", "googleDrive", "ftp",
            "dateTime", "crypto", "validator", "regex"
        }
        
        return node_type in supported_types
    
    def _validate_node_data(self, node_type: str, data: Dict[str, Any]) -> bool:
        """
        Validate node data based on node type
        """
        if not isinstance(data, dict):
            return False
        
        # Define required fields for each node type
        required_fields = {
            # Input/Output Nodes
            "ChatInput": ["display_name", "template"],
            "ChatOutput": ["display_name", "template"],
            "Input": ["display_name", "template"],
            "Output": ["display_name", "template"],
            
            # AI & Language Models
            "OpenAIModel": ["display_name", "template"],
            "ChatModel": ["display_name", "template"],
            "Prompt": ["display_name", "template"],
            "HFTextGeneration": ["display_name", "template"],
            
            # API & Web
            "APIRequest": ["display_name", "template"],
            "WebSearch": ["display_name", "template"],
            
            # Data Processing
            "ExecutePython": ["display_name", "template"],
            "ConditionalLogic": ["display_name", "template"],
            "Wait": ["display_name", "template"],
            
            # RAG & Knowledge
            "KnowledgeBase": ["display_name", "template"],
            "RAGQuery": ["display_name", "template"],
            
            # Speech & Vision
            "HFSpeechToText": ["display_name", "template"],
            "HFTextToSpeech": ["display_name", "template"],
            "HFVisionModel": ["display_name", "template"],
            
            # Image Generation
            "HFImageGeneration": ["display_name", "template"],
            "NebiusImage": ["display_name", "template"],
            
            # MCP Integration
            "MCPConnection": ["display_name", "template"],
            "MCPAgent": ["display_name", "template"],
            
            # Legacy types
            "webhook": ["method", "path"],
            "httpRequest": ["method", "url"],
            "openaiChat": ["model"],
            "claudeChat": ["model"],
            "codeNode": ["language", "code"],
            "ifCondition": ["conditions"],
            "email": ["fromEmail", "toEmail", "subject"],
            "awsS3": ["operation", "bucketName"]
        }
        
        # Check required fields for this node type
        if node_type in required_fields:
            required = required_fields[node_type]
            if not all(field in data for field in required):
                return False
        
        return True

    def api_info(self) -> Dict[str, Any]:
        """
        API information for the component
        """
        return {
            "info": {
                "type": "object",
                "properties": {
                    "nodes": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},
                                "type": {"type": "string"},
                                "position": {
                                    "type": "object",
                                    "properties": {
                                        "x": {"type": "number"},
                                        "y": {"type": "number"}
                                    }
                                },
                                "data": {"type": "object"}
                            }
                        }
                    },
                    "edges": {
                        "type": "array", 
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},
                                "source": {"type": "string"},
                                "target": {"type": "string"}
                            }
                        }
                    }
                }
            }
        }

    def example_payload(self) -> Dict[str, Any]:
        """
        Example payload for the component
        """
        return {
            "nodes": [
                {
                    "id": "ChatInput-1",
                    "type": "ChatInput",
                    "position": {"x": 100, "y": 100},
                    "data": {
                        "display_name": "User's Question",
                        "template": {
                            "input_value": {
                                "display_name": "Input",
                                "type": "string",
                                "value": "What is the capital of France?",
                                "is_handle": True
                            }
                        }
                    }
                },
                {
                    "id": "Prompt-1",
                    "type": "Prompt",
                    "position": {"x": 300, "y": 100},
                    "data": {
                        "display_name": "System Prompt",
                        "template": {
                            "prompt_template": {
                                "display_name": "Template",
                                "type": "string",
                                "value": "You are a helpful geography expert. The user asked: {input_value}",
                                "is_handle": True
                            }
                        }
                    }
                },
                {
                    "id": "OpenAI-1",
                    "type": "OpenAIModel",
                    "position": {"x": 500, "y": 100},
                    "data": {
                        "display_name": "OpenAI gpt-4o-mini",
                        "template": {
                            "model": {
                                "display_name": "Model",
                                "type": "options",
                                "options": ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
                                "value": "gpt-4o-mini"
                            },
                            "api_key": {
                                "display_name": "API Key",
                                "type": "SecretStr",
                                "required": True,
                                "env_var": "OPENAI_API_KEY"
                            },
                            "prompt": {
                                "display_name": "Prompt",
                                "type": "string",
                                "is_handle": True
                            }
                        }
                    }
                },
                {
                    "id": "ChatOutput-1",
                    "type": "ChatOutput",
                    "position": {"x": 700, "y": 100},
                    "data": {
                        "display_name": "Final Answer",
                        "template": {
                            "response": {
                                "display_name": "Response",
                                "type": "string",
                                "is_handle": True
                            }
                        }
                    }
                }
            ],
            "edges": [
                {
                    "id": "e1",
                    "source": "ChatInput-1",
                    "source_handle": "input_value",
                    "target": "Prompt-1",
                    "target_handle": "prompt_template"
                },
                {
                    "id": "e2",
                    "source": "Prompt-1",
                    "source_handle": "prompt_template",
                    "target": "OpenAI-1",
                    "target_handle": "prompt"
                },
                {
                    "id": "e3",
                    "source": "OpenAI-1",
                    "source_handle": "response",
                    "target": "ChatOutput-1",
                    "target_handle": "response"
                }
            ]
        }

    def example_value(self) -> Dict[str, Any]:
        """
        Example value for the component
        """
        return self.example_payload()
    from typing import Callable, Literal, Sequence, Any, TYPE_CHECKING
    from gradio.blocks import Block
    if TYPE_CHECKING:
        from gradio.components import Timer
        from gradio.components.base import Component

    
    def change(self,
        fn: Callable[..., Any] | None = None,
        inputs: Block | Sequence[Block] | set[Block] | None = None,
        outputs: Block | Sequence[Block] | None = None,
        api_name: str | None | Literal[False] = None,
        scroll_to_output: bool = False,
        show_progress: Literal["full", "minimal", "hidden"] = "full",
        show_progress_on: Component | Sequence[Component] | None = None,
        queue: bool | None = None,
        batch: bool = False,
        max_batch_size: int = 4,
        preprocess: bool = True,
        postprocess: bool = True,
        cancels: dict[str, Any] | list[dict[str, Any]] | None = None,
        every: Timer | float | None = None,
        trigger_mode: Literal["once", "multiple", "always_last"] | None = None,
        js: str | Literal[True] | None = None,
        concurrency_limit: int | None | Literal["default"] = "default",
        concurrency_id: str | None = None,
        show_api: bool = True,
        key: int | str | tuple[int | str, ...] | None = None,
    
        ) -> Dependency:
        """
        Parameters:
            fn: the function to call when this event is triggered. Often a machine learning model's prediction function. Each parameter of the function corresponds to one input component, and the function should return a single value or a tuple of values, with each element in the tuple corresponding to one output component.
            inputs: list of gradio.components to use as inputs. If the function takes no inputs, this should be an empty list.
            outputs: list of gradio.components to use as outputs. If the function returns no outputs, this should be an empty list.
            api_name: defines how the endpoint appears in the API docs. Can be a string, None, or False. If False, the endpoint will not be exposed in the api docs. If set to None, will use the functions name as the endpoint route. If set to a string, the endpoint will be exposed in the api docs with the given name.
            scroll_to_output: if True, will scroll to output component on completion
            show_progress: how to show the progress animation while event is running: "full" shows a spinner which covers the output component area as well as a runtime display in the upper right corner, "minimal" only shows the runtime display, "hidden" shows no progress animation at all
            show_progress_on: Component or list of components to show the progress animation on. If None, will show the progress animation on all of the output components.
            queue: if True, will place the request on the queue, if the queue has been enabled. If False, will not put this event on the queue, even if the queue has been enabled. If None, will use the queue setting of the gradio app.
            batch: if True, then the function should process a batch of inputs, meaning that it should accept a list of input values for each parameter. The lists should be of equal length (and be up to length `max_batch_size`). The function is then *required* to return a tuple of lists (even if there is only 1 output component), with each list in the tuple corresponding to one output component.
            max_batch_size: maximum number of inputs to batch together if this is called from the queue (only relevant if batch=True)
            preprocess: if False, will not run preprocessing of component data before running 'fn' (e.g. leaving it as a base64 string if this method is called with the `Image` component).
            postprocess: if False, will not run postprocessing of component data before returning 'fn' output to the browser.
            cancels: a list of other events to cancel when this listener is triggered. For example, setting cancels=[click_event] will cancel the click_event, where click_event is the return value of another components .click method. Functions that have not yet run (or generators that are iterating) will be cancelled, but functions that are currently running will be allowed to finish.
            every: continously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.
            trigger_mode: if "once" (default for all events except `.change()`) would not allow any submissions while an event is pending. If set to "multiple", unlimited submissions are allowed while pending, and "always_last" (default for `.change()` and `.key_up()` events) would allow a second submission after the pending event is complete.
            js: optional frontend js method to run before running 'fn'. Input arguments for js method are values of 'inputs' and 'outputs', return should be a list of values for output components.
            concurrency_limit: if set, this is the maximum number of this event that can be running simultaneously. Can be set to None to mean no concurrency_limit (any number of this event can be running simultaneously). Set to "default" to use the default concurrency limit (defined by the `default_concurrency_limit` parameter in `Blocks.queue()`, which itself is 1 by default).
            concurrency_id: if set, this is the id of the concurrency group. Events with the same concurrency_id will be limited by the lowest set concurrency_limit.
            show_api: whether to show this event in the "view API" page of the Gradio app, or in the ".view_api()" method of the Gradio clients. Unlike setting api_name to False, setting show_api to False will still allow downstream apps as well as the Clients to use this event. If fn is None, show_api will automatically be set to False.
            key: A unique key for this event listener to be used in @gr.render(). If set, this value identifies an event as identical across re-renders when the key is identical.
        
        """
        ...
    
    def input(self,
        fn: Callable[..., Any] | None = None,
        inputs: Block | Sequence[Block] | set[Block] | None = None,
        outputs: Block | Sequence[Block] | None = None,
        api_name: str | None | Literal[False] = None,
        scroll_to_output: bool = False,
        show_progress: Literal["full", "minimal", "hidden"] = "full",
        show_progress_on: Component | Sequence[Component] | None = None,
        queue: bool | None = None,
        batch: bool = False,
        max_batch_size: int = 4,
        preprocess: bool = True,
        postprocess: bool = True,
        cancels: dict[str, Any] | list[dict[str, Any]] | None = None,
        every: Timer | float | None = None,
        trigger_mode: Literal["once", "multiple", "always_last"] | None = None,
        js: str | Literal[True] | None = None,
        concurrency_limit: int | None | Literal["default"] = "default",
        concurrency_id: str | None = None,
        show_api: bool = True,
        key: int | str | tuple[int | str, ...] | None = None,
    
        ) -> Dependency:
        """
        Parameters:
            fn: the function to call when this event is triggered. Often a machine learning model's prediction function. Each parameter of the function corresponds to one input component, and the function should return a single value or a tuple of values, with each element in the tuple corresponding to one output component.
            inputs: list of gradio.components to use as inputs. If the function takes no inputs, this should be an empty list.
            outputs: list of gradio.components to use as outputs. If the function returns no outputs, this should be an empty list.
            api_name: defines how the endpoint appears in the API docs. Can be a string, None, or False. If False, the endpoint will not be exposed in the api docs. If set to None, will use the functions name as the endpoint route. If set to a string, the endpoint will be exposed in the api docs with the given name.
            scroll_to_output: if True, will scroll to output component on completion
            show_progress: how to show the progress animation while event is running: "full" shows a spinner which covers the output component area as well as a runtime display in the upper right corner, "minimal" only shows the runtime display, "hidden" shows no progress animation at all
            show_progress_on: Component or list of components to show the progress animation on. If None, will show the progress animation on all of the output components.
            queue: if True, will place the request on the queue, if the queue has been enabled. If False, will not put this event on the queue, even if the queue has been enabled. If None, will use the queue setting of the gradio app.
            batch: if True, then the function should process a batch of inputs, meaning that it should accept a list of input values for each parameter. The lists should be of equal length (and be up to length `max_batch_size`). The function is then *required* to return a tuple of lists (even if there is only 1 output component), with each list in the tuple corresponding to one output component.
            max_batch_size: maximum number of inputs to batch together if this is called from the queue (only relevant if batch=True)
            preprocess: if False, will not run preprocessing of component data before running 'fn' (e.g. leaving it as a base64 string if this method is called with the `Image` component).
            postprocess: if False, will not run postprocessing of component data before returning 'fn' output to the browser.
            cancels: a list of other events to cancel when this listener is triggered. For example, setting cancels=[click_event] will cancel the click_event, where click_event is the return value of another components .click method. Functions that have not yet run (or generators that are iterating) will be cancelled, but functions that are currently running will be allowed to finish.
            every: continously calls `value` to recalculate it if `value` is a function (has no effect otherwise). Can provide a Timer whose tick resets `value`, or a float that provides the regular interval for the reset Timer.
            trigger_mode: if "once" (default for all events except `.change()`) would not allow any submissions while an event is pending. If set to "multiple", unlimited submissions are allowed while pending, and "always_last" (default for `.change()` and `.key_up()` events) would allow a second submission after the pending event is complete.
            js: optional frontend js method to run before running 'fn'. Input arguments for js method are values of 'inputs' and 'outputs', return should be a list of values for output components.
            concurrency_limit: if set, this is the maximum number of this event that can be running simultaneously. Can be set to None to mean no concurrency_limit (any number of this event can be running simultaneously). Set to "default" to use the default concurrency limit (defined by the `default_concurrency_limit` parameter in `Blocks.queue()`, which itself is 1 by default).
            concurrency_id: if set, this is the id of the concurrency group. Events with the same concurrency_id will be limited by the lowest set concurrency_limit.
            show_api: whether to show this event in the "view API" page of the Gradio app, or in the ".view_api()" method of the Gradio clients. Unlike setting api_name to False, setting show_api to False will still allow downstream apps as well as the Clients to use this event. If fn is None, show_api will automatically be set to False.
            key: A unique key for this event listener to be used in @gr.render(). If set, this value identifies an event as identical across re-renders when the key is identical.
        
        """
        ...
