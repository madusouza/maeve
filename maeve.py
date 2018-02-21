# encoding: utf-8
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyzabbix import ZabbixMetric, ZabbixSender
import configparser
import time
import platform


def setup():
    driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
    driver.set_window_size(1920, 1080)
    return driver


def screenshot(nome_arquivo,sistema):
    if platform.system() == 'Windows':
        path = 'screenshots\\' + sistema + '\\'
    else:
        path = 'screenshots/' + sistema + '/'

    data_hora = time.strftime('%Y-%m-%d_%H%M%S')
    arquivo_screenshot = path + nome_arquivo + '_' + data_hora + '.png'
    return arquivo_screenshot


def limpar_arquivos():
    pass


def zbx_enviar(host,chave,valor):
    metrics = []
    m = ZabbixMetric(host,chave,valor)
    metrics.append(m)
    zbx = ZabbixSender('t-kyoto')
    zbx.send(metrics)


def pje1g(usuario,senha,url_login):
    driver = setup()

    # Login
    start = time.time()
    driver.get(url_login)
    driver.save_screenshot(screenshot('pagina-login','pje1g'))
    user = driver.find_element_by_id('username')
    user.send_keys(usuario)
    password = driver.find_element_by_id('password')
    password.send_keys(senha)
    password.submit()

    try:
        # Verifica se logou
        driver.find_element_by_class_name('usuario-logado')
        end = time.time()
        tempo_login = end - start
        zbx_enviar('PJe 1Grau','tempo_login',tempo_login)
        print('Tempo login: ' + str(tempo_login))
        print(driver.current_url)

        try:
            start = time.time()
            wait = WebDriverWait(driver, 10)

            # Navegação no menu para entrar na pesquisa
            menu_processo = wait.until(EC.visibility_of_element_located((By.ID, '_1007_j_id70j_id71')))
            ActionChains(driver).move_to_element(menu_processo).perform()
            menu_pesquisar_n1 = wait.until(EC.visibility_of_element_located((By.ID, '_1008_j_id70j_id75')))
            ActionChains(driver).move_to_element(menu_pesquisar_n1).perform()
            menu_pesquisar_n2 = wait.until(EC.visibility_of_element_located((By.ID, '_1009_j_id70j_id76')))
            ActionChains(driver).move_to_element(menu_pesquisar_n2).click().perform()
            wait.until(EC.visibility_of_element_located((By.ID, 'fPP:consultaSearchFields_header')))
            # print("Estou na url %s" % (driver.current_url))

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
            print("Tempo pesquisa: " + str(tempo_pesquisa))

            # Logout
            start = time.time()
            logout = driver.find_element_by_id('desconectar')
            logout.click()
            end = time.time()
            tempo_logout = end - start
            zbx_enviar('PJe 1Grau', 'tempo_logout', tempo_logout)
            print('Tempo logout: ' + str(tempo_logout))

            driver.quit()

        except Exception:
            zbx_enviar('PJe 1Grau', 'tempo_pesquisa', 0)
            driver.save_screenshot(screenshot('pesquisa-falha','pje1g'))
            print("A pesquisa falhou.")
            driver.quit()

    except Exception:
        zbx_enviar('PJe 1Grau', 'tempo_login', 0)
        driver.save_screenshot(screenshot('login-falha','pje1g'))
        print("O login falhou.")
        driver.quit()


def main():
    try:
        credenciais = configparser.ConfigParser()
        credenciais.read('credenciais.conf')
        usuario = credenciais.get('Credenciais', 'usuario')
        senha = credenciais.get('Credenciais', 'senha')
        url_login = 'https://pje.tjrn.jus.br/pje1grau/'
        pje1g(usuario,senha,url_login)
        return 0

    except Exception:
        return 1


if __name__ == '__main__':
    exit(main())