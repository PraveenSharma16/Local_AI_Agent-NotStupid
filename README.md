# NotStupid AI

NotStupid AI is a local AI-powered email assistant built using LangGraph, LangChain, and Ollama. The system retrieves unread emails directly from an IMAP mailbox, generates concise summaries, and displays them in a structured terminal interface with real-time performance metrics.

The project focuses on practical AI orchestration using local LLMs, tool-calling workflows, and lightweight automation without relying on cloud APIs.

---

## Features

* Retrieve latest unread emails from inbox
* Dynamic email retrieval (`latest mail`, `latest 3 mails`, etc.)
* Automatic summarization of email content
* Local LLM inference using Ollama
* LangGraph-based tool workflow
* Terminal-based interactive interface
* Real-time performance metrics
* Zero cloud dependency
* Configurable IMAP integration

---

## Tech Stack

| Component            | Technology    |
| -------------------- | ------------- |
| LLM Framework        | LangChain     |
| Workflow Engine      | LangGraph     |
| Local Inference      | Ollama        |
| Model                | Llama 3.2     |
| Email Retrieval      | imap-tools    |
| Language             | Python        |
| Environment Handling | python-dotenv |

---

## Project Structure

```bash
NotStupid-AI/
│
├── main.py
├── requirements.txt
├── .env.example
├── README.md
---

## Installation

Clone the repository:

```bash
git clone https://github.com/aryanjamwalzx/NotStupid-AI.git
cd NotStupid-AI
```


Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Ollama Setup

Install Ollama and pull the required model:

```bash
ollama pull llama3.2
```

Start Ollama locally before running the project.

---

## Environment Variables

Create a `.env` file in the root directory:

```env
IMAP_HOST=imap.gmail.com
IMAP_USER=your_email@gmail.com
IMAP_PASSWORD=your_app_password
```

For Gmail accounts, use an App Password instead of your actual password.

---

## Running the Application

```bash
python main.py
```

Example queries:

```text
latest mail
latest 3 unread emails
show latest 5 mails
```

---

## Sample Output

```text
-------------------------------------------------------

[1] 15+ Interview Calls with just 1 Resume Fix

From:
aditi@talent500.co

Date:
2026-05-07 13:31

Summary:
Boost your resume visibility and improve interview response rate.

-------------------------------------------------------
```

---

## Performance Metrics

The assistant tracks runtime performance metrics during execution:

* Total Requests
* Successful Requests
* Failed Requests
* Current Response Time
* Average Response Time
* Success Rate

Example:

```text
---------- PERFORMANCE METRICS ----------

Total Requests        : 12
Successful Requests   : 12
Failed Requests       : 0
Current Response Time : 1.8 sec
Average Response Time : 2.1 sec
Success Rate          : 100%
```

---

## Architecture Overview

```text
User Input
   ↓
LangGraph Workflow
   ↓
Tool Calling
   ↓
IMAP Mailbox Access
   ↓
Local LLM Processing
   ↓
Formatted AI Response
```

---

## Design Goals

This project was built with the following objectives:

* Practical local AI automation
* Lightweight orchestration
* Minimal latency
* Simple extensibility
* Recruiter-friendly architecture
* Real-world AI engineering workflow exposure

---

## Future Improvements

* Email categorization
* Priority detection
* AI-generated reply suggestions
* Vector memory integration
* Multi-agent workflow support
* Voice interaction
* Web dashboard

---

## Author

Parveen Sharma

Focused on building practical AI systems using LLM orchestration, local inference, automation workflows, and applied AI engineering.



---
