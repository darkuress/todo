from flask import Flask, render_template, request
import json
import os
import pprint
import db

app = Flask(__name__)
dataBase = 'data'
dataFile = 'data.txt'
indexFile = 'index.txt'

todoDB = db.DB()

@app.route('/')
def index():
    """
    login page
    """
    return render_template('login.html')
    
@app.route('/login', methods=['POST'])
def login():
    """
    first page
    """
    data = request.form
    
    #- check if valid
    userId = data['id']
    userPasswd = data['passwd']
    
    if todoDB.validate(userId, userPasswd):        
        templateData = {'templateData' : []}
        init_data = readJson(userId)
        if init_data:
            if init_data.has_key('templateData'):
                templateData = init_data
            else:
                templateData = {'templateData' : []}
        
        templateData['userId'] = userId
        
        return render_template('todo.html', **templateData)
    
    else:
        print 'log in failed'
        return render_template('login.html')

@app.route('/join', methods=['POST'])
def join():
    """
    join page
    """    
    return render_template('join.html')

@app.route('/addUser', methods=['POST'])
def addUser():
    """
    adding new person to db
    """
    data = request.form
    print data
    
    userId   = str(data['id'])
    name     = str(data['name'])    
    passwd   = str(data['passwd'])
    repasswd = str(data['repasswd'])
    
    if passwd == repasswd:
        addedUser = todoDB.addUser(userId, name, passwd, repasswd)
    else:
        print 'Joining Failed - unmatchingi Password'
        return render_template('login.html')
        
    if addedUser:
        print 'user %s added' %addedUser
        return render_template('login.html')
    else:
        print 'Joining Failed - DB'
        return render_template('login.html')
    

@app.route('/updateData', methods=['POST'])
def updateData():
    """
    update request
    """
    data = request.form
    userId = str(data['userId'])
    old_data = readJson(userId)
    
    pprint.pprint(data)
    
    if old_data:
        if old_data.has_key('templateData'):
            templateData = old_data
    else:
        templateData = {'templateData' : []}
    
    #- parse data    
    parsed_data = argParser(userId, data)
    
    #- append or remove data from template data
    if parsed_data['action'] == 'create':
        templateData['templateData'].append(parsed_data)
        
    elif parsed_data['action'] == 'delete':
        temp_data_del = []
        for one_temp_data in templateData['templateData']:
            print '...........1', one_temp_data['chkbx']
            print '...........', parsed_data['chkbx'].split(',')
            if one_temp_data['chkbx'] in parsed_data['chkbx'].split(','):
                temp_data_del.append(one_temp_data)
        
        for x in temp_data_del:
            templateData['templateData'].remove(x)
    
    elif parsed_data['action'] == 'update':
        for one_temp_data in templateData['templateData']:
            if one_temp_data['status_id'] == parsed_data['status_id']:
                one_temp_data['status'] = parsed_data['status']
                one_temp_data['all_status'] = parsed_data['all_status']
    
    print 'templateData : \n', pprint.pprint(templateData)
    
    writingJson(userId, templateData)
    todoDB.fillTable(userId, data)
    templateData['userId'] = userId
    
    return render_template('todo.html', **templateData)

def writingJson(userId, data):
    """
    writing JsonFile
    """
    dataFullFile = os.path.join(dataBase, userId + '_' + dataFile)
    with open(dataFullFile, 'w') as outfile:
        json.dump(data, outfile)

def writingTableDB(userId, data):
    """
    writing table database
    """
    todoDB.fillTable(userId, data)

def readJson(userId):
    """
    read json file
    """
    dataFullFile = os.path.join(dataBase, userId + '_' + dataFile)
    if os.path.exists(dataFullFile):       
        with open(dataFullFile, 'r') as outfile:
            json_data = json.load(outfile)
        return json_data
    else:
        return None

def increaseIndex(userId):
    """
    increase index
    """
    indexFullFile = os.path.join(dataBase, userId + '_' + indexFile)
    if os.path.exists(indexFullFile):
        file = open(indexFullFile, "r")
        last_index = int(file.readline())
        new_index = str(last_index+1)
        file.close()
    else:
        new_index = '1'
    file = open(indexFullFile, "w")
    file.write(new_index)
    
    return new_index
        
def argParser(userId, data):
    """
    parse requested data
    """
    dataKey = data.keys()[0]
    org_data = data[dataKey]

    new_data = {}
    new_data['who']    = data.get('person')
    new_data['what']   = data.get('content')
    new_data['status'] = str(data.get('status'))
    if str(data.get('status_id')):
        new_data['status_id'] = str(data.get('status_id'))
    else:
        new_data['status_id'] = 'status_' + increaseIndex(userId)
    new_data['action'] = data.get('action')
    if new_data['action'] == 'create':
        new_data['chkbx']  = data.get('chkbx') + '_' + increaseIndex(userId)
    elif new_data['action'] == 'delete':
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