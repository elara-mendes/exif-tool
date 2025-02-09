# Install library
# !pip install google-generativeai --upgrade
from dotenv import load_dotenv
import google.generativeai as ai  
import time
import os
import re

load_dotenv()
# API key
API_IA = 'AIzaSyAngJFO8F1ptgbzwdL8hWUvDYEG3c_Ltzc' 
os.environ['API_KEY'] = API_IA

# API config
ai.configure(api_key=API_IA)

# Create the model
model = ai.GenerativeModel('gemini-pro')  
chat = model.start_chat()  

def pythonGPT(lat, lon):
    # coord = f'what place is it {lat} {lon}'
    coord = f'Which city is located at latitude {lat} and longitude {lon}? What is the current weather there?'
    response = chat.send_message(coord)
    print('Chatbot:', response.text)


def knowMore(lat, lon):
    question = f'Provide detailed information about the place at latitude {lat} and longitude {lon}, including historical facts and points of interest.'
    response = chat.send_message(question)    
    return response.text