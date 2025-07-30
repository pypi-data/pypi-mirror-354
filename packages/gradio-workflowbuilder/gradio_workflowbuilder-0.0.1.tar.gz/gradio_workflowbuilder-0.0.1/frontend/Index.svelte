<script lang="ts">
	import { createEventDispatcher, onMount } from 'svelte';
	
	export let value: { nodes: any[]; edges: any[] } = { nodes: [], edges: [] };
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export const container = true;
	export const scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export const gradio: any = {};

	const dispatch = createEventDispatcher<{
		change: { nodes: any[]; edges: any[] };
		input: { nodes: any[]; edges: any[] };
	}>();

	// State management
	let canvas: HTMLDivElement;
	let canvasContainer: HTMLDivElement;
	let isDragging = false;
	let isDraggingFromSidebar = false;
	let dragNode: any = null;
	let dragOffset = { x: 0, y: 0 };
	let isConnecting = false;
	let connectionStart: any = null;
	let mousePos = { x: 0, y: 0 };
	let selectedNode: any = null;
	let sidebarCollapsed = false;
	let propertyPanelCollapsed = false;
	
	// Workflow metadata
	let workflowName = "My Workflow";
	let workflowId = "workflow-" + Date.now();
	
	// Zoom and pan state
	let zoomLevel = 0.6;
	let panOffset = { x: 0, y: 0 };
	let isPanning = false;
	let lastPanPoint = { x: 0, y: 0 };

	// Define default workflow
	const defaultWorkflow = {
		workflow_id: "simple-rag-v1",
		workflow_name: "Simple RAG Workflow",
		nodes: [
			{
				id: "Input-1",
				type: "Input",
				position: { x: 30, y: 100 },
        		data: { 
					label: "Input",
					display_name: "User Question",
					template: {
						data_type: {
							display_name: "Data Type",
							type: "options",
							options: ["string", "image", "video", "audio", "file"],
							value: "string"
						},
						value: {
							display_name: "Value or Path",
							type: "string",
							value: "How do I get started with Modal?"
						},
						data: {
							display_name: "Output Data",
							type: "object",
							is_handle: true
						}
					},
					resources: {
						cpu: 0.1,
						memory: "128Mi",
						gpu: "none"
					}
				}
			},
			{
				id: "KnowledgeBase-1",
				type: "KnowledgeBase",
				position: { x: 50, y: 500 },
        		data: { 
					label: "Knowledge Base",
					display_name: "Create Product Docs KB",
					template: {
						kb_name: {
							display_name: "Knowledge Base Name",
							type: "string",
							value: "product-docs-v1"
						},
						source_type: {
							display_name: "Source Type",
							type: "options",
							options: ["Directory", "URL"],
							value: "URL"
						},
						path_or_url: {
							display_name: "Path or URL",
							type: "string",
							value: "https://modal.com/docs/guide"
						},
						knowledge_base: {
							display_name: "Knowledge Base Out",
							type: "object",
							is_handle: true
						}
					},
					resources: {
						cpu: 0.2,
						memory: "256Mi",
						gpu: "none"
					}
				}
			},
			{
				id: "RAGQuery-1",
				type: "RAGQuery",
				position: { x: 400, y: 300 },
        		data: { 
					label: "RAG Query",
					display_name: "Retrieve & Augment Prompt",
					template: {
						query: {
							display_name: "Original Query",
							type: "string",
							is_handle: true
						},
						knowledge_base: {
							display_name: "Knowledge Base",
							type: "object",
							is_handle: true
						},
						rag_prompt: {
							display_name: "Augmented Prompt Out",
							type: "string",
							is_handle: true
						}
					},
					resources: {
						cpu: 0.3,
						memory: "512Mi",
						gpu: "none"
					}
				}
			},
			{
				id: "ChatModel-1",
				type: "ChatModel",
				position: { x: 800, y: 200 },
        		data: { 
					label: "Chat Model",
					display_name: "AI Assistant",
					template: {
						provider: {
							display_name: "Provider",
							type: "options",
							options: ["OpenAI", "Anthropic"],
							value: "OpenAI"
						},
						model: {
							display_name: "Model Name",
							type: "string",
							value: "gpt-4o-mini"
						},
						api_key: {
							display_name: "API Key",
							type: "SecretStr",
							required: true,
							env_var: "OPENAI_API_KEY"
						},
						system_prompt: {
							display_name: "System Prompt (Optional)",
							type: "string",
							value: "You are a helpful assistant that answers questions based on the provided context."
						},
						prompt: {
							display_name: "Prompt",
							type: "string",
							is_handle: true
						},
						response: {
							display_name: "Response",
							type: "string",
							is_handle: true
						}
					},
					resources: {
						cpu: 0.5,
						memory: "512Mi",
						gpu: "none"
					}
				}
			},
			{
				id: "Output-1",
				type: "Output",
				position: { x: 1000, y: 600 },
        		data: { 
					label: "Output",
					display_name: "Final Result",
					template: {
						input_data: {
							display_name: "Input Data",
							type: "object",
							is_handle: true
						}
					},
					resources: {
						cpu: 0.1,
						memory: "128Mi",
						gpu: "none"
					}
				}
			}
		],
		edges: [
			{
				id: "e1-3",
				source: "Input-1",
				source_handle: "data",
				target: "RAGQuery-1",
				target_handle: "query"
			},
			{
				id: "e2-3",
				source: "KnowledgeBase-1",
				source_handle: "knowledge_base",
				target: "RAGQuery-1",
				target_handle: "knowledge_base"
			},
			{
				id: "e3-4",
				source: "RAGQuery-1",
				source_handle: "rag_prompt",
				target: "ChatModel-1",
				target_handle: "prompt"
			},
			{
				id: "e4-5",
				source: "ChatModel-1",
				source_handle: "response",
				target: "Output-1",
				target_handle: "input_data"
			}
		]
	};

	// Initialize nodes and edges
	let nodes = value?.nodes?.length > 0 ? [...value.nodes] : defaultWorkflow.nodes;
	let edges = value?.edges?.length > 0 ? [...value.edges] : defaultWorkflow.edges;

	// Initialize workflow metadata
	if (value?.workflow_name) {
		workflowName = value.workflow_name;
	}
	if (value?.workflow_id) {
		workflowId = value.workflow_id;
	}

	// Update value if empty
	$: if (!value || !value.nodes || value.nodes.length === 0) {
		value = defaultWorkflow;
	}

	// Component categories with new node types
	const componentCategories = {
		'Input/Output': {
			icon: '📥',
			components: {
				ChatInput: {
					label: 'Chat Input',
					icon: '💬',
					color: '#4CAF50',
					defaultData: { 
						display_name: 'Chat Input',
						template: {
							input_value: {
								display_name: 'User Message',
								type: 'string',
								value: '',
								is_handle: true
							}
						},
						resources: {
							cpu: 0.1,
							memory: '128Mi',
							gpu: 'none'
						}
					}
				},
				ChatOutput: {
					label: 'Chat Output',
					icon: '💭',
					color: '#F44336',
					defaultData: { 
						display_name: 'Chat Output',
						template: {
							response: {
								display_name: 'AI Response',
								type: 'string',
								is_handle: true
							}
						},
						resources: {
							cpu: 0.1,
							memory: '128Mi',
							gpu: 'none'
						}
					}
				},
				Input: {
					label: 'Input',
					icon: '📥',
					color: '#2196F3',
					defaultData: { 
						display_name: 'Source Data',
						template: {
							data_type: {
								display_name: 'Data Type',
								type: 'options',
								options: ['string', 'image', 'video', 'audio', 'file'],
								value: 'string'
							},
							value: {
								display_name: 'Value or Path',
								type: 'string',
								value: 'This is the initial text.'
							},
							data: {
								display_name: 'Output Data',
								type: 'object',
								is_handle: true
							}
						},
						resources: {
							cpu: 0.1,
							memory: '128Mi',
							gpu: 'none'
						}
					}
				},
				Output: {
					label: 'Output',
					icon: '📤',
					color: '#FF9800',
					defaultData: { 
						display_name: 'Final Result',
						template: {
							input_data: {
								display_name: 'Input Data',
								type: 'object',
								is_handle: true
							}
						},
						resources: {
							cpu: 0.1,
							memory: '128Mi',
							gpu: 'none'
						}
					}
				}
			}
		},
		'AI & Language': {
			icon: '🤖',
			components: {
				OpenAIModel: {
					label: 'OpenAI Model',
					icon: '🎯',
					color: '#9C27B0',
					defaultData: { 
						display_name: 'OpenAI Model',
						template: {
							model: { 
								display_name: 'Model',
								type: 'options', 
								value: 'gpt-4', 
								options: ['gpt-4o', 'gpt-4o-mini', 'gpt-3.5-turbo']
							},
							temperature: { 
								display_name: 'Temperature',
								type: 'number', 
								value: 0.7, 
								min: 0, 
								max: 1 
							},
							max_tokens: { 
								display_name: 'Max Tokens',
								type: 'number', 
								value: 2048, 
								min: 1, 
								max: 4096 
							},
							api_key: { 
								display_name: 'API Key',
								type: 'SecretStr', 
								value: '', 
								env_var: 'OPENAI_API_KEY' 
							},
							prompt: {
								display_name: 'Prompt',
								type: 'string',
								is_handle: true
							},
							response: {
								display_name: 'Response',
								type: 'string',
								is_handle: true
							}
						},
						resources: {
							cpu: 0.5,
							memory: '512Mi',
							gpu: 'none'
						}
					}
				},
				ChatModel: {
					label: 'Chat Model',
					icon: '💭',
					color: '#673AB7',
					defaultData: { 
						display_name: 'Chat Model',
						template: {
							provider: {
								display_name: 'Provider',
								type: 'options',
								options: ['OpenAI', 'Anthropic'],
								value: 'OpenAI'
							},
							model: {
								display_name: 'Model',
								type: 'string',
								value: 'gpt-4o-mini'
							},
							api_key: {
								display_name: 'API Key',
								type: 'SecretStr',
								required: true,
								env_var: 'OPENAI_API_KEY'
							},
							system_prompt: {
								display_name: 'System Prompt',
								type: 'string',
								value: 'You are a helpful assistant.'
							},
							prompt: {
								display_name: 'Prompt',
								type: 'string',
								is_handle: true
							},
							response: {
								display_name: 'Response',
								type: 'string',
								is_handle: true
							}
						},
						resources: {
							cpu: 0.5,
							memory: '512Mi',
							gpu: 'none'
						}
					}
				},
				Prompt: {
					label: 'Prompt',
					icon: '📝',
					color: '#3F51B5',
					defaultData: { 
						display_name: 'Prompt',
						template: {
							prompt_template: { 
								display_name: 'Template',
								type: 'string', 
								value: '{{input}}',
								is_handle: true
							}
						},
						resources: {
							cpu: 0.1,
							memory: '128Mi',
							gpu: 'none'
						}
					}
				},
				HFTextGeneration: {
					label: 'HF Text Generation',
					icon: '🤗',
					color: '#E91E63',
					defaultData: { 
						display_name: 'HF Text Generation',
						template: {
							model: { 
								display_name: 'Model',
								type: 'string', 
								value: 'gpt2' 
							},
							temperature: { 
								display_name: 'Temperature',
								type: 'number', 
								value: 0.7, 
								min: 0, 
								max: 1 
							},
							max_tokens: { 
								display_name: 'Max Tokens',
								type: 'number', 
								value: 2048, 
								min: 1, 
								max: 4096 
							},
							api_key: { 
								display_name: 'API Key',
								type: 'SecretStr', 
								value: '', 
								env_var: 'HF_API_KEY' 
							},
							prompt: {
								display_name: 'Prompt',
								type: 'string',
								is_handle: true
							},
							response: {
								display_name: 'Response',
								type: 'string',
								is_handle: true
							}
						},
						resources: {
							cpu: 0.3,
							memory: '256Mi',
							gpu: 'none'
						}
					}
				},
				ReActAgent: {
					label: 'ReAct Agent',
					icon: '🤖',
					color: '#9C27B0',
					defaultData: { 
						display_name: 'LlamaIndex ReAct Agent',
						template: {
							tools_input: {
								display_name: 'Available Tools',
								type: 'list',
								is_handle: true,
								info: 'Connect WebSearch, ExecutePython, APIRequest, and other tool nodes'
							},
							llm_model: {
								display_name: 'LLM Model',
								type: 'options',
								options: ['gpt-4o', 'gpt-4o-mini', 'gpt-3.5-turbo', 'gpt-4', 'gpt-3.5-turbo-16k'],
								value: 'gpt-4o-mini'
							},
							api_key: {
								display_name: 'OpenAI API Key',
								type: 'SecretStr',
								required: true,
								env_var: 'OPENAI_API_KEY'
							},
							system_prompt: {
								display_name: 'System Prompt',
								type: 'string',
								value: 'You are a helpful AI assistant with access to various tools. Use the available tools to answer user questions accurately and efficiently.',
								multiline: true
							},
							user_query: {
								display_name: 'User Query',
								type: 'string',
								is_handle: true
							},
							max_iterations: {
								display_name: 'Max Iterations',
								type: 'number',
								value: 8
							},
							temperature: {
								display_name: 'Temperature',
								type: 'number',
								value: 0.1,
								min: 0,
								max: 2,
								step: 0.1
							},
							verbose: {
								display_name: 'Verbose Output',
								type: 'boolean',
								value: true
							},
							agent_response: {
								display_name: 'Agent Response',
								type: 'string',
								is_handle: true
							}
						},
						resources: {
							cpu: 0.5,
							memory: '512Mi',
							gpu: 'none'
						}
					}
				}
			}
		},
		'API & Web': {
			icon: '🌐',
			components: {
				APIRequest: {
					label: 'API Request',
					icon: '🔌',
					color: '#00BCD4',
					defaultData: { 
						display_name: 'API Request',
						template: {
							url: { 
								display_name: 'URL',
								type: 'string', 
								value: '' 
							},
							method: { 
								display_name: 'Method',
								type: 'options', 
								value: 'GET', 
								options: ['GET', 'POST', 'PUT', 'DELETE'] 
							},
							headers: { 
								display_name: 'Headers',
								type: 'dict', 
								value: {} 
							},
							body: { 
								display_name: 'Body',
								type: 'string', 
								value: '' 
							},
							response: {
								display_name: 'Response',
								type: 'object',
								is_handle: true
							}
						},
						resources: {
							cpu: 0.2,
							memory: '256Mi',
							gpu: 'none'
						}
					}
				},
				WebSearch: {
					label: 'Web Search',
					icon: '🔍',
					color: '#009688',
					defaultData: { 
						display_name: 'Web Search',
						template: {
							query: { 
								display_name: 'Query',
								type: 'string', 
								value: '',
								is_handle: true
							},
							num_results: { 
								display_name: 'Number of Results',
								type: 'number', 
								value: 5, 
								min: 1, 
								max: 10 
							},
							api_key: { 
								display_name: 'API Key',
								type: 'SecretStr', 
								value: '', 
								env_var: 'SERPAPI_KEY' 
							},
							results: {
								display_name: 'Search Results',
								type: 'list',
								is_handle: true
							}
						},
						resources: {
							cpu: 0.2,
							memory: '256Mi',
							gpu: 'none'
						}
					}
				}
			}
		},
		'Data Processing': {
			icon: '⚙️',
			components: {
				ExecutePython: {
					label: 'Execute Python',
					icon: '🐍',
					color: '#FF5722',
					defaultData: { 
						display_name: 'Execute Python',
						template: {
							code: { 
								display_name: 'Python Code',
								type: 'string', 
								value: 'def process(input_data):\n    return input_data' 
							},
							timeout: { 
								display_name: 'Timeout',
								type: 'number', 
								value: 30, 
								min: 1, 
								max: 300 
							},
							input_data: {
								display_name: 'Input Data',
								type: 'object',
								is_handle: true
							},
							output_data: {
								display_name: 'Output Data',
								type: 'object',
								is_handle: true
							}
						},
						resources: {
							cpu: 0.3,
							memory: '256Mi',
							gpu: 'none'
						}
					}
				},
				ConditionalLogic: {
					label: 'Conditional Logic',
					icon: '🔀',
					color: '#795548',
					defaultData: { 
						display_name: 'Conditional Logic',
						template: {
							condition: { 
								display_name: 'Condition',
								type: 'string', 
								value: '{{input}} == True' 
							},
							input: {
								display_name: 'Input',
								type: 'object',
								is_handle: true
							},
							true_output: {
								display_name: 'True Output',
								type: 'object',
								is_handle: true
							},
							false_output: {
								display_name: 'False Output',
								type: 'object',
								is_handle: true
							}
						},
						resources: {
							cpu: 0.1,
							memory: '128Mi',
							gpu: 'none'
						}
					}
				},
				Wait: {
					label: 'Wait',
					icon: '⏳',
					color: '#607D8B',
					defaultData: { 
						display_name: 'Wait',
						template: {
							seconds: { 
								display_name: 'Seconds',
								type: 'number', 
								value: 1, 
								min: 1, 
								max: 3600 
							},
							input: {
								display_name: 'Input',
								type: 'object',
								is_handle: true
							},
							output: {
								display_name: 'Output',
								type: 'object',
								is_handle: true
							}
						},
						resources: {
							cpu: 0.1,
							memory: '128Mi',
							gpu: 'none'
						}
					}
				}
			}
		},
		'RAG & Knowledge': {
			icon: '📚',
			components: {
				KnowledgeBase: {
					label: 'Knowledge Base',
					icon: '📖',
					color: '#8BC34A',
					defaultData: { 
						display_name: 'Knowledge Base',
						template: {
							kb_name: {
								display_name: 'Knowledge Base Name',
								type: 'string',
								value: ''
							},
							source_type: {
								display_name: 'Source Type',
								type: 'options',
								options: ['Directory', 'URL'],
								value: 'Directory'
							},
							path_or_url: {
								display_name: 'Path or URL',
								type: 'string',
								value: ''
							},
							knowledge_base: {
								display_name: 'Knowledge Base',
								type: 'object',
								is_handle: true
							}
						},
						resources: {
							cpu: 0.2,
							memory: '512Mi',
							gpu: 'none'
						}
					}
				},
				RAGQuery: {
					label: 'RAG Query',
					icon: '🔎',
					color: '#FFC107',
					defaultData: { 
						display_name: 'RAG Query',
						template: {
							query: {
								display_name: 'Query',
								type: 'string',
								is_handle: true
							},
							knowledge_base: {
								display_name: 'Knowledge Base',
								type: 'object',
								is_handle: true
							},
							num_results: { 
								display_name: 'Number of Results',
								type: 'number', 
								value: 3, 
								min: 1, 
								max: 10 
							},
							rag_prompt: {
								display_name: 'RAG Prompt',
								type: 'string',
								is_handle: true
							}
						},
						resources: {
							cpu: 0.3,
							memory: '512Mi',
							gpu: 'none'
						}
					}
				}
			}
		},
		'Speech & Vision': {
			icon: '👁️',
			components: {
				HFSpeechToText: {
					label: 'HF Speech to Text',
					icon: '🎤',
					color: '#9E9E9E',
					defaultData: { 
						display_name: 'HF Speech to Text',
						template: {
							model: { 
								display_name: 'Model',
								type: 'string', 
								value: 'facebook/wav2vec2-base-960h' 
							},
							api_key: { 
								display_name: 'API Key',
								type: 'SecretStr', 
								value: '', 
								env_var: 'HF_API_KEY' 
							},
							audio_input: {
								display_name: 'Audio Input',
								type: 'file',
								is_handle: true
							},
							text_output: {
								display_name: 'Text Output',
								type: 'string',
								is_handle: true
							}
						},
						resources: {
							cpu: 0.4,
							memory: '512Mi',
							gpu: 'optional'
						}
					}
				},
				HFTextToSpeech: {
					label: 'HF Text to Speech',
					icon: '🔊',
					color: '#CDDC39',
					defaultData: { 
						display_name: 'HF Text to Speech',
						template: {
							model: { 
								display_name: 'Model',
								type: 'string', 
								value: 'facebook/fastspeech2-en-ljspeech' 
							},
							api_key: { 
								display_name: 'API Key',
								type: 'SecretStr', 
								value: '', 
								env_var: 'HF_API_KEY' 
							},
							text_input: {
								display_name: 'Text Input',
								type: 'string',
								is_handle: true
							},
							audio_output: {
								display_name: 'Audio Output',
								type: 'file',
								is_handle: true
							}
						},
						resources: {
							cpu: 0.4,
							memory: '512Mi',
							gpu: 'optional'
						}
					}
				},
				HFSVisionModel: {
					label: 'HF Vision Model',
					icon: '👁️',
					color: '#FF9800',
					defaultData: { 
						display_name: 'HF Vision Model',
						template: {
							model: { 
								display_name: 'Model',
								type: 'string', 
								value: 'google/vit-base-patch16-224' 
							},
							api_key: { 
								display_name: 'API Key',
								type: 'SecretStr', 
								value: '', 
								env_var: 'HF_API_KEY' 
							},
							image_input: {
								display_name: 'Image Input',
								type: 'file',
								is_handle: true
							},
							prediction: {
								display_name: 'Prediction',
								type: 'object',
								is_handle: true
							}
						},
						resources: {
							cpu: 0.4,
							memory: '512Mi',
							gpu: 'required'
						}
					}
				}
			}
		},
		'Image Generation': {
			icon: '🎨',
			components: {
				HFImageGeneration: {
					label: 'HF Image Generation',
					icon: '🎨',
					color: '#E91E63',
					defaultData: { 
						display_name: 'HF Image Generation',
						template: {
							model: { 
								display_name: 'Model',
								type: 'string', 
								value: 'stabilityai/stable-diffusion-2' 
							},
							prompt: { 
								display_name: 'Prompt',
								type: 'string', 
								value: '',
								is_handle: true
							},
							num_images: { 
								display_name: 'Number of Images',
								type: 'number', 
								value: 1, 
								min: 1, 
								max: 4 
							},
							api_key: { 
								display_name: 'API Key',
								type: 'SecretStr', 
								value: '', 
								env_var: 'HF_API_KEY' 
							},
							images: {
								display_name: 'Generated Images',
								type: 'list',
								is_handle: true
							}
						},
						resources: {
							cpu: 0.5,
							memory: '1Gi',
							gpu: 'required'
						}
					}
				},
				NebiusImage: {
					label: 'Nebius Image',
					icon: '🖼️',
					color: '#2196F3',
					defaultData: { 
						display_name: 'Nebius Image',
						template: {
							model: {
								display_name: 'Model',
								type: 'options',
								options: ['black-forest-labs/flux-dev', 'black-forest-labs/flux-schnell', 'stability-ai/sdxl'],
								value: 'black-forest-labs/flux-dev'
							},
							prompt: { 
								display_name: 'Prompt',
								type: 'string', 
								value: '',
								is_handle: true
							},
							negative_prompt: {
								display_name: 'Negative Prompt',
								type: 'string',
								value: ''
							},
							width: {
								display_name: 'Width',
								type: 'number',
								value: 1024
							},
							height: {
								display_name: 'Height',
								type: 'number',
								value: 1024
							},
							num_inference_steps: {
								display_name: 'Inference Steps',
								type: 'number',
								value: 28
							},
							seed: {
								display_name: 'Seed',
								type: 'number',
								value: -1
							},
							api_key: { 
								display_name: 'API Key',
								type: 'SecretStr', 
								value: '', 
								env_var: 'NEBIUS_API_KEY' 
							},
							image: {
								display_name: 'Generated Image',
								type: 'file',
								is_handle: true
							}
						},
						resources: {
							cpu: 0.5,
							memory: '1Gi',
							gpu: 'required'
						}
					}
				}
			}
		},
		'MCP Integration': {
			icon: '🤝',
			components: {
				MCPConnection: {
					label: 'MCP Connection',
					icon: '🔌',
					color: '#673AB7',
					defaultData: { 
						display_name: 'MCP Connection',
						template: {
							server_url: {
								display_name: 'Server URL',
								type: 'string',
								value: ''
							},
							connection_type: {
								display_name: 'Connection Type',
								type: 'options',
								options: ['http', 'stdio'],
								value: 'http'
							},
							allowed_tools: {
								display_name: 'Allowed Tools',
								type: 'string',
								value: ''
							},
							api_key: { 
								display_name: 'API Key',
								type: 'SecretStr', 
								value: '', 
								env_var: 'MCP_API_KEY' 
							},
							connection: {
								display_name: 'MCP Connection',
								type: 'object',
								is_handle: true
							}
						},
						resources: {
							cpu: 0.2,
							memory: '256Mi',
							gpu: 'none'
						}
					}
				},
				MCPAgent: {
					label: 'MCP Agent',
					icon: '🤖',
					color: '#3F51B5',
					defaultData: { 
						display_name: 'MCP Agent',
						template: {
							llm_model: {
								display_name: 'LLM Model',
								type: 'options',
								options: ['gpt-4o', 'gpt-4o-mini', 'gpt-3.5-turbo', 'gpt-4', 'gpt-3.5-turbo-16k'],
								value: 'gpt-4o'
							},
							api_key: {
								display_name: 'OpenAI API Key',
								type: 'SecretStr',
								required: true,
								env_var: 'OPENAI_API_KEY'
							},
							system_prompt: {
								display_name: 'System Prompt',
								type: 'string',
								value: 'You are a helpful AI assistant.',
								multiline: true
							},
							max_iterations: {
								display_name: 'Max Iterations',
								type: 'number',
								value: 10,
								min: 1,
								max: 20
							},
							temperature: {
								display_name: 'Temperature',
								type: 'number',
								value: 0.1,
								min: 0,
								max: 2,
								step: 0.1
							},
							verbose: {
								display_name: 'Verbose Output',
								type: 'boolean',
								value: false
							},
							user_query: {
								display_name: 'User Query',
								type: 'string',
								is_handle: true
							},
							mcp_connection: {
								display_name: 'MCP Connection',
								type: 'object',
								is_handle: true
							},
							agent_response: {
								display_name: 'Agent Response',
								type: 'string',
								is_handle: true
							}
						},
						resources: {
							cpu: 0.5,
							memory: '512Mi',
							gpu: 'none'
						}
					}
				}
			}
		}
	};

	// Property fields for each node type
	const propertyFields = {
		// Input/Output nodes
		ChatInput: [
			{ key: 'display_name', label: 'Display Name', type: 'text', help: 'Name shown in the workflow' },
			{ key: 'template.input_value.display_name', label: 'Input Field Label', type: 'text', help: 'Label shown in the chat input field' },
			{ key: 'template.input_value.value', label: 'Default Message', type: 'textarea', help: 'Default message shown in the input field' }
		],
		ChatOutput: [
			{ key: 'display_name', label: 'Display Name', type: 'text', help: 'Name shown in the workflow' },
			{ key: 'template.response.display_name', label: 'Response Field Label', type: 'text', help: 'Label shown in the chat output field' }
		],
		Input: [
			{ key: 'display_name', label: 'Display Name', type: 'text', help: 'Name shown in the workflow' },
			{ key: 'template.data_type.value', label: 'Data Type', type: 'select', options: ['string', 'image', 'video', 'audio', 'file'], help: 'Type of data this node will handle' },
			{ key: 'template.value.value', label: 'Default Value', type: 'textarea', help: 'Default value or path' }
		],
		Output: [
			{ key: 'display_name', label: 'Display Name', type: 'text', help: 'Name shown in the workflow' }
		],

		// AI & Language nodes
		OpenAIModel: [
			{ key: 'display_name', label: 'Display Name', type: 'text', help: 'Name shown in the workflow' },
			{ key: 'template.model.value', label: 'Model', type: 'select', options: ['gpt-4o', 'gpt-4o-mini', 'gpt-3.5-turbo'] },
			{ key: 'template.temperature.value', label: 'Temperature', type: 'number', min: 0, max: 1, step: 0.1 },
			{ key: 'template.max_tokens.value', label: 'Max Tokens', type: 'number', min: 1, max: 4096 }
		],
		ChatModel: [
			{ key: 'display_name', label: 'Display Name', type: 'text', help: 'Name shown in the workflow' },
			{ key: 'template.provider.value', label: 'Provider', type: 'select', options: ['OpenAI', 'Anthropic'], help: 'AI model provider' },
			{ key: 'template.model.value', label: 'Model', type: 'text', help: 'Model name' },
			{ key: 'template.system_prompt.value', label: 'System Prompt', type: 'textarea', help: 'Optional system prompt' }
		],
		Prompt: [
			{ key: 'display_name', label: 'Display Name', type: 'text', help: 'Name shown in the workflow' },
			{ key: 'template.prompt_template.value', label: 'Prompt Template', type: 'textarea', help: 'Prompt template' }
		],
		HFTextGeneration: [
			{ key: 'display_name', label: 'Display Name', type: 'text', help: 'Name shown in the workflow' },
			{ key: 'template.model.value', label: 'Model', type: 'text', help: 'Model name' },
			{ key: 'template.temperature.value', label: 'Temperature', type: 'number', min: 0, max: 1, step: 0.1, help: 'Model temperature' },
			{ key: 'template.max_tokens.value', label: 'Max Tokens', type: 'number', min: 1, max: 4096, help: 'Maximum tokens' }
		],
		ReActAgent: [
			{ key: 'display_name', label: 'Display Name', type: 'text', help: 'Name shown in the workflow' },
			{ key: 'template.llm_model.value', label: 'LLM Model', type: 'select', options: ['gpt-4o', 'gpt-4o-mini', 'gpt-3.5-turbo', 'gpt-4', 'gpt-3.5-turbo-16k'], help: 'Model to use for the agent' },
			{ key: 'template.system_prompt.value', label: 'System Prompt', type: 'textarea', help: 'System prompt for the agent', multiline: true },
			{ key: 'template.max_iterations.value', label: 'Max Iterations', type: 'number', min: 1, max: 20, help: 'Maximum number of agent iterations' },
			{ key: 'template.temperature.value', label: 'Temperature', type: 'number', min: 0, max: 2, step: 0.1, help: 'Model temperature (0-2)' },
			{ key: 'template.verbose.value', label: 'Verbose Output', type: 'checkbox', help: 'Show detailed agent reasoning' }
		],

		// API & Web nodes
		APIRequest: [
			{ key: 'display_name', label: 'Display Name', type: 'text', help: 'Name shown in the workflow' },
			{ key: 'template.url.value', label: 'URL', type: 'text', help: 'API endpoint URL' },
			{ key: 'template.method.value', label: 'Method', type: 'select', options: ['GET', 'POST', 'PUT', 'DELETE'], help: 'HTTP method' }
		],
		WebSearch: [
			{ key: 'display_name', label: 'Display Name', type: 'text', help: 'Name shown in the workflow' },
			{ key: 'template.num_results.value', label: 'Number of Results', type: 'number', help: 'Number of search results' }
		],

		// Data Processing nodes
		ExecutePython: [
			{ key: 'display_name', label: 'Display Name', type: 'text', help: 'Name shown in the workflow' },
			{ key: 'template.code.value', label: 'Python Code', type: 'textarea', help: 'Python code to execute' },
			{ key: 'template.timeout.value', label: 'Timeout', type: 'number', help: 'Execution timeout' }
		],
		ConditionalLogic: [
			{ key: 'display_name', label: 'Display Name', type: 'text', help: 'Name shown in the workflow' },
			{ key: 'template.condition.value', label: 'Condition', type: 'text', help: 'Condition expression' }
		],
		Wait: [
			{ key: 'display_name', label: 'Display Name', type: 'text', help: 'Name shown in the workflow' },
			{ key: 'template.seconds.value', label: 'Seconds', type: 'number', help: 'Wait time in seconds' }
		],

		// RAG nodes
		KnowledgeBase: [
			{ key: 'display_name', label: 'Display Name', type: 'text', help: 'Name shown in the workflow' },
			{ key: 'template.kb_name.value', label: 'Knowledge Base Name', type: 'text', help: 'Name for the knowledge base' },
			{ key: 'template.source_type.value', label: 'Source Type', type: 'select', options: ['Directory', 'URL'], help: 'Type of source' },
			{ key: 'template.path_or_url.value', label: 'Path or URL', type: 'text', help: 'Source location' }
		],
		RAGQuery: [
			{ key: 'display_name', label: 'Display Name', type: 'text', help: 'Name shown in the workflow' },
			{ key: 'template.num_results.value', label: 'Number of Results', type: 'number', help: 'Number of results to retrieve' }
		],

		// Speech & Vision nodes
		HFSpeechToText: [
			{ key: 'display_name', label: 'Display Name', type: 'text', help: 'Name shown in the workflow' },
			{ key: 'template.model.value', label: 'Model', type: 'text', help: 'HuggingFace model ID' }
		],
		HFTextToSpeech: [
			{ key: 'display_name', label: 'Display Name', type: 'text', help: 'Name shown in the workflow' },
			{ key: 'template.model.value', label: 'Model', type: 'text', help: 'HuggingFace model ID' }
		],
		HFSVisionModel: [
			{ key: 'display_name', label: 'Display Name', type: 'text', help: 'Name shown in the workflow' },
			{ key: 'template.model.value', label: 'Model', type: 'text', help: 'HuggingFace model ID' }
		],

		// Image Generation nodes
		HFImageGeneration: [
			{ key: 'display_name', label: 'Display Name', type: 'text', help: 'Name shown in the workflow' },
			{ key: 'template.model.value', label: 'Model', type: 'text', help: 'HuggingFace model ID' },
			{ key: 'template.num_images.value', label: 'Number of Images', type: 'number', help: 'Number of images to generate' }
		],
		NebiusImage: [
			{ key: 'display_name', label: 'Display Name', type: 'text', help: 'Name shown in the workflow' },
			{ key: 'template.model.value', label: 'Model', type: 'select', options: ['black-forest-labs/flux-dev', 'black-forest-labs/flux-schnell', 'stability-ai/sdxl'], help: 'Nebius model to use' },
			{ key: 'template.width.value', label: 'Width', type: 'number', help: 'Image width' },
			{ key: 'template.height.value', label: 'Height', type: 'number', help: 'Image height' },
			{ key: 'template.num_inference_steps.value', label: 'Inference Steps', type: 'number', help: 'Number of inference steps' },
			{ key: 'template.seed.value', label: 'Seed', type: 'number', help: 'Random seed (-1 for random)' }
		],

		// MCP nodes
		MCPConnection: [
			{ key: 'display_name', label: 'Display Name', type: 'text', help: 'Name shown in the workflow' },
			{ key: 'template.server_url.value', label: 'Server URL', type: 'text', help: 'MCP server URL' },
			{ key: 'template.connection_type.value', label: 'Connection Type', type: 'select', options: ['http', 'stdio'], help: 'Connection type' },
			{ key: 'template.allowed_tools.value', label: 'Allowed Tools', type: 'text', help: 'Optional list of allowed tools' }
		],
		MCPAgent: [
			{ key: 'display_name', label: 'Display Name', type: 'text', help: 'Name shown in the workflow' },
			{ key: 'template.llm_model.value', label: 'LLM Model', type: 'select', options: ['gpt-4o', 'gpt-4o-mini', 'gpt-3.5-turbo', 'gpt-4', 'gpt-3.5-turbo-16k'], help: 'Model to use for the agent' },
			{ key: 'template.system_prompt.value', label: 'System Prompt', type: 'textarea', help: 'System prompt for the agent', multiline: true },
			{ key: 'template.max_iterations.value', label: 'Max Iterations', type: 'number', min: 1, max: 20, help: 'Maximum number of agent iterations' },
			{ key: 'template.temperature.value', label: 'Temperature', type: 'number', min: 0, max: 2, step: 0.1, help: 'Model temperature (0-2)' },
			{ key: 'template.verbose.value', label: 'Verbose Output', type: 'checkbox', help: 'Show detailed agent reasoning' }
		]
	};

	// Update parent component when data changes
	$: {
		const newValue = { nodes, edges };
		if (JSON.stringify(newValue) !== JSON.stringify(value)) {
			value = newValue;
			dispatch('change', newValue);
		}
	}

	// Export workflow to JSON

	// Clear workflow function
