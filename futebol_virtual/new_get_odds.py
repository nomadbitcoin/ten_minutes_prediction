#!/usr/bin/env python
# coding: utf-8

# In[284]:


import requests
import bs4
import time
from datetime import datetime

import pandas as pd
pd.options.display.max_rows = 100
pd.options.display.max_columns = 100


# In[2]:


mundial = 'https://www.betfair.com/sport/virtuals/football-world-cup'


# In[3]:





# ### IRA PEGAR OS DADOS DO JOGO ATUAL

# In[342]:





# In[ ]:





# In[ ]:





# In[340]:





# In[324]:





# In[349]:


def saveDataToDF():
    '''
        Salva os dados no Dataframe
    '''
    colunas = ['hora', 'event_id', 'time_A', 'empate', 'time_B', 'under', 'over', 'resultado_1_0', 'resultado_2_0', 'resultado_2_1', 'resultado_0_0', 'resultado_1_1', 'resultado_2_2', 'resultado_0_1', 'resultado_0_2', 'resultado_1_2', 'visitado_empate', 'visitado_visitante', 'empate_visitante', 'total_0', 'total_1', 'total_2', 'total_3', 'total_4']
    
    row = 0
    global data
    data = pd.DataFrame(columns=colunas, dtype=str)
    
    data.loc[row, 'hora'] = hora
    data.loc[row, 'event_id'] = event_id

    data.loc[row, 'time_A'] = time_A
    data.loc[row, 'empate'] = empate
    data.loc[row, 'time_B'] = time_B

    data.loc[row, 'under'] = under
    data.loc[row, 'over'] = over

    data.loc[row, 'resultado_1_0'] = resultado_1_0
    data.loc[row, 'resultado_2_0'] = resultado_2_0
    data.loc[row, 'resultado_2_1'] = resultado_2_1

    data.loc[row, 'resultado_0_0'] = resultado_0_0
    data.loc[row, 'resultado_1_1'] = resultado_1_1
    data.loc[row, 'resultado_2_2'] = resultado_2_2

    data.loc[row, 'resultado_0_1'] = resultado_0_1
    data.loc[row, 'resultado_0_2'] = resultado_0_2
    data.loc[row, 'resultado_1_2'] = resultado_1_2

    data.loc[row, 'visitado_empate'] = visitado_empate
    data.loc[row, 'visitado_visitante'] = visitado_visitante
    data.loc[row, 'empate_visitante'] = empate_visitante

    data.loc[row, 'total_0'] = total_0
    data.loc[row, 'total_1'] = total_1
    data.loc[row, 'total_2'] = total_2
    data.loc[row, 'total_3'] = total_3
    data.loc[row, 'total_4'] = total_4
    return data


# In[326]:


# data_event = pd.DataFrame(columns=colunas, dtype=str)


# In[ ]:


data_event = pd.read_csv('data_event.csv')


# In[ ]:


while True:
    # if req.status_code == 200:
    req = requests.get(mundial)
    htmlPage = bs4.BeautifulSoup(req.content, features='html.parser')
    
    evento_atual = htmlPage.find('div',{'class':'mod-virtuals-marketview'})
    informacoes = evento_atual.find('span',{'data-gaaction':'Clicked'})
    hora = informacoes.text.replace('\n','')
    event_id = informacoes.get('data-eventid')

    if event_id not in data['event_id'].tolist():
        
        tabela_dados = evento_atual.find('div',{'class':'content eventid-' + str(event_id)})
    
        event_name = tabela_dados.find('div',{'class':'event-name'}).text

        probabilidades = tabela_dados.find('div',{'class':'market type-match_odds'}).find_all('div',{'class':'bet-button'})
        time_A = probabilidades[0].text.replace('\n','')
        empate = probabilidades[1].text.replace('\n','')
        time_B = probabilidades[2].text.replace('\n','')

        under_over = tabela_dados.find('div',{'class':'market type-over_under_25'}).find_all('div',{'class':'bet-button'})
        under = under_over[0].text.replace('\n','')
        over = under_over[1].text.replace('\n','')

        resultado_correto = tabela_dados.find('div',{'class':'market market-correct-score type-correct_score'}).find_all('div',{'class':'cell'})

        #para os resultados do time 1
        resultado_1_0 = resultado_correto[1].find('span',{'class':'ui-runner-price'}).text.replace('\n','')
        resultado_2_0 = resultado_correto[2].find('span',{'class':'ui-runner-price'}).text.replace('\n','')
        resultado_2_1 = resultado_correto[3].find('span',{'class':'ui-runner-price'}).text.replace('\n','')

        #para os empates
        resultado_0_0 = resultado_correto[5].find('span',{'class':'ui-runner-price'}).text.replace('\n','')
        resultado_1_1 = resultado_correto[6].find('span',{'class':'ui-runner-price'}).text.replace('\n','')
        resultado_2_2 = resultado_correto[7].find('span',{'class':'ui-runner-price'}).text.replace('\n','')

        #para os resultados do time 2
        resultado_0_0 = resultado_correto[9].find('span',{'class':'ui-runner-price'}).text.replace('\n','')
        resultado_0_1 = resultado_correto[10].find('span',{'class':'ui-runner-price'}).text.replace('\n','')
        resultado_1_2 = resultado_correto[11].find('span',{'class':'ui-runner-price'}).text.replace('\n','')

        dupla_chance = tabela_dados.find('div',{'class':'market type-double_chance'}).find_all('div',{'class':'bet-button'})
        visitado_empate = dupla_chance[0].text.replace('\n','')
        visitado_visitante = dupla_chance[1].text.replace('\n','')
        empate_visitante = dupla_chance[2].text.replace('\n','')

        total_gols = tabela_dados.find('div',{'class':'market type-total_goals'}).find_all('div',{'class':'bet-button'})
        total_0 = total_gols[0].text.replace('\n','')
        total_1 = total_gols[1].text.replace('\n','')
        total_2 = total_gols[2].text.replace('\n','')
        total_3 = total_gols[3].text.replace('\n','')
        total_4 = total_gols[4].text.replace('\n','')
        
        
        saveDataToDF()
        
        data_event = data_event.append(data)
        data_event.to_csv('data_event.csv', index=None)
        print('dados salvos {}'.format(datetime.now().strftime('%H:%M:%S')))
    else:
        time.sleep(90)


# In[ ]:





# In[ ]:




