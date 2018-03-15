# encoding: utf-8
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyzabbix import ZabbixMetric, ZabbixSender
import configparser
import time
import os
import logging
import logging.handlers


arquivo_log = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'maeve.log')
logging.basicConfig(
    filename=arquivo_log,
    level=logging.NOTSET,
    format='[ %(asctime)s ] [ %(name)s:%(lineno)d - %(funcName)s() ] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler = logging.handlers.RotatingFileHandler(arquivo_log, maxBytes=1000000, backupCount=5)
logging.getLogger().addHandler(handler)


def setup():
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
    driver.set_window_size(1920, 1080)
    driver.set_page_load_timeout(15)
    return driver


def zbx_enviar(host,chave,valor):
    metrics = []
    m = ZabbixMetric(host,chave,valor)
    metrics.append(m)
    zbx = ZabbixSender('t-kyoto')
    zbx.send(metrics)


def pje1g():
    driver = setup()
    wait = WebDriverWait(driver, 10)
    config = configparser.ConfigParser()
    config.read('maeve.conf')
    usuario = config.get('PJe1G', 'usuario')
    senha = config.get('PJe1G', 'senha')
    url = config.get('PJe1G', 'url')

    try:
        # Login
        start = time.time()
        driver.get(url)
        user = driver.find_element_by_id('username')
        user.send_keys(usuario)
        password = driver.find_element_by_id('password')
        password.send_keys(senha)
        password.submit()

        # Verifica se logou
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'usuario-logado')))
        end = time.time()
        tempo_login = end - start
        zbx_enviar('PJe 1Grau','tempo_login', tempo_login)
        logging.info('Tempo login PJe 1Grau: ' + str(tempo_login))

    except Exception:
        zbx_enviar('PJe 1Grau', 'tempo_login', 0)
        zbx_enviar('PJe 1Grau', 'tempo_logout', 0)
        zbx_enviar('PJe 1Grau', 'tempo_pesquisa', 0)
        logging.error("Login PJe 1Grau falhou.")
        driver.quit()

    try:
        # Pesquisa
        start = time.time()

        # Navegação no menu para entrar na pesquisa
        menu_processo = wait.until(EC.visibility_of_element_located((By.ID, '_1007_j_id70j_id71')))
        ActionChains(driver).move_to_element(menu_processo).perform()
        menu_pesquisar_n1 = wait.until(EC.visibility_of_element_located((By.ID, '_1008_j_id70j_id75')))
        ActionChains(driver).move_to_element(menu_pesquisar_n1).perform()
        menu_pesquisar_n2 = wait.until(EC.visibility_of_element_located((By.ID, '_1009_j_id70j_id76')))
        ActionChains(driver).move_to_element(menu_pesquisar_n2).click().perform()
        wait.until(EC.visibility_of_element_located((By.ID, 'fPP:consultaSearchFields_header')))

        # Preenchimento do formulário de pesquisa
        num_sequencial = driver.find_element_by_id('fPP:numeroProcesso:numeroSequencial')
        num_sequencial.send_keys('0821120')
        num_digito_verificador = driver.find_element_by_id('fPP:numeroProcesso:numeroDigitoVerificador')
        num_digito_verificador.send_keys('67')
        num_processo_ano = driver.find_element_by_id('fPP:numeroProcesso:Ano')
        num_processo_ano.send_keys('2017')
        num_orgao_justica = driver.find_element_by_id('fPP:numeroProcesso:NumeroOrgaoJustica')
        num_orgao_justica.send_keys('5004')
        submete_pesquisa = driver.find_element_by_id('fPP:searchProcessos')
        submete_pesquisa.click()
        wait.until(EC.visibility_of_element_located((By.ID, '0821120-67.2017.8.20.5004')))
        end = time.time()
        tempo_pesquisa = end - start
        zbx_enviar('PJe 1Grau', 'tempo_pesquisa', tempo_pesquisa)
        logging.info("Tempo pesquisa PJe 1Grau: " + str(tempo_pesquisa))

    except Exception:
        zbx_enviar('PJe 1Grau', 'tempo_pesquisa', 0)
        logging.error("Pesquisa PJe 1Grau falhou.")

    try:
        # Logout
        start = time.time()
        logout = driver.find_element_by_id('desconectar')
        logout.click()
        wait.until(EC.visibility_of_element_located((By.ID, 'username')))
        end = time.time()
        tempo_logout = end - start
        zbx_enviar('PJe 1Grau', 'tempo_logout', tempo_logout)
        logging.info('Tempo logout PJe 1Grau: ' + str(tempo_logout))
        driver.quit()

    except Exception:
        zbx_enviar('PJe 1Grau', 'tempo_logout', 0)
        logging.error("Logout PJe 1Grau falhou.")
        driver.quit()


