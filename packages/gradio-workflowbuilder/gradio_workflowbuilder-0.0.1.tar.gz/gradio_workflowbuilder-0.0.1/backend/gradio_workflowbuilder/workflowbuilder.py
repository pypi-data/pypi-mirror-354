from __future__ import annotations
from typing import Any, Dict, List, Optional, Union, Callable
import json
from gradio.components import Component
from gradio.events import Events


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


# Utility functions for workflow analysis and execution
class WorkflowAnalyzer:
    """
    Analyze workflow configurations and provide insights
    """
    
    @staticmethod
    def analyze_workflow(workflow: Dict[str, Any]) -> Dict[str, Any]:
        """
        Provide detailed analysis of a workflow
        """
        nodes = workflow.get("nodes", [])
        edges = workflow.get("edges", [])
        
        # Count node types
        node_types = {}
        for node in nodes:
            node_type = node.get("type", "unknown")
            node_types[node_type] = node_types.get(node_type, 0) + 1
        
        # Analyze workflow complexity
        complexity = "Simple"
        if len(nodes) > 10:
            complexity = "Complex"
        elif len(nodes) > 5:
            complexity = "Medium"
        
        # Check for potential issues
        issues = []
        
        # Check for disconnected nodes
        connected_nodes = set()
        for edge in edges:
            connected_nodes.add(edge["source"])
            connected_nodes.add(edge["target"])
        
        disconnected = [node["id"] for node in nodes if node["id"] not in connected_nodes]
        if disconnected:
            issues.append(f"Disconnected nodes: {', '.join(disconnected)}")
        
        # Check for missing required fields and API keys
        for node in nodes:
            node_type = node.get("type")
            data = node.get("data", {})
            
            # Check for required API keys
            if node_type == "OpenAIModel" and not data.get("template", {}).get("api_key", {}).get("value"):
                issues.append(f"Node {node['id']} missing OpenAI API key")
            elif node_type == "ChatModel" and not data.get("template", {}).get("api_key", {}).get("value"):
                issues.append(f"Node {node['id']} missing API key")
            elif node_type == "NebiusImage" and not data.get("template", {}).get("api_key", {}).get("value"):
                issues.append(f"Node {node['id']} missing Nebius API key")
            
            # Check for required model configurations
            if node_type in ["OpenAIModel", "ChatModel", "HFTextGeneration"] and not data.get("template", {}).get("model", {}).get("value"):
                issues.append(f"Node {node['id']} missing model configuration")
            
            # Check for required templates
            if node_type in ["Prompt", "ChatInput", "ChatOutput"] and not data.get("template"):
                issues.append(f"Node {node['id']} missing template configuration")
        
        # Analyze node categories
        input_nodes = [n for n in nodes if n.get("type") in ["ChatInput", "Input"]]
        processing_nodes = [n for n in nodes if n.get("type") in [
            "OpenAIModel", "ChatModel", "Prompt", "HFTextGeneration",
            "ExecutePython", "ConditionalLogic", "Wait", "APIRequest",
            "WebSearch", "KnowledgeBase", "RAGQuery"
        ]]
        output_nodes = [n for n in nodes if n.get("type") in ["ChatOutput", "Output"]]
        ai_nodes = [n for n in nodes if n.get("type") in [
            "OpenAIModel", "ChatModel", "HFTextGeneration", "HFImageGeneration",
            "NebiusImage", "HFSpeechToText", "HFTextToSpeech", "HFVisionModel"
        ]]
        
        return {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "node_types": node_types,
            "complexity": complexity,
            "issues": issues,
            "is_valid": len(issues) == 0,
            "categories": {
                "input_nodes": len(input_nodes),
                "processing_nodes": len(processing_nodes),
                "output_nodes": len(output_nodes),
                "ai_nodes": len(ai_nodes)
            }
        }
    
    @staticmethod
    def validate_for_execution(workflow: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate if workflow is ready for execution
        """
        analysis = WorkflowAnalyzer.analyze_workflow(workflow)
        
        # Additional execution-specific checks
        nodes = workflow.get("nodes", [])
        
        # Check for entry points (input nodes)
        input_types = {"ChatInput", "Input"}
        inputs = [n for n in nodes if n.get("type") in input_types]
        
        if not inputs:
            analysis["issues"].append("No input nodes found - workflow needs an entry point")
        
        # Check for output nodes
        output_types = {"ChatOutput", "Output"}
        outputs = [n for n in nodes if n.get("type") in output_types]
        
        if not outputs:
            analysis["issues"].append("No output nodes found - workflow needs an exit point")
        
        # Check for required environment variables
        env_vars = set()
        for node in nodes:
            data = node.get("data", {})
            template = data.get("template", {})
            for field in template.values():
                if isinstance(field, dict) and field.get("type") == "SecretStr":
                    env_var = field.get("env_var")
                    if env_var:
                        env_vars.add(env_var)
        
        if env_vars:
            analysis["required_env_vars"] = list(env_vars)
        
        analysis["is_executable"] = len(analysis["issues"]) == 0
        
        return analysis


# Export the main component
__all__ = ["WorkflowBuilder", "WorkflowAnalyzer"]
