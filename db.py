import MySQLdb

db = MySQLdb.connect("localhost","root","83872732","todo_member_management" )
cursor = db.cursor()

#insert into user value(null,'admin', 'administrator', sha1('password'))
#select * from user where userid='admin'
class DB(object):
    def __init__(self):
        db = MySQLdb.connect("localhost","root","83872732","todo_member_management" )
        self.cursor = db.cursor()
    
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
        
def addUser(userId, name, passwd, repasswd):
    """
    add user to database
    """
    # check if exists
    if not validateNewId:
        return False
    else:
        try:
            sql = """insert into user value(
                     null,'%s', '%s', sha1('%s'))""" %(userId, name, passwd)
            cursor.execute(sql)
            db.commit()
            return userId
        except:
            db.rollback()
            return False

def validateNewId(userId):
    """
    check if id already exists
    """
    sql = """select userid from user"""
    cursor.execute(sql)
    result = cursor.fetchall()
    existingIds = []
    for oneId in result:
        existingIds.append(oneId[0])
    
    if userId in existingIds:
        return False
    else:
        return True

def validate(userId, passwd):
    """
    check if userId and passwd matches
    """
    sql = """select * from user where userId='%s' and passwd=sha1('%s')""" %(str(userId), str(passwd))
    cursor.execute(sql)
    result = cursor.fetchall()

    if result:
        return True
    else:
        return False