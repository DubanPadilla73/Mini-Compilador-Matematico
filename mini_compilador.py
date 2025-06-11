import re

variables = {}  # Diccionario para guardar las variables

# Tokenizacion: sacar numeros, variables, operadores, simbolos.


def tokenizador(expresion):

    # definimos el patron de los tokens
    patron = r'\d+\.\d+|\d+|[a-zA-Z_][a-zA-Z0-9_]*|[\+\-\*\/\^]|=|\(|\)'
    tokens = re.findall(patron, expresion)
    return tokens

# Asignaciones y entorno de variables.


def reemplazar_variables(tokens):
    resultado = []
    for token in tokens:
        if token in variables:
            resultado.append(variables[token])
        else:
            resultado.append(token)
    return resultado


def evaluar(tokens):
    expresion_string = ''.join(tokens)
    expresion_string = expresion_string.replace(
        '^', '**')  # Reemplazar ^ por ** para potencia
    try:
        resultado = eval(expresion_string)
        return resultado
    except Exception as e:
        print(f"Error al evaluar la expresión: {expresion_string}")
        return None


def procesar_linea(entrada):
    tokens = tokenizador(entrada)
    if '=' in tokens:
        # Asignación
        nombre_variable = tokens[0]
        expresion = tokens[2:]  # lo que viene después del igual
        expresion_con_valor = reemplazar_variables(expresion)
        print("Evaluando:", ' '.join(expresion_con_valor))
        resultado = evaluar(expresion_con_valor)
        if resultado is not None:
            variables[nombre_variable] = resultado
            print(f"Asignado: {nombre_variable} = {resultado}")
            print("Variables actuales:", variables)
    else:
        # Evaluación
        expresion = tokens
        expresion_con_valor = reemplazar_variables(expresion)
        resultado = evaluar(expresion_con_valor)
        print(f"Resultado: {resultado}")
