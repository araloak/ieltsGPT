from openai import OpenAI # type: ignore

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
    aspects = ['ta','cc','lr','gra']
    text = []
    for aspect in aspects:
        with open("prompts/ielts/ielts_writing_"+str(task)+"_prompt_"+aspect+".txt", 'r', encoding='utf-8') as f:
            text.append((aspect,f.read().strip()))
    return text

def clean(text):
    text = text.replace('<br>',"\n")
    return text

def overall_assess():
    short_names = {'ta':'Task Achievement','cc':'Coherence and Cohesion','lr': 'Lexical Resource', 'gra':'Grammatical Range and Accuracy'}
    overall_assessments = []
    prompts = load_prompt(task=2)
    text = get_essay()
    done = []
    while True:
        for prompt in prompts:
            if prompt[0] in done:
                continue
            query = prompt[1] + "\n" + text
            try:
                overall_assessments.append(clean(ask_llm(query)))
                done.append(prompt[0])
            except:
               continue
            print(len(done))
        if len(done) == 4:
            break

    with open("data/feedback.md", 'w', encoding='utf-8') as f:
        f.write("## Task Description & My Writing:\n" + text.replace("\n","\n\n") + "\n\n---\n\n")
        for short_name,feedback in zip(done,overall_assessments):
            f.write("## "+short_names[short_name]+"\n" + feedback+"\n\n")

if __name__ == '__main__':
    overall_assess()