def pje2g():
    driver = setup()
    wait = WebDriverWait(driver, 10)
    config = configparser.ConfigParser()
    config.read('maeve.conf')
    usuario = config.get('PJe2G', 'usuario')
    senha = config.get('PJe2G', 'senha')
    url = config.get('PJe2G', 'url')

    try:
        # Login
        start = time.time()
        driver.get(url)
        user = driver.find_element_by_id('username')
        user.send_keys(usuario)
        password = driver.find_element_by_id('password')
        password.send_keys(senha)
        password.submit()

        # Verifica se logou
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'usuario-logado')))
        end = time.time()
        tempo_login = end - start
        zbx_enviar('PJe 2Grau','tempo_login', tempo_login)
        logging.info('Tempo login PJe 2Grau: ' + str(tempo_login))

    except Exception:
        zbx_enviar('PJe 2Grau', 'tempo_login', 0)
        zbx_enviar('PJe 2Grau', 'tempo_logout', 0)
        zbx_enviar('PJe 2Grau', 'tempo_pesquisa', 0)
        logging.error("Login PJe 2Grau falhou.")
        driver.quit()

    try:
        # Pesquisa
        start = time.time()

        # Navegação no menu para entrar na pesquisa
        menu_processo = wait.until(EC.visibility_of_element_located((By.ID, '_1007_j_id70j_id71')))
        ActionChains(driver).move_to_element(menu_processo).perform()
        menu_pesquisar_n1 = wait.until(EC.visibility_of_element_located((By.ID, '_1008_j_id70j_id75')))
        ActionChains(driver).move_to_element(menu_pesquisar_n1).perform()
        menu_pesquisar_n2 = wait.until(EC.visibility_of_element_located((By.ID, '_1009_j_id70j_id76')))
        ActionChains(driver).move_to_element(menu_pesquisar_n2).click().perform()
        wait.until(EC.visibility_of_element_located((By.ID, 'fPP:consultaSearchFields_header')))


        # Preenchimento do formulário de pesquisa
        num_sequencial = driver.find_element_by_id('fPP:numeroProcesso:numeroSequencial')
        num_sequencial.send_keys('0800754')
        num_digito_verificador = driver.find_element_by_id('fPP:numeroProcesso:numeroDigitoVerificador')
        num_digito_verificador.send_keys('89')
        num_processo_ano = driver.find_element_by_id('fPP:numeroProcesso:Ano')
        num_processo_ano.send_keys('2017')
        num_orgao_justica = driver.find_element_by_id('fPP:numeroProcesso:NumeroOrgaoJustica')
        num_orgao_justica.send_keys('5106')
        submete_pesquisa = driver.find_element_by_id('fPP:searchProcessos')
        submete_pesquisa.click()
        wait.until(EC.visibility_of_element_located((By.ID, '0800754-89.2017.8.20.5106')))
        end = time.time()
        tempo_pesquisa = end - start
        zbx_enviar('PJe 2Grau', 'tempo_pesquisa', tempo_pesquisa)
        logging.info("Tempo pesquisa PJe 2Grau: " + str(tempo_pesquisa))

    except Exception:
        zbx_enviar('PJe 2Grau', 'tempo_pesquisa', 0)
        logging.error("Pesquisa PJe 2Grau falhou.")

    try:
        # Logout
        start = time.time()
        logout = driver.find_element_by_id('desconectar')
        logout.click()
        wait.until(EC.visibility_of_element_located((By.ID, 'username')))
        end = time.time()
        tempo_logout = end - start
        zbx_enviar('PJe 2Grau', 'tempo_logout', tempo_logout)
        logging.info('Tempo logout PJe 2Grau: ' + str(tempo_logout))
        driver.quit()

    except Exception:
        zbx_enviar('PJe 2Grau', 'tempo_logout', 0)
        logging.error("Logout PJe 2Grau falhou.")
        driver.quit()


def correicao():
    driver = setup()
    wait = WebDriverWait(driver, 10)
    config = configparser.ConfigParser()
    config.read('maeve.conf')
    usuario = config.get('Correicao', 'usuario')
    senha = config.get('Correicao', 'senha')
    url = config.get('Correicao', 'url')

    try:
        start = time.time()
        driver.get(url)
        user = driver.find_element_by_id('username')
        user.send_keys(usuario)
        password = driver.find_element_by_id('password')
        password.send_keys(senha)
        password.submit()

        wait.until(EC.visibility_of_element_located((By.ID, 'minutes_left')))
        end = time.time()
        tempo_login = end - start
        zbx_enviar('Correicao Virtual', 'tempo_login', tempo_login)
        logging.info('Tempo login Correição: ' + str(tempo_login))

    except Exception:
        zbx_enviar('Correicao Virtual', 'tempo_login', 0)
        zbx_enviar('Correicao Virtual', 'tempo_logout', 0)
        logging.error("O login Correicao falhou.")
        driver.quit()

    try:
        # Logout
        start = time.time()
        logout = driver.find_element_by_partial_link_text('Logout')
        logout.click()
        wait.until(EC.visibility_of_element_located((By.ID, 'username')))
        end = time.time()
        tempo_logout = end - start
        zbx_enviar('Correicao Virtual', 'tempo_logout', tempo_logout)
        logging.info('Tempo logout Correicao: ' + str(tempo_logout))
        driver.quit()

    except Exception:
        zbx_enviar('Correicao Virtual', 'tempo_logout', 0)
        logging.error("O logout Correicao falhou.")
        driver.quit()


def main():
    try:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        pje1g()
        pje2g()
        correicao()
        return 0

    except Exception:
        logging.error("Não foi possível executar os testes, verifique o log.")
        return 1


if __name__ == '__main__':
    exit(main())
