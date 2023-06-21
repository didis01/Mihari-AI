import openai

openai.api_key = ""
model_engine = "gpt-3.5-turbo-0613"

def summarize():
    contextFile = open('memory.txt','r+')
    context=contextFile.read()
    contextFile.close()
    response = openai.ChatCompletion.create(
                model=model_engine,
                messages=[{"role": "system", "content":"I want you to summarize this text, but you need to maintain the important information. You can delete the non-inportant information." },
                            {"role": "user", "content": context}
                ])
    print(response)
    open('memory.txt', 'w').close()
    open('memory.txt','r+').write("Your name is Mihari."+"\n"+response["choices"][0]["message"]["content"])
    contextFile.close()

summarize()