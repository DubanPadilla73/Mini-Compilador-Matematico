import re  # Librería para expresiones regulares

variables = {}  # Diccionario para guardar las variables

# TOKENIZADOR: sacar numeros, variables, operadores, simbolos.


def tokenizador(expresion):
    # definimos el patron de los tokens
    patron = r'\d+\.\d+|\d+|[a-zA-Z_][a-zA-Z0-9_]*|[\+\-\*\/\^]|=|\(|\)'
    tokens = re.findall(patron, str(expresion))
    return tokens

# PARSER: Conversión de notación infija a posfija (Shunting Yard Algorithm)


def reemplazar_variables(tokens):
    resultado = []
    for token in tokens:
        if token in variables:
            # convertir a string para evitar errores de tipo
            resultado.append(str(variables[token]))
        else:
            resultado.append(token)
    return resultado


def procesar_linea(entrada):
    tokens = tokenizador(entrada)
    if '=' in tokens:
        # Asignación
        nombre_variable = tokens[0]
        expresion = tokens[2:]  # lo que viene después del igual
        expresion_con_valor = reemplazar_variables(expresion)
        resultado = evaluar(expresion_con_valor)
        if resultado is not None:
            variables[nombre_variable] = float(resultado)
        return expresion, resultado
    else:
        # Evaluación
        expresion_con_valor = reemplazar_variables(tokens)
        resultado = evaluar(expresion_con_valor)
    return tokens, resultado


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

# Conversion de notación infija a posfija (Shunting Yard Algorithm)


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
            while (pila and pila[-1] != "(" and papomudas(pila[-1]) >= papomudas(token)):
                salida.append(pila.pop())
            pila.append(token)
    while pila:
        salida.append(pila.pop())
    return salida

# Conversión de notación infija a prefija


def infija_a_prefija(tokens):
    tokens = tokens[::-1]  # Invertir la lista de tokens
    for i in range(len(tokens)):
        if tokens[i] == '(':
            tokens[i] = ')'
        elif tokens[i] == ')':
            tokens[i] = '('
    salida = infija_a_posfija(tokens)
    return salida[::-1]  # Invertir la salida para obtener la notación prefija

# EVALUADOR: Paso a paso


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


def paso_a_paso(posfija):
    pila = []

    for token in posfija:
        if re.match(r"\d+|\d+\.\d+", str(token)):  # Verifica si es un número
            pila.append(int(token))
        elif token in variables:
            pila.append((variables[token]))
            print(f"{token} = {variables[token]}")
        elif token in ["+", "-", "*", "/", "^"]:
            if len(pila) < 2:
                print("Error: No hay suficientes operandos en la pila.")
                return
            b = pila.pop()
            a = pila.pop()
            if token == "+":
                resultado = a + b
            elif token == "-":
                resultado = a - b
            elif token == "*":
                resultado = a * b
            elif token == "/":
                if b == 0:
                    print("División por cero.")
                resultado = a / b
            elif token == "^":
                resultado = a ** b
            print(f"{a} {token} {b} = {resultado}")
            pila.append(resultado)
        else:
            print(f"Token desconocido: {token}")
            return
    if len(pila) == 1:
        resultado_final = pila.pop()
    else:
        print("Error: La pila no tiene un único resultado al final.")
        return


def imprimir_variables(entrada):
    if not variables:
        print("No hay variables definidas.")
    elif entrada[0] in variables:
        print(f"Salida: {entrada[0]} = {variables[entrada[0]]}")
    contador = len(variables)
    if len(variables) > 0:
        print("Variables:", end=" {")
        for variable in variables:
            if contador > 1:
                print(f"{variable} : {variables[variable]}", end=", ")
            elif contador == 1:
                print(f"{variable} : {variables[variable]}", end="")
            contador -= 1
        print("}")


# Interfaz de usuario
activo = True

while activo:
    print("-"*5 + " Entrada " + "-"*5)
    entrada = str(input("Entrada: "))

    print("\n"+"-"*5 + " Salida " + "-"*5)
    print("Evaluacion paso a paso:\n")

    expresion, resultado = procesar_linea(entrada)
    posfija = infija_a_posfija(expresion)
    prefija = infija_a_prefija(expresion)

    paso_a_paso(posfija)

    imprimir_variables(entrada)

    print("\nPrefija:", " ".join(prefija))
    print("Postfija:", " ".join(posfija))
    print("\n")

    print("Desea continuar? (s/n): ")
    continuar = str(input()).lower()
    if continuar != 's':
        activo = False
        print("Saliendo del programa...")
