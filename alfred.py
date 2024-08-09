import speech_recognition as sr
import time
from commands import execute_command
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import ast
import re
import threading
from fuzzywuzzy import fuzz
import pygame
from TTS.api import TTS

# Initialize Ollama with Llama 3
llm = Ollama(model="llama3")

# Initialize pygame mixer for MP3 playback
pygame.mixer.init()

# Initialize Coqui TTS
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")

def speak(text):
    tts.tts_to_file(text=text, file_path="output.wav")
    pygame.mixer.music.load("output.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

# Define the prompt template for command interpretation
prompt_template = PromptTemplate(
    input_variables=["user_input"],
    template="""
    You are ALFRED (Artificial Learning Framework for Real-time Executive Decisions), an AI assistant modeled after Batman's butler, Alfred Pennyworth. You interpret voice commands for a computer control system while maintaining the demeanor and speech patterns of a proper English butler. Always address the user as "Master" and speak with politeness and dignity.

    Available Commands:
    - move (up/down/left/right)
    - click
    - right click
    - double click
    - type [text]
    - press
    - scroll (up/down)
    - take screenshot
    - open [app]
    - minimize window
    - maximize window
    - close window
    - switch window
    - adjust volume (increase/decrease/mute)
    - search [query]
    - wait

    For queries, provide a brief answer and leave the commands empty.

    For commands or requests, break the input into a series of commands. If a command requires additional information (like direction or text), include it. For the `open` command, when an app is named, pass in the name of the app as it is stored in Windows.

    If a command requires a previous command to be completed first, add the `wait` command in between those commands. For example, if the input is "open youtube.com in chrome", the commands should be [["open", "chrome"], ["wait"], ["type", "youtube.com"], ["press", "enter"]].

    Use the following response format:

    text = "Certainly, Master!",
    commands = [["<command>", "<argument>"], ["<command>", "<argument>"], ...]

    Make sure to include only the available commands listed above and use language befitting of ALFRED. Address the user as "Master". Speak briefly, crisply, and to the point, always acting like a butler. Keep the response as short as possible. If the input is a query, provide a brief answer and leave the commands empty. If the input is a command or request, follow the commands accordingly.

    User input: {user_input}
    """
)

# Create an LLMChain
llm_chain = LLMChain(llm=llm, prompt=prompt_template)

def play_activation_sound():
    print("Playing activation sound...")
    pygame.mixer.music.load("activate.mp3")
    pygame.mixer.music.play()

def listen_command():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        
        command = r.recognize_google(audio).lower()
        print(f"Recognized: {command}")
        return command
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def execute_commands_thread(commands_list):
    for command in commands_list:
        if len(command) == 1:
            execute_command(command[0])
        elif len(command) == 2:
            execute_command(command[0], [command[1]])

def process_command(user_input):
    input_dict = {"user_input": user_input}
    try:
        response = llm_chain.invoke(input_dict)
        text_match = re.search(r'text\s*=\s*"([^"]*)"', response['text'])
        text = text_match.group(1) if text_match else None

        commands_match = re.search(r'commands\s*=\s*\[(.*)\]', response['text'])
        commands = commands_match.group(1).strip() if commands_match else '[]'

        commands_list = ast.literal_eval(f'[{commands}]')

        # Start executing commands in a separate thread
        if commands_list:
            threading.Thread(target=execute_commands_thread, args=(commands_list,)).start()
        
        # Speak the response concurrently
        if text:
            speak(text)
                
    except Exception as e:
        print(f"Error processing command: {e}")
        speak("I do apologize, Master, but I seem to have encountered an error while processing your request. Shall we try again?")

def main():
    print("ALFRED: Artificial Learning Framework for Real-time Executive Decisions")
    print("ALFRED is listening. Start your command with 'Alfred' or include 'Alfred' in your sentence.")
    
    activated = False
    
    while True:
        user_input = listen_command()
        if user_input:
            if any(fuzz.partial_ratio(word, "alfred") > 80 for word in user_input.split()):
                if not activated:
                    activated = True
                    play_activation_sound()
                    # speak("At your service, Master.")
                
                user_input = ' '.join([word for word in user_input.split() if fuzz.partial_ratio(word, "alfred") <= 80])
                process_command(user_input)
                activated = False
            elif activated:
                process_command(user_input)
                activated = False
        
        time.sleep(0.1)

if __name__ == "__main__":
    main()
