import streamlit as st
from openai import OpenAI  # DeepSeek 兼容 OpenAI 格式
import pypdfium2 as pdfium
from PIL import Image

# --- 页面配置 ---
st.set_page_config(page_title="智能翻译官", page_icon="🇨🇳", layout="wide")

# 注入一点自定义 CSS 让界面更像高级国产软件
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .main-card { border-radius: 15px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 极简 AI 翻译")
st.info("基于国产 DeepSeek 模型，国内直接秒开")

# --- 侧边栏配置 ---
with st.sidebar:
    st.header("设置")
    api_key = st.text_input("输入 DeepSeek API Key:", type="password")
    target_lang = st.selectbox("目标语言", ["中文", "英文", "日语", "韩语"], index=0)

# --- 核心翻译逻辑 ---
def deepseek_translate(text, target_lang, api_key):
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": f"你是一个专业的翻译官，请将以下内容翻译成{target_lang}。保持原有的语气和排版。"},
            {"role": "user", "content": text},
        ],
        stream=False
    )
    return response.choices[0].message.content

# --- 界面交互 ---
if api_key:
    tab1, tab2 = st.tabs(["📄 文档/PDF 翻译", "✍️ 文本翻译"])

    with tab1:
        uploaded_file = st.file_uploader("点击上传 PDF 或图片", type=['pdf', 'png', 'jpg'])
        if uploaded_file:
            content = ""
            if uploaded_file.type == "application/pdf":
                # PDF 解析
                pdf = pdfium.PdfDocument(uploaded_file)
                for page in pdf:
                    textpage = page.get_textpage()
                    content += textpage.get_text_range()
            else:
                # 图片直接提醒（因为 OCR 需要额外服务器资源，建议先做 PDF 和文字）
                st.warning("图片识别建议直接复制文字到‘文本翻译’栏。")
            
            if content and st.button("开始解析并翻译"):
                with st.spinner("DeepSeek 正在思考中..."):
                    result = deepseek_translate(content[:4000], target_lang, api_key) # 限制长度防止溢出
                    st.subheader("翻译结果")
                    st.write(result)

    with tab2:
        input_text = st.text_area("粘贴需要翻译的原文:", height=200)
        if st.button("立即翻译"):
            if input_text:
                with st.spinner("翻译中..."):
                    result = deepseek_translate(input_text, target_lang, api_key)
                    st.success("翻译成功！")
                    st.write(result)
else:
    st.warning("👈 请先在左侧输入 DeepSeek API Key 才能开始工作。")
