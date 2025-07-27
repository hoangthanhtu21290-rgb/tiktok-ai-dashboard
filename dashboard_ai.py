import streamlit as st
from openai import OpenAI  # Phiên bản mới
import google.generativeai as genai
from anthropic import Anthropic
from dotenv import load_dotenv
import os
import requests

# Tải biến môi trường từ .env
load_dotenv()

# Cấu hình Streamlit
st.set_page_config(
    page_title="DASHBOARD ĐA NĂNG",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Giao diện tối
DARK_THEME = """
<style>
    :root {
        --primary-bg: #1E1E1E;
        --secondary-bg: #2D2D2D;
        --text-color: #E0E0E0;
    }
    body, .stApp {
        background-color: var(--primary-bg);
        color: var(--text-color);
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background: var(--secondary-bg);
        color: var(--text-color);
        border: 1px solid #444;
    }
    .stButton>button {
        background: #4A90E2;
        color: white;
        border: none;
        border-radius: 5px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background: #3a7bc8 !important;
    }
    .stTab {
        background: var(--secondary-bg) !important;
    }
</style>
"""
st.markdown(DARK_THEME, unsafe_allow_html=True)

# ====== Khởi tạo clients ======
openai_client = OpenAI(api_key=os.getenv("OPENAI_KEY"))  # Phiên bản mới
genai.configure(api_key=os.getenv("GEMINI_KEY"))
claude_client = Anthropic(api_key=os.getenv("CLAUDE_KEY"))
pexels_key = os.getenv("PEXELS_KEY")

# ====== Giao diện Sidebar ======
st.sidebar.header("🔑 QUẢN LÝ API KEYS")
openai_key = st.sidebar.text_input("OpenAI Key", value=os.getenv("OPENAI_KEY", ""), type="password")
gemini_key = st.sidebar.text_input("Gemini Key", value=os.getenv("GEMINI_KEY", ""), type="password")
claude_key = st.sidebar.text_input("Claude Key", value=os.getenv("CLAUDE_KEY", ""), type="password")
pexels_key = st.sidebar.text_input("Pexels Key", value=pexels_key or "", type="password")

if st.sidebar.button("💾 Lưu cài đặt"):
    os.environ["OPENAI_KEY"] = openai_key
    os.environ["GEMINI_KEY"] = gemini_key
    os.environ["CLAUDE_KEY"] = claude_key
    os.environ["PEXELS_KEY"] = pexels_key
    st.success("Đã lưu API keys!")

# ====== Tabs chính ======
tab1, tab2, tab3, tab4 = st.tabs(["GPT-4", "Gemini", "Claude", "Pexels Images"])

with tab1:
    st.header("🧠 OpenAI GPT-4")
    prompt = st.text_area("Nhập nội dung...", height=150, key="gpt_input")
    if st.button("🚀 Gửi yêu cầu", key="gpt_btn"):
        if not openai_client.api_key:
            st.error("Vui lòng nhập OpenAI Key!")
        else:
            with st.spinner("Đang xử lý..."):
                try:
                    response = openai_client.chat.completions.create(
                        model="gpt-4-turbo-preview",  # Đã sửa cú pháp
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.markdown(f"```markdown\n{response.choices[0].message.content}\n```")
                except Exception as e:
                    st.error(f"Lỗi: {str(e)}")  
with tab2:
    st.header("🌐 Google Gemini")
    question = st.text_input("Nhập câu hỏi...", key="gemini_input")
    if st.button("🚀 Gửi yêu cầu", key="gemini_btn"):
        if not gemini_key:
            st.error("Vui lòng nhập Gemini Key!")
        else:
            try:
                genai.configure(api_key=gemini_key)
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(question)
                st.code(response.text, language="markdown")
            except Exception as e:
                st.error(f"Lỗi: {str(e)}")

with tab3:
    st.header("🎭 Anthropic Claude")
    query = st.text_area("Nhập tin nhắn...", height=150, key="claude_input")
    if st.button("🚀 Gửi yêu cầu", key="claude_btn"):
        if not claude_client.api_key:
            st.error("Vui lòng nhập Claude Key!")
        else:
            try:
                message = claude_client.messages.create(
                    model="claude-3-opus-20240229",
                    max_tokens=1000,
                    messages=[{"role": "user", "content": query}]
                )
                st.success(message.content[0].text)
            except Exception as e:
                st.error(f"Lỗi: {str(e)}")

with tab4:
    st.header("📷 Tìm ảnh Pexels")

    def search_pexels(query, api_key):
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=10"
        headers = {"Authorization": api_key}
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.json().get("photos", [])
        return []

    search_term = st.text_input("Từ khóa tìm ảnh (ví dụ: sad, happy, nature)")
    if st.button("🔍 Tìm kiếm") and pexels_key:
        images = search_pexels(search_term, pexels_key)
        if images:
            cols = st.columns(3)
            for i, img in enumerate(images[:6]):
                with cols[i % 3]:
                    st.image(img["src"]["medium"], use_column_width=True, caption=f"Photo by {img['photographer']}")
        else:
            st.warning("Không tìm thấy ảnh phù hợp!")

# ====== Hướng dẫn ======
with st.expander("ℹ️ HƯỚNG DẪN CÀI ĐẶT", expanded=False):
    st.markdown("""
    1. **Cài đặt thư viện**:
       ```bash
       pip install streamlit openai google-generativeai anthropic python-dotenv requests
       ```
    2. **Tạo file `.env`** trong cùng thư mục:
       ```env
       OPENAI_KEY="sk-cua-ban"
       GEMINI_KEY="gemini-cua-ban"
       CLAUDE_KEY="sk-ant-cua-ban"
       PEXELS_KEY="pexels-cua-ban"
       ```
    3. **Chạy ứng dụng**:
       ```bash
       streamlit run dashboard_ai.py
       ```
    """)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Mẹo**: Nhấn `R` để reload trang khi có lỗi!")