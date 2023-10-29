import openai
from pathlib import Path
from dotenv import load_dotenv
import os

base_dir = Path(__file__).parents[1]
load_dotenv(f"{base_dir}/.secret/gpt.env")

openai.api_key = os.environ.get("api_key")

def evaluation_score(score):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"あなたはプログラマーやエンジニアに対して心の健康を向上させるようなプロの心理カウンセラーです。scoreはストレスレベルで0が最低100が最高でストレスレベルが高ければ高いほど危険な状態です。プロのプログラマーに対して次の作業に気持ちよく取り掛かれるような50文字くらいの言葉のコメントをくださいまた以下の一文はあなたの出力の例でこの形式以外は許しません。リラックスし、自信を持って次のプロジェクトに取り組みましょう。健康な心がクリエイティビティを支えます。\nsocre:{score}"},
        ]
    )
    return response['choices'][0]['message']['content']