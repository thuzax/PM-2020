import sys
import time
import random
from operator import itemgetter 


import gerenciador_arquivo

from modelo import *

from veiculo import Veiculo
from vertice import Vertice

def somente_inteiros(vetor):
    for item in vetor:
        if (not item.x.is_integer()):
            return False
    return True


def time_out(time, time_limit):
    if (time >= time_limit):
        return True
    return False


def flip_pelo_intervalo(limite_inf, limite_sup, sol_int_anterior, sol_anterior):
    numero = random.randint(limite_inf, limite_sup)
    maiores = {}

    dic_valores = {}

    for v in sol_anterior:
        if ("pedido_no_banco" in v.varName):
            dic_valores[v.varName] = abs(v.x - sol_int_anterior[v.varName])
            continue
        if ("aresta" in v.varName):
            dic_valores[v.varName] = abs(v.x - sol_int_anterior[v.varName])
            continue
    
    
    res = sorted(
        dic_valores.items(), 
        key = itemgetter(1), 
        reverse = True
    )[:numero]
    for key, value in res:
        if ("pedido_no_banco" in v.varName):
            sol_int_anterior[key] = 1 - sol_int_anterior[key]
            continue
        if ("aresta" in v.varName):
            sol_int_anterior[key] = 1 - sol_int_anterior[key]
            continue
    


def perturbacao_ro(variaveis, solucao_int_anterior):
    for v in variaveis:
        if (
            not ("aresta" in v.varName) 
            and not ("pedido_no_banco") in v.varName
        ):
            continue

        x_estrela = v.x
        x_barra = solucao_int_anterior[v.varName]
        ro_aleatorio = random.randint(-3000, 7000)
        ro_aleatorio = ro_aleatorio/10000.0
        soma = (
            abs(x_estrela - x_barra) 
            + max(ro_aleatorio, 0)
        )
        if (soma > 0.5):
            solucao_int_anterior[v.varName] = 1 - x_barra

def add_solucao_detecta_loop(vetor_detecta_loop, solucao_int_anterior):
    set_loop = set()
    for key, value in solucao_int_anterior.items():
        set_loop.add((key, value))
    
    vetor_detecta_loop.append(set_loop)

def detecta_loop(vetor_detecta_loop, solucao_int_inicial):
    set_nova_sol = set()
    for key, value in solucao_int_inicial.items():
        set_nova_sol.add((key, value))
    
    if (set_nova_sol in vetor_detecta_loop):
        return True
    
    return False


