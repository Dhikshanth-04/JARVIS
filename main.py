import random
import subprocess
import threading
from datetime import datetime
import os
import pyqrcode
import serial
import wmi
import asyncio
from AppOpener import close
import pyautogui
import pyscreenshot
import wikipedia
import pyttsx3
import requests
from bs4 import BeautifulSoup
import webbrowser
import csv
import cv2
import time
import mediapipe as mp
import pywhatkit as pwt
import datetime
from geopy import Nominatim
from plotly.io._orca import psutil
import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
from googletrans import Translator, LANGUAGES
#from jarvis.gesture import light_on, light_off

# Initialize speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 200)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def india():
    def speak(text):
        # Used to handle text-to-speech only if needed
        pass

    # Function for vocal input
    def command():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print("User said:", query)
            input_text.insert(tk.END, query)  # Vocal input is entered here
            return query.lower()

        except Exception as e:
            print(e)
            speak("Pardon, please repeat.")
            return None

    # Function to handle translation
    async def translate(target_lang):
        text = input_text.get("1.0", tk.END).strip()

        if not text:
            messagebox.showerror("Error", "Please enter text to translate")
            return

        try:
            translator = Translator()

            # Ensure the detect method is awaited since it's asynchronous
            det = await translator.detect(text)  # Await the detect coroutine
            tras = await translator.translate(text, src=det.lang, dest=target_lang)  # Await the translation coroutine

            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, tras.text)

            det_lab.config(text=f"Detected Language: {LANGUAGES.get(det.lang, 'Unknown').title()}")

        except Exception as e:
            messagebox.showerror("Translation Error", str(e))

    # Function to run the async translation via root.after()
    def run_async_translate(lang_code):
        # Schedule the async translation to run on the asyncio event loop
        loop.call_soon_threadsafe(asyncio.create_task, translate(lang_code))

    # Create the Tkinter window
    root1 = tk.Tk()
    root1.title("Indian Language Translator")
    root1.geometry("500x500")

    text = tk.Label(root1, text="Enter Text:", font=("Segoe UI", 12))
    text.pack(pady=5)

    # Button for microphone
    mic = tk.Button(root1, text="Mic", command=command)
    mic.pack(pady=5)

    input_text = tk.Text(root1, height=5, wrap="word")
    input_text.pack(pady=5)

    det_lab = tk.Label(root1, text="Detected Language: Auto", font=("Arial", 10), fg="blue")
    det_lab.pack(pady=5)

    languages = {
        "Hindi": "hi",
        "Tamil": "ta",
        "Telugu": "te",
        "Bengali": "bn",
        "Marathi": "mr",
        "Gujarati": "gu",
        "Kannada": "kn",
        "Malayalam": "ml",
        "Punjabi": "pa",
        "Urdu": "ur"
    }

    # Arrange buttons for each language
    but_fra = tk.Frame(root1)
    but_fra.pack(pady=5)

    for lang, code in languages.items():
        btn = tk.Button(but_fra, text=lang, width=15, command=lambda c=code: run_async_translate(c))
        btn.pack(side="right", padx=10)

    output_label = tk.Label(root1, text="Translated Text:", font=("Arial bold", 12))
    output_label.pack(pady=5)

    output_text = tk.Text(root1, height=10, wrap="word", bg="white smoke")
    output_text.pack(pady=5)

    # Create the asyncio event loop and start it in a separate thread
    def start_loop():
        global loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_forever()

    # Start the asyncio event loop in a separate thread
    loop_thread = threading.Thread(target=start_loop, daemon=True)
    loop_thread.start()
    # Start the Tkinter event loop
    root1.mainloop()

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print("User said:", query)

        return query.lower()

    except Exception as e:
        print(e)
        speak("Pardon, please repeat.")
        return None

def light_on():
    try:
        arduino = serial.Serial('COM3', 9600, timeout=1)  # Open the port and set timeout to 1 second
        time.sleep(2)  # Allow time for connection to settle
        arduino.write(b'1')  # Send command to turn on LED
        arduino.close()  # Close the connection after sending the command
        speak("lights are turned on")
    except Exception as e:
        print(f"Error: {e}")

