from vertice import Vertice

def ler_arquivo(nome_arquivo_entrada):
    with open(nome_arquivo_entrada, "r") as arquivo:
        linhas = arquivo.read().splitlines()
        
        indice_linha = 0
        nome_instancia = linhas[indice_linha].split(" ")[1:]
        
        indice_linha += 1
        local = linhas[indice_linha].split(" ")[1:]
        
        indice_linha += 1
        comentario = linhas[indice_linha].split(" ")[1:]
        
        indice_linha += 1
        tipo = linhas[indice_linha].split(" ")[1:]
        
        indice_linha += 1
        tamanho = int(linhas[indice_linha].split(" ")[1])

        indice_linha += 1
        distribuicao = linhas[indice_linha].split(" ")[1:]

        indice_linha += 1
        escolha_deposito = linhas[indice_linha].split(" ")[1:]

        indice_linha += 1
        tempo_maximo = int(linhas[indice_linha].split(" ")[1])

        indice_linha += 1
        janela_tempo = int(linhas[indice_linha].split(" ")[1])

        indice_linha += 1
        capacidade = int(linhas[indice_linha].split(" ")[1])

        indice_linha += 1
        indice_linha += 1

        vertices = []

        inicio_loop = indice_linha
        fim_loop = tamanho + indice_linha

        for i in range(inicio_loop, fim_loop):
            linha = linhas[i].split()
            idx = int(linha[0])
            coord_x = float(linha[1])
            coord_y = float(linha[2])
            demanda = int(linha[3])
            ini_janela = int(linha[4])
            fim_janela = int(linha[5])
            duracao_servico = int(linha[6])
            par_pickup = int(linha[7])
            par_delivery = int(linha[8])
            
            vertice = Vertice(idx, coord_x, coord_y, demanda, ini_janela, 
                                fim_janela, duracao_servico, par_pickup, 
                                par_delivery)

            
            vertices.append(vertice)


        indice_linha += tamanho + 1

        matriz = []

        inicio_loop = indice_linha
        fim_loop = indice_linha + tamanho


        for i in range(inicio_loop, fim_loop):
            matriz.append([])
            linha = linhas[i]
            pesos = linha.split()
            for peso in pesos:
                matriz[i-inicio_loop].append(int(peso))
        
        return (vertices, matriz)