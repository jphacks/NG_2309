from flask import Flask, redirect, render_template, request
from dotenv import load_dotenv
from pathlib import Path
import requests
import githubinfo
from model.model_create import calculate_anmalous_percent
import os

base_dir = Path(__file__).parents[1]

load_dotenv(f"{base_dir}/.secret/gitapi.env")

app = Flask(__name__)


@app.route('/')
def index():

    if request.method == "GET":
        return render_template("")
    
    elif request.method == "POST":
        return redirect(f'https://github.com/login/oauth/authorize?client_id={os.environ.get("client_id")}&scope=repo&redirect_uri=http://localhost:5000/home')

# githubのアクセストークンを取得
@app.route('/home')
def get_token():
    code = request.args.get("code")
    post = requests.post(f"https://github.com/login/oauth/access_token?code={code}&client_id={os.environ.get('client_id')}&client_secret={os.environ.get('client_secret')}")
    access_token = post.text.split("&")[0].split("=")[1]
    print(access_token)
    return redirect(f"http://localhost:5000/login?access_token={access_token}")

@app.route("/login")
def login():
    access_token = request.args.get("access_token")
    user_name = githubinfo.get_user(access_token)
    month_commit = githubinfo.commit_month_datetime(access_token, user_name)
    percent = calculate_anmalous_percent()

    
    


if __name__ == "__main__":
    app.run()