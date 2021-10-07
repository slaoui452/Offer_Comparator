import threading
import time
import pandas as pd
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from tkinter import *
from tkinter import ttk
from selenium import webdriver
from GUI import Best_Offres
from SGCA import DataProcessing, ProxyScraper
from seleniumwire import webdriver
from tkinter import messagebox


def get_details(url,driver):

    """
    Extraction des données suivantes :  ["Title","Product_Id","Category_Id","Store_name","Follower_Num","Company_Id","Discount","Protection_Acheteur",
    "Delivry_Contry","Shipped_to","Shipping_Service","Currency_Shipping","Shipping_Price","Shipping_Time","Tracking","Delivery_Date"]
    et ["Attribut_ID","Activ_Price","Init_Price","Avail_Quantity"] de toutes les couleurs/modéles/choix disponibles

    :param url: Url du produit
    :param driver: utilisé dans le premier scraping où les paramètres ( pays, langue et devise) sont déjà saisis

    :return: Un Dictionnair contenant les différents éléments extraits de la page web.



    """

    dict={}
    driver.get(url)
    WebDriverWait(driver,0).until(lambda d: d.find_element_by_xpath("/html/body/script[12]"))

    try:
        dict["Title"] = driver.execute_script('return window.runParams.data.pageModule.title')
    except:
        pass
    try:
        dict["Product_Id"] = driver.execute_script('return window.runParams.data.actionModule.productId')
    except:
        pass
    try:
        dict["Category_Id"] = driver.execute_script('return window.runParams.data.actionModule.categoryId')
    except:
        pass
    try:
        dict["Store_name"] = driver.execute_script('return window.runParams.data.storeModule.storeName')


    except:
        pass
    try:
        dict["Store_Rate"] = driver.execute_script('return window.runParams.data.storeModule.positiveRate')
    except:
        pass
    try:
        dict["Follower_Num"] = driver.execute_script('return window.runParams.data.storeModule.followingNumber')
    except:
        pass

    try:
        dict["Company_Id"] = driver.execute_script('return window.runParams.data.actionModule.companyId')
    except:
        pass
    try:
        dict["Discount"] = driver.execute_script('return window.runParams.data.priceModule.discount')
    except:
        pass
    try:
        dict["Protection_Acheteur"] = driver.execute_script(
            'return window.runParams.data.shippingModule.freightCalculateInfo.freight.commitDay')
    except:
        pass
    try:
        dict["Delivry_Contry"] = driver.execute_script(
            'return window.runParams.data.shippingModule.freightCalculateInfo.freight.sendGoodsCountryFullName')
    except:
        pass
    try:
        dict["Shipped_to"] = driver.execute_script('return window.runParams.data.shippingModule.regionCountryName')
    except:
        pass
    try:
        dict["Shipping_Service"] = driver.execute_script(
            'return window.runParams.data.shippingModule.freightCalculateInfo.freight.serviceName')
    except:
        pass
    try:
        dict["Currency_Shipping"] = driver.execute_script(
            'return window.runParams.data.shippingModule.freightCalculateInfo.freight.currency')
    except:
        pass
    try:

        dict["Shipping_Price"] = driver.execute_script(
            'return window.runParams.data.shippingModule.freightCalculateInfo.freight.standardFreightAmount.value')
    except:
        pass
    try:
        dict["Shipping_Time"] = driver.execute_script(
            'return window.runParams.data.shippingModule.freightCalculateInfo.freight.time')
    except:
        pass
    try:
        dict["Tracking"] = driver.execute_script(
            'return window.runParams.data.shippingModule.freightCalculateInfo.freight.tracking')
    except:
        pass
    try:
        dict["Delivery_Date"] = driver.execute_script(
            'return window.runParams.data.shippingModule.freightCalculateInfo.freight.deliveryDateFormat')
    except:
        pass

    i = 0
    dict["Attributes"] = []
    while (True):
        Att={}
        C = driver.execute_script('return window.runParams.data.skuModule.skuPriceList[' + str(i) + ']')
        if not C:
            break
        try:
            Att["Attribut"] = driver.execute_script(
                'return window.runParams.data.skuModule.skuPriceList[' + str(i) + '].skuAttr')
            Att["Attribut"] = Att["Attribut"][Att["Attribut"].find('#') + 1:]
        except:
            pass
        try:
            Att["Attribut_ID"] = driver.execute_script(
                'return window.runParams.data.skuModule.skuPriceList[' + str(i) + '].skuId')
        except:
            pass
        try:
            Att["Activ_Price"] = driver.execute_script(
                'return window.runParams.data.skuModule.skuPriceList[' + str(i) + '].skuVal.skuActivityAmount.value')
        except:
            pass
        try:
            Att["Init_Price"] = driver.execute_script(
                'return window.runParams.data.skuModule.skuPriceList[' + str(i) + '].skuVal.skuAmount.value')
        except:
            pass
        try:
            Att["Avail_Quantity"] = driver.execute_script(
                'return window.runParams.data.skuModule.skuPriceList[' + str(i) + '].skuVal.availQuantity')
        except:
            pass
        i += 1
        dict["Attributes"]=dict["Attributes"]+[Att]
    DataProcessing.get_text(dict)
    return dict


