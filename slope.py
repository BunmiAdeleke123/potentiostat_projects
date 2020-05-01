import numpy as np
import tkinter as tk
from tkinter import ttk
from sklearn.linear_model import LinearRegression
from tkinter import *
import matplotlib
matplotlib.use("TKAGG")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import math
import matplotlib.animation as animation
from matplotlib import style
import serial
import serial.tools.list_ports
import time
from tkinter import filedialog
import os
import threading
import warnings
from tkinter import filedialog
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)
label_6=None
t = None
k =None
t1 =None
first=None
ser = None
fact =None
f=None
en =None
en_1 = None
en_2 =None
tset=None
xy=None
LARGE_FONT= ("Verdana",12)

style.use("ggplot")
f = Figure(figsize=(5, 5), dpi=100)
k = Figure(figsize=(5, 5), dpi=100)

q= plt.figure(figsize=(8, 5), dpi=100)
ax1 = f.add_subplot(111)
ax2 = k.add_subplot(111)
ax3 = q.add_subplot(111)
sc = os.path.dirname(os.path.abspath(__file__))


def simple():

    mas = Tk()
    en = StringVar(mas)
    en_1 = StringVar(mas)
    en_2 = StringVar(mas)




    rows = 0
    while rows < 10:
        mas.rowconfigure(rows, weight=5)
        mas.columnconfigure(rows,weight=5)
        rows+=1

    mas.resizable(0, 0)
    label_7= Label(mas,text=" my name", bg="white", fg="black")
    label_7.grid(column=2, row=0)
    ent = Entry(mas,textvar=en)
    ent.grid(column=4, row=0)
    button_1= Button(mas,text="Change...")
    button_1.grid(column=8, row=0)

    label_8= Label(mas,text="Scan Rate", bg="white", fg="black")
    label_8.grid(column=2, row=3)
    ent_1 = Entry(mas,textvar=en_1)
    ent_1.grid(column=4, row=3)
    button_2= Button(mas,text="Change...")
    button_2.grid(column=8, row=3)

    label_9 = Label(mas, text=" Area ", bg="white", fg="black")
    label_9.grid(column=2, row=6)
    ent_2 = Entry(mas, textvar=en_2)
    ent_2.grid(column=4, row=6)
    button_3 = Button(mas, text="Change...")
    button_3.grid(column=8, row=6)



    mas.wm_title("Settings")
    mas.wm_geometry(newGeometry="360x360")




