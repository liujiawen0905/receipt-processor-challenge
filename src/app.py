from flask import Flask, request, jsonify
from utils import validate_receipt, calculate_points
import uuid


app = Flask(__name__)

receipts_map = {}


@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    """
    Endpoint to process and calculate points based on recepit details
    Return JSON object containing the receipt ID or an error message
    """
    receipt  = request.json
    is_valid, validation_errors = validate_receipt(receipt)
    if not is_valid:
        return jsonify(
            {
                "error": "The receipt is invalid",
                "messages": validation_errors
            }
        ), 400
    
    receipt_id = str(uuid.uuid4())
    points = calculate_points(receipt)
    receipts_map[receipt_id] = points
    
    return jsonify({"id": receipt_id}), 200

@app.route('/receipts/<id>/points', methods=['GET'])
def get_points(id):
    points = receipts_map.get(id)
    if not points:
        return jsonify({"error": "No receipt found for that id"}), 404 
    
    return jsonify({"points": points})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)