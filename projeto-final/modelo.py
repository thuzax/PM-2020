import random

from gurobipy import *

M = 999999

def calc_dist(v1, v2):
    x_quadrado = v1.coord_x**2
    y_quadrado = v2.coord_y**2
    soma = x_quadrado + y_quadrado
    resultado = soma**(1/2)
    return resultado

def separa_conjuntos(vertices, veiculos):
    vertices_pickup = []
    vertices_delivery = []
    vertices_depoisto = []
    for key, vertice in vertices.items():
        if (vertice.e_deposito):
            vertices_depoisto.append(key)
            continue

        if (vertice.e_pickup):
            vertices_pickup.append(key)
            continue

        if (vertice.e_delivery):
            vertices_delivery.append(key)
            continue

    return (vertices_pickup, vertices_delivery, vertices_depoisto)

'''
Define os conjuntos de variáveis do modelo, retornando uma tupla com os vetores 
de cada conjunto.
'''
def declara_variaveis(modelo, vertices, veiculos):
    
    # Define x_ijk
    aresta_usada_por_veiculo = {}

    for key_1, vertice_1 in vertices.items():
        aresta_usada_por_veiculo[key_1] = {}
        for key_2, vertice_2 in vertices.items():
            aresta_usada_por_veiculo[key_1][key_2] = {}
            for veiculo in veiculos:
                nome_var = ""
                nome_var += "aresta_" 
                nome_var += str(key_1) 
                nome_var += "_" 
                nome_var += str(key_2) 
                nome_var += "_" 
                nome_var += str(veiculo)
                
                aresta_usada_por_veiculo[key_1][key_2][veiculo] = modelo.addVar(
                    name=nome_var,
                    # vtype=GRB.BINARY,
                    vtype=GRB.CONTINUOUS,
                    lb=0,
                    ub=1
                )

    # Define S_ik
    local_de_comeco_veiculo = {}

    for key in vertices.keys():
        local_de_comeco_veiculo[key] = {}
        for veiculo in veiculos:
            nome_var = ""
            nome_var += "local_inicio_"
            nome_var += str(key)
            nome_var += "_"
            nome_var += str(veiculo)

            local_de_comeco_veiculo[key][veiculo] = modelo.addVar(
                name=nome_var,
                # vtype=GRB.INTEGER,
                vtype=GRB.CONTINUOUS,
                lb=0
            )

    # Define L_ik
    ub_apos_servico = {}

    for key in vertices.keys():
        ub_apos_servico[key] = {}
        for veiculo in veiculos:
            nome_var = ""
            nome_var += "ub_apos_servico_"
            nome_var += str(key)
            nome_var += "_"
            nome_var += str(veiculo)


            ub_apos_servico[key][veiculo] = modelo.addVar(
                name=nome_var,
                # vtype=GRB.INTEGER,
                vtype=GRB.CONTINUOUS,
                lb=0
            )


    # Define z_i
    pedido_esta_no_banco = {}

    for key, vertice in vertices.items():
        if (vertice.e_pickup and not vertice.e_deposito):
            nome_var = ""
            nome_var = "pedido_no_banco_" + str(key)
            pedido_esta_no_banco[key] = modelo.addVar(
                name=nome_var,
                # vtype=GRB.BINARY,
                vtype=GRB.CONTINUOUS,
                lb=0,
                ub=1
            )
    
    conjunto_variaveis = (
        aresta_usada_por_veiculo, 
        local_de_comeco_veiculo, 
        ub_apos_servico, 
        pedido_esta_no_banco
    )
    
    return conjunto_variaveis