class Sea(tk.Tk):
    def __init__(self, *args , **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Graph")

        menubar = Menu(self)
        Tk.config(self, menu=menubar)
        filemenu = Menu(menubar)
        helpmenu = Menu(menubar)
        expmenu = Menu(menubar)
        menubar.add_cascade(label="File", menu=filemenu)
        menubar.add_cascade(label="Experiment", menu=expmenu)
        menubar.add_cascade(label="Help", menu=helpmenu)

        filemenu.add_command(label='Open')
        filemenu.add_command(label='Settings', command=simple)
        filemenu.add_command(label='About')
        filemenu.add_command(label='Import')
        helpmenu.add_command(label='Information')

        expmenu.add_command(label='potetentiodynamic')
        expmenu.add_command(label='Potentiostatic')

        container = tk.Frame(self)
        container.pack(side="top", fill ="both", expand = True)
        container.grid_rowconfigure(0,weight=1)
        self.frames = {}

        for F in (StartPage,PageOne,PageTwo, PageThree):
            frame = F(container , self)
            self.frames[F] = frame
            frame.grid(row=0,column=0, sticky="nsew")
            self.show_frame(StartPage)

    def show_frame(self,cont):
        frame= self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        ports = list(serial.tools.list_ports.comports())
        self.portlists =['']
        for p in ports:
            self.portlists.append(p.device)

        label_5 = tk.Label(self, text="", bg="#89CFF0", height="3",  relief="groove",font=("axial", 19, "bold", "italic"))
        label_5.pack(fill=tk.X)
        #label = tk.Label(self, text = "Page ", font = LARGE_FONT)
        #label.place(x=500,y=10)


        button1 = ttk.Button(self, text = "Back", command= lambda: controller.show_frame(StartPage))

        button1.place(x = 30, y= 10)

        button2 = ttk.Button(self, text="Page 1", command=lambda: controller.show_frame(PageOne))

        button2.place(x=90, y= 10)

        button4 = ttk.Button(self, text="Check graph", command=Tafel)

        button4.place(x=160, y=10)
        fn = StringVar(self)
        sn = StringVar(self)
        dob = StringVar(self)
        nf= StringVar(self)

        label_0 = tk.Label(self,text ="",bg="white", fg="white", borderwidth=1, relief="sunken",font = ("axial", 19,"bold"))
        label_0.pack(fill=tk.X)

        l_child=tk.Label(self,text="Tafel",bg="#89CFF0",width=10,fg="white", font=("Helvetica", 8, "bold", "italic"))
        l_child.place(x=30, y=100)

        l_child = tk.Label(self, text="Current", bg="#89CFF0", width=10, fg="white", font=("Helvetica", 8, "bold", "italic"))
        l_child.place(x=120, y=100)

        l_child = tk.Label(self, text="Volt", bg="#89CFF0", width=10, fg="white", font=("Helvetica", 8, "bold", "italic"))
        l_child.place(x=220, y=100)

        l_child = tk.Label(self, text="", bg="#89CFF0", width=60, fg="white", font=("axial", 8, "bold", "italic"))
        l_child.place(x=310, y=100)

        self.pvar = StringVar(self)
        self.pvar.set("COM3")
        self.droplist = OptionMenu(self,self.pvar,*self.portlists)
        self.droplist.place(x=450,y=220)

        def change_dropdown(*args):
            return(self.pvar.get())
        self.pvar.trace('w',change_dropdown)
        label_1 = tk.Label(self, text="COM PORT:",fg="#89CFF0", width = 30,font=("Helvetica", 12, "bold", "italic"))
        label_1.place(x=200, y=200)

        label_2 = tk.Label(self, text="SCAN RATE:",fg="#89CFF0", width = 30,font=("Helvetica", 12, "bold", "italic"))
        label_2.place(x=200, y=300)

        entry_1 =tk.Entry(self,textvar=sn)
        entry_1.place(x =450, y= 300)

        label_3 = tk.Label(self, text="FILE NAME:",fg="#89CFF0", width=30, font=("Helvetica", 12, "bold", "italic"))
        label_3.place(x=200, y=400)

        entry_1 = tk.Entry(self, textvar=nf)
        entry_1.place(x=450, y=400)

        lb= Listbox(self, width=30)
        lb.pack(side=tk.LEFT, fill=tk.Y)
        lb.insert(END, "Fist entry")
        lb.insert(END, "Fist entry")
        lb.insert(END, "Fist entry")
        sb= Scrollbar(self, orient=VERTICAL)
        sb.config(command=lb.yview)
        sb.pack(side=tk.LEFT,fill=tk.Y)

        lb.config(yscrollcommand=sb.set)
        for x in range(100):
            lb.insert(END,"")


        def printt():

            global first
            global fact
            first = fn.get()
            sec = sn.get()
            date = dob.get()
            fact= nf.get()
            global ser
            ser = serial.Serial(self.pvar.get(), baudrate=9600, timeout=0)

            if ser.isOpen():
                label_6.configure(text="connected")
                controller.show_frame(PageThree)
                msg = "b"
                ser.write(msg.encode())

                def tim():
                    global t
                    t = threading.Timer(1.0, tim)
                    t.start()


                    def getValue():
                        data = None
                        data = ser.readline().decode('ascii')
                        return (str(data))

                    xy = os.path.join(sc, fact)

                    with open(xy, 'a', encoding="utf-8") as f:
                        k = getValue()
                        a = k.split(",")

                        if len(a) == 3:
                            if (a[0] and a[1]) != None:
                                try:
                                    d = float(a[0])
                                    e = float(a[1])
                                    if type(d) and type(e) is float:

                                        f.write(k)
                                        print("I passed the test")
                                    else:
                                        print("Not a float")

                                except ValueError:
                                    print("This is not a float")
                            else:
                                print("you have a None")

                        else:
                            f.write(k)



                tim()
            else:
                label_6.configure(text="cannot connect")

                print("Not connected")
            print("{},{},{}".format(first,sec, date))

        def exitt():
            if t is not None:
                t.cancel()
                label_6.configure(text="Not connected")
                ser.close()
            else:
                label_6.configure(text="Not connected")
                ser.close()



        but_quit = Button(self, text="Submit", width=12, bg='#89CFF0', fg='white', command=printt).place(x=280, y=450)
        but_quit = Button(self, text="Quit", width=12, bg='#89CFF0', fg='white', command=exitt).place(x=400, y=450)
        label_6 = tk.Label(self, text="Not connected",bg='brown', fg='white', width = 20,font=("bold",10))
        label_6.place(x=850,y=600)

    def exitt():
        if t is not None:
            t.cancel()
            label_6.configure(text="Not connected")
            ser.close()
        else:
            label_6.configure(text="Not connected")
            ser.close()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Page 1", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))

        button1.pack()
        button2 = ttk.Button(self, text="Page2", command=lambda: controller.show_frame(PageTwo))

        button2.pack()




class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page 2", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))

        button1.pack()
        button2 = ttk.Button(self, text="page 1", command=lambda: controller.show_frame(PageOne))

        button2.pack()


class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page ", font=LARGE_FONT)

        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back", command=lambda: controller.show_frame(StartPage))

        button1.pack()
        button2 = ttk.Button(self, text="Stop",command=StartPage.exitt)
        button2.pack()
        mainFrame= Frame(self,bg='#89CFF0')
        mainFrame.pack()

        canvas = FigureCanvasTkAgg(f, mainFrame)

        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, mainFrame)
        toolbar.update()

        canva = FigureCanvasTkAgg(k, mainFrame)

        canva.get_tk_widget().pack()
        bar = NavigationToolbar2Tk(canva, mainFrame)
        bar.update()
