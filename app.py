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
    print '..........', data
    if old_data:
        if old_data.has_key('templateData'):
            templateData = old_data
    else:
        templateData = {'templateData' : []}
    
    #- parse data    
    parsed_data = argParser(data)
    print 'parsed_data : ', parsed_data
    #- append or remove data from template data
    if parsed_data['action'] == 'create':
        templateData['templateData'].append(parsed_data)
        
    elif parsed_data['action'] == 'delete':
        for one_temp_data in templateData['templateData']:
            #new_parsed_data_what = [str(x) for x in eval(parsed_data['what'])]
            if one_temp_data['chkbx'] in parsed_data['what'].split(','):
                templateData['templateData'].remove(one_temp_data)
    
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
    new_data['who']    = data.get('person')
    new_data['what']   = data.get('content')
    new_data['status'] = data.get('status')
    new_data['action'] = data.get('action')
    new_data['chkbx']  = data.get('chkbx')
    all_status = ['wtg', 'ip', 'done', 'fix']
    new_data['all_status'] = []

    for status in all_status:
        if status == new_data['status']:
            new_data['all_status'].append({"s":status, "tf":'selected'})
        else:
            new_data['all_status'].append({"s":status, "tf":''})

    return new_data

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 5002)