function clearWorkflow() {
    nodes = [];
    edges = [];
    selectedNode = null;
    workflowName = "My Workflow";
    workflowId = "workflow-" + Date.now();
}


	function exportWorkflow() {
		const exportData = {
			workflow_id: workflowId,
			workflow_name: workflowName,
			nodes: nodes.map(node => ({
				id: node.id,
				type: node.type,
				data: {
					display_name: node.data.display_name,
					template: node.data.template,
					resources: node.data.resources || {
						cpu: 0.1,
						memory: "128Mi",
						gpu: "none"
					}
				}
			})),
			edges: edges.map(edge => ({
				source: edge.source,
				source_handle: edge.source_handle || 'output',
				target: edge.target,
				target_handle: edge.target_handle || 'input'
			}))
		};

		const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = `${workflowName.replace(/\s+/g, '-').toLowerCase()}.json`;
		document.body.appendChild(a);
		a.click();
		document.body.removeChild(a);
		URL.revokeObjectURL(url);
	}

	// Zoom functions
	function zoomIn() {
		zoomLevel = Math.min(zoomLevel * 1.2, 3);
	}

	function zoomOut() {
		zoomLevel = Math.max(zoomLevel / 1.2, 0.3);
	}

	function resetZoom() {
		zoomLevel = 1;
		panOffset = { x: 0, y: 0 };
	}

	function handleWheel(event: WheelEvent) {
		event.preventDefault();
		if (event.ctrlKey || event.metaKey) {
			const delta = event.deltaY > 0 ? 0.9 : 1.1;
			zoomLevel = Math.max(0.3, Math.min(3, zoomLevel * delta));
		} else {
			panOffset.x -= event.deltaX * 0.5;
			panOffset.y -= event.deltaY * 0.5;
			panOffset = { ...panOffset };
		}
	}

	// Pan functions
	function startPanning(event: MouseEvent) {
		if (event.button === 1 || (event.button === 0 && event.altKey)) {
			isPanning = true;
			lastPanPoint = { x: event.clientX, y: event.clientY };
			event.preventDefault();
		}
	}

	function handlePanning(event: MouseEvent) {
		if (isPanning) {
			const deltaX = event.clientX - lastPanPoint.x;
			const deltaY = event.clientY - lastPanPoint.y;
			panOffset.x += deltaX;
			panOffset.y += deltaY;
			panOffset = { ...panOffset };
			lastPanPoint = { x: event.clientX, y: event.clientY };
		}
	}

	function stopPanning() {
		isPanning = false;
	}

	// Drag and drop from sidebar
	function handleSidebarDragStart(event: DragEvent, componentType: string, componentData: any) {
		if (event.dataTransfer) {
			event.dataTransfer.setData('application/json', JSON.stringify({
				type: componentType,
				data: componentData
			}));
			isDraggingFromSidebar = true;
		}
	}

	function handleCanvasDropFromSidebar(event: DragEvent) {
		event.preventDefault();
		if (!isDraggingFromSidebar) return;
		
		const rect = canvas.getBoundingClientRect();
		const x = (event.clientX - rect.left - panOffset.x) / zoomLevel;
		const y = (event.clientY - rect.top - panOffset.y) / zoomLevel;
		
		try {
			const dropData = JSON.parse(event.dataTransfer?.getData('application/json') || '{}');
			if (dropData.type && dropData.data) {
				const newNode = {
					id: `${dropData.type}-${Date.now()}`,
					type: dropData.type,
					position: { x: Math.max(20, x - 160), y: Math.max(20, y - 80) },
					data: { ...dropData.data.defaultData, label: dropData.data.label }
				};
				nodes = [...nodes, newNode];
			}
		} catch (error) {
			console.error('Failed to parse drop data:', error);
		}
		
		isDraggingFromSidebar = false;
	}

	function handleCanvasDragOver(event: DragEvent) {
		event.preventDefault();
	}

	// Node interaction handlers with proper event handling
	function handleMouseDown(event: MouseEvent, node: any) {
		// Only start dragging if clicking on the node header or empty areas
		if (event.target.closest('.node-property') || 
			event.target.closest('.property-input') || 
			event.target.closest('.property-select') ||
			event.target.closest('.property-checkbox')) {
			return; // Don't start dragging if clicking on form controls
		}
		
		if (event.button !== 0) return;
		
		isDragging = true;
		dragNode = node;
		const rect = canvas.getBoundingClientRect();
		const nodeScreenX = node.position.x * zoomLevel + panOffset.x;
		const nodeScreenY = node.position.y * zoomLevel + panOffset.y;
		dragOffset.x = event.clientX - rect.left - nodeScreenX;
		dragOffset.y = event.clientY - rect.top - nodeScreenY;
		
		event.preventDefault();
		event.stopPropagation();
	}

	function handleNodeClick(event: MouseEvent, node: any) {
		event.stopPropagation();
		selectedNode = { ...node };
	}

	function handleMouseMove(event: MouseEvent) {
		const rect = canvas.getBoundingClientRect();
		mousePos.x = (event.clientX - rect.left - panOffset.x) / zoomLevel;
		mousePos.y = (event.clientY - rect.top - panOffset.y) / zoomLevel;

		if (isDragging && dragNode) {
			const nodeIndex = nodes.findIndex(n => n.id === dragNode.id);
			if (nodeIndex >= 0) {
				const newX = Math.max(0, (event.clientX - rect.left - dragOffset.x - panOffset.x) / zoomLevel);
				const newY = Math.max(0, (event.clientY - rect.top - dragOffset.y - panOffset.y) / zoomLevel);
				nodes[nodeIndex].position.x = newX;
				nodes[nodeIndex].position.y = newY;
				nodes = [...nodes];
				
				if (selectedNode?.id === dragNode.id) {
					selectedNode = { ...nodes[nodeIndex] };
				}
			}
		}

		handlePanning(event);
	}

	function handleMouseUp() {
		isDragging = false;
		dragNode = null;
		isConnecting = false;
		connectionStart = null;
		stopPanning();
	}

	// Connection handling
	function startConnection(event: MouseEvent, nodeId: string) {
		event.stopPropagation();
		isConnecting = true;
		connectionStart = nodeId;
	}

	function endConnection(event: MouseEvent, nodeId: string) {
		event.stopPropagation();
		if (isConnecting && connectionStart && connectionStart !== nodeId) {
			const existingEdge = edges.find(e => 
				(e.source === connectionStart && e.target === nodeId) ||
				(e.source === nodeId && e.target === connectionStart)
			);
			
			if (!existingEdge) {
				const newEdge = {
					id: `e-${connectionStart}-${nodeId}-${Date.now()}`,
					source: connectionStart,
					target: nodeId
				};
				edges = [...edges, newEdge];
			}
		}
		isConnecting = false;
		connectionStart = null;
	}

	// Node and edge management
	function deleteNode(nodeId: string) {
		nodes = nodes.filter(n => n.id !== nodeId);
		edges = edges.filter(e => e.source !== nodeId && e.target !== nodeId);
		if (selectedNode?.id === nodeId) {
			selectedNode = null;
		}
	}

	function deleteEdge(edgeId: string) {
		edges = edges.filter(e => e.id !== edgeId);
	}

	// Property updates with proper reactivity
	function updateNodeProperty(nodeId: string, key: string, value: any) {
		const nodeIndex = nodes.findIndex(n => n.id === nodeId);
		if (nodeIndex >= 0) {
			// Handle nested property paths
			const keyParts = key.split('.');
			let target = nodes[nodeIndex].data;
			
			for (let i = 0; i < keyParts.length - 1; i++) {
				if (!target[keyParts[i]]) {
					target[keyParts[i]] = {};
				}
				target = target[keyParts[i]];
			}
			
			target[keyParts[keyParts.length - 1]] = value;
			nodes = [...nodes]; // Trigger reactivity
			
			if (selectedNode?.id === nodeId) {
				selectedNode = { ...nodes[nodeIndex] };
			}
		}
	}

	function getNodeProperty(node: any, key: string) {
		const keyParts = key.split('.');
		let value = node.data;
		
		for (const part of keyParts) {
			value = value?.[part];
		}
		
		return value;
	}

	// Panel toggle functions
	function toggleSidebar() {
		sidebarCollapsed = !sidebarCollapsed;
	}

	function togglePropertyPanel() {
		propertyPanelCollapsed = !propertyPanelCollapsed;
	}

	// Helper functions
	function getComponentConfig(type: string) {
		for (const category of Object.values(componentCategories)) {
			if (category.components[type]) {
				return category.components[type];
			}
		}
		return { label: type, icon: '⚡', color: '#6b7280' };
	}

	function getConnectionPoints(sourceNode: any, targetNode: any) {
		const sourceX = sourceNode.position.x + 320;
		const sourceY = sourceNode.position.y + 80;
		const targetX = targetNode.position.x;
		const targetY = targetNode.position.y + 80;
		
		return { sourceX, sourceY, targetX, targetY };
	}

	// Canvas setup
	onMount(() => {
		document.addEventListener('mousemove', handleMouseMove);
		document.addEventListener('mouseup', handleMouseUp);
		
		return () => {
			document.removeEventListener('mousemove', handleMouseMove);
			document.removeEventListener('mouseup', handleMouseUp);
		};
	});
