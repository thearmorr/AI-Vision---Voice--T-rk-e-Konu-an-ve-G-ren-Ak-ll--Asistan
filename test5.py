import cv2
import speech_recognition as sr
from gtts import gTTS
import google.generativeai as genai
import os
import pygame
import time
import threading
import uuid
import re

# Konfigürasyonlar
genai.configure(api_key="AIzaSyByPphVHrDjaBHMERqF5LhP7TnjZf3vayA")
model = genai.GenerativeModel("gemini-1.5-flash")

# Görüntü İşleme Ayarları
classNames = []
with open('coco.names', "rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

net = cv2.dnn_DetectionModel('frozen_inference_graph.pb', 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt')
net.setInputSize(320, 320)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

# Global Değişkenler
focus_class = None
focus_id = None
tracking = False
object_counter = {}
chat_history = []  # Kısa süreli hafıza için sohbet geçmişi

# Türkçe sayı sözcüklerini rakamlara çevirme sözlüğü
number_map = {
    "bir": "1",
    "iki": "2",
    "üç": "3",
    "dört": "4",
    "beş": "5",
    "altı": "6",
    "yedi": "7",
    "sekiz": "8",
    "dokuz": "9",
    "on": "10"
}

def speak(text):
    try:
        filename = f"voice_{uuid.uuid4().hex}.mp3"
        tts = gTTS(text=text, lang='tr')
        tts.save(filename)
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.music.unload()
        os.remove(filename)
    except Exception as e:
        print("Ses oynatma hatası:", e)

def getObjects(img, thres=0.45, nms=0.2):
    global object_counter
    classIds, confs, bbox = net.detect(img, confThreshold=thres, nmsThreshold=nms)
    current_objects = {}
    
    if len(classIds) != 0:
        object_counter = {cls: 0 for cls in classNames}
        
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            className = classNames[classId - 1]
            object_counter[className] += 1
            obj_id = f"{className}_{object_counter[className]}"
            
            color = (0, 255, 0)
            if tracking and focus_class:
                if className == focus_class:
                    if focus_id is not None:
                        if obj_id == f"{focus_class}_{focus_id}":
                            color = (255, 0, 0)
                        else:
                            continue
                    else:
                        color = (255, 0, 0)
            
            cv2.rectangle(img, box, color, 2)
            label = f"{className} {object_counter[className]}"
            cv2.putText(img, label, (box[0] + 10, box[1] + 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            
            current_objects[obj_id] = box

    return img, current_objects

def convert_number_words(command):
    for word, digit in number_map.items():
        command = re.sub(rf'\b{word}\b', digit, command)
    return command

def process_command(command):
    global focus_class, focus_id, tracking, chat_history
    
    command = command.lower().strip()
    command = convert_number_words(command)
    print("İşlenen komut:", command)

    # Odaklanma komutlarını kontrol et
    if any(keyword in command for keyword in ["odaklan", "takibe al", "takibi bırak", "takipten çık"]):
        handle_system_command(command)
        # Odaklanma komutunu sohbet geçmişine ekle
        chat_history.append(f"Kullanıcı: {command}")
        chat_history.append(f"AI: İnsan {focus_id}'ye odaklanılıyor" if focus_id else "AI: Takip bırakılıyor")
    else:
        # Sohbet modu
        handle_chat(command)

def handle_system_command(command):
    global focus_class, focus_id, tracking
    
    if ('odaklan' in command) or ('takibe al' in command):
        if 'insan' in command:
            matches = re.findall(r'\d+', command)
            id_number = int(matches[0]) if matches else None
            
            focus_class = 'person'
            focus_id = id_number
            tracking = True

            msg = f"İnsan {id_number}'ye odaklanılıyor" if id_number else "Bütün insanlara odaklanılıyor"
            speak(msg)
    elif ('takibi bırak' in command) or ('takipten çık' in command):
        msg = f"İnsan {focus_id}'nin takibi bırakılıyor" if focus_id else "Takip bırakılıyor"
        focus_class = None
        focus_id = None
        tracking = False
        speak(msg)

def handle_chat(command):
    global chat_history
    
    try:
        # Sohbet geçmişini ekleyerek devam et
        chat_history.append(f"Kullanıcı: {command}")
        # Son 5 mesajı hafızada tut
        if len(chat_history) > 10:
            chat_history = chat_history[-10:]
        
        # Gemini'ye sohbet geçmişi ile birlikte soruyu gönder
        prompt = "\n".join(chat_history) + f"\nAI: "
        response = model.generate_content(f"{prompt} (Cevabı Türkçe ver,kanka diyerek başla samimi,dostane bir şekilde kısa ve net 15 kelimeyi geçmeyecek şekilde tut)")
        
        # Gemini'nin cevabını sohbet geçmişine ekle
        chat_history.append(f"AI: {response.text}")
        speak(response.text)
    except Exception as e:
        print("Gemini hatası:", e)
        speak("Üzgünüm, bir sorun oluştu")

def listen_and_recognize():
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("Dinliyorum...")
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio, language='tr-TR')
                print("Algılandı:", text)
                process_command(text)
            except Exception as e:
                print("Hata:", str(e))

def video_processing():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    
    while True:
        success, img = cap.read()
        if not success:
            continue
        result, _ = getObjects(img)
        cv2.imshow("AI Vision", result)
        
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    vision_thread = threading.Thread(target=video_processing)
    audio_thread = threading.Thread(target=listen_and_recognize)

    vision_thread.start()
    audio_thread.start()

    vision_thread.join()
    audio_thread.join()