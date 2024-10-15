import oracledb
import pandas as pd
import os
import json
from datetime import datetime


#         Tipo, Nome,     Preço por tonelada em real, faixa de umidade, faixa de temperatura e faixa de ph
milho  = (1,    "Milho",  1440.97,                    13.0, 14.1,       15.0, 25.1,            6.0, 7.6)
soja   = (2,    "Soja",   1784.67,                    11.0, 13.1,       15.0, 25.1,            6.0, 7.6)
arroz  = (3,    "Arroz",  1255.00,                    12.0, 14.1,       10.0, 25.1,            6.0, 7.1)
trigo  = (4,    "Trigo",  1432.76,                    12.0, 14.1,       10.0, 25.1,            5.5, 6.6)
feijao = (5,    "Feijão", 3103.00,                    11.0, 13.1,       15.0, 25.1,            5.8, 6.9)
#         0     1         2                           3     4           5     6                7    8
#         Posições dos valores na tupla
conectado = bool

conn = None

inst_cadastro = None
inst_consulta = None
inst_alteracao = None
inst_exclusao = None


def set_connection(usuario: str, senha: str) -> bool:
    global conn, conectado, inst_cadastro, inst_consulta, inst_alteracao, inst_exclusao
    try:
        conn = oracledb.connect(user=usuario, password=senha, dsn='oracle.fiap.com.br:1521/ORCL')

    except oracledb.DatabaseError as Error:
        print("Erro ao estabelcer conexão: " + str(Error))
        conectado = False
        return False

    except Exception as Error:
        print("Erro: " + str(Error))
        conectado = False
        return False
    
    else:
        conectado = True
        
        inst_cadastro = conn.cursor()
        inst_consulta = conn.cursor()
        inst_alteracao = conn.cursor()
        inst_exclusao = conn.cursor()
        return True

def close_connection():
    if conn:
        try:
            conn.close()
        except oracledb.DatabaseError as e:
            print(f"Erro ao fechar a conexão: {e}\n")

def insert(tipo: int, quantidade: float, silo_nome: str, endereco: str,
            capacidade: float, umidade: float, temperatura: float, ph: float, obs: str) -> bool:
    print("----- CADASTRAR SILO -----\n")
    try:
        with conn.cursor() as cursor:
            match tipo:
                case 1:
                    nome_produto = milho[1]
                case 2:
                    nome_produto = soja[1]
                case 3:
                    nome_produto = arroz[1]
                case 4:
                    nome_produto = trigo[1]
                case 5:
                    nome_produto = feijao[1]
                case _:
                    nome_produto = ''
            
            cadastro = f""" INSERT INTO SILOS(nome_produto, tipo_produto, quantidade, silo_nome,
                endereco, capacidade, data_hora_registro, umidade, temperatura, ph, observacoes) 
                VALUES(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11) """
            
            cursor.execute(cadastro, (nome_produto, tipo, quantidade, silo_nome, endereco, capacidade, 
                datetime.now(), umidade, temperatura, ph, obs))
            conn.commit()

    except oracledb.DatabaseError as Error:
        print(f"Erro ao gravar registro: {Error}")
        return False
    except Exception as Error:
        print(f"Erro inesperado: {Error}")
        return False
    else:
        print("Registro gravado com sucesso!")
        return True

"""
def insert(tipo: int, quantidade: float, silo_nome: str, endereco: str,
            capacidade: float, umidade: float, temperatura: float, ph: float, obs: str) -> bool:
        print("----- CADASTRAR SILO -----\n")

        global conectado, inst_cadastro, conn

        match tipo:
            case 1:
                nome_produto = milho[1]
            case 2:
                nome_produto = soja[1]
            case 3:
                nome_produto = arroz[1]
            case 4:
                nome_produto = trigo[1]
            case 5:
                nome_produto = feijao[1]
            case _:
                nome_produto = ''

        cadastro = f"" " INSERT INTO SILOS(nome_produto, tipo_produto, quantidade, silo_nome,
          endereco, capacidade, data_hora_registro, umidade, temperatura, ph, observacoes) 
          VALUES(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11) 
          "" "

        try:
            inst_cadastro.execute(cadastro, (nome_produto, tipo, quantidade, silo_nome, endereco, capacidade, 
                                         datetime.now(), umidade, temperatura, ph, obs))
            conn.commit()
        except oracledb.DatabaseError as Error:
            print("Erro ao gravar registro: " + str(Error))
            conectado = False
            return False
        except Exception as Error:
            print("Erro: " + str(Error))
            return False
        else:
            print("Registro gravado com sucesso!")
            return True
"""


