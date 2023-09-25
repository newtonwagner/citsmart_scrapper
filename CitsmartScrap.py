# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 13:40:42 2023

@author: newton
"""

#%% Importar as bibliotecas necessarias
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from time import sleep
import re
import pandas as pd

#%% Entrar no SIGEDE (Citsmart)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get('https://yourCitsmartUrl')

#%% Logar com usuario e senha

sleep(10)
#//input[@id="user"]
campo_user = driver.find_element(By.XPATH, "//input[@id='user']")
campo_user.send_keys('username')

#//input[@id="senha"]
campo_senha = driver.find_element(By.XPATH, "//input[@id='senha']")
campo_senha.send_keys('password')

#//button[@id]
botao_entrar = driver.find_element(By.XPATH, "//button[@id]")
botao_entrar.click()

#%% Entrar no Módulo de Atendimento

sleep(6)
driver.get('https://yourCitsmartUrl/ServiceMOdule')

#%% Selecionar "Ver 200 por página"

sleep(4)
#//select[@id='itensPorPagina']
campo_porPagina = driver.find_element(By.XPATH, "//select[@id='itensPorPagina']")
opcoes_porPagina = Select(campo_porPagina)
opcoes_porPagina.select_by_visible_text('200')

#%% Varrer e registrar os Numeros de Solicitacoes

# recupera cada chamado do sigede separadamente
elementos_sigedes = driver.find_elements(By.XPATH, "//div[contains(@class, 'listaDetalhada')]")

# pattern para o numero do sigede
regex_numero = re.compile('\[(\d{5,6})\]')
# pattern para a data de criacao
regex_data = re.compile('Criada em.?\n(\d{2}\/\d{2}\/\d{4})')
# pattern para demandante
regex_autor = re.compile('Criado por.?\n([^\(]+)')
# pattern para a situacao
regex_situacao = re.compile('Situa..o.?\n(.+)')
# pattern para o servico
regex_servico = re.compile('Servi.o.?\n(.*)')

#%% Varre os sigedes printando os encontrados

lista_sigedes = []
for sigede in elementos_sigedes:
    conteudo = sigede.text
    numero = re.search(regex_numero, conteudo).group(1)
    criado_em = re.search(regex_data, conteudo).group(1)
    situacao = re.search(regex_situacao, conteudo).group(1)
    autor = re.search(regex_autor, conteudo).group(1)
    servico = re.search(regex_servico, conteudo)
    if (servico != None):
        lista_sigedes.append([numero, servico.group(1), criado_em, autor, situacao])

sigedes = pd.DataFrame(lista_sigedes, columns=['numero', 'servico', 'criado_em', 'autor', 'situacao'])
print(sigedes)

#%% Fecha o webdriver

sleep(10) 
driver.close()
driver.quit()
