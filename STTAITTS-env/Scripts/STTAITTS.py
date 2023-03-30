import speech_recognition as sr
import os
import sys
import time
import openai
from pydub import AudioSegment
from pydub.playback import play
import keyboard
import json
import traceback

openai.api_key = os.getenv("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")
openai.api_key = "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"
openai.organization = "org-4xUbQUKzM7LkGIGepaZV3CTs"
OPENAI_API_KEY = "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"



logPath = "STTAITTSLog.txt"
recOn = False
x = 0
from google.oauth2 import service_account
import google.cloud.texttospeech as tts

dict = {
  "type": "service_account",
  "project_id": "sttaitts",
  "private_key_id": "8b0ad904fd6d6096d8b5e87f54d64fbb977d0012",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCjfzADY4T+re73\ncBkv7GTShE6AkcxYhr8ShVsj2Fsa3Czwoy666nbh2oxcH9NiIC7jzDuT0G3MteSp\nwL2y33lwtZHvFt8sGiJtEqba8CxQIyhAiEbwz3FsgQjaKGPmciDvwCY4PN7fxpzd\njcqOXg1HhpT6+GRCCAVfoiTplzPwf7haGd/+TyvyY2/zIhMsZVo8aGdybMVu4yKs\nxjrJWAKZTtcVNr88Rc2ORHNOP2nW2OjzJMf8gWqHa45LRG2AyrMyW9xdJwV973VH\nFu9oNpTJPHCAxBsWbS62u0eoa6jw2mKpBBAxY5F8xEn1eR2NEQE0UKsrhUsKY9G5\nEHbY5/QbAgMBAAECggEAPfvkKgS60QsEA8793YtTlfQPBvM/c3hyTAU+zlIiCAbd\nCsXy2240b9+5QtvV+eeVn0s4cwub9PYooKqvwHa0xaQwlWIobcHit1NQ6sQPKLqL\nchu4OWeL6sTopDyX0zAFiJ9iXgPFwzS7F8u/tUW25x0Asj0lVVtRHjaMo/ps+In3\noFMKbLVELxzTa8U5FauT+5Vx08DmEntJW0I9RsSiOgsqlTvly+yvCNSNAfh2g6+q\n+bXBGtvUMiabKRsnnRZ+QCYGI+pSpBPzQFHaA5xSI7tajQpKQSewVf8JnmVVreUc\nMaI92v7QZ5ewXfjwTcvdQnUF+sne1aMbCkEwphi9oQKBgQDef+VNnSjhpk7UR/YI\nktj4eDhrfQVlBVyz1q3HuWWIR/YaH72MppYGq0JQu8kmczm/IOVOQIFktMQ88Yna\n70Xcu7vQbhA+Mz8Fx85uu0303vFbaJj8DdkkFOypLSEvcw9nYrnEmJuERqPy0oR4\n6dp7e9IF78Jvkv8Q/ozp22in0wKBgQC8HRFonJ/XY5UmDwbRA8p5Y/rDNyHplBCA\nSOajEOqoU3mz6Ib+Xlof5KP7zhqZPHIxNHlFA/hy+mAgveAR2uDlUHqZ0DcLEFhJ\nNOwJLmt7NrWDqsx7FyXh0B4KzCnP0mBRsUGgArxFR1pO4GxIvl8GU0VAKIlTnCLo\nHXIGiYxdmQKBgC9ZsnfY+UlENkRw6AgdEDWYiBE/8vTzti3DgwodB2GARvx6QsF6\n9jSHH77Ep+MZ5HErVAFaMu82lQiPMpI4F3sJLMgHlEdYapIVWnYwQD/bbivQz7Xc\nUJigJ1k9dHF/oAiVdwlCnN4CloNnj6+XvNpImIKQ6qUJ+GQqd9yQx+3nAoGAEdbT\n2s7Xna5063oLVHD+l4pysmadEbCX7AJ91ML67eGUrgoEG0VJWLLvFicSgKupzJ7E\nTVY2DnlN+mznPeo636RFLCcBwUvYg4DATZKYYMPsbMMaxyWH0yVQZAe+g1XZCoY7\nyffYcN12Y/qGalObYVcuPwpZE5O//7EjKhmLNSkCgYBCo/our+7uqRumXsmu9Usg\np2iXRpGGemvY10AuHIpVT2J3iv522SCfnVNTnLnkQ8KEWOyzwZJIVlFnRzFx84ep\nquFEbrcBxaExlDvcLsfovNG+bDRKCIfnmjDqkEqT3ZugX+EhXlTimGXmHyQsQVss\ncllqtyU8LOUCdPoWQ84oEA==\n-----END PRIVATE KEY-----\n",
  "client_email": "ghvgcfd@sttaitts.iam.gserviceaccount.com",
  "client_id": "103741498037869784292",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/ghvgcfd%40sttaitts.iam.gserviceaccount.com"
}






