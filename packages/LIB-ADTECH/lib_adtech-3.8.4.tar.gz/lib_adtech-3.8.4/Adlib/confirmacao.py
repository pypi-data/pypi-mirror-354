from selenium.webdriver import Chrome
from .api import EnumBanco
from .logins import loginVirtaus
from .virtaus import importarArquivos
from .funcoes import setupDriver, getCredenciais


def confirmacaoCredito(driver: Chrome, user: str, senha: str, codigoLoja: str, nomeProduto: str, filePaths: list[str], enumBanco: EnumBanco, subPastaRede: str):

    loginVirtaus(driver, user, senha)
    importarArquivos(driver, enumBanco, codigoLoja, nomeProduto, filePaths, subPastaRede)


if __name__ == '__main__':

    virtaus = setupDriver(webdrivePath=r"C:\Users\dannilo.costa\Documents\chromedriver.exe")
    
    userVirtaus, senhaVirtaus = getCredenciais(168)
    usuarioWindows = "dannilo.costa"
    nomeBanco = "Pan"
    codigoPasta = 1836846
    substring = "teste"
    extensao = "pdf"

    loginVirtaus(virtaus, userVirtaus, senhaVirtaus)
    importarArquivos(virtaus, EnumBanco.PAN, codigoPasta, nomeBanco, substring, extensao, usuarioWindows)