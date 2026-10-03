# 🤖 AI Personal Assistant

An AI-powered personal assistant built using **Python, Flask, Groq, and Hugging Face**. The application combines multiple AI capabilities into a single web interface, allowing users to interact with AI for **question answering, text summarization, image analysis, and image generation**.

The project demonstrates the integration of **Large Language Models (LLMs), Generative AI, Natural Language Processing, and Computer Vision** into a practical AI application.

---

## ✨ Features

### 💬 Question Answering

Ask natural-language questions and receive AI-generated responses using a Large Language Model.

### 📝 Text Summarization

Provide lengthy text and generate a concise summary while retaining the important information.

### 🖼️ Image Analysis

Provide an image and ask questions about it. The assistant can analyze the image and generate a response based on its visual content.

### 🎨 Image Generation

Generate images from natural-language prompts using a generative image model through **Hugging Face**.

### 🌐 Interactive Web Interface

A simple and user-friendly web interface built with **HTML, CSS, JavaScript, and Flask**.

---

# 🛠️ Tech Stack

## Programming Language

* **Python**

## Backend

* **Flask**
* **OpenAI-compatible API**
* **Groq API**

## AI / Machine Learning

* **Large Language Models (LLMs)**
* **Generative AI**
* **Natural Language Processing (NLP)**
* **Computer Vision**
* **Text Summarization**
* **Image Understanding**
* **Image Generation**
* **Hugging Face**

## Frontend

* **HTML5**
* **CSS3**
* **JavaScript**

## Tools & Platforms

* **Git**
* **GitHub**
* **VS Code**

---

# 📂 Project Structure

```text
AI-Personal-Assistant/
│
├── main.py
│
├── static/
│   └── style.css
│
├── templates/
│   └── index.html
│
├── Output/
│   ├── output.txt
│   ├── image_generated.jpeg
│
├── .gitignore
└── README.md
```

### 📄 File & Folder Description

| File / Folder          | Description                                                              |
| ---------------------- | ------------------------------------------------------------------------ |
| `main.py`              | Main Flask application containing the backend logic and AI functionality |
| `templates/index.html` | Frontend interface of the application                                    |
| `static/style.css`     | CSS styling for the web interface                                        |
| `Output/`              | Screenshots and output examples of the implemented AI features           |
| `.gitignore`           | Specifies files and folders that should not be committed to GitHub       |
| `README.md`            | Project documentation                                                    |

---

# ⚙️ How It Works

The application follows a simple **frontend → Flask backend → AI model/API → response** architecture.

```text
                         ┌──────────────────┐
                         │       User       │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  Web Interface   │
                         │    index.html    │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    Flask App     │
                         │     main.py      │
                         └────────┬─────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
       Question Answering   Text Summarization   Image Processing
              │                   │                   │
              └───────────────────┼───────────────────┘
                                  │
                     ┌────────────┴────────────┐
                     │                         │
                     ▼                         ▼
                Groq API                 Hugging Face
              LLM / AI Models          Generative Models
                     │                         │
                     └────────────┬────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   AI Response    │
                         └──────────────────┘
```

---

# 🚀 Getting Started

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/heerify15/AI-Personal-Assistant.git
```

Navigate to the project directory:

```bash
cd AI-Personal-Assistant
```

---

## 2️⃣ Create a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

Install the required Python packages:

```bash
pip install flask openai
```

---

# 🔑 API Configuration

This project uses external AI services, so API credentials are required.

### Groq API

Set your Groq API key as an environment variable.

For Windows PowerShell:

```powershell
$env:GROQ_API_KEY="your_groq_api_key"
```

### Hugging Face

```powershell
$env:HF_TOKEN="your_huggingface_token"
```

---

# ▶️ Run the Application

Start the Flask application:

```bash
python main.py
```

Once the server starts, open the following address in your browser:

```text
http://127.0.0.1:5000
```

---

# 📸 Output & Demonstration

The `Output` folder contains screenshots demonstrating the different capabilities of the AI Personal Assistant.

## 💬 Question Answering

The assistant accepts natural-language questions and generates AI-powered responses.

![Question Answering](Output/question_answering.png)

---

## 📝 Text Summarization

The assistant can process lengthy text and generate a concise summary.

![Text Summarization](Output/text_summarization.png)

---

## 🖼️ Image Analysis

The assistant can analyze an image and respond to questions based on its visual content.

![Image Analysis](Output/image_analysis.png)

---

## 🎨 Image Generation

The assistant can generate images from natural-language prompts using a generative AI model through Hugging Face.

![Image Generation](Output/image_generation.png)

> **Note:** Make sure these image filenames exactly match the files present inside the `Output` folder.

---

# 🧠 AI Capabilities

| Feature               | Technology / Concept | Purpose                             |
| --------------------- | -------------------- | ----------------------------------- |
| 💬 Question Answering | LLM + Groq           | Generates responses to user queries |
| 📝 Text Summarization | LLM + Groq           | Produces concise summaries          |
| 🖼️ Image Analysis    | Vision-capable AI    | Understands and analyzes images     |
| 🎨 Image Generation   | Hugging Face         | Generates images from text prompts  |

---

# 🔐 Security

API credentials should be stored securely using environment variables.

### ❌ Avoid

```python
client = OpenAI(
    api_key="YOUR_API_KEY"
)
```

### ✅ Recommended

```python
import os

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY")
)
```

For Hugging Face:

```python
import os

hf_token = os.getenv("HF_TOKEN")
```

Make sure the following are included in `.gitignore`:

```text
.env
```

---

# 🎯 Project Objective

The objective of this project is to build a practical **AI-powered personal assistant** that integrates multiple AI capabilities into a single web application.

This project provides hands-on experience with:

* Large Language Models
* Generative AI
* Natural Language Processing
* Computer Vision
* Image Generation
* API Integration
* Hugging Face
* Flask
* AI Application Development

---

# 📚 What I Learned

Through this project, I gained practical experience in:

* Integrating LLM APIs into Python applications
* Building AI-powered backend services using Flask
* Connecting frontend interfaces with AI backends
* Working with Hugging Face models
* Implementing text summarization
* Implementing image analysis
* Implementing AI image generation
* Managing API credentials securely
* Structuring an AI application for future expansion

---

# 👨‍💻 Author

## Heer Shah

**Computer Science & Engineering — AI/ML**

GitHub: **[@heerify15](https://github.com/heerify15)**

---

# ⭐ Support

If you find this project interesting or useful, consider giving the repository a **⭐ Star** on GitHub!
