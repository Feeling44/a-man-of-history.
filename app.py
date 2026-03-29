import streamlit as st
import google.generativeai as genai

# إعداد واجهة المستخدم
st.set_page_config(page_title="المؤرخ العليم", layout="wide")
st.title("📚 محراب الكتابة التاريخية")

# جلب المفتاح من الإعدادات السرية
api_key = st.sidebar.text_input("أدخل مفتاح API الخاص بك:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # وضع الـ Prompt الذي صغناه سوياً كتعليمات نظام
    system_instruction = """
    You are the 'Omniscient Historical Architect'. 
    Co-author ultra-realistic historical fiction in Formal Arabic and High-Register English.
    Focus on legal, financial, and psychological accuracy. No anachronisms.
    """
    
model = genai.GenerativeModel('gemini-3-pro-preview', system_instruction=system_instruction)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض المحادثة بملء الشاشة
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("ماذا تريد أن نكتب اليوم في سجلات التاريخ؟"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    st.info("الرجاء إدخال مفتاح API في القائمة الجانبية للبدء.")
    
