from datetime import datetime, timedelta

from flask import current_app, render_template, redirect, request, url_for, session

import numpy as np

import random

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from objects import User
"""
def convert_date(date):
    s = ''.join(x for x in date if x.isdigit())
    full_date =int(s)
    year=int(full_date/10000)
    month=int((full_date/100)%100)
    day=int(full_date%100)
    _date_=[year,month,day]
    return _date_  """

def home_page():
    db = current_app.config["db"]
    today = datetime.today()
    day_name = today.strftime("%A")
    if("userid" in session):
        user=db.get_user(int(session["userid"]))
        return render_template("home.html", day=day_name, name=None, username=user.username, user=user)
    else:
        return render_template("home.html", day=day_name, name=None)

def gym_page():
    db = current_app.config["db"]
    if("userid" in session):
        user=db.get_user(int(session["userid"]))
        return render_template("gym.html", username=user.username)
    else:
        return render_template("gym.html")

def carpet_page():
    db = current_app.config["db"]
    if("userid" in session):
        user=db.get_user(int(session["userid"]))
        register=db.get_carpet_registration(int(session["userid"]))
        return render_template("carpet.html", username=user.username, register=register)
    else:
        return render_template("carpet.html")

def pool_page():
    db = current_app.config["db"]
    if("userid" in session):
        user=db.get_user(int(session["userid"]))
        return render_template("pool.html", username=user.username)
    else:
        return render_template("pool.html")
    
def tennis_page():
    db = current_app.config["db"]
    if("userid" in session):
        user=db.get_user(int(session["userid"]))
        register=db.get_tennis_registration(int(session["userid"]))
        return render_template("tennis.html", username=user.username, register=register)
    else:
        return render_template("tennis.html")

def register_gym():
    db = current_app.config["db"]
    message=db.register_to_gym(int(session["userid"]))
    user=db.get_user(int(session["userid"]))
    return render_template("gym.html", username=user.username, message=message)

def register_carpet():
    db = current_app.config["db"]
    message=db.register_to_carpet(int(session["userid"]))
    user=db.get_user(int(session["userid"]))
    register=db.get_carpet_registration(int(session["userid"]))
    return render_template("carpet.html", username=user.username, message=message, register=register)    

def register_pool():
    db = current_app.config["db"]
    message=db.register_to_pool(int(session["userid"]))
    user=db.get_user(int(session["userid"]))
    return render_template("pool.html", username=user.username, message=message)

def register_tennis():
    db = current_app.config["db"]
    message=db.register_to_tennis(int(session["userid"]))
    user=db.get_user(int(session["userid"]))
    register=db.get_tennis_registration(int(session["userid"]))
    return render_template("tennis.html", username=user.username, message=message, register=register)

def get_min_date():
    today = datetime.now()
    today_month=""
    today_day=""
    if(today.month<10):
        today_month+="0"
    if(today.day<10):
        today_day+="0"
    today_month+=str(today.month)
    today_day+=str(today.day)    
    min_date=(str(today.year)+"-"+str(today_month)+"-"+str(today_day))
    return min_date

def get_max_date():
    today = datetime.now()
    a_week_later = today + timedelta(days=6)
    max_month=""
    max_day=""
    if(a_week_later.month<10):
        max_month+="0"
    if(a_week_later.day<10):
        max_day+="0"   
    max_month+=str(a_week_later.month)
    max_day+=str(a_week_later.day)    
    max_date=(str(a_week_later.year)+"-"+str(max_month)+"-"+str(max_day))
    return max_date 

def reservation_tennis():
    db = current_app.config["db"]
    user=db.get_user(int(session["userid"]))
    min_date=get_min_date()
    max_date=get_max_date()
    this_week_dates=get_this_week()
    number_of_reservations = db.this_week_tennis_reservation(this_week_dates)
    day_names=day_names_of_this_week()
    rand=plot_tennis_res(number_of_reservations, day_names)
    if request.method =="GET":
        return render_template(
            "tennis_reservation.html", 
            username=user.username,
            min_date=min_date,
            max_date=max_date,
            image="static/tennis_res.jpeg?foo="+str(rand)
        )
    else:
        date = request.form.get("date")
        message=""
        if(not date):
            date_ = request.form.get("date_")
            time_slot = request.form.getlist("time_slot")
            i=0
            for time in time_slot:
                if i==1:
                    message="You cannot make double reservation for same day, only first reservation is accepted!"
                    break
                message = db.check_tennis_res(date_, time, int(session["userid"]))
                i+=1
        this_week_dates=get_this_week()
        number_of_reservations = db.this_week_tennis_reservation(this_week_dates)
        day_names=day_names_of_this_week()
        rand=plot_tennis_res(number_of_reservations, day_names)
        res_list=db.get_tennis_res_time(date)
        return render_template(
            "tennis_reservation.html", 
            username=user.username,
            max_date=max_date,
            min_date=min_date,
            date=date,
            message=message,
            reserved=res_list,
            image="static/tennis_res.jpeg?foo="+str(rand)
        )

