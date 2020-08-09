from flask import Flask, request, jsonify, abort, make_response
from models import expenses

app = Flask(__name__)
app.config['SECRET_KEY'] = 'whisper'


@app.route('/api/v1/expenses/', methods=['GET'])
def expenses_list_api_v1():
    return jsonify(expenses.all())


@app.route('/api/v1/expenses/<int:expense_id>', methods=['GET'])
def get_expense(expense_id):
    expense = expenses.get(expense_id)
    if not expense:
        abort(404)
    return jsonify({'expense': expense})


@app.route('/api/v1/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    result = expenses.delete(expense_id)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route('/api/v1/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    expense = expenses.get(expense_id)
    if not expense:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'category' in data and not isinstance(data.get('category'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'value' in data and not isinstance(data.get('value'), float),
        'periodic' in data and not isinstance(data.get('periodic'), bool)
    ]):
        abort(400)

    expense = {
        'title': data.get('title', expense['title']),
        'category': data.get('category', expense['category']),
        'description': data.get('description', expense['description']),
        'value': data.get('value', expense['value']),
        'periodic': data.get('periodic', expense['periodic']),
        'id': expense_id
    }
    expenses.update(expense_id, expense)
    return jsonify({'expense': expense})


@app.route('/api/v1/expenses/', methods=['POST'])
def create_expense():
    if not request.json:
        abort(400)

    if any(['title' not in request.json, 'category' not in request.json,
           'value' not in request.json, 'periodic' not in request.json]):
        abort(400)

    expense = {
        'id': expenses.all()[-1]['id'] + 1,
        'title': request.json['title'],
        'category': request.json['category'],
        'description': request.json.get('description', ""),
        'value': request.json['value'],
        'periodic': request.json['periodic']
    }
    expenses.create(expense)
    return jsonify({'expense': expense}), 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status code': 404}))


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status code': 400}))


if __name__ == "__main__":
    app.config['ENV'] = 'development'
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True, load_dotenv=False)
