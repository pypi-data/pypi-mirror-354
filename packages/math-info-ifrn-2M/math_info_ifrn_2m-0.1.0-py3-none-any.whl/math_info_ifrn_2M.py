def soma_dois_numeros(a=0, b=0):
    return a + b
def soma_tres_numeros(a=0, b=0, c=0):
    return a + b + c
def soma_lista(lista=[]):
    if not lista:
        return 0
    return sum(lista)
def calcular_raiz_enesima(radicando=0, indice=2):
    if indice <= 0:
        return None
    if indice == 1:
        return radicando
    return radicando ** (1 / indice)
def converter_velocidade(valor=0, unidade='km'):
    unidades = {
        'km': 1000,
        'm': 1,
        'cm': 0.01,
        'mm': 0.001,
        'mi': 1609.34,
        'yd': 0.9144,
        'ft': 0.3048,
        'in': 0.0254
    }
    if unidade not in unidades:
        return None
    return valor * unidades[unidade]
def converter_temperatura(valor=0, unidade='C'):
    unidades = {
        'C': lambda x: x,
        'F': lambda x: (x - 32) * 5 / 9,
        'K': lambda x: x - 273.15
    }
    if unidade not in unidades:
        return None
    return unidades[unidade](valor)
def calcular_vel_media(distancia=0.0, tempo=1.0):
    if distancia <= 0 or tempo <= 0:
        return None
    return distancia // tempo
def uniao(n=[], r=[]):
    aux = []
    for i in r:
        if i not in aux:
            aux.append(i)
    for i in n:
        if i not in aux:
            aux.append(i)
    aux.sort()
    return aux
def permutation_simples(n):
    if n == 0 or n == 1:
        return 1
    else:
        result = n
        while n > 1:
            n -= 1
            result *= n
        return result
def permutation_rep(n, repetidos=[0]):
    lista_fatoriais = []
    for i in repetidos:
        aux = permutation_simples(i)
        lista_fatoriais.append(aux)
    aux = 1
    for i in lista_fatoriais:
        aux *= i
    return permutation_simples(n) // aux
def arranjo(n,r):
    if r > n:
        return 0
    return permutation_simples(n) // permutation_simples(n - r)
def combination(n,r):
    if r > n:
        return 0
    return permutation_simples(n) // (permutation_simples(r) * permutation_simples(n - r))
def intersection(n=[], r=[]):
    aux = []
    for i in r:
        if i in n and i not in aux:
            aux.append(i)
    return aux
def diferenca(n=[], r=[]):
    diferenca = []
    for i in n:
        if i not in r:
            diferenca.append(i)
    diferenca.sort()
    return diferenca
def probabilidade(n, r):
    if n == 0 or r == 0:
        return 0
    return (n / r) * 100
def resolver_equacao_1grau(a, b=0,c=0):
    if a == 0:
        if b == 0:
            return None
    if a == 0:
        return None
    return (c + (b * -1)) / a
def resolver_equacao_2grau(a, b=0, c=0):
    if a == 0:
        return None
    if b**2 - 4 * a * c < 0:
        return -b + complex(0, (4 * a * c - b**2)**0.5) / (2 * a), -b - complex(0, (4 * a * c - b**2)**0.5) / (2 * a)
    if b**2 - 4 * a * c == 0:
        return -b / (2 * a)
    return (-b + (b**2 - 4 * a * c)**0.5) / (2 * a), (-b - (b**2 - 4 * a * c)**0.5) / (2 * a)
def resolver_equacao_3grau(a, b=0, c=0, d=0):
    divisores = []
    raizes = []
    coeficientes_2_grau = []
    if a == 0:
        return resolver_equacao_2grau(b, c, d)
    for i in range(d + 1) if d >= 0 else range(d+1, 0):
        if d % i == 0:
            divisores.append(i)
            divisores.append(-i)
    for i in divisores:
        if a * i**3 + b * i**2 + c * i + d == 0:
            raizes.append(i)
    if len(raizes) == 3:
        return raizes
    coeficientes_2_grau.append(a)
    aux = a*raizes[0] + b
    coeficientes_2_grau.append(aux)
    aux = aux * raizes[0] + c
    coeficientes_2_grau.append(aux)
    aux = resolver_equacao_2grau(coeficientes_2_grau[0], coeficientes_2_grau[1], coeficientes_2_grau[2])
    if isinstance(aux, tuple):
        return raizes + list(aux)
    return raizes + [aux]
