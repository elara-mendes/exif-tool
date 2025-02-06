# Install library
# !pip install google-generativeai --upgrade
from dotenv import load_dotenv
import google.generativeai as ai  
import time
import os
import re

load_dotenv()
# API key
API-IA = 'AIzaSyAngJFO8F1ptgbzwdL8hWUvDYEG3c_Ltzc' 
os.environ['API_KEY'] = API-IA

# API config
ai.configure(api_key=API-IA)

# Create the model
model = ai.GenerativeModel('gemini-pro')  
chat = model.start_chat()  

def pythonGPT(lat, lon):
    coord = f'what place is it {lat} {lon}'
    response = chat.send_message(coord)
    print('Chatbot:', response.text)