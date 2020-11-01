from tkinter import*
import sqlite3
import datetime
import statistics
from itertools import groupby
import matplotlib.pyplot as plt
import numpy as np
import math
from tkinter import filedialog
from tkinter import font


##################### TKINTER ####################


root=Tk()
root.withdraw()

DB_NAME=filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Data Base","*.db"),("all files","*.*")))

root.destroy()

fen=Tk()
fen.title("Gestion de resultat d'etudiants")
fen.geometry("900x900")

frame=Frame()
frame.grid()

################### ETUDIANTS #################

connection=sqlite3.connect(DB_NAME)
cursor=connection.cursor()
cursor.execute("SELECT * FROM etudiants")
etudiants=cursor.fetchall()

############ GUI FUNCTIONS ##############

def releve_de_notes():

    def index_2d(myList, v):
        for i, x in enumerate(myList):
            if v in x:
                return (i, x.index(v))

    cursor.execute("SELECT * FROM devoirs")
    devoirs=cursor.fetchall()

    def NEW_DEVOIR():

        def get_values():
            cursor.execute("INSERT INTO devoirs (name,blocID,note) VALUES(?,?,?)",(x1.get(),x3.get(),x2.get()))
            connection.commit()
            fen2.destroy()
            releve_de_notes()

        fen2=Toplevel()
        fen2.title("Nouveau devoir")
        x1,x2,x3=StringVar(),StringVar(),StringVar()

        Label(fen2,text="Nom du devoir").grid(column=0,row=0,padx=10,pady=10)
        Entry(fen2,textvariable=x1,width=30).grid(column=1,row=0,padx=10,pady=10)

        Label(fen2,text="Nombre de point max").grid(column=0,row=1,padx=10,pady=10)
        Entry(fen2,textvariable=x2,width=30).grid(column=1,row=1,padx=10,pady=10)

        Label(fen2,text="Bloc numero ").grid(column=0,row=2,padx=10,pady=10)
        Entry(fen2,textvariable=x3,width=30).grid(column=1,row=2,padx=10,pady=10)

        Button(fen2,text="VALIDER",width=30,bg="green",command=get_values).grid(column=0,row=3,columnspan=2,padx=10,pady=10)

    def CHANGE_DEVOIR():

        def del_devoir(x):
            cursor.execute("DELETE FROM devoirs WHERE ID = ?",(x,))
            connection.commit()
            fen2.destroy()
            releve_de_notes()

        fen2=Toplevel()
        fen2.title("Nouveau devoir")
        for loop in range(len(devoirs)):
            Button(fen2,text=devoirs[loop][1],command= lambda x= devoirs[loop][0]: del_devoir(x)).grid(column=0,row=loop)


    def valider():
        for loop in range(len(notes)):
            for lopp in range(len(notes[loop])):
                cursor.execute("SELECT * FROM notes WHERE studentID= ? AND testID = ?",(etudiants[loop][0],devoirs[lopp][0]))
                elem=cursor.fetchall()
                if len(elem)==0:
                    cursor.execute("INSERT INTO notes (studentID,note,testID) VALUES(?,?,?)",(etudiants[loop][0],notes[loop][lopp].get(),devoirs[lopp][0]))
                    connection.commit()
                else:
                    cursor.execute("UPDATE notes SET note = ? WHERE studentID= ? AND testID = ?",(notes[loop][lopp].get(),etudiants[loop][0],devoirs[lopp][0]))
                    connection.commit()

    def INFO_DEVOIR():
        def show_devoir(x):
            for widget in fen2.winfo_children():
                widget.destroy()
            Label(fen2,text="Nom du devoir: "+str(devoirs[x][1])).grid(column=0,row=0,padx=10,pady=10)
            Label(fen2,text="Numero de bloc du devoir: "+str(devoirs[x][2])).grid(column=0,row=1,padx=10,pady=10)
            Label(fen2,text="Note maximale du devoir: "+str(devoirs[x][3])).grid(column=0,row=2,padx=10,pady=10)

        fen2=Toplevel()
        fen2.title("Nouveau devoir")
        for loop in range(len(devoirs)):
            Button(fen2,text=devoirs[loop][1],command= lambda x= loop: show_devoir(x)).grid(column=0,row=loop,padx=10,pady=10)

    def stats(x):
        fen2=Toplevel()
        fen2.title("Statistiques du controle "+str(devoirs[x][1]))
        fen2.geometry("500x500")

        devoirs

        cursor.execute("SELECT * FROM notes WHERE testID = ?",(devoirs[x][0],))
        resultats=cursor.fetchall()
        resultat=[]
        for loop in resultats:
            resultat.append(loop[2])
        resultat.sort()

        Label(fen2,text="Etendue: "+str(round((resultat[-1]-resultat[0])*20/devoirs[x][3],2))).grid(column=0,row=0,padx=10,pady=10)
        Label(fen2,text="Moyenne: "+str(round(sum(resultat)/len(resultat)*20/devoirs[x][3],2))).grid(column=0,row=1,padx=10,pady=10)
        Label(fen2,text="Minimum: "+str(round(min(resultat)*20/devoirs[x][3],2))).grid(column=0,row=2,padx=10,pady=10)
        Label(fen2,text="Quartile 1: "+str(round(statistics.quantiles(resultat)[0]*20/devoirs[x][3],2))).grid(column=0,row=3,padx=10,pady=10)
        Label(fen2,text="Mediane: "+str(round(statistics.median(resultat)*20/devoirs[x][3],2))).grid(column=0,row=4,padx=10,pady=10)
        Label(fen2,text="Quartile 3: "+str(round(statistics.quantiles(resultat)[2]*20/devoirs[x][3],2))).grid(column=0,row=5,padx=10,pady=10)
        Label(fen2,text="Maximum: "+str(round(max(resultat)*20/devoirs[x][3],2))).grid(column=0,row=6,padx=10,pady=10)

        freq = {k:0 for k in range(21)}
        for item in resultat:
            freq[round(item*20/devoirs[x][3])] = freq.get(round(item*20/devoirs[x][3]), 0) + 1

        fig, ax = plt.subplots()
        candidats = list(freq.keys())
        voter = list(freq.values())
        y_pos = np.arange(len(candidats))
        plt.title('Resultat de '+devoirs[x][1])
        plt.ylabel("Frequence")
        plt.xlabel('Note sur 20')
        plt.bar(y_pos, voter, align='center')
        ax.set_xticks(range(len(candidats)))
        ax.set_xticklabels(candidats, rotation='vertical')
        plt.show()

    for widget in frame.winfo_children():
        widget.destroy()


    notes=[[StringVar() for lopp in range(len(devoirs))] for loop in range(len(etudiants))]
    cursor.execute("SELECT * FROM notes")
    noteS=cursor.fetchall()

    for loop in range(len(noteS)):
        try:
            notes[index_2d(etudiants,noteS[loop][1])[0]][index_2d(devoirs,noteS[loop][3])[0]].set(noteS[loop][2])
        except:
            pass

    Label(frame,text="NOM ETUDIANTS").grid(column=0,row=0)

    for loop in range(len(devoirs)):
        Button(frame,text=devoirs[loop][1],relief = FLAT,command = lambda x= loop: stats(x)).grid(column=1+loop,row=0)

    for loop in range(len(etudiants)):
        Button(frame,text=etudiants[loop][1]+" "+etudiants[loop][2],command = lambda x= etudiants[loop][0]: profile(x),relief = FLAT).grid(column=0,row=1+loop,padx=10,pady=10)
        COLUMN_ID=0
        for lopp in range(len(devoirs)):
            Entry(frame,width=15,textvariable=notes[loop][lopp]).grid(column=1+COLUMN_ID,row=1+loop,padx=5,pady=10)
            COLUMN_ID+=1
    frame2=Frame(frame,bg="grey50")
    frame2.grid(column=0,row=2+len(etudiants),padx=10,pady=10,columnspan=4)
    Button(frame,text="VALIDER LES ENTREES",bg="green",command=valider).grid(column=0,row=1+len(etudiants),padx=10,pady=10)
    Button(frame2,text="Nouveau Devoir",command = NEW_DEVOIR).grid(column=0,row=0,padx=15,pady=10)
    Button(frame2,text="Effacer Devoirs",command = CHANGE_DEVOIR).grid(column=1,row=0,padx=20,pady=10)
    Button(frame2,text="Informations Devoirs",command = INFO_DEVOIR).grid(column=2,row=0,padx=20,pady=10)
    Button(frame2,text="Statistiques du groupe",command=statistiques_groupe).grid(column=3,row=0,padx=15,pady=10)

