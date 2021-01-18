from flask import Flask

import views
#import mysql.connector
from database import Database
    
app = Flask(__name__)
app.secret_key="secret"

app.add_url_rule("/", view_func=views.home_page)
app.add_url_rule("/gym", view_func=views.gym_page)
app.add_url_rule("/carpet", view_func=views.carpet_page)
app.add_url_rule("/pool", view_func=views.pool_page)
app.add_url_rule("/tennis", view_func=views.tennis_page)
app.add_url_rule("/register", view_func=views.user_add_page, methods=["GET", "POST"])
app.add_url_rule("/login", view_func=views.login_page, methods=["GET", "POST"])
app.add_url_rule("/sign_out", view_func=views.sign_out, methods=["GET", "POST"])
app.add_url_rule("/forgot_password", view_func=views.forgot_password, methods=["GET", "POST"])
app.add_url_rule("/update_password<int:userid>", view_func=views.update_password, methods=["GET", "POST"])
app.add_url_rule("/register_gym", view_func=views.register_gym)
app.add_url_rule("/register_carpet", view_func=views.register_carpet)
app.add_url_rule("/register_pool", view_func=views.register_pool)
app.add_url_rule("/register_tennis", view_func=views.register_tennis)
app.add_url_rule("/user", view_func=views.user_page)
app.add_url_rule("/update_user", view_func=views.update_user, methods=["GET", "POST"])
app.add_url_rule("/delete_user", view_func=views.delete_user, methods=["GET", "POST"])
app.add_url_rule("/delete_gym_registration", view_func=views.delete_gym_reg, methods=["GET", "POST"])
app.add_url_rule("/delete_pool_registration", view_func=views.delete_pool_reg, methods=["GET", "POST"])
app.add_url_rule("/delete_carpet_registration", view_func=views.delete_carpet_reg, methods=["GET", "POST"])
app.add_url_rule("/delete_tennis_registration", view_func=views.delete_tennis_reg, methods=["GET", "POST"])
app.add_url_rule("/reservation_tennis", view_func=views.reservation_tennis, methods=["GET", "POST"])
app.add_url_rule("/reservation_carpet", view_func=views.reservation_carpet, methods=["GET", "POST"])
app.add_url_rule("/tennis_res_manage", view_func=views.tennis_res_manage, methods=["GET", "POST"])
app.add_url_rule("/carpet_res_manage", view_func=views.carpet_res_manage, methods=["GET", "POST"])

db = Database()
app.config["db"] = db


if __name__ == "__main__":
    app.run()