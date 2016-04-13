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
    
    def addTable(self, user):
        """
        Create content table
        """
        try:
            sql = """CREATE TABLE todo_list_%s (
                     tid int not null primary key auto_increment,
                     check CHAR(5) NOT NULL,
                     status CHAR(10) NOT NULL,
                     content CHAR(80) NOT NULL,
                     requested by CHAR(20) NOT NULL )""" %user
                     
            self.cursor.execute(sql)
            return "%s_todo_list" %user
        except:
            print "Falied creating new table for user %s" %user
            return False
        
    def fillTable(self):
        pass
                     
                 