def profile(ID):

    def index_2d(myList, v):
        for i, x in enumerate(myList):
            if v in x:
                return (i, x.index(v))


    for widget in frame.winfo_children():
        widget.destroy()

    cursor.execute("SELECT * FROM notes")
    resultats=cursor.fetchall()

    cursor.execute("SELECT * FROM devoirs")
    controles=cursor.fetchall()

    cursor.execute("SELECT * FROM etudiants WHERE id = ?",(ID,))
    info=cursor.fetchall()

    cursor.execute("SELECT * FROM bonus")
    bonuS=cursor.fetchall()


    Label(frame,text=info[0][2]+" "+info[0][1],font=(12),fg="red").grid(column=0,row=0,padx=25,pady=10)

    blocs=[]
    noteTotale=0
    nombreDeDevoir=0
    nombreDePointMax=0
    for loop in range(len(resultats)):
        for lopp in range(len(controles)):
            if resultats[loop][1] == info[0][0] and resultats[loop][3] == controles[lopp][0]:
                noteTotale+=float(resultats[loop][2])
                nombreDeDevoir+=1
                inside=False
                nombreDePointMax+=controles[lopp][3]
                for lop in blocs:
                    if controles[lopp][2] == lop[1]:
                        inside=True
                        lop[0]+=resultats[loop][2]
                        lop[2]+=controles[lopp][3]


                if not inside:
                    blocs.append([resultats[loop][2],controles[lopp][2],controles[lopp][3]])
                break

    Label(frame,text="Nombre de point total: "+str(round(noteTotale,3))).grid(column=0,row=1,padx=10,pady=10,sticky=NW)
    Label(frame,text="Nombre de points max possible: "+str(nombreDePointMax)).grid(column=0,row=2,padx=10,pady=10,sticky=NW)
    Label(frame,text="Nombre de devoirs: "+str(nombreDeDevoir)).grid(column=0,row=3,padx=10,pady=10,sticky=NW)


    note_par_bloc=[]
    negative=-1

    for loop in range(len(blocs)):
        Label(frame,text="Nombre de points sur le bloc "+str(blocs[loop][1])+" : "+str(blocs[loop][0])).grid(column=0,row=4+loop,padx=20,pady=10,sticky=NW)
        Label(frame,text="Nombre de points maximal sur le bloc "+str(blocs[loop][1])+" : "+str(blocs[loop][2])).grid(column=1,row=4+loop,padx=20,pady=10,sticky=NW)
        note_par_bloc.append(round(blocs[loop][0]/blocs[loop][2],3)*20)
        Label(frame,text="Nombre de points sur 20 dans le bloc "+str(blocs[loop][1])+" atteint : "+str(note_par_bloc[-1])).grid(column=2,row=4+loop,padx=20,pady=10,sticky=NW)

    passage=True
    for loop in range(len(note_par_bloc)):
        if note_par_bloc[loop]<10:
            passage=False
            negative=loop

    bonusVALUE=float(bonuS[index_2d(bonuS,ID)[0]][1])

    Label(frame,text="Bonus: "+str(bonusVALUE)).grid(column=0,row=5+len(blocs),padx=10,pady=10,sticky=NW)

    moyenne=round((noteTotale+bonusVALUE)/nombreDePointMax*20,3)

    Label(frame,text="Moyenne sur 20: "+str(moyenne),fg="red",font=(12)).grid(column=0,row=6+len(blocs),padx=10,pady=10,sticky=NW)
    if passage:
        cursor.execute("SELECT * FROM conversion")
        valeur=cursor.fetchall()
        Label(frame,text="PASSAGE TOUS LES BLOCS SONT POSITIFS.").grid(column=0,row=7+len(blocs),padx=20,pady=10,sticky=NW)
        noteALL=" "
        for loop in valeur:
            if math.floor(moyenne)>=loop[1] and math.floor(moyenne)<=loop[2]:
                noteALL=loop[0]
                break

        Label(frame,text="LA NOTE DANS LE SYSTEME AUTRICHIEN D'APRES LES LIMITES EST: "+noteALL).grid(column=0,row=8+len(blocs),padx=20,pady=10,sticky=NW,columnspan=2)
    else:
        Label(frame,text="NON PASSAGE, CAR LE BLOC "+str(blocs[negative][1])+" EST NEGATIF.").grid(column=0,row=7+len(blocs),padx=20,pady=10,sticky=NW)
        Label(frame,text="LA NOTE DANS LE SYSTEME AUTRICHIEN D'APRES LES LIMITES EST: Nicht genugend").grid(column=0,row=8+len(blocs),padx=20,pady=10,sticky=NW,columnspan=2)

