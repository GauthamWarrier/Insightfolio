import streamlit as st
import PyPDF2
from openai import OpenAI

# ✅ Configure Groq's LLaMA3 via OpenAI-compatible client
client = OpenAI(
    api_key="",  # Make sure to keep this secure!
    base_url="https://api.groq.com/openai/v1"  # Groq endpoint
)

# 🎯 Streamlit App Config
st.set_page_config(page_title="⚡ Resume Q&A Chatbot (Groq AI)")
st.title("💬Resume Q&A using Groq’s LLaMA 3")
st.caption("Upload your resume and ask smart questions, powered by **Groq + LLaMA 3** 💡")

# 📄 Upload Resume
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
resume_text = ""

if uploaded_file:
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            resume_text += page.extract_text() + "\n"
        st.success("✅ Resume uploaded and processed!")
    except Exception as e:
        st.error(f"❌ Error reading PDF: {e}")

# ❓ Ask Questions
if resume_text:
    question = st.text_input("Ask a question about your resume:")
    if question:
        prompt = f"""
        You are a helpful assistant reviewing a resume.

        Resume:
        {resume_text}

        Question:
        "{question}"

        Please answer based only on the content of the resume. Be concise and helpful.
        """

        with st.spinner("Groq AI is thinking... ⚡"):
            try:
                response = client.chat.completions.create(
                    model="llama3-8b-8192",  # Groq’s LLaMA 3 model
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                answer = response.choices[0].message.content
                st.markdown("### 🧠 Answer")
                st.write(answer)
            except Exception as e:
                st.error(f"❌ Failed to get response from Groq AI: {e}")
