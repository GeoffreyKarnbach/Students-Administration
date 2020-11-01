#coding :utf-8
import sqlite3
from tkinter import*
from tkinter.messagebox import*
import webbrowser
import math
import pyperclip
from tkinter import filedialog




def create_DB():
    cursor.execute("CREATE TABLE etudiants(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,nom TEXT,prenom TEXT,email TEXT)")
    connection.commit()
    return True

def affiche_tout():
    cursor.execute("SELECT * FROM etudiants")
    return cursor.fetchall()

def insertion_nom(data):
    cursor.execute("INSERT INTO etudiants(nom,prenom,email) VALUES(?,?,?)",data)
    connection.commit()
    return True

def suppression_nom(id):
    cursor.execute('DELETE FROM etudiants WHERE id = ?',(id,))
    connection.commit()
    return True


def modification(info):
    cursor.execute("UPDATE etudiants SET (nom, prenom,email) = (?,?,?) WHERE id = ?",info)
    connection.commit()
    return True

def search_by_char(CHAR):
    texte="%"+CHAR+"%"
    cursor.execute("SELECT * FROM etudiants WHERE nom LIKE ? OR prenom LIKE ? OR email LIKE ?",(texte,texte,texte))
    res=cursor.fetchall()
    liste=[]
    for loop in res:
        liste.append(loop[0])
    SHOW_SOME(liste)
    connection.commit()

def close_connection():
    cursor.close()
    connection.close()
    return True

def ADD():
    fen.title("ADD NEW")
    def check():
        infos=(x1.get(),x2.get(),x3.get())
        possible=True
        for loop in infos:
            if loop == "":
                possible=False
        if possible:
            insertion_nom(infos)
        else:
            showerror("ERROR","All fields must be different from null.")
        SHOW_ALL()

    for widget in frame.winfo_children():
        widget.destroy()

    x1,x2,x3=StringVar(),StringVar(),StringVar()

    Label(frame,text="NOM: ").grid(column=0,row=0,sticky=W,padx=10,pady=10)
    Entry(frame,textvariable=x1,width=30).grid(column=1,row=0,padx=10)

    Label(frame,text="PRENOM: ").grid(column=0,row=1,sticky=W,padx=10,pady=10)
    Entry(frame,textvariable=x2,width=30).grid(column=1,row=1,padx=10)

    Label(frame,text="Email: ").grid(column=0,row=4,sticky=W,padx=10,pady=10)
    Entry(frame,textvariable=x3,width=30).grid(column=1,row=4,padx=10)

    Button(frame,text="CONFIRM",command=check,width=30,height=2,bg="green").grid(column=0,row=8,columnspan=2,pady=10)

def DELETE(ID):
    for widget in frame.winfo_children():
        widget.destroy()
    suppression_nom(ID)
    SHOW_ALL()

def MODIFY(ID):
    fen.title("MODIFY DATA")
    def check():
        infos=(x1.get(),x2.get(),x3.get())
        possible=True
        for loop in infos:
            if loop == "":
                possible=False
        if possible:
            infos=(x1.get(),x2.get(),x3.get(),ID)
            modification(infos)
        else:
            showerror("ERROR","All fields must be different from null.")

        SHOW(ID)

    for widget in frame.winfo_children():
        widget.destroy()

    infos=affiche_tout()
    x1,x2,x3=StringVar(),StringVar(),StringVar()

    for loop in infos:
        if loop[0]==ID:


            Label(frame,text="NOM: ").grid(column=0,row=0,sticky=W,padx=10,pady=10)
            e1=Entry(frame,textvariable=x1,width=30)
            e1.insert(0,loop[1])
            e1.grid(column=1,row=0,padx=10)

            Label(frame,text="PRENOM: ").grid(column=0,row=1,sticky=W,padx=10,pady=10)
            e2=Entry(frame,textvariable=x2,width=30)
            e2.insert(0,loop[2])
            e2.grid(column=1,row=1,padx=10)


            Label(frame,text="Email: ").grid(column=0,row=4,sticky=W,padx=10,pady=10)
            e5=Entry(frame,textvariable=x3,width=30)
            e5.insert(0,loop[3])
            e5.grid(column=1,row=4,padx=10)


            Button(frame,text="CONFIRM",command=check,width=30,height=2,bg="green").grid(column=0,row=8,columnspan=2,pady=10)

