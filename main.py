import tkinter as tk
from tkinter import filedialog, ttk
import pyttsx3
import os
import threading
import wave
import speech_recognition as sr
import time

class TextToSpeechGUI:
    def __init__(self, master):
        self.master = master
        master.title("Text to Speech and Speech to Text")

        # Tạo tab control
        self.tab_control = ttk.Notebook(master)
        self.tab_control.pack(pady=10)

        # Tạo tab Text to Speech
        self.text_to_speech_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.text_to_speech_tab, text="Text to Speech")
        self.create_text_to_speech_tab(self.text_to_speech_tab)

        # Tạo tab Speech to Text
        self.speech_to_text_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.speech_to_text_tab, text="Speech to Text")
        self.create_speech_to_text_tab(self.speech_to_text_tab)

        # Khởi tạo engine Text-to-Speech và cài đặt giọng đọc tiếng Việt
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', r'Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_viVN_An')

    def create_text_to_speech_tab(self, tab):
        # Tạo giao diện cho tab Text to Speech
        self.text_area = tk.Text(tab, height=10, width=50)
        self.text_area.pack(pady=10)

        self.open_file_button = tk.Button(tab, text="Open File", command=self.open_file)
        self.open_file_button.pack(pady=5)

        self.voice_label = tk.Label(tab, text="Select Voice:")
        self.voice_label.pack(pady=5)

        self.voice_var = tk.StringVar()
        self.male_voice_radio = tk.Radiobutton(tab, text="Male", variable=self.voice_var, value="male")
        self.female_voice_radio = tk.Radiobutton(tab, text="Female", variable=self.voice_var, value="female")
        self.male_voice_radio.pack(side=tk.LEFT)
        self.female_voice_radio.pack(side=tk.LEFT)

        self.volume_label = tk.Label(tab, text="Volume:")
        self.volume_label.pack(pady=5)

        self.volume_scale = ttk.Scale(tab, from_=0, to=1, value=0.5, orient=tk.HORIZONTAL, length=200)
        self.volume_scale.pack(pady=5)

        self.rate_label = tk.Label(tab, text="Rate:")
        self.rate_label.pack(pady=5)

        self.rate_scale = ttk.Scale(tab, from_=50, to=300, value=200, orient=tk.HORIZONTAL, length=200)
        self.rate_scale.pack(pady=5)

        self.speak_button = tk.Button(tab, text="Speak", command=self.speak)
        self.speak_button.pack(pady=10)

    def create_speech_to_text_tab(self, tab):
        # Tạo giao diện cho tab Speech to Text
        self.speech_text_area = tk.Text(tab, height=10, width=50)
        self.speech_text_area.pack(pady=10)

        self.record_button = tk.Button(tab, text="Record", command=self.record_and_transcribe)
        self.record_button.pack(pady=5)

        self.save_button = tk.Button(tab, text="Save to File", command=self.save_speech_to_file)
        self.save_button.pack(pady=5)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, text)

    def speak(self):
        text = self.text_area.get("1.0", tk.END)
        voice = self.voice_var.get()
        volume = self.volume_scale.get()
        rate = self.rate_scale.get()

        voices = self.engine.getProperty('voices')
        if voice == "male":
            self.engine.setProperty('voice', voices[1].id)
        else:
            self.engine.setProperty('voice', voices[3].id)

        self.engine.setProperty('volume', volume)
        self.engine.setProperty('rate', rate)
        self.engine.say(text)
        self.engine.runAndWait()

    def record_and_transcribe(self):
        text = get_text()
        if text:
            self.speech_text_area.insert(tk.END, text + "\n")
        else:
            print("Failed to transcribe speech.")

    def save_speech_to_file(self):
        text = self.speech_text_area.get("1.0", tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(text)

def get_audio():
    ear_robot = sr.Recognizer()
    with sr.Microphone() as source:
        print("Trợ Lý Ảo:  Đang nghe ! -- __ -- !")
        audio = ear_robot.record(source, duration=4)
        try:
            print(("Trợ Lý Ảo :  ...  "))
            text = ear_robot.recognize_google(audio, language="vi-VN")
            print("Tôi:  ", text)
            return text
        except Exception as ex:
            print("Trợ Lý Ảo:  Lỗi Rồi ! ... !")
            return None

def get_text():
    for i in range(3):
        text = get_audio()
        if text:
            return text.lower()
        elif i < 2:
            print("Trợ Lý Ảo không nghe rõ bạn nói. Vui lòng nói lại nha !")
    time.sleep(3)
    return None

root = tk.Tk()
text_to_speech_gui = TextToSpeechGUI(root)
root.mainloop()