def get_this_week():
    this_week = []
    today = datetime.now()
    dates=["","","","","","",""]
    month=["","","","","","",""]
    day=["","","","","","",""]
    i=0
    while i<7:
        this_week.append(today + timedelta(days=i))      
        if(this_week[i].month<10):
            month[i]+="0"
        if(this_week[i].day<10):
            day[i]+="0"
        month[i]+=str(this_week[i].month)
        day[i]+=str(this_week[i].day)
        dates[i] = (str(this_week[i].year)+"-"+str(month[i])+"-"+str(day[i]))
        i+=1
    return dates

def day_names_of_this_week():
    this_week = []
    day_name=[]
    today = datetime.now()
    i=0
    while i<7:
        this_week.append(today + timedelta(days=i)) 
        day_name.append(this_week[i].strftime("%a"))
        i+=1
    return day_name

def plot_tennis_res(number_of_reservations, day_name):
    plt.clf()
    y_pos=np.arange(len(day_name))
    rand=random.randrange(0,1000)
    plt.xticks(y_pos, day_name)
    plt.ylabel("Number of reservations")
    plt.title("THIS WEEK TENNIS COURT RESERVATIONS")
    plt.bar(y_pos, number_of_reservations)
    plt.ylim([0,4])
    plt.savefig("static/tennis_res.jpeg", dpi=150)
    return rand

def plot_carpet_res(number_of_reservations, day_name):
    plt.clf()
    y_pos=np.arange(len(day_name))
    rand=random.randrange(0,1000)
    plt.xticks(y_pos, day_name)
    plt.ylabel("Number of carpet reservations")
    plt.title("THIS WEEK FOOTBALL FIELD CARPET RESERVATIONS")
    plt.bar(y_pos, number_of_reservations)
    plt.ylim([0,4])
    plt.savefig("static/carpet_res.jpeg", dpi=150)
    return rand

def reservation_carpet():
    db = current_app.config["db"]
    user=db.get_user(int(session["userid"]))
    min_date=get_min_date()
    max_date=get_max_date()
    this_week_dates=get_this_week()
    number_of_reservations = db.this_week_carpet_reservation(this_week_dates)
    day_names=day_names_of_this_week()
    rand=plot_carpet_res(number_of_reservations, day_names)
    if request.method =="GET":
        return render_template(
            "carpet_reservation.html", 
            username=user.username,
            min_date=min_date,
            max_date=max_date,
            image="static/carpet_res.jpeg?foo="+str(rand)
        )
    else:
        date = request.form.get("date")
        res_list=db.get_carpet_res_time(date)
        message=""
        if(not date):
            date_ = request.form.get("date_")
            time_slot = request.form.getlist("time_slot")
            i=0
            for time in time_slot:
                if i==1:
                    message="You cannot make double reservation for same day, only first reservation is accepted!"
                    break
                message = db.check_carpet_res(date_, time, int(session["userid"]))
                i+=1
        this_week_dates=get_this_week()
        number_of_reservations = db.this_week_carpet_reservation(this_week_dates)
        day_names=day_names_of_this_week()
        rand=plot_carpet_res(number_of_reservations, day_names)
        return render_template(
            "carpet_reservation.html", 
            username=user.username,
            max_date=max_date,
            min_date=min_date,
            date=date,
            message=message,
            reserved=res_list,
            image="static/carpet_res.jpeg?foo="+str(rand)
        )