def scroll_down(driver):
    """
    Cette fonction permet de défiler la page en-bas petit à petit afin de charger toutes les données de cette derniére

    :param driver: le driver utilisé pour le scraping
    """

    total_height = int(driver.execute_script("return document.body.scrollHeight"))
    for i in range(1, total_height, 200):
        driver.execute_script("window.scrollTo(0, {});".format(i))

def scrape(driver,devise,i):
    """
    Cette fonction permet d'extraire les informations presentées dans les pages de recherche d'une façon efficace :
     ['Nom', 'Prix', 'Evaluation', 'Nombre De Commandes', 'Prix de livraison']
    en effet, l'algorithme ne collecte que les produits susceptible d'être envoyés au pays sélectionné par l'utilisateur.

    :param driver: le driver utilisé pour le scraping
    :param devise: Code de la devise selectionée par l'utilisateur

    :return: Renvoie une erreur si il n'existe pas un marqueur de livraison sur le pays sélectionné, sinon il renvoie une liste de la forme ['Nom', 'Prix', 'Evaluation', 'Nombre De Commandes', 'Prix de livraison']

    """

    x=driver.find_element_by_xpath("//*[@id=\"root\"]/div/div/div[2]/div[2]/div/div[2]/div["+str(i)+"]//*[@class=\"_2mXVg shIx4\"]")
    # Si le marqueur de la livraison "x" n'existe pas alors il renvoi une erreur

    livraison=0
    price=driver.find_element_by_xpath("//*[@id=\"root\"]/div/div/div[2]/div[2]/div/div[2]/div["+str(i)+"]//*[@class=\"_12A8D\"]").text
    price=price[len(devise):]
    Rate= driver.find_element_by_xpath("//*[@id=\"root\"]/div/div/div[2]/div[2]/div/div[2]/div["+str(i)+"]//*[@class=\"_1hEhM\"]").text
    Nombre_Com= driver.find_element_by_xpath("//*[@id=\"root\"]/div/div/div[2]/div[2]/div/div[2]/div["+str(i)+"]//*[@class=\"_2i3yA\"]").text
    Nom= driver.find_element_by_xpath("//*[@id=\"root\"]/div/div/div[2]/div[2]/div/div[2]/div["+str(i)+"]/div/div[1]/a/span").text

    ## 3 scénario existe dans cette partie:
    # Soit x.text == "+ envoie : prix livraison" et dans ce cas nous devons ajouter ce coût au prix initial
    # Soit x.text == "Livraison incluse " et donc le coût de la livraison est déjà inclus dans la variable extraite "price"
    # Soit x.text == "Retour gratuit" et donc il n'y a pas de livraison (cela a été conclu à partir de plusieurs testes et observations)
    # Étant données que ces valeurs change avec le changement de la langue nous n'avons utiliser que "+" et "R" pour l'analyse.

    if x.text[0]=="+":
        envoie= x.text
        livraison_pos= envoie.find(devise)+len(devise)
        pos2=envoie.find("R")
        if pos2!=-1:
            livraison=envoie[livraison_pos:pos2-1]
            print(envoie,livraison)
        else:
            livraison=envoie[livraison_pos:]

    if x.text[0]!="R":
        return [Nom,price,Rate,Nombre_Com,livraison]


