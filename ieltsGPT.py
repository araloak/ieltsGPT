import requests

with open("key.txt", 'r', encoding='utf-8') as f:
    key = [i.strip() for i in f.readlines()]

def get_essay():
    with open("ielts_essay.txt", 'r', encoding='utf-8') as f:
        text = f.read().split("\n\n")
    title = text[0].strip()+"\n"
    passage = text[1].strip()
    return title, passage

def ask_chatgpt(query):
    data = []
    data.append([query, None])
    response = requests.post("https://araloak-test.hf.space/run/bot_response", json={
        "data": [
            data,
            keys,
        ]
    }).json()

    resp = response["data"][0]
    return resp[-1][1]
def load_prompt(task=1):
    aspects = ['ta','cc','lr','gra']
    text = []
    for aspect in aspects:
        with open("prompts/ielts_writing_"+str(task)+"_prompt_"+aspect+".txt", 'r', encoding='utf-8') as f:
            text.append((aspect,f.read().strip()))
    return text

def clean(text):
    text = text.replace('<br>',"\n")
    return text

def overall_assess():
    short_names = {'ta':'Task Achievement','cc':'Coherence and Cohesion','lr': 'Lexical Resource', 'gra':'Grammatical Range and Accuracy'}
    overall_assessments = []
    prompts = load_prompt(task=2)
    prefix = "Here is the task description:\n"
    
    infix = "Here is the essay for evaluation:\n"

    title, passage = get_essay()
    done = []
    while True:
        for prompt in prompts:
            if prompt[0] in done:
                continue
            query = prompt[1] + "\n" + prefix + title +"\n" + infix + passage
            try:
                overall_assessments.append(clean(ask_chatgpt(query)))
                done.append(prompt[0])
            except:
               continue
            print(len(done))
        if len(done) == 4:
            break

    with open("ielts_feedback.md", 'w', encoding='utf-8') as f:
        f.write("## Task Description\n"+title+"\n"+ "## Essay:\n" + passage.replace("\n","\n\n") + "\n\n---\n\n")
        for short_name,feedback in zip(done,overall_assessments):
            f.write("## "+short_names[short_name]+"\n" + feedback+"\n\n")

overall_assess()

