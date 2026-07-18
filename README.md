# Soni

A fully local AI Assistant built with Python.

## Features

- Offline Speech Recognition (Faster Whisper)
- Offline LLM (Ollama)
- Offline Text-to-Speech (Piper)
- Tool-based AI Agent
- File Search
- File Reader
- Open Applications
- Session Context
- Semantic Memory
- Modular Tool Registry

## Architecture

User
↓
LLM Planner
↓
Tool Executor
↓
Python Tool
↓
Response / LLM