def bonus():

    def index_2d(myList, v):
        for i, x in enumerate(myList):
            if v in x:
                return (i, x.index(v))

    def valider():
        for loop in valeurBonus:
            cursor.execute("SELECT * FROM bonus WHERE studentID= ?",(loop[0],))
            elem=cursor.fetchall()

            if len(elem)==0:
                cursor.execute("INSERT INTO bonus (studentID,val) VALUES(?,?)",(loop[0],float(loop[1].get())))
                connection.commit()
            else:
                cursor.execute("UPDATE bonus SET val = ? WHERE studentID= ?",(float(loop[1].get()),loop[0]))
                connection.commit()

    cursor.execute("SELECT * FROM bonus")
    bonuS=cursor.fetchall()

    valeurBonus=[[etudiants[loop][0],StringVar()] for loop in range(len(etudiants))]

    for loop in range(len(valeurBonus)):
        try:
            valeurBonus[loop][1].set(bonuS[index_2d(etudiants,bonuS[loop][0])[0]][1])
        except:
            pass

    for widget in frame.winfo_children():
        widget.destroy()

    Label(frame,text="Bonus",font="Verdana 15 underline").grid(column=0,row=0,padx=50,pady=10,columnspan=3)
    for loop in range(len(etudiants)):
        Label(frame,text=etudiants[loop][1]+" "+etudiants[loop][2]).grid(column=0,row=1+loop,pady=10,sticky=W,padx=10)
        Entry(frame,width=10,textvariable=valeurBonus[loop][1]).grid(column=1,row=1+loop,pady=10,sticky=W,padx=10)

    Button(frame,text="VALIDER LES ENTREES",bg="green",command=valider).grid(column=0,row=1+len(etudiants),padx=10,pady=10,columnspan=2)


