
import streamlit as st
from resume_parser import extract_text_from_file
from evaluator import evaluate_resume
from lang import get_translation

st.set_page_config(page_title="AI Résumé Evaluator", layout="wide")

# Language selection
lang_choice = st.sidebar.selectbox("🌐 Langue / Language", ["Français", "English"])
lang = "fr" if lang_choice == "Français" else "en"
t = get_translation(lang)

# Title
st.title(t["title"][lang])
st.markdown(t["subtitle"][lang])

# File uploader
uploaded_file = st.file_uploader(t["upload_prompt"][lang], type=["pdf", "txt"])

if uploaded_file:
    with st.spinner(t["extracting"][lang]):
        raw_text = extract_text_from_file(uploaded_file)
        if not raw_text.strip():
            st.error(t["error_no_text"][lang])
        else:
            st.subheader(t["text_preview"][lang])
            st.text_area("", raw_text, height=300)

            # Evaluation
            st.subheader(t["evaluation_title"][lang])
            score, suggestions = evaluate_resume(raw_text, lang)

            st.metric(t["score"][lang], f"{score}/100")
            st.markdown("### " + t["suggestions"][lang])
            for item in suggestions:
                st.write("- " + item)
else:
    st.info(t["upload_instruction"][lang])

# Footer
st.markdown("---")
st.markdown(t["footer"][lang] + " · [GitHub](https://github.com/mahdidrm)")
