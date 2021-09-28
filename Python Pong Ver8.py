import tkinter as Tkinter
import math
import random

###############################
''' Python Pong, Anton Dmitriev, 2019'''
###############################
root_main=Tkinter.Tk()

ball_speed=Tkinter.IntVar()
paddle_speed=Tkinter.IntVar()
radius=15
paddle_width=100


global P1score 
P1score = 0
global P2score
P2score = 0
global direction 
direction = random.uniform(0,6.28) #2pi radians in 360 degrees
    
def paddle1_movementUP(event):
    PX1, PY1, PX2, PY2 = canvas.coords(paddle1)
    if PY1<0:
        pass
    else:
        canvas.move(paddle1,0,(-1*paddle_speed.get()))
    
def paddle1_movementDOWN(event):
    PX1, PY1, PX2, PY2 = canvas.coords(paddle1)
    if PY2>600:
        pass
    else:
        canvas.move(paddle1,0,(paddle_speed.get()))

def paddle2_movement(event):
    PX1, PY1, PX2, PY2 = canvas.coords(paddle2)
    paddle_midpointY=PY1+(paddle_width/2)
    x,y = event.x,event.y
    if y<paddle_midpointY:
        if PY1<0:
            pass
        else:
            canvas.move(paddle2,0,(-1*paddle_speed.get()))
    if y>paddle_midpointY:
        if PY2>600:
            pass
        else:
            canvas.move(paddle2,0,paddle_speed.get())

def ball_movement():
    global direction
    global P1score
    global P2score
    #The code below (in lines 56-59, and line 14) was based off of the PLTW Computer Science Principles curriculum, lesson 1.5.3d
    VX= int(ball_speed.get()) * math.cos(direction)
    VY= int(ball_speed.get()) * math.sin(direction)
    canvas.move(ball, VX, VY)
    X1, Y1, X2, Y2 = canvas.coords(ball)
    P1_X1, P1_Y1, P1_X2, P1_Y2 = canvas.coords(paddle1)
    P2_X1, P2_Y1, P2_X2, P2_Y2 = canvas.coords(paddle2)
    #Bouncing Off Of Walls
    if X1 < 0:
        direction = math.pi - direction
        P2score+=1
    if X2 > canvas.winfo_width():
        direction = math.pi - direction
        P1score+=1
    if Y1 < 0:
        direction = -1 * direction
    if Y2 > canvas.winfo_height():
        direction = -1 * direction
    #Bouncing Off of Paddle 1 Front
    if X1<P1_X2 and (P1_Y1<Y1<P1_Y2 or P1_Y1<Y2<P1_Y2):
        direction = math.pi - direction
    #Bouncing Off of Paddle 1 Sides
    if P1_X1<X1<P1_X2 and (P1_Y1<Y2<P1_Y2 or P1_Y1<Y1<P1_Y2):
        direction = -1 * direction
    #Bouncing Off of Paddle 2 Front
    if X2>P2_X1 and (P2_Y1<Y1<P2_Y2 or P2_Y1<Y2<P2_Y2):
        direction = math.pi - direction
    #Bouncing Off of Paddle 2 Sides
    if P2_X1<X2<P2_X2 and (P2_Y1<Y2<P2_Y2 or P2_Y1<Y1<P2_Y2):
        direction = -1 * direction
    #Changing font color to the current winner
    if P1score>P2score:
        scorebox.config(fg='red')
    elif P2score>P1score:
        scorebox.config(fg='blue')
    elif P1score==P2score:
        scorebox.config(fg='purple')
    scorebox.config(text="Red: "+str(P1score)+" vs "+"Blue: "+str(P2score))
    recursion=canvas.after(1,ball_movement)
    if P1score+P2score==15:
        root_main.after_cancel(recursion)
        if P1score>P2score:
            scorebox.config(text="Red Wins!!! With "+str(P1score)+" Points!", fg = 'red')
        elif P2score>P1score:
            scorebox.config(text="Blue Wins!!! With "+str(P2score)+" Points!", fg = 'blue')

def start():
    ball_movement()

def restart():
    global P1score
    global P2score
    if P1score+P2score<15:
        pass
    else:
        recursion=canvas.after(1,ball_movement)
        root_main.after_cancel(recursion)
        P1score=0 
        P2score=0
        canvas.coords(ball,500-radius,300-radius,500+(2*radius),300+(2*radius))
        canvas.coords(paddle1,5,paddle_initialY1,25,paddle_initialY2)
        canvas.coords(paddle2,999,paddle_initialY1,979,paddle_initialY2)
        scorebox.config(text="Red: "+str(P1score)+" vs "+"Blue: "+str(P2score), fg = 'black')
        start()

canvas = Tkinter.Canvas(root_main, height = 600, width = 1000, background = '#FFFFFF')
canvas.grid(row = 4, column = 2, rowspan = 1)

welcome_text = Tkinter.Label(root_main, text = "Welcome to Python Pong!\nMade By Anton Dmitriev")
welcome_text.grid(row=0,column=0)

paddle_initialY1=(600-paddle_width)/2
paddle_initialY2=((600-paddle_width)/2)+paddle_width


ball=canvas.create_oval(500-radius,300-radius,500+(2*radius),300+(2*radius), fill='#000000')

paddle1=canvas.create_rectangle(5,paddle_initialY1,25,paddle_initialY2, fill='#FF0000')
paddle2=canvas.create_rectangle(999,paddle_initialY1,979,paddle_initialY2, fill='#0000FF')

root_main.bind("<w>", paddle1_movementUP)
root_main.bind("<s>", paddle1_movementDOWN)
root_main.bind("<B1-Motion>", paddle2_movement)
root_main.bind("<B1-Motion>", paddle2_movement)


start_button=Tkinter.Button(root_main,text="Start Game!",command=start)
start_button.grid(row=1,column=0)
playagain_button=Tkinter.Button(root_main,text="Play Again!",command=restart)
playagain_button.grid(row=2,column=0)

scorebox=Tkinter.Label(root_main, text="Red: "+str(P1score)+" vs "+"Blue: "+str(P2score), font=("Courier", 44), fg='black')

scorebox.grid(row=0,column=2)

instructions_text = Tkinter.Label(root_main, text = "Move the Red Paddle with the w + s keys!\nMove the Blue Paddle by left clicking and dragging up or down!")
instructions_text.grid(row=3,column=0)


ball_speedSlider=Tkinter.Scale(root_main, from_=0, to=30, label="Ball Speed", variable=ball_speed)
ball_speedSlider.grid(row=4,column=0)
ball_speedSlider.set(15)

paddle_speedSlider=Tkinter.Scale(root_main,from_=0, to=30, label="Paddle Speed", variable=paddle_speed)
paddle_speedSlider.grid(row=4,column=1)
paddle_speedSlider.set(20)
 
###############################
root_main.mainloop()