def select_attributes(driver, contry, Langue, code_langue, Currency):
    """
    Cette fonction permet de passer les parametres selectionner sur l'interface graphique (Pays de livraison, Langue, Devise)
    au site Ali Expresse avant d'entamer le scraping des données.

    :param driver: le driver utilisé pour le scraping.
    :param contry: le pays de la livraison.
    :param Langue: la langue des details.
    :param code_langue: le code de la langue associer que Ali express Comprend.
    :param Currency: la devis d'affichage des prix des produits.


    """
    element = driver.find_element_by_xpath(("//*[@id=\"nav-global\"]/div[4]/div"))
    action = ActionChains(driver)
    action.click(on_element=element)
    action.perform()
    time.sleep(2)
    if contry!='Default':
        while (True):
            try:
                driver.find_element_by_xpath(("//*[@id=\"nav-global\"]/div[4]/div/div/div/div[1]/div/a[1]")).click()
                break
            except:
                action.perform()
                time.sleep(2)
                driver.get(driver.getCurrentURL())
        driver.find_element_by_xpath((" //*[@id=\"nav-global\"]/div[4]/div/div/div/div[1]/div/div[1]/div/input")).send_keys(
            contry)
        driver.find_element_by_xpath(
            ("//*[@id=\"nav-global\"]/div[4]/div/div/div/div[1]/div/div[1]/ul//*[@data-name=\"" + contry + "\"]")).click()

    time.sleep(1)
    if Langue!='Default':
        while (True):
            try:
                driver.find_element_by_xpath(("//*[@id=\"nav-global\"]/div[4]/div/div/div/div[2]/div/span")).click()
                break
            except:
                action.perform()
                time.sleep(3)
                print("im stuck here2")
        driver.find_element_by_xpath(("//*[@id=\"nav-global\"]/div[4]/div/div/div/div[2]/div/div/input")).send_keys(Langue)
        driver.find_element_by_xpath(
            ("//*[@id=\"nav-global\"]/div[4]/div/div/div/div[2]/div/ul//*[@data-locale=\"" + code_langue + "\"]")).click()

    if Currency!='Def':
        while (True):
            try:
                driver.find_element_by_xpath(("//*[@id=\"nav-global\"]/div[4]/div/div/div/div[3]/div/span")).click();
                break;
            except:
                action.perform()
                time.sleep(3)
                print("im stuck here2")
        driver.find_element_by_xpath(("//*[@id=\"nav-global\"]/div[4]/div/div/div/div[3]/div/div/input")).send_keys(
            Currency)
        driver.find_element_by_xpath(
            ("//*[@id=\"nav-global\"]/div[4]/div/div/div/div[3]/div/ul//*[@data-currency=\"" + Currency + "\"]")).click()

    element1 = driver.find_element_by_xpath(("//*[@id=\"nav-global\"]/div[4]/div/div/div/div[4]/button"))
    action2 = ActionChains(driver)
    action2.click(on_element=element1)
    action2.perform()
    time.sleep(3)


def get_devise(driver):
    """
    :param driver: le driver utilisé pour le scraping
    :return: Renvoie le code de la devise séléctionnée (Ex : € pour la devise EUR)
    """

    devise= driver.find_element_by_xpath(("//*[@class=\"_12A8D\"]")).text
    for i in range(len(devise)):
        try:
            int(devise[i])
            break
        except :
            pass
    return devise[:i]

def add(main,Valeur):
    """
    Cette fonction permet d'ajouter le label contenant le nom du produit recherché,
    la barre de progression et le pourcentage de progrès à l'interface main

    :param main: L'interface graphique
    :param Valeur: Le nom du produit recherché

    :return: Renvoie le nouveau frame, la barre de progression et le label qui affiche le pourcentage
    """

    frame6=Frame(main)
    frame6.configure(bg='#ffffff')
    frame6.grid()
    s = ttk.Style()
    s.theme_use('clam')
    s.configure("red.Horizontal.TProgressbar", foreground='#f7961a', background='#f7961a')
    try :
        Valeur=Valeur[0].upper()+Valeur[1:]
    except:
        pass
    Label(frame6, text=Valeur + " : ", font="Helvetica 12 ", bg='#ffffff',width=15).grid(column=0, row=0, pady=(10,10),padx=(20))

    pb = ttk.Progressbar(
        frame6,
        orient='horizontal',
        mode='determinate',
        length=300,
        style="red.Horizontal.TProgressbar",
    )

    # place the progressbar
    pb.grid_forget()
    label = Label(frame6, text="00%", font="Helvetica 12 ", bg='#ffffff',width=15)
    label.grid_forget()

    return frame6,pb,label