def exittt():
    t.cancel()
    ser.close()

def xitt():
    if t is not None:
        t.cancel()
        exit()
    else:
        exit()

class Tafel(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)


        mainFrame = Frame(self, bg='#89CFF0')
        mainFrame.pack()

        print("ok")
        menubar1 = Menu(self)
        Tk.config(self,menu=menubar1)
        filemenu = Menu(menubar1)
        menubar1.add_cascade(label="Analysis", menu=filemenu)

        filemenu.add_command(label='Plot Tafel', command =self.file)

        filemenu.add_command(label='Plot points selected', command=self.linear)
        filemenu.add_command(label='Point Selected', command=self.pointsel)
        filemenu.add_command(label='Clear Plot', command=self.linearclear)
        filemenu.add_command(label='Save', command=self.save)
        can = FigureCanvasTkAgg(q, mainFrame)

        can.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        plt.ion()
        self.cursor = Cursor(ax3,horizOn=True,lw=1)

        q.canvas.mpl_connect("button_press_event",self.onclick)
        self.listx= []
        self.listy=[]
    def onclick(self,event):
        x1,y1 = event.xdata, event.ydata
        print("{},{}".format(x1,y1))
        if x1 and y1 is not None:
            e = self.listx.append(x1)
            f = self.listy.append(y1)
        else:
            print("Guy None value detected")
        self.lis()
    def lis(self):
        print("{},{}".format(self.listx,self.listy))

    def pointsel(self):
        mas = Tk()
        rows = 0
        while rows < 10:
            mas.rowconfigure(rows, weight=5)
            mas.columnconfigure(rows, weight=5)
            rows += 1

        mas.resizable(0, 0)
        label_7 = Label(mas, text=" x and y: {}, {} ".format(self.listx[0],self.listy[0]), bg="white", fg="black")
        label_7.grid(column=2, row=0)

        mas.wm_title("The Points Selected")
        mas.wm_geometry(newGeometry="360x100")
        self.listx, self.listy= [],[]

    def linear(self):
        valx= np.linspace(self.listx[0],self.listx[-1],100)
        valy = np.linspace(self.listy[0], self.listy[-1], 100)

        x1 = np.array(valx[:]).reshape((-1, 1))
        y = np.array(valy[:])

        model = LinearRegression().fit(x1, y)

        y_pred = model.predict(x1)

        new = y_pred.tolist()

        e =int(len(new) / 2)
        f = int(len(x1) / 2)

        print(f)
        slop = (new[e+5]-new[e]) /(x1[f+5]-x1[f])
        ax3.plot(x1, y_pred, color="blue")

        self.listx, self.listy = [], []
        try:
            def slope():
                mas = Tk()
                rows = 0
                while rows < 10:
                    mas.rowconfigure(rows, weight=5)
                    mas.columnconfigure(rows, weight=5)
                    rows += 1

                mas.resizable(0, 0)
                label_7 = Label(mas, text=" The slope is {}".format(slop), bg="white", fg="black")
                label_7.grid(column=2, row=0)

                mas.wm_title("Slope of the line")
                mas.wm_geometry(newGeometry="360x100")
            slope()
        except:
            pass


    def linearclear(self):
        plt.cla()

    def analyses(self):
        global en
        global en_1
        global en_2
        mas = Tk()
        en =StringVar(mas)
        en_1 =StringVar(mas)
        en_2 = StringVar(mas)
        rows = 0
        while rows < 10:
            mas.rowconfigure(rows, weight=5)
            mas.columnconfigure(rows, weight=5)
            rows += 1

        mas.resizable(0, 0)
        label_7 = Label(mas, text=" Set X1 interval", bg="white", fg="black")
        label_7.grid(column=2, row=0)
        ent = Entry(mas, textvar=en)
        ent.grid(column=4, row=0)

        label_8 = Label(mas, text="Set X2 interval", bg="white", fg="black")
        label_8.grid(column=2, row=3)
        ent_1 = Entry(mas, textvar=en_1)
        ent_1.grid(column=4, row=3)

        label_9 = Label(mas, text=" Set y1 interval ", bg="white", fg="black")
        label_9.grid(column=2, row=6)
        ent_2 = Entry(mas, textvar=en_2)
        ent_2.grid(column=4, row=6)
        button_3 = Button(mas, text="Change...", command= self.locate)
        button_3.grid(column=8, row=6)

        mas.wm_title("Settings")
        mas.wm_geometry(newGeometry="360x360")
    def locate(self):
        x_t = en.get()
        y_t = en_1.get()
        z_t = en_2.get()

        print("{},{}".format(x_t,y_t,z_t))

    def file(self):




        if fact == None:
            global mas
            mas = Tk()
            self.ken = StringVar(mas)
            self.color = StringVar(mas)
            self.label = StringVar(mas)

            rows = 0
            while rows < 10:
                mas.rowconfigure(rows, weight=5)
                mas.columnconfigure(rows, weight=5)
                rows += 1

            mas.resizable(0, 0)
            label_7 = Label(mas, text=" File :", bg="white", fg="black")
            label_7.grid(column=2, row=1)

            ent = Entry(mas, textvar=self.ken)
            ent.grid(column=4, row=1)
            label_7 = Label(mas, text=" color :", bg="white", fg="black")
            label_7.grid(column=2, row=2)
            ent = Entry(mas, textvar=self.color)
            ent.grid(column=4, row=2)

            label_7 = Label(mas, text=" Plot Label :", bg="white", fg="black")
            label_7.grid(column=2, row=3)
            ent = Entry(mas, textvar=self.label)
            ent.grid(column=4, row=3)
            button_1 = Button(mas, text="send..", command=self.click)
            button_1.grid(column=8, row=3)

            mas.wm_title("Enter file name")
            mas.wm_geometry(newGeometry="360x90")



        else:
            print("fact has a value!")
            self.plot_data(fact)



    def click(self):
        global f
        f = self.ken.get()
        col = self.color.get()
        l = self.label.get()
        print(f)

        mas.destroy()

        def plot_data(x, y, lab):

            try:
                data = np.loadtxt(x, delimiter=",", dtype=float)
            except ValueError as e:
                print(e)

            anode1 = []
            anode2 = []
            anode11 = []
            anode12 = []
            anode13 = []
            anode = []
            anode3 = []
            try:
                X = data[:250, 2]
                Y = data[:250, 0]
                Z = data[:250, 1]
                for (i, j) in zip(X, Y):
                    s = math.log10(i)

                    anode1.append(s)
                    anode.append(j - 5 - Y[0])

                    anode3.append(j)

                print(Y[0])
            except:
                pass
            try:
                X = data[250:, 2]
                Y = data[250:, 0]
                Z = data[250:, 1]
                for (i, j) in zip(X, Y):
                    s = math.log10(i)

                    anode11.append(s)
                    anode12.append(-j + 9.5 - Y[0])

                    anode13.append(-j)

                print(Y[0])
            except:
                pass
            ax3.plot(anode11, anode12,  color=y, label=lab)
            ax3.plot(anode1, anode,  color=y)
            ax3.legend(loc="best")
            ax3.set_xlim(0.30, 0.7)
            ax3.set_ylim(-5, 5)
            ax3.set_xlabel('log(i/cm\u00b2)', fontsize=10)
            ax3.set_ylabel('E vs Ag/AgCl', fontsize=10)



            print("done")

        print(l)
        plot_data(f, col, l)

    def plot_data(self,x):



        xy = os.path.join(sc,x)
        print(xy)
        try:
            data = np.loadtxt(xy, delimiter=",", dtype=float)
        except ValueError as e:
            print(e)

        anode1 = []
        anode2 = []
        anode11 = []
        anode12 = []
        anode13 = []
        anode=[]
        anode3 = []
        try:
            X = data[:250, 2]
            Y = data[:250, 0]
            Z = data[:250, 1]
            for (i, j) in zip(X, Y):
                s = math.log10(i)

                anode1.append(s)
                anode.append(j-5-Y[0])



                anode3.append(j)

            print(Y[0])
        except:
            pass
        try:
            X = data[250:, 2]
            Y = data[250:, 0]
            Z = data[250:, 1]
            for (i, j) in zip(X, Y):
                s = math.log10(i)

                anode11.append(s)
                anode12.append(-j+9.5-Y[0])

                anode13.append(-j)

            print(Y[0])
        except:
            pass
        ax3.plot(anode11, anode12, color='blue')
        ax3.plot(anode1, anode, color='blue')
        ax3.set_xlim(0.30, 0.7)
        ax3.set_ylim(-5, 5)

        ax3.set_xlabel('log(i/cm\u00b2)', fontsize=10)
        ax3.set_ylabel('E vs Ag/AgCl', fontsize=10)
        print("done")


    def save(self):
        global kas
        kas = Tk()
        self.r = StringVar(kas)

        rows = 0
        while rows < 10:
            kas.rowconfigure(rows, weight=5)
            kas.columnconfigure(rows, weight=5)
            rows += 1

        kas.resizable(0, 0)
        label_7 = Label(kas, text=" File :", bg="white", fg="black")
        label_7.grid(column=2, row=1)
        ent = Entry(kas, textvar=self.r)
        ent.grid(column=4, row=1)
        button_1 = Button(kas, text="Save", command=self.c)
        button_1.grid(column=8, row=1)

        kas.wm_title("Save as")
        kas.wm_geometry(newGeometry="360x90")
    def c(self):

        plt.savefig(self.r.get())
        kas.destroy()
        Tafel.destroy(self)
        refresh()






