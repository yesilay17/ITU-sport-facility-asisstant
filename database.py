import mysql.connector

mc=mysql.connector.connect(user="root", password ="159753", database="blg317e")

mycursor=mc.cursor()


from objects import User
    
class Database:
    def __init__(self):
        self.__userid = -1

    def add_user(self, user, userid):
        self.__userid=userid
        if(not self.get_user()):   
            mycursor.execute("INSERT INTO user_(userid, username, password_, name_surname, age, status_) VALUES(%d,'%s','%s', '%s', %d, '%s');" %(int(userid),user.username,user.password,user.name_surname ,int(user.age),user.status))
            mc.commit()
            return True
        else:
            self.__userid=-1
            return False

    def get_user(self):
        mycursor.execute("SELECT * FROM blg317e.user_ Where userid=%d" %(int(self.__userid)))
        data=mycursor.fetchall()
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

    def forgot_password(self, userid, username, name_surname, age, status):
        bools=[False, False, False, False, False]
        mycursor.execute("SELECT * FROM blg317e.user_ Where userid=%d and username='%s' and  name_surname='%s' and  age=%d and  status_='%s'" %(int(userid), username ,name_surname, int(age), status))
        data=mycursor.fetchall()
        if(data):
            bools[0]=True
        data=None
        mycursor.execute("SELECT * FROM blg317e.gym Where userid=%d" %(int(userid)))
        data=mycursor.fetchall()
        if(data):
            bools[1]=True
        data=None
        mycursor.execute("SELECT * FROM blg317e.carpet Where userid=%d" %(int(userid)))
        data=mycursor.fetchall()
        if(data):
            bools[2]=True
        data=None
        mycursor.execute("SELECT * FROM blg317e.pool Where userid=%d" %(int(userid)))
        data=mycursor.fetchall()
        if(data):
            bools[3]=True
        data=None
        mycursor.execute("SELECT * FROM blg317e.tennis Where userid=%d" %(int(userid)))
        data=mycursor.fetchall()
        if(data):
            bools[4]=True
        return bools

    def update_password(self, userid, password):
        mycursor.execute("UPDATE user_ SET password_ = '%s' WHERE userid = %d;" %(password, int(userid)))
        mc.commit()


    def get_gym_registration(self):
        mycursor.execute("SELECT * FROM blg317e.gym Where userid=%d" %(int(self.__userid)))
        data=mycursor.fetchall()
        userid=-1
        for row in data:
            gymid=row[0]
            userid=row[1]
        if(userid!=-1):
            return gymid
        else:
            return False

    def get_carpet_registration(self):
        mycursor.execute("SELECT * FROM blg317e.carpet Where userid=%d" %(int(self.__userid)))
        data=mycursor.fetchall()
        userid=-1
        for row in data:
            carpetid=row[0]
            userid=row[1]
        if(userid!=-1):
            return carpetid
        else:
            return False

    def get_pool_registration(self):
        mycursor.execute("SELECT * FROM blg317e.pool Where userid=%d" %(int(self.__userid)))
        data=mycursor.fetchall()
        userid=-1
        for row in data:
            poolid=row[0]
            userid=row[1]
        if(userid!=-1):
            return poolid
        else:
            return False

    def get_tennis_registration(self):
        mycursor.execute("SELECT * FROM blg317e.tennis Where userid=%d" %(int(self.__userid)))
        data=mycursor.fetchall()
        userid=-1
        for row in data:
            tennisid=row[0]
            userid=row[1]
        if(userid!=-1):
            return tennisid
        else:
            return False        

    def check_tennis_res(self, date, time_slot):
        tennis_id=self.get_tennis_registration()
        mycursor.execute("SELECT * FROM blg317e.tennis_res Where tennisid=%d and day_='%s'" %(int(tennis_id), str(date)))
        data=mycursor.fetchall()
        if(data):
            return "You cannot make double reservation for same day."
        else:
            mycursor.execute("INSERT INTO tennis_res(tennisid, day_, time_slot) VALUES(%d, '%s', '%s');" %(int(tennis_id), str(date), str(time_slot)))
            mc.commit()
            return "You have reserved successfully."    
        
    def get_tennis_res_time(self, date):
        mycursor.execute("SELECT * FROM blg317e.tennis_res Where day_='%s'" %(str(date)))
        data=mycursor.fetchall()
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

    def get_tennis_res_user(self):
        tennis_id=self.get_tennis_registration()
        mycursor.execute("SELECT * FROM blg317e.tennis_res Where tennisid=%d" %(int(tennis_id)))
        data=mycursor.fetchall()
        reservation={}
        for row in data:
            reservation[row[2]]=int(row[3])
        return reservation

    def update_tennis_res(self, update_date, new_date, new_time):
        tennis_id=self.get_tennis_registration()
        mycursor.execute("UPDATE tennis_res SET day_ = '%s', time_slot = '%s' WHERE tennisid = %d and day_ = '%s'" %(new_date, new_time, int(tennis_id), update_date))
        mc.commit()
        return "Updated successfully, you can check from the list."

    def delete_tennis_res(self, day):
        tennis_id=self.get_tennis_registration()
        mycursor.execute("DELETE FROM tennis_res WHERE tennisid = %d and day_ = '%s'" %(int(tennis_id), day))
        mc.commit()
        return

    def check_carpet_res(self, date, time_slot):
        carpet_id=self.get_carpet_registration()
        mycursor.execute("SELECT * FROM blg317e.carpet_res Where carpetid=%d and day_='%s'" %(int(carpet_id), str(date)))
        data=mycursor.fetchall()
        if(data):
            return "You cannot make double reservation for same day."
        else:
            mycursor.execute("INSERT INTO carpet_res(carpetid, day_, time_slot) VALUES(%d, '%s', '%s');" %(int(carpet_id), str(date), str(time_slot)))
            mc.commit()
            return "You have reserved successfully."    
        
    def get_carpet_res_time(self, date):
        mycursor.execute("SELECT * FROM blg317e.carpet_res Where day_='%s'" %(str(date)))
        data=mycursor.fetchall()
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

    def get_carpet_res_user(self):
        carpet_id=self.get_carpet_registration()
        mycursor.execute("SELECT * FROM blg317e.carpet_res Where carpetid=%d" %(int(carpet_id)))
        data=mycursor.fetchall()
        reservation={}
        for row in data:
            reservation[row[2]]=int(row[3])
        return reservation

    def update_carpet_res(self, update_date, new_date, new_time):
        carpet_id=self.get_carpet_registration()
        mycursor.execute("UPDATE carpet_res SET day_ = '%s', time_slot = '%s' WHERE carpetid = %d and day_ = '%s'" %(new_date, new_time, int(carpet_id), update_date))
        mc.commit()
        return "Updated successfully, you can check from the list."

    def delete_carpet_res(self, day):
        carpet_id=self.get_carpet_registration()
        mycursor.execute("DELETE FROM carpet_res WHERE carpetid = %d and day_ = '%s'" %(int(carpet_id), day))
        mc.commit()
        return

    def find_user(self, userid, username, password):
        mycursor.execute("SELECT * FROM blg317e.user_ Where userid=%d and username='%s' and  password_='%s'" %(int(userid),username ,password))
        data=mycursor.fetchall()
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
        self.login(userid)    
        user = User(username, password, name_surname, age, status)
        if(user.age!=-1):
            return user
        else:
            return None

    def update_user(self,user,userid):
        temp=self.__userid
        self.__userid=int(userid)
        if(not self.get_user() or int(temp)==int(userid)):
            mycursor.execute("UPDATE user_ SET userid=%d, username = '%s', password_ = '%s', name_surname = '%s', age = %d, status_='%s' WHERE userid = %d;" %(int(userid), user.username,user.password,user.name_surname ,int(user.age),user.status, int(temp)))
            mc.commit()
            return True
        else:
            self.__userid=temp
            return False

    def login(self, userid):
        self.__userid=userid

    def get_login(self):
        return self.__userid    
    
    def sign_out(self):
        self.__userid=-1    

    def delete_user(self):
        mycursor.execute("DELETE FROM user_ WHERE userid = %d;" %(int(self.__userid)))
        mc.commit()
        return

    def delete_gym_registration(self):
        mycursor.execute("DELETE FROM gym WHERE userid = %d;" %(int(self.__userid)))
        mc.commit()
        return

    def delete_carpet_registration(self):
        mycursor.execute("DELETE FROM carpet WHERE userid = %d;" %(int(self.__userid)))
        mc.commit()
        return

    def delete_pool_registration(self):
        mycursor.execute("DELETE FROM pool WHERE userid = %d;" %(int(self.__userid)))
        mc.commit()
        return

    def delete_tennis_registration(self):
        mycursor.execute("DELETE FROM tennis WHERE userid = %d;" %(int(self.__userid)))
        mc.commit()
        return

    def register_to_gym(self):
        if(not self.get_gym_registration()):
            mycursor.execute("INSERT INTO gym(userid) VALUES(%d);" %(int(self.__userid)))
            mc.commit()
            return "You have registred successfully to the gym."
        else:
            return "You have aldready registred!"    

    def register_to_carpet(self):
        if(not self.get_carpet_registration()):
            mycursor.execute("INSERT INTO carpet(userid) VALUES(%d);" %(int(self.__userid)))
            mc.commit()
            return "You have registred successfully to the football field carpet."
        else:
            return "You have aldready registred!"

    def register_to_pool(self):
        if(not self.get_pool_registration()):
            mycursor.execute("INSERT INTO pool(userid) VALUES(%d);" %(int(self.__userid)))
            mc.commit()
            return "You have registred successfully to the swimming pool."
        else:
            return "You have aldready registred!"    

    def register_to_tennis(self):
        if(not self.get_tennis_registration()):
            mycursor.execute("INSERT INTO tennis(userid) VALUES(%d);" %(int(self.__userid)))
            mc.commit()
            return "You have registred successfully to the tennis courts."
        else:
            return "You have aldready registred!"                    

    def this_week_tennis_reservation(self, dates):
        number_of_reservations=[0,0,0,0,0,0,0]
        i=0
        while i<7:
            mycursor.execute("SELECT * FROM blg317e.tennis_res Where day_='%s'" %(str(dates[i])))
            data=mycursor.fetchall()
            for row in data:
                number_of_reservations[i]+=1
            i+=1
        return number_of_reservations

    def this_week_carpet_reservation(self, dates):
        number_of_reservations=[0,0,0,0,0,0,0]
        i=0
        while i<7:
            mycursor.execute("SELECT * FROM blg317e.carpet_res Where day_='%s'" %(str(dates[i])))
            data=mycursor.fetchall()
            for row in data:
                number_of_reservations[i]+=1
            i+=1
        return number_of_reservations