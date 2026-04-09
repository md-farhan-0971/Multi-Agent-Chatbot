# Multi-Agent-Chatbot
A Multi-Agent Chatbot is an AI system where multiple specialized agents collaborate to handle tasks. Each agent performs a specific role, such as answering queries, processing data, or managing workflows, enabling more accurate, efficient, and scalable conversations compared to single-agent chatbots.

# 🤖 Agent Ecosystem • AI Workspace

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-FF4B4B.svg)
![Gemini](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-8A2BE2.svg)
![UI/UX](https://img.shields.io/badge/UI%2FUX-Glassmorphism-00E5FF.svg)

An enterprise-grade, multi-agent AI workspace built with Python and Streamlit, powered by the Google Gemini API. This project goes beyond standard chatbot templates by implementing advanced session state management, multimodal file processing, and a custom-engineered UI that bypasses default framework limitations to deliver a seamless, high-performance user experience.

---

## ✨ Key Features & Engineering Highlights

### 1. Specialized Agent Routing
Instead of a generic LLM wrapper, the system utilizes a dynamic persona-routing engine. Users can instantly switch contexts between:
* **🛠️ Code Agent:** Strict focus on highly efficient, bug-free software engineering and architecture.
* **🛠️ Research Agent:** Factual, detailed, and analytical data retrieval.
* **🛠️ Writing Agent:** Creative, structured, and engaging copywriting.
* **🛠️ QA / Review Agent:** Strict critique, logical flaw detection, and optimization suggestions.

### 2. Advanced State Management (Edit & Regenerate)
Built a custom CRUD (Create, Read, Update, Delete) flow for chat history that overcomes standard Streamlit limitations:
* **Clunk-Free Editing:** Users can edit previous prompts inline through a dedicated editing container.
* **State Truncation:** The system intelligently slices the session state array to remove orphaned conversational branches.
* **Automatic Regeneration:** Automatically triggers the AI to generate a fresh response based on the newly edited historical context, maintaining perfect conversational continuity.

### 3. Multimodal Data Pipeline
Fully integrated with generative AI vision and document capabilities:
* **Native File Handling:** Processes `.pdf`, `.csv`, `.txt`, `.png`, and `.jpg` directly in the chat stream.
* **Tempfile Management:** Securely handles binary streams and visual data via Python's `PIL` and `tempfile` libraries before piping them into the LLM context window.

### 4. Enterprise-Grade UI/UX (CSS Injection)
Overhauled Streamlit's native DOM using raw CSS injection to create an immersive, fluid workspace:
* **Glassmorphism & Depth:** Implemented frosted glass effects, dynamic shadows, and layered z-indexing.
* **Animated Aesthetics:** Features a subtle, breathing radial gradient background and interactive, glowing input fields on focus.
* **Component Overrides:** Completely restyled native buttons, popovers, and text areas into cohesive, gradient-mapped interactive elements, matching top-tier industry design standards.

---

## 🏗️ System Architecture

1. **Frontend:** Streamlit (Python) + Custom injected HTML/CSS.
2. **State Layer:** Streamlit `session_state` managing chat histories, active editing indexes, and simulated database logs.
3. **LLM Engine:** Google Generative AI (`gemini-2.5-flash`) handling complex reasoning and multimodal payloads.
4. **File Processing:** `Pillow` for image buffering, Python `tempfile` for rapid PDF/document ingestion.

---

## 🚀 Installation & Setup

### Prerequisites
* Python 3.9 or higher
* A Google Gemini API Key ([Get one here](https://aistudio.google.com/app/apikey))

### 1. Clone the repository
```bash
git clone [https://github.com/yourusername/agent-ecosystem.git](https://github.com/yourusername/agent-ecosystem.git)
cd agent-ecosystem

### Install dependencies

pip install streamlit google-generativeai pillow

### Configure API Key

# --- 1. API CONFIGURATION (REQUIRED) ---
GOOGLE_API_KEY = "YOUR_ACTUAL_API_KEY_HERE"

### Run the Application

streamlit run app.py

### Usage Guide

Enter the Workspace: Provide a username on the welcome screen to initialize your session.

Select an Agent: Use the top-right control panel to select the appropriate AI persona for your task.

Attach Context: Click the ➕ Attach popover to upload documents or images before sending your prompt.

Edit History: Click the ✎ icon next to any of your past messages to enter editing mode. The system will automatically truncate the old response and generate a new one based on your update.

Audit Logs: Click the 📜 History button in the top navigation bar to view the interactive simulated session audit panel.


