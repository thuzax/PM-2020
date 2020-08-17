import sys

import gerenciador_arquivo


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Execute o comando como abaixo:")
        print("python3 main.py <arquivo-de-entrada>")

    arquivo_entrada = sys.argv[1]


    vertices, matriz = gerenciador_arquivo.ler_arquivo(arquivo_entrada)

