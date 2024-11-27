# Virtual Lawyer: AI-Powered Legal Analysis Assistant ⚖️
Virtual Lawyer is a cutting-edge AI-powered application designed to perform comprehensive legal analysis on Indian criminal cases. Built with Streamlit and integrated with the Groq API, this app assists legal professionals and individuals by analyzing case descriptions and legal documents to provide structured legal insights.

## 📝 Features
Legal Classification: Identifies relevant sections under Bharatiya Nyaya Sanhita (BNS) 2023 and Indian Penal Code (IPC).
Legal Provisions: Detailed breakdown of applicable laws and their interpretations.
Punishment Details: Specifies punishment ranges, fines, and legal consequences.
Risk Assessment: Evaluates the severity of consequences and likelihood of conviction.
Procedural Recommendations: Guides users on next steps, documentation, and law enforcement interactions.
PDF Integration: Extracts context from uploaded legal documents.

## 🛠 Tech Stack
Frontend: Streamlit
Backend: Python
APIs: Groq API
Utilities: PyPDF2, dotenv

## 🚀 How It Works
Case Input: Users provide a detailed case description and upload relevant PDF documents.
Analysis Generation: The app leverages the Groq API to analyze the inputs and generate a structured legal report.
Results: Displays a comprehensive analysis with sections on legal classification, nuances, punishments, and recommendations.

## 📦 Setup Instructions
### Clone the repository:

git clone https://github.com/your-repo/virtual-lawyer.git

### Navigate to the project directory:

cd virtual-lawyer

### Install dependencies:

pip install -r requirements.txt

### Add your Groq API key in a .env file:

GROQ_API_KEY=your_api_key_here

### Run the application:

streamlit run app.py

## 🏆 Key Highlights
Supports multiple case types: Criminal, Civil, Property Disputes, Cybercrime, and more.
Ensures data security and confidentiality.
Provides actionable insights for legal strategies.
