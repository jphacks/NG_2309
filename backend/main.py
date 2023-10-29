from flask import *
from dotenv import load_dotenv
from pathlib import Path
import requests
import githubinfo
from model.model_create import calculate_anmalous_percent
import os
import db
import gpt

base_dir = "../"

load_dotenv(f"{base_dir}/.secret/gitapi.env")


app = Flask("app",
            static_folder=f"{str(base_dir)}/frontend/",
            template_folder=f"{str(base_dir)}/frontend/")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template("Home/home_un.html")
    
    elif request.method == "POST":
        return redirect(f'https://github.com/login/oauth/authorize?client_id={os.environ.get("client_id")}&scope=repo&redirect_uri=http://localhost:5000/home')

# githubのアクセストークンを取得
@app.route('/home')
def get_token():
    code = request.args.get("code")
    post = requests.post(f"https://github.com/login/oauth/access_token?code={code}&client_id={os.environ.get('client_id')}&client_secret={os.environ.get('client_secret')}")
    access_token = post.text.split("&")[0].split("=")[1]
    return redirect(f"http://localhost:5000/login?access_token={access_token}")


@app.route("/login")
def login():
    access_token = request.args.get("access_token")
    user_name = githubinfo.get_user(access_token)
    month_commit = githubinfo.commit_month_datetime(access_token, user_name)
    print("processing...")
    all_comitt_data = githubinfo.commit_all_datetime(access_token, user_name)
    print("processing...")
    print(all_comitt_data)
    data = githubinfo.modify(all_comitt_data)
    X,Y = [],[]
    month = 12
    day = 30
    x_window = 20
    for i in range(month):
        X.append(data[i*day:i*day+x_window])
        Y.append(data[i*day+x_window:(i+1)*day])
    print(X,Y)
    percent = calculate_anmalous_percent(X, Y, data)
    print("processing...")
    db.insert_data(user_name, month_commit, percent)
    text = gpt.evaluation_score(percent)
    return render_template('Home/main.html', percent=percent, text=text)

@app.route("/search/<user_name>")
def search(user_name):
    data = db.get_data(user_name)
    print(data)
    return render_template("search/search.html")

if __name__ == "__main__":
    app.run()