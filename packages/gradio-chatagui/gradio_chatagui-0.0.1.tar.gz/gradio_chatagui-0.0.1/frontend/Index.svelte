<svelte:options accessors={true} />

<script lang="ts">
	import type { Gradio } from "@gradio/utils";
	import { BlockTitle } from "@gradio/atoms";
	import { Block } from "@gradio/atoms";
	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";
	import { onMount, onDestroy, afterUpdate } from "svelte";
	import { marked } from "marked";
	import Chart from "chart.js/auto";

	interface Message {
		id: string;
		role: "user" | "assistant" | "system";
		content: string;
		type?: "text" | "tool_call" | "tool_result";
		toolCallId?: string;
		name?: string;
		timestamp: number;
		streaming?: boolean;
	}

	interface AGUIEvent {
		type: string;
		id?: string;
		content?: string;
		args?: any;
		toolCallId?: string;
		snapshot?: any;
		delta?: any;
		name?: string;
		value?: any;
		parentMessageId?: string;
	}

	interface ToolCall {
		id: string;
		name: string;
		args: any;
		status: "pending" | "executing" | "completed" | "error";
		result?: any;
	}

	export let gradio: Gradio<{
		change: string;
		submit: { message: string; thread_id: string };
		input: never;
		clear_status: LoadingStatus;
	}>;
	export let label = "AG-UI Chat";
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value = "";
	export let show_label = true;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus | undefined = undefined;
	export let interactive = true;
	export let root: string;
	export let api_root = "";
	export let initial_thread_id = "";

	let messages: Message[] = [];
	let currentInput = "";
	let isRunning = false;
	let eventSource: EventSource | null = null;
	let messagesContainer: HTMLElement;
	let toolCalls: Map<string, ToolCall> = new Map();
	let state: any = {};
	let runId = "";
	let threadId = initial_thread_id || `thread_${Date.now()}`;
	let charts: Map<string, Chart> = new Map();
	let shouldAutoScroll = true;
	let userScrollPosition = 0;

	onMount(() => {
		if (messagesContainer) {
			messagesContainer.addEventListener('scroll', handleScroll);
		}
	});

	onDestroy(() => {
		if (eventSource) {
			eventSource.close();
		}
		if (messagesContainer) {
			messagesContainer.removeEventListener('scroll', handleScroll);
		}
		// Destroy all charts
		charts.forEach(chart => chart.destroy());
		charts.clear();
	});

	afterUpdate(() => {
		if (shouldAutoScroll && messagesContainer) {
			messagesContainer.scrollTop = messagesContainer.scrollHeight;
		}
	});

	function handleScroll() {
		if (!messagesContainer) return;
		const { scrollTop, scrollHeight, clientHeight } = messagesContainer;
		userScrollPosition = scrollTop;
		shouldAutoScroll = (scrollHeight - scrollTop - clientHeight) < 80;
	}

	function generateId(): string {
		return `id_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
	}

	async function sendMessage() {
		if (!currentInput.trim() || isRunning) return;

		const userMessage: Message = {
			id: generateId(),
			role: "user",
			content: currentInput.trim(),
			timestamp: Date.now()
		};

		messages = [...messages, userMessage];
		const messageText = currentInput.trim();
		currentInput = "";
		isRunning = true;

		runId = generateId();

		try {
			const response = await fetch(`${api_root}/run_agent`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({
					thread_id: threadId,
					run_id: runId,
					messages: messages,
					tools: getToolDefinitions()
				})
			});

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			openEventStream();
			gradio.dispatch("submit", { message: messageText, thread_id: threadId });
		} catch (error) {
			console.error("Error sending message:", error);
			addErrorMessage("Failed to send message. Please try again.");
			isRunning = false;
		}
	}

	function openEventStream() {
		if (eventSource) {
			eventSource.close();
		}

		// Connect directly to the SSE stream from /run_agent POST response
		// The backend should handle SSE streaming after the initial POST
		eventSource = new EventSource(`${api_root}/stream?run_id=${runId}`);
		
		eventSource.onmessage = (event) => {
			try {
				const agEvent: AGUIEvent = JSON.parse(event.data);
				handleEvent(agEvent);
			} catch (error) {
				console.error("Error parsing SSE event:", error);
			}
		};

		eventSource.onerror = (error) => {
			console.error("SSE error:", error);
			if (eventSource?.readyState === EventSource.CLOSED) {
				isRunning = false;
			}
		};
	}

	function handleEvent(event: AGUIEvent) {
		switch (event.type) {
			case "RUN_STARTED":
				isRunning = true;
				break;
			
			case "RUN_FINISHED":
				isRunning = false;
				if (eventSource) {
					eventSource.close();
					eventSource = null;
				}
				break;
			
			case "TEXT_MESSAGE_START":
				const newMessage: Message = {
					id: event.id || generateId(),
					role: "assistant",
					content: "",
					timestamp: Date.now(),
					streaming: true
				};
				messages = [...messages, newMessage];
				break;
			
			case "TEXT_MESSAGE_CONTENT":
				if (event.id && event.content) {
					messages = messages.map(msg => 
						msg.id === event.id 
							? { ...msg, content: msg.content + event.content }
							: msg
					);
				}
				break;
			
			case "TEXT_MESSAGE_END":
				if (event.id) {
					messages = messages.map(msg => 
						msg.id === event.id 
							? { ...msg, streaming: false }
							: msg
					);
				}
				break;
			
			case "TOOL_CALL_START":
				if (event.id && event.name) {
					const toolCall: ToolCall = {
						id: event.toolCallId || event.id,
						name: event.name,
						args: event.args || {},
						status: "pending"
					};
					toolCalls.set(toolCall.id, toolCall);
					toolCalls = toolCalls;
					
					const toolMessage: Message = {
						id: generateId(),
						role: "assistant",
						content: `🔧 Calling tool: ${event.name}`,
						type: "tool_call",
						toolCallId: toolCall.id,
						timestamp: Date.now()
					};
					messages = [...messages, toolMessage];
				}
				break;
			
			case "TOOL_CALL_END":
				if (event.toolCallId) {
					const toolCall = toolCalls.get(event.toolCallId);
					if (toolCall) {
						toolCall.status = "completed";
						toolCall.result = event.content;
						toolCalls.set(event.toolCallId, toolCall);
						toolCalls = toolCalls;
						
						if (isBackendTool(toolCall.name)) {
							// Backend tools are auto-executed, just show the result
							updateToolMessage(event.toolCallId, `✅ ${toolCall.name} completed`);
						} else {
							// Frontend tool needs user interaction
							executeFrontendTool(toolCall);
						}
					}
				}
				break;
			
			case "STATE_SNAPSHOT":
				state = event.snapshot || {};
				break;
			
			case "STATE_DELTA":
				if (event.delta) {
					applyStateDelta(event.delta);
				}
				break;
			
			case "CUSTOM":
				if (event.name === "chart") {
					renderChart(event);
				}
				break;
			
			case "RUN_ERROR":
				addErrorMessage(event.content || "An error occurred");
				isRunning = false;
				if (eventSource) {
					eventSource.close();
					eventSource = null;
				}
				break;
		}
	}

	function updateToolMessage(toolCallId: string, content: string) {
		messages = messages.map(msg => 
			msg.toolCallId === toolCallId 
				? { ...msg, content }
				: msg
		);
	}

	function addErrorMessage(content: string) {
		const errorMessage: Message = {
			id: generateId(),
			role: "system",
			content: `❌ Error: ${content}`,
			timestamp: Date.now()
		};
		messages = [...messages, errorMessage];
	}

	function isBackendTool(toolName: string): boolean {
		// Check tool definition mode to determine if it's a backend tool
		const toolDef = getToolDefinitions().find(t => t.name === toolName);
		return toolDef?.mode === "backend";
	}

	function executeFrontendTool(toolCall: ToolCall) {
		switch (toolCall.name) {
			case "confirmAction":
				showConfirmModal(toolCall);
				break;
			default:
				console.warn(`Unknown frontend tool: ${toolCall.name}`);
				sendToolResult(toolCall.id, "false");
		}
	}

	function showConfirmModal(toolCall: ToolCall) {
		const { action } = toolCall.args;
		const confirmed = confirm(`${action}\n\nProceed with this action?`);
		sendToolResult(toolCall.id, confirmed ? "true" : "false");
	}

	async function sendToolResult(toolCallId: string, content: string) {
		try {
			await fetch(`${api_root}/tool_result`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({
					thread_id: threadId,
					run_id: runId,
					toolCallId,
					content
				})
			});
			
			updateToolMessage(toolCallId, `✅ Tool result sent: ${content}`);
		} catch (error) {
			console.error("Error sending tool result:", error);
			updateToolMessage(toolCallId, `❌ Failed to send tool result`);
		}
	}

	function applyStateDelta(delta: any) {
		// Simple merge for now - could use a proper JSON patch library
		state = { ...state, ...delta };
	}

	function renderChart(event: AGUIEvent) {
		const { value } = event;
		if (!value) return;

		const chartId = generateId();
		let chartMessage: Message;

		if (value.image) {
			// Pre-rendered image
			chartMessage = {
				id: chartId,
				role: "assistant",
				content: `<img src="${value.image}" alt="Chart" style="max-width: 100%; height: auto;" />`,
				timestamp: Date.now()
			};
		} else if (value.spec) {
			// Chart.js spec
			chartMessage = {
				id: chartId,
				role: "assistant",
				content: `<canvas id="chart_${chartId}" width="400" height="200"></canvas>`,
				timestamp: Date.now()
			};
		} else {
			return;
		}

		messages = [...messages, chartMessage];

		// If it's a Chart.js spec, render after DOM update
		if (value.spec) {
			setTimeout(() => {
				const canvas = document.getElementById(`chart_${chartId}`) as HTMLCanvasElement;
				if (canvas) {
					const chart = new Chart(canvas, {
						type: value.spec.type,
						data: {
							labels: value.spec.labels,
							datasets: [{
								label: value.spec.title,
								data: value.spec.values,
								backgroundColor: value.spec.type === "bar" 
									? "rgba(54, 162, 235, 0.8)"
									: "rgba(75, 192, 192, 0.8)",
								borderColor: value.spec.type === "bar"
									? "rgba(54, 162, 235, 1)"
									: "rgba(75, 192, 192, 1)",
								borderWidth: 2
							}]
						},
						options: {
							responsive: true,
							plugins: {
								title: {
									display: true,
									text: value.spec.title
								}
							}
						}
					});
					charts.set(chartId, chart);
				}
			}, 100);
		}
	}

	function getToolDefinitions() {
		return [
			{
				name: "confirmAction",
				description: "Ask user to confirm an action",
				mode: "frontend",
				parameters: {
					type: "object",
					properties: {
						action: { type: "string", description: "Action to confirm" },
						importance: { type: "string", enum: ["low", "medium", "high"], default: "medium" }
					},
					required: ["action"]
				}
			},
			{
				name: "webSearch",
				description: "Search the web for information",
				mode: "backend", 
				parameters: {
					type: "object",
					properties: {
						query: { type: "string", description: "Search query" }
					},
					required: ["query"]
				}
			},
			{
				name: "plotGraph",
				description: "Create a chart or graph",
				mode: "backend",
				parameters: {
					type: "object",
					properties: {
						data: { type: "array", items: { type: "number" }, description: "Data values" },
						chartType: { type: "string", enum: ["line", "bar"], description: "Chart type" },
						title: { type: "string", description: "Chart title" },
						labels: { type: "array", items: { type: "string" }, description: "Data labels" }
					},
					required: ["data", "chartType"]
				}
			}
		];
	}

	function handleKeyPress(e: KeyboardEvent) {
		if (e.key === "Enter" && !e.shiftKey) {
			e.preventDefault();
			sendMessage();
		}
	}

	function formatContent(content: string): string {
		try {
			return marked(content) as string;
		} catch {
			return content;
		}
	}

	function getMessageClass(message: Message): string {
		let classes = "message";
		classes += ` message-${message.role}`;
		if (message.streaming) classes += " streaming";
		if (message.type) classes += ` message-${message.type}`;
		return classes;
	}

	$: if (value !== currentInput) {
		currentInput = value;
	}

	$: gradio.dispatch("change", currentInput);
</script>

<Block
	{visible}
	{elem_id}
	{elem_classes}
	{scale}
	{min_width}
	allow_overflow={false}
	padding={true}
>
	{#if loading_status}
		<StatusTracker
			autoscroll={gradio.autoscroll}
			i18n={gradio.i18n}
			{...loading_status}
			on:clear_status={() => gradio.dispatch("clear_status", loading_status)}
		/>
	{/if}

	<div class="chat-container">
		{#if show_label}
			<BlockTitle {root} {show_label} info={undefined}>{label}</BlockTitle>
		{/if}

		<div class="messages-container" bind:this={messagesContainer}>
			{#each messages as message (message.id)}
				<div class={getMessageClass(message)}>
					<div class="message-content">
						{@html formatContent(message.content)}
					</div>
					{#if message.streaming}
						<div class="typing-indicator">
							<span></span>
							<span></span>
							<span></span>
						</div>
					{/if}
				</div>
			{/each}
		</div>

		<div class="input-container">
			<textarea
				bind:value={currentInput}
				placeholder="Type your message..."
				disabled={!interactive || isRunning}
				on:keydown={handleKeyPress}
				rows="3"
			></textarea>
			<button 
				on:click={sendMessage} 
				disabled={!interactive || isRunning || !currentInput.trim()}
				class="send-button"
			>
				{isRunning ? "⏳" : "Send"}
			</button>
		</div>

		{#if isRunning}
			<div class="status-indicator">
				<div class="spinner"></div>
				Agent is thinking...
			</div>
		{/if}
	</div>
</Block>

<style>
	.chat-container {
		display: flex;
		flex-direction: column;
		height: 500px;
		border: 1px solid var(--input-border-color);
		border-radius: var(--input-radius);
		background: var(--background-fill-primary);
	}

	.messages-container {
		flex: 1;
		overflow-y: auto;
		padding: 1rem;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.message {
		max-width: 80%;
		padding: 0.75rem 1rem;
		border-radius: 1rem;
		position: relative;
	}

	.message-user {
		align-self: flex-end;
		background: var(--button-primary-background-fill);
		color: var(--button-primary-text-color);
	}

	.message-assistant {
		align-self: flex-start;
		background: var(--input-background-fill);
		border: 1px solid var(--input-border-color);
	}

	.message-system {
		align-self: center;
		background: var(--color-accent-soft);
		font-style: italic;
		text-align: center;
		max-width: 90%;
	}

	.message-content {
		line-height: 1.5;
	}

	.message-content :global(p) {
		margin: 0;
	}

	.message-content :global(pre) {
		background: var(--background-fill-secondary);
		padding: 0.5rem;
		border-radius: 0.25rem;
		overflow-x: auto;
		margin: 0.5rem 0;
	}

	.message-content :global(code) {
		background: var(--background-fill-secondary);
		padding: 0.1rem 0.3rem;
		border-radius: 0.25rem;
		font-family: var(--font-mono);
	}

	.message-content :global(canvas) {
		max-width: 100%;
		height: auto;
		margin: 0.5rem 0;
	}

	.streaming {
		border-color: var(--color-accent);
	}

	.typing-indicator {
		display: flex;
		gap: 0.25rem;
		margin-top: 0.5rem;
		justify-content: flex-start;
	}

	.typing-indicator span {
		width: 0.5rem;
		height: 0.5rem;
		background: var(--body-text-color);
		border-radius: 50%;
		animation: typing 1.5s infinite;
	}

	.typing-indicator span:nth-child(2) {
		animation-delay: 0.2s;
	}

	.typing-indicator span:nth-child(3) {
		animation-delay: 0.4s;
	}

	@keyframes typing {
		0%, 60%, 100% {
			opacity: 0.3;
			transform: translateY(0);
		}
		30% {
			opacity: 1;
			transform: translateY(-0.25rem);
		}
	}

	.input-container {
		display: flex;
		padding: 1rem;
		gap: 0.5rem;
		border-top: 1px solid var(--input-border-color);
		background: var(--background-fill-secondary);
	}

	.input-container textarea {
		flex: 1;
		resize: none;
		border: 1px solid var(--input-border-color);
		border-radius: var(--input-radius);
		padding: 0.75rem;
		background: var(--input-background-fill);
		color: var(--body-text-color);
		font-family: inherit;
		font-size: var(--input-text-size);
		line-height: 1.4;
	}

	.input-container textarea:focus {
		outline: none;
		border-color: var(--input-border-color-focus);
		box-shadow: var(--input-shadow-focus);
	}

	.input-container textarea:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.send-button {
		padding: 0.75rem 1.5rem;
		background: var(--button-primary-background-fill);
		color: var(--button-primary-text-color);
		border: none;
		border-radius: var(--button-border-radius);
		cursor: pointer;
		font-weight: 600;
		transition: background-color 0.2s;
	}

	.send-button:hover:not(:disabled) {
		background: var(--button-primary-background-fill-hover);
	}

	.send-button:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	.status-indicator {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.5rem 1rem;
		background: var(--color-accent-soft);
		border-top: 1px solid var(--input-border-color);
		font-size: 0.875rem;
		color: var(--body-text-color-subdued);
	}

	.spinner {
		width: 1rem;
		height: 1rem;
		border: 2px solid var(--input-border-color);
		border-top: 2px solid var(--color-accent);
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}

	/* Responsive design */
	@media (max-width: 480px) {
		.chat-container {
			height: 400px;
		}
		
		.message {
			max-width: 95%;
		}
		
		.input-container {
			flex-direction: column;
		}
		
		.send-button {
			align-self: flex-end;
		}
	}
</style>