def get_all() -> None:
    print("----- LISTAR SILOS -----\n")

    global conectado

    lista_silos = list()

    leitura = f""" SELECT * FROM SILOS """

    try:
        inst_consulta.execute(leitura)
        data = inst_consulta.fetchall()

        for dt in data:
            lista_silos.append(dt)

        #dados_df = pd.DataFrame.from_records(lista_silos, columns=['id', 'silo_nome'], index='id')
        dados_df = pd.DataFrame.from_records(lista_silos, columns=['id', 'nome_produto', 'tipo_produto', 'quantidade', 'silo_nome', 'endereco', 'capacidade', 'data_hora_registro', 'umidade', 'temperatura', 'ph', 'observacoes'], index='id')
    
    except oracledb.DatabaseError as Error:
        conectado = False
        print("Erro ao ler registros: " + str(Error))
    except Exception as Error:
        print("Erro: " + str(Error))
    else:
        if dados_df.empty:
            print(f"Não há registros")
        else:
            print(dados_df)

def get(id: int) -> list:

    global conectado

    lista_silos = list()

    leitura = f""" SELECT * FROM SILOS WHERE id = {id}"""

    try:
        inst_consulta.execute(leitura)
        data = inst_consulta.fetchall()

        for dt in data:
            lista_silos.append(dt)

        dados_df = pd.DataFrame.from_records(lista_silos, columns=['id', 'nome_produto', 'tipo_produto', 'quantidade', 'silo_nome', 'endereco', 'capacidade', 'data_hora_registro', 'umidade', 'temperatura', 'ph', 'observacoes'], index='id')
    
    except oracledb.DatabaseError as error:
        print("Erro ao ler registros: " + str(error))
        conectado = False
        return []
    except Exception as error:
        print("Erro: " + str(error))
        return []
    else:
        if dados_df.empty:
            print(f"Não há registros")
        else:
            linha = dados_df.iloc[0]
            cultura_escolhida = tuple()

            match linha.iloc[1]:
                case 1:
                    cultura_escolhida = milho
                case 2:
                    cultura_escolhida = soja
                case 3:
                    cultura_escolhida = arroz
                case 4:
                    cultura_escolhida = trigo
                case 5:
                    cultura_escolhida = feijao

            print(f""""
                Id: {id}
                Nome do Produto: {linha.iloc[0]}
                Tipo do Produto: {linha.iloc[1]}
                Quantidade: {linha.iloc[2]}
                Nome do Silo: {linha.iloc[3]}
                Endereço: {linha.iloc[4]}
                Capacidade: {linha.iloc[5]}
                Data e Hora de Registro: {linha.iloc[6]}
                Umidade: {linha.iloc[7]}
                Temperatura: {linha.iloc[8]}
                PH: {linha.iloc[9]}
                Observações: {linha.iloc[10]}
                Valor: {linha.iloc[2] * cultura_escolhida[2]}
            """)
            
            print("*** SITUAÇÃO DO SILO***")
            situacao = True
            
            umidade_arredondada = round(linha.iloc[7], 1)
            temperatura_arredondada = round(linha.iloc[8], 1)
            ph_arredondado = round(linha.iloc[9], 1)

            print("Situação da umidade: ", end="")
            if umidade_arredondada < cultura_escolhida[3] or umidade_arredondada > cultura_escolhida[4]:
                situacao = False
                if umidade_arredondada > cultura_escolhida[3]:
                    print("Anormal - Umidade acima do ideal - Pode causar mofo e deterioração dos grãos.")
                else:
                    print("Anormal - Umidade abaixo do ideal - Pode resultar em secagem excessiva e perda de qualidade.")
            else:
                print("Normal")

            print("Situação da temperatura: ", end="")
            if temperatura_arredondada < cultura_escolhida[5] or temperatura_arredondada > cultura_escolhida[6]:
                situacao = False
                if temperatura_arredondada > cultura_escolhida[5]:
                    print("Anormal - Temperatura acima do ideal - Pode levar ao crescimento de fungos e deterioração rápida dos produtos.")
                else:
                    print("Anormal - Temperatura abaixo do ideal - Pode resultar em dormência de sementes e redução na qualidade.")
            else:
                print("Normal")

            print("Situação do pH: ", end="")
            if ph_arredondado < cultura_escolhida[7] or ph_arredondado > cultura_escolhida[8]:
                situacao = False
                if ph_arredondado > cultura_escolhida[7]:
                    print("Anormal - pH acima do ideal - Pode causar toxicidade para as plantas e afetar a qualidade dos grãos.")
                else:
                    print("Anormal - pH abaixo do ideal - Pode resultar em deficiências nutricionais e prejudicar o desenvolvimento dos produtos.")
            else:
                print("Normal")

            if situacao:
                print("\nSituação geral: Normal")
            else:
                print("\nO silo apresenta condições anormais que podem afetar a qualidade dos grãos. É necessário verificar e ajustar os parâmetros!")

            return lista_silos

