from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/getNextMeal', methods=['GET'])
def get_meal():
    data = {'message': 'Returning Meal'}
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(debug=True)