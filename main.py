import speech_recognition as sr
import pyttsx3
import openai
import os
import time
import simpleaudio as sa

r = sr.Recognizer()
openai.api_key = "ENTER_YOUR_PUBLIC_API_KEY"

# ----SFX---FUNCTIONS---- #

def sharingan():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    sfx_directory = os.path.join(script_directory, "sfx")
    sharingan = "sharingan.wav"
    sharingan_path = os.path.join(sfx_directory, sharingan)
    wave_obj = sa.WaveObject.from_wave_file(sharingan_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()

def end_sharingan():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    sfx_directory = os.path.join(script_directory, "sfx")
    end_sharingan = "end_sharingan.wav"
    end_sharingan_path = os.path.join(sfx_directory, end_sharingan)
    wave_obj = sa.WaveObject.from_wave_file(end_sharingan_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()

def jutsu():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    sfx_directory = os.path.join(script_directory, "sfx")
    jutsu = "jutsu.wav"
    jutsu_path = os.path.join(sfx_directory, jutsu)
    wave_obj = sa.WaveObject.from_wave_file(jutsu_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()

# -------x---------x------- #

def activate():
    with sr.Microphone() as source:
        try:
            print("Listening...")
            audio = r.listen(source)
            text = r.recognize_google(audio)
            print("You: " + text)
            
            if "alexa" in text.lower():
                sharingan()
                return True
            else:
                return False
        except sr.UnknownValueError:
                print("...")
        except TimeoutError:
                print("Timeout error. Retrying...")
                time.sleep(2)
                return activate()
            
def generate_text(prompt):
    try:
        response = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=0.3, max_tokens=100)
        return response.choices[0].text.strip()
    
    except openai.error.RateLimitError:
        print("Rate Limited! Waiting 1 min.")
        speak("Rate Limited! Waiting 1 min.")
        time.sleep(60)
        end_sharingan()
        return ""
    except openai.error.OpenAIError as e:
        print("OpenAI API error:", e)
        return ""
    except Exception as e:
        print("An error has occured: ", e)
        return ""
    
def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.say(text)
    engine.runAndWait()

def listen_speech():
    with sr.Microphone() as source:
        try:
            audio = r.listen(source)
            prompt = r.recognize_google(audio)
            prompt = prompt.lower()
            print("You: " + prompt)
            return prompt
        except sr.UnknownValueError:
            print("I didn't catch that, say the call word again")
            speak("I didn't catch that, say the call word again")
            end_sharingan()
        except sr.RequestError:
            print("Sorry, my speech recognition service is currently unavailable.")
            speak("Sorry, my speech recognition service is currently unavailable.")
            return ""
        except TimeoutError:
            print("Timeout error. Retrying...")
            speak("Timeout error. Retrying...")
            time.sleep(2)
            return activate()   

def main():
    with sr.Microphone() as source2:
        print("Silence please, calibrating background noise")
        r.adjust_for_ambient_noise(source2, duration=2)
        r.energy_threshold = 3000
        print("Calibrated, now speak...")

    while True:
        if activate():
            prompt = listen_speech()
            if prompt:
                jutsu()
                response = generate_text(prompt)
                print("Response: " + response)
                speak(response)
                end_sharingan()
                
if __name__ == "__main__":
    main()