def feasibility_pump(modelo, vertices, matriz, veiculos, time_limit):
    tempo_inicio = time.time()

    modelo.optimize()

    iteracao = 0
    texto = ""
    for v in modelo.getVars():
        texto += str(v.varName)
        texto += ": "
        texto += str(v.x)
        texto += "\n"

    texto += "obj: "
    texto += str(modelo.objVal)
    texto += "\n"

    with open("saida.txt", "w") as saida:
        saida.write(texto)

    solucao_int_anterior = {}

    for v in modelo.getVars():
        if ("aresta" in v.varName):
            solucao_int_anterior[v.varName] = round(v.x)
            continue
        if ("pedido_no_banco" in v.varName):
            solucao_int_anterior[v.varName] = round(v.x)
            continue

    numero_para_flip = int(len(solucao_int_anterior)/2)
    
    ultimo_viavel = modelo

    m = cria_modelo_feasibility_pump(
        modelo, 
        solucao_int_anterior, 
        vertices, 
        matriz, 
        veiculos,
        time_limit
    )

    vetor_detecta_loop = []
    tam_detecta_loop = 5
    add_solucao_detecta_loop(vetor_detecta_loop, solucao_int_anterior)

    m.optimize()

    print(GRB.OPTIMAL)

    tempo_atual = time.time()
    tempo = tempo_atual - tempo_inicio
    iteracao += 1
    factivel = somente_inteiros(m.getVars())
    while (
            GRB.OPTIMAL == 2
            and not factivel 
            and not time_out(tempo, time_limit)
    ):

        ultimo_viavel = m
        foi_diferente = False

        for v in modelo.getVars():
            arredondado = round(v.x)
            if (
                not ("aresta" in v.varName)
                and not ("pedido_no_banco" in v.varName)
            ):
                continue
            if (arredondado != solucao_int_anterior[v.varName]):
                solucao_int_anterior[v.varName] = arredondado
                foi_diferente = True

        tamanho = numero_para_flip
        if (foi_diferente):
            if (not detecta_loop(vetor_detecta_loop, solucao_int_anterior)):
                if (len(vetor_detecta_loop) > tam_detecta_loop):
                    vetor_detecta_loop.pop(0)
                add_solucao_detecta_loop(
                    vetor_detecta_loop, 
                    solucao_int_anterior
                )
            else:
                perturbacao_ro(m.getVars(), solucao_int_anterior)
        else:
            flip_pelo_intervalo(
                int(tamanho/2), 
                int(3*tamanho/2), 
                solucao_int_anterior, 
                modelo.getVars()
            )

        m = cria_modelo_feasibility_pump(
            modelo, 
            solucao_int_anterior, 
            vertices, 
            matriz, 
            veiculos,
            time_limit
        )

        m.optimize()
        
        iteracao += 1
        
        tempo_atual = time.time()
        print(tempo_atual)
        tempo = tempo_atual - tempo_inicio

        factivel = somente_inteiros(m.getVars())

    tempo_atual = time.time()
    tempo = tempo_atual - tempo_inicio

    texto = ""
    for v in m.getVars():
        texto += str(v.varName)
        texto += ": "
        texto += str(v.x)
        texto += "\n"

    texto += "obj: "
    texto += str(m.objVal)
    texto += "\n"

    with open("saida_fp.txt", "w") as saida:
        saida.write(texto)

    return (m.objVal, factivel, tempo)

if __name__ == "__main__":
    if (len(sys.argv) < 3):
        print("Execute o comando como abaixo:")
        print("python3 main.py <arquivo-de-entrada> <numero-de-caminhoes>")

    arquivo_entrada = sys.argv[1]
    arquivo_saida = arquivo_entrada.split(".")[0] + "-saida" + ".txt"
    num_caminhoes = int(sys.argv[2])


    dados, vertices, matriz = gerenciador_arquivo.ler_arquivo(arquivo_entrada)


    fake_vertice = Vertice(
        len(vertices), 
        vertices[0].coord_x, 
        vertices[0].coord_y, 
        vertices[0].demanda, 
        vertices[0].ini_janela, 
        vertices[0].fim_janela, 
        vertices[0].duracao_servico, 
        vertices[0].par_pickup, 
        vertices[0].par_delivery
    )
    fake_vertice.e_pickup = not vertices[0].e_pickup
    fake_vertice.e_delivery = not vertices[0].e_delivery
    fake_vertice.e_deposito = vertices[0].e_deposito

    vertices[0].par_delivery = len(vertices)

    vertices[fake_vertice.idx] = fake_vertice

    matriz.append([])
    for i in range(len(vertices)):
        matriz[-1].append(0)


    for i in range(len(vertices)):
        matriz[i].append(0)
    


    indices_veiculos = [i for i in range(num_caminhoes)]
    veiculos = {}
    for idx in indices_veiculos:
        veiculos[idx] = Veiculo(
            idx=idx,
            terminal_ini=0,
            terminal_fim=vertices[0].par_delivery,
            capacidade=dados["capacidade"]
        )


    time_limit = 25*60
    m = cria_modelo(vertices, matriz, veiculos, time_limit)

    resultado = feasibility_pump(m, vertices,  matriz, veiculos, time_limit)

    texto = ""
    texto += str(num_caminhoes)
    texto += "\n"
    texto += str(1) if resultado[1] else str(0)
    texto += "\n"
    texto += str(resultado[0])
    texto += "\n"
    texto += str(resultado[2])
    texto += "\n"

    with open(arquivo_saida, "w") as saida:
        saida.write(texto)


