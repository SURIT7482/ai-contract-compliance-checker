from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os

class ClauseExtractor:
    def __init__(self):
        # Use OpenAI API (you can use free tier or demo mode)
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY", "demo-key")
        )
    
    def extract_clauses(self, contract_text):
        """Extract key clauses from contract"""
        prompt = ChatPromptTemplate.from_template(
            """Analyze this contract and extract the following key clauses:
            1. Payment Terms
            2. Termination Clause
            3. Confidentiality Clause
            4. Liability Clause
            5. Data Protection/Privacy Clause
            6. Dispute Resolution
            
            Contract: {contract}
            
            Provide a structured summary of each clause found."""
        )
        
        try:
            response = self.llm.invoke(prompt.format(contract=contract_text))
            return response.content
        except:
            return self._fallback_extraction(contract_text)
    
    def _fallback_extraction(self, text):
        """Fallback keyword-based extraction"""
        clauses = {
            "Payment Terms": self._find_section(text, ["payment", "fee", "compensation"]),
            "Termination": self._find_section(text, ["termination", "cancel", "end agreement"]),
            "Confidentiality": self._find_section(text, ["confidential", "non-disclosure", "NDA"]),
            "Liability": self._find_section(text, ["liability", "indemnification", "damages"]),
            "Data Protection": self._find_section(text, ["data protection", "GDPR", "privacy", "personal data"]),
            "Dispute Resolution": self._find_section(text, ["dispute", "arbitration", "jurisdiction"])
        }
        return "\n\n".join([f"**{k}:**\n{v}" for k, v in clauses.items() if v])
    
    def _find_section(self, text, keywords):
        """Find sections containing keywords"""
        sentences = text.split('.')
        relevant = []
        for sent in sentences:
            if any(kw.lower() in sent.lower() for kw in keywords):
                relevant.append(sent.strip())
        return " ".join(relevant[:3]) if relevant else "Not found"
