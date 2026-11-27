# 🎓 EduMind AI Tutor

An intelligent, multi-modal AI tutoring web application powered by **Groq** and Meta's **Llama** models. EduMind assists students across any academic subject through conversational tutoring, PDF textbook analysis, diagram interpretation, and interactive quiz generation.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45+-red.svg)
![Groq](https://img.shields.io/badge/Powered%20by-Groq%20Ultra--Fast%20Inference-orange.svg)

---

## 👥 Group 1 Members
1. **Vishav Bhan Singh Parmar**
2. **Adarsh Sharma**
3. **Mayank Singh Pathania**
4. **Dinesh Mandela**
5. **Saksham Neb**

---

## ✨ Features
- **📄 PDF Textbook & Document Analysis**: Upload PDFs to automatically extract content and ask targeted questions.
- **🖼️ Diagram & Image Understanding**: Upload scientific charts, formulas, geometry problems, and diagrams for multi-modal analysis.
- **💬 Smart Conversational Tutor**: Socratic tutoring style providing clear, structured explanations, step-by-step logic, and bullet points.
- **✏️ Manual Study Notes**: Paste lecture notes, formulas, or homework questions directly.
- **🧠 Flexible AI Models**: Choose between `llama-3.3-70b-versatile`, `llama-3.1-8b-instant`, `llama-3.2-11b-vision-preview`, and more with automatic vision routing.
- **🎨 Modern Dark Gradient UI**: Responsive, sleek design with interactive badges, shimmer animations, and quick-start starter prompts.

---

## 🚀 Quick Start (Local Run)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Groq API Key
You can obtain a free API key at [console.groq.com](https://console.groq.com).

Configure your key using **any** of the following methods:
- **Directly in UI**: Type or paste it in the sidebar inside the app (persists automatically).
- **Environment Variable**:
  ```powershell
  # Windows PowerShell:
  $env:GROQ_API_KEY="gsk_your_key_here"
  ```
  ```bash
  # Linux / macOS:
  export GROQ_API_KEY="gsk_your_key_here"
  ```
- **`.env` File**: Copy `.env.example` to `.env` and paste your key.
- **`api_key.txt`**: Place your key inside `api_key.txt`.

### 3. Launch the Application
Run via Streamlit or Python directly:
```bash
# Option A:
streamlit run app.py

# Option B:
python edumind_ai_tutor.py
```

The application will start at `http://localhost:8501`.

---

## 📁 Project Structure
```
d:/ai_tutor/
│
├── edumind_ai_tutor.py        # Core application logic & UI
├── app.py                     # Streamlit entrypoint
├── requirements.txt           # Project dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore file
├── README.md                  # Project documentation
│
└── GEN-AI-PROJECT-main/       # Original notebook archive
    ├── AI_Tutor.ipynb         # Google Colab notebook
    └── README.md
```

---

## 🛠️ Technologies Used
- **Streamlit**: Interactive web UI framework.
- **Groq API**: High-speed LLM inference.
- **Meta Llama Models**: Llama 3.3 70B Versatile, Llama 3.1 8B, Llama 3.2 11B Vision.
- **PyMuPDF (`fitz`)**: Fast PDF text extraction.
- **Pillow (`PIL`)**: Image processing and multimodal preparation.
- **Python-dotenv**: Environment configuration.
