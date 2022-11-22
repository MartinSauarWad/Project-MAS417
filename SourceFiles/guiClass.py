import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from SourceFiles import dataGetterClass
from SourceFiles import CheckButtonClass
from SourceFiles import stlMaker






class GUI:

    def __init__(self):
        self.stlFileNumber = 1
        self.bgColor = '#000000'
        self.buttonBgColor = '#3C415C'
        self.satGetter = dataGetterClass.dataGetter()
        self.root = tk.Tk()
        self.satNamesAndIDs = {}
        self.satCoords = {}
        self.selectedSats = []
        self.width= self.root.winfo_screenwidth()               
        self.height= self.root.winfo_screenheight()               
        self.root.geometry("%dx%d" % (self.width, self.height))
        self.root.title("Display satellites")
        self.root.config(background=self.bgColor)
        self.goToPage("MAIN_MENU")
        

    def checkValidSelection(self):
        if len(self.selectedSats) <= 0:
            tk.messagebox.showerror("Ikke prøv deg, Muri!", "Vi tok høyde for dette...")
            return
        else:
            self.goToPage("LOADING_SCREEN_2")

    def goToPage(self, toPage):
        self.clearWindow()

        if toPage == "MAIN_MENU":
            img = self.prepImage("earth.png", fitToScreenX=True)
            img = ImageTk.PhotoImage(img)
            panel = tk.Label(self.root, image=img, bg=self.bgColor)
            panel.photo = img
            panel.place(relx=0.5, rely=0.6,anchor= 'center')#(0.5, 0.6)

            tk.Label(self.root,
                     text="Welcome to the satellite position stl generator",
                     font=('Comic Sans', 30, 'bold'),
                     fg='black',
                     bg=self.buttonBgColor,
                     relief=tk.RAISED,
                     bd=6,
                     padx=15,
                     pady=15).place(relx=0.5, rely=0.1,anchor= 'center') 

            tk.Button(self.root, text="START", padx=60, pady=20, relief=tk.RAISED, fg='white', bg=self.buttonBgColor, command=lambda: self.goToPage("LOADING_SCREEN_1")).place(relx=0.9, rely=0.9,anchor= 'center')
            tk.Button(self.root, text="QUIT", padx=60, pady=20, relief=tk.RAISED, fg='white', bg=self.buttonBgColor, command=self.root.quit).place(relx=0.1, rely=0.9,anchor= 'center')
            
        #------------------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------------------

        elif toPage == "SELECTION_SCREEN":
            self.selectedSats.clear()

            img = self.prepImage("earth-horizon.jpg", fitToScreenX=True)
            img = ImageTk.PhotoImage(img)
            panel = tk.Label(self.root, image=img, bg=self.bgColor)
            panel.photo = img
            panel.place(relx=0.5, rely=0.85,anchor= 'center')

            label1 = tk.Label(self.root,
                            text="You may select up to 5 satellites you want to display",
                            font=('Comic Sans', 20, 'bold'),
                            fg='#000000',
                            bg='#3C415C',
                            relief=tk.RAISED,
                            bd=6,
                            padx=15,
                            pady=15)
            label1.pack()

            satelitteOutline = tk.Frame(self.root, bg='#807e7d')
            satelitteOutline.columnconfigure(0, weight=1)
            satelitteOutline.columnconfigure(2, weight=1)
            satelitteOutline.columnconfigure(1, weight=1)
            satelitteOutline.columnconfigure(3, weight=1)
            satelitteOutline.columnconfigure(4, weight=1)
            satelitteOutline.columnconfigure(5, weight=1)

            satNames = list(self.satNamesAndIDs.keys())
            satIDs = list(self.satNamesAndIDs.values())

            for i in range(len(self.satNamesAndIDs.keys())):
                gridPosX = i % 6
                gridPosY = i // 6
                CheckButtonClass.selectionButton(satelitteOutline, satNames[i], satIDs[i], gridPosX, gridPosY, self.selectedSats).drawSelf()
                
            satelitteOutline.pack(fill='x')
            #self.goToPage("LOADING_SCREEN_2")
            tk.Button(self.root, text="SELECT",padx=60, pady=20, relief=tk.RAISED, bg=self.buttonBgColor, command=lambda: self.checkValidSelection()).place(relx=0.9, rely=0.9, anchor='center')
            tk.Button(self.root, text="QUIT", padx=60, pady=20, relief=tk.RAISED, bg=self.buttonBgColor, command=self.root.quit).place(relx=0.1, rely=0.9, anchor='center')
        
        #------------------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------------------

        elif toPage == "DISPLAY_DATA": 
            #Shows the data for the selected satellites to the user
            #The user can choose to generate an STL with this data, or go back and select other satellites

            #Place the background image
            img = self.prepImage("esb.png", fitToScreenX=True)
            img = ImageTk.PhotoImage(img)
            panel = tk.Label(self.root, image=img, bg=self.bgColor)
            panel.photo = img
            panel.place(relx=0.5, rely=0.5,anchor= 'center')

            #Place the info- text on the top of the window
            tk.Label(self.root,
                     text="Your chosen satellites",
                     font=('Comic Sans', 30, 'bold'),
                     fg='#000000',
                     bg='#3C415C',
                     relief=tk.RAISED,
                     bd=6,
                     padx=15,
                     pady=15).pack()

            #Display the coordinates of the selected satellites
            i = 0
            for id, coord in self.satCoords.items():
                tk.Label(self.root,
                     text=f"{id}   {coord}",
                     font=('Comic Sans', 15, 'bold'),
                     fg='#FFFFFF',
                     bg='#000000',
                     bd=6,
                     padx=15,
                     pady=15).place(relx=0.5, rely=0.2+0.08*i,anchor= 'center')
                i += 1

            tk.Button(self.root, text="CONFIRM", font=('Comic Sans', 15), padx=40, pady=15, relief=tk.RAISED, bg=self.buttonBgColor, command=lambda: self.goToPage("LOADING_SCREEN_3")).place(relx=0.9, rely=0.9,anchor= 'center')
            tk.Button(self.root, text="SELECT AGAIN", font=('Comic Sans', 15), padx=30, pady=15, relief=tk.RAISED, bg=self.buttonBgColor, command=lambda: self.goToPage("SELECTION_SCREEN")).place(relx=0.15, rely=0.9,anchor= 'center')


        #------------------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------------------

        elif toPage == "LOADING_SCREEN_1":
            #Loading screen shown when fetching the available satellites

            #Place the background image 
            img = self.prepImage("satellite above earth getty.webp", fitToScreenX=True)
            img = ImageTk.PhotoImage(img)
            panel = tk.Label(self.root, image=img, bg=self.bgColor, width=self.width)
            panel.photo = img
            panel.place(relx=0.5, rely=0.6,anchor= 'center')

            label1 = tk.Label(self.root,
                            text="Fetching available satellites. Please wait...",
                            font=('Comic Sans', 30, 'bold'),
                            fg='#000000',
                            bg='#3C415C',
                            relief=tk.RAISED,
                            bd=6,
                            padx=15,
                            pady=15).pack()

            self.root.update()

            if len(self.satNamesAndIDs.keys()) == 0:
                #Feilhåndtering her
                #urllib.error.URLError: <urlopen error [Errno 11001] getaddrinfo failed>
                self.satNamesAndIDs = self.satGetter.getSatNamesAndIDs()

            self.goToPage("SELECTION_SCREEN")

        #------------------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------------------

        elif toPage == "LOADING_SCREEN_2":
            #Loading screen when fetching coordinates of the selected satellites

            #Place the background image 
            img = self.prepImage("asdasdasd.webp", fitToScreenX=True)
            img = ImageTk.PhotoImage(img)
            panel = tk.Label(self.root, image=img, bg=self.bgColor, width=self.width)
            panel.photo = img
            panel.place(relx=0.5, rely=0.6,anchor= 'center')

            tk.Label(self.root,
                     text="Fetching coordinates for selected satellites...",
                     font=('Comic Sans', 30, 'bold'),
                     fg='#000000',
                     bg='#3C415C',
                     relief=tk.RAISED,
                     bd=6,
                     padx=15,
                     pady=15).pack()

            self.root.update()
            self.satCoords.clear()#Just in case the user got the data, but changed his mind
            self.satCoords = self.satGetter.getSatCoord(self.selectedSats)
            self.goToPage("DISPLAY_DATA")

        #------------------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------------------

        elif toPage == "LOADING_SCREEN_3": #Lagring av filen skjer her?
            #Loading screen shown when generating the .stl

            #Place the background image
            img = self.prepImage("EarthFromMoon.png", fitToScreenX=True)
            img = ImageTk.PhotoImage(img)
            panel = tk.Label(self.root, image=img, bg=self.bgColor, width=self.width)
            panel.photo = img
            panel.place(relx=0.5, rely=0.6,anchor= 'center')
            
            #Place the info- text at the top of the window
            tk.Label(self.root,
                     text="Generating your STL...",
                     font=('Comic Sans', 30, 'bold'),
                     fg='#000000',
                     bg='#3C415C',
                     relief=tk.RAISED,
                     bd=6,
                     padx=15,
                     pady=15).pack()
            
            self.root.update()

            stlMaker.generateSTL(self.satCoords, self.stlFileNumber)
            self.stlFileNumber += 1
            self.goToPage("END_SCREEN")

        #------------------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------------------

        elif toPage == "END_SCREEN":

            label1 = tk.Label(self.root,
                            text="Your STL is ready",
                            font=('Comic Sans', 30, 'bold'),
                            fg='#000000',
                            bg='#3C415C',
                            relief=tk.RAISED,
                            bd=6,
                            padx=15,
                            pady=15)
            label1.pack()

            tk.Button(self.root, text="MAKE ANOTHER", font=('Comic Sans', 15), padx=25, pady=15, relief=tk.RAISED, bg=self.buttonBgColor, command=lambda: self.goToPage("SELECTION_SCREEN")).place(relx=0.7, rely=0.4,anchor= 'center')
            tk.Button(self.root, text="QUIT", font=('Comic Sans', 15), padx=60, pady=15, relief=tk.RAISED, bg=self.buttonBgColor, command=lambda: self.root.quit()).place(relx=0.3, rely=0.4,anchor= 'center')




    def getSats(self):
        self.satNames = self.satGetter.getSatNamesAndIDs()




    def clearWindow(self):
        elements = self.getAllChildren(self.root)
        for element in elements:
            element.destroy()




    def getAllChildren(self, root):
        childList = root.winfo_children()

        for item in childList :
            if item.winfo_children() :
                childList.extend(item.winfo_children())

        return childList




    def start(self):
        self.root.mainloop()




    def prepImage(self, filename, fitToScreenX=False, fitToScreenY=False):
        img = Image.open(f"Images/{filename}")

        #Scale the image to fit the window in the x- direction
        if fitToScreenX:
            imgWidth, imgHeight = img.size
            aspectRatio = imgWidth / imgHeight
            img = img.resize((self.width, int(round(self.width / aspectRatio))), Image.ANTIALIAS)

        return img