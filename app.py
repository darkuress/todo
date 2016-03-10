from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route('/')
def index():
    templateData = {}
    return render_template('todo.html', **templateData)

@app.route('/updateData', methods=['POST'])
def updateData():
    print 'request....', request
    #-asdfasdf
    data = request.form
    writingJson(data)
    print 'data is.....', str(data['content'])
    return render_template('todo.html')

def writingJson(data):
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 5002)