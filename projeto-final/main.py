import sys

import gerenciador_arquivo

from modelo import *

from veiculo import Veiculo
from vertice import Vertice


def feasibility_pump(modelo, vertices, matriz, veiculos):
    modelo.optimize()

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

    print(modelo.getVars())




if __name__ == "__main__":
    if (len(sys.argv) < 3):
        print("Execute o comando como abaixo:")
        print("python3 main.py <arquivo-de-entrada> <numero-de-caminhoes>")

    arquivo_entrada = sys.argv[1]
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


    m = cria_modelo(vertices, matriz, veiculos)

    feasibility_pump(m, vertices,  matriz, veiculos)