def delete(id: int) -> bool:
    print('----- APAGAR -----')
    try:
        with conn.cursor() as cursor:
            exclusao = f"DELETE FROM SILOS WHERE id = :1"
            cursor.execute(exclusao, (id,))
            conn.commit()

    except oracledb.DatabaseError as Error:
        print(f"Erro ao excluir: {Error}")
        return False
    except Exception as Error:
        print(f"Erro inesperado: {Error}")
        return False
    else:
        print("Registro apagado com sucesso!")
        return True


"""
def delete(id: int) -> bool:
        print('----- APAGAR -----')

        global conectado

        exclusao = f"" " DELETE FROM SILOS WHERE id = {id}"" "

        try:
            inst_exclusao.execute(exclusao)
            conn.commit()
        except oracledb.DatabaseError as Error:
            print("Erro ao excluir: " + str(Error))
            conectado = False
            return False
        except Exception as Error:
            print("Erro: " + str(Error))
            return False
        else:
            print("Apagado com sucesso")
            return True
"""


def get_id_nome() -> None:
    print("----- LISTAR SILOS -----\n")

    global conectado
    
    lista_silos = list()

    leitura = f""" SELECT id, silo_nome FROM SILOS """

    try:
        inst_consulta.execute(leitura)
        data = inst_consulta.fetchall()

        for dt in data:
            lista_silos.append(dt)

        dados_df = pd.DataFrame.from_records(lista_silos, columns=['id', 'silo_nome'], index='id')
       
    except oracledb.DatabaseError as Error:
        conectado = False
        print("Erro ao ler registros: " + str(Error))
    except Exception as Error:
        print("Erro: " + str(Error))
    else:
        if dados_df.empty:
            print(f"Não há registros")
        else:
            print(dados_df)

def update(dados_silo: list) -> bool:
    print("----- ALTERAR -----\n")
    try:
        with conn.cursor() as cursor:
            alteracao = f"""UPDATE SILOS SET nome_produto = :1, tipo_produto = :2, quantidade = :3, 
                silo_nome = :4, endereco = :5, capacidade = :6, umidade = :7, temperatura = :8, 
                ph = :9, observacoes = :10 WHERE id = :11"""
            
            match dados_silo[1]:
                case 1:
                    nome_produto = milho[1]
                case 2:
                    nome_produto = soja[1]
                case 3:
                    nome_produto = arroz[1]
                case 4:
                    nome_produto = trigo[1]
                case 5:
                    nome_produto = feijao[1]
                case _:
                    nome_produto = ''

            cursor.execute(alteracao, (nome_produto,  dados_silo[1], dados_silo[2], 
                                       dados_silo[3], dados_silo[4], dados_silo[5],
                                       dados_silo[6], dados_silo[7], dados_silo[8], 
                                       dados_silo[9], dados_silo[0]))
            conn.commit()

    except oracledb.DatabaseError as Error:
        print(f"Erro ao alterar registro: {Error}")
        return False
    except Exception as Error:
        print(f"Erro inesperado: {Error}")
        return False
    else:
        print("Registro alterado com sucesso!")
        return True


"""
def update(dados_silo: list) -> bool:
    global conectado
    try:
        print("----- ALTERAR -----\n")

        lista_dados = [] 

        consulta = f"" " SELECT * FROM SILOS WHERE id = {dados_silo[0]}"" "
        inst_consulta.execute(consulta)
        data = inst_consulta.fetchall()

        for dt in data:
            lista_dados.append(dt)

        if len(lista_dados) == 0: 
            print(f"Não existem silos com o ID = {dados_silo[0]}")
        else:

            alteracao = f"" " UPDATE SILOS
                SET nome_produto = {dados_silo[1]}, 
                tipo_produto = {dados_silo[2]}, 
                quantidade = {dados_silo[3]}, 
                silo_nome = {dados_silo[4]},
                endereco = {dados_silo[5]}, 
                capacidade = {dados_silo[6]},  
                umidade = {dados_silo[8]}, 
                temperatura = {dados_silo[9]}, 
                ph = {dados_silo[10]}, 
                observacoes = {dados_silo[11]}) 
                WHERE id = {dados_silo[0]}
                "" "
            inst_alteracao.execute(alteracao)
            conn.commit()
    except oracledb.DatabaseError as Error:
        print("Erro ao excluir: " + str(Error))
        return False
    except Exception as Error:
        print("Erro: " + str(Error))
        return False
    else:
        print("Alterado com sucesso")
        return True
"""