def light_off():
    try:
        arduino = serial.Serial('COM3', 9600, timeout=1)
        time.sleep(2)  # Allow time for connection to settle
        arduino.write(b'0')  # Send command to turn off LED
        arduino.close()  # Close the connection after sending the command
        speak("lights ar turned off")
    except Exception as e:
        print(f"Error: {e}")


def gesture():
    # Global variable to track previous state of the gesture
    previous_state = None

    # Setup serial communication
    def light_on():
        try:
            arduino = serial.Serial('COM3', 9600, timeout=1)  # Open the port and set timeout to 1 second
            time.sleep(2)  # Allow time for connection to settle
            arduino.write(b'1')  # Send command to turn on LED
            arduino.close()  # Close the connection after sending the command
        except Exception as e:
            print(f"Error: {e}")

    def light_off():
        try:
            arduino = serial.Serial('COM3', 9600, timeout=1)
            time.sleep(2)  # Allow time for connection to settle
            arduino.write(b'0')  # Send command to turn off LED
            arduino.close()  # Close the connection after sending the command
        except Exception as e:
            print(f"Error: {e}")


    # Initialize MediaPipe Hands solution
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils

    # Open webcam feed
    cap = cv2.VideoCapture(0)

    # Define gesture detection functions
    def is_hand_open(landmarks):
        """Detects if the hand is open (all fingers extended)."""
        thumb_tip = landmarks.landmark[4]
        index_tip = landmarks.landmark[8]
        middle_tip = landmarks.landmark[12]
        ring_tip = landmarks.landmark[16]
        pinky_tip = landmarks.landmark[20]

        if (thumb_tip.y < landmarks.landmark[3].y and
                index_tip.y < landmarks.landmark[5].y and
                middle_tip.y < landmarks.landmark[9].y and
                ring_tip.y < landmarks.landmark[13].y and
                pinky_tip.y < landmarks.landmark[17].y):
            return True
        return False

    def is_hand_closed(landmarks):
        """Detects if the hand is closed (all fingers curled into a fist)."""
        thumb_tip = landmarks.landmark[4]
        index_tip = landmarks.landmark[8]
        middle_tip = landmarks.landmark[12]
        ring_tip = landmarks.landmark[16]
        pinky_tip = landmarks.landmark[20]

        if (thumb_tip.y > landmarks.landmark[2].y and
                index_tip.y > landmarks.landmark[5].y and
                middle_tip.y > landmarks.landmark[9].y and
                ring_tip.y > landmarks.landmark[13].y and
                pinky_tip.y > landmarks.landmark[17].y):
            return True
        return False

    # Main loop to capture gestures
    while True:
        # Capture frame-by-frame from the webcam
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally for a mirror effect
        frame = cv2.flip(frame, 1)

        # Convert the frame to RGB (MediaPipe requires RGB input)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image and get hand landmarks
        results = hands.process(rgb_frame)

        # Draw landmarks and connections if hands are detected
        if results.multi_hand_landmarks:
            for landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

                # Gesture detection based on hand landmarks
                if is_hand_open(landmarks):
                    cv2.putText(frame, "Hand Open: ON", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    # Only turn on the light if the state has changed
                    if previous_state != 'open':
                        light_on()
                        previous_state = 'open'

                elif is_hand_closed(landmarks):
                    cv2.putText(frame, "Hand Closed: OFF", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                    # Only turn off the light if the state has changed
                    if previous_state != 'closed':
                        light_off()
                        previous_state = 'closed'

                # Optional: Draw circles at specific landmarks (for debugging purposes)
                for id, landmark in enumerate(landmarks.landmark):
                    h, w, _ = frame.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)

                    # Draw circles at each landmark
                    if id == 4:  # Thumb tip
                        cv2.circle(frame, (cx, cy), 10, (0, 0, 255), -1)
                    elif id == 8:  # Index finger tip
                        cv2.circle(frame, (cx, cy), 10, (255, 0, 0), -1)
                    elif id == 12:  # Middle finger tip
                        cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)
                    elif id == 16:  # Ring finger tip
                        cv2.circle(frame, (cx, cy), 10, (255, 255, 0), -1)
                    elif id == 20:  # Pinky finger tip
                        cv2.circle(frame, (cx, cy), 10, (255, 0, 255), -1)

        # Show the output frame
        cv2.imshow('Hand Gesture Recognition', frame)

        # Exit loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close any open windows
    cap.release()
    cv2.destroyAllWindows()


