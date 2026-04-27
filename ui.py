import streamlit as st

# Configure the page
st.set_page_config(page_title="Sentinel AI", page_icon="🛡️", layout="centered")

# Header section
st.title("🛡️ Sentinel AI: Job Match Evaluator")
st.markdown("Evaluate your resume against a job profile to see how well you match.")

st.divider()

# Input section
st.subheader("1. Job Profile")
job_link = st.text_input("Job Profile Link", placeholder="https://example.com/job-posting")

st.subheader("2. Resume")
resume_pdf = st.file_uploader("Upload your Resume", type=["pdf"])

st.divider()

# Action section
if st.button("Evaluate Match", type="primary", use_container_width=True):
    if not job_link:
        st.warning("Please provide a job profile link.", icon="⚠️")
    elif not resume_pdf:
        st.warning("Please upload your resume in PDF format.", icon="⚠️")
    else:
        # Placeholder for future integration
        st.success("Inputs received successfully! Evaluation will run here.")
        
        # Displaying the inputs for verification
        st.write("### Received Data:")
        st.write(f"**Job Link:** {job_link}")
        st.write(f"**Resume File:** `{resume_pdf.name}` ({resume_pdf.size} bytes)")
        
        # Future integration point with our LangGraph agent via FastAPI
        # requests.post("http://127.0.0.1:8000/chat", json={"message": f"Evaluate this profile..."})