def participations():
    cursor.execute("SELECT * FROM participation")
    absences=cursor.fetchall()
    for widget in frame.winfo_children():
        widget.destroy()
    def add_absence(x):
        cursor.execute("INSERT INTO participation(studentID,date) VALUES (?,?)",(x,datetime.datetime.now().strftime("%d/%m/%Y")))
        connection.commit()
        participations()
    def delete_abs(x):
        cursor.execute("DELETE FROM participation WHERE ID = ?",(x,))
        connection.commit()
        participations()

    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame,text="Participation",font="Verdana 15 underline").grid(column=0,row=0,padx=50,pady=10,columnspan=3)
    for loop in range(len(etudiants)):
        Label(frame,text=etudiants[loop][1]+" "+etudiants[loop][2]).grid(column=0,row=1+loop,pady=10,sticky=W,padx=10)
        Button(frame,bg="green",text="+",command= lambda x=etudiants[loop][0]: add_absence(x)).grid(column=1,row=1+loop)
        nbABS=0
        for lopp in range(len(absences)):
            if absences[lopp][1]==etudiants[loop][0]:
                nbABS+=1
                Button(frame,text=absences[lopp][2],command= lambda x=absences[lopp][0]: delete_abs(x)).grid(column=2+nbABS,row=1+loop)

def absence():
    cursor.execute("SELECT * FROM absences")
    absences=cursor.fetchall()
    def add_absence(x):
        cursor.execute("INSERT INTO absences(studentID,date) VALUES (?,?)",(x,datetime.datetime.now().strftime("%d/%m/%Y")))
        connection.commit()
        absence()
    def delete_abs(x):
        cursor.execute("DELETE FROM absences WHERE ID = ?",(x,))
        connection.commit()
        absence()

    for widget in frame.winfo_children():
        widget.destroy()
    Label(frame,text="Absences",font="Verdana 15 underline").grid(column=0,row=0,padx=50,pady=10,columnspan=3)
    for loop in range(len(etudiants)):
        Label(frame,text=etudiants[loop][1]+" "+etudiants[loop][2]).grid(column=0,row=1+loop,pady=10,sticky=W,padx=10)
        Button(frame,bg="green",text="+",command= lambda x=etudiants[loop][0]: add_absence(x)).grid(column=1,row=1+loop)
        nbABS=0
        for lopp in range(len(absences)):
            if absences[lopp][0]==etudiants[loop][0]:
                nbABS+=1
                Button(frame,text=absences[lopp][1],command= lambda x=absences[lopp][2]: delete_abs(x)).grid(column=2+nbABS,row=1+loop)

