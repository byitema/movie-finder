from webserver import app, index
from flask import current_app, jsonify

def test_index():
    with app.app_context():
        assert index() == jsonify({'error': 'wrong request'})