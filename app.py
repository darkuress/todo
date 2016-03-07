from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    templateData = {}
    return render_template('todo.html', **templateData)

@app.route('/updateData')
def updateData():
    try:
        return str(request.args['data'])
    except KeyError:
        return "Missing parameter"
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 5002)