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
    x = request.data
    print 'data is.....', str(x)
    return render_template('todo.html')
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 5002)