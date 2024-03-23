from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

@app.route('/getNextMeal', methods=['GET'])
def get_meal():
    time_parameter = request.args.get('currentTime')
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM meals WHERE TIME(meal_time) > TIME(%s)"
    cursor.execute(query, (time_parameter,))
    
    # Fetch all rows from the cursor
    result = cursor.fetchall()
    
    # Get column names
    columns = [column[0] for column in cursor.description]
    
    # Convert the result into a list of dictionaries
    data = []
    for row in result:
        row_dict = {}
        for i, column in enumerate(cursor.description):
            row_dict[column[0]] = row[i]
            # Convert timedelta object to total seconds
            if isinstance(row[i], datetime.timedelta):
                row_dict[column[0]] = (datetime.datetime.min + row[i]).time().isoformat()
        data.append(row_dict)

    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
  

if __name__ == '__main__':
    app.run(debug=True)