import os
from tkinter import *
from tkinter import messagebox

import cv2 as cv
import imutils
from PIL import ImageTk, Image

#from GenerateHighlightPKG import generateHighlight
from Generate import generateHighlight
from Generate import extractFeature

window = Tk()
file_dir=''
save_dir=''
videoname=''
goal=0
card=0
substitution=0
cornerkick=0


def GetFileDirectory():
    global file_dir
    #print(fd.get())
    file_dir = fd.get()
    #messagebox.showinfo("Notification", "입력되었습니다")

def ClearEntry1():
        fd.set("")
        sd.set("")
        vn.set("")
        messagebox.showinfo("Notification", "초기화 되었습니다")
'''
def ClearEntry2():
        sd.set("")
def ClearEntry3():
        vn.set("")
'''
def GetVideoName():
    global videoname
    videoname = vn.get()
    #messagebox.showinfo("Notification", "입력되었습니다")

def GetSaveDirectory():
    global save_dir
    save_dir = sd.get()
    #messagebox.showinfo("Notification", "입력되었습니다")

def FileSave():
    messagebox.showinfo("Notification","저장되었습니다")


def Gh():
    num_class = goal+card+substitution+cornerkick
    #print(num_class)
    weights = 'last_weights_C3D_11_25.h5'
    #messagebox.showwarning("Notification", "하이라이트가 생성되고 있습니다! 잠시만 기다려주세요")
    extractFeature.ex1(file_dir,videoname)
    generateHighlight.generate(file_dir, videoname, num_class, save_dir, weights)
    #if end is True:

    messagebox.showinfo("Notification","하이라이트가 생성되었습니다")

def GetVar():
    global goal, card,substitution,cornerkick,audio
    goal = g.get()
    card = yc.get()
    substitution = sub.get()
    cornerkick = corner.get()
    audio = corner.get()

fd=StringVar()
vn=StringVar()
sd = StringVar()
g = IntVar()
yc = IntVar()
sub = IntVar()
corner = IntVar()
a = IntVar()

window.title("Highlight video Generator")
window.geometry("700x400+100+100")
window.resizable(False,False)


lbl1 = Label(window,text="Video DIR")
lbl1.place(x=10,y=10)
lbl2 = Label(window, text="Save DIR")
lbl2.place(x=10, y=40)
lbl3 = Label(window, text="Video Name")
lbl3.place(x=280, y=10)
e1=Entry(window,textvariable=fd,bg="lightblue")
e1.place(x=80,y=10)
e2=Entry(window,textvariable=sd,bg="lightblue")
e2.place(x=80,y=40)
e3=Entry(window,textvariable=vn,bg="lightblue")
e3.place(x=360,y=10)

btn1=Button(window,text="입력", command = GetFileDirectory)
btn1.place(x=230,y=5)
btn11=Button(window,text="입력", command = GetSaveDirectory)
btn11.place(x=230,y=36)
btn111=Button(window,text="입력", command = GetVideoName)
btn111.place(x=510,y=5)
btn222=Button(window,text="다시하기",bg='palegreen', command = ClearEntry1)
btn222.place(x=620,y=5)

btn3=Button(window, text="저장하기", command = FileSave, bg="lightpink")
btn3.place(x=550, y = 325)
btn4=Button(window, text="하이라이트생성", command = Gh, bg="gold")
btn4.place(x=550, y = 280)

Checkbtn1 = Checkbutton(window,text="Goal",variable = g, command = GetVar, bg="lightgrey",onvalue=1, offvalue=0)
Checkbtn1.place(x=550,y=80)
Checkbtn2 = Checkbutton(window,text="Card", variable = yc, command = GetVar, bg="lightgrey",onvalue=1, offvalue=0)
Checkbtn2.place(x=550,y=110)
Checkbtn3 = Checkbutton(window,text="Subtitution", variable = sub, command = GetVar, bg="lightgrey",onvalue=1, offvalue=0)
Checkbtn3.place(x=550,y=140)
Checkbtn4 = Checkbutton(window,text="CornerKick", variable = corner, command = GetVar, bg="lightgrey",onvalue=1, offvalue=0)
Checkbtn4.place(x=550,y=170)
Checkbtn5 = Checkbutton(window,text="Audio HIghlight", variable = a, command = GetVar, bg="lightgrey",onvalue=1, offvalue=0)
Checkbtn5.place(x=550,y=200)

#동영상 프레임
frm = Frame(window, bg="white", width=500, height=300)
frm.place(x=10, y=70)
lblf = Label(frm)
lblf.place(x=0,y=0)
os.chdir("C:\\Users\\dneir\\Downloads\\labels")
cap = cv.VideoCapture("2_NY Red Bulls trick corner.mp4")

def video_play():
    ret, frame = cap.read()

    if not ret:
        cap.release()
        print("비디오 안열림")
        return
    frame = imutils.resize(frame, width=500,height=400)
    img = Image.fromarray(frame)
    #img = cv.resize(img, dsize=(320, 480), interpolation=cv.INTER_AREA)
    imgtk = ImageTk.PhotoImage(image=img)
    lblf.imgtk = imgtk
    lblf.configure(image=imgtk)
    lblf.after(10,video_play)

video_play()

window.mainloop()
#print(type(file_dir))
print(goal, card, substitution, cornerkick)