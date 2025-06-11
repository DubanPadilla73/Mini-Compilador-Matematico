import re

# Tokenizador: sacar numeros, variables, operadores, simbolos.


def tokenizador(expresion):

    # definimos el patron de los tokens
    patron = r'\d+\.\d+|\d+|[a-zA-Z_][a-zA-Z0-9_]*|[\+\-\*\/\^]|=|\(|\)'
    tokens = re.findall(patron, expresion)
    return tokens


expresion = "a = 3 + 5 * (2 - 8) / 4 ^ 2"
tokens = tokenizador(expresion)
print("Tokens:", tokens)

# Parsear: respetar la procedencia de operadores y paréntesis.
# Evaluacion: evaluar expresiones matemáticas.
# Asignacion: asignar valores a variables.
# Conversion a prefijo y posfijo.