def statistiques_groupe():
    for widget in frame.winfo_children():
        widget.destroy()

def parametres():

    def valider_note():

        liste=(x1.get(),x2.get(),x3.get(),x4.get(),x5.get(),x6.get(),x7.get(),x8.get(),x9.get(),x10.get())

        for loop in range(5):
            cursor.execute("UPDATE conversion SET MIN = ? , MAX = ? WHERE ID = ?",(liste[loop*2],liste[loop*2+1],loop))
        connection.commit()
        parametres()
        # ADD TO DATABASE

    for widget in frame.winfo_children():
        widget.destroy()

    cursor.execute("SELECT MIN , MAX FROM conversion")
    valeur=cursor.fetchall()

    x1,x2,x3,x4,x5,x6,x7,x8,x9,x10=StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar()

    x1.set(valeur[0][0])
    x2.set(valeur[0][1])
    x3.set(valeur[1][0])
    x4.set(valeur[1][1])
    x5.set(valeur[2][0])
    x6.set(valeur[2][1])
    x7.set(valeur[3][0])
    x8.set(valeur[3][1])
    x9.set(valeur[4][0])
    x10.set(valeur[4][1])


    Label(frame,text="Note").grid(column=0,row=0,padx=10,pady=10)
    Label(frame,text="Minimum").grid(column=1,row=0,padx=10,pady=10)
    Label(frame,text="Maximum").grid(column=2,row=0,padx=10,pady=10)

    Label(frame,text="Nicht genugend: ").grid(column=0,row=1,padx=10,pady=10)
    Entry(frame,textvariable=x1,width=5).grid(column=1,row=1,padx=10,pady=10)
    Entry(frame,textvariable=x2,width=5).grid(column=2,row=1,padx=10,pady=10)

    Label(frame,text="Genugend: ").grid(column=0,row=2,padx=10,pady=10)
    Entry(frame,textvariable=x3,width=5).grid(column=1,row=2,padx=10,pady=10)
    Entry(frame,textvariable=x4,width=5).grid(column=2,row=2,padx=10,pady=10)

    Label(frame,text="Befriedigend: ").grid(column=0,row=3,padx=10,pady=10)
    Entry(frame,textvariable=x5,width=5).grid(column=1,row=3,padx=10,pady=10)
    Entry(frame,textvariable=x6,width=5).grid(column=2,row=3,padx=10,pady=10)

    Label(frame,text="Gut: ").grid(column=0,row=4,padx=10,pady=10)
    Entry(frame,textvariable=x7,width=5).grid(column=1,row=4,padx=10,pady=10)
    Entry(frame,textvariable=x8,width=5).grid(column=2,row=4,padx=10,pady=10)

    Label(frame,text="Sehr Gut: ").grid(column=0,row=5,padx=10,pady=10)
    Entry(frame,textvariable=x9,width=5).grid(column=1,row=5,padx=10,pady=10)
    Entry(frame,textvariable=x10,width=5).grid(column=2,row=5,padx=10,pady=10)

    Button(frame,text="VALIDER",command=valider_note,bg="green",width=40).grid(column=0,row=6,padx=10,pady=10,columnspan=3)

######### MENU BAR ###################

menubar = Menu(fen)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Releve de notes",command=releve_de_notes)
menu1.add_command(label="Participation",command=participations)
menu1.add_command(label="Bonus",command=bonus)
menubar.add_cascade(label="Evaluation", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Absence",command=absence)
menubar.add_cascade(label="Administratif", menu=menu2)

menu3 = Menu(menubar, tearoff=0)
menu3.add_command(label="Settings",command=parametres)
menubar.add_cascade(label="Parametres", menu=menu3)

fen.config(menu=menubar)

############ MAINLOOP ###################

releve_de_notes()

fen.mainloop()
connection.close()

######