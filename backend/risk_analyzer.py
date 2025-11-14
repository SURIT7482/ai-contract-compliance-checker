class RiskAnalyzer:
    def __init__(self):
        self.compliance_rules = {
            "GDPR": ["data protection", "consent", "right to erasure", "data portability"],
            "HIPAA": ["PHI", "health information", "privacy rule", "security rule"],
            "General": ["termination clause", "liability limit", "dispute resolution"]
        }
    
    def assess_risk(self, contract_text, clauses_found):
        """Assess compliance risks"""
        risks = []
        
        # Check for missing critical clauses
        critical_clauses = ["termination", "liability", "confidentiality"]
        for clause in critical_clauses:
            if clause.lower() not in clauses_found.lower():
                risks.append({
                    "severity": "HIGH",
                    "type": "Missing Clause",
                    "description": f"Missing {clause.title()} clause",
                    "recommendation": f"Add clear {clause} terms to ensure legal protection"
                })
        
        # GDPR compliance check
        if "personal data" in contract_text.lower() or "user data" in contract_text.lower():
            gdpr_terms = ["consent", "data protection", "right to erasure"]
            missing_gdpr = [term for term in gdpr_terms if term not in contract_text.lower()]
            
            if missing_gdpr:
                risks.append({
                    "severity": "HIGH",
                    "type": "GDPR Non-Compliance",
                    "description": f"Missing GDPR requirements: {', '.join(missing_gdpr)}",
                    "recommendation": "Add GDPR-compliant data processing clauses"
                })
        
        # Liability check
        if "unlimited liability" in contract_text.lower():
            risks.append({
                "severity": "MEDIUM",
                "type": "Liability Risk",
                "description": "Contract contains unlimited liability clause",
                "recommendation": "Consider capping liability to reasonable limits"
            })
        
        return risks if risks else [{"severity": "LOW", "type": "No Major Issues", 
                                     "description": "Contract appears compliant", 
                                     "recommendation": "Regular review recommended"}]
