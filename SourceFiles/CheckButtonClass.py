import tkinter as tk

class selectionButton:

    def __init__(self, frame_, buttonText, buttonID, xPos_, yPos_, IDs):
        self.state = tk.IntVar()
        self.frame = frame_
        self.text = buttonText
        self.ID = buttonID
        self.xPos = xPos_
        self.yPos = yPos_
        self.fg_color = 'white'
        self.bg_color = '#3C415C'
        self.background_color = '#807e7d'
        self.chosenSatIDs = IDs
        self.button = tk.Checkbutton(frame_,
                                text=buttonText,
                                variable=self.state,
                                onvalue=True,
                                offvalue=False,
                                #command=lambda: passSatelliteID(self.state, self.text),
                                command=lambda: self.passData(self.ID, self.chosenSatIDs),
                                font=("Comic Sans", 15),
                                fg='black',
                                bg=self.bg_color,
                                activeforeground='black',
                                activebackground=self.bg_color,
                                padx=5,
                                pady=5,
                                indicatoron=0,
                                )
    
    def drawSelf(self):
        self.button.grid(row=self.yPos, column=self.xPos, sticky=tk.W+tk.E)
        #self.button.pack()

    def passData(self, ID, satelliteIDList):
        if len(satelliteIDList) >= 5:
            if self.state.get() == True:
                self.state.set(not self.state)
                return
            else:
                satelliteIDList.remove(ID)
                return

        elif self.state.get() == True:
            satelliteIDList.append(ID)
        else:
            satelliteIDList.remove(ID)