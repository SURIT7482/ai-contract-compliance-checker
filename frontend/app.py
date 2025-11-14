import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.clause_extractor import ClauseExtractor
from backend.risk_analyzer import RiskAnalyzer
import PyPDF2
from docx import Document

def extract_text_from_pdf(file):
    """Extract text from PDF"""
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    """Extract text from DOCX"""
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def main():
    st.set_page_config(page_title="AI Contract Compliance Checker", page_icon="📋", layout="wide")
    
    st.title("📋 AI-Powered Regulatory Compliance Checker")
    st.markdown("**Automated contract analysis for GDPR, HIPAA, and regulatory compliance**")
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.info("""
        This AI system:
        - Extracts key contract clauses
        - Assesses compliance risks
        - Recommends amendments
        - Supports GDPR & HIPAA standards
        """)
        
        st.header("Supported Formats")
        st.write("📄 PDF, DOCX, TXT")
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 Upload Contract")
        uploaded_file = st.file_uploader(
            "Choose a contract file",
            type=['pdf', 'docx', 'txt'],
            help="Upload your contract document for analysis"
        )
        
        if uploaded_file:
            st.success(f"✅ Uploaded: {uploaded_file.name}")
            
            # Extract text
            if uploaded_file.type == "application/pdf":
                contract_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                contract_text = extract_text_from_docx(uploaded_file)
            else:
                contract_text = uploaded_file.read().decode()
            
            # Display preview
            with st.expander("📄 View Contract Preview"):
                st.text_area("Contract Text", contract_text[:1000] + "...", height=200)
    
    with col2:
        st.header("⚙️ Analysis Options")
        analysis_type = st.multiselect(
            "Select compliance frameworks",
            ["GDPR", "HIPAA", "General Contract Law"],
            default=["GDPR", "General Contract Law"]
        )
        
        analyze_button = st.button("🔍 Analyze Contract", type="primary", use_container_width=True)
    
    # Analysis section
    if uploaded_file and analyze_button:
        with st.spinner("🔄 Analyzing contract..."):
            # Initialize analyzers
            extractor = ClauseExtractor()
            analyzer = RiskAnalyzer()
            
            # Extract clauses
            st.header("📋 Extracted Clauses")
            clauses = extractor.extract_clauses(contract_text)
            st.markdown(clauses)
            
            # Risk assessment
            st.header("⚠️ Risk Assessment")
            risks = analyzer.assess_risk(contract_text, clauses)
            
            for risk in risks:
                severity_color = {
                    "HIGH": "🔴",
                    "MEDIUM": "🟡",
                    "LOW": "🟢"
                }
                
                with st.expander(f"{severity_color.get(risk['severity'], '🔵')} {risk['type']} - {risk['severity']} Severity"):
                    st.write(f"**Issue:** {risk['description']}")
                    st.write(f"**Recommendation:** {risk['recommendation']}")
            
            # Summary
            st.header("📊 Compliance Summary")
            high_risks = sum(1 for r in risks if r['severity'] == 'HIGH')
            medium_risks = sum(1 for r in risks if r['severity'] == 'MEDIUM')
            
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("High Risk Issues", high_risks)
            col_b.metric("Medium Risk Issues", medium_risks)
            col_c.metric("Compliance Score", f"{max(0, 100 - (high_risks * 20 + medium_risks * 10))}%")

if __name__ == "__main__":
    main()
