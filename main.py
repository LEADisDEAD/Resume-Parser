import unittest

from docx import Document

import re
import spacy
from spacy.matcher import Matcher
from pdfminer.high_level import extract_text as extract_pdf_text
import streamlit as st

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_file):
    return extract_pdf_text(pdf_file)

def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_txt(txt_path):
    with open(txt_path, 'r') as file:
        return file.read()
def extract_contact_number(text):
    pattern = r"\+?\(?\d{1,4}\)?[-.\s]?\(?\d{1,4}\)?[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}"
    match = re.search(pattern, text)
    return match.group() if match else None

def extract_email(text):
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    return match.group() if match else None

def extract_skills(text, skills_list):
    skills = []
    for skill in skills_list:
        pattern = r"\b{}\b".format(re.escape(skill))
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            skills.append(skill)
    return skills

def extract_education(text):
    education = []
    keywords = [
        # Undergraduate
        "BTech", "B.Tech", "B.E", "BE", "Bachelor of Technology", "Bachelor of Engineering",
        "BSc", "B.Sc", "Bachelor of Science",
        "BCA", "Bachelor of Computer Applications",
        "BBA", "Bachelor of Business Administration",
        "B. Pharmacy", "B Pharmacy", "B.Pharm",

        # Postgraduate
        "MTech", "M.Tech", "ME", "M.E", "Master of Technology", "Master of Engineering",
        "MSc", "M.Sc", "Master of Science",
        "MCA", "Master of Computer Applications",
        "MBA", "Master of Business Administration",
        "M. Pharmacy", "M Pharmacy", "M.Pharm",

        # Doctorate
        "PhD", "Ph.D", "Doctor of Philosophy",

        # Diploma / Certifications
        "Diploma", "Polytechnic", "PG Diploma"
    ]

    for keyword in keywords:
        pattern = r"(?i)\b{}\b".format(re.escape(keyword))
        match = re.search(pattern, text)
        if match:
            education.append(match.group())
    return education

def extract_name(text):
    matcher = Matcher(nlp.vocab)
    patterns = [
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}],
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}]
    ]
    for pattern in patterns:
        matcher.add("NAME", [pattern])
    doc = nlp(text)
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        return span.text
    return None

def extract_socials(text):
    socials = {}

    def format_url(match):
        url = match.group(0)
        if not url.startswith("http"):
            url = "https://" + url
        return url

    github = re.search(r"(https?:\/\/)?(www\.)?github\.com\/[A-Za-z0-9_.-]+", text)
    linkedin = re.search(r"(https?:\/\/)?(www\.)?linkedin\.com\/in\/[A-Za-z0-9_-]+", text)
    instagram = re.search(r"(https?:\/\/)?(www\.)?instagram\.com\/[A-Za-z0-9_.-]+", text)
    artstation = re.search(r"(https?:\/\/)?(www\.)?artstation\.com\/[A-Za-z0-9_.-]+", text)

    if linkedin:
        socials['LinkedIn'] = format_url(linkedin)
    if github:
        socials['GitHub'] = format_url(github)
    if instagram:
        socials['Instagram'] = format_url(instagram)
    if artstation:
        socials['ArtStation'] = format_url(artstation)

    return socials


import streamlit as st

# Title and Intro
st.title("Resume Parser")
st.markdown("Welcome to My Resume parser! Simply upload the file and your resume will be parsed and the following information will be extracted:\n\n- Name\t, Contact no\tand Email\n- Education\t, Skills\t and socials")

# Upload File
uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

resume_text = ""
if uploaded_file is not None:
    file_type = uploaded_file.name.split('.')[-1].lower()
    if file_type == "pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
    elif file_type == "docx":
        resume_text = extract_text_from_docx(uploaded_file)
    else:
        st.error("Unsupported file type. Please upload a PDF or DOCX file.")
else:
    # Do not show anything if no file is uploaded
    pass

# Show extracted info only if text is extracted
if resume_text:
    st.subheader("Extracted Information:")

    name = extract_name(resume_text)
    st.write("**Name:**", name or "Not found")

    contact = extract_contact_number(resume_text)
    st.write("**Contact:**", contact or "Not found")

    email = extract_email(resume_text)
    st.write("**Email:**", email or "Not found")

    skills_list = [
        # Programming Languages
        "Python", "C", "C++", "Java", "JavaScript", "TypeScript", "Kotlin", "Go", "Rust", "Ruby", "PHP", "R", "Swift",

        # Web Development
        "HTML", "CSS", "React", "Angular", "Vue", "Node.js", "Express", "Django", "Flask", "Tailwind CSS", "Bootstrap",
        "Next.js",

        # Databases
        "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Redis", "Firebase",

        # DevOps & Tools
        "Git", "GitHub", "Docker", "Kubernetes", "CI/CD", "Jenkins", "Linux", "Shell Scripting", "AWS", "Azure", "GCP",

        # Data Science / ML / AI
        "Data Analysis", "Data Visualization", "Pandas", "NumPy", "Matplotlib", "Seaborn",
        "Scikit-learn", "TensorFlow", "PyTorch", "OpenCV", "Keras", "Computer Vision", "NLP",
        "Machine Learning", "Deep Learning", "Model Deployment",

        # App Development
        "Android", "Flutter", "React Native", "Firebase", "SwiftUI",

        # Cybersecurity / Networks
        "Network Security", "Ethical Hacking", "Penetration Testing", "Wireshark", "Kali Linux", "Firewalls",
        "Cryptography",

        # Software Engineering / Other Tools
        "OOP", "DSA", "Agile", "Scrum", "System Design", "UML", "SDLC", "VS Code", "Postman", "Figma",

        # Soft Skills
        "Problem Solving", "Teamwork", "Communication", "Time Management", "Leadership", "Critical Thinking"
    ]

    skills = extract_skills(resume_text, skills_list)
    st.write("**Skills:**", ", ".join(skills) if skills else "Not found")

    education = extract_education(resume_text)
    st.write("**Education:**", ", ".join(education) if education else "Not found")

    socials = extract_socials(resume_text)
    if socials:
        st.write("**Socials:**")
        for platform, url in socials.items():
            st.markdown(f"[{platform}]({url})", unsafe_allow_html=True)


# Footer Credits
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>Made with ❤️ by Prathmesh Bajpai</p>", unsafe_allow_html=True)


st.markdown(
    """
    <div style='text-align: center; margin-top: -10px;'>
        <a href='https://www.linkedin.com/in/prathmesh-bajpai-8429652aa/' target='_blank' style='text-decoration: none; font-size: 14px; color: #0A66C2;'>
            <img src='https://cdn-icons-png.flaticon.com/512/174/174857.png' width='16' style='vertical-align: middle; margin-right: 6px;'/>
            Follow me on LinkedIn
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- End of Streamlit UI ----------------


class TestResumeParser(unittest.TestCase):

    def test_extract_email(self):
        text = "Contact me at test@example.com"
        self.assertEqual(extract_email(text), "test@example.com")

    def test_extract_contact_number(self):
        text = "My phone number is +91 394587934"
        self.assertEqual(extract_contact_number(text), "+91 394587934")

if __name__ == '__main__':
    unittest.main()
