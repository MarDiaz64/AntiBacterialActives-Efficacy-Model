#visual aspects in tkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk

#Load data from excel and initiate model 
from Model import Model
model = Model()

#active arrays: (how actives are modeled here may be subject to change, right now only 3 actives are concidered)
activeValue=[0,0,0]

def set_text(text):
    efficacy.delete(0,END)
    efficacy.insert(0,text)
    return

def prediction():
    temp=model.predict(activeValue,float(dilution.get()),float(hValue.get()),float(dValue.get()),float(ph.get()))
    set_text(temp)
    
def addDataPt():
    added=model.updateModel(activeValue,float(dilution.get()),float(hValue.get()),float(dValue.get()),float(ph.get()),float(efficacy.get()),eid.get())
    if added:
        clear()
    
def select_value():
    #clear the boxes
    addName.delete(0,END)
    addValue.delete(0,END)
    
    #get the selected row:
    selected=actives.focus()
    #get the values of the row
    values = actives.item(selected,'values')

    #output to the boxes for editing
    addName.insert(0,values[0])
    addValue.insert(0,values[1])      
        
def clicked(event):  #Click event callback function.
    w=event.widget
    parent = w.nametowidget(w.winfo_parent())
    if parent==leftFrame: #select the row data
        select_value()

def enter(event): #Enter event callback function
    if addName.get()!='':
        update_active()
    
def update_active(): #updates values of the actives
    selected=actives.focus()
    #save new data 
    actives.item(selected,text="",values=(addName.get(),addValue.get()))
    
    #update the list for prediction and DB updates:
    selectedidd= actives.selection()[0]
    activeValue[int(selectedidd)]=float(addValue.get())

   #clear entry boxes
    addName.delete(0,END)
    addValue.delete(0,END)

def clear():
    addName.delete(0,END)
    addValue.delete(0,END)
    dilution.delete(0,END)
    efficacy.delete(0,END)
    ph.delete(0,END)
    for child in actives.get_children():
        actives.set(child, '#2', 0)

        
#beginning of UI script
root = Tk()
root.title("Efficacy Prediction Model V1.0")
root['bg'] = '#000000'
content = ttk.Frame(root)
root.bind('<ButtonRelease-1>', clicked)
root.bind('<Return>',enter)

leftFrame = ttk.Frame(content,width=50, height=100)
#v = Scrollbar(leftFrame), scroll bar will be updated later
#v.config(command=leftFrame.yview)
#v.pack(side=RIGHT,fill=X)

#ACTIVE LABEL AND ADDITION
activeList = []
activeLbl = ttk.Label(content, text="Actives")
addActive= ttk.Button(content, text="+",width=5,command=update_active)
addName= ttk.Entry(content,width=34)
addValue= ttk.Entry(content,width=31)

#ACTIVE TABLE
actives = ttk.Treeview(leftFrame)
actives['columns'] = ('name','value')
actives.column("#0", width=0,  stretch=NO)
actives.column("name",anchor=CENTER)
actives.column("value",anchor=CENTER)

actives.heading("#0",text="",anchor=CENTER)
actives.heading("name",text="Name",anchor=CENTER)
actives.heading("value",text="Value",anchor=CENTER)
actives.pack(side=LEFT,fill=X)

actives.insert(parent='',index='end',iid=0,text='',
values=('DDAC','0'))
actives.insert(parent='',index='end',iid=1,text='',
values=('BKC','0'))
actives.insert(parent='',index='end',iid=2,text='',
values=('Citric','0'))

#OTHER VALUES
other = ttk.Label(content, text="Other Factors")
rightFrame= ttk.Frame(content,width=100, height=100)

dilutionLbl=ttk.Label(rightFrame, text="Dilution")
dilution = ttk.Entry(rightFrame)


#DIRTY OPTIONS
dirtyLbl=ttk.Label(rightFrame, text="Dirty")
#radio buttons for dirty:
dValue = tk.IntVar()
dValue.set(0)
def ShowChoiceD():
    print(dValue.get())
ttk.Radiobutton(rightFrame, 
                   text="No",
                   variable=dValue, 
                   command=ShowChoiceD,
                   value=0).grid(column=4,row=2)
ttk.Radiobutton(rightFrame, 
                   text="Yes",
                   variable=dValue, 
                   command=ShowChoiceD,
                   value=1).grid(column=5,row=2)

#HARDNESS OPTIONS
hardnessLbl=ttk.Label(rightFrame, text="Water Hardness")
#radio buttons for hardness:
hValue = tk.IntVar()
hValue.set(1)
def ShowChoiceH():
    print(hValue.get())
ttk.Radiobutton(rightFrame, 
                   text="Low",
                   variable=hValue, 
                   command=ShowChoiceH,
                   value=0).grid(column=4,row=3)
ttk.Radiobutton(rightFrame, 
                   text="High",
                   variable=hValue, 
                   command=ShowChoiceH,
                   value=1).grid(column=5,row=3)

#PH
pHLbl = ttk.Label(rightFrame, text="PH")
ph = ttk.Entry(rightFrame)

#EFFICACY
efficacyLbl = ttk.Label(rightFrame, text="Efficacy*")
efficacy = ttk.Entry(rightFrame)

efficacyComment=ttk.Label(rightFrame, text="*leave efficacy & id blank for model prediction")

idLbl= ttk.Label(rightFrame,text="Id*")
eid=ttk.Entry(rightFrame)

for child in rightFrame.winfo_children():
    child.grid_configure(padx=10, pady=10)

#more user actions:
predict = ttk.Button(content, text="Predict",width=20,command=prediction)
addDB = ttk.Button(content, text="Add Data",width=20,command=addDataPt)

#clear data:
clearbtn = ttk.Button(content,text="Clear",width = 20, command=clear )

#CONTENT GRIDE ALIGNMENTS
content.grid(column=0,row=0)
#left
activeLbl.grid(column=0,row=0,columnspan=1)
clearbtn.grid(column=1,row=0,columnspan=1)
leftFrame.grid(sticky="W",column=0,row=1, columnspan=3,rowspan=5)
addName.grid(sticky="W",column=0,row=6)
addValue.grid(column=1,row=6)
addActive.grid(sticky="E",column=2,row=6)
#right
other.grid(column=3,row=0,columnspan=3)
rightFrame.grid(sticky="N",column=3,row=1,columnspan=3,rowspan=5)

#within the right frame
dilutionLbl.grid(sticky="W",column=3,row=1)
dilution.grid(column=4,row=1,columnspan=2)

dirtyLbl.grid(sticky="W",column=3,row=2)

hardnessLbl.grid(sticky="W",column=3,row=3)

pHLbl.grid(sticky="W",column=3,row=4)
ph.grid(column=4,row=4,columnspan=2)

efficacyLbl.grid(sticky="W",column=3,row=5)
efficacy.grid(column=4,row=5,columnspan=2)

idLbl.grid(sticky="W",column=3,row=6)
eid.grid(column=4,row=6,columnspan=2)

efficacyComment.grid(sticky="W",column=3,row=7,columnspan=3)

#last 2 buttons
predict.grid(column=3,row=6)
addDB.grid(column=4,row=6)


root.mainloop()
