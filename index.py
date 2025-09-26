import requests # type: ignore
from urllib.parse import urlparse # type: ignore
import ollama # type: ignore
import json # type: ignore
from dotenv import load_dotenv # type: ignore
import os
from google import genai
from google.genai import types # type: ignore

load_dotenv()

def isValidURL(url):
    u = urlparse(url)
    if not u.netloc or not u.path:
        return False
    return True

def llmCall(text):
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=text,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
        ),
    )

    print(response.text)
    return response.text

    # response = ollama.chat(model='llama3.2:1b', messages=[
    #     {
    #         'role': 'user',
    #         'content': text,
    #     },
    # ])
    # return response['message']['content']

def getDeepDive(url):
    newURL = url.split('-')[-1]

    url = "https://api.oboe.fyi/courses/" + newURL + '/deepdive'
    request = requests.get(url)
    myDict = json.loads(request.text)
    returnText = ''
    for el in myDict["steps"]:
        returnText += el["content"] + '\n'
    return returnText

def mermaidChart(text):
    text = """Can you please look at the following information from a course and give a **broad overview** of only the **top two to three levels of the hierarchy** of the **most essential concepts and principles** in this course. 
            **Exclude highly specific examples, sanity checks, or minor technical details.** 
            Can you just output the hierarchy as a **Graphviz DOT language** block.

            **Your Graphviz DOT output must adhere to the following rules:**
            1.  **Enclose the entire output in a `digraph G { ... }` block.**
            2.  **Set the graph direction to Left-To-Right (`rankdir=LR;`).**
            3.  **Use clear, descriptive labels for all nodes.**

            Here is the course material: """ + text
    return llmCall(text)

def brainMap(text):
    text = """Please look at the following information and generate a **general** mind map representation of the **most essential concepts and principles** in this course. 
            **Show them as nodes connected by their relationships, without enforcing a strict hierarchy.**
            Can you just output the mind map as a **Graphviz DOT language** block. 

            **Your Graphviz DOT output must adhere to the following rules:**
            1.  **Enclose the entire output in a `digraph G { ... }` block.**
            2.  **Set the graph direction to Left-To-Right (`rankdir=LR;`).**
            3.  **Use clear, descriptive labels for all nodes.**

            Here is the course material: """ + text
    return llmCall(text)

def eli5(text):
    text = """Can you please look at the following information from a course and can you explain the concept like I am a 5 year old? 
                Please use **simple words** and **common, everyday analogies** to explain the concept.
                Make the tone **fun, engaging, and non-intimidating**.

                Please limit your explanation to a maximum of **three short paragraphs**.
                Here is the course material: """ + text
    return llmCall(text)

def explainBackToMe(userText, text):
    myText = "I am going to give you two things, 1) I am going to give you information about a course I am reading up on, I want you to digest it and understand the content. 2) I am going to give you what I remember from reading the course. I want you to use these two things to tell me what I got right and the information to fill in the gaps of my knowledge from the course material. "
    myText += "My knowledge about this subject: " + userText + "\n"
    myText += "The course materials: " + text
    return llmCall(myText)

if __name__ == "__main__":
    url = 'https://oboe.fyi/courses/unlocking-the-secrets-of-hardware-programming-p2veoyq0'
    targetText = getDeepDive(url)