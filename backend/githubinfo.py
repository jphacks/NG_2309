import os 
from dotenv import load_dotenv
from github import Github
from github import Auth
import datetime 

token =  load_dotenv()

def get_user():
    # アクセストークンを取得
    # ユーザー名取得
    auth = Auth.Token(token)
    g = Github(auth=auth)
    user = g.get_user()
    g.close()
    return user.name

def commit_history(reponame):
    # アクセストークンを取得
    # ユーザー名取得 

    auth = Auth.Token(token)
    g = Github(auth=auth)
    # repositoryを取得
    repo = g.get_repo(full_name_or_id=reponame)
    commit = repo.get_commits()
    # listに変換
    data = list(commit)
    data = list(map(lambda v: str(v)[12:52],data))
    lists = []
    for i in data:
        commit = repo.get_commit(sha=i)
        v=datetime.datetime.fromisoformat(str(commit.commit.author.date))
        lists.append(v)
        commit = repo.get_commit(sha=i)
        print(commit.commit.author.date)
    g.close()
    return lists


# グローバル変数



def commit_all_datetime(author):
    # result定義
    result = []
    # 一年前の日付の取得
    today =datetime.datetime.now()
    today = today.replace(year=today.year-1)
    today = 'author-date:>'+str(today.year) + '-' + str(today.month) + '-' + str(today.day)
    # アクセストークンを取得
    g = Github(token)
    # コミット履歴の取得
    commit =  g.search_commits(sort ='author-date', order='desc', author=author,query=today)
    

    for i in commit:
        commitday = str(i.commit.author.date.year) + '-' + str(i.commit.author.date.month) + '-' + str(i.commit.author.date.day)
        result.append(commitday)
    g.close()
    return result
def commit_month_datetime(author):
    # result定義
    result = []
    # 一年前の日付の取得
    today =datetime.datetime.now()
    today = today.replace(year=today.month-1)
    today = 'author-date:>'+str(today.year) + '-' + str(today.month) + '-' + str(today.day)
    # アクセストークンを取得
    g = Github(token)
    # コミット履歴の取得
    commit =  g.search_commits(sort ='author-date', order='desc', author=author,query=today)
    total=commit.totalCount
    g.close()
    return total

def issue_commit(author):
    # result定義
    result = []
    # 一年前の日付の取得
    today =datetime.datetime.now()
    today = today.replace(year=today.year-1)
    today = 'author-date:>'+str(today.year) + '-' + str(today.month) + '-' + str(today.day)
    # アクセストークンを取得
    g = Github(token)
    # issueの取得
    issue =  g.search_issues(sort ='author-date', order='desc', author=author,query=today)

    # issueのステータスで場合分け
    if issue.state == 'open':
        for i in issue:
            issueday = str(i.created_at.year) + '-' + str(i.created_at.month) + '-' + str(i.created_at.day)
            updateday = str(i.updated_at.year) + '-' + str(i.updated_at.month) + '-' + str(i.updated_at.day)
            result.append(issueday)
            result.append(updateday)
    elif issue.state == 'closed':
        for i in issue:
            issuecreatday = str(i.closed_at.year) + '-' + str(i.closed_at.month) + '-' + str(i.closed_at.day)
            issuecloseday = str(i.created_at.year) + '-' + str(i.created_at.month) + '-' + str(i.created_at.day)
            updateday = str(i.updated_at.year) + '-' + str(i.updated_at.month) + '-' + str(i.updated_at.day)
            result.append(issuecreatday)
            result.append(issuecloseday)
            result.append(updateday)
    g.close()
    return result




if __name__ == '__main__':
    print(get_user())