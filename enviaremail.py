from email.mime.image import MIMEImage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time
from leituras import reloadapi


def enviar():

    infos, lisboa, porto, coimbra, evora, faro, riscos, dataprev, risco_lisboa, risco_porto, risco_coimbra, \
    risco_evora, risco_faro = reloadapi()

    estilo = """
    .um{{max-width:37.5rem; display: flex; flex-direction:column; justify-content:center; align-items: center;padding:1rem;margin: auto;border:0.125rem solid grey;border-radius:0.625rem;box-shadow: 0.313rem 0.313rem #DCDCDC}}
    .dois{{max-width:10rem;}}
    .tres{{display: flex; flex-direction:column; justify-content:center; align-items: center;}}
    .quatro{{font-size: 1.5rem;font-family: 'Oswald', sans-serif;padding:0;margin-bottom:0;margin-top:0}}
    .cinco{{font-size: 1.2rem;font-family: 'Oswald', sans-serif;padding:0;margin-top:0}}
    .seis{{font-family: 'Inter', sans-serif;text-align: center;font-size:1rem;
            {% if risco_lisboa == 'Risco reduzido' %} color:#61D741; {% endif %}
            {% if risco_lisboa == 'Risco moderado' %} color:#E4E143; {% endif %}
            {% if risco_lisboa == 'Risco elevado' %} color:#FB9C31; {% endif %}
            {% if risco_lisboa == 'Risco muito elevado' %} color:#E8511F; {% endif %}
            {% if risco_lisboa == 'Risco máximo' %} color:#DA0303; {% endif %}}}
    .sete{{font-family: 'Inter', sans-serif;text-align: center;font-size:0.8rem}}
    .oito{{font-family: 'Inter', sans-serif;text-align: center;font-size: 0.5rem;color:grey}}
    """

    message_html = f'''
    <!doctype html>
    <html lang="pt-PT">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <link href="https://fonts.googleapis.com/css2?family=Beau+Rivage&family=Oswald&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Cormorant+SC:wght@700&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300&display=swap" rel="stylesheet">
        <style type="text/css"> {estilo} </style>
        <title>Risco de Incêndios</title>
    </head>
    <body>
    
    
    <div class="um">
    
        <img class="dois" src="cid:imagem1" alt="Logo-IPMA">
    
        <div class="tres">
            <p class="quatro">RISCO DE INCÊNDIOS</p>
            <p class="cinco">{dataprev}</p>
        </div>
    
        <div>
            <b><p class="seis">LISBOA</p></b>
            <p class="sete">{risco_lisboa}</p>
        </div>
        <div>
            <b><p class="seis">PORTO</p></b>
            <p class="sete">{risco_porto}</p>
        </div>
        <div>
            <b><p class="seis">COIMBRA</p></b>
            <p class="sete">{risco_coimbra}</p>
        </div>
        <div>
            <b><p class="seis">ÉVORA</p></b>
            <p class="sete">{risco_evora}</p>
        </div>
        <div>
            <b><p class="seis">FARO</p></b>
            <p class="sete">{risco_faro}</p>
        </div>
    
    
        <p class="oito">Todos os dados foram reunidos pelo IPMA e podem ser encontrados em http://api.ipma.pt/.</p>
        <p class="oito">Copyright © IPMA 2017 | ipma.pt</p>
    
    </div>
    
    </body>
    </html>
    '''

    host = 'smtp.gmail.com'
    port = 587
    user = 'EMAIL_REMETENTE@gmail.com'
    password = 'SUA_SENHA_DE_APP'
    server = smtplib.SMTP(host, port)

    server.ehlo()
    server.starttls()
    server.login(user, password)

    email_msg = MIMEMultipart()
    # Lista de destinatários
    destinatarios = ['email1@gmail.com', 'email2@gmail.com', 'email3@gmail.com']
    email_msg['From'] = user
    # Transformar a lista de destinatários em uma str divididindo os emails por vírgulas.
    email_msg['To'] = str(destinatarios).replace('[', '').replace(']', '').replace("'", '').replace(" ", '')
    email_msg['Subject'] = 'Newsletter - Riscos de Incéndios'

    # Logo
    logo = open('static/images/download.png', 'rb')
    logoImage = MIMEImage(logo.read())
    logo.close()
    logoImage.add_header('Content-ID', '<imagem1>')
    email_msg.attach(logoImage)

    email_msg.attach(MIMEText(message_html, 'html'))

    # Receberá email_msg['To'] um por um
    multidest = MIMEMultipart()
    loop = 1
    while loop <= len(destinatarios):
        # Abrir e fechar o terminal a cada envio, para driblar o problema com o servidor do SMTP
        server.quit()

        server = smtplib.SMTP(host, port)
        server.ehlo()
        server.starttls()
        server.login(user, password)
        # Iniciar sempre com essa variável limpa
        multidest.__delitem__('To')
        # Se a lista do email_msg['To'] tiver mais de 1 elemento:
        if (email_msg['To'].find(',')) != -1:
            # Salvar na variável transitória o email (até a vírgula)
            multidest['To'] = email_msg['To'][0:(email_msg['To'].find(',')) + 1]
        # Se não houver vírgula, significa que só há 1 elemento:
        else:
            # Salvar o elemento inteiro
            multidest['To'] = email_msg['To'][0:]
        # Enviar para este elemento
        server.sendmail(email_msg['From'], f"<{multidest['To']}>", email_msg.as_string())
        print("Email enviado para ", multidest['To'])
        # Apagar este email da listagem do email_msg['To']
        att = str(email_msg['To'].split(',')[1:]).replace('[', '').replace(']', '').replace("'", '').replace(" ", '')
        # Limpar variável
        email_msg.__delitem__('To')
        # Adicionar os emails restantes na lista
        email_msg['To'] = att
        print("Seguintes: ", email_msg['To'], "\n")

        loop += 1
        time.sleep(2)

    server.quit()


if __name__ == '__main__':
    schedule.every(15).seconds.do(enviar)
    while True:
        schedule.run_pending()
        time.sleep(1)

