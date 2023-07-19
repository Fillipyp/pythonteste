from selenium import webdriver
from time import sleep
from datetime import datetime, timedelta
import pandas as pd
import os.path
import glob
import getpass


User = getpass.getuser()
navegador = webdriver.Firefox()
link_braip = 'https://ev.braip.com/login'
painel_braip = 'https://ev.braip.com/vendas/relatorio'
navegador.get(url=link_braip)
abrir_arquivo = open('login.txt', 'r')
login_braip = abrir_arquivo.readline()
senha_braip = abrir_arquivo.readline()
abrir_arquivo.close()

campo_email = navegador.find_element_by_class_name('form-control')
sleep(1)
campo_email.send_keys(login_braip)
sleep(1)
campo_password = navegador.find_element_by_name('password')
sleep(1)
campo_password.send_keys(senha_braip)
alerta_login = datetime.today().strftime("[%H:%M %d/%m/%Y] ").ljust(8) + 'Login preenchido com sucesso\n'


def Recaptcha():
    get_url = navegador.current_url
    while get_url != link_braip:
        print(f'{get_url} você esta na pagina de relatorio')
        sleep(4)
        break
    else:
        sleep(10)
        print('você esta na pagina de login')
        return Recaptcha()


Recaptcha()
alerta_recaptcha = datetime.today().strftime("[%H:%M %d/%m/%Y] ").ljust(8) + 'Recaptcha feito com sucesso\n'

status = 'Pagamento Aprovado'
selecionar_status = navegador.find_element_by_xpath("//input[@placeholder='Todos os status']")
sleep(1)
selecionar_status.send_keys(status)
sleep(1)
selecionar_status.send_keys(u'\ue007')
sleep(1)
alerta_status = datetime.today().strftime("[%H:%M %d/%m/%Y] ").ljust(8) + 'Status preenchido com sucesso\n'

pagamento_boleto = 'Boleto'
pagamento_cartao = 'Cartão de Crédito'
pagamento_pix = 'Pix'

sleep(1)
selecionar_pagamento = navegador.find_element_by_xpath("//input[@placeholder='Todas as formas']")
sleep(1)
selecionar_pagamento.send_keys(pagamento_boleto)
sleep(1)
selecionar_pagamento.send_keys(u'\ue007')
sleep(1)
selecionar_pagamento.send_keys(pagamento_cartao)
sleep(1)
selecionar_pagamento.send_keys(u'\ue007')
sleep(1)
selecionar_pagamento.send_keys(pagamento_pix)
sleep(1)
selecionar_pagamento.send_keys(u'\ue007')
sleep(1)
alerta_pagamento = datetime.today().strftime("[%H:%M %d/%m/%Y] ").ljust(8) + 'Pagamento preenchido com sucesso\n'
sleep(1)

selecionar_filtro = navegador.find_element_by_class_name("abre_filtro").click()
sleep(1)
produto_growup = "Instagrowup"
selecionar_filtro = navegador.find_element_by_xpath("//input[@placeholder='Selecione...']")
sleep(1)
selecionar_filtro.send_keys(produto_growup)
sleep(1)
selecionar_filtro.send_keys(u'\ue007')
sleep(1)
selecionar_filtro = navegador.find_element_by_class_name("m-quick-sidebar__close").click()
sleep(1)

selecionar_data = navegador.find_element_by_name('dataPedido').click()
sleep(1)
# clicar em selecionar a data
selecionar_periodo = navegador.find_element_by_name('daterangepicker_start')
selecionar_periodo = selecionar_periodo.clear()
# limpar o campo da data padrão
sleep(1)
selecionar_periodo = navegador.find_element_by_name('daterangepicker_start')
dia_semana = datetime.today()
dia_semana = dia_semana.strftime('%A')


def verificardata():
    if dia_semana == 'Monday':
        data_hoje = datetime.today() - timedelta(days=3)
        data_hoje = data_hoje.strftime('%d/%m/%Y')
        selecionar_periodo.send_keys(data_hoje)
    else:
        data_hoje = datetime.today() - timedelta(days=1)
        data_hoje = data_hoje.strftime('%d/%m/%Y')
        selecionar_periodo.send_keys(data_hoje)


verificardata()

alerta_data = datetime.today().strftime("[%H:%M %d/%m/%Y] ").ljust(8) + 'Data preenchida com sucesso\n'
sleep(1)
# preencher o campo com a data de hoje
botao_ok = navegador.find_element_by_class_name('applyBtn').click()
sleep(1)
# clicar em ok
baixar_excel = navegador.find_element_by_id('exp_csv').click()
alerta_download = datetime.today().strftime("[%H:%M %d/%m/%Y] ").ljust(8) + 'Planilha baixada com sucesso\n'
sleep(10)

# pegar o ultimo elemento baixado na pasta downloads
diretorio = fr'C:/Users/{User}/Downloads'
tipo_de_arquivo = '\*xlsx'  # se nao quiser filtrar por extenção deixe apenas *
arquivo = glob.glob(diretorio + tipo_de_arquivo)
retorno = max(arquivo, key=os.path.getctime)
excel = pd.read_excel(retorno)
df_relatorio = excel
df_relatorio = df_relatorio[
    ['Utm_source', 'Comprador', 'E-mail', 'Telefone', 'Valor', 'Pagamento', 'Data Venda', 'Comissão do Afiliado',
     'Afiliado']]