def teorema_pitagoras(a, b,c):
    if a + b + c != 0 and a + b + c != a and a + b + c != b and a + b + c != c:
        if a == 0 and b != 0 and c != 0:
            a = (c**2 - b**2)**0.5
            return a 
        if b == 0 and a != 0 and c != 0:
            b = (c**2 - a**2)**0.5
            return b
        if c == 0 and a != 0 and b != 0:
            c = (a**2 + b**2)**0.5
            return c
def sin(hipotenusa=0,cateto_oposto=0,cateto_adjacente=0):
    if hipotenusa == 0:
        hipotenusa = teorema_pitagoras(cateto_oposto, cateto_adjacente, hipotenusa)
    if cateto_oposto == 0:
        cateto_oposto = teorema_pitagoras(cateto_oposto, cateto_adjacente, hipotenusa)
    if hipotenusa is None or cateto_oposto is None or hipotenusa == 0:
        return None
    return cateto_oposto / hipotenusa
def cos(hipotenusa=0,cateto_oposto=0,cateto_adjacente=0):
    if hipotenusa == 0:
        hipotenusa = teorema_pitagoras(cateto_oposto, cateto_adjacente, hipotenusa)
    if cateto_adjacente == 0:
        cateto_adjacente = teorema_pitagoras(cateto_oposto, cateto_adjacente, hipotenusa)
    if hipotenusa is None or cateto_adjacente is None or hipotenusa == 0:
        return None
    return cateto_adjacente / hipotenusa
def tan(hipotenusa=0,cateto_oposto=0,cateto_adjacente=0):
    if hipotenusa == 0:
        hipotenusa = teorema_pitagoras(cateto_oposto, cateto_adjacente, hipotenusa)
    if cateto_oposto == 0:
        cateto_oposto = teorema_pitagoras(cateto_oposto, cateto_adjacente, hipotenusa)
    if cateto_adjacente == 0:
        cateto_adjacente = teorema_pitagoras(cateto_oposto, cateto_adjacente, hipotenusa)
    if hipotenusa is None or cateto_oposto is None or cateto_adjacente is None or hipotenusa == 0:
        return None
    return cateto_oposto / cateto_adjacente if cateto_oposto < cateto_adjacente else cateto_adjacente // cateto_oposto
def log(base=10, valor=0):
    for i in range(valor + 1):
        if base**i == valor:
            return i if isinstance(i, int) else None
    if base <= 0 or valor <= 0:
        return None
def converter_binario_decimal(binario):
    b4 = binario[:8]
    b3 = binario[8:16]
    b2 = binario[16:24]
    b1 = binario[24:32]
    bloco = 0
    decimal = ""
    if len(b4) == 8:
        for i, digito in enumerate(reversed(b4)):
            if digito == '1':
                bloco += 2**i
    decimal += str(bloco) + "."
    bloco = 0
    if len(b3) == 8:
        for i, digito in enumerate(reversed(b3)):
            if digito == '1':
                bloco += 2**i
    decimal += str(bloco) + "."
    bloco = 0
    if len(b2) == 8:
        for i, digito in enumerate(reversed(b2)):
            if digito == '1':
                bloco += 2**i
    decimal += str(bloco) + "."
    bloco = 0
    if len(b1) == 8:
        for i, digito in enumerate(reversed(b1)):
            if digito == '1':
                bloco += 2**i
    decimal += str(bloco)
    return decimal
def converter_decimal_binario(ip_decimal):
    octetos = ip_decimal.split('.')
    if len(octetos) != 4:
        return "Erro: Formato de IP inválido. Certifique-se de que há 4 octetos separados por pontos."

    octetos_binarios = []
    for octeto in octetos:
        try:
            num_decimal = int(octeto)
            if not (0 <= num_decimal <= 255):
                return f"Erro: O octeto '{octeto}' está fora do intervalo válido (0-255)."
            binario = bin(num_decimal)[2:]
            binario_com_padding = binario.zfill(8)
            octetos_binarios.append(binario_com_padding)
        except ValueError:
            return f"Erro: O octeto '{octeto}' não é um número válido."
    return ".".join(octetos_binarios)