def carpet_res_manage():
    db = current_app.config["db"]
    carpet_res=db.get_carpet_res_user(int(session["userid"]))
    user=db.get_user(int(session["userid"]))
    sorted_date=sorted(carpet_res)
    if request.method == "GET":
        return render_template(
                "carpet_res_manage.html",
                carpet_res=carpet_res,
                username=user.username,
                sorted_date=sorted_date
            )
    else:
        dates = request.form.getlist("dates")
        update = request.form.get("update")
        delete = request.form.get("delete")
        i=0
        message=""
        flag=True
        if update!=None:
            for time in dates:
                if i==1:
                    message="You cannot update two or more reservation at the same time! Please update one by one."
                    flag=False
                    break
                i+=1
            if not dates:
                flag=False
                message="You have to select at least one reservation to update."
            if flag:
                return update_carpet_res(dates[0])
        elif delete!=None:
            for time in dates:
                db.delete_carpet_res(time)
            if not dates:
                message="You have to select at least one reservation to delete."
        else:
            user=db.get_user(int(session["userid"]))
            min_date=get_min_date()
            max_date=get_max_date()
            date = request.form.get("date")
            update_date = request.form.get("update_date")
            message="Reservation dated "+update_date+" will be updated."
            if(not date):
                new_date = request.form.get("date_")
                new_time_slot = request.form.getlist("time_slot")    
                message=db.update_carpet_res(update_date, new_date, new_time_slot[0], int(session["userid"]))
                carpet_res=db.get_carpet_res_user(int(session["userid"]))
                user=db.get_user(int(session["userid"]))
                sorted_date=sorted(carpet_res)
                return render_template(
                        "carpet_res_manage.html",
                        carpet_res=carpet_res,
                        username=user.username,
                        sorted_date=sorted_date,
                        message=message
                    )
            this_week_dates=get_this_week()
            number_of_reservations = db.this_week_carpet_reservation(this_week_dates)
            day_names=day_names_of_this_week()
            rand=plot_carpet_res(number_of_reservations, day_names)
            res_list=db.get_carpet_res_time(date)
            return render_template(
                "carpet_reservation.html", 
                username=user.username,
                min_date=min_date,
                max_date=max_date,
                date=date,
                message=message,
                reserved=res_list,
                update_date = update_date,
                image="static/carpet_res.jpeg?foo="+str(rand)
            )
        carpet_res=db.get_carpet_res_user(int(session["userid"]))
        user=db.get_user(int(session["userid"]))
        sorted_date=sorted(carpet_res)
        return render_template(
                "carpet_res_manage.html",
                carpet_res=carpet_res,
                username=user.username,
                sorted_date=sorted_date,
                message=message
            )

def update_carpet_res(update_date):
    db = current_app.config["db"]
    user=db.get_user(int(session["userid"]))
    min_date=get_min_date()
    max_date=get_max_date()
    this_week_dates=get_this_week()
    number_of_reservations = db.this_week_carpet_reservation(this_week_dates)
    day_names=day_names_of_this_week()
    rand=plot_carpet_res(number_of_reservations, day_names)
    return render_template(
        "carpet_reservation.html", 
        username=user.username,
        min_date=min_date,
        max_date=max_date,
        update_date=update_date,
        image="static/carpet_res.jpeg?foo="+str(rand)
    )

def tennis_res_manage():
    db = current_app.config["db"]
    if request.method == "GET":
        tennis_res=db.get_tennis_res_user(int(session["userid"]))
        user=db.get_user(int(session["userid"]))
        sorted_date=sorted(tennis_res)
        return render_template(
                "tennis_res_manage.html",
                tennis_res=tennis_res,
                username=user.username,
                sorted_date=sorted_date
            )
    else:
        dates = request.form.getlist("dates")
        update = request.form.get("update")
        delete = request.form.get("delete")
        i=0
        message=""
        flag=True
        if update!=None:
            for time in dates:
                if i==1:
                    message="You cannot update two or more reservation at the same time! Please update one by one."
                    flag=False
                    break
                i+=1
            if not dates:
                flag=False
                message="You have to select at least one reservation to update."
            if flag:
                return update_tennis_res(dates[0])
        elif delete!=None:
            for time in dates:
                db.delete_tennis_res(time)
            if not dates:
                message="You have to select at least one reservation to delete."
        else:
            db = current_app.config["db"]
            user=db.get_user(int(session["userid"]))
            min_date=get_min_date()
            max_date=get_max_date()
            date = request.form.get("date")
            update_date = request.form.get("update_date")
            this_week_dates=get_this_week()
            number_of_reservations = db.this_week_tennis_reservation(this_week_dates)
            day_names=day_names_of_this_week()
            rand=plot_tennis_res(number_of_reservations, day_names)
            message="Reservation dated "+update_date+" will be updated."
            if(not date):
                new_date = request.form.get("date_")
                new_time_slot = request.form.getlist("time_slot")    
                message=db.update_tennis_res(update_date, new_date, new_time_slot[0], int(session["userid"]))
                tennis_res=db.get_tennis_res_user(int(session["userid"]))
                user=db.get_user(int(session["userid"]))
                sorted_date=sorted(tennis_res)
                return render_template(
                        "tennis_res_manage.html",
                        tennis_res=tennis_res,
                        username=user.username,
                        sorted_date=sorted_date,
                        message=message
                    )
            this_week_dates=get_this_week()
            number_of_reservations = db.this_week_tennis_reservation(this_week_dates)
            day_names=day_names_of_this_week()
            rand=plot_tennis_res(number_of_reservations, day_names)
            res_list=db.get_tennis_res_time(date)
            return render_template(
                "tennis_reservation.html", 
                username=user.username,
                min_date=min_date,
                max_date=max_date,
                date=date,
                message=message,
                reserved=res_list,
                update_date = update_date,
                image="static/tennis_res.jpeg?foo="+str(rand)
            )
        tennis_res=db.get_tennis_res_user(int(session["userid"]))
        user=db.get_user(int(session["userid"]))
        sorted_date=sorted(tennis_res)
        return render_template(
                "tennis_res_manage.html",
                tennis_res=tennis_res,
                username=user.username,
                sorted_date=sorted_date,
                message=message
            )

