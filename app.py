from flask import Flask, render_template, request
import json
import os
import pprint
import db

app = Flask(__name__)
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
        init_data = readTable(userId)
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
    old_data = readTable(userId)
    
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
        writingTableDB(userId, parsed_data)
        parsed_data['all_status'] = statusSelector(parsed_data['status'])
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
                one_temp_data['all_status'] = statusSelector(parsed_data['status'])
                
                todoDB.updateStatus(userId, one_temp_data['status'], parsed_data['status_id'])
        
    print 'templateData : \n', pprint.pprint(templateData)

    templateData['userId'] = userId
    
    return render_template('todo.html', **templateData)

def writingTableDB(userId, data):
    """
    writing table database
    """
    todoDB.fillTable(userId, data)

def readTable(userId):
    """
    read existing values in table in db
    """
    db_table_data = todoDB.readTable(userId)
    data = {'templateData' : db_table_data}
    
    print 'Database : \n', pprint.pprint(data)
    
    return data

def statusSelector(status):
    """
    this will be added to template data
    """
    all_status = ['wtg', 'ip', 'done', 'fix']
    result = []

    for one_status in all_status:
        if one_status == status:
            result.append({"s":one_status, "tf":'selected'})
        else:
            result.append({"s":one_status, "tf":''})    
    
    return result
    
def argParser(userId, data):
    """
    parse requested data
    """
    dataKey = data.keys()[0]
    org_data = data[dataKey]

    new_data = {}
    new_data['who']       = data.get('person')
    new_data['what']      = data.get('content')
    new_data['chkbx']     = data.get('chkbx')
    new_data['status']    = str(data.get('status'))
    new_data['status_id'] = str(data.get('status_id'))
    new_data['action']    = data.get('action')    

    return new_data

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 5002)