def PageLoader(driver,url):
    driver.execute_script('window.open("' + url + '")')

def AliExpress_Scraper(Valeurs,Langues,Code_Langue,scale,frame6,pb,label):
    """
    Il s'agit de la fonction principale de l'exécution de la requête.
    A l'aide des méthodes prédéfinies, cette algorithme permet de :

    - Ajouter la progresse barre et les label correspandentes a l'interface graphique, add()
    - En cas de "Default proxy" lancer l'extraction des adresses ip et les tester, ProxyScraper.get_Proxy_list()
    - Inserer les parramétres de la requete sur le site AliExpress, select_attributes()
    - Extraction des données, scrape()
    - L'analyse et le traitement des données, DataProcessing.Get_Suggestion()


    :param Valeurs: un dictionnaire qui contient toutes les entrées de l'utilisateur ("KeyWord","Shipping_Country","Currency","Language","Proxy","Config","Min_price","Max_price","Max_Items")
    :param Langues: la liste des langues des details.
    :param Code_Langue: la liste des code de langues associées que Ali express Comprend.
    :param main: L'interface graphique
    :param scale: la valeur du rapport qualité prix determiner par le scale barre.


    :return: Renvoie une Data Frame trier par ordre de pertinences selon les besoins de l'utilisateur, et aussi le temps d'exécution de la requête.

    """

    coefficient=scale.get()
    Dict = {}
    WebDriver_path = "./chromedriver.exe"
    Values = DataProcessing.Get_GUI_Values(Valeurs)

    ## Configuration du webdriver

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument("--window-size=1900,900")
    if Values['Proxy'] == 'None':
        proxy=''
    elif Values['Proxy'] == 'Own Proxy':
        proxy =Values["Config"]


    else: # Si Values['Proxy'] == 'Default Proxy'
        print("Get Proxies List ...")
        ## Srape une liste d'adresse IP a partir du site https://www.sslproxies.org/
        Proxies = ProxyScraper.get_Proxy_list(WebDriver_path)
        print(Proxies)
        ##### Get a working proxy
        print("Get a working proxy ...")
        proxy = ProxyScraper.det_Av_Proxy(Proxies)
        print(proxy)

    ######### Prepare and Launch The webdriver which we'll use to scrape data from AliExpress

    if Values['Proxy'] != 'None' :
        options = {
            'proxy': {
                'http': 'http://'+proxy,
                'https': 'https://'+proxy,
                'no_proxy': 'localhost,127.0.0.1'
            }
        }
        chrome_options.headless = True
        driver = webdriver.Chrome(WebDriver_path, options=chrome_options, seleniumwire_options=options)
    else:
        chrome_options.headless = True
        driver = webdriver.Chrome(WebDriver_path, options=chrome_options)


    ######### For calculate timing of the scraping
    t1 = time.time()

    print("Collecte de données depuis AliExpress ... ")
    pb['value'] = 10
    label['text'] = "    10%     "
    driver.get(
        "https://fr.aliexpress.com/wholesale?trafficChannel=main&d=y&CatId=0&SearchText=" + Values[
            "KeyWord"] + "&ltype=wholesale&SortType=default&page=1")
    pb['value'] = 20
    label['text'] = "    20%     "

    Code_Langue = Code_Langue[Langues.index(Values["Language"])]

    # Sélectionner les différentes attribut sur le site AliExpress
    if Values["Shipping_Country"] != 'Default' or Values["Language"]!='Default' or Values["Currency"]!='Default':
        select_attributes(driver, Values["Shipping_Country"], Values["Language"], Code_Langue, Values["Currency"][:3])

    pb['value'] = 45
    label['text'] = "    45%     "

    ### Get the currency of prodect
    devise = get_devise(driver)
    print("La devise des prix est : " + str(devise))
    print("Collecte des données de la 1 ère page ...")

    # Lancement des threads pour le chargement des 7 pages à scraper
    Threads = []
    for m in range(2, 8):
        url = "https://fr.aliexpress.com/wholesale?trafficChannel=main&d=y&CatId=0&SearchText=" + Values[
            "KeyWord"] + "&ltype=wholesale&SortType=default&page=" + str(m)
        t = threading.Thread(target=PageLoader, args=[driver,url])
        t.start()
        Threads.append(t)

    for thread in Threads:
        thread.join()

    ###############################
    all_handeles = driver.window_handles
    for tab in all_handeles:
        driver.switch_to.window(tab)
        ### Scroll down to load all the elements of the page
        scroll_down(driver)
        pb['value'] = pb['value'] +5
        label['text'] = "    "+str(pb['value'])+"%     "
        print(all_handeles.index(tab))
        ### Start Scrapping
        i = 1
        while (True):
            try:
                link = driver.find_element_by_xpath(
                    "//*[@id=\"root\"]/div/div/div[2]/div[2]/div/div[2]/div[" + str(i) + "]/a").get_attribute("href")
                try:
                    text = link[:link.find('.html') + 5]
                    Dict[text] = scrape(driver, devise, i)
                except:
                    pass
                i += 1
            except:
                driver.close()
                break

    pb['value'] = 90
    label['text'] = "    90%     "
    print(len(Dict), " produits collectés")
    print("Traitement ... ")
    Values["Currency"] = devise
    ### Get Suggested Product
    try:
        Df = pd.DataFrame.from_dict(Dict, orient='index',columns=['Nom', 'Prix', 'Rating', 'Nombre De Commandes', 'Prix livraison'])

    except:
        Df = pd.DataFrame(data=Dict).T
        Df=Df.set_axis(['Nom', 'Prix', 'Rating', 'Nombre De Commandes', 'Prix livraison'], axis=1, inplace=False)

    Df=Df.dropna()
    Df = DataProcessing.Get_Suggestion(Df, devise,coefficient)

    t2 = time.time()
    print("Les Produits suggérés")
    pb['value'] = 100

    # Remplacer le label qui affiche le pourcentage par un bouton pour accéder à la liste des meilleurs offres
    label.grid_forget()
    Boutton = Button(frame6, text="Best Offers", width=15, bg='#ffffff', borderwidth='2',command=lambda:Best_Offres.Get_product(Df,Values,driver), font="time 9")
    Boutton.grid(column=3, row=0, pady=(10, 10),padx=(43,20))
    print(t2-t1)
    return Df, t2 - t1


