from tkinter import *
from tkinter import ttk
from SGCA import AliExpressScraper
import threading
from PIL import ImageTk, Image
from ttkwidgets import TickScale



def Prepare_Languages_Data(Languages):
    """
    Prépare les données à afficher sur la GUI et les données qui passeront en paramètres de la requête Aliexpress

    :param Languages: Liste de Langues disponibles sous le format "Langue : le code interpreté par Aliexpress" : ('English : en_US')
    :return: Deux listes, une contient le nom des langues et l'autre les codes correspondantes au format AliExpress sur le même ordre.


    """

    Langues = ['Default']
    Code_Langue = ['']
    for i in range(len(Languages)):
        Temp = Languages[i].split(' : ')
        Langues.append(Temp[0])
        Code_Langue.append(Temp[1])
    return Langues,Code_Langue

def set_config(Proxy,Config,Lab):
    """
    Tester si Proxy est égale à 'Own Proxy', si c'est le cas, il ajoute les widgets Config et Lab à
    l'interface graphique, sinon il les cache

    :param Proxy: Combobox ttk Widget qui contient une des valeur de la liste ['None', 'Default Proxy', 'Own Proxy']
    :param Config: Entry Widget de l'adresse IP à utiliser
    :param Lab: Label Widget associé à l'entrée l'entrée



    """
    x=Proxy.get()
    if x=='Own Proxy':
        Lab.grid(row=6, column=0, sticky=W, pady=(3, 0), padx=20)
        Config.grid(row=6, column=1, sticky=W, pady=(3, 0), padx=20)
    else:
        Lab.grid_forget()
        Config.grid_forget()

def Search(Box, Entry, liste):

    """
    Sélectionner toutes les valeurs de la liste contenant la suite des caractères entrées par l'utilisateur
    et les afficher sur le Box.

    :param Box: Il réfère au Combobox widget qui affiche la liste des valeurs possibles pour une entrées.
    :param Entry: Le contenue de la recherche.
    :param liste: La liste globale des valeurs possibles.

    """

    S = Entry.get().upper()
    Return=[]
    for e in liste:
        if e.upper().find(S)!=-1:
            Return.append(e)
    if len(Return)==0:
        Return = ['']
    Box['values'] = Return
    Box.current(0)


def set_img_color(img, color):
    """
    :param img: image Png
    :param color: la couleur du background souhaité sur l'image png
    """
    pixel_line = "{" + " ".join(color for i in range(img.width())) + "}"
    pixels = " ".join(pixel_line for i in range(img.height()))
    img.put(pixels)

def main(Countries, Languages, devises):
    """
    Générer et construire l'interface graphique d'accueil contenant les différents widgets d'input et le button du lancement de la requête.

    :param Countries: La liste des pays de livraison
    :param Languages: La liste des langues sous la forme 'Langue : Code_Langue'
    :param Devises: La liste des devises des prix.
    """

    ## Définir et preparer quelque variables
    bg='#ffffff'
    Langues, Code_Langue = Prepare_Languages_Data(Languages)
    devises[1:] = sorted(devises[1:])

    ## Créer l'Interface Tkinter
    main = Tk()
    main.title("Product Suggestion")
    main.configure(bg=bg)
    main.resizable(width=0, height=0)
    Values = {}

    ## Insérer le logo du comparateur d'offres
    frame0=Frame(main)
    frame0.configure(bg=bg)
    frame0.grid(row=0)

    img1 = ImageTk.PhotoImage(master=frame0, file="./Data/Scraper menu.png")
    can = Canvas(frame0, width=700, height=90,
                 borderwidth=0,
                 highlightthickness=0,
                 background=bg)
    can.configure(bg=bg)
    can.create_image(350, 60, image=img1)
    can.pack()

    ## Ajout les differents Input labels
    frame1 = Frame(main)
    frame1.configure(bg=bg)
    frame1.grid(row=1)

    ############ Nom du produit :
    Label(frame1, text="Product  : ", font="Times 14 ", justify="left", bg=bg).grid(row=0, column=0, sticky=W, pady=(30, 0), padx=(20,60))
    KeyWord = Entry(frame1, width=54, bg="#ffffff")
    KeyWord.grid(row=0, column=0, sticky=W, pady=(30, 0), padx=(160,30),ipady=2,columnspan=2)
    Values["KeyWord"] = KeyWord

    ###########################################  Settings : ###########################################
    Label(frame1, text="Settings :", font="Times 16 bold underline", justify="center", bg=bg,fg="#413d5c").grid(row=1, column=0,pady=(15, 0),columnspan=6)

    ############ Shipping Country :
    Label(frame1, text="Shipping Country : ", font="Times 14 ", justify="left", bg=bg).grid(row=2, column=0,sticky=W,pady=(20, 0),padx=20)
    Country_Search = Entry(frame1, width=36, bg="#FFFFFF")
    Country_Search.grid(row=2, column=1, sticky=W, padx=20, ipady=2)
    img = ImageTk.PhotoImage(master=frame1, file="./Data/Search.png")
    can = Canvas(frame1, width=34, height=24,
                 borderwidth=0,
                 highlightthickness=0,
                 background=bg)
    can.configure(bg=bg)
    can.create_image(17, 11.5, anchor=CENTER, image=img)
    can.grid(row=2, column=1, sticky=W, padx=(325, 20), pady=(0, 0))
    Shipping_Country = ttk.Combobox(frame1, values=Countries, width=40)
    Shipping_Country.current(0)
    Shipping_Country.grid(row=2, column=1, sticky=W, pady=(55, 0), padx=20)
    Values["Shipping_Country"] = Shipping_Country
