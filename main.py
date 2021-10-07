# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from SGCA import ProxyScraper
from GUI import GUI_MAIN
from selenium import webdriver
from SGCA import AliExpressScraper

##### Import Countries Data
with open("Data/Countries.txt", "r") as f:
    Countries = ['Default']+f.read().split(' \n')[:-1]

##### Import Languages Data
with open("Data/Languages.txt", "r", encoding="utf-8") as f:
    Languages= f.read().split('\n')[:-1]

##### Import Currency Data
with open("Data/Currency.txt", "r") as f:
    devises = ['Default']+f.read().split('\n')[:-1]




if __name__ == '__main__':
    GUI_MAIN.main(Countries, Languages, devises)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
