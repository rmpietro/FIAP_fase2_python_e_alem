import os
import platform

def exibir_menu() -> None:
    print(
    """
    1 - Inserir
    2 - Ler Registro
    3 - Listar Todos
    4 - Alterar
    5 - Excluir
    6 - Gerar Relatório
    7 - Exportar Dados do Banco
    8 - Importar Dados para o Banco
    9 - Sair
    """    
    )

def limpar_console() -> None:
    sistema = platform.system()
    if sistema == "Windows":
        os.system("cls")
    elif sistema == "Linux" or sistema == "Darwin":
        os.system("clear")

def exibir_tipo() -> None:
    print("""
1 - Milho
2 - Soja
3 - Arroz
4 - Trigo
5 - Feijão
""")