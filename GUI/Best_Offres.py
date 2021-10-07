
import webbrowser
from tkinter import *

from PIL import ImageTk

from SGCA import AliExpressScraper


def callback(ind):
    # Cette fonction permet de forcer l'utilisation des paramètre utiliser la création des widgets
    webbrowser.open_new(ind)

def display_details(text):
    """
        Cette fonction permet d'afficher les détails d'un produit sur une nouvelle interface graphique

        :param text: le text généré par la fonction DataProcessing.get_text()

    """
    master = Tk()
    master.title("Product Details")
    scroll = Scrollbar(master)
    scroll.pack(side=RIGHT, fill=Y)

    eula = Text(master, wrap=NONE, yscrollcommand=scroll.set,font='Lucida 11',width=100,height=500)
    eula.insert("1.0", text)
    eula.pack(side="left")

    scroll.config(command=eula.yview)
    master.mainloop()


def Get_product(Df,Values,driver):
    """
        Cette fonction permet de créer un interface graphique pour l'affichage des suggestions de produits à l'utilisateur.

        :param Df: Dataframe des produits classés par ordre de pertinences selon les critères de l'utilisateur.
        :param Values: les valeurs entrées par l'utilisateur.
        :param driver: le driver utilisé pour le scraping et qui permettra de scrapper plus de détails sur les produits.

        :return: Renvoie une Data Frame trier par ordre de pertinences selon les besoins de l'utilisateur, et aussi le temps d'exécution de la requête.


    """
    sgca = Tk()
    sgca.title("SGCA")
    sgca.configure(bg='#ffffff')
    img = ImageTk.PhotoImage(master = sgca, file="./Data/Scrapper.png")
    canvas = Canvas(sgca, width=400,height=300,
                    borderwidth=0,
                    highlightthickness=0,
                    background='white')
    canvas.configure(bg='#ffffff')
    canvas.create_image(200,150, anchor=CENTER, image=img)
    canvas.pack()
    try:
        max=int(Values["Max_price"])+int(Values["Max_price"])*0.2
        indexmax = Df[Df['Prix'] > max ].index
        Df.drop(indexmax, inplace=True)
    except:
        pass
    try:
        min=int(Values["Min_price"])-int(Values["Min_price"])*0.2
        indexmin = Df[Df['Prix'] < min ].index
        Df.drop(indexmin, inplace=True)
    except:
        pass
    try:
        Df = Df.head(int(Values["Max_Items"]))
    except:
        Df = Df.head(5)
    L=[]
    ind=Df.index
    Mores=[]
    eval_link = lambda x: (lambda p: callback(x))
    get_detail = lambda x: (lambda p: AliExpressScraper.get_details(x,driver))
    for i in range(len(Df.index)):
        L=L+[Label(sgca, text=ind[i][:ind[i].find('.html')+5], fg="blue", cursor="hand2", font="Times 14 ",bg='#ffffff')]
        L[i].pack(pady=5, padx=20)
        L[i].bind("<Button-1>", eval_link(ind[i]))
        detail='Price : '+str(Df['Prix'].iloc[i])+' '+str(Values["Currency"])+'         Rating : '+str(Df['Rating'].iloc[i])+'         Sold : '+str(Df['Nombre De Commandes'].iloc[i])
        frame =Frame(sgca, bd=1, relief=SUNKEN)
        frame.pack()
        details=Label(frame, text=detail, fg="#727272", font="Times 12 ", bg='#ffffff')
        details.pack(pady=(0,10),side=LEFT)
        Mores = Mores+[Label(frame, text="          More >>>", fg="#095a50", cursor="hand2", font="Times 13 ", bg='#ffffff')]
        Mores[i].pack(pady=(0, 10))
        Mores[i].bind("<Button-1>", get_detail(ind[i]))

    sgca.mainloop()

