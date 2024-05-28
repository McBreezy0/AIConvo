from dotenv import load_dotenv
import os
from flask import Flask, request
from flask_cors import CORS
from openai import OpenAI
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
generation_config = {"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 1000}
model = genai.GenerativeModel("gemini-pro", generation_config=generation_config)
gemini_chat = model.start_chat()
gemini_chat.send_message("You are going to have a discussion about a topic I decide. I expect you to briefly describe the topic and then ask a question. Try to have a more casual tone and keep it brief:")

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
openai_messages = []

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return open("index.html").read()

@app.route('/begin', methods=['POST'])
def Conversation():
    print("hello")
    i = 0
    conversation = []
    openai_messages = [{"role": "system", "content": "You are about to have a discussion about a topic that I decide. I expect you to at first describe the topic and also ask a question about it, like what my thoughts are, would I try it, etc. After the initial response I want you to engage in a casual conversation and feel free to go on leave the initial topic if that is what the conversation calls for."}]
    topic = request.form['topic']
    openai_messages.append({"role": "user", "content": topic})
    for _ in range(5):
        #Calls and records openai response
        openai_response = openaiResponse(topic, openai_messages)
        conversation.append(openai_response)
        #Changes topic to last thing said by openai
        topic = conversation[i]
        #Calls and records gemini response
        gemini_response = geminiResponse(topic, openai_messages)
        conversation.append(gemini_response)
        i = i + 2
    return conversation
    #i = 0 # for loop
    #x = 1 # if loops
    #conversation = []
    #topic = request.form['topic']
    
    #for i in range(3):
    #    if x == 0: #OpenAI runs a response
    #        i = i + 1
    #        x = 1
    #        openai_messages.append({"role": "user", "content": topic})
    #        print('1')
    #        conversation.append(openaiResponse(topic, openai_messages))
    #    elif x == 1: #Gemini runs a response
    #        i = i + 1
    #        x = 0
            #openai_messages.append({"role":"user", "content": topic})
    #        print('2')
    #        conversation.append(geminiResponse(topic, openai_messages))
    #x = 1

@app.route('/reset', methods=['POST'])
def reset():
    print("Hola")
    global openai_messages
    openai_messages.clear()
    open("index.html").read()
    return "0"


    

#Function takes user question or gemini response and generates a response from OpenAI
def openaiResponse(topic, openai_messages): 
    
    completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages = openai_messages
    )
    message = completion.choices[0].message
    content = message.content
    openai_messages.append({"role":"user","content": content})
    print(openai_messages , "\n\n")
    return content

#Function passes chatgpt response to google gemini
def geminiResponse(message, openai_messages): 
    response = gemini_chat.send_message([message])
    openai_messages.append({"role":"user","content": response.text})
    print(openai_messages ,"\n\n")
    return response.text

if __name__ == '__main__':
    app.run(debug=True)