## Lier Country_Search à la fonction Search qui s'exécute après chaque entrée du clavier.
    Country_Search.bind("<KeyRelease>", lambda event: Search(Shipping_Country, Country_Search, Countries))

    ############ Currency :
    Label(frame1, text="Currency : ", font="Times 14 ", justify="left", bg=bg).grid(row=3, column=0, sticky=W,pady=(20, 0), padx=20)
    Currency_Search = Entry(frame1, width=36, bg="#FFFFFF")
    Currency_Search.grid(row=3, column=1, sticky=W, padx=20, ipady=2)
    canvas = Canvas(frame1, width=34, height=24,
                    borderwidth=0,
                    highlightthickness=0,
                    background=bg)
    canvas.configure(bg=bg)
    canvas.create_image(17, 11.5, anchor=CENTER, image=img)
    canvas.grid(row=3, column=1, sticky=W, padx=(325, 20), pady=(0, 0))
    Currency = ttk.Combobox(frame1, values=devises, width=40)
    Currency.current(0)
    Currency.grid(row=3, column=1, sticky=W, pady=(55, 0), padx=20)
    Values["Currency"] = Currency
## Lier Currency_Search à la fonction Search qui s'exécute après chaque entrée du clavier.
    Currency_Search.bind("<KeyRelease>", lambda event: Search(Currency, Currency_Search, devises))

    ############ Language :
    Label(frame1, text="Language : ", font="Times 14 ", justify="left", bg=bg).grid(row=4, column=0, sticky=W,pady=(25, 0), padx=20)
    Language = ttk.Combobox(frame1, values=Langues, width=40)
    Language.current(0)
    Language.grid(row=4, column=1, sticky=W, pady=(25, 0), padx=20)
    Values["Language"] = Language

    ############ Proxy configuration :
    Label(frame1, text="Proxy configuration : ", font="Times 14 ", justify="left", bg=bg).grid(row=5, column=0,sticky=W,pady=(25, 0),padx=20)
    Proxy = ttk.Combobox(frame1, values=['None', 'Default Proxy', 'Own Proxy'], width=40)
    Lab = Label(frame1, text="\"user:pw@ip:port\" : ", font="Times 14 ", justify="left", bg=bg)
    Lab.grid_forget()
    Config = Entry(frame1, width=40, bg="#FFFFFF")
    Config.grid_forget()
    Proxy.current(0)
    Proxy.grid(row=5, column=1, sticky=W, pady=(25, 0), padx=20)
