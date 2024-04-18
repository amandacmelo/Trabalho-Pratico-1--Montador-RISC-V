
#Importar o módulo sys.
#OBS.: O módulo sys fornece acesso a algumas variáveis usadas ou mantidas pelo interpretador Python e a funções que interagem fortemente com o interpretador.
#Neste código em específico: sys.argv, que contém os argumentos de linha de comando passados para o script.
import sys

# Função para calcular o complemento de dois de um número decimal e usada para tipo de instruções que possuem imediatos
def complemento_de_dois(numero):
    if numero >= 0: # Se o número for positivo o seu complemento é apenas seu valor em binário
        complemento = bin(numero)[2:].zfill(12)  # Converte para binário e preenche com zeros à esquerda para ter 12 bits
    else:
        numero = numero * (-1)  # Transforma número negativo em positivo
        numero_binario = bin(numero)[2:].zfill(12)  # Converte para binário e preenche com zeros à esquerda para ter 12 bits
        binario_invertido = numero_binario.replace('0', '.').replace('1', '0').replace('.', '1')  # Inverte os bits
        complemento = bin(int(binario_invertido, 2) + 1)[2:]  # Adiciona 1 ao número invertido para obter o complemento de dois
    return complemento

# Função para converter um número decimal para binário com um número específico de bits;
# É usada para converter os valores dos registradores, recebe dois parâmetros para que os registradores possam ter 5 bits
def decimal_binario(numero, bits):
    numero_binario = bin(numero)[2:].zfill(bits)  # Converte para binário e preenche com zeros à esquerda para ter o número especificado de bits
    return numero_binario

# Função que retorna o código de operação (opcode) com base no tipo de instrução
def opcode(instrucao):
    valor_opcode = {'r': '0110011', 's': '0100011', 'sb' : '1100011', 'i' : '0010011', 'i-1' :'0000011'} 
    return valor_opcode[instrucao]

# Função que retorna o campo funct3 com base no tipo de instrução
def funct3(instrucao):
    valor_funct3 = {'add': '000', 'addi': '000', 'and': '111', 'andi': '111',
                     'beq': '000', 'bge': '101', 'bne': '001',
                     'lw': '010', 'or': '110', 'ori': '110',
                     'sb': '000', 'sh': '001', 'sll': '001', 'srl': '101',
                     'sub': '000', 'sw': '010', 'xor': '100', 'xori': '100',
                     'li': '000', 'mv': '000', 'not': '100', 'neg': '000'}
    return valor_funct3[instrucao]

# Função para montar a linha de instrução do assembly para linguagem de máquina EX: add, x2, x0, x1
def montar_linha(elementos):

    instrucao = elementos[0]  # Pega a instrução
    rd = elementos[1][1:]  # Remove o 'x' do registrador de destino
    r1 = elementos[2][1:]  # Remove o 'x' do registrador r1
    linha = ''
