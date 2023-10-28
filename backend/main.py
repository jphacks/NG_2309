from re import T
from flask import Flask, redirect, render_template, request, url_for
from dotenv import load_dotenv
from pathlib import Path
import requests
import githubinfo
from model.model_create import calculate_anmalous_percent
import os
import db
from celery import Celery

base_dir = Path(__file__).parents[1]

load_dotenv(f"{base_dir}/.secret/gitapi.env")


app = Flask(__name__,
            static_folder=f"{str(base_dir)}/frontend/",
            template_folder=f"{str(base_dir)}/frontend/")

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@app.route('/')
def index():
    if request.method == "GET":
        return render_template("Home/home_authenticated.html")
    
    elif request.method == "POST":
        return redirect(f'https://github.com/login/oauth/authorize?client_id={os.environ.get("client_id")}&scope=repo&redirect_uri=http://localhost:5000/home')

# githubのアクセストークンを取得
@app.route('/home')
def get_token():
    code = request.args.get("code")
    post = requests.post(f"https://github.com/login/oauth/access_token?code={code}&client_id={os.environ.get('client_id')}&client_secret={os.environ.get('client_secret')}")
    access_token = post.text.split("&")[0].split("=")[1]
    return redirect(f"http://localhost:5000/login?access_token={access_token}")


@celery.task(bind=True)
def background_process(self, access_token):
    user_name = githubinfo.get_user(access_token)
    month_commit = githubinfo.commit_month_datetime(access_token, user_name)
    data = ""
    X,Y = "",""
    percent = calculate_anmalous_percent(X, Y, data)
    db.insert_data(user_name, month_commit, percent)
    return (user_name, month_commit, percent)



@app.route("/login")
def login():
    access_token = request.args.get("access_token")
    task = background_process.apply_async(args=(access_token))
    return redirect(url_for('result', task_id=task.id))


@app.route('/result/<task_id>')
def processing_result(task_id):
    task = background_process.AsyncResult(task_id)
    
    if task.state == 'SUCCESS':
        result = task.result
        return render_template('Home/home_authenticated.html', result=result)
    else:
        return render_template("load/load.html")

@app.route("/search/<user_name>")
def search(user_name):
    data = ""
    return render_template("")

if __name__ == "__main__":
    app.run()