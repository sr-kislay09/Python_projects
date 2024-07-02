
from tkinter import *
import pandas as pd
import folium
import io
import os
import webbrowser
from folium.plugins import MousePosition
import jinja2
import Map
import voicerec
import tkinter.messagebox
import deploy


class MyWindow:

    def __init__(self, win):
        self.ships = pd.read_csv('Shipdatabase.csv', encoding='cp1252')
        self.ships.head(3)

        self.aps = (self.ships.iloc[list(
            self.ships['Best Suited for'] == 'Anti Piracy')])
        self.res = (self.ships.iloc[list(
            self.ships['Best Suited for'] == 'Refueling')])
        self.pas = (self.ships.iloc[list(
            self.ships['Best Suited for'] == 'Patrolling')])
        self.ros = (self.ships.iloc[list(
            self.ships['Best Suited for'] == 'Relief Operation')])
        self.destroyers = (self.ships.iloc[list(
            self.ships['Type'] == 'Destroyer')])
        self.frigates = (self.ships.iloc[list(
            self.ships['Type'] == 'Frigate')])
        self.tankers = (self.ships.iloc[list(self.ships['Type'] == 'Tanker')])

        self.directory = os.path.dirname(__file__)
        # self.path=self.directory+"/"
        self.path = self.directory + "/"
        self.bg = PhotoImage(file=self.path+"1.png")
        self.lblbg = Label(window, image=self.bg)
        self.lblbg.place(x=0, y=0)

        self.lblTargetLat = Label(
            win, text="Target Latitude", fg='black', font=("Times", 16))
        self.lblTargetLat.place(x=50, y=100)
        self.txtfldTargetLat = Text(window, height=1, width=20)
        self.txtfldTargetLat.place(x=260, y=100)
        # self.txtfldTargetLat.pack(expand=True)

        self.lblTargetLon = Label(
            win, text="Target Longitude", fg='black', font=("Times", 16))
        self.lblTargetLon.place(x=50, y=150)
        self.txtfldTargetLon = Text(window, height=1, width=20)
        self.txtfldTargetLon.place(x=260, y=150)

        #self.inp = self.inputtxt.get(1.0, "end-1c")
        #self.inputtxt = tk.Text(frame,height = 5,width = 20)

        #self.txtfldTargetLoc.insert(0, "Lat Long")
        #self.txtfldTargetLoc.place(x=250, y=100)
        self.lblShipDeployment = Label(
            win, text="SHIP DEPLOYMENT SYSTEM", fg='red', font=("Times", 26))
        self.lblShipDeployment.place(x=130, y=40)

       # self.inputtxt = Text(win,height = 5,width = 20)

        self.btnGlobalStatus = Button(win, text='Global Status')
        self.btnGlobalStautsBind = Button(win, text='Global Status', font=(
            "Arial Bold", 13), width=10, height=2, command=self.globalStatus)
        self.btnGlobalStautsBind.place(x=50, y=500)

        self.btnGiveCommand = Button(win, text='Say It!!')
        self.btnGiveCommand = Button(win, text='Say It!!', font=(
            "Arial Bold", 14), width=10, height=2, command=self.sayIt)
        self.btnGiveCommand.place(x=50, y=400)

        self.btnExit = Button(win, text='Exit')
        self.btnExit = Button(win, text='Exit', font=(
            "Arial Bold", 13), width=8, height=2, command=self.exitFunc)
        self.btnExit.place(x=570, y=500)

        #self.lblTargetLoc=Label(win, text="Target Location", fg='red', font=("Helvetica", 16))

    def select_ship_color(self, shipName):
        if shipName == 'Anti Piracy':
            return 'red'
        if shipName == 'Refueling':
            return 'orange'
        if shipName == 'Patrolling':
            return 'green'
        if shipName == 'Destroyer':
            return 'lightred'
        if shipName == 'Frigate':
            return 'beige'
        if shipName == 'Tanker':
            return 'black'
        elif shipName == 'Relief Operation':
            return 'cadetblue'
        return 'blue'

    def printInput(self):
        self.inp_lat = self.txtfldTargetLat.get(1.0, "end-1c")
        self.inp_lon = self.txtfldTargetLon.get(1.0, "end-1c")
        lat = self.inp_lat
        lon = self.inp_lon
        print(self.inp_lat)
        print(self.inp_lon)

    def sayIt(self):
        print("say it ::: ")
        self.inp_lat = self.txtfldTargetLat.get(1.0, "end-1c")
        self.inp_lon = self.txtfldTargetLon.get(1.0, "end-1c")
        lat = self.inp_lat
        lon = self.inp_lon
        self.command = voicerec.listen()
        print(self.command)
        a = self.command.__contains__(b"refuel")
        q = self.command.__contains__(b"anti")
        c = self.command.__contains__(b"patrol")
        d = self.command.__contains__(b"relief")
        e = self.command.__contains__(b"destroy")
        f = self.command.__contains__(b"gate")
        g = self.command.__contains__(b"tanker")

        if a:
            print("Refueling Status")
            aa = Map.plotMap(self.res, 'Refueling',
                             self.select_ship_color('Refueling'))
            op, fdf = deploy.diss("Refueling", lat, lon)
            result = fdf.iloc[[0, 1, 2]]
            ca = Map.plotCmdMap(result, 'Refueling', 'black')

            tkinter.messagebox.showinfo('BEST SUITED SHIP', op)
        elif q:
            print("Anti Piracy Status")
            aa = Map.plotMap(self.aps, 'Anti Piracy',
                             self.select_ship_color('Anti Piracy'))
            op, fdf = deploy.diss("Anti Piracy", lat, lon)
            result = fdf.iloc[[0, 1, 2]]
            ca = Map.plotCmdMap(result, 'Anti Piracy', 'black')

            tkinter.messagebox.showinfo('BEST SUITED SHIP', op)
        elif c:
            print("Patrolling Status")
            aa = Map.plotMap(self.pas, 'Patrolling',
                             self.select_ship_color('Patrolling'))
            op, fdf = deploy.diss("Patrolling", lat, lon)
            result = fdf.iloc[[0,1, 2]]


            ca = Map.plotCmdMap(result, 'Patrolling', 'black')

            tkinter.messagebox.showinfo('BEST SUITED SHIP', op)
        elif d:
            print("Relief Operation Status")
            aa = Map.plotMap(self.ros, 'Relief Operation',
                             self.select_ship_color('Relief Operation'))
            op, fdf = deploy.diss("Relief Operation", lat, lon)
            result = fdf.iloc[[0,1, 2]]
            ca = Map.plotCmdMap(result, 'Relief Operation', 'black')
            tkinter.messagebox.showinfo('BEST SUITED SHIP', op)
        elif e:
            print("Destroyers Status")
            ca = Map.plotMap(self.destroyers, 'Destroyer',
                             self.select_ship_color('Destroyer'))
        elif f:
            print("Frigates Status")
            ca = Map.plotMap(self.frigates, 'Frigate',
                             self.select_ship_color('Frigate'))
        elif g:
            print("Tankers Status")
            ca = Map.plotMap(self.tankers, 'Tanker',
                             self.select_ship_color('Tanker'))
        else:
            tkinter.messagebox.showinfo(
                "PLEASE SPEAK AGAIN",  "COULDN'T RECOGNIZE")
            print("PLEASE GIVE COMMAND AGAIN")

    def exitFunc(self):
        print("Exit")
        window.destroy()

    def antiPiracyStatus(self):
        print("Anti Piracy Status")
        ca = Map.plotMap(self.aps, 'Anti Piracy',
                         self.select_ship_color('Anti Piracy'))

    def refulingStatus(self):
        print("Refueling Status")
        ca = Map.plotMap(self.res, 'Refueling',
                         self.select_ship_color('Refueling'))

    def patrollingStatus(self):
        print("Patrolling Status")
        ca = Map.plotMap(self.pas, 'Patrolling',
                         self.select_ship_color('Patrolling'))

    def reliefOperationStatus(self):
        print("Relief Operation Status")
        ca = Map.plotMap(self.ros, 'Relief Operation',
                         self.select_ship_color('Relief Operation'))

    def globalStatus(self):
        print("Global Status")
        ca = Map.plotMap(self.ships, 'Global Operation', 'blue')
        '''
        self.antiPiracyStatus()
        self.refulingStatus()
        self.patrollingStatus()
        self.reliefOperationStatus()'''

    def add(self):
        self.t3.delete(0, 'end')
        num1 = int(self.t1.get())
        num2 = int(self.t2.get())
        result = num1+num2
        self.t3.insert(END, str(result))

    def sub(self, event):
        self.t3.delete(0, 'end')
        num1 = int(self.t1.get())
        num2 = int(self.t2.get())
        result = num1-num2
        self.t3.insert(END, str(result))


window = Tk()
mywin = MyWindow(window)
'''directory=os.path.dirname(__file__)
path=directory+"/"
bgpath=path+"1.jpg"
'''
# Add image file
# directory=os.path.dirname(__file__)
# path=directory+"/"
#bg = PhotoImage(file = path+"1.png")

# Show image using label


window.title('SHIP DEPLOYMENT SYSTEM')
window.geometry("700x600+10+10")

window.mainloop()
