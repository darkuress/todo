import MySQLdb

class DB(object):
    def __init__(self):
        self.db = MySQLdb.connect("localhost","root","83872732","todo_member_management" )
        self.cursor = self.db.cursor()
    
    @property
    def allUser(self):
        """
        querry all member
        """
        sql = """select userid from user"""
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        existingIds = []
        for oneId in result:
            existingIds.append(oneId[0])
        
        return existingIds

    def addUser(self, userId, name, passwd, repasswd):
        """
        add user to database
        """
        # check if exists
        if not self.validateNewId(userId):
            return False
        else:
            try:
                sql = """insert into user value(
                         null,'%s', '%s', sha1('%s'))""" %(userId, name, passwd)
                self.cursor.execute(sql)
                self.db.commit()
                
                #- creating table for user
                self.addTable(userId)
                
                return userId
            except:
                self.db.rollback()
                return False
    
    def removeUser(self, userId):
        """
        delete user and user todo table from the database
        """
        sql = """delete from user where userid=%s;
                 drop table todo_list_%s;"""  %(userId, userId)
        self.cursor.execute(sql)
        
        return "deleted user : %s" %userId
    
    def validateNewId(self, userId):
        """
        check if id already exists
        """
        sql = """select userid from user"""
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        existingIds = []
        for oneId in result:
            existingIds.append(oneId[0])
        
        if userId in existingIds:
            return False
        else:
            return True

    def validate(self, userId, passwd):
        """
        check if userId and passwd matches
        """
        sql = """select * from user where userId='%s' and passwd=sha1('%s')""" %(str(userId), str(passwd))
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
    
        if result:
            return True
        else:
            return False
    
    def addTable(self, userId):
        """
        Create content table
        """
        try:
            sql = """create table todo_list_%s (
                     tid int not null primary key auto_increment,
                     chkbx char(10),
                     status char(10) not null,
                     status_id char(10),
                     content char(80) not null,
                     requestedby char(20) not null)""" %userId
                     
            self.cursor.execute(sql)
            return "todo_list_%s" %userId
        except:
            print "Falied creating new table for user %s" %userId
            return False
        
    def fillTable(self, userId, data):
        """
        fill content 
        """
        tid       = data['chkbx']
        status    = data['status']
        status_id = data['status_id']
        content   = data['what']
        reqby     = data['who']
        
        try:
            sql = """insert into todo_list_%s value(
                     null, null, '%s', null, '%s', '%s')""" %(userId, status, content, reqby)
            self.cursor.execute(sql)
            self.db.commit()
            
        except:
            self.db.rollback()
            return False                     
        
        #- fill status_id with name_tid
        sql = """select * from todo_list_%s order by tid desc limit 1""" %userId
        self.cursor.execute(sql)
        line = self.cursor.fetchall()
        index = str(int(line[0][0]))
        status_id = 'status_' + index
        
        try:
            sql = """update todo_list_%s set chkbx='chkbx_%s', status_id='status_%s' where tid=%s""" %(userId, index, index, int(index))
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
        
        return index

    def updateStatus(self, userId, new_status, status_id):
        """
        update status
        """
        try:
            sql = """update todo_list_%s set status='%s' where status_id='%s'""" %(userId, new_status, status_id)
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
        
    def readLine(self, userId, tid):
        """
        read one line of the table where tid
        """
        sql = """select * from todo_list_%s where tid=%s""" %(userId, tid)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        
        data = {}
        data['chkbx']     = int(result[0][0])
        data['status']    = result[0][1]
        data['status_id'] = result[0][2]
        data['what']      = result[0][3]
        data['who']       = result[0][4]
        
        return data
    
    def readTable(self, userId):
        """
        read all info of table
        """
        sql = """select * from todo_list_%s""" %(userId)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        
        all_data = []
        for line in result:
            data = {}
            data['chkbx']     = line[1]
            data['status']    = line[2]
            data['status_id'] = line[3]
            data['what']      = line[4]
            data['who']       = line[5]
            all_data.append(data)
            
        return all_data

    def removeLine(self, userId, chkbx):
        """
        delete row from the table
        """
        sql = """delete from todo_list_%s where chkbx='%s'""" %(userId, chkbx)
        try:
           self.cursor.execute(sql)
           self.db.commit()
        except:
           self.db.rollback()        
        