def SHOW_ALL():
    fen.title("SHOW ALL")
    for widget in frame.winfo_children():
        widget.destroy()
    infos=affiche_tout()
    if len(infos)==0:
        Label(frame,text="Pas d'etudiants dans la liste",width=30,height=2).grid()
    for loop in range(len(infos)//8+1):
        for lopp in range(8):
            try:
                Button(frame,text=infos[loop*8+lopp][2]+" "+infos[loop*8+lopp][1],height=2,width=30,command=lambda x=infos[loop*8+lopp][0] :SHOW(x)).grid(column=lopp,row=loop,padx=10,pady=10)
            except:
                pass

def SHOW_SOME(IDS):
    fen.title("SHOW SEARCH RESULTS")
    for widget in frame.winfo_children():
        widget.destroy()
    infos=affiche_tout()
    for loop in range(len(infos)):
        if infos[loop][0] in IDS:
            Button(frame,text=infos[loop][2]+" "+infos[loop][1],height=2,width=30,command=lambda x=infos[loop][0] :SHOW(x)).grid(column=0,row=loop,padx=10,pady=10)

def SHOW(ID):
    fen.title("SHOW PROFILE OF")
    for widget in frame.winfo_children():
        widget.destroy()

    infos=affiche_tout()
    for loop in infos:
        if loop[0]==ID:
            Label(frame,text="NOM: "+loop[1]).grid(column=0,row=0,padx=10,pady=10,sticky=W,columnspan=2)

            Label(frame,text="PRENOM: "+loop[2]).grid(column=0,row=1,padx=10,pady=10,sticky=W,columnspan=2)


            Button(frame,text="Email: "+loop[3],command= lambda x = loop[3]: pyperclip.copy(x), relief=FLAT).grid(column=0,row=4,padx=10,pady=10,sticky=W,columnspan=2)

            Button(frame,text="DELETE", width=15,height=2,bg="red",command= lambda x = loop[0] : DELETE(x)).grid(column=0,row=8,padx=5,pady=5)
            Button(frame,text="MODIFIER", width=15,height=2,bg="yellow",command= lambda x = loop[0] : MODIFY(x)).grid(column=1,row=8,padx=5,pady=5)

            break

def SEARCH():
    fen.title("SEARCH")
    def check():
        infos=x1.get()
        if infos != "":
            search_by_char(infos)
        else:
            showerror("ERROR","Can't search for empty string")

    for widget in frame.winfo_children():
        widget.destroy()

    x1=StringVar()
    Label(frame,text="Search: ").grid(column=0,row=0,padx=10,pady=10)
    Entry(frame,textvariable=x1,width=30).grid(column=1,row=0,padx=10,pady=10)
    Button(frame,text="CONFIRM",command=check,bg="green",width=35,height=2).grid(column=0,row=1,columnspan=2,padx=10,pady=10)


def ABOUT():
    fen.title("ABOUT")
    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame,text="(c) Geoffrey Karnbach 2020").grid()

root = Tk()
root.withdraw()

DB_NAME=filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Data Base","*.db"),("all files","*.*")))
connection=sqlite3.connect(DB_NAME)
cursor=connection.cursor()

root.destroy()


fen=Tk()
fen.title("Repertoire")

menubar = Menu(fen)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Ajouter",command=ADD)
menu1.add_separator()
menu1.add_command(label="Afficher",command=SHOW_ALL)
menu1.add_command(label="Rechercher",command=SEARCH)
menubar.add_cascade(label="Contacts", menu=menu1)

menu3 = Menu(menubar, tearoff=0)
menu3.add_command(label="A propos",command=ABOUT)
menu3.add_command(label="Quitter",command=fen.destroy)
menubar.add_cascade(label="Aide", menu=menu3)

fen.config(menu=menubar)

frame=Frame(fen)
frame.grid()

SHOW_ALL()

fen.mainloop()
close_connection()
