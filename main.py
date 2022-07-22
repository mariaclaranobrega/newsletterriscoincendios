from flask import Flask, render_template
import threading
import requests
import datetime


app = Flask(__name__)


@app.route('/')
def index():
    def reloadapi():
        threading.Timer(43200.0, reloadapi).start()
        info = requests.get("http://api.ipma.pt/open-data/forecast/meteorology/rcm/rcm-d0.json")
        infos = info.json()

        lisboa = '1106'
        porto = '1312'
        faro = '0805'
        coimbra = '0603'
        evora = '0705'
        riscos = ["Risco reduzido", "Risco moderado", "Risco elevado", "Risco muito elevado", "Risco máximo"]

        for top, desc in infos.items():
            if type(desc) is str:
                if top == 'dataPrev':
                    dataprev = (datetime.date(int(desc[0:4]), int(desc[5:7]), int(desc[8:10]))).strftime("%d/%m/%Y")
            if type(desc) is dict:
                for chave, valor in desc.items():
                    if chave == lisboa:
                        risco_lisboa = riscos[(valor['data']['rcm']) - 1]
                    elif chave == porto:
                        risco_porto = riscos[(valor['data']['rcm']) - 1]
                    elif chave == coimbra:
                        risco_coimbra = riscos[(valor['data']['rcm']) - 1]
                    elif chave == evora:
                        risco_evora = riscos[(valor['data']['rcm']) - 1]
                    elif chave == faro:
                        risco_faro = riscos[(valor['data']['rcm']) - 1]
        return risco_lisboa, risco_porto, dataprev,risco_coimbra, risco_faro, risco_evora

    risco_lisboa, risco_porto, dataprev, risco_coimbra, risco_faro, risco_evora = reloadapi()

    return render_template("index.html", risco_lisboa=risco_lisboa, risco_porto=risco_porto, dataprev=dataprev,
                           risco_coimbra=risco_coimbra, risco_faro=risco_faro, risco_evora=risco_evora)


if __name__ == "__main__":
    app.run(debug=True)
