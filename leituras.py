from datetime import datetime, date, timedelta, time
import requests
import json
import datetime
import threading


def reloadapi():
    threading.Timer(5.0, reloadapi).start()
    info = requests.get("http://api.ipma.pt/open-data/forecast/meteorology/rcm/rcm-d0.json")
    infos = info.json()

    """
    1 - Risco reduzido #61D741
    2 - Risco moderado #E4E143
    3 - Risco Elevado #FB9C31
    4 - Risco muito elevado #E8511F
    5 - Risco máximo #DA0303
    
    {% if risco_X == 'Risco reduzido' %} color:#61D741; {% endif %}
    {% if risco_X == 'Risco moderado' %} color:#E4E143; {% endif %}
    {% if risco_X == 'Risco elevado' %} color:#FB9C31; {% endif %}
    {% if risco_X == 'Risco muito elevado' %} color:#E8511F; {% endif %}
    {% if risco_X == 'Risco máximo' %} color:#DA0303; {% endif %}
    
    1106 - Lisboa
    1312 - Porto
    0805 - Faro
    0603 - Coimbra
    0705 - Évora
    """

    lisboa = '1106'
    porto = '1312'
    faro = '0805'
    coimbra = '0603'
    evora = '0705'

    riscos = ["Risco reduzido", "Risco moderado", "Risco elevado", "Risco muito elevado", "Risco máximo"]


    for top, desc in infos.items():
        if type(desc) is str:
            if top == 'dataPrev':
                # dataprev = datetime(desc[0:4], desc[5:7], desc[8:10])
                dataprev = (datetime.date(int(desc[0:4]), int(desc[5:7]), int(desc[8:10]))).strftime("%d/%m/%Y")
        if type(desc) is dict:
            for chave, valor in desc.items():
                if chave == lisboa:
                    risco_lisboa = riscos[(valor['data']['rcm'])-1]
                elif chave == porto:
                    risco_porto = riscos[(valor['data']['rcm']) - 1]
                elif chave == coimbra:
                    risco_coimbra = riscos[(valor['data']['rcm']) - 1]
                elif chave == evora:
                    risco_evora = riscos[(valor['data']['rcm']) - 1]
                elif chave == faro:
                    risco_faro = riscos[(valor['data']['rcm']) - 1]

    return infos, lisboa, porto, coimbra, evora, faro, riscos, dataprev, risco_lisboa, risco_porto, risco_coimbra, risco_evora, risco_faro