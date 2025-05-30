import streamlit as st
from resume_parser import extract_text_from_file, extract_resume_data
from lang import get_translation

st.set_page_config(page_title="Résumé Analyzer", layout="wide")

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
    text = extract_text_from_file(uploaded_file)
    
    if not text.strip():
        st.error(t["error_no_text"][lang])
    else:
        st.subheader(t["text_preview"][lang])
        st.text_area("", text, height=250)

        # Extract structured data
        resume_data = extract_resume_data(text)

        # Contact Info
        st.subheader("Contact Info")
        contact = resume_data.get("contact", {})
        if contact:
            st.write(pd.DataFrame([contact]))
        else:
            st.write("No contact information found.")

        # Skills
        st.subheader("Skills")
        skills = resume_data.get("skills", [])
        if skills:
            st.table(pd.DataFrame(skills, columns=["Skill"]))
        else:
            st.write("No skills detected.")

        # Education
        st.subheader("Education")
        education = resume_data.get("education", [])
        if education:
            st.table(pd.DataFrame(education, columns=["Entry"]))
        else:
            st.write("No education section found.")

        # Experience
        st.subheader("Experience")
        experience = resume_data.get("experience", [])
        if experience:
            st.table(pd.DataFrame(experience, columns=["Entry"]))
        else:
            st.write("No experience section found.")

        # Warnings
        st.subheader("Structure Feedback")
        for w in resume_data.get("structure_warnings", []):
            st.warning(w)
else:
    st.info(t["upload_instruction"][lang])

# Footer
st.markdown("---")
st.markdown(t["footer"][lang] + " · [GitHub](https://github.com/mahdidrm)")