def create_confidential_file():
    output_text.insert(tk.END, "Confidential file has been created for you sir..")
    output_text.see(tk.END)
    app.update()
    speak("Confidential file has been created for you sir..")

    # Create a new Tkinter window for the CSV writer
    root = tk.Tk()
    root.title("CSV Writer")

    # Create and place the labels and entry widgets
    tk.Label(root, text="Data:").grid(row=0, column=0)
    name_entry = tk.Entry(root)
    name_entry.grid(row=0, column=1)

    tk.Label(root, text="Detail:").grid(row=1, column=0)
    detail_entry = tk.Entry(root)
    detail_entry.grid(row=1, column=1)

    # Label for error messages
    error_label = tk.Label(root, text="", fg="red")
    error_label.grid(row=4, columnspan=2)

    # Function to save data to CSV
    def save_to_csv():
        name = name_entry.get()
        detail = detail_entry.get()
        if name and detail:  # Check if both fields are filled
            with open('filename.txt', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([name, detail])  # Save name and detail
            name_entry.delete(0, tk.END)
            detail_entry.delete(0, tk.END)
            error_label.config(text="")  # Clear any previous error messages
            speak("Data has been added successfully sir..")
        else:
            error_label.config(text='Please fill in both fields.')

    def close():
        root.destroy()
        speak("yes sir!!")
        jarvis()

    # Create and place the Save button
    save_button = tk.Button(root, text="Save", command=save_to_csv)
    save_button.grid(row=2, columnspan=2)

    # Create and place the Close button
    close_button = tk.Button(root, text="Close", command=close)
    close_button.grid(row=3, columnspan=2)

    # Start the application
    root.mainloop()

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        greeting = "Good morning boss."
    elif hour < 16:
        greeting = "Good afternoon boss."
    else:
        greeting = "Good evening boss."
    return greeting

def music():
    music = "C:\\Users\\srice\\Downloads\\songs"
    song = os.listdir(music)
    os.startfile(os.path.join(music, song[3]))

def jarvis():
    query = "jarvis"
    wish_message = wish()
    output_text.insert(tk.END, wish_message + "\n")
    output_text.see(tk.END)  # Scroll to the bottom
    app.update()  # Update the GUI immediately

    speak(wish_message)  # Speak the greeting

    while True:

        output_text.insert(tk.END,"\nwhat can i do for you?")
        output_text.see(tk.END)
        app.update()
        speak("what can i do for you")
        output_text.insert(tk.END, "listening...")
        output_text.see(tk.END)
        app.update()
        query = command()

        if query is None:
            continue

        output_text.insert(tk.END, "User said: " + query + "\n")
        output_text.see(tk.END)
        app.update()

        if "deactivate" in query:
            response = "Deactivating. Goodbye!"
            output_text.insert(tk.END, response + "\n")
            output_text.see(tk.END)
            app.update()
            speak(response)  # Speak the response
            break

        elif "gesture" in query:
            output_text.insert(tk.END, "\n with pleasure sir i will wait after your arrival just call me  back")
            output_text.see(tk.END)
            app.update()
            speak("with pleasure sir i will wait after your arrival just call me  back")
            gesture()
            break

        # Additional command handling here
        elif "search" in query:
            query = query.replace("search", "").strip()
            res = wikipedia.summary(query, sentences=2)
            output_text.insert(tk.END, "Search result: " + res + "\n")
            output_text.see(tk.END)
            app.update()
            speak(res)  # Speak after displaying

        elif "youtube" in query:
            query = query.replace("in youtube", "")
            output_text.insert(tk.END, "\n with pleasure sir i will wait after your arrival just say me came back")
            output_text.see(tk.END)
            app.update()
            speak("with pleasure sir i will wait after your arrival just say me came back")
            pwt.playonyt(query)
            break

        elif "open browser" in query:
            webbrowser.open("http://google.com")
            response = "Opening browser..."
            output_text.insert(tk.END, response + "\n")
            output_text.see(tk.END)
            app.update()
            speak(response)  # Speak after displaying

        elif "instagram" in query:
            output_text.insert(tk.END, "\nwith pleasure sir i will wait after your arrival just say me came back...")
            output_text.see(tk.END)
            app.update()
            speak("with pleasure sir i will wait after your arrival just say me came back...")
            webbrowser.open("instagram.com")
            break

        elif "capture" in query:
            image = pyscreenshot.grab()
            # To display the captured screenshot
            image.show()
            # To save the screenshot
            image.save("capture.png")

        elif "music" in query:
            output_text.insert(tk.END, "\nwith pleasure sir i will wait after your arrival just say me came back...")
            output_text.see(tk.END)
            app.update()
            speak("with pleasure sir i will wait after your arrival just say me came back...")
            music()
            break

        elif "voice" in query :
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[0].id)
            output_text.insert(tk.END, "\nis it fine now boss...")
            output_text.see(tk.END)
            app.update()
            speak("is it fine now boss...")

        elif "default" in query:
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)
            output_text.insert(tk.END, "\nis it fine now boss...")
            output_text.see(tk.END)
            app.update()
            speak("is it fine now boss...")

        elif "time" in query:
            time = datetime.datetime.now().strftime("%H:%M")
            output_text.insert(tk.END, f"\nTime :{time}")
            output_text.see(tk.END)
            app.update()
            speak(time)

        elif "coordinates" in query:
            query = query.replace("jarvis give me the coordinates of", "")
            query = query.lower()
            geolocator = Nominatim(user_agent="MyApp")
            location = geolocator.geocode(query)
            output_text.insert(tk.END, f"\nthe latitude of the location :{location.latitude}")
            output_text.see(tk.END)
            output_text.insert(tk.END, f"\nthe latitude of the location :{location.longitude}")
            output_text.see(tk.END)
            app.update()
            speak("the latitide and logitudes are..")
            speak(location.latitude)
            speak(location.longitude)

        elif "ip" in query :
            ip_address = requests.get('https://api64.ipify.org?format=json').json()
            output_text.insert(tk.END, f"\nthe ip address:{ip_address}")
            output_text.see(tk.END)
            app.update()
            speak(ip_address)

        elif "open brave" in query:
            import time
            code = "AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
            os.startfile(code)
            speak("please tell me what do you want me to search")
            search = command()
            pyautogui.typewrite(search)
            pyautogui.press('enter')
            time.sleep(5)

        elif "shutdown" in query :
            app1 = "brave.exe"
            speak("yes sir...")
            subprocess.run(["taskkill", "/F", "/IM", app1])

        elif "wordpad" in query:
            code = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Accessories\\wordpad.lnk"
            os.startfile(code)
            times = 0
            while True:
                tell = "tell me the note" if times < 1 else (".. then")
                speak(tell)
                note = command()
                pyautogui.typewrite(note)
                pyautogui.typewrite(" ")
                times += 1
                if note == "enough":
                    close("WordPad")
                    break
        elif "system details" in query:
            output_text.insert(tk.END, "the details of your system sir..")
            output_text.see(tk.END)
            app.update()
            speak("the details of your system sir..")
            b = wmi.WMI()
            my_system = b.Win32_ComputerSystem()[0]
            output_text.insert(tk.END, f"\nmodel:{my_system.Model}")
            output_text.see(tk.END)

            output_text.insert(tk.END, f"\nNumber of processors:{my_system.NumberOfProcessors}")
            output_text.see(tk.END)

            output_text.insert(tk.END, f"\nSystem type:{my_system.SystemType}")
            output_text.see(tk.END)

            output_text.insert(tk.END,f"\nSystem Family:{my_system.SystemFamily}")
            output_text.see(tk.END)

            app.update()
            speak(my_system.Model)
            speak(my_system.NumberOfProcessors)
            speak(my_system.SystemType)
            speak(my_system.SystemFamily)

        elif "webcam" in query:
            output_text.insert(tk.END, "\nwith pleasure sir i will wait after your arrival just say me came back...")
            output_text.see(tk.END)
            app.update()
            speak("with pleasure sir i will wait after your arrival just say me came back...")
            cap = cv2.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
                cv2.imshow('Input', frame)
                c = cv2.waitKey(1)
                if c == 27:
                    break
            cap.release()
            cv2.destroyAllWindows()
            break

        elif "date" in query:
            today = datetime.date.today()
            output_text.insert(tk.END, f"\nDate :{today}")
            output_text.see(tk.END)
            app.update()
            speak(today)

        elif "news" in query:
            api = "dcd54f67cf40479ab8a5a9b21b0db31d"
            url = " https://newsapi.org/v2/top-headlines?country=in&apiKey=" + api
            news = requests.get(url).json()
            art = news['articles']
            final = []
            for acle in art:
                final.append(acle['title'])
            for i in range(5):
                output_text.insert(tk.END,final[i])
                output_text.see(tk.END)
                app.update()
                speak(final[i])

        elif "flip a coin" in query:
            str1 = ["head", "tail"]
            str2 = str1[random.randint(0, 1)]
            speak(" it is.....")
            output_text.insert(tk.END, str2)
            output_text.see(tk.END)
            app.update()
            speak(str2)

        elif "turn on" in query:
            light_on()

        elif "turn off" in query:
            light_off()

        elif "roll a dice" in query:
            speak(" it is.....")
            str2 = [random.randint(1, 6)]
            output_text.insert(tk.END, str2)
            output_text.see(tk.END)
            app.update()
            speak(str2)

        elif "translator" in query:
            print("Yes boss, i will wait untill you come back")
            speak("Yes boss, i will wait untill you come back")
            india()
            break

        elif "countdown" in query:
            import time
            res = []
            for i in query.split():
                if i.isdigit():
                    res.append(i)
            for j in res:
                t = int(j)
                while t:
                    min, sec = divmod(t, 60)
                    timer = '{:02d}:{:02d}'.format(min, sec)
                    output_text.insert(tk.END, timer)
                    output_text.see(tk.END)
                    app.update()
                    time.sleep(1)
                    t -= 1
                output_text.insert(tk.END, "times up...")
                output_text.see(tk.END)
                app.update()
                speak("...time is up")

        elif "report" in query:
            query = query.replace("jarvis give me the weather report of", "")
            url = "https://www.google.com/search?q=" + "weather" + query
            html = requests.get(url).content
            soup = BeautifulSoup(html, 'html.parser')
            temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
            str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
            data = str.split('\n')
            time = data[0]
            sky = data[1]
            output_text.insert(tk.END, temp)
            output_text.see(tk.END)
            output_text.insert(tk.END, sky)
            output_text.see(tk.END)
            app.update()
            speak(temp)
            speak(sky)

        elif "qr code" in query :
            output_text.insert(tk.END, "tell me the text...")
            output_text.see(tk.END)
            app.update()
            speak("tell me the text sir..")
            code = command()
            url = pyqrcode.create(code)
            url.png("myqr.png", scale=6)
            output_text.insert(tk.END, "the Qr code ahs been generated successfully sir...")
            output_text.see(tk.END)
            app.update()
            speak("the QR code has been generated sir...")

        elif "password" in query :
            str1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            str2 = "abcdefghijklmnopqrstuvwxyz"
            str3 = "1234567890"
            str4 = "!@#$%^&*?"
            al = str1 + str2 + str3 + str4
            for i in range(6):
                str5 = "".join(random.sample(al, 6))
            output_text.insert(tk.END, f"password :{str5}")
            output_text.see(tk.END)
            app.update()
            speak(str5)

        elif "battery" in query :
            battery = psutil.sensors_battery()
            output_text.insert(tk.END, f"battery :{battery.percent}")
            output_text.see(tk.END)
            app.update()
            speak(battery.percent)
            speak("percent boss...")
            if (battery.percent < 20):
                output_text.insert(tk.END, "plug in")
                output_text.see(tk.END)
                app.update()
                speak("plug in me ...")

        elif "confidential" in query:
            create_confidential_file()

        elif "translation" in query:
            output_text.insert(tk.END, "yes boss, i will wait untill you come back")
            output_text.see(tk.END)
            app.update()
            speak("yes boss, i will wait untill you come back")
            subprocess.run(['streamlit', 'run', 'D:\\python\\stream_trans.py'])
            break

        elif "clean" in query:
            file = "D:\\python\\confidential.txt"
            os.remove(file)
            output_text.insert(tk.END, "files cleaned boss..")
            output_text.see(tk.END)
            app.update()
            speak("files cleaned boss...")

        elif "move forward" in query:
            import time
            arduino = serial.Serial('COM10', 9600)
            #time.sleep(2)  # Wait for the serial connection to initialize
            output_text.insert(tk.END, "Moving forward..")
            output_text.see(tk.END)
            app.update()
            speak("moving forward...")
            # Send command to run the motor forward
            arduino.write(b'F')  # 'F' for forward
            arduino.close()  # Close the connection
            time.sleep(5)

        elif "turn right" in query:
            import time
            arduino = serial.Serial('COM10', 9600)
            # time.sleep(2)  # Wait for the serial connection to initialize
            output_text.insert(tk.END, "turning right..")
            output_text.see(tk.END)
            app.update()
            speak("turning right..")
            # Send command to run the motor forward
            arduino.write(b'R')  # 'F' for forward
            time.sleep(4)
            arduino.close()  # Close the connection

        elif "turn left" in query:
            import time
            arduino = serial.Serial('COM10', 9600)
            #time.sleep(2)  # Wait for the serial connection to initialize
            output_text.insert(tk.END, "turning left..")
            output_text.see(tk.END)
            app.update()
            speak("turning left...")
            # Send command to run the motor forward
            arduino.write(b'L')  # 'F' for forward
            time.sleep(4)
            arduino.close()  # Close the connection

        elif "move backward" in query:
            import time
            arduino = serial.Serial('COM10', 9600)
            #time.sleep(2)  # Wait for the serial connection to initialize
            output_text.insert(tk.END, "Moving backward..")
            output_text.see(tk.END)
            app.update()
            speak("moving backward...")
            # Send command to run the motor forward
            arduino.write(b'B')  # 'F' for forward
            # Run for 1 second
            time.sleep(5)
            arduino.close()  # Close the connection

        elif "stop" in query:
            arduino = serial.Serial('COM10', 9600)
            output_text.insert(tk.END, "yes boss..")
            output_text.see(tk.END)
            app.update()
            speak("yes boss...")
            arduino.write(b'S')  # 'S' for stop
            arduino.close()

        elif "increase" in query:
            pyautogui.press("volumeup")
        elif "decrease" in query:
            pyautogui.press("volumedown")
        elif "mute" in query:
            pyautogui.press("mute")
        elif "hold on" in query:
            import time
            speak("Yes boss i will wait for 5seconds")
            time.sleep(5.0)

        else:
            with open(r"D:\jarvis\JARVIS\simpcomnds.txt") as F:
                a = 0
                reader = csv.reader(F)
                for coloumn in reader:
                    if coloumn[0] in query:
                        a += 1
                        speak("boss.... ")
                        output_text.insert(tk.END, coloumn[1],"\n")
                        output_text.see(tk.END)
                        app.update()
                        speak(coloumn[1])
            F.close()
            with open(r"D:\jarvis\JARVIS\filename.txt") as F:
                c = 0
                reader = csv.reader(F)
                for coloumn in reader:
                    if coloumn[0] in query:
                        c += 1
                        output_text.insert(tk.END, "it is the confidential file.. please tell me the pass code.. ")
                        output_text.see(tk.END)
                        app.update()
                        speak("it is the confidential file... please tell me the pass code ")
                        output_text.insert(tk.END, "listening.. ")
                        output_text.see(tk.END)
                        app.update()
                        str2 = command()
                        str1 = "unlock 17a"
                        if str2 == str1:
                            with open('filename.txt', 'r') as F:
                                reader = csv.reader(F)
                                for coloumn in reader:
                                    if coloumn[0] in query:
                                        output_text.insert(tk.END, coloumn[1],"\n")
                                        output_text.see(tk.END)
                                        app.update()
                                        speak(coloumn[1])
                                        break
                        else:
                            output_text.insert(tk.END, "\nwrong password..")
                            output_text.see(tk.END)
                            app.update()
                            speak("wrong password!!!")

            if ((c < 1) and (a < 1)):
                output_text.insert(tk.END, "\ni am one of the self developing AI.. i am developing myself.. sorry for the inconvenience..")
                output_text.see(tk.END)
                app.update()
                speak(
                    "i am one of the self developing AI... iam developing myself.. sorry for the inconvenience")
                continue

# Setup Tkinter
app = tk.Tk()
app.title("Jarvis Assistant")
app.geometry("400x900")

# Text widget for output
output_text = tk.Text(app, wrap=tk.WORD, height=40, width=400)
output_text.pack(pady=20)

def start_jarvis():

    jarvis()

# Start Jarvis when button is pressed
start_button = tk.Button(app, text="Start Jarvis", command=start_jarvis)
start_button.pack(pady=20)
app.mainloop()