def launch(Valeurs,Langues,Code_Langue,main,scale):
    """
    Cette fonction à pour rôle de gérer les exceptions et les erreurs qui pourront y parvenir. Par exemple l'échec
     de la connexion au serveur proxy.

    :param Valeurs: un dictionnaire qui contient toutes les entrées de l'utilisateur
    ["KeyWord","Shipping_Country","Currency","Language","Proxy","Config","Min_price","Max_price","Max_Items"]
    :param Langues: la liste des langues des details.
    :param Code_Langue: la liste des code de langues associées que Ali express Comprend.
    :param main: L'interface graphique
    :param scale: la valeur du rapport qualité prix determiner par le scale barre.

    :return: En cas d'erreur dans l'exécution de la requête il renvoit un message d'erreur et il met fin au thread
    """

    Values = DataProcessing.Get_GUI_Values(Valeurs)
    frame6,pb,label= add(main,Values["KeyWord"])
    pb.grid(column=1, row=0,columnspan=2, pady=(10,10),sticky=W)
    label.grid(column=3, row=0, pady=(10,10),padx=20,sticky=W)
    try:
        AliExpress_Scraper(Valeurs, Langues, Code_Langue, scale,frame6,pb,label)
    except Exception as ex:
        frame6.grid_forget()
        return messagebox.showwarning("Attention", "Scraping \"%s\" product has been interrupted. \nError: %s" %(Values["KeyWord"],str(type(ex).__name__)))


