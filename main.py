from tkinter import *
import os
import pandas as pd
import csv
from tkinter import messagebox

def getRow(uoa,uniqueName): # uoa - user or admin
    if uoa == 1:
        with open('Customers.csv') as o:
            myData = csv.reader(o) 
            index = 0 
            for row in myData:
                if row[0] == uniqueName: 
                    # res.set(index)
                    return index 
                else : index+=1
    else:
        with open('managers.csv') as o:
            myData = csv.reader(o) 
            index = 0 
            for row in myData:
                if row[0] == uniqueName: 
                    return index 
                else : index+=1
    return -1

class Frames(object):
    def __init__(self) -> None:
        pass
    def Signup(self,root):
        root.title("Signup Page")
        root.geometry('500x250')
        self.username=StringVar()
        self.password=StringVar()
        self.var = IntVar()
        Radiobutton(root, text="User", variable=self.var, value=1).pack()
        Radiobutton(root, text="Manager", variable=self.var, value=2).pack()
        Label(root,text="Enter Name").pack()
        Entry(root,textvariable=self.username).pack()
        Label(root,text="Enter Password").pack()
        Entry(root,textvariable=self.password).pack()
        Button(root,text="Register",command=self.SignupWork).pack()
        Button(root,text="Login",command=self.Login).pack()
    
    def SignupWork(self):
        if self.var.get()==1:
            if not os.path.exists("./customers.csv"):
                cdf = pd.DataFrame(columns=["Username","Password"])
                cdf.to_csv("Customers.csv")
            data = {'Username' : [self.username.get()],'Password' : [self.password.get()]}
            df = pd.DataFrame(data)
            df.to_csv('Customers.csv',mode='a', index=False, header=False)
        else:
            if not os.path.exists("./managers.csv"):
                cdf = pd.DataFrame(columns=["managerName","Password"])
                cdf.to_csv("managers.csv")
            data = {'Username' : [self.username.get()],'Password' : [self.password.get()]}
            df = pd.DataFrame(data)
            df.to_csv('managers.csv',mode='a', index=False, header=False)
        self.Login()

    def Login(self):
        tl = Toplevel()
        tl.geometry('500x250')
        tl.title("Login page")
        self.loginUser = StringVar()
        self.loginPassword = StringVar()
        var = IntVar()
        Radiobutton(tl, text="User", variable=var, value=1).pack()
        Radiobutton(tl, text="Manager", variable=var, value=2).pack()
        Label(tl,text="Username").pack()
        Entry(tl,textvariable=self.loginUser).pack()
        Label(tl,text="Password").pack()
        Entry(tl,textvariable=self.loginPassword).pack()
        Button(tl,text="Login",command=lambda : self.loginWorker(var.get(),self.loginUser.get(),self.loginPassword.get())).pack()
    
    def loginWorker(self,uoa,uname,password):
        global id
        id = IntVar()
        if uoa == 1:
            filename = 'Customers.csv'
        else:
            filename = 'managers.csv'
        with open(filename) as o:
            myData = csv.reader(o)
            index = 0
            for row in myData:
                if row[0] == uname:
                    if row[1] == password:
                        id.set(index)
                        messagebox.showinfo("Message","Welcome ")
                        if uoa == 1:
                            self.WelcomeUser()
                        else:
                            self.WelcomeManager()
                        return index
                index +=1
        messagebox.showinfo("Message","Invalid login credentials")
        
    
    def WelcomeUser(self):
        result = Toplevel()
        result.geometry('500x250')
        result.title("Welcome page")
        col_names = ("Area","Cost","Address")
        for i, col_name in enumerate(col_names, start=1):
            Label(result, text=col_name).grid(row=0, column=i, padx=40)
        with open("RealEstates.csv", "r") as passfile:
            reader = csv.reader(passfile)
            data = list(reader)
        entrieslist = []
        for i, row in enumerate(data,start=0):
            if i!=0:
                entrieslist.append(row[0])
                for col in range(0, 4):
                    Label(result, text=row[col]).grid(row=i, column=col)
                Button(result,text=i,command= lambda row=row: self.Addprop(row)).grid(row=i, column=len(col_names)+1)

    def Addprop(self,i):
        # Mid,Area,Cost,Address
        mid = int(i[0])
        area = i[1]
        cost = i[2]
        address = i[3]
        user = self.loginUser.get()
        # mid area cost address propertryID uid
        if not os.path.exists("./PersonalProperty.csv"):
            cdf = pd.DataFrame(columns=["mid","username","area","cost","address"])
            cdf.to_csv("PersonalProperty.csv")
        data = {'mid':[mid],'username' : [user],'area':[area],'cost':[cost],'address':[address]}
        df = pd.DataFrame(data)
        df.to_csv('PersonalProperty.csv',mode='a', index=False, header=False)

        # removing row from realestates.csv
        with open('RealEstates.csv', 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
        ind = self.verify_get('RealEstates.csv',i)
        rows.pop(int(ind))

        print("hello from below rows")
        with open("RealEstates.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
    
    def verify_get(self,filename,row_detail):
        with open(filename) as file_obj:
            reader_obj = csv.reader(file_obj)
            for i,row in enumerate(reader_obj):
                if row == row_detail:
                    return i

    def WelcomeManager(self):
        global area,cost,address
        tl = Toplevel(root)
        tl.geometry('500x250')
        tl.title("Manager Page")

        area = StringVar()
        cost = StringVar()
        address = StringVar()

        Label(tl,text="Enter area").pack()
        Entry(tl,textvariable=area).pack()

        Label(tl,text="Enter Cost in USD").pack()
        Entry(tl,textvariable=cost).pack()

        Label(tl,text="Enter Address").pack()
        Entry(tl,textvariable=address).pack()

        Button(tl,text="Add",command= lambda: self.Add(self.loginUser.get(),area.get(),cost.get(),address.get(),2)).pack()
        
    def Add(self,username,area,cost,address,uoa):
        if not os.path.exists("./RealEstates.csv"):
            cdf = pd.DataFrame(columns=["Mid","Area","Cost","Address"])
            cdf.to_csv("RealEstates.csv")
        data = {'Mid':[getRow(uoa,username)],'Area' : [area],'Cost' : [cost],'Address':[address]}
        df = pd.DataFrame(data)
        df.to_csv('RealEstates.csv',mode='a', index=False, header=False)

root = Tk()
app = Frames()
app.Signup(root)
root.mainloop()