'''
Declara as restrições do Programa Linear e retorna uma tupla com os conjuntos.
'''
def declara_restricoes(modelo, vertices, matriz, veiculos, conjunto_variaveis):
    aresta_veic, local_ini_veic, ub_pos_serv, pedido_banco = conjunto_variaveis

    pickups, deliveries, depoistos = separa_conjuntos(vertices, veiculos)

    nao_forma_loop = {}
    for key in vertices.keys():
        nao_forma_loop[key] = {}
        for ind_veic in veiculos.keys():
            
            nome_rest = ""
            nome_rest += "nao_forma_loop_"
            nome_rest += str(key)
            nome_rest += "_"
            nome_rest += str(ind_veic)

            nao_forma_loop[key][ind_veic] = modelo.addConstr(
                aresta_veic[key][key][ind_veic],
                GRB.EQUAL,
                0,
                name=nome_rest
            )


    pickup_visitado_ou_banco = {}
    for key in pickups:
        vertice = vertices[key]
        soma = (
            quicksum(
                quicksum(
                    aresta_veic[key][key_2][veiculo]
                    for veiculo in veiculos.keys()
                )
                for key_2 in vertices.keys()
            ) 
            + pedido_banco[key]
        )
        nome_rest = ""
        nome_rest += "pickup_visitado_ou_banco_"
        nome_rest += str(key)
        pickup_visitado_ou_banco[key] = modelo.addConstr(
            soma,
            GRB.EQUAL,
            1,
            name=nome_rest
        )


    restricao_pick_delivery = {}

    for veiculo in veiculos.keys():
        restricao_pick_delivery[veiculo] = {}
        for key in pickups:
            soma_pickup = (
                quicksum(
                    aresta_veic[key][ind_vertice][veiculo]
                    for ind_vertice in vertices.keys()
                )
            )

            par_delivery = vertices[key].par_delivery
            soma_delivery = (
                quicksum(
                    aresta_veic[ind_vertice][par_delivery][veiculo]
                    for ind_vertice in vertices
                )
            )
            nome_rest = ""
            nome_rest = "pickup_delivery_"
            nome_rest += str(veiculo)
            nome_rest += "_"
            nome_rest += str(key)
            restricao_pick_delivery[veiculo][key] = modelo.addConstr(
                soma_pickup - soma_delivery,
                GRB.EQUAL,
                0,
                name=nome_rest
            )
    

    restricao_inicio_fim_pt_1 = {}
    for indice, veiculo in veiculos.items():
        vetor_percorrido = pickups + [veiculo.terminal_fim]
        soma = (
            quicksum(
                aresta_veic[veiculo.terminal_ini][j][indice]
                for j in vetor_percorrido
            )
        )
        
        nome_rest = "inicio_fim_pt_1_"
        nome_rest += str(indice)
        restricao_inicio_fim_pt_1[indice] = modelo.addConstr(
            soma,
            GRB.EQUAL,
            1,
            name=nome_rest
        )
    
    restricao_inicio_fim_pt_2 = {}
    for indice, veiculo in veiculos.items():
        vetor_percorrido = deliveries + [veiculo.terminal_ini]
        soma = (
            quicksum(
                aresta_veic[j][veiculo.terminal_fim][indice]
                for j in vetor_percorrido
            )
        )
        
        nome_rest = "inicio_fim_pt_2_"
        nome_rest += str(indice)
        restricao_inicio_fim_pt_2[indice] = modelo.addConstr(
            soma,
            GRB.EQUAL,
            1,
            name=nome_rest
        )

    caminhos_conexo = {}

    for ind_veiculo, veiculo in veiculos.items():
        for ind_vertice, vertice in vertices.items():
            if vertice.e_deposito:
                continue
            caminhos_conexo[ind_vertice] = {}
            soma_chegada = (
                quicksum(
                    aresta_veic[i][ind_vertice][ind_veiculo]
                    for i in vertices.keys()
                )
            )

            soma_saida = (
                quicksum(
                    aresta_veic[ind_vertice][i][ind_veiculo]
                    for i in vertices.keys()
                )
            )

            nome_rest = ""
            nome_rest += "caminho_conexo_"
            nome_rest += str(ind_vertice)
            nome_rest += "_"
            nome_rest += str(ind_veiculo)

            caminhos_conexo[ind_vertice][ind_veiculo] = modelo.addConstr(
                soma_chegada - soma_saida,
                GRB.EQUAL,
                0,
                name=nome_rest
            )


    define_local_ini_pt_1 = {}

    for ind_veiculo, veiculo in veiculos.items():
        define_local_ini_pt_1[ind_veiculo] = {}
        for i, v1 in vertices.items():
            define_local_ini_pt_1[ind_veiculo][i] = {}
            for j, v2 in vertices.items():
                soma_esquerda = (
                    local_ini_veic[i][ind_veiculo]
                    + v1.duracao_servico
                    + matriz[i][j]
                )


                soma_direita = (
                    (1 - aresta_veic[i][j][ind_veiculo])
                    * M
                    + local_ini_veic[j][ind_veiculo]
                )

                nome_rest = "define_local_ini_pt_1_"
                nome_rest += str(i)
                nome_rest += "_"
                nome_rest += str(j)
                nome_rest += "_"
                nome_rest += str(ind_veiculo)

                define_local_ini_pt_1[ind_veiculo][i][j] = modelo.addConstr(
                    soma_esquerda,
                    GRB.LESS_EQUAL,
                    soma_direita,
                    name=nome_rest
                )


    define_local_ini_pt_2 = {}

    for ind_veiculo in veiculos.keys():
        define_local_ini_pt_2[ind_veiculo] = {}
        for i, vertice in vertices.items():
            define_local_ini_pt_2[ind_veiculo][i] = {}


            nome_rest_0 = "ini_servico_0_"
            nome_rest_0 += str(ind_veiculo)
            nome_rest_0 += "_"
            nome_rest_0 += str(i)

            define_local_ini_pt_2[ind_veiculo][i][0] = modelo.addConstr(
                vertice.ini_janela,
                GRB.LESS_EQUAL,
                local_ini_veic[i][ind_veiculo],
                name=nome_rest_0
            )

            nome_rest_1 = "ini_servico_1_"
            nome_rest_1 += str(ind_veiculo)
            nome_rest_1 += "_"
            nome_rest_1 += str(i)

            define_local_ini_pt_2[ind_veiculo][i][1] = modelo.addConstr(
                local_ini_veic[i][ind_veiculo],
                GRB.LESS_EQUAL,
                vertice.fim_janela,
                name=nome_rest_1
            )

    pickup_antes_delivery = {}
    for ind_veiculo in veiculos.keys():
        pickup_antes_delivery[ind_veiculo] = {}
        for i in pickups:
            nome_rest = "pickup_antes_delivery_"
            nome_rest += str(i)
            nome_rest += "_"
            nome_rest += str(ind_veiculo)
            par_delivery = vertices[i].par_delivery
            pickup_antes_delivery[ind_veiculo][i] = modelo.addConstr(
                local_ini_veic[i][ind_veiculo],
                GRB.LESS_EQUAL,
                local_ini_veic[par_delivery][ind_veiculo],
                name=nome_rest
            )



    ub_correto_pt_1 = {}

    for ind_veiculo, veiculo in veiculos.items():
        ub_correto_pt_1[ind_veiculo] = {}
        for i, v1 in vertices.items():
            ub_correto_pt_1[ind_veiculo][i] = {}
            for j, v2 in vertices.items():
                soma_esquerda = (
                    ub_pos_serv[i][ind_veiculo]
                    + v2.demanda
                )

                soma_direita = (
                    (1 - aresta_veic[i][j][ind_veiculo])
                    * M
                    + ub_pos_serv[j][ind_veiculo]
                )

                nome_rest = "define_ub_correto_pt_1"
                nome_rest += str(ind_veiculo)
                nome_rest += "_"
                nome_rest += str(i)
                nome_rest += "_"
                nome_rest += str(j)

                ub_correto_pt_1[ind_veiculo][i][j] = modelo.addConstr(
                    soma_esquerda,
                    GRB.LESS_EQUAL,
                    soma_direita,
                    name=nome_rest
                )    



    ub_correto_pt_2 = {}

    for ind_veiculo in veiculos.keys():
        ub_correto_pt_2[ind_veiculo] = {}

        for i in vertices.keys():    
            nome_rest = ""
            nome_rest += "ub_correto_pt_2_"
            nome_rest += str(ind_veiculo)
            nome_rest += "_"
            nome_rest += str(i)

            ub_correto_pt_2[ind_veiculo][i] = modelo.addConstr(
                ub_pos_serv[i][ind_veiculo],
                GRB.LESS_EQUAL,
                veiculos[ind_veiculo].capacidade,
                name=nome_rest
            )

    ub_correto_pt_3 = {}
    for ind_veiculo, veiculo in veiculos.items():
        ub_correto_pt_3[ind_veiculo] = {}

        nome_rest_1 = ""
        nome_rest_1 += "ini_fim_demanda_0_"
        nome_rest_1 += str(ind_veiculo)

        ub_correto_pt_3[ind_veiculo][0] = modelo.addConstr(
            ub_pos_serv[veiculo.terminal_ini][ind_veiculo],
            GRB.EQUAL,
            0,
            name=nome_rest_1
        )

        nome_rest_2 = ""
        nome_rest_2 += "ini_fim_demanda_1_"
        nome_rest_2 += str(ind_veiculo)

        ub_correto_pt_3[ind_veiculo][1] = modelo.addConstr(
            ub_pos_serv[veiculo.terminal_fim][ind_veiculo],
            GRB.EQUAL,
            0,
            name=nome_rest_2
        )


