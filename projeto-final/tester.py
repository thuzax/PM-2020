import sys
import os

if __name__=="__main__":
    input_local = "./instancias/testes_projetos/"

    if (not os.path.exists(input_local)):
        print("INPUT FILE NOT FOUND")
        exit(0)

    test_files = os.popen("ls " + input_local).read().strip().splitlines()

    executer = "python3"

    executed_file = "main.py"

    number_of_trucks = "5"

    executed_commands = []
    final_results = []
    errors = []

    for test_file in test_files:
        command = ""
        command += executer + " " + executed_file + " "
        command += input_local + test_file + " " + number_of_trucks

        print(command)

        executed_commands.append(command)
        returned = os.popen(command).readlines()

        final_results.append(returned)

    text_errors = ""
    for error in errors:
        text_errors += error + "\n"

    with open("./tests_with_errors.txt", "w") as err_out:
        err_out.write(text_errors)