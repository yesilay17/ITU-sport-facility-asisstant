import mysql.connector

from objects import User

sql="""CREATE DATABASE IF NOT EXISTS heroku_263577567345e1f;
USE heroku_263577567345e1f;
CREATE TABLE IF NOT EXISTS user_(
    userid INT NOT NULL UNIQUE,
    username VARCHAR(50) NOT NULL,
    password_ VARCHAR(50) NOT NULL,
    name_surname VARCHAR(50) NOT NULL,
    age INT NOT NULL,
    status_ VARCHAR(50) NOT NULL,
    PRIMARY KEY (userid)
);

CREATE TABLE IF NOT EXISTS gym(
    gymid INT AUTO_INCREMENT NOT NULL,
    userid INT NOT NULL,
    PRIMARY KEY (gymid),
    FOREIGN KEY (userid) 
        REFERENCES user_(userid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS tennis(
    tennisid INT AUTO_INCREMENT NOT NULL,
    userid INT NOT NULL,
    PRIMARY KEY (tennisid),
    FOREIGN KEY (userid) 
        REFERENCES user_(userid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS carpet(
    carpetid INT AUTO_INCREMENT NOT NULL,
    userid INT NOT NULL,
    PRIMARY KEY (carpetid),
    FOREIGN KEY (userid) 
        REFERENCES user_(userid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS pool(
    poolid INT AUTO_INCREMENT NOT NULL,
    userid INT NOT NULL,
    PRIMARY KEY (poolid),
    FOREIGN KEY (userid)
        REFERENCES user_(userid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS carpet_res(
    carpet_res_id INT AUTO_INCREMENT NOT NULL,
    carpetid INT NOT NULL,
    day_ VARCHAR(15) NOT NULL,
    time_slot VARCHAR(15) NOT NULL,
    PRIMARY KEY (carpet_res_id),
    FOREIGN KEY (carpetid) 
        REFERENCES carpet(carpetid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS tennis_res(
    tennis_res_id INT AUTO_INCREMENT NOT NULL,
    tennisid INT NOT NULL,
    day_ VARCHAR(15) NOT NULL,
    time_slot VARCHAR(15) NOT NULL,
    PRIMARY KEY (tennis_res_id),
    FOREIGN KEY (tennisid) 
        REFERENCES tennis(tennisid)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);"""

