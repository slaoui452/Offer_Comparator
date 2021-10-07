from sklearn.preprocessing import MinMaxScaler
from GUI import Best_Offres
import math


def get_text(dict):
    """
    Cette fonction permet de transformer un dictionnaire à un texte bien structuré et fait appelle a la fonction qui crée
    une nouvelle fenêtre et affiche le résultat obtenu Best_Offres.display_details()

    :param dict: un dictionnaire qui contient tous les détails sur le produit en question
    """

    general_details=''
    att_details=''
    Nb_attr=len(dict["Attributes"])
    for key in dict:
        if key=="Attributes":
            for i in range(Nb_attr):
                e=dict["Attributes"][i]
                att_details = att_details + str(i) +". "+str(e["Attribut"]) + " : \n"
                del e["Attribut"]
                for key2 in e:
                    att_details=att_details+key2+' : '+ str(e[key2])+'\n'
                att_details = att_details+'\n\n'
        else:
            general_details=general_details+key+' : '+ str(dict[key])+'\n'

    Best_Offres.display_details(general_details+att_details)

def Get_GUI_Values(Values):
    # Get values from tkinter widgets
    Valeurs={}
    for key in Values:
        Valeurs[key]=Values[key].get()
    return Valeurs


def Get_Suggestion(Df,devise,scale):
    """
    Cette fonction assure le prétraitement, le traitement et l'analyse des données afin d'extraire les produits les plus adéquates aux attentes de l'utilisateur.

    :param Df: Dataframe contenant les produit collecté par scraping du site Aliexpress
    :param devise: représente la devise des prix sans la dataframe
    :param scale: réfère au rapport qualité/prix voulu par l'utilisateur

    :return: En cas d'erreur dans l'exécution de la requête il renvoit un message d'erreur et il met fin au thread
    """

    Df['Prix']=Df['Prix'].replace(devise,'',regex=True)
    com=''
    if devise=='€ ':
        com='.'
        Df['Prix livraison']=Df['Prix livraison'].replace('\.','',regex=True)
        Df['Prix']=Df['Prix'].replace('\.','',regex=True)

    Df['Prix livraison']=Df['Prix livraison'].replace(',',com,regex=True).astype(float)
    Df['Prix']=Df['Prix'].replace(',',com,regex=True).astype(float)+Df['Prix livraison']
    Df['Prix']=round(Df['Prix'], 2)
    Df['Nombre De Commandes']=Df['Nombre De Commandes'].map(lambda x: x[:x.find(' ')])

    columns_to_standarize = ['Rating', 'Nombre De Commandes']
    scaled_data = Df.copy()
    scaler = MinMaxScaler()
    scaled_columns = scaler.fit_transform(scaled_data[columns_to_standarize].values)
    scaled_data[columns_to_standarize] = scaled_columns
    Df['Quality'] = scaled_data['Rating']*0.6+scaled_data['Nombre De Commandes']*0.4

    Df=Df.sort_values(by=['Quality'],ascending=False)

    columns_to_standarize=['Prix']
    scaled_data=Df.copy()
    scaler = MinMaxScaler()
    scaled_columns = scaler.fit_transform(scaled_data[columns_to_standarize].values)
    scaled_data[columns_to_standarize]=scaled_columns
    scaled_data['Prix']=abs(scaled_data['Prix']-1)

    columns_to_standarize = ['Quality']
    scaler = MinMaxScaler()
    scaled_coef = scaler.fit_transform(scaled_data[columns_to_standarize].values)
    scaled_data[columns_to_standarize]=scaled_coef

    Coef_Quality = math.exp(scale)
    # Scale -> [-5,2]  //  Avg = -1.5
    # Coef_Quality -> [0.006, 7.389]  //  math.exp(Avg) = 0.22
    Df['Rate'] = scaled_data['Quality']*Coef_Quality+scaled_data['Prix']

    Df=Df.sort_values(by=['Rate'],ascending=False)
    return Df