def gerar_relatorio() -> bool:
    def margem(i: int) -> str:
        retorno = "    "
        for i in range(0, i):
            retorno += "    "
        return retorno
    
    def obter_valor_por_tipo(tipo: int) -> float:
        valores_por_tipo = {
            1: 1440.97,  # Milho
            2: 1784.67,  # Soja
            3: 1255.00,  # Arroz
            4: 1432.76,  # Trigo
            5: 3103.00   # Feijão
        }
        return valores_por_tipo.get(tipo, 0)
    
    def condicao_adequada(tipo: int, valor: float, tipo_validacao:int):

        cultura_escolhida = tuple()

        match tipo:
            case 1:
                cultura_escolhida = milho
            case 2:
                cultura_escolhida = soja
            case 3:
                cultura_escolhida = arroz
            case 4:
                cultura_escolhida = trigo
            case 5:
                cultura_escolhida = feijao

        match tipo_validacao:
            case 1:
                return cultura_escolhida[3] <= valor <= cultura_escolhida[4]
            case 2:
                return cultura_escolhida[5] <= valor <= cultura_escolhida[6]
            case 3:
                return cultura_escolhida[7] <= valor <= cultura_escolhida[8]
            
    global conectado

    diretorio_raiz = os.path.dirname(os.path.abspath(__file__))
    caminho = os.path.join(diretorio_raiz, 'arquivos', 'relatorio.txt')
    try:
        with open(caminho, "w") as arq:
            arq.seek(0)
            texto = "Relatório dos silos: \n\n"
            
            texto += margem(0) + "* Listagem de silos:\n"

            lista_silos = list()
            leitura = "SELECT * FROM SILOS"

            try:

                inst_consulta.execute(leitura)
                data = inst_consulta.fetchall()

                for dt in data:
                    lista_silos.append(dt)


                dados_df = pd.DataFrame.from_records(lista_silos, columns=['id', 'nome_produto', 'tipo_produto', 'quantidade', 'silo_nome', 'endereco', 'capacidade', 'data_hora_registro', 'umidade', 'temperatura', 'ph', 'observacoes'], index='id')
    
                dados_df["valor_tonelada"] = dados_df["tipo_produto"].apply(obter_valor_por_tipo)
                dados_df["valor_total"] = dados_df["quantidade"] * dados_df["valor_tonelada"]
            except oracledb.DatabaseError as Error:
                print("Erro ao ler registros: " + str(Error))
                conectado = False
                return False
            except Exception as Error:
                print("Erro: " + str(Error))
                return False
            else:
                if dados_df.empty:
                    texto += "Não há registros no banco de dados"
                    arq.write(texto)
                    return True
                else:
                    texto += dados_df.to_string()
                    texto += "\n\n"

            texto += margem(0) + "* Valor total em mercadorias: " + str(dados_df["valor_total"].sum()) + "\n\n"

            texto += margem(0) + "* Silos com umidade inadequada:\n"

            for _, dado_df in dados_df.iterrows():
                if not condicao_adequada(dado_df["tipo_produto"], dado_df["quantidade"], 1):
                    texto += margem(1) + "* " + dado_df["silo_nome" + "\n"]
            texto += "\n\n"

            texto += margem(0) + "* Silos com temperatura inadequada:\n"

            for _, dado_df in dados_df.iterrows():
                if not condicao_adequada(dado_df["tipo_produto"], dado_df["quantidade"], 2):
                    texto += margem(1) + "* " + dado_df["silo_nome" + "\n"]
            texto += "\n\n"

            texto += margem(0) + "* Silos com pH inadequado:\n"

            for _, dado_df in dados_df.iterrows():
                if not condicao_adequada(dado_df["tipo_produto"], dado_df["quantidade"], 3):
                    texto += margem(1) + "* " + dado_df["silo_nome" + "\n"]
            texto += "\n\n"
            

            arq.write(texto)

    except FileNotFoundError as e:
        print(f"Arquivo não encontrado: {e}")
        return False
    except IOError as e:
        print(f"Erro de entrada/saída: {e}")
        return False
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return False