class Database:
    def __init__(self):
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute(sql, multi=True)
        mc.commit()
        mycursor.close()
        mc.close()

    def add_user(self, user, userid):
        if(not self.get_user(userid)):
            mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
            mycursor=mc.cursor()   
            mycursor.execute("INSERT INTO user_(userid, username, password_, name_surname, age, status_) VALUES(%d,'%s','%s', '%s', %d, '%s');" %(int(userid),user.username,user.password,user.name_surname ,int(user.age),user.status))
            mc.commit()
            mycursor.close()
            mc.close()
            return True
        else:
            return False

    def get_user(self, userid):
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("SELECT * FROM heroku_263577567345e1f.user_ Where userid=%d" %(int(userid)))
        data=mycursor.fetchall()
        mycursor.close()
        mc.close()
        userid=0
        username=""
        password=""
        name_surname=""
        age=-1
        status=""
        for row in data:
            userid=row[0]
            username=row[1]
            password=row[2]
            name_surname=row[3]
            age=row[4]
            status=row[5]
        user = User(username, password, name_surname, age, status)
        if(user.age!=-1):
            return user
        else:
            return None

    def get_status_numbers(self):
        data=[0,0,0,0]
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("SELECT COUNT(userid) FROM heroku_263577567345e1f.user_ where status_='ITU student';")
        num=mycursor.fetchall()
        if (num):
            data[0]=int(num[0][0])
        mycursor.execute("SELECT COUNT(userid) FROM heroku_263577567345e1f.user_ where status_='Staff';")
        num=mycursor.fetchall()
        if (num):
            data[1]=int(num[0][0])
        mycursor.execute("SELECT COUNT(userid) FROM heroku_263577567345e1f.user_ where status_='Grad student';")
        num=mycursor.fetchall()
        if (num):
            data[2]=int(num[0][0])
        mycursor.execute("SELECT COUNT(userid) FROM heroku_263577567345e1f.user_ where status_='Guest';")
        num=mycursor.fetchall()
        if (num):
            data[3]=int(num[0][0])
        mycursor.close()
        mc.close()
        return data



    def forgot_password(self, userid, username, name_surname, age, status):
        bools=[False, False, False, False, False]
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("SELECT * FROM heroku_263577567345e1f.user_ Where userid=%d and username='%s' and  name_surname='%s' and  age=%d and  status_='%s'" %(int(userid), username ,name_surname, int(age), status))
        data=mycursor.fetchall()
        mycursor.close()
        mc.close()
        if(data):
            bools[0]=True
        data=None
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("SELECT * FROM heroku_263577567345e1f.gym Where userid=%d" %(int(userid)))
        data=mycursor.fetchall()
        mycursor.close()
        mc.close()
        if(data):
            bools[1]=True
        data=None
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("SELECT * FROM heroku_263577567345e1f.carpet Where userid=%d" %(int(userid)))
        data=mycursor.fetchall()
        mycursor.close()
        mc.close()
        if(data):
            bools[2]=True
        data=None
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("SELECT * FROM heroku_263577567345e1f.pool Where userid=%d" %(int(userid)))
        data=mycursor.fetchall()
        mycursor.close()
        mc.close()
        if(data):
            bools[3]=True
        data=None
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("SELECT * FROM heroku_263577567345e1f.tennis Where userid=%d" %(int(userid)))
        data=mycursor.fetchall()
        mycursor.close()
        mc.close()
        if(data):
            bools[4]=True
        return bools

    def update_password(self, userid, password):
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("UPDATE user_ SET password_ = '%s' WHERE userid = %d;" %(password, int(userid)))
        mc.commit()
        mycursor.close()
        mc.close()


    def get_gym_registration(self, userid):
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("SELECT * FROM heroku_263577567345e1f.gym Where userid=%d" %(int(userid)))
        data=mycursor.fetchall()
        mycursor.close()
        mc.close()
        userid=-1
        for row in data:
            gymid=row[0]
            userid=row[1]
        if(userid!=-1):
            return gymid
        else:
            return False

    def get_carpet_registration(self, userid):
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("SELECT * FROM heroku_263577567345e1f.carpet Where userid=%d" %(int(userid)))
        data=mycursor.fetchall()
        mycursor.close()
        mc.close()
        userid=-1
        for row in data:
            carpetid=row[0]
            userid=row[1]
        if(userid!=-1):
            return carpetid
        else:
            return False

    def get_pool_registration(self, userid):
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("SELECT * FROM heroku_263577567345e1f.pool Where userid=%d" %(int(userid)))
        data=mycursor.fetchall()
        mycursor.close()
        mc.close()
        userid=-1
        for row in data:
            poolid=row[0]
            userid=row[1]
        if(userid!=-1):
            return poolid
        else:
            return False

    def get_tennis_registration(self, userid):
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("SELECT * FROM heroku_263577567345e1f.tennis Where userid=%d" %(int(userid)))
        data=mycursor.fetchall()
        mycursor.close()
        mc.close()
        userid=-1
        for row in data:
            tennisid=row[0]
            userid=row[1]
        if(userid!=-1):
            return tennisid
        else:
            return False        

    def check_tennis_res(self, date, time_slot, userid):
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("SELECT * FROM heroku_263577567345e1f.tennis INNER JOIN heroku_263577567345e1f.tennis_res Where tennis_res.tennisid=tennis.tennisid and day_='%s' and userid=%d " %(str(date), int(userid)))
        data=mycursor.fetchall()
        mycursor.close()
        mc.close()
        if(data):
            return "You cannot make double reservation for same day."
        else:
            tennis_id=self.get_tennis_registration(userid)
            mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
            mycursor=mc.cursor()
            mycursor.execute("INSERT INTO tennis_res(tennisid, day_, time_slot) VALUES(%d, '%s', '%s');" %(int(tennis_id), str(date), str(time_slot)))
            mc.commit()
            mycursor.close()
            mc.close()
            return "You have reserved successfully."    
        
    def get_tennis_res_time(self, date):
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("SELECT * FROM heroku_263577567345e1f.tennis_res Where day_='%s'" %(str(date)))
        data=mycursor.fetchall()
        mycursor.close()
        mc.close()
        time_slot=[False, False, False, False]
        for row in data:
            if int(row[3])==8:
                time_slot[0]=True
            elif int(row[3])==10:
                time_slot[1]=True
            elif int(row[3])==12:
                time_slot[2]=True
            elif int(row[3])==14:
                time_slot[3]=True    
        return time_slot

    def get_tennis_res_user(self, userid):
        tennis_id=self.get_tennis_registration(userid)
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("SELECT * FROM heroku_263577567345e1f.tennis_res Where tennisid=%d" %(int(tennis_id)))
        data=mycursor.fetchall()
        mycursor.close()
        mc.close()
        reservation={}
        for row in data:
            reservation[row[2]]=int(row[3])
        return reservation

    def update_tennis_res(self, update_date, new_date, new_time, userid):
        tennis_id=self.get_tennis_registration(userid)
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("UPDATE tennis_res SET day_ = '%s', time_slot = '%s' WHERE tennisid = %d and day_ = '%s'" %(new_date, new_time, int(tennis_id), update_date))
        mc.commit()
        mycursor.close()
        mc.close()
        return "Updated successfully, you can check from the list."

    def delete_tennis_res(self, day, userid):
        tennis_id=self.get_tennis_registration(userid)
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("DELETE FROM tennis_res WHERE tennisid = %d and day_ = '%s'" %(int(tennis_id), day))
        mc.commit()
        mycursor.close()
        mc.close()
        return

    def check_carpet_res(self, date, time_slot, userid):  
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("SELECT * FROM heroku_263577567345e1f.carpet INNER JOIN heroku_263577567345e1f.carpet_res Where carpet_res.carpetid=carpet.carpetid and day_='%s' and userid=%d " %(str(date), int(userid)))
        data=mycursor.fetchall()
        mycursor.close()
        mc.close()
        if(data):
            return "You cannot make double reservation for same day."
        else:
            carpet_id=self.get_carpet_registration(userid)
            mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
            mycursor=mc.cursor()
            mycursor.execute("INSERT INTO carpet_res(carpetid, day_, time_slot) VALUES(%d, '%s', '%s');" %(int(carpet_id), str(date), str(time_slot)))
            mc.commit()
            mycursor.close()
            mc.close()
            return "You have reserved successfully."    
        
    def get_carpet_res_time(self, date):
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("SELECT * FROM heroku_263577567345e1f.carpet_res Where day_='%s'" %(str(date)))
        data=mycursor.fetchall()
        mycursor.close()
        mc.close()
        time_slot=[False, False, False, False]
        for row in data:
            if int(row[3])==17:
                time_slot[0]=True
            elif int(row[3])==18:
                time_slot[1]=True
            elif int(row[3])==19:
                time_slot[2]=True
            elif int(row[3])==20:
                time_slot[3]=True          
        return time_slot

    def get_carpet_res_user(self, userid):
        carpet_id=self.get_carpet_registration(userid)
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("SELECT * FROM heroku_263577567345e1f.carpet_res Where carpetid=%d" %(int(carpet_id)))
        data=mycursor.fetchall()
        mycursor.close()
        mc.close()
        reservation={}
        for row in data:
            reservation[row[2]]=int(row[3])
        return reservation

    def update_carpet_res(self, update_date, new_date, new_time, userid):
        carpet_id=self.get_carpet_registration(userid)
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("UPDATE carpet_res SET day_ = '%s', time_slot = '%s' WHERE carpetid = %d and day_ = '%s'" %(new_date, new_time, int(carpet_id), update_date))
        mc.commit()
        mycursor.close()
        mc.close()
        return "Updated successfully, you can check from the list."

    def delete_carpet_res(self, day, userid):
        carpet_id=self.get_carpet_registration(userid)
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("DELETE FROM carpet_res WHERE carpetid = %d and day_ = '%s'" %(int(carpet_id), day))
        mc.commit()
        mycursor.close()
        mc.close()
        return

    def find_user(self, userid, username, password):
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("SELECT * FROM heroku_263577567345e1f.user_ Where userid=%d and username='%s' and  password_='%s'" %(int(userid),username ,password))
        data=mycursor.fetchall()
        mycursor.close()
        mc.close()
        userid=0
        username=""
        password=""
        name_surname=""
        age=-1
        status=""
        for row in data:
            userid=row[0]
            username=row[1]
            password=row[2]
            name_surname=row[3]
            age=row[4]
            status=row[5]    
        user = User(username, password, name_surname, age, status)
        if(user.age!=-1):
            return user
        else:
            return None

    def update_user(self,user,userid, old_userid):
        if((not self.get_user(userid)) or (int(userid)==int(old_userid))):
            mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
            mycursor=mc.cursor()
            mycursor.execute("UPDATE user_ SET userid=%d, username = '%s', password_ = '%s', name_surname = '%s', age = %d, status_='%s' WHERE userid = %d;" %(int(userid), user.username,user.password,user.name_surname ,int(user.age),user.status, int(old_userid)))
            mc.commit()
            mycursor.close()
            mc.close()
            return True
        else:
            return False
 

    def delete_user(self, userid):
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("DELETE FROM user_ WHERE userid = %d;" %(int(userid)))
        mc.commit()
        mycursor.close()
        mc.close()
        return

    def delete_gym_registration(self, userid):
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("DELETE FROM gym WHERE userid = %d;" %(int(userid)))
        mc.commit()
        mycursor.close()
        mc.close()
        return

    def delete_carpet_registration(self, userid):
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("DELETE FROM carpet WHERE userid = %d;" %(int(userid)))
        mc.commit()
        mycursor.close()
        mc.close()
        return

    def delete_pool_registration(self, userid):
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("DELETE FROM pool WHERE userid = %d;" %(int(userid)))
        mc.commit()
        mycursor.close()
        mc.close()
        return

    def delete_tennis_registration(self, userid):
        mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
        mycursor=mc.cursor()
        mycursor.execute("DELETE FROM tennis WHERE userid = %d;" %(int(userid)))
        mc.commit()
        mycursor.close()
        mc.close()
        return

    def register_to_gym(self, userid):
        if(not self.get_gym_registration(userid)):
            mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
            mycursor=mc.cursor()
            mycursor.execute("INSERT INTO gym(userid) VALUES(%d);" %(int(userid)))
            mc.commit()
            mycursor.close()
            mc.close()
            return "You have registred successfully to the gym."
        else:
            return "You have aldready registred!"    

    def register_to_carpet(self, userid):
        if(not self.get_carpet_registration(userid)):
            mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
            mycursor=mc.cursor()
            mycursor.execute("INSERT INTO carpet(userid) VALUES(%d);" %(int(userid)))
            mc.commit()
            mycursor.close()
            mc.close()
            return "You have registred successfully to the football field carpet."
        else:
            return "You have aldready registred!"

    def register_to_pool(self, userid):
        if(not self.get_pool_registration(userid)):
            mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
            mycursor=mc.cursor()
            mycursor.execute("INSERT INTO pool(userid) VALUES(%d);" %(int(userid)))
            mc.commit()
            mycursor.close()
            mc.close()
            return "You have registred successfully to the swimming pool."
        else:
            return "You have aldready registred!"    

    def register_to_tennis(self, userid):
        if(not self.get_tennis_registration(userid)):
            mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
            mycursor=mc.cursor()
            mycursor.execute("INSERT INTO tennis(userid) VALUES(%d);" %(int(userid)))
            mc.commit()
            mycursor.close()
            mc.close()
            return "You have registred successfully to the tennis courts."
        else:
            return "You have aldready registred!"                    

    def this_week_tennis_reservation(self, dates):
        number_of_reservations=[0,0,0,0,0,0,0]
        i=0
        while i<7:
            mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
            mycursor=mc.cursor()
            mycursor.execute("SELECT * FROM heroku_263577567345e1f.tennis_res Where day_='%s'" %(str(dates[i])))
            data=mycursor.fetchall()
            mycursor.close()
            mc.close()
            for row in data:
                number_of_reservations[i]+=1
            i+=1
        return number_of_reservations

    def this_week_carpet_reservation(self, dates):
        number_of_reservations=[0,0,0,0,0,0,0]
        i=0
        while i<7:
            mc=mysql.connector.connect(host="eu-cdbr-west-03.cleardb.net", user="b801b6ee025905", password ="f189b700", database="heroku_263577567345e1f")
            mycursor=mc.cursor()
            mycursor.execute("SELECT * FROM heroku_263577567345e1f.carpet_res Where day_='%s'" %(str(dates[i])))
            data=mycursor.fetchall()
            mycursor.close()
            mc.close()
            for row in data:
                number_of_reservations[i]+=1
            i+=1
        return number_of_reservations