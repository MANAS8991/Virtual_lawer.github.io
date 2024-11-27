import streamlit as st
import PyPDF2
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class VirtualLawyer:
    def __init__(self):
        # Retrieve Groq API Key from environment variable
        groq_api_key = os.getenv("GROQ_API_KEY")
        
        # Validate API Key
        if not groq_api_key:
            st.error("GROQ_API_KEY not found in .env file. Please configure it.")
            st.stop()
        
        # Initialize Groq client
        self.client = Groq(api_key=groq_api_key)
        
        # Comprehensive legal analysis prompt template
        self.legal_analysis_prompt = """
        You are an advanced legal AI assistant specialized in Indian criminal law, 
        specifically the Bharatiya Nyaya Sanhita (BNS) 2023 and Indian Penal Code (IPC).

        Case Description: {case_description}

        Perform a comprehensive legal analysis with the following structured output:

        1. LEGAL CLASSIFICATION
        - Precise legal classification of the offense
        - Relevant sections under BNS 2023 or IPC
        - Specific sub-clauses applicable

        2. LEGAL PROVISIONS
        - Detailed breakdown of legal provisions
        - Specific sections and their exact wordings
        - Potential interpretations of law

        3. PUNISHMENT DETAILS
        - Exact punishment range (imprisonment)
        - Monetary fine specifications
        - Additional legal consequences

        4. LEGAL NUANCES
        - Intent requirements
        - Burden of proof
        - Potential defenses
        - Aggravating and mitigating factors

        5. PROCEDURAL RECOMMENDATIONS
        - Suggested immediate legal steps
        - Documentation requirements
        - Potential law enforcement interactions

        6. RISK ASSESSMENT
        - Severity of potential legal consequences
        - Probability of conviction based on provided details
        - Recommended legal strategy overview

        7. ADDITIONAL CONTEXT
        - Relevant case law references
        - Recent judicial interpretations
        - Societal and legal implications

        Format the response in a clear, professional, and authoritative manner, 
        citing specific legal references and maintaining utmost precision.
        """

    def extract_pdf_text(self, uploaded_files):
        """
        Extract text from uploaded PDF files
        
        Args:
            uploaded_files (list): List of uploaded PDF file objects
        
        Returns:
            str: Extracted text from PDFs
        """
        extracted_text = ""
        for pdf_file in uploaded_files:
            try:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                for page in pdf_reader.pages:
                    extracted_text += page.extract_text() + "\n\n"
            except Exception as e:
                st.error(f"Error processing PDF: {e}")
        return extracted_text

    def generate_legal_analysis(self, case_description, pdf_context=""):
        """
        Generate comprehensive legal analysis using Groq API
        
        Args:
            case_description (str): Description of the legal case
            pdf_context (str, optional): Additional context from PDFs
        
        Returns:
            str: Detailed legal analysis
        """
        full_context = f"{pdf_context}\n\nCase Details: {case_description}"
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a highly skilled legal AI assistant specialized in Indian criminal law."},
                    {"role": "user", "content": self.legal_analysis_prompt.format(case_description=full_context)}
                ],
                model="mixtral-8x7b-32768",
                max_tokens=4000,
                temperature=0.3
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            st.error(f"Legal analysis generation error: {e}")
            return "Unable to generate legal analysis. Please try again."

    def app(self):
        """
        Streamlit application main interface
        """
        st.set_page_config(
            page_title="Virtual Lawyer",
            page_icon="⚖️",
            layout="wide"
        )
        
        st.title("⚖️ Virtual Lawyer: Legal Analysis Assistant")
        
        # Sidebar for advanced settings
        st.sidebar.header("Legal Document Upload")
        uploaded_pdfs = st.sidebar.file_uploader(
            "Upload Relevant Legal Documents (Max 2 PDFs)", 
            type=['pdf'], 
            accept_multiple_files=True
        )
        
        # Main case description input
        st.header("Case Description Input")
        case_description = st.text_area(
            "Enter Detailed Case Description", 
            height=200, 
            placeholder="Provide a comprehensive description of the legal case...\n\nInclude details such as:\n- Nature of the incident\n- Parties involved\n- Specific actions or allegations\n- Relevant circumstances"
        )
        
        # Case Type Selection
        case_types = [
            "Criminal", 
            "Civil", 
            "Property Dispute", 
            "Harassment", 
            "Cyber Crime", 
            "Domestic Violence",
            "Other"
        ]
        selected_case_type = st.selectbox(
            "Select Case Type", 
            options=case_types
        )
        
        # Analysis generation
        if st.button("Analyze Case", type="primary"):
            # Input validation
            if not case_description.strip():
                st.warning("Please provide a detailed case description.")
                return
            
            with st.spinner("Generating Comprehensive Legal Analysis..."):
                # Extract PDF context if files uploaded
                pdf_context = self.extract_pdf_text(uploaded_pdfs) if uploaded_pdfs else ""
                
                # Generate legal analysis
                legal_analysis = self.generate_legal_analysis(
                    case_description, 
                    pdf_context
                )
                
                # Display results with enhanced formatting
                st.markdown("## 📜 Legal Analysis Report")
                
                # Expandable sections for better readability
                with st.expander("Full Legal Analysis", expanded=True):
                    st.write(legal_analysis)
                
                # Additional insights
                st.markdown("### 🔍 Quick Insights")
                st.info(f"Case Type: {selected_case_type}")

def main():
    virtual_lawyer = VirtualLawyer()
    virtual_lawyer.app()

if __name__ == "__main__":
    main()