def update_tennis_res(update_date):
    db = current_app.config["db"]
    user=db.get_user(int(session["userid"]))
    min_date=get_min_date()
    max_date=get_max_date()
    this_week_dates=get_this_week()
    number_of_reservations = db.this_week_tennis_reservation(this_week_dates)
    day_names=day_names_of_this_week()
    rand=plot_tennis_res(number_of_reservations, day_names)
    return render_template(
        "tennis_reservation.html", 
        username=user.username,
        min_date=min_date,
        max_date=max_date,
        update_date=update_date,
        image="static/tennis_res.jpeg?foo="+str(rand)
    )
    

def user_page():
    db = current_app.config["db"]
    user=db.get_user(int(session["userid"]))
    gym=db.get_gym_registration(int(session["userid"]))
    carpet=db.get_carpet_registration(int(session["userid"]))
    pool=db.get_pool_registration(int(session["userid"]))
    tennis=db.get_tennis_registration(int(session["userid"]))
    carpet_res=db.get_carpet_res_user(int(session["userid"]))
    tennis_res=db.get_tennis_res_user(int(session["userid"]))
    return render_template(
                "user.html",
                userid=int(session["userid"]),
                user=user,
                username=user.username,
                gym=gym,
                carpet=carpet,
                pool=pool,
                tennis=tennis,
                tennis_res=tennis_res,
                carpet_res=carpet_res
    )

def update_user():
    db = current_app.config["db"]
    if request.method == "GET":
        user=db.get_user(int(session["userid"]))
        return render_template(
                "user.html",
                user=user,
                userid=int(session["userid"]),
                update="active"
        )
    else:
        userid = request.form.get("userid")
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        name_surname = request.form.get("name_surname")
        age = request.form.get("age")
        status = request.form.get("status", "").strip()
        user = User(username, password, name_surname, int(age), status)
        if(db.update_user(user, userid, int(session["userid"]))):
            session["userid"]=userid
            return user_page()
        else:
            return render_template(
                "user.html",
                user=user,
                userid=int(session["userid"]),
                update="active",
                message="This userid is used by another account, please select another one."
                )
            
def login_page():
    db = current_app.config["db"]
    if request.method == "GET":
        if("userid" in session):
            user=db.get_user(int(session["userid"]))
            return render_template(
                "login.html",
                userid=int(session["userid"]),
                username=user.username
            )
        else:
            return render_template(
                "login.html"
            )        
    else:
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        userid = request.form.get("userid")
        user=db.find_user(userid,username,password)
        today = datetime.today()
        day_name = today.strftime("%A")
        if(user!=None):
            session["userid"]=userid
            print("Login__userid", int(session["userid"]))
            user=db.get_user(int(session["userid"]))
            return render_template("home.html", day=day_name, username=user.username, user=user)
        else:    
            db.sign_out()
            return render_template("login.html", wrong_data="Incorrect userid or username or password.")