## Lier Proxy à la fonction set_config qui s'exécute après chaque entrée du clavier.
    Proxy.bind("<<ComboboxSelected>>", lambda event: set_config(Proxy, Config, Lab))
    Values["Proxy"] = Proxy
    Values["Config"] = Config

    ###########################################  Preferences : ###########################################
    Label(frame1, text="Preferences :", font="Times 16 bold underline", justify="center", bg=bg,fg="#413d5c").grid(row=7, column=0,pady=(16, 0),columnspan=6)

    ############ Price :
    Label(frame1, text="Price : ", font="Times 14 ", justify="left", bg=bg).grid(row=8, column=0, sticky=W,pady=(25, 0), padx=(20, 18))
    Min_price = Entry(frame1, width=8, bg="#ffffff")
    Min_price.grid(row=8, column=0, sticky=W, pady=(25, 0), ipady=2,padx=(120,0))
    Values["Min_price"] = Min_price
    Label(frame1, text=" - ", font="Times 14 ", justify="left", bg=bg).grid(row=8, column=0, sticky=W,pady=(25, 0), padx=(185,3))
    Max_price = Entry(frame1, width=8, bg="#ffffff")
    Max_price.grid(row=8, column=0, sticky=W, pady=(25, 0), ipady=2,padx=(207,0),columnspan=3)
    Values["Max_price"] = Max_price

    ############ Items Count :
    Label(frame1, text="Items Count :", font="Times 14 ", justify="left", bg=bg).grid(row=8, column=1,sticky=W, pady=(25, 0),padx=(120, 20))
    Max_Items = Entry(frame1, width=11, bg="#ffffff")
    Max_Items.grid(row=8, column=1, sticky=W, pady=(25, 0), ipady=2,padx=(270,0))
    Values["Max_Items"] = Max_Items

    ######################### Style Du TickScale :
    slider_width = 30
    slider_height = 17
    # normal slider
    img_slider = PhotoImage('img_slider', width=slider_width, height=slider_height, master=frame1)
    set_img_color(img_slider, "#e43225")
    # active slider
    img_slider_active = PhotoImage('img_slider_active', width=slider_width, height=slider_height, master=frame1)
    set_img_color(img_slider_active, '#f7971d')
    style = ttk.Style(frame1)
    style.theme_use('clam')
    style.configure("TCombobox", fieldbackground='#ffffff', background="#F9F9Fd")
    main.option_add('*TCombobox*Listbox.font', "Franklin 11")

    # create scale element
    style.element_create('custom.Horizontal.Scale.slider', 'image', img_slider,
                         ('active', img_slider_active))

    # create custom layout
    style.layout('custom.Horizontal.TScale',
                 [('Horizontal.Scale.trough',
                   {'sticky': 'nswe',
                    'children': [('custom.Horizontal.Scale.slider',
                                  {'side': 'left', 'sticky': ''})]})])
    style.configure('custom.Horizontal.TScale', background=bg, foreground='black',troughcolor='#ffffff')


    ############ Scale Barre :
    scale = TickScale(frame1, from_=-5, to=2, orient="horizontal", resolution=0.01,style='custom.Horizontal.TScale', length=360, showvalue=False)
    scale.set(-1.5)
    Label(frame1, text="Price  - ", font="Times 14 bold", justify="left", bg=bg).grid(row=9, column=0, sticky=W,pady=(20, 0),padx=(20,0))
    scale.grid(row=9, column=0, sticky=W, pady=(22, 0), ipady=2, columnspan=5, padx=(120, 0))
    Label(frame1, text=" +  Quality", font="Times 14 bold ", justify="left", bg=bg).grid(row=9, column=1, sticky=W,pady=(20, 0), padx=(262,0),columnspan=2)


    ## Ajouter le bouton de lancement lier a la fonction AliExpressScraper.launch qui s'exécute sur un thread:
    Button(frame1, text="Launch", width=30, bg='#ffffff', borderwidth='2', font="time 10",command=lambda: threading.Thread(target=AliExpressScraper.launch,
                            args=(Values, Langues, Code_Langue, main, scale)).start()).grid(row=10,column=0,pady=(30, 20),sticky=W,padx=(162,0),columnspan=2)
    main.mainloop()