def declara_restricoes_rota_trivial(
    modelo,
    ini_vertice, 
    fim_vertice, 
    veiculos, 
    arestas_veic
):
    n = min(len(veiculos)-1, fim_vertice-1)
    num_veic = random.randint(0, n)

    restricoes_rota_trivial = {}

    name_rest = ""
    name_rest += "rota_trivial_"
    name_rest += str(1)

    restricoes_rota_trivial[0] = modelo.addConstr(
        arestas_veic[ini_vertice][fim_vertice][num_veic],
        GRB.EQUAL,
        0,
        name=name_rest
    )


    name_rest = ""
    name_rest += "rota_trivial_"
    name_rest += str(2)
    restricoes_rota_trivial[1] = modelo.addConstr(
        arestas_veic[fim_vertice][ini_vertice][num_veic],
        GRB.EQUAL,
        0,
        name=name_rest
    ) 



def declara_funcao_objetivo(modelo, vertices, matriz, veiculos, conj_vars):
    arestas_veic, local_ini_veic, ub_pos_serv, pedido_banco = conj_vars
    pickups, deliveries, depoistos = separa_conjuntos(vertices, veiculos)


    soma_1 = (
        quicksum(
            quicksum(
                quicksum(
                    calc_dist(vertices[i], vertices[j]) * arestas_veic[i][j][k]
                    for j in vertices.keys()
                )
                for i in vertices.keys()
            )
            for k in veiculos.keys()
        )
    )

    soma_2 = (
        quicksum(
            local_ini_veic[veiculo.terminal_fim][k] 
            - vertices[veiculo.terminal_ini].ini_janela
            for k, veiculo in veiculos.items()
        )
    )

    soma_3 = (
        quicksum(
            pedido_banco[i]
            for i in pickups
        )
    )

    alfa = 1
    beta = 1
    lamb = 1000

    modelo.setObjective(
        (
            alfa * soma_1 
            + beta * soma_2 
            + lamb * soma_3
        ),
        GRB.MINIMIZE
    )