def forgot_password():
    db = current_app.config["db"]
    if request.method == "GET":
        values={"userid": "", "username": "", "name_surname": "", "age": "", "status": ""}
        return render_template(
            "forgot_password.html",
            values=values
            )
    else:
        username = request.form.get("username", "").strip()
        userid = request.form.get("userid")
        name_surname = request.form.get("name_surname")
        age = request.form.get("age")
        status = request.form.get("status", "").strip()
        gym_reg = request.form.get("gym_reg")
        carpet_reg = request.form.get("carpet_reg")
        pool_reg = request.form.get("pool_reg")
        tennis_reg = request.form.get("tennis_reg")
        bools=db.forgot_password(userid, username, name_surname, age, status)
        bool_1=False
        bool_2=False
        bool_3=False
        bool_4=False
        if ((bools[1]==False and gym_reg=="no") or (bools[1]!=False and gym_reg=="yes")):
            bool_1=True
        if ((bools[2]==False and carpet_reg=="no") or (bools[2]!=False and carpet_reg=="yes")):
            bool_2=True
        if ((bools[3]==False and pool_reg=="no") or (bools[3]!=False and pool_reg=="yes")):
            bool_3=True
        if ((bools[4]==False and tennis_reg=="no") or (bools[4]!=False and tennis_reg=="yes")):
            bool_4=True
        if(bool_1 and bool_2 and bool_3 and bool_4 and bools[0]):
            return redirect(url_for("update_password", userid=int(userid)))
        else:
            values={"userid": userid, "username": username, "name_surname": name_surname, "age": int(age), "status": status}
            return render_template(
            "forgot_password.html",
            message="No matching for that user!",
            values=values
            )

def update_password(userid):
    db = current_app.config["db"]
    if request.method == "GET":
        return render_template(
            "update_password.html"
            )
    else:
        password1 = request.form.get("password1", "").strip()
        password2 = request.form.get("password2", "").strip()
        if(password1==password2):
            db.update_password(userid, password1)
            return redirect(url_for("home_page"))
        else:
            return render_template(
            "update_password.html",
            message="Passwords do not match!"
            )

def user_add_page():
    if request.method == "GET":
        values={"username": "", "password": "", "name_surname": "", "age": "", "status": ""}
        return render_template(
            "register.html",
            min_age=0,
            values=values
        )
    else:
        db = current_app.config["db"]
        username = request.form.get("username", "").strip()
        userid = request.form.get("userid")
        password = request.form.get("password", "").strip()
        name_surname = request.form.get("name_surname")
        age = request.form.get("age")
        status = request.form.get("status", "").strip()
        user = User(username, password, name_surname, age, status)
        new_user=db.add_user(user, userid)
        today = datetime.today()
        day_name = today.strftime("%A")
        values={"username": username, "password": password, "name_surname": name_surname, "age": age, "status": status}
        if(new_user):
            if "userid" in session:
                session.pop("userid", None)
            return render_template("home.html", day=day_name, name=name_surname, userid=userid)
        else:    
            return render_template("register.html", warning="This userid is used by another user, please try another one.", values=values)

def delete_user():
    if request.method == "GET":
        warning1="Your reservations and registrations will be deleted too, are you sure?"
        return render_template("user.html", warning1=warning1)
    else:
        db = current_app.config["db"]
        db.delete_user(int(session["userid"]))
        return sign_out()

def delete_gym_reg():
    if request.method == "GET":
        warning1="Are you sure?"
        return render_template("user.html", warning1=warning1)
    else:
        db = current_app.config["db"]
        db.delete_gym_registration(int(session["userid"]))
        return user_page()

def delete_carpet_reg():
    if request.method == "GET":
        warning1="Your reservations will be deleted too, are you sure?"
        return render_template("user.html", warning1=warning1)
    else:
        db = current_app.config["db"]
        db.delete_carpet_registration(int(session["userid"]))
        return user_page()

def delete_pool_reg():
    if request.method == "GET":
        warning1="Are you sure?"
        return render_template("user.html", warning1=warning1)
    else:
        db = current_app.config["db"]
        db.delete_pool_registration(int(session["userid"]))
        return user_page()

def delete_tennis_reg():
    if request.method == "GET":
        warning1="Your reservations will be deleted too, are you sure?"
        return render_template("user.html", warning1=warning1)
    else:
        db = current_app.config["db"]
        db.delete_tennis_registration(int(session["userid"]))
        return user_page()

def sign_out():
    if "userid" in session:
        session.pop("userid", None)
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name, name=None)
