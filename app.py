import streamlit as st
from utils.parser import extract_text_from_pdf
from utils.nlp_matcher import calculate_match, extract_keywords_only
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Resume Analyzer", layout="centered", page_icon="📄")

# --- CSS Styling ---
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
    color: #333;
}
h1, h2, h3 {
    color: #3b82f6;
}
.block-container {
    background-color: #f9f9f9;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
button {
    border-radius: 8px !important;
    background-color: #3b82f6 !important;
    color: white !important;
    padding: 0.5em 1.2em !important;
    transition: 0.2s ease-in-out all;
}
button:hover {
    background-color: #2563eb !important;
    transform: scale(1.03);
}
.stFileUploader label {
    font-weight: bold;
    color: #444;
}
.stRadio > div {
    display: flex;
    justify-content: space-evenly;
}
textarea, .stTextInput {
    border-radius: 6px;
}
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}
.watermark {
    position: fixed;
    bottom: 10px;
    right: 15px;
    opacity: 0.5;
    font-size: 14px;
    z-index: 9999;
}
</style>
<div class="watermark">Made by Vinit Puri</div>
""", unsafe_allow_html=True)

# Title
st.title("📄 AI-Powered Resume Analyzer")
st.write("Upload your resume and compare it with a job description to evaluate your skill alignment.")

# Upload resume
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type="pdf")

# Job description input
job_desc_option = st.radio("Job Description Input Method", ("Paste Text", "Upload File", "Skip"))
job_desc_text = ""

if job_desc_option == "Paste Text":
    job_desc_text = st.text_area("Paste the job description here")
elif job_desc_option == "Upload File":
    job_desc_file = st.file_uploader("Upload Job Description (TXT only)", type="txt")
    if job_desc_file:
        job_desc_text = job_desc_file.read().decode("utf-8")

# ✅ Expanded default skills list
default_job_keywords = [
    "Python", "SQL", "Tableau", "Power BI", "Excel", "Machine Learning",
    "Data Analysis", "Communication", "Collaboration", "Problem Solving",
    "Critical Thinking", "Deep Learning", "Pandas", "Numpy", "Scikit-Learn",
    "Data Visualization", "Data Engineering", "APIs", "Dashboards", "Cloud",
    "AWS", "Azure", "BigQuery", "Statistics", "ETL", "Docker", "Git", "Agile"
]

# Main analysis
if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)

    with st.expander("📝 View Extracted Resume Text"):
        st.text_area("Resume Content", resume_text, height=250)

    # Extract keywords
    job_keywords = extract_keywords_only(job_desc_text) if job_desc_text.strip() else default_job_keywords

    # Skill match
    score, matched = calculate_match(resume_text, job_keywords)
    matched = set([s.title() for s in matched])
    missing = set([s.title() for s in job_keywords]) - matched

    st.subheader("📊 Skill Match Analysis")
    st.progress(score / 100)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="✅ Match Score", value=f"{score:.1f}%")
        st.success("Matched Skills:\n" + (", ".join(sorted(matched)) if matched else "None"))

    with col2:
        st.warning("Missing Skills:\n" + (", ".join(sorted(missing)) if missing else "None"))

    # --- Chart for PDF ---
    def generate_skill_chart(matched, missing):
        labels = ['Matched Skills', 'Missing Skills']
        values = [len(matched), len(missing)]

        fig, ax = plt.subplots()
        ax.bar(labels, values, color=['#10b981', '#ef4444'])
        ax.set_ylabel('Skill Count')
        ax.set_title('Resume Skill Overview')
        fig.tight_layout()

        buf = BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        return buf

    # --- PDF Generator ---
    def generate_pdf(score, matched, missing):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        y = height - 50

        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, y, "Resume Skill Match Report")

        y -= 40
        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"Match Score: {score:.1f}%")

        y -= 30
        c.setFont("Helvetica-Bold", 13)
        c.drawString(50, y, "Matched Skills:")
        y -= 20
        c.setFont("Helvetica", 11)
        for skill in sorted(matched):
            c.drawString(70, y, f"• {skill}")
            y -= 15

        y -= 10
        c.setFont("Helvetica-Bold", 13)
        c.drawString(50, y, "Missing Skills:")
        y -= 20
        c.setFont("Helvetica", 11)
        for skill in sorted(missing):
            c.drawString(70, y, f"• {skill}")
            y -= 15

        # Add skill chart
        y -= 40
        chart_img = generate_skill_chart(matched, missing)
        c.drawImage(ImageReader(chart_img), 50, y - 200, width=500, height=200)

        # Only create new page if not enough space
        if y < 250:
            c.showPage()
            y = height - 50

        # Explanation section
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Detailed Skill Gap Analysis")
        y -= 25

        c.setFont("Helvetica", 11)
        explanation = (
            "The above report highlights the skills from your resume that match the job description, "
            "as well as those that are missing. We recommend reviewing the missing skills carefully. "
            "Consider gaining experience, certifications, or training in these areas to strengthen your profile "
            "and increase your chances of being shortlisted."
        )

        def wrap_text(canvas_obj, text, x, y, max_width, line_height):
            words = text.split()
            line = ''
            for word in words:
                test_line = line + word + ' '
                if canvas_obj.stringWidth(test_line, "Helvetica", 11) < max_width:
                    line = test_line
                else:
                    canvas_obj.drawString(x, y, line.strip())
                    y -= line_height
                    line = word + ' '
            if line:
                canvas_obj.drawString(x, y, line.strip())
            return y

        y = wrap_text(c, explanation, 50, y, max_width=500, line_height=15)

        # Footer
        c.setFont("Helvetica-Oblique", 9)
        c.drawRightString(width - 20, 20, "Made by Vinit Puri")

        c.save()
        buffer.seek(0)
        return buffer

    # --- PDF Download ---
    st.markdown("### ⬇️ Download Your PDF Skill Report")
    pdf_bytes = generate_pdf(score, matched, missing)
    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_bytes,
        file_name="resume_skill_report.pdf",
        mime="application/pdf"
    )
