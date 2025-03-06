import streamlit as st
import requests

st.set_page_config(page_title="O-1A Visa Assessment Tool", layout="wide")

st.title("O-1A Visa Assessment Tool")

st.write("""
This tool helps you assess your eligibility for an O-1A visa by analyzing your CV against the 8 criteria.
Upload your CV in PDF, DOCX, or TXT format to get started.
""")

with st.expander("Learn about O-1A Visa Criteria"):
    st.markdown("""
    The O-1A visa is for individuals with extraordinary ability in sciences, arts, education, business, or athletics. 
    You must meet at least 3 of these 8 criteria:
    
    1. **Awards**: Receipt of nationally or internationally recognized prizes/awards for excellence
    2. **Membership**: Membership in associations requiring outstanding achievement
    3. **Press**: Published material in professional publications about you and your work
    4. **Judging**: Acting as a judge of others' work in your field
    5. **Original contribution**: Original scientific, scholarly, or business-related contributions of major significance
    6. **Scholarly articles**: Authorship of scholarly articles in professional journals or major media
    7. **Critical employment**: Employment in a critical or essential capacity for distinguished organizations
    8. **High remuneration**: Command of a high salary or remuneration
    """)

uploaded_file = st.file_uploader("Upload your CV", type=["pdf", "docx", "txt"])

if uploaded_file:
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"File uploaded: {uploaded_file.name}")
    
    with col2:
        if st.button("Assess CV", type="primary"):
            with st.spinner("Analyzing your CV... This may take up to a minute."):
                try:
                    # Prepare the file for the API request
                    files = {"cv": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                    
                    # Make the API request to your FastAPI backend
                    response = requests.post(
                        "http://localhost:8000/api/v1/assess",
                        files=files
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Display the rating
                        rating = result["rating"].lower()
                        rating_color = {
                            "high": "green",
                            "medium": "orange",
                            "low": "red"
                        }.get(rating, "blue")
                        
                        st.subheader("Assessment Result")
                        st.markdown(f"<h3 style='text-align: center; color: {rating_color};'>Overall Rating: {rating.upper()}</h3>", unsafe_allow_html=True)
                        
                        # Display criteria matches
                        st.subheader("Criteria Matches")
                        
                        # Sort criteria by the highest confidence match in each category
                        criteria_confidence = {}
                        for criterion, matches in result["criteria_matches"].items():
                            if matches and len(matches) > 0:
                                # Find the highest confidence in matches
                                highest_conf = max(match.get('confidence', 0) for match in matches)
                                criteria_confidence[criterion] = highest_conf
                        
                        # Sort criteria by highest confidence (descending)
                        sorted_criteria = sorted(
                            criteria_confidence.keys(),
                            key=lambda x: criteria_confidence[x],
                            reverse=True
                        )
                        
                        # Display sorted criteria
                        for criterion in sorted_criteria:
                            matches = result["criteria_matches"][criterion]
                            
                            # Sort matches within each criterion by confidence (descending)
                            sorted_matches = sorted(
                                matches, 
                                key=lambda x: x.get('confidence', 0), 
                                reverse=True
                            )
                            
                            with st.expander(f"{criterion} ({len(matches)} matches)"):
                                for match in sorted_matches:
                                    st.markdown("---")
                                    st.markdown(f"**Evidence:** {match.get('evidence', 'N/A')}")
                                    st.markdown(f"**Explanation:** {match.get('explanation', 'N/A')}")
                                    
                                    # Show confidence as a progress bar
                                    confidence = match.get('confidence', 0)
                                    st.markdown(f"**Confidence:** {confidence:.2f}")
                                    st.progress(confidence)
                                    
                                    if 'source' in match:
                                        st.markdown(f"**Source:** {match.get('source', 'N/A')}")
                            
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                        
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

st.sidebar.title("About")
st.sidebar.info("""
This tool uses AI to analyze your CV against the O-1A visa criteria.
It provides a rough assessment of your eligibility based on the information in your CV.
""")