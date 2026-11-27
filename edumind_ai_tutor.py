import streamlit as st
import os
import base64
import sys
from dotenv import load_dotenv

# Try importing PyMuPDF with modern and legacy fallbacks
try:
    import pymupdf as fitz
except ImportError:
    try:
        import fitz
    except ImportError:
        fitz = None

# Try importing Groq
try:
    from groq import Groq
except ImportError:
    Groq = None

# ---------------------------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="EduMind AI Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------------------------
# Styling & Theme
# ---------------------------------------------------------------------------
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*='css'] { font-family: 'Inter', sans-serif; }

@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes shimmer {
    0% { background-position: -200% center; }
    100% { background-position: 200% center; }
}
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
}
@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4); }
    50% { box-shadow: 0 0 0 10px rgba(99, 102, 241, 0); }
}

.hero-title {
    font-size: 2.8rem;
    font-weight: 700;
    text-align: center;
    background: linear-gradient(135deg, #6366f1, #8b5cf6, #06b6d4);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: fadeSlideIn 0.8s ease, shimmer 4s linear infinite;
    margin-bottom: 0.2rem;
}
.hero-sub {
    text-align: center;
    color: #94a3b8;
    font-size: 1.05rem;
    animation: fadeSlideIn 1s ease;
    margin-bottom: 1.5rem;
}
.feature-card {
    background: linear-gradient(135deg, #1e1b4b, #312e81);
    border: 1px solid rgba(99, 102, 241, 0.35);
    border-radius: 14px;
    padding: 1.1rem 0.8rem;
    text-align: center;
    animation: fadeSlideIn 1.1s ease, float 5s ease-in-out infinite;
    color: white;
    margin-bottom: 0.8rem;
    transition: transform 0.2s ease;
}
.feature-card:hover {
    transform: translateY(-3px);
    border-color: rgba(99, 102, 241, 0.6);
}
.feature-card h3 { font-size: 1.5rem; margin: 0; }
.feature-card p { color: #c7d2fe; font-size: 0.88rem; margin: 0.35rem 0 0; }

.chat-bubble-user {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    padding: 0.95rem 1.25rem;
    border-radius: 18px 18px 4px 18px;
    margin: 0.6rem 0;
    max-width: 82%;
    margin-left: auto;
    animation: fadeSlideIn 0.3s ease;
    font-size: 0.95rem;
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.25);
}
.chat-bubble-ai {
    background: rgba(30, 27, 75, 0.85);
    border: 1px solid rgba(99, 102, 241, 0.3);
    color: #f1f5f9;
    padding: 1rem 1.3rem;
    border-radius: 18px 18px 18px 4px;
    margin: 0.6rem 0;
    max-width: 88%;
    animation: fadeSlideIn 0.3s ease;
    font-size: 0.95rem;
    line-height: 1.65;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
}
.upload-zone {
    border: 2px dashed rgba(99, 102, 241, 0.45);
    border-radius: 14px;
    padding: 1rem;
    text-align: center;
    background: rgba(99, 102, 241, 0.05);
    margin-bottom: 1rem;
    color: #cbd5e1;
}
.context-badge {
    background: rgba(6, 182, 212, 0.15);
    border: 1px solid rgba(6, 182, 212, 0.45);
    border-radius: 20px;
    padding: 0.25rem 0.75rem;
    font-size: 0.8rem;
    color: #38bdf8;
    display: inline-block;
    margin: 0.2rem;
}
.api-key-box {
    background: rgba(30, 27, 75, 0.6);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1.2rem;
}
.stButton>button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}
.stButton>button:hover {
    box-shadow: 0 4px 14px rgba(99, 102, 241, 0.45) !important;
    transform: translateY(-1px) !important;
}
[data-testid='stAppViewContainer'] {
    background: linear-gradient(160deg, #0f0c29, #1a1040, #0f0c29);
}
[data-testid='stSidebar'] {
    background: rgba(15, 12, 41, 0.96) !important;
    border-right: 1px solid rgba(99, 102, 241, 0.2);
}
label, .stMarkdown p, .stMarkdown li {
    color: #cbd5e1 !important;
}
</style>""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# API Key Resolution
# ---------------------------------------------------------------------------
load_dotenv()

def resolve_api_key():
    """Retrieve Groq API key from session state, environment, or file."""
    # 1. Session state
    if st.session_state.get("groq_api_key"):
        return st.session_state["groq_api_key"].strip()
    # 2. Environment variable
    env_key = os.environ.get("GROQ_API_KEY", "").strip()
    if env_key:
        return env_key
    # 3. api_key.txt file
    if os.path.exists("api_key.txt"):
        try:
            with open("api_key.txt", "r", encoding="utf-8") as f:
                k = f.read().strip()
                if k:
                    return k
        except Exception:
            pass
    return ""

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []
if "context_text" not in st.session_state:
    st.session_state.context_text = ""
if "context_names" not in st.session_state:
    st.session_state.context_names = []
if "image_b64" not in st.session_state:
    st.session_state.image_b64 = []
if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = resolve_api_key()

# ---------------------------------------------------------------------------
# Sidebar UI
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    
    current_key = resolve_api_key()
    api_key_input = st.text_input(
        "🔑 Groq API Key",
        value=current_key,
        type="password",
        placeholder="gsk_...",
        help="Get your free API key at console.groq.com"
    )
    
    if api_key_input != current_key:
        st.session_state.groq_api_key = api_key_input
        # Save to api_key.txt for persistence
        if api_key_input.strip():
            try:
                with open("api_key.txt", "w", encoding="utf-8") as f:
                    f.write(api_key_input.strip())
            except Exception:
                pass
        st.rerun()

    if not current_key:
        st.warning("⚠️ Enter your Groq API Key above to start. [Get one free](https://console.groq.com)")

    # Model Selection
    st.markdown("### 🧠 AI Model")
    available_models = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "llama-3.2-11b-vision-preview",
        "llama-3.2-90b-vision-preview",
        "meta-llama/llama-4-scout-17b-16e-instruct"
    ]
    
    # Auto-recommend vision model if images are loaded
    default_index = 0
    if st.session_state.image_b64:
        default_index = 2  # llama-3.2-11b-vision-preview
    
    selected_model = st.selectbox(
        "Choose Model",
        available_models,
        index=default_index,
        help="Llama 3.3 70B is recommended for text tutoring; Llama 3.2 11B Vision is recommended for images."
    )

    st.markdown("---")
    st.markdown("## 📂 Study Material")
    st.markdown('<div class="upload-zone">Upload documents or images to give context to your AI tutor</div>', unsafe_allow_html=True)

    # PDF Uploader
    pdf_files = st.file_uploader("📄 Upload PDF(s)", type=["pdf"], accept_multiple_files=True)
    if pdf_files:
        for pdf in pdf_files:
            if pdf.name not in st.session_state.context_names:
                if fitz is not None:
                    try:
                        doc = fitz.open(stream=pdf.read(), filetype="pdf")
                        text = "".join(page.get_text() for page in doc)
                        st.session_state.context_text += f"\n\n[PDF: {pdf.name}]\n{text}"
                        st.session_state.context_names.append(pdf.name)
                        st.success(f"Loaded: {pdf.name}")
                    except Exception as e:
                        st.error(f"Error reading {pdf.name}: {e}")
                else:
                    st.error("PyMuPDF (fitz) is not installed. PDF extraction unavailable.")

    # Image Uploader
    img_files = st.file_uploader("🖼️ Upload Image(s)", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=True)
    if img_files:
        for img in img_files:
            if img.name not in st.session_state.context_names:
                try:
                    raw = img.read()
                    mime = getattr(img, "type", "image/jpeg") or "image/jpeg"
                    b64 = base64.b64encode(raw).decode("utf-8")
                    st.session_state.image_b64.append((mime, b64))
                    st.session_state.context_names.append(img.name)
                    st.image(raw, caption=img.name, use_container_width=True)
                    st.success(f"Loaded: {img.name}")
                except Exception as e:
                    st.error(f"Error reading {img.name}: {e}")

    # Manual Study Notes
    st.markdown("### ✏️ Paste Study Notes")
    manual_text = st.text_area("", placeholder="Paste textbook excerpts, definitions, formulas, or homework problems...", height=130)
    if st.button("➕ Add Notes to Context"):
        if manual_text.strip():
            snippet = f"\n\n[Study Notes]\n{manual_text.strip()}"
            st.session_state.context_text += snippet
            label = f"Notes ({len(manual_text.strip().split())} words)"
            st.session_state.context_names.append(label)
            st.success("✅ Notes added to context!")
            st.rerun()

    # Active Context Display
    if st.session_state.context_names:
        st.markdown("### 📌 Active Context")
        badges = "".join(f'<span class="context-badge">📌 {n}</span>' for n in st.session_state.context_names)
        st.markdown(badges, unsafe_allow_html=True)
        total_chars = len(st.session_state.context_text)
        if total_chars > 0:
            st.caption(f"Total context text size: ~{total_chars:,} characters")

    # Clear Context Button
    if st.button("🗑️ Clear All Context & Chat"):
        st.session_state.context_text = ""
        st.session_state.context_names = []
        st.session_state.messages = []
        st.session_state.image_b64 = []
        st.rerun()

    st.markdown("---")
    st.markdown("<p style='text-align:center;color:#64748b;font-size:0.78rem;'>👥 <b>Group 1</b><br>Vishav Bhan Singh Parmar • Adarsh Sharma<br>Mayank Singh Pathania • Dinesh Mandela • Saksham Neb</p>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Main Content
# ---------------------------------------------------------------------------
st.markdown('<div class="hero-title">🎓 EduMind AI Tutor</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Upload anything. Ask anything. Learn everything across science, math, history & more.</div>', unsafe_allow_html=True)

# Feature Badges
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown('<div class="feature-card"><h3>📄</h3><p>PDF Study Material</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="feature-card"><h3>🖼️</h3><p>Diagram & Image Analysis</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="feature-card"><h3>💬</h3><p>Smart Tutoring Chat</p></div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="feature-card"><h3>📚</h3><p>All Subjects Covered</p></div>', unsafe_allow_html=True)

st.markdown("---")

# Quick Prompt Suggestions (if chat is empty)
if not st.session_state.messages:
    st.markdown("#### 💡 Quick Prompts to Get Started:")
    qp1, qp2, qp3, qp4 = st.columns(4)
    prompt_to_send = None
    with qp1:
        if st.button("📐 Pythagoras Theorem"):
            prompt_to_send = "Explain the Pythagorean theorem with real-world examples and step-by-step problem solutions."
    with qp2:
        if st.button("🧪 Photosynthesis"):
            prompt_to_send = "Explain the process of photosynthesis, light-dependent and dark reactions, simply."
    with qp3:
        if st.button("📝 Summarize Material"):
            prompt_to_send = "Please summarize the key takeaways, definitions, and concepts from my uploaded study material."
    with qp4:
        if st.button("❓ Quiz Me"):
            prompt_to_send = "Create a 5-question interactive quiz based on my study material with multiple choice options."

    if prompt_to_send:
        st.session_state.messages.append({"role": "user", "content": prompt_to_send})
        st.rerun()

# Display Chat History
st.markdown("## 💬 Chat with EduMind")
for msg in st.session_state.messages:
    if msg["role"] == "user":
        content = msg["content"] if isinstance(msg["content"], str) else "[Multimodal Query]"
        st.markdown(f'<div class="chat-bubble-user">🧑‍🎓 <b>You:</b><br>{content}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bubble-ai">🎓 <b>EduMind Tutor:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Chat Input & Response Handling
# ---------------------------------------------------------------------------
user_question = st.chat_input("Ask a question about your study material or any subject...")

# Also handle prompt triggered by quick suggestions
if not user_question and st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    user_question = st.session_state.messages[-1]["content"]
    is_followup = False
else:
    is_followup = True

if user_question:
    # If it's a new input from chat_input, append to messages
    if is_followup:
        st.session_state.messages.append({"role": "user", "content": user_question})
        st.markdown(f'<div class="chat-bubble-user">🧑‍🎓 <b>You:</b><br>{user_question}</div>', unsafe_allow_html=True)

    api_key = resolve_api_key()
    if not api_key:
        error_msg = "Please configure your Groq API key in the sidebar to enable EduMind AI Tutor responses."
        st.session_state.messages.append({"role": "assistant", "content": f"⚠️ {error_msg}"})
        st.error(error_msg)
    else:
        system_msg = {
            "role": "system",
            "content": (
                "You are EduMind, an expert, patient, and encouraging AI tutor for students across ALL subjects "
                "(science, mathematics, computer science, history, law, engineering, literature, and arts). "
                "Provide clear, structured explanations with intuitive analogies, step-by-step reasoning, and bullet points. "
                "If study material or images are provided in the context, reference them accurately and specifically."
            )
        }

        # Build context section
        context_section = ""
        if st.session_state.context_text.strip():
            truncated_context = st.session_state.context_text[:14000]
            context_section = f"\n\n--- UPLOADED STUDY MATERIAL ---\n{truncated_context}\n--- END STUDY MATERIAL ---"

        # Check if multimodal (images) is used
        has_images = bool(st.session_state.image_b64)
        active_model = selected_model
        
        # If user selected a text-only model but uploaded images, automatically switch to vision model
        if has_images and "vision" not in active_model.lower() and "scout" not in active_model.lower():
            active_model = "llama-3.2-11b-vision-preview"

        # Prepare user message content
        if has_images:
            user_content = []
            for mime, b64 in st.session_state.image_b64:
                user_content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:{mime};base64,{b64}"}
                })
            user_content.append({
                "type": "text",
                "text": f"{context_section}\n\nQuestion: {user_question}"
            })
        else:
            user_content = f"{context_section}\n\nQuestion: {user_question}"

        # Build chat history (limit to last 6 messages for context economy)
        chat_history = [system_msg]
        for m in st.session_state.messages[-7:-1]:
            # Convert any non-string content in history to string for compatibility
            c = m["content"]
            if not isinstance(c, str):
                c = str(c)
            chat_history.append({"role": m["role"], "content": c})
        
        chat_history.append({"role": "user", "content": user_content})

        with st.spinner(f"🧠 EduMind is thinking with {active_model}..."):
            answer = ""
            try:
                client = Groq(api_key=api_key)
                response = client.chat.completions.create(
                    model=active_model,
                    messages=chat_history,
                    max_tokens=2048,
                    temperature=0.7
                )
                answer = response.choices[0].message.content
            except Exception as e:
                err_str = str(e)
                # Fallback to standard text model if custom or vision model failed
                if ("model" in err_str.lower() or "not_found" in err_str.lower()) and active_model != "llama-3.3-70b-versatile":
                    try:
                        fallback_model = "llama-3.3-70b-versatile"
                        # Strip images for fallback if needed
                        fallback_content = f"{context_section}\n\nQuestion: {user_question}"
                        fallback_history = [system_msg]
                        for m in st.session_state.messages[-7:-1]:
                            fallback_history.append({"role": m["role"], "content": str(m["content"])})
                        fallback_history.append({"role": "user", "content": fallback_content})
                        
                        fb_response = client.chat.completions.create(
                            model=fallback_model,
                            messages=fallback_history,
                            max_tokens=2048,
                            temperature=0.7
                        )
                        answer = f"*(Note: Handled with fallback model {fallback_model})*\n\n" + fb_response.choices[0].message.content
                    except Exception as fb_err:
                        answer = f"⚠️ Groq API Error: {err_str}\n\nPlease verify your API key and model selection."
                else:
                    answer = f"⚠️ Groq API Error: {err_str}\n\nPlease check your API key, connection, or quota at console.groq.com."

            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#64748b;font-size:0.85rem;'>"
    "🎓 EduMind AI Tutor • Powered by Groq Ultra-Fast Inference • Built with Streamlit"
    "</p>",
    unsafe_allow_html=True
)

# ---------------------------------------------------------------------------
# Direct Execution Support
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        from streamlit.web import cli as stcli
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx() is None:
            # Script was run directly with 'python edumind_ai_tutor.py'
            print("🚀 Launching EduMind AI Tutor via Streamlit...")
            sys.argv = ["streamlit", "run", sys.argv[0]] + sys.argv[1:]
            sys.exit(stcli.main())
    except Exception:
        pass