# Comandos para montar a linha de cada tipo de instrução de acordo com suas particularidades
#As quatro primeiras são pseudo-instruções
    if instrucao == 'li':
        # Pseudo-instrução 'li' é equivalente a 'addi rd, x0, imediato'
        imediato = complemento_de_dois(int(elementos[2]) ) # Valor imediato
        r1 = 0
        tipo_instrucao = 'i'
        linha = (imediato + decimal_binario(r1, 5) + funct3(instrucao) + decimal_binario(int(rd), 5) + opcode(tipo_instrucao))

    elif instrucao == 'mv':
        # Pseudo-instrução 'mv' é equivalente a 'addi rd, r1, 0'
        tipo_instrucao = 'i'
        imediato = complemento_de_dois(0)
        linha = (imediato + decimal_binario(int(r1), 5) + funct3(instrucao) + decimal_binario(int(rd), 5) + opcode(tipo_instrucao))

    elif instrucao == 'not':
        # Pseudo-instrução 'not' é equivalente a 'xori rd, r1, -1'
        tipo_instrucao = 'i'
        imediato = complemento_de_dois(-1)
        linha = (imediato + decimal_binario(int(r1), 5) + funct3(instrucao) + decimal_binario(int(rd), 5) + opcode(tipo_instrucao))

    elif instrucao == 'neg':
        # Pseudo-instrução 'neg' é equivalente a 'sub rd, x0, r1'
        tipo_instrucao = 'r'
        funct7 = '0100000'
        r2 = 0
        linha = (funct7 + decimal_binario(int(r1), 5) + decimal_binario(r2, 5) + funct3(instrucao)  + decimal_binario(int(rd), 5) + opcode(tipo_instrucao))

    elif instrucao in ['add', 'xor', 'sll', 'or', 'sub', 'srl', 'and']:  # Instruções do tipo 'r'
        tipo_instrucao = 'r'
        funct7 = '0000000'
        r2 = elementos[3][1:]  # Remove o 'x' do registrador r2
        if instrucao == 'sub':
            funct7= '0100000'  # Funct7 específico para a subtração (sub)
        linha = (funct7 + decimal_binario(int(r2), 5) + decimal_binario(int(r1), 5) + funct3(instrucao) +  decimal_binario(int(rd), 5) + opcode(tipo_instrucao))

    elif instrucao in [ 'bne', 'beq', 'bge']:  # Instruções do tipo 'sb'
        tipo_instrucao = 'sb'
        imediato = complemento_de_dois(int(elementos[-1]))  # Calcula o complemento de dois do valor imediato
        linha = (imediato[0] + imediato[1:7] + decimal_binario(int(r1), 5) + decimal_binario(int(rd), 5) + funct3(instrucao) + imediato[7:11] + imediato[-1] + opcode(tipo_instrucao))

    elif instrucao in ['sw', 'sb', 'sh']:  # Instruções do tipo 's'
        tipo_instrucao = 's'
        imediato = complemento_de_dois(int(elementos[2].split('(')[0]))  # Extrai o deslocamento e calcula o complemento de dois
        r1 = elementos[2].split('(')[1][1:-1]  # Extrai o registrador de origem base
        linha = (imediato[:7]+ decimal_binario(int(rd), 5) + decimal_binario(int(r1), 5 ) +  funct3(instrucao) + imediato[-5:] + opcode(tipo_instrucao)) 

    elif instrucao in ['addi', 'ori', 'andi', 'lw', 'lb', 'lh', 'xori']:  # Instruções do tipo 'i' 
        tipo_instrucao = 'i'
        if instrucao in ['addi', 'ori', 'andi', 'xori']:  # Instruções do tipo 'i'
            imediato = complemento_de_dois(int(elementos[-1]))  # Calcula o complemento de dois do valor imediato
            linha = (imediato + decimal_binario(int(r1), 5) + funct3(instrucao) + decimal_binario(int(rd), 5) + opcode(tipo_instrucao))

        #Como a instrução tipo i possui dois tipos diferentes de opcode, criamos dois para diferenciar
        elif instrucao in ['lw', 'lb', 'lh']:  # Instruções do tipo 'i-1'
            tipo_instrucao = 'i-1'
            imediato = complemento_de_dois(int(elementos[2].split('(')[0]))  # Extrai o deslocamento e calcula o complemento de dois ignorando os parênteses 
            r1 = elementos[2].split('(')[1][1:-1]  # Extrai o registrador ignorando os parênteses 
            linha = ( imediato + decimal_binario(int(r1), 5) +  funct3(instrucao) + decimal_binario(int(rd), 5) + opcode(tipo_instrucao))
           
    else:
        print("Instrução não reconhecida:", instrucao)  # Mensagem de erro para instruções não reconhecidas

    return linha

# Função principal
def main():
    tipo_saida = "indefinido"
    if len(sys.argv) == 2:  # Verifica se apenas o arquivo de entrada foi fornecido
        tipo_saida = "terminal"
    elif len(sys.argv) == 4 and sys.argv[2] == "-o":  # Verifica se o arquivo de entrada e a opção de saída foram fornecidos
        tipo_saida = "arquivo"
    else:
        print("Comando errado")  # Mensagem de erro para formato de comando incorreto
        exit()

    try:
        arquivo_entrada = open(sys.argv[1], "r")  # Abre o arquivo de entrada
    except FileNotFoundError:
        print("Arquivo não foi encontrado")  # Mensagem de erro para arquivo de entrada não encontrado
        exit()

    if tipo_saida == "arquivo":
        try:
            arquivo_saida = open(sys.argv[3], "w")  # Abre o arquivo de saída se a opção for especificada
        except:
            print("Não foi possível abrir o arquivo de saída")  # Mensagem de erro para falha ao abrir o arquivo de saída
            exit()

    comandos = arquivo_entrada.readlines()  # Lê todas as linhas do arquivo de entrada

    for linha in comandos:
        if not linha.strip():
            continue  # Ignora linhas em branco

        elementos = linha.strip().replace(',', '').split()  # Remove espaços em branco, vírgulas e divide a linha em elementos
        linha_montada = montar_linha(elementos)  # Monta a linha de instrução

        if tipo_saida == "terminal":
            print(linha_montada)  # Imprime a linha de instrução no terminal
        elif tipo_saida == "arquivo":
            arquivo_saida.write(linha_montada + "\n")  # Escreve a linha de instrução no arquivo de saída

    arquivo_entrada.close()  # Fecha o arquivo de entrada
    if tipo_saida == "arquivo":
        arquivo_saida.close()  # Fecha o arquivo de saída

if __name__ == "__main__":
    main()





