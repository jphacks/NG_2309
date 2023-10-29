import openai


def evaluation_score(score):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
        ]
    )
    return response['choices'][0]['message']['content']