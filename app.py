from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route('/')
def index():
    """
    first page
    """
    templateData = {}
    return render_template('todo.html', **templateData)

@app.route('/updateData', methods=['POST'])
def updateData():
    """
    update request
    """
    data = request.form
    writingJson(data)
    
    templateData = {'templateData' : []}
    templateData['templateData'].append(argParser(data))
    print templateData
    
    return render_template('todo.html', **templateData)

def writingJson(data):
    """
    writing JsonFile
    """
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)

def argParser(data):
    """
    parse requested data
    """
    dataKey = data.keys()[0]
    org_data = data[dataKey]
    new_data = {}
    new_data['chked']  = str(org_data.split('__')[0])
    new_data['who']    = str(org_data.split('__')[1])
    new_data['what']   = str(org_data.split('__')[2])
    new_data['status'] = str(org_data.split('__')[3])
    
    return new_data

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 5002)