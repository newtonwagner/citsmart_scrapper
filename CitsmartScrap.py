# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 13:40:42 2023

@author: newton
"""

#%% Importing
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from time import sleep
import re
import pandas as pd

#%% Creating driver and getting to Citsmart page

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get('https://yourCitsmartUrl')

#%% Login

sleep(10)
#//input[@id="user"]
field_user = driver.find_element(By.XPATH, "//input[@id='user']")
field_user.send_keys('username')

#//input[@id="senha"]
field_password = driver.find_element(By.XPATH, "//input[@id='senha']")
field_password.send_keys('password')

#//button[@id]
button_enter = driver.find_element(By.XPATH, "//button[@id]")
button_enter.click()

#%% Get to service module (url) after login

sleep(6)
driver.get('https://yourCitsmartUrl/ServiceMOdule')

#%% Select "View 200 per page"

sleep(4)
#//select[@id='itensPorPagina']
field_perPage = driver.find_element(By.XPATH, "//select[@id='itensPorPagina']")
option_perPage = Select(field_perPage)
option_perPage.select_by_visible_text('200')

#%% Scrap the page identifying tickets

# search list of tickets
elements_tickets = driver.find_elements(By.XPATH, "//div[contains(@class, 'listaDetalhada')]")

# pattern to ticket number
regex_number = re.compile('\[(\d{5,6})\]')
# pattern to create date
regex_create_date = re.compile('Criada em.?\n(\d{2}\/\d{2}\/\d{4})')
# pattern to author
regex_author = re.compile('Criado por.?\n([^\(]+)')
# pattern to status
regex_status = re.compile('Situa..o.?\n(.+)')
# pattern to service name
regex_service_name = re.compile('Servi.o.?\n(.*)')

#%% Varre os sigedes printando os encontrados

list_tickets = []
for ticket in elements_tickets:
    content = ticket.text
    ticket_number = re.search(regex_number, content).group(1)
    ticket_create_date = re.search(regex_create_date, content).group(1)
    ticket_status = re.search(regex_status, content).group(1)
    ticket_author = re.search(regex_author, content).group(1)
    ticket_service = re.search(regex_service_name, content)
    if (ticket_service != None):
        list_tickets.append([ticket_number, ticket_service.group(1), ticket_create_date, ticket_author, ticket_status])

tickets = pd.DataFrame(list_tickets, columns=['numero', 'servico', 'criado_em', 'autor', 'situacao'])
print(tickets)

#%% Fecha o webdriver

sleep(10) 
driver.close()
driver.quit()
