import re

def analizador_lexico(codigo_fuente):
    tokens = []
    patron = re.compile(r'(Había una vez|brujas|pueblerinos|con|llegaron|partieron|transformaron|dividieron|y así termina|\d+|".*?")')
    coincidencias = patron.findall(codigo_fuente)
    for coincidencia in coincidencias:
        if coincidencia == "Había una vez":
            tokens.append(('PALABRA_CLAVE', coincidencia))
        elif re.match(r'\d+', coincidencia):
            tokens.append(('NUMERO', int(coincidencia)))
        elif re.search(r'"[^"]*"', coincidencia):
            tokens.append(('CADENA', coincidencia.strip('"')))
        else:
            tokens.append(('PALABRA_CLAVE', coincidencia))
    return tokens

def analizador_sintactico(tokens):
    i = 0
    arbol_sintactico = []
    variables = {
        "brujas": [],
        "brujas_llegaron": [],
        "brujas_partieron": [],
        "brujas_transformaron": [],
        "brujas_dividieron": []
    }
    estado = "inicio"

    if tokens[i][1] != "Había una vez":
        raise SyntaxError("Código debe empezar con 'Había una vez'")
    i += 1

    while i < len(tokens):
        if tokens[i][0] == 'NUMERO':
            if i + 1 < len(tokens) and tokens[i + 1][1] == "brujas":
                if estado == "inicio":
                    variables["brujas"].append(tokens[i][1])
                elif estado == "llegaron":
                    variables["brujas_llegaron"].append(tokens[i][1])
                elif estado == "partieron":
                    variables["brujas_partieron"].append(tokens[i][1])
                elif estado == "transformaron":
                    variables["brujas_transformaron"].append(tokens[i][1])
                elif estado == "dividieron":
                    variables["brujas_dividieron"].append(tokens[i][1])
                arbol_sintactico.append(('DECLARACION_ENTERO', tokens[i][1], "brujas"))
                i += 2
            else:
                raise SyntaxError("Esperado 'brujas' después de número")
        elif tokens[i][0] == 'CADENA':
            if i + 1 < len(tokens) and tokens[i + 1][1] == "pueblerinos":
                arbol_sintactico.append(('DECLARACION_CADENA', tokens[i][1], "pueblerinos"))
                i += 2
            else:
                raise SyntaxError("Esperado 'pueblerinos' después de cadena")
        elif tokens[i][1] == "llegaron":
            arbol_sintactico.append(('FUNCION_SUMAR', "llegaron"))
            estado = "llegaron"
            i += 1
        elif tokens[i][1] == "partieron":
            arbol_sintactico.append(('FUNCION_RESTAR', "partieron"))
            estado = "partieron"
            i += 1
        elif tokens[i][1] == "transformaron":
            arbol_sintactico.append(('FUNCION_MULTIPLICAR', "transformaron"))
            estado = "transformaron"
            i += 1
        elif tokens[i][1] == "dividieron":
            arbol_sintactico.append(('FUNCION_DIVIDIR', "dividieron"))
            estado = "dividieron"
            i += 1
        elif tokens[i][1] == "brujas":
            i += 1
        elif tokens[i][1] == "con":
            i += 1
        elif tokens[i][1] == "pueblerinos":
            i += 1
        elif tokens[i][1] == "y así termina":
            break
        else:
            raise SyntaxError(f"Palabra no esperada: {tokens[i][1]}")
    return arbol_sintactico, variables

def analizador_semantico(arbol_sintactico, variables):
    for nodo in arbol_sintactico:
        if len(nodo) > 2:
            if nodo[0] == 'DECLARACION_ENTERO' and nodo[2] == 'brujas':
                if nodo[1] < 0:
                    raise ValueError("El número de brujas no puede ser negativo")
            elif nodo[0] == 'FUNCION_DIVIDIR' and nodo[2] == 'brujas':
                for numero in variables['brujas']:
                    if numero == 0:
                        raise ZeroDivisionError("División por cero no permitida en el número de brujas")

def generador_codigo(arbol_sintactico, variables):
    codigo_ejecutable = []
    suma_brujas = sum(variables["brujas"])
    suma_llegaron = 0
    resta_partieron = 0

    for nodo in arbol_sintactico:
        if nodo[0] == 'DECLARACION_ENTERO':
            codigo_ejecutable.append(f"entero_{nodo[1]} = {nodo[1]}")
        elif nodo[0] == 'DECLARACION_CADENA':
            codigo_ejecutable.append(f"cadena = \"{nodo[1]}\"")
        elif nodo[0] == 'FUNCION_SUMAR':
            suma_llegaron = sum(variables["brujas_llegaron"])
            total_suma = suma_brujas + suma_llegaron
            codigo_ejecutable.append(f"suma_brujas = {suma_brujas}")
            suma_brujas = total_suma
        elif nodo[0] == 'FUNCION_RESTAR':
            resta_partieron = sum(variables["brujas_partieron"])
        
            if len(variables["brujas"]) > 1:
                resultado_resta = variables["brujas"][0]
                for numero in variables["brujas"][1:]:
                    resultado_resta -= numero
                codigo_ejecutable.append(f"resta_final_brujas = {' - '.join(map(str, variables['brujas']))} = {resultado_resta}")
        elif nodo[0] == 'FUNCION_MULTIPLICAR':
            if len(variables["brujas"]) > 1:
                resultado_multiplicacion = variables["brujas"][0]
                for numero in variables["brujas"][1:]:
                    resultado_multiplicacion *= numero
                codigo_ejecutable.append(f"multiplicacion_final_brujas = {' * '.join(map(str, variables['brujas']))} = {resultado_multiplicacion}")
        elif nodo[0] == 'FUNCION_DIVIDIR':
            if len(variables["brujas"]) > 1:
                resultado_division = variables["brujas"][0]
                for numero in variables["brujas"][1:]:
                    if numero == 0:
                        raise ZeroDivisionError("División por cero no permitida")
                    resultado_division /= numero
                codigo_ejecutable.append(f"division_final_brujas = {' / '.join(map(str, variables['brujas']))} = {resultado_division}")

    codigo_ejecutable = [linea + "\n" for linea in codigo_ejecutable]

    return codigo_ejecutable


codigo_fuente = 'Había una vez "Alegres" pueblerinos con 7 brujas 3 brujas llegaron partieron transformaron dividieron y así termina'
tokens = analizador_lexico(codigo_fuente)
arbol, variables = analizador_sintactico(tokens)
analizador_semantico(arbol, variables)
codigo_ejecutable = generador_codigo(arbol, variables)
print(codigo_ejecutable)
