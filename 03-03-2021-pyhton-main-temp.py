import serial,time
from tkinter import *
from datetime import date
uart = serial.Serial()
uart.port = "COM4"
uart.bytesize = serial.EIGHTBITS
uart.baudrate = 9600
uart.parity = serial.PARITY_NONE
uart.stopbits = serial.STOPBITS_ONE
uart.timeout = 1
uart.open()

today1 = ''
time1 = ''
def tick():
    global time1
    time2 = time.strftime('%H:%M:%S')
    if time2 != time1:
        time1 = time2
        lbl_time.config(text=time2)
    lbl_time.after(200, tick)
def datetostring():
    global today1
    today2 = date.today()
    if today2 != today1:
        today1 = today2
        lbl_date.config(text=today2)
    lbl_date.after(3600,datetostring)
def SEND1():
    global lbl_Temp,lbl_Ans
    DATA = uart.inWaiting()
    if DATA != 0:
        DATA2 = uart.read(DATA)
        if len(DATA2) == 6:
            Temp_01 = str(hex(DATA2[2])).split('0x')
            Temp_02 = str(hex(DATA2[3])).split('0x')
            ANS = int("0x" + Temp_01[1] + Temp_02[1], 16)
            lbl_Ans = Label(F2, font=('Arial', 15, 'bold'), text="{:.1f}".format(ANS * 0.1), bg="Tomato", width=8, bd=5).grid(row=1,column=1)
    root.after(500,SEND1)
root = Tk()
root.geometry("1024x300")
root.title("บอสสาระ (เครื่องวัดอุณหภูมิ)")
root.bind("<Escape>",lambda e: root.destroy())

F1 = Frame(root,width=1024,height=50,bg="Spring green")
F1.pack(side=TOP)
lbl_space = Label(F1,font=('Arial',15,'bold'),text="  ",bd=10,anchor='e')
lbl_space.pack(side=LEFT)
lbl_time = Label(F1,font=('Arial',15,'bold'),bd=10,anchor='e')
lbl_time.pack(side=RIGHT)
lbl_date = Label(F1,font=('Arial',15,'bold'),bd=10,anchor='w')
lbl_date.pack(side=RIGHT)
#----------------------------------------------------------------------------------------
F2 = Frame(root,width=1024,height=100)
F2.pack(side=TOP)
lbl_Ans = Label(F2,font=('Arial',15,'bold'),text="36.5",bg="Tomato",width=8,bd=5).grid(row=1,column=1)
lbl_Temp = Label(F2,font=('Arial',15,'bold'),text="TEMP :",bg="Tomato",width=8,bd=5).grid(row=1,column=0)
#----------------------------------------------------------------------------------------
tick()
datetostring()
root.after_idle(SEND1)
root.mainloop()
