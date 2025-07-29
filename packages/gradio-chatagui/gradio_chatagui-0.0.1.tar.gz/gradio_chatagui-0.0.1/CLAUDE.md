# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a pure Gradio custom component called `gradio_chatagui` that implements an AG-UI (Agentic UI) chat interface. It provides a reusable chat UI component that can connect to any SSE-streaming backend for real-time AI agent conversations.

## Architecture

The project consists of two main parts:

1. **Backend Python Component** (`backend/gradio_chatagui/`):
   - `chatagui.py`: Main Gradio component class that handles frontend/backend communication
   - Lightweight component that passes through SSE streaming from external backends

2. **Frontend Svelte Component** (`frontend/`):
   - `Index.svelte`: Main chat UI with real-time streaming, tool execution, and chart rendering
   - Uses Server-Sent Events (SSE) for real-time communication with any compatible backend
   - Integrates Chart.js for dynamic chart rendering and marked for markdown parsing

3. **Demo Backend** (`demo_backend.py`):
   - Standalone FastAPI server with LangGraph agent integration for demonstration
   - Shows how to implement a compatible SSE backend for the component

4. **Demo Application** (`demo/`):
   - Simple Gradio app demonstrating the component usage

## Key Components

- **AG-UI Event System**: Custom event-driven architecture for streaming agent interactions
- **Tool Execution**: Supports both backend tools (executed on server) and frontend tools (require user interaction)
- **Chart Rendering**: Supports both pre-rendered images and dynamic Chart.js visualizations
- **Backend Agnostic**: Works with any SSE backend that implements the AG-UI event protocol

## Development Commands

### Component Development
```bash
# Install in development mode
pip install -e .
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Demo Backend (Optional)
```bash
# Install dependencies for demo backend
pip install fastapi uvicorn sse-starlette langchain-openai langgraph matplotlib

# Run the demo backend
python demo_backend.py
```

### Demo Application
```bash
cd demo
pip install -r requirements.txt
python app.py
```

### Building the Component
```bash
# Build the component for distribution
python -m build
```

## API Configuration

The component requires an `api_root` parameter to specify the backend API URL. Any compatible backend should provide these endpoints:

- `/run_agent`: Main SSE endpoint for agent execution (POST with JSON body)
- `/tool_result`: Endpoint for frontend tool results (POST)
- `/stream`: Alternative SSE endpoint (GET with run_id param)
- `/health`: Health check endpoint (GET)

## Environment Setup

- Component itself has no external dependencies beyond Gradio
- Demo backend requires OpenAI API key for LangGraph agent
- Frontend built with Svelte and integrates with Gradio's component system

## Usage

The component is designed to be backend-agnostic. You can use it with any SSE-streaming backend that implements the AG-UI event protocol.