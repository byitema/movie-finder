from .src.webserver import index
import flask

def test_index():
    assert index() == flask.jsonify({'error': 'wrong request'})