def text_to_wav(voice_name: str, text: str):
        try:
            with open('sdadsasg.json', 'w', encoding='utf-8') as f:
                json.dump(dict, f, ensure_ascii=False, indent=2)
        except Exception as e:
            traceback.print_exception(e)
            wait_for_it = input('Press enter to close the terminal window')
        
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "sdadsasg.json"

        language_code = "-".join(voice_name.split("-")[:2])
        text_input = tts.SynthesisInput(text=text)
        voice_params = tts.VoiceSelectionParams(
            language_code=language_code, name=voice_name
        )
        audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

        client = tts.TextToSpeechClient()
        response = client.synthesize_speech(
            input=text_input, voice=voice_params, audio_config=audio_config
        )
        os.remove("sdadsasg.json")

        filename = "tempTTS.wav"
        with open(filename, "wb") as out:
            out.seek(0)
            out.write(response.audio_content)
            print(f'Saved to: "{filename}"')
        out.close()


        clip = AudioSegment.from_wav(filename)
        play(clip)
        



while True:


    if not recOn:
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed(';'): 
                recOn = True
                pass  # finishing the loop
        except:
            pass

    if recOn:

        #time.sleep(1)

        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Waiting.")
            audio = r.listen(source)
        # recognize speech using Google Speech Recognition
        try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
            saidString = r.recognize_google(audio, language='cs-CZ')
            print("Recognized: " + saidString)

            if "leo" in saidString.lower() or "listen" in saidString.lower() or "poslouchej" in saidString.lower(): #Legendary Effective Operant
                # obtain audio from the microphone
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    text_to_wav("cs-CZ-Wavenet-A", "Ano?")
                    print("Ano?")
                    audio = r.listen(source)
                # recognize speech using Google Speech Recognition
                try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                    saidString = r.recognize_google(audio, language='cs-CZ')
                    print("Recognized: " + saidString)

                    if saidString.lower() == "what's the temperature" or saidString.lower() == "what is the temperature" or saidString.lower() == "jaká je teplota" or saidString.lower() == "teplota":
                        #gpt_prompt = "What's the temperature in Černošice"
                        gpt_prompt = "Jaká je v Černošicích teplota?"
                        response = openai.Completion.create(
                        engine="text-davinci-003",
                        prompt=gpt_prompt,
                        temperature=0.5,
                        max_tokens=256,
                        top_p=1.0,
                        frequency_penalty=0.0,
                        presence_penalty=0.0
                        )
                        print(response['choices'][0]['text'])

                        f = open(logPath, "w", encoding="utf-8")
                        f.write(response['choices'][0]['text']+"\n")
                        f.close()

                        text_to_wav("cs-CZ-Wavenet-A", response['choices'][0]['text'])

                    elif saidString.lower() == "what's the time" or saidString.lower() == "what is the time" or saidString.lower() == "what time is it" or saidString.lower() == "čas" or saidString.lower() == "kolik je hodin" or saidString.lower() == "kolik je":
                        
                        t = time.localtime()
                        TIME = time.strftime("%I:%M %p", t)

                        print(f"Je {TIME}.")

                        f = open(logPath, "w", encoding="utf-8")
                        f.write(f"Je {TIME}."+"\n")
                        f.close()

                        text_to_wav("cs-CZ-Wavenet-A", f"Je {TIME}.")
                    
                    elif saidString.lower() == "open steam" or saidString.lower() == "otevři steam" or saidString.lower() == "steam":
        
                        print("Otevírám Steam.")

                        os.startfile("C:\\Program Files (x86)\\Steam\\steam.exe")

                        f = open(logPath, "w", encoding="utf-8")
                        f.write("Otevírám Steam.")
                        f.close()

                        text_to_wav("cs-CZ-Wavenet-A", "Otevírám Steam.")

                    elif saidString.lower() == "shut down" or saidString.lower() == "turn off" or saidString.lower() == "shutdown" or saidString.lower() == "vypnout" or saidString.lower() == "vypni se" or saidString.lower() == "konec":

                        resp = "Vypínám se."
                        print(resp)

                        f = open(logPath, "w", encoding="utf-8")
                        f.write(resp)
                        f.close()

                        text_to_wav("cs-CZ-Wavenet-A", resp)

                        sys.exit()

                    elif saidString.lower() == "bedtime" or saidString.lower() == "turn off my computer" or saidString.lower() == "goodnight" or saidString.lower() == "good night" or saidString.lower() == "dobrou" or saidString.lower() == "dobrou noc" or saidString.lower() == "jdu spát" or saidString.lower() == "vypni mi počítač" or saidString.lower() == "vypni počítač":

                        if saidString.lower() == "good night" or saidString.lower() == "bedtime" or saidString.lower() == "goodnight" or saidString.lower() == "dobrou" or saidString.lower() == "dobrou noc" or saidString.lower() == "jdu spát":
                            resp = "Dobrou noc, vypnu vám počítač."
                        else:
                            resp = "Vypínám vám počítač."
                        print(resp)

                        f = open(logPath, "w", encoding="utf-8")
                        f.write(resp)
                        f.close()

                        text_to_wav("cs-CZ-Wavenet-A", resp)

                        os.system("shutdown /s /t 1")

                    elif saidString.lower() == "go to sleep" or saidString.lower() == "put my computer to sleep" or saidString.lower() == "jdi spát" or saidString.lower() == "dej můj počítač do spacího režimu":

                        
                        resp = "Dávám váš počítač do spacího režimu."
                        print(resp)

                        f = open(logPath, "w", encoding="utf-8")
                        f.write(resp)
                        f.close()

                        text_to_wav("cs-CZ-Wavenet-A", resp)

                        os.system("Rundll32.exe Powrprof.dll,SetSuspendState Sleep") 
                    else:
                        gpt_prompt = saidString
                        response = openai.Completion.create(
                        engine="text-davinci-003",
                        prompt=gpt_prompt,
                        temperature=0.5,
                        max_tokens=256,
                        top_p=1.0,
                        frequency_penalty=0.0,
                        presence_penalty=0.0
                        )
                        print(response['choices'][0]['text'])

                        f = open(logPath, "w", encoding="utf-8")
                        f.write(response['choices'][0]['text']+"\n")
                        f.close()

                        if response['choices'][0]['text'][0] == "?":
                            text_to_wav("cs-CZ-Wavenet-A", response['choices'][0]['text'][1:])
                        else:
                            text_to_wav("cs-CZ-Wavenet-A", response['choices'][0]['text'])
                except sr.UnknownValueError:
                    print("Could not understand audio")



                    
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
            

            
            
            

        except sr.UnknownValueError:
            print("Could not understand audio")
            x = x + 1
            if x > 4:
                recOn = True
                x = 0
            
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        
        os.system('cls' if os.name == 'nt' else 'clear')
    
