import streamlit as st
from modules.matcher import calculate_similarity
from modules.pdf_extractor import extract_text_from_pdf
from modules.resume_parser import extract_skills, compare_skills


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📄 AI Resume Screening System")

st.write(
    "Upload a job description and multiple resumes "
    "to automatically analyze and rank candidates."
)


# --------------------------------------------------
# JOB DESCRIPTION
# --------------------------------------------------

st.subheader("1. Job Description")

job_description = st.text_area(
    "Enter the Job Description",
    height=250,
    placeholder="Paste the job description here..."
)


# --------------------------------------------------
# REQUIRED SKILLS FROM JOB DESCRIPTION
# --------------------------------------------------

job_skills = []

if job_description.strip():

    job_skills = extract_skills(job_description)

    st.subheader("🎯 Required Skills")

    if job_skills:

        st.write(
            ", ".join(
                skill.title()
                for skill in job_skills
            )
        )

    else:

        st.info(
            "No known technical skills detected "
            "in the job description."
        )


# --------------------------------------------------
# RESUME UPLOAD
# --------------------------------------------------

st.subheader("2. Upload Resumes")

uploaded_resumes = st.file_uploader(
    "Upload multiple resume PDFs",
    type=["pdf"],
    accept_multiple_files=True
)


# --------------------------------------------------
# DISPLAY UPLOADED FILES
# --------------------------------------------------

if uploaded_resumes:

    st.write("### Uploaded Resumes")

    for resume in uploaded_resumes:

        st.write(
            f"📄 {resume.name}"
        )


# --------------------------------------------------
# SCREEN RESUMES
# --------------------------------------------------

if st.button("🔍 Screen Resumes"):

    if not job_description.strip():

        st.warning(
            "Please enter a job description."
        )

    elif not uploaded_resumes:

        st.warning(
            "Please upload at least one resume."
        )

    elif not job_skills:

        st.warning(
            "No skills were detected in the job description."
        )

    else:

        st.success(
            "Resumes are being processed..."
        )

        # ------------------------------------------
        # PROCESS EACH RESUME
        # ------------------------------------------

        for resume in uploaded_resumes:

            st.divider()

            st.subheader(
                f"📄 {resume.name}"
            )

            # Extract text
            text = extract_text_from_pdf(resume)

            # Error handling
            if text.startswith("Error"):

                st.error(text)
                continue

            # Empty PDF
            if not text.strip():

                st.warning(
                    "No text could be extracted "
                    "from this PDF."
                )
                continue

            st.success(
                "Resume text extracted successfully."
            )

            # --------------------------------------
            # SHOW EXTRACTED TEXT
            # --------------------------------------

            with st.expander(
                "View extracted text"
            ):

                st.text(text)

            # --------------------------------------
            # EXTRACT RESUME SKILLS
            # --------------------------------------

            candidate_skills = extract_skills(text)
            semantic_score = calculate_similarity(
                job_description,
                text)

            st.write("### 🛠️ Detected Skills")

            if candidate_skills:

                st.write(
                    ", ".join(
                        skill.title()
                        for skill in candidate_skills
                    )
                )

            else:

                st.info(
                    "No known skills detected."
                )

            # --------------------------------------
            # COMPARE SKILLS
            # --------------------------------------

            matched_skills, missing_skills, skill_score = (
                compare_skills(
                    job_skills,
                    candidate_skills
                )
            )

            # --------------------------------------
            # MATCHED SKILLS
            # --------------------------------------

            st.write("### ✅ Matched Skills")

            if matched_skills:

                for skill in matched_skills:

                    st.write(
                        f"✓ {skill.title()}"
                    )

            else:

                st.write(
                    "No matching skills found."
                )

            # --------------------------------------
            # MISSING SKILLS
            # --------------------------------------

            st.write("### ❌ Missing Skills")

            if missing_skills:

                for skill in missing_skills:

                    st.write(
                        f"• {skill.title()}"
                    )

            else:

                st.write(
                    "No required skills are missing."
                )

            # --------------------------------------
            # SKILL SCORE
            # --------------------------------------

            st.write(
                f"### 📊 Skill Match Score: "
                f"{skill_score}%"
            )

            st.progress(
                min(int(skill_score), 100)
            )
            st.write(
                f"### 🧠 Semantic Similarity: {semantic_score}%")

            st.progress(
                min(int(semantic_score), 100))