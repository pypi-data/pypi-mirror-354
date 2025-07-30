# genai/programs.py

programs = {
    1: """import gensim.downloader as api

model=api.load("glove-wiki-gigaword-50")
word1="paris"
word2="france"
word3="india"
word4="capital"

vec1=model[word1]+model[word2]
vec2=model[word1]-model[word2]+model[word3]

result1=model.most_similar(vec1,topn=1)
result2=model.most_similar(vec2,topn=1)

print(f"{word1}+{word2}={result1[0][0]}")
print(f"{word1}-{word2}+{word3}={result2[0][0]}")
""",
    2: """import gensim.downloader as api
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np

model=api.load("glove-twitter-50")

words=["cricket","ball","over","batsman","out","wicket"]

validw=[word for word in words if word in model]
validv=np.array([model[word] for word in validw])

tsne=TSNE(n_components=2, perplexity=5)
wordv=tsne.fit_transform(validv)

plt.figure(figsize=(8,6))
for i in range(len(validv)):
    x=wordv[i][0]
    y=wordv[i][1]
    plt.scatter(x,y,color="blue")
    plt.text(x+0.1,y+0.1,validw[i])

plt.title("cric")
plt.grid(True)
plt.show()

print("simwords\n")
for word,score in model.most_similar('cricket',topn=5):
    print(f"{word:15} {score:.3f}")
    """,
    3: """from transformers import pipeline
import gensim.downloader as api

model=api.load("glove-wiki-gigaword-50")
word="technology"
simwords=model.most_similar(word,topn=5)
print(f"simi words '{word}' are {simwords}")

generator=pipeline("text-generation",model="distilgpt2")

def gen_res(prompt,max_length=100):
    response=generator(prompt,max_length=max_length)
    return response[0]['generated_text']

orgi="explain the impact of technology on society"
orgires=gen_res(orgi)

en=(
    "explain the the impact of technology,innovation,science"
    ",engineeering and digital advancements on society"
)

enres=gen_res(en)
print("orgi:")
print(orgires)
print("enrich:")
print(enres)""",
    4: """import gensim.downloader as api

model=api.load("glove-wiki-gigaword-50")

def gen(code,simiword):
    print(f"make a sentence of your own{code}  {simiword[0][0]} {simiword[1][0]} {simiword[2][0]} {simiword[3][0]} {simiword[4][0]}")

similar=model.most_similar("technology",topn=5)
gen("technology",similar)""",
    5: """import gensim
from gensim.models import Word2Vec
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt',quiet=True)
nltk.download('punkt_tab',quiet=True)

corpus=[
    "Doctor can give you injections when you are sick",
    "heart surgery is done by surgeons",
    "health is wealth",
    "nurses help doctors wank" 
]

tokenize=[word_tokenize(sent.lower()) for sent in corpus]

model=Word2Vec(
    sentences=tokenize,
    vector_size=100,
    window=3,
    min_count=1,
    workers=4,
    sg=1
)

print("simi words are")
for word,score in model.wv.most_similar("doctor",topn=5):
    print(f"{word} (simi score:{score:.3f})")""",
    6: """from transformers import pipeline
print("loading\n")
sent=pipeline("sentiment-analysis")
print("done\n")

text=["hi fuck off","hi how are you"]
result=sent(text)
for i in range(len(text)):
    print(f"text={text[i]}")
    print(f"senti={result[i]['label']}")
    print(f"text={result[i]['score']:.2%}")""",
    7: """from transformers import pipeline

sum=pipeline("summarization")
text=""
A fire broke out in a building in Delhi's Dwarka, killing three of a family after they jumped. The visuals from the ground showed a house engulfed in fire, with massives flames erupting out of windows. In another video, clouds of smoke could be seen billowing.

The fire broke out on the eight and ninth floor of a residential building, Shapath Society, in Dwarka Sector-13. The incident was reported at 9:58 am on Tuesday.

Two children - a boy and a girl, both aged 10 years - jumped from the balcony to save themselves, but were declared dead at Aakash Hospital. Their father, Yash Yadav, aged 35 years, also jumped from the balcony and was also declared dead at IGI Hospital. Mr Yadav was involved in the flex board business.

Mr Yadav's wife and elder son survived the fire and have been sent to IGI Hospital for medical assistance.

All the residents of Shapath society have been evacuated. Electricity and gas connections have been switched off for the moment to avoid any following accident.
""

result=sum(text,max_length=50,min_length=25)
print(f"summary={result[0]['summary_text']}")""",
    8: """from cohere import Client
from langchain.prompts import PromptTemplate

co=Client("3heejpgVk1sDUTtvLtpj4KnIsU43ywG83DMIjdKe")
with open(r"filelocation","r",encoding="utf-8") as file:
    textdoc=file.read()

template=""
you are an expert summarizer. summmarize in the following manner:
text: {text}
summary: 
""
prompt_temp=PromptTemplate(input_variables=['text'],template=template)
fromat_prompt=prompt_temp.format(text=textdoc)

result=co.generate(
    model="command",
    prompt=fromat_prompt,
    
)
print("sumary:")
print(result.generations[0].text.strip())r""",
    9: """import wikipedia
from pydantic import BaseModel
from typing import Optional
import json

class institution(BaseModel):
    name:str
    founder:Optional[str]
    founding_year:Optional[int]
    summary:str

def find_institution(name:str):
    pagetit=wikipedia.search(name)[0]
    page=wikipedia.page(pagetit)
    content=page.content.lower()
    summary=wikipedia.summary(pagetit,sentences=5)
    founder=next((line.split("auspices of")[1] for line in content.split("\n") if "auspices of" in line),None)
    year=next((int(word) for word in content.split() if word.isdigit() and len(word)==4),None)
    return institution(name=page.title,founder=founder,founding_year=year,summary=summary)

name=input("Institution plij")
info=find_institution(name)
print(json.dumps(info.dict(),indent=2))""",
    10: """from pypdf import PdfReader
from cohere import Client

co=Client("XgHOwe0YWKhnr5Tt8lxYl6QORGVGux7C2MXTOaop")
textdoc=PdfReader(r"file location")

text=""
for page in textdoc.pages:
    text+=page.extract_text()

def ipc(q):
    prompt=f""
    you are a Indian penal code bot. use the following content to answer the user
    {text[:1000]}
    user question:{q}
    answer and be precise with ipc sections
    ""
    res=co.generate(
        prompt=prompt,
        model="command-r-plus",
        max_tokens=300
    )
    print("\n"+res.generations[0].text.strip())
que=input("question:")
print(ipc(que))"""
}

def print_genai(n):
    if n in programs:
        print(programs[n])
    else:
        print(f"No program found for number {n}. Choose 1–10.")
