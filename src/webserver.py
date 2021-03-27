from flask import request, Flask, jsonify
from ORMConnector import ORMConnector

app = Flask(__name__)
orm=ORMConnector()

def request_handler():
    try:
        body = request.json
        
        if request.method == 'GET':
            return jsonify(orm.get_movies_list(body['top_number'], body['genres'], body['year_from'], body['year_to'], body['regexp']))
        elif request.method == 'POST':
            orm.insert_new_rating(body['id'], body['rate'])
            return jsonify({'response': 'OK'})
    except BaseException:
        return jsonify({'error': 'wrong request'})

    return jsonify({'error': 'no such method'})

@app.route('/', methods=['GET', 'POST'])
def index():
    return request_handler()

# handle any other route
@app.route('/<path:u_path>', methods=['GET', 'POST'])
def catch_all(u_path):  
    return request_handler()


if __name__ == '__main__':
    app.run()