def cria_modelo(vertices, matriz, veiculos, time_limit):

    modelo = Model("modelo_pdjt")

    modelo.setParam("TimeLimit", time_limit)
    modelo.setParam("Threads", 6)

    conjunto_variaveis = declara_variaveis(modelo, vertices, veiculos.keys())

    declara_restricoes(modelo, vertices, matriz, veiculos, conjunto_variaveis)
    
    declara_funcao_objetivo(modelo, vertices, matriz, veiculos, 
                            conjunto_variaveis)

    modelo.write("teste_modelo.lp")


    return modelo


def cria_modelo_feasibility_pump(
        modelo_anterior, 
        solucao_int_anterior, 
        vertices, 
        matriz, 
        veiculos, 
        time_limit
):

    solucao_anterior = modelo_anterior.getVars()

    modelo = Model("modelo_feasibility_pump")
    modelo.setParam("TimeLimit", time_limit)
    modelo.setParam("Threads", 6)

    conj_vars = declara_variaveis(modelo, vertices, veiculos)
    arestas_veic, local_ini_veic, ub_pos_serv, pedido_banco = conj_vars


    soma = 0

    for i in range(len(solucao_anterior)):
        nome_var = solucao_anterior[i].varName
        if ("aresta" in nome_var):
            nome_var_separado = nome_var.split("_")
            v1 = int(nome_var_separado[1])
            v2 = int(nome_var_separado[2])
            veic = int(nome_var_separado[3])

            if (solucao_int_anterior[nome_var] == 0):
                soma += arestas_veic[v1][v2][veic]
            
            if (solucao_int_anterior[nome_var] == 1):
                soma += (1 - arestas_veic[v1][v2][veic])

            continue
        if ("local_inicio" in nome_var):
            continue
        if ("ub_apos_servico" in nome_var):
            continue
        if ("pedido_no_banco" in nome_var):
            nome_var_separado = nome_var.split("_")
            pos = int(nome_var_separado[-1])

            if (solucao_int_anterior[nome_var] == 0):
                soma += pedido_banco[pos]
            
            if (solucao_int_anterior[nome_var] == 1):
                soma += (1 - pedido_banco[pos])
            continue

    pickups, deliveries, depoistos = separa_conjuntos(vertices, veiculos)
    soma_2 = (
        quicksum(
            pedido_banco[i]
            for i in pickups
        )
    )

    soma_3 = (
        quicksum(
            quicksum(
                local_ini_veic[i][k]
                for k in veiculos.keys()
            )
            for i in vertices.keys()
        )
    )

    soma_4 = (
        quicksum(
            quicksum(
                ub_pos_serv[i][k]
                for k in veiculos.keys()
            )
            for i in vertices.keys()
        )
    )

    modelo.setObjective(
        (
            2*soma
            + 100*soma_3
            - 0.00001*soma_4
        ),
        GRB.MINIMIZE
    )


    declara_restricoes(modelo, vertices, matriz, veiculos, conj_vars)

    declara_restricoes_rota_trivial(
        modelo,
        vertices[0].idx, 
        vertices[vertices[0].par_delivery].idx, 
        veiculos, 
        arestas_veic
    )

    modelo.write("fp.lp")

    return modelo