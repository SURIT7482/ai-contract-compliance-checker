from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/upload', methods=['POST'])
def upload_contract():
    """Handle contract upload"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400
        
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        
        return jsonify({
            'message': 'File uploaded successfully',
            'filename': file.filename
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_contract():
    """Analyze contract for compliance"""
    try:
        data = request.json
        filename = data.get('filename')
        
        # Simple demo response
        return jsonify({
            'clauses': {
                'payment_terms': ['Found payment clause'],
                'termination': ['Found termination clause'],
                'data_protection': ['GDPR compliant clause found']
            },
            'risks': [
                {
                    'severity': 'medium',
                    'clause': 'liability',
                    'description': 'Liability clause needs review'
                }
            ],
            'compliance': {
                'GDPR': {'compliant': True, 'score': 85, 'missing': []},
                'HIPAA': {'compliant': False, 'score': 60, 'missing': ['PHI clause']}
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