df_relatorio.columns = ['Pago', 'Comprador', 'E-mail', 'Telefone', 'Valor', 'Pagamento', 'INICIO',
                        'Comissão do Afiliado', 'Afiliado']
df_relatorio = df_relatorio.fillna('')
inicio_formatado = df_relatorio["INICIO"] = (pd.to_datetime(df_relatorio['INICIO'])).dt.strftime('%d/%b')
df_controle = pd.read_excel(f'C:/Users/{User}/Documents/planilha_controle.xlsx')
# df_controle.drop([1, 15])
df_controle = df_controle.fillna('')
df_controle = df_controle[
    ['Pago', 'Comprador', 'E-mail', 'Telefone', 'Valor', 'Pagamento', 'INSTAGRAM', 'CONTROLE ID', 'INICIO', 'JANEIRO',
     'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO']]

df_relatorio['Comissão do Afiliado'] = df_relatorio['Comissão do Afiliado'].replace('', '0')
df_relatorio['Comissão do Afiliado'] = df_relatorio['Comissão do Afiliado'].apply(
    lambda x: float(x.replace(".", ",").replace(",", ".")))
df_relatorio['Valor'] = df_relatorio['Valor'].apply(lambda x: float(x.replace(".", ",").replace(",", ".")))
df_relatorio['Valor'] = df_relatorio['Valor'] - df_relatorio['Comissão do Afiliado']

df_relatorio = df_relatorio.round({'Valor': 0})
df_controle = df_controle.round({'Valor': 0})

df_relatorio['Valor'] = df_relatorio['Valor'].apply(lambda x: str(x))


def pagamento(value):
    if value == 'Crédito':
        return 'Braip Cartão'
    elif value == 'Pix':
        return 'Braip Pix'
    elif value == 'Boleto':
        return 'Boleto'


df_relatorio['Pagamento'] = df_relatorio['Pagamento'].apply(lambda x: pagamento(x))

def valorpagamento(value):
    if value == '497.0':
        return '467'
    elif value == '465.0':
        return '437'
    elif value >= '670.0' and value <= '680.0':
        return '638'
    elif value == '697.0':
        return '655'
    elif value == '436.50':
        return '409'
    elif value == '370.0':
        return '370'
    elif value == '357.0':
        return '357'
    elif value == '347.0':
        return '326'
    elif value == '247.0':
        return '232'
    elif value >= '242.0' and value <= '249.0':
        return '232'
    elif value >= '230.' and value <= '234.0':
        return '233'
    elif value == '197.0':
        return '186'
    elif value >= '180.0' and value <= '190.0':
        return '184'
    elif value >= '160.0' and value <= '164.0':
        return '163'
    elif value == '147.0':
        return '147'
    elif value >= '130.0' and value <= '132.0':
        return '131'
    elif value == "116.0":
        return '116'
    elif value == '108.0':
        return '108'
    elif value == '100.0':
        return '91'
    elif value == '97.0':
        return '91'
    elif value == '94.0':
        return '91'
    elif value == '96.0':
        return '91'
    # elif value >= '94.0' and value <= '99.80':
    #     return '91'
    elif value == '67.0':
        return '63'
    elif value == '52.0':
        return '52'
    elif value >= '50.0' and value <= '57.0':
        return '50'
    elif value == '49.90':
        return '46'
    elif value == '47.0':
        return '44'
    elif value >= '40.0' and value <='43.0':
        return '42'
    elif value == '30.0':
        return '30'
    elif value == '22.0':
        return '22'
    elif value == '43.0':
        return '43'


df_relatorio['Valor'] = df_relatorio['Valor'].apply(lambda x: valorpagamento(x))

df_relatorio.loc[
    (df_relatorio['Afiliado'] != "") & (df_relatorio['Pagamento'] == "Braip Pix"), 'Pagamento'] = "Braip Pix Afl"
df_relatorio.loc[
    (df_relatorio['Afiliado'] != "") & (df_relatorio['Pagamento'] == "Braip Cartão"), 'Pagamento'] = "Braip Cartão Afl"
df_relatorio.loc[(df_relatorio['Afiliado'] != "") & (df_relatorio['Pagamento'] == "Boleto"), 'Pagamento'] = "Boleto Afl"

df_relatorio = df_relatorio[['Pago', 'Comprador', 'E-mail', 'Telefone', 'Valor', 'Pagamento', 'INICIO']]
df_controle.set_index("Pago", inplace=True)
df_relatorio.set_index("Pago", inplace=True)
merge_dataframe = pd.merge(df_controle, df_relatorio,
                           on=['Pago', 'Comprador', 'E-mail', 'Telefone', 'Valor', 'Pagamento', 'INICIO'], how='outer')

merge_dataframe.to_excel(f'C:/Users/{User}/Documents/planilha_controle.xlsx')

navegador.execute_script(
    "document.querySelector(\"body\").innerHTML = \"<div style='display:  flex; background-color: #fff; justify-content: center; align-items: center; height: 100vh'; ><h1 style='color: #4BB543;'>Automação finalizada com sucesso</h1></div>\"")
sleep(1)
alerta_finalizado = datetime.today().strftime("[%H:%M %d/%m/%Y] ").ljust(8) + 'Automação finalizada com sucesso\n'
data_atual = datetime.today().strftime("%d-%m-%Y")
file = open("relatorio_automação" + str(data_atual) + ".txt", 'w')
file.write(alerta_login + alerta_recaptcha + alerta_status + alerta_pagamento + alerta_data + alerta_download + alerta_finalizado)
file.close()
sleep(4)
navegador.close()