</script>

<div 
	class="workflow-builder {elem_classes.join(' ')}"
	class:hide={!visible}
	style:min-width={min_width && min_width + "px"}
	id={elem_id}
>
	<!-- Top Section: Main Workflow Area -->
	<div class="top-section">
		<!-- Left Sidebar -->
		<div class="sidebar" class:collapsed={sidebarCollapsed}>
			<div class="sidebar-header">
				{#if !sidebarCollapsed}
					<h3>Components</h3>
				{/if}
				<button 
					class="toggle-btn sidebar-toggle"
					on:click={toggleSidebar}
					title={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
				>
					{sidebarCollapsed ? '→' : '←'}
				</button>
			</div>
			
			{#if !sidebarCollapsed}
				<div class="sidebar-content">
					{#each Object.entries(componentCategories) as [categoryName, category]}
						<div class="category">
							<div class="category-header">
								<span class="category-icon">{category.icon}</span>
								<span class="category-name">{categoryName}</span>
							</div>
							
							<div class="category-components">
								{#each Object.entries(category.components) as [componentType, component]}
									<div 
										class="component-item"
										draggable="true"
										on:dragstart={(e) => handleSidebarDragStart(e, componentType, component)}
									>
										<span class="component-icon">{component.icon}</span>
										<span class="component-label">{component.label}</span>
									</div>
								{/each}
							</div>
						</div>
					{/each}
				</div>
			{/if}
		</div>

		<!-- Main Canvas Area -->
		<div class="canvas-area">
			<!-- Toolbar -->
			<div class="toolbar">
				<div class="toolbar-left">
					<input 
						class="workflow-name-input"
						type="text"
						bind:value={workflowName}
						placeholder="Workflow Name"
						title="Enter workflow name"
					/>
				</div>
				<div class="toolbar-center">
					<!-- Zoom Controls -->
					<div class="zoom-controls">
						<button class="zoom-btn" on:click={zoomOut} title="Zoom Out">-</button>
						<span class="zoom-level">{Math.round(zoomLevel * 100)}%</span>
						<button class="zoom-btn" on:click={zoomIn} title="Zoom In">+</button>
						<button class="zoom-btn reset" on:click={resetZoom} title="Reset View">⌂</button>
					</div>
				</div>
				<div class="toolbar-right">
					<span class="node-count">Nodes: {nodes.length}</span>
					<span class="edge-count">Edges: {edges.length}</span>
					<button class="clear-btn" on:click={clearWorkflow} title="Clear Workflow">
						🗑️ Clear
					</button>
				</div>
			</div>

			<!-- Canvas Container -->
			<div class="canvas-container" bind:this={canvasContainer}>
				<div 
					class="canvas"
					bind:this={canvas}
					style="transform: scale({zoomLevel}) translate({panOffset.x / zoomLevel}px, {panOffset.y / zoomLevel}px);"
					on:drop={handleCanvasDropFromSidebar}
					on:dragover={handleCanvasDragOver}
					on:wheel={handleWheel}
					on:mousedown={startPanning}
					on:click={() => { selectedNode = null; }}
				>
					<!-- Grid Background -->
					<div class="grid-background"></div>

					<!-- Edges (SVG) -->
					<svg class="edges-layer">
						{#each edges as edge (edge.id)}
							{@const sourceNode = nodes.find(n => n.id === edge.source)}
							{@const targetNode = nodes.find(n => n.id === edge.target)}
							{#if sourceNode && targetNode}
								{@const points = getConnectionPoints(sourceNode, targetNode)}
								<g class="edge-group">
									<path
										d="M {points.sourceX} {points.sourceY} C {points.sourceX + 80} {points.sourceY} {points.targetX - 80} {points.targetY} {points.targetX} {points.targetY}"
										stroke="#64748b"
										stroke-width="2"
										fill="none"
										class="edge-path"
									/>
									<circle
										cx={points.targetX}
										cy={points.targetY}
										r="4"
										fill="#64748b"
									/>
									<circle
										cx={(points.sourceX + points.targetX) / 2}
										cy={(points.sourceY + points.targetY) / 2}
										r="10"
										fill="#ef4444"
										class="edge-delete"
										on:click|stopPropagation={() => deleteEdge(edge.id)}
									/>
									<text
										x={(points.sourceX + points.targetX) / 2}
										y={(points.sourceY + points.targetY) / 2 + 4}
										text-anchor="middle"
										class="edge-delete-text"
										on:click|stopPropagation={() => deleteEdge(edge.id)}
									>
										✕
									</text>
								</g>
							{/if}
						{/each}
						
						<!-- Connection preview -->
						{#if isConnecting && connectionStart}
							{@const startNode = nodes.find(n => n.id === connectionStart)}
							{#if startNode}
								<path
									d="M {startNode.position.x + 320} {startNode.position.y + 80} L {mousePos.x} {mousePos.y}"
									stroke="#3b82f6"
									stroke-width="3"
									stroke-dasharray="8,4"
									fill="none"
									opacity="0.8"
								/>
							{/if}
						{/if}
					</svg>

					<!-- FIXED: Nodes with guaranteed connection points -->
					{#each nodes as node (node.id)}
						{@const config = getComponentConfig(node.type)}
						<div 
							class="node"
							class:selected={selectedNode?.id === node.id}
							style="left: {node.position.x}px; top: {node.position.y}px; border-color: {config.color};"
							on:mousedown={(e) => handleMouseDown(e, node)}
							on:click={(e) => handleNodeClick(e, node)}
						>
							<div class="node-header" style="background: {config.color};">
								<span class="node-icon">{config.icon}</span>
								<span class="node-title">{node.data.display_name || node.data.label}</span>
								<button 
									class="node-delete"
									on:click|stopPropagation={() => deleteNode(node.id)}
									title="Delete node"
								>
									✕
								</button>
							</div>
							
							<div class="node-content">
								<!-- Dynamic property rendering based on node type -->
								{#if propertyFields[node.type]}
									{#each propertyFields[node.type].slice(0, 3) as field}
										<div class="node-property">
											<label class="property-label">{field.label}:</label>
											{#if field.type === 'select'}
												<select 
													class="property-select"
													value={getNodeProperty(node, field.key) || ''}
													on:change={(e) => updateNodeProperty(node.id, field.key, e.target.value)}
													on:click|stopPropagation
												>
													{#each field.options as option}
														<option value={option}>{option}</option>
													{/each}
												</select>
											{:else if field.type === 'number'}
												<input 
													class="property-input"
													type="number"
													min={field.min}
													max={field.max}
													step={field.step}
													value={getNodeProperty(node, field.key) || 0}
													on:input={(e) => updateNodeProperty(node.id, field.key, Number(e.target.value))}
													on:click|stopPropagation
												/>
											{:else if field.type === 'checkbox'}
												<label class="property-checkbox">
													<input 
														type="checkbox"
														checked={getNodeProperty(node, field.key) || false}
														on:change={(e) => updateNodeProperty(node.id, field.key, e.target.checked)}
														on:click|stopPropagation
													/>
													<span>Yes</span>
												</label>
											{:else if field.type === 'textarea'}
												<textarea
													class="property-input"
													value={getNodeProperty(node, field.key) || ''}
													on:input={(e) => updateNodeProperty(node.id, field.key, e.target.value)}
													on:click|stopPropagation
													rows="2"
												></textarea>
											{:else}
												<input 
													class="property-input"
													type="text"
													value={getNodeProperty(node, field.key) || ''}
													on:input={(e) => updateNodeProperty(node.id, field.key, e.target.value)}
													on:click|stopPropagation
												/>
											{/if}
										</div>
									{/each}
								{:else}
									<div class="node-status">Ready</div>
								{/if}
							</div>

							<!-- FIXED: Connection points with fallback system -->
							{#if node.data.template}
								<!-- Try to create dynamic connection points based on template -->
								{@const templateHandles = Object.entries(node.data.template).filter(([_, handle]) => handle.is_handle)}
								{#each templateHandles as [handleId, handle], index}
									{#if handle.type === 'string' || handle.type === 'object' || handle.type === 'list' || handle.type === 'file'}
										<div 
											class="connection-point {handle.type === 'string' || handle.type === 'list' || handle.type === 'file' ? 'output' : 'input'}"
											style="top: {index * 25 + 40}px; {(handle.type === 'string' || handle.type === 'list' || handle.type === 'file') ? 'right: -6px;' : 'left: -6px;'}"
											on:mouseup={(e) => (handle.type === 'object') && endConnection(e, node.id)}
											on:mousedown={(e) => (handle.type === 'string' || handle.type === 'list' || handle.type === 'file') && startConnection(e, node.id)}
											title={`${handle.display_name || handleId} (${handle.type})`}
										></div>
									{/if}
								{/each}
								
								<!-- FALLBACK: Ensure every node has at least basic connection points -->
								{@const hasInputHandles = templateHandles.some(([_, h]) => h.type === 'object')}
								{@const hasOutputHandles = templateHandles.some(([_, h]) => h.type === 'string' || h.type === 'list' || h.type === 'file')}
								
								{#if !hasInputHandles}
									<div 
										class="connection-point input"
										style="top: 50%; left: -6px; transform: translateY(-50%);"
										on:mouseup={(e) => endConnection(e, node.id)}
										title="Input"
									></div>
								{/if}
								
								{#if !hasOutputHandles}
									<div 
										class="connection-point output"
										style="top: 50%; right: -6px; transform: translateY(-50%);"
										on:mousedown={(e) => startConnection(e, node.id)}
										title="Output"
									></div>
								{/if}
							{:else}
								<!-- FALLBACK: Nodes without templates get basic connection points -->
								<div 
									class="connection-point input"
									style="top: 50%; left: -6px; transform: translateY(-50%);"
									on:mouseup={(e) => endConnection(e, node.id)}
									title="Input"
								></div>
								<div 
									class="connection-point output"
									style="top: 50%; right: -6px; transform: translateY(-50%);"
									on:mousedown={(e) => startConnection(e, node.id)}
									title="Output"
								></div>
							{/if}
						</div>
					{/each}
				</div>
			</div>
		</div>

		<!-- Right Property Panel -->
		<div class="property-panel" class:collapsed={propertyPanelCollapsed}>
			<div class="property-header">
				{#if !propertyPanelCollapsed}
					<h3>Properties</h3>
				{/if}
				<button 
					class="toggle-btn property-toggle"
					on:click={togglePropertyPanel}
					title={propertyPanelCollapsed ? 'Expand properties' : 'Collapse properties'}
				>
					{propertyPanelCollapsed ? '←' : '→'}
				</button>
			</div>
			
			{#if !propertyPanelCollapsed}
				<div class="property-content">
					{#if selectedNode && propertyFields[selectedNode.type]}
						<div class="property-node-info">
							<h4>{selectedNode.data.display_name || selectedNode.data.label}</h4>
							<p class="property-node-type">TYPE: {selectedNode.type.toUpperCase()}</p>
						</div>
						
						<div class="property-fields">
							{#each propertyFields[selectedNode.type] as field}
								<div class="property-field">
									<label for={field.key}>{field.label}</label>
									{#if field.help}
										<small class="field-help">{field.help}</small>
									{/if}
									
									{#if field.type === 'text'}
										<input
											type="text"
											id={field.key}
											value={getNodeProperty(selectedNode, field.key) || ''}
											on:input={(e) => updateNodeProperty(selectedNode.id, field.key, e.target.value)}
										/>
									{:else if field.type === 'number'}
										<input
											type="number"
											id={field.key}
											value={getNodeProperty(selectedNode, field.key) || 0}
											min={field.min}
											max={field.max}
											step={field.step}
											on:input={(e) => updateNodeProperty(selectedNode.id, field.key, Number(e.target.value))}
										/>
									{:else if field.type === 'checkbox'}
										<label class="checkbox-label">
											<input
												type="checkbox"
												id={field.key}
												checked={getNodeProperty(selectedNode, field.key) || false}
												on:change={(e) => updateNodeProperty(selectedNode.id, field.key, e.target.checked)}
											/>
											<span class="checkbox-text">Enable</span>
										</label>
									{:else if field.type === 'select'}
										<select
											id={field.key}
											value={getNodeProperty(selectedNode, field.key) || ''}
											on:change={(e) => updateNodeProperty(selectedNode.id, field.key, e.target.value)}
										>
											{#each field.options as option}
												<option value={option}>{option}</option>
											{/each}
										</select>
									{:else if field.type === 'textarea'}
										<textarea
											id={field.key}
											value={getNodeProperty(selectedNode, field.key) || ''}
											on:input={(e) => updateNodeProperty(selectedNode.id, field.key, e.target.value)}
											rows="4"
										></textarea>
									{/if}
								</div>
							{/each}
						</div>
					{:else}
						<div class="property-empty">
							<div class="empty-icon">🎯</div>
							<p>Select a node to edit properties</p>
							<small>Click on any node to configure its detailed settings</small>
						</div>
					{/if}
				</div>
			{/if}
		</div>
	</div>
</div>

<style>
	/* Base styles with proper sizing */
	.workflow-builder {
		width: 100%;
		height: 700px;
		border: 1px solid #e2e8f0;
		border-radius: 12px;
		display: flex;
		flex-direction: column;
		background: #ffffff;
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
		overflow: hidden;
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
	}

	.hide {
		display: none;
	}

	.top-section {
		flex: 1;
		display: flex;
		min-height: 0;
	}

	/* Sidebar Styles */
	.sidebar {
		width: 240px;
		min-width: 240px;
		background: #f8fafc;
		border-right: 1px solid #e2e8f0;
		display: flex;
		flex-direction: column;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		position: relative;
	}

	.sidebar.collapsed {
		width: 48px;
		min-width: 48px;
	}

	.sidebar-header {
		padding: 12px;
		border-bottom: 1px solid #e2e8f0;
		display: flex;
		align-items: center;
		justify-content: space-between;
		background: white;
		min-height: 50px;
		box-sizing: border-box;
	}

	.sidebar-header h3 {
		margin: 0;
		font-size: 15px;
		font-weight: 600;
		color: #1e293b;
	}

	.toggle-btn {
		background: #f1f5f9;
		border: 1px solid #e2e8f0;
		border-radius: 6px;
		padding: 6px 8px;
		cursor: pointer;
		color: #64748b;
		font-size: 14px;
		transition: all 0.2s;
		min-width: 28px;
		height: 28px;
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 10;
		position: relative;
	}

	.toggle-btn:hover {
		background: #e2e8f0;
		color: #475569;
	}

	.sidebar-toggle {
		position: absolute;
		right: 8px;
		top: 50%;
		transform: translateY(-50%);
	}

	.sidebar-content {
		flex: 1;
		overflow-y: auto;
		padding: 12px;
	}

	.category {
		margin-bottom: 12px;
	}

	.category-header {
		display: flex;
		align-items: center;
		padding: 6px 0;
		font-weight: 600;
		font-size: 12px;
		color: #374151;
		border-bottom: 1px solid #e5e7eb;
		margin-bottom: 6px;
	}

	.category-icon {
		margin-right: 6px;
		font-size: 14px;
	}

	.component-item {
		display: flex;
		align-items: center;
		padding: 6px 8px;
		margin-bottom: 3px;
		background: white;
		border: 1px solid #e5e7eb;
		border-radius: 6px;
		cursor: grab;
		transition: all 0.2s ease;
		font-size: 12px;
	}

	.component-item:hover {
		background: #f8fafc;
		border-color: #cbd5e1;
		transform: translateX(2px);
	}

	.component-item:active {
		cursor: grabbing;
	}

	.component-icon {
		margin-right: 6px;
		font-size: 14px;
	}

	.component-label {
		font-weight: 500;
		color: #374151;
	}

	/* Canvas Area Styles */
	.canvas-area {
		flex: 1;
		display: flex;
		flex-direction: column;
		min-width: 400px;
	}

	.toolbar {
		height: 50px;
		border-bottom: 1px solid #e2e8f0;
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 0 16px;
		background: white;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
	}

	.workflow-name-input {
		font-size: 16px;
		font-weight: 600;
		color: #1e293b;
		border: none;
		background: transparent;
		outline: none;
		padding: 4px 8px;
		border-radius: 4px;
		transition: background 0.2s;
	}

	.workflow-name-input:hover,
	.workflow-name-input:focus {
		background: #f1f5f9;
	}

	.toolbar-center {
		display: flex;
		align-items: center;
	}

	.zoom-controls {
		display: flex;
		align-items: center;
		gap: 4px;
		background: #f1f5f9;
		padding: 4px;
		border-radius: 8px;
		border: 1px solid #e2e8f0;
	}

	.zoom-btn {
		background: white;
		border: none;
		width: 28px;
		height: 28px;
		border-radius: 4px;
		cursor: pointer;
		font-weight: 600;
		display: flex;
		align-items: center;
		justify-content: center;
		transition: all 0.2s;
		font-size: 14px;
	}

	.zoom-btn:hover {
		background: #e2e8f0;
	}

	.zoom-btn.reset {
		font-size: 12px;
	}

	.zoom-level {
		font-size: 12px;
		font-weight: 600;
		color: #64748b;
		min-width: 40px;
		text-align: center;
	}

	.toolbar-right {
		display: flex;
		gap: 12px;
		font-size: 12px;
		align-items: center;
	}

	.node-count, .edge-count {
		color: #64748b;
		background: #f1f5f9;
		padding: 4px 8px;
		border-radius: 12px;
		font-weight: 500;
	}

	.export-btn {
		background: #3b82f6;
		color: white;
		border: none;
		padding: 6px 12px;
		border-radius: 6px;
		font-size: 12px;
		font-weight: 500;
		cursor: pointer;
		transition: all 0.2s;
		display: flex;
		align-items: center;
		gap: 4px;
	}

	.export-btn:hover {
		background: #2563eb;
		transform: translateY(-1px);
	}

	.canvas-container {
		flex: 1;
		position: relative;
		overflow: hidden;
		background: #fafbfc;
		cursor: grab;
	}

	.canvas-container:active {
		cursor: grabbing;
	}

	.canvas {
		position: absolute;
		top: 0;
		left: 0;
		width: 4000px;
		height: 4000px;
		transform-origin: 0 0;
	}

	.grid-background {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-image: 
			radial-gradient(circle, #e2e8f0 1px, transparent 1px);
		background-size: 20px 20px;
		pointer-events: none;
		opacity: 0.6;
	}

	.edges-layer {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		pointer-events: none;
		z-index: 1;
	}

	.edge-delete, .edge-delete-text {
		pointer-events: all;
		cursor: pointer;
	}

	.edge-delete-text {
		font-size: 10px;
		fill: white;
		text-anchor: middle;
		user-select: none;
	}

	.edge-delete:hover {
		fill: #dc2626;
	}

	/* Node styles with proper sizing and no overflow */
	.node {
		position: absolute;
		width: 320px;
		min-height: 160px;
		background: white;
		border: 2px solid #e2e8f0;
		border-radius: 10px;
		cursor: move;
		user-select: none;
		z-index: 2;
		transition: all 0.2s ease;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
		overflow: visible;
	}

	.node:hover {
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
		transform: translateY(-1px);
	}

	.node.selected {
		border-color: #3b82f6;
		box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1), 0 4px 16px rgba(0, 0, 0, 0.15);
	}

	.node-header {
		display: flex;
		align-items: center;
		padding: 12px 16px;
		color: white;
		font-weight: 600;
		font-size: 14px;
		border-radius: 8px 8px 0 0;
		min-height: 24px;
	}

	.node-icon {
		margin-right: 8px;
		font-size: 16px;
		flex-shrink: 0;
	}

	.node-title {
		flex: 1;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.node-delete {
		background: rgba(255, 255, 255, 0.2);
		border: none;
		color: white;
		cursor: pointer;
		font-size: 12px;
		padding: 4px 6px;
		border-radius: 4px;
		transition: all 0.2s;
		flex-shrink: 0;
	}

	.node-delete:hover {
		background: rgba(255, 255, 255, 0.3);
	}

	.node-content {
		padding: 12px 16px;
		max-height: 200px;
		overflow-y: auto;
		overflow-x: hidden;
	}

	.node-property {
		display: flex;
		flex-direction: column;
		gap: 4px;
		margin-bottom: 12px;
		font-size: 12px;
	}

	.property-label {
		font-weight: 600;
		color: #374151;
		font-size: 11px;
		margin-bottom: 2px;
	}

	.property-input, .property-select {
		width: 100%;
		padding: 6px 8px;
		border: 1px solid #d1d5db;
		border-radius: 4px;
		font-size: 11px;
		background: white;
		transition: all 0.2s;
		box-sizing: border-box;
		resize: vertical;
	}

	.property-input:focus, .property-select:focus {
		outline: none;
		border-color: #3b82f6;
		box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
	}

	.property-input:hover, .property-select:hover {
		border-color: #9ca3af;
	}

	.property-checkbox {
		display: flex;
		align-items: center;
		gap: 6px;
		font-size: 11px;
		color: #374151;
		cursor: pointer;
	}

	.property-checkbox input[type="checkbox"] {
		width: auto;
		margin: 0;
		cursor: pointer;
	}

	.node-status {
		font-size: 12px;
		color: #64748b;
		text-align: center;
		padding: 20px;
		font-style: italic;
	}

	/* FIXED: Connection points that work for ALL nodes */
	.connection-point {
		position: absolute;
		width: 12px;
		height: 12px;
		border-radius: 50%;
		background: #3b82f6;
		border: 2px solid white;
		cursor: crosshair;
		z-index: 3;
		transition: all 0.2s ease;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
	}

	.connection-point.input {
		left: -6px;
	}

	.connection-point.output {
		right: -6px;
	}

	.connection-point:hover {
		background: #2563eb;
		transform: scale(1.2);
		box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
	}

	/* Property Panel Styles */
	.property-panel {
		width: 280px;
		min-width: 280px;
		background: #f8fafc;
		border-left: 1px solid #e2e8f0;
		display: flex;
		flex-direction: column;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		position: relative;
	}

	.property-panel.collapsed {
		width: 48px;
		min-width: 48px;
	}

	.property-header {
		padding: 12px;
		border-bottom: 1px solid #e2e8f0;
		display: flex;
		align-items: center;
		justify-content: space-between;
		background: white;
		min-height: 50px;
		box-sizing: border-box;
	}

	.property-header h3 {
		margin: 0;
		font-size: 15px;
		font-weight: 600;
		color: #1e293b;
	}

	.property-toggle {
		position: absolute;
		left: 8px;
		top: 50%;
		transform: translateY(-50%);
	}

	.property-content {
		flex: 1;
		overflow-y: auto;
		padding: 16px;
	}

	.property-node-info {
		margin-bottom: 20px;
		padding: 12px;
		background: white;
		border-radius: 8px;
		border: 1px solid #e2e8f0;
	}

	.property-node-info h4 {
		margin: 0 0 4px 0;
		font-size: 16px;
		color: #1e293b;
	}

	.property-node-type {
		margin: 0;
		font-size: 11px;
		color: #64748b;
		text-transform: uppercase;
		font-weight: 600;
	}

	.property-field {
		margin-bottom: 16px;
	}

	.property-field label {
		display: block;
		margin-bottom: 6px;
		font-size: 13px;
		font-weight: 600;
		color: #374151;
	}

	.field-help {
		display: block;
		margin-bottom: 4px;
		font-size: 11px;
		color: #64748b;
		font-style: italic;
	}

	.property-field input,
	.property-field select,
	.property-field textarea {
		width: 100%;
		padding: 8px 10px;
		border: 1px solid #d1d5db;
		border-radius: 6px;
		font-size: 13px;
		background: white;
		transition: border-color 0.2s;
		box-sizing: border-box;
	}

	.property-field input:focus,
	.property-field select:focus,
	.property-field textarea:focus {
		outline: none;
		border-color: #3b82f6;
		box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
	}

	.checkbox-label {
		display: flex !important;
		align-items: center;
		margin-bottom: 0 !important;
		cursor: pointer;
	}

	.checkbox-label input[type="checkbox"] {
		width: auto !important;
		margin-right: 8px !important;
	}

	.property-empty {
		text-align: center;
		padding: 40px 16px;
		color: #64748b;
	}

	.empty-icon {
		font-size: 32px;
		margin-bottom: 12px;
		opacity: 0.5;
	}

	.property-empty p {
		margin: 0 0 6px 0;
		font-size: 14px;
		font-weight: 500;
	}

	.property-empty small {
		font-size: 12px;
		opacity: 0.7;
	}
	.clear-btn {
    background: #ef4444;
    color: white;
    border: none;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 4px;
}

.clear-btn:hover {
    background: #dc2626;
    transform: translateY(-1px);
}

</style>
