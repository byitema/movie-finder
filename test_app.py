from webserver import app, index
from flask import current_app, jsonify, json

def test_index():
    with app.app_context():
        data = json.loads(index().get_data(as_text=True))
        assert data['error'] == 'wrong request'