def backup():
    """
    global conectado
    try:
        diretorio_raiz = os.path.dirname(os.path.abspath(__file__))
        caminho = os.path.join(diretorio_raiz, 'arquivos', 'relatorio.txt')

        lista_silos = list()

        consulta = "SELECT * FROM SILOS"
        inst_consulta.execute(consulta)
        data = inst_consulta.fetchall()

        dados_df = pd.DataFrame.from_records(data, columns=['id', 'nome_produto', 'tipo_produto', 'quantidade', 'silo_nome', 'endereco', 'capacidade', 'data_hora_registro', 'umidade', 'temperatura', 'ph', 'observacoes'], index='id')
    except oracledb.DatabaseError as e:
        print("Erro ao acessar o banco de dados:", e)
        conectado = False
    except Exception as e:
        print("Erro inesperado:", e)
    else:
        dict_silos = dict()

        dict_silos = dados_df.to_dict(orient='index')

        with open(caminho, "w") as arq:
            

def backup():
    global conectado
    try:

        consulta = "SELECT * FROM SILOS"
        inst_consulta.execute(consulta)
        registros = inst_consulta.fetchall()

        colunas = [desc[0] for desc in inst_consulta.description]

        lista_dicionarios = []
        for registro in registros:
            # Crie um dicionário para cada registro
            dicionario = dict(zip(colunas, registro))
            
            # Converte os campos datetime para strings
            for chave, valor in dicionario.items():
                if isinstance(valor, datetime):
                    dicionario[chave] = valor.isoformat()  # Converte datetime para string

            lista_dicionarios.append(dicionario)

        diretorio_raiz = os.path.dirname(os.path.abspath(__file__))
        caminho = os.path.join(diretorio_raiz, 'arquivos', 'backup.json')

        with open(caminho, "w") as arquivo_json:
            json.dump(lista_dicionarios, arquivo_json, indent=4)

        print("Dados salvos com sucesso em", caminho)

    except oracledb.DatabaseError as e:
        print("Erro ao acessar o banco de dados:", e)
        conectado = False
    except Exception as e:
        print("Erro inesperado:", e)""""""

def restaurar_backup():
    print("----- RESTAURAR BACKUP -----\n")
    try:
        diretorio_raiz = os.path.dirname(os.path.abspath(__file__))
        caminho = os.path.join(diretorio_raiz, 'arquivos', 'backup.json')

        with open(caminho, "r") as arquivo_json:
            lista_dicionarios = json.load(arquivo_json)

        with conn.cursor() as cursor:
            for registro in lista_dicionarios:
                consulta = f"" "
                INSERT INTO SILOS (id, nome_produto, tipo_produto, quantidade, silo_nome, endereco, capacidade, 
                data_hora_registro, umidade, temperatura, ph, observacoes)
                VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)"" "
                
                cursor.execute(consulta, (registro['id'], registro['nome_produto'], registro['tipo_produto'], 
                                          registro['quantidade'], registro['silo_nome'], registro['endereco'], 
                                          registro['capacidade'], registro['data_hora_registro'], 
                                          registro['umidade'], registro['temperatura'], registro['ph'], 
                                          registro['observacoes']))
            conn.commit()

        print("Backup restaurado com sucesso!")

    except FileNotFoundError:
        print("Arquivo de backup não encontrado.")
    except oracledb.DatabaseError as e:
        print(f"Erro ao acessar o banco de dados: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
"""

def restaurar_backup():
    """
    global conectado
    try:
        diretorio_raiz = os.path.dirname(os.path.abspath(__file__))
        caminho = os.path.join(diretorio_raiz, 'arquivos', 'backup.json')

        with open(caminho, "r") as arquivo_json:
            lista_dicionarios = json.load(arquivo_json)

        for registro in lista_dicionarios:
            consulta = f"" "
            INSERT INTO SILOS (id, nome_produto, tipo_produto, quantidade, silo_nome, endereco, capacidade,
            data_hora_registro, umidade, temperatura, ph, observacoes)
            VALUES ({registro['id']}, '{registro['nome_produto']}', {registro['tipo_produto']},
            {registro['quantidade']}, '{registro['silo_nome']}',   '{registro['endereco']}',
            {registro['capacidade']}, '{registro['data_hora_registro']}',
            {registro['umidade']}, {registro['temperatura']}, {registro['ph']},
            '{registro['observacoes']}')
            "" "

            inst_consulta.execute(consulta)

        conn.commit()
        print("Backup restaurado com sucesso!")

    except FileNotFoundError:
        print("Arquivo de backup não encontrado.")
    except oracledb.DatabaseError as e:
        print("Erro ao acessar o banco de dados:", e)
        conectado = False
    except Exception as e:
        print("Erro inesperado:", e)
    """