from openai import OpenAI # type: ignore
import argparse

with open("key.txt", 'r', encoding='utf-8') as f:
    key = [i.strip() for i in f.readlines()]
client = OpenAI(api_key=key[0])

def ask_llm(prompt):
    resp = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user",
                           "content": prompt},
                ]
            )
    answer = resp.choices[0].message.content
    return answer.strip()

def get_essay():
    with open("data/essay.txt", 'r', encoding='utf-8') as f:
        text = f.read().strip()

    return text

def load_prompt(task=1):
    if task == 1: # integrated_writing
        text = open("prompts/toefl/toefl_integrated_writing.txt", 'r', encoding='utf-8').read().strip()
    if task == 2: # academic_discussion
        text = open("prompts/toefl/toefl_academic_discussion.txt", 'r', encoding='utf-8').read().strip()

    return text

def clean(text):
    text = text.replace('<br>',"\n")
    return text

def overall_assess(task):
    prompt = load_prompt(task)
    text= get_essay()
    query = prompt + "\n" + text

    feedback = clean(ask_llm(query))

    with open("data/feedback.md", 'w', encoding='utf-8') as f:
        f.write("## Task Description & My Writing:\n" + text.replace("\n","\n\n") + "\n\n---\n\n")
        f.write("## Feedback\n" + feedback+"\n\n")

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--task', type=int, default=2, help='1 stands for [Integrated Writing] task, 2 stands for [Writing for an Academic Discussion] task')
    args = parser.parse_args()

    overall_assess(args.task)

if __name__ == '__main__':
    main()

