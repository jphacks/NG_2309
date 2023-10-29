import os 
from dotenv import load_dotenv
from github import Github
from github import Auth
import datetime 

def get_user(token):
    # アクセストークンを取得
    # ユーザー名取得
    auth = Auth.Token(token)
    g = Github(auth=auth)
    user = g.get_user()
    g.close()
    return user.name

def commit_history(token, reponame):
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


# commitdataをtokenとauthorの名前で取得
# authorはgithubのユーザー名
# tokenはgithubのアクセストークン
# resultはcommitの日付のリスト
def commit_all_datetime(token, author):
    # result定義
    result = []
    # 一年前の日付の取得
    today =datetime.datetime.today()
    lasttoday = today.replace(year=today.year-1)
    lasttoday = 'author-date:>'+str(lasttoday.year) + '-' + str(lasttoday.month) + '-' + str(lasttoday.day)
    # アクセストークンを取得
    g = Github(token)
    # コミット履歴の取得
    commit =  g.search_commits(sort ='author-date', order='desc', author=author,query=lasttoday)

    for i in commit:
        commitday = str(i.commit.author.date.year) + '-' + str(i.commit.author.date.month) + '-' + str(i.commit.author.date.day)
        result.append(commitday)
    g.close()
    return result

def commit_private_datetime(token, author):
    # プライベートリポジトリのコミットの取得
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


def commit_month_datetime(token, author):
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



def issue_commit(token, author):
    # result定義
    result = []
    # 一年前の日付の取得
    today =datetime.datetime.now()
    today = today.replace(year=today.year-1)
    today = 'author-date:>'+str(today.year) + '-' + str(today.month) + '-' + str(today.day)
    # アクセストークンを取得
    g = Github(token)
    # issueの取得
    issue =  g.search_issues(sort ="created", order='desc', author=author,query=today)

    # issueのステータスで場合分け
    if issue.state == 'open':
        for i in issue:
            issueday = str(i.created_at.year) + '-' + str(i.created_at.month) + '-' + str(i.created_at.day)
            updateday = str(i.updated_at.year) + '-' + str(i.updated_at.month) + '-' + str(i.updated_at.day)
            result.append(issueday)
            result.append(updateday)
    elif issue.issue.state == 'closed':
        for i in issue:
            issuecreatday = str(i.closed_at.year) + '-' + str(i.closed_at.month) + '-' + str(i.closed_at.day)
            issuecloseday = str(i.created_at.year) + '-' + str(i.created_at.month) + '-' + str(i.created_at.day)
            updateday = str(i.updated_at.year) + '-' + str(i.updated_at.month) + '-' + str(i.updated_at.day)
            result.append(issuecreatday)
            result.append(issuecloseday)
            result.append(updateday)
    g.close()
    return result

def modify(result):
    d = {}
    nowday = datetime.datetime.now()
    for i in range(360):
        key = str(nowday.year) + '-' + str(nowday.month) + '-' + str(nowday.day)
        d.setdefault(key, 0)
        nowday = nowday - datetime.timedelta(days=1)
    for date in result:
        if date in d.keys():
            d[date] +=1
    result = list(d.values())
    return result





if __name__ == '__main__':
    load_dotenv()
    token = os.environ.get("token")
    author = "vyuma"
    result=modify(commit_all_datetime(token, author))
    print(result)
    print(sum(result))