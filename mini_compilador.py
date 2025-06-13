import re  # Librería para expresiones regulares

variables = {}  # Diccionario para guardar las variables

# Tokenizacion: sacar numeros, variables, operadores, simbolos.


def tokenizador(expresion):

    # definimos el patron de los tokens
    patron = r'\d+\.\d+|\d+|[a-zA-Z_][a-zA-Z0-9_]*|[\+\-\*\/\^]|=|\(|\)'
    tokens = re.findall(patron, str(expresion))
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
        expresion_con_valor = reemplazar_variables(tokens)
        resultado = evaluar(expresion_con_valor)
        print(f"Resultado: {resultado}")
    return expresion


def papomudas(operador):
    if operador == '+':
        return 1
    elif operador == '-':
        return 1
    elif operador == '*':
        return 2
    elif operador == '/':
        return 2
    elif operador == '^':
        return 3
    else:
        return 0

# Conversión de notación infija a posfija (Shunting Yard Algorithm)


def infija_a_posfija(tokens):
    salida = []
    pila = []
    for token in tokens:
        # Si el token es un número o una variable, lo añadimos a la salida.
        # re.match() devuelve un objeto de coincidencia si el patrón coincide con el token
        if re.match(r'\d+|\d+\.\d+', token) or re.match(r'[a-zA-Z_][a-zA-Z0-9_]*', token):
            # append agrega el token al final de la lista
            salida.append(token)
        elif token == '(':
            pila.append(token)
        elif token == ')':
            # pop hasta encontrar el paréntesis de apertura
            while pila and pila[-1] != '(':
                # pop() elimina el último elemento de la lista y lo devuelve
                salida.append(pila.pop())
            pila.pop()  # Elimina el paréntesis de apertura
        else:  # Es un operador
            while (pila and pila[-1] != '(' and papomudas(pila[-1]) >= papomudas(token)):
                salida.append(pila.pop())
            pila.append(token)
    while pila:
        salida.append(pila.pop())
    return salida


# Ejemplo de uso
entrada = "x = (3 + 43) * 200 / (1 - 5) ^ 2 ^ 3"
tokens = tokenizador(entrada)
print("Tokens:", tokens)
expresion = tokenizador(procesar_linea(entrada))
posfija = infija_a_posfija(expresion)
print("Postfija:", ' '.join(posfija))
