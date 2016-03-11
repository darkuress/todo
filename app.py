from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    """
    first page
    """
    templateData = {'templateData' : []}
    init_data = readJson()
    if init_data:
        if init_data.has_key('templateData'):
            templateData = init_data
        else:
            templateData = {'templateData' : []}
    
    return render_template('todo.html', **templateData)

@app.route('/updateData', methods=['POST'])
def updateData():
    """
    update request
    """
    data = request.form
    old_data = readJson()
    if old_data:
        if old_data.has_key('templateData'):
            templateData = oldData
    else:
        templateData = {'templateData' : []}
    templateData['templateData'].append(argParser(data))
    
    writingJson(templateData)
    
    print templateData
    
    return render_template('todo.html', **templateData)

def writingJson(data):
    """
    writing JsonFile
    """
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)

def readJson():
    """
    read json file
    """
    if os.path.exists('data.txt'):       
        with open('data.txt', 'r') as outfile:
            json_data = json.load(outfile)
        return json_data
    else:
        return None
    
        
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
    all_status = ['wtg', 'ip', 'done', 'fix']
    new_data['all_status'] = []
    for status in all_status:
        if status == new_data['status']:
            new_data['all_status'].append({"s":status, "tf":True})
        else:
            new_data['all_status'].append({"s":status, "rd":False})
    
    return new_data

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 5002)