class A:
    def animate(i):

        '''luck = 'example.txt'

        graph_data = np.loadtxt(luck, delimiter=",", dtype=float)

        xs = graph_data[:, 0]
        ys = graph_data[:, 1]

        k = graph_data[:, 0]
        z = graph_data[:, 1]
        ks = np.array(k).reshape((1, -1))
        zs = np.array(z).reshape((1, -1))
        l=[]

        o = []
        anode1=[]
        anode2=[]
        for (i, j) in zip(xs, ys):
            if "-" in str(i):
                l.append(i)
                o.append(j)

            else:
                anode1.append(i)
                anode2.append(j)

        s = np.array(l).reshape((1, -1))
        d = np.array(o).reshape((1, -1))
        import numpy.polynomial.polynomial as poly
        coefs1 = poly.polyfit(s.reshape(-1), d.reshape(-1), 3)
        x_new1 = np.linspace(s.reshape(-1)[0], d.reshape(-1)[-1], num=len(l) * 5)

        ffit1 = poly.polyval(x_new1, coefs1)
        ax1.clear()

        ax1.scatter(l, o, c='red')
        ax1.plot(x_new1, ffit1, color='blue')
        ax1.set_xlabel('current', fontsize=10)
        ax1.set_ylabel('voltage', fontsize=10)'''


        if fact == None:
            luck = "r.txt"

            xy = os.path.join(sc, luck)
            try:
                data = np.loadtxt(xy, delimiter=",", dtype=float)
            except IndexError:
                pass

            global l
            global o
            l = []

            o = []
            anode8 = []
            anode9 = []
            try:
                X = data[:, 0]
                Y = data[:, 2]
                Z = data[:, 1]


                for (i, j) in zip(X,Y):

                    anode8.append(i)
                    anode9.append(j)
            except IndexError:
                pass
            w = np.array(anode8).reshape(1, -1)
            e = np.array(anode9).reshape(1, -1)

            import numpy.polynomial.polynomial as poly

            ax2.plot(anode9,anode8, color='red')
            #ax2.plot(o, l, color='blue')
            ax2.set_xlabel('current', fontsize=10)
            ax2.set_ylabel('voltage', fontsize=10)
        else:
            print(fact)
            xy = os.path.join(sc, fact)
            data = np.loadtxt(xy, delimiter=",", dtype=float)




            anode1 = []
            anode2 = []
            anode11 = []
            anode12 = []
            anode13 = []
            anode=[]
            anode3 = []
            try:
                X = data[:250, 2]
                Y = data[:250, 0]
                Z = data[:250, 1]
                for (i, j) in zip(X, Y):
                    s = math.log10(i)

                    anode1.append(s)
                    anode.append(j-5-Y[0])



                    anode3.append(j)

                print(Y[0])
            except:
                pass
            try:
                X = data[250:, 2]
                Y = data[250:, 0]
                Z = data[250:, 1]
                for (i, j) in zip(X, Y):
                    s = math.log10(i)

                    anode11.append(s)
                    anode12.append(j)

                    anode13.append(j)

                print(Y[0])
            except:
                pass
            w = np.array(anode1).reshape(1, -1)
            e = np.array(anode2).reshape(1, -1)

            import numpy.polynomial.polynomial as poly

            ax1.plot(anode11,anode12, color="blue")
            ax2.plot(anode1, anode, color='red')
            ax2.plot(anode1, anode3, color='blue')
            ax2.set_xlabel('current', fontsize=10)
            ax2.set_ylabel('voltage', fontsize=10)
            ax2.set_xlim([0.3,0.8])
            ax2.set_ylim([-5, 0])
            ax1.set_xlim([0.4,0.8])
            ax1.set_ylim([0,5])


class Stat:

    def n():
        print("Pres")

def refresh():
    try:
        re = threading.Thread(target=Sea)
        re.start()
        re.join()
    except RuntimeError as e:
        pass


app = Sea()
app.resizable(0,0)
app.title("POTENTIOSTAT")
ani = animation.FuncAnimation(f, A.animate, interval=1000)
me = animation.FuncAnimation(k, A.animate, interval=1000)
app.configure(bg='blue')
app.protocol("WM_DELETE_WINDOW",xitt)

if __name__=="__main__":
    app.mainloop()

