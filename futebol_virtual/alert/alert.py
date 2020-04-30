#!/usr/bin/env python
# coding: utf-8

# In[37]:


import pygame
from pygame.locals import *
import time
import requests
from datetime import datetime
import bs4
import os


# In[38]:


pygame.init()
musica = pygame.mixer.Sound('alert.wav')
musica.set_volume(1)


# In[43]:


verified_events = []


# In[40]:
from twilio.rest import Client

account_sid = 'AC9c0f990c8862e7233314e7cb4c763078'
auth_token = '9e69cd4edea02c36f50f33483bbbdd3d'
client = Client(account_sid, auth_token)

# this is the Twilio sandbox testing number
from_whatsapp_number='whatsapp:+14155238886'
# replace this number with your own WhatsApp Messaging number
yan_number='whatsapp:+554788917321'
uilton_number='whatsapp:+557191289667'

def sendMessage(message):
    client.messages.create(body=message, from_=from_whatsapp_number, to=yan_number)
    # time.sleep(0.3)
    # client.messages.create(body=message, from_=from_whatsapp_number, to=uilton_number)
    return True

# sendMessage('Mensagem Funcionando7')



def playSong():
    '''
        Reproduz som de alerta
    '''
    try:
        musica.play(-1)
        time.sleep(10)
        musica.stop()
    except KeyboardInterrupt:
        print('Stopped')
        return True


# In[1]:


def getGameSequence(sequence_size, all_markets=True, market=None):
    '''
        Ira pegar uma sequencia de jogos under para poder apostar no over
    '''
    
    futebol_virtual = 'https://www.betfair.com/sport/virtuals-results?sport=SOCCER&day='
    mundial_virtual = 'https://www.betfair.com/sport/virtuals-results?sport=SOCCER_WORLD_CUP&day='
    
    if all_markets != True and market == 1:
        urls = {'futebol_virtual':futebol_virtual}
    elif all_markets != True and market == 2:
        urls = {'futebol_mundial_virtual':mundial_virtual}
    else:
#         print('\nVerificando se ha uma sequencia de {} jogos com under\n'.format(sequence_size))
        urls = {'futebol_virtual':futebol_virtual, 'futebol_mundial_virtual':mundial_virtual}
    
    last_games = []
    for pos, url in enumerate(urls.keys()):
        os.system('clear')
        print('Verificando sequencia de {} eventos...\n'.format(size))
        
#         link = urls[url] + datetime.today().strftime('%Y-%m-%d')
        link = urls[url] + "2020-04-30"
        
        req = requests.get(link)
        if req.status_code == 200:
            htmlPage = bs4.BeautifulSoup(req.content, features='html.parser')
            table_results = htmlPage.find('div',{'class':'result-list-wrapper'})

            global goals
            goals = []
    #         print('\nUltimos {} jogos em {}'.format(sequence_size, url.replace('_', ' ').upper()))
            for pos, content in enumerate(table_results.find_all('div',{'class':'result-title'})):
                to_save = content.text
                content = content.text.split('\n')
                team_A = int(content[4].split('-')[0])
                team_B = int(content[4].split('-')[1])
                if (team_A + team_B) > 2:
                    goals.append(False)
                else:
                    goals.append(True)
    #             print(content[4])

                if pos == (sequence_size-1):
                    break

            if False not in goals and to_save not in verified_events:
                os.system('clear')

                print('\n------------> com boa sequencia para {} <------------'.format(url.replace('_', ' ').upper()))
                # print('\nUltimo jogo: {}\n'.format(content[4]))

                message = 'com boa sequencia para {}'.format(url.replace('_', ' ').upper())
                # sendMessage(message)
                playSong()

#                input('\n\nPressione alguma tecla para continuar...')

                goals = []
                verified_events.append(to_save)
                #salva o ultimo evento dessa sequencia como verificado
            else:
    #             print('\n\n------------> SEM BOA SEQUENCIA PARA {} <------------ \n\n\n'.format(url.replace('_', ' ')))
                goals = []
        else:
            print('problem with request')
            time.sleep(15)


# In[46]:

os.system('clear')
size = input('Verificar sequencia de quantos jogos?\n:')

while True:
    # 1 para FUTEBOL VIRTUAL
    
    # 2 PARA FUTEBOL VIRTUAL MUNDIAL
    
    # PARA OS DOIS MERCADOS:all_markets=True e sem parametro para market
    
#     getGameSequence(sequence_size=4, all_markets=False, market=2)    
    getGameSequence(sequence_size=int(size), all_markets=True)
    time.sleep(30)


# In[26]:


# musica.stop()

