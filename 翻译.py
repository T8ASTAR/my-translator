import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# --- 1. 页面配置 (高颜值UI设置) ---
st.set_page_config(page_title="极简翻译官", page_icon="🌐", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #4A90E2; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 智能多模态翻译器")
st.caption("支持图片、PDF、文档直接上传翻译")

# --- 2. 配置 API ---
# 建议通过 Streamlit 的 Secrets 管理 Key，这里为了方便你测试先留空
api_key = st.sidebar.text_input("请输入你的 Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # --- 3. 文件上传 ---
    uploaded_file = st.file_uploader("上传图片或 PDF 文件", type=['png', 'jpg', 'jpeg', 'pdf'])

    if uploaded_file is not None:
        st.info("正在处理文件，请稍候...")
        
        try:
            # 准备翻译指令
            prompt = "你是一个专业的翻译官。请识别并翻译这个文件中的所有文字。如果是图片，请保持段落逻辑；如果是文档，请确保完整。翻译目标语言为：中文。"

            # 根据文件类型处理
            if uploaded_file.type == "application/pdf":
                # 处理 PDF
                content = [{"mime_type": "application/pdf", "data": uploaded_file.read()}]
            else:
                # 处理图片
                img = Image.open(uploaded_file)
                st.image(img, caption='已上传图片', use_container_width=True)
                content = [prompt, img]

            # 调用 AI
            if st.button("开始翻译"):
                with st.spinner('AI 正在深度解析中...'):
                    response = model.generate_content([prompt, uploaded_file] if uploaded_file.type == "application/pdf" else content)
                    
                    st.subheader("翻译结果")
                    st.markdown("---")
                    st.write(response.text)
                    st.success("翻译完成！")
        except Exception as e:
            st.error(f"出错了: {e}")
else:
    st.warning("请在左侧边栏输入 API Key 以开始使用。")