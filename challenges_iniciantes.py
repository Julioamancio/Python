from challenges_utils import (
    validator_print,
    validator_var,
    validator_input_print_final,
    validator_contains,
)

# ====== Validadores dinâmicos e robustos ======

def validador_nome_ola(code, input_data=None):
    nome = (input_data or "").strip() or "Maria"
    esperado = f"Olá, {nome}!"
    return validator_input_print_final(code, nome + "\n", esperado)

def validador_soma_dois_numeros(code, input_data=None):
    if input_data:
        try:
            a, b = map(int, input_data.strip().splitlines())
            esperado = str(a + b)
            return validator_input_print_final(code, input_data, esperado)
        except Exception:
            return False, "Digite dois números válidos, um por linha."
    tests = [("2\n3\n", "5"), ("7\n10\n", "17"), ("-2\n8\n", "6")]
    for entrada, esperado in tests:
        ok, msg = validator_input_print_final(code, entrada, esperado)
        if not ok:
            return False, msg
    return True, "Correto!"

def validador_maiusculo(code, input_data=None):
    texto = (input_data or "").strip()
    if texto:
        esperado = texto.upper()
        return validator_input_print_final(code, texto + "\n", esperado)
    tests = [("ana\n", "ANA"), ("Python\n", "PYTHON"), ("jUlio\n", "JULIO")]
    for entrada, esperado in tests:
        ok, msg = validator_input_print_final(code, entrada, esperado)
        if not ok:
            return False, msg
    return True, "Correto!"

def validador_dobro(code, input_data=None):
    texto = (input_data or "").strip()
    if texto:
        try:
            n = int(texto)
            esperado = str(n * 2)
            return validator_input_print_final(code, texto + "\n", esperado)
        except Exception:
            return False, "Digite um número válido."
    tests = [("5\n", "10"), ("0\n", "0"), ("-3\n", "-6")]
    for entrada, esperado in tests:
        ok, msg = validator_input_print_final(code, entrada, esperado)
        if not ok:
            return False, msg
    return True, "Correto!"

def validador_primeira_letra(code, input_data=None):
    texto = (input_data or "").strip()
    if texto:
        esperado = texto[0]
        return validator_input_print_final(code, texto + "\n", esperado)
    tests = ["amor", "Python", "julio", "7", "Brasil"]
    for entrada in tests:
        esperado = entrada[0]
        ok, msg = validator_input_print_final(code, entrada + "\n", esperado)
        if not ok:
            return False, f"Para o input '{entrada}': {msg}"
    return True, "Correto!"

def validador_idade_maioridade(code, input_data=None):
    idade = (input_data or "").strip()
    if idade:
        try:
            i = int(idade)
            esperado = "Maior de idade" if i >= 18 else "Menor de idade"
            return validator_input_print_final(code, idade + "\n", esperado)
        except Exception:
            return False, "Digite uma idade válida."
    testes = [("20\n", "Maior de idade"), ("15\n", "Menor de idade")]
    for entrada, esperado in testes:
        ok, msg = validator_input_print_final(code, entrada, esperado)
        if not ok:
            return False, msg
    return True, "Correto!"

def validador_par_ou_impar(code, input_data=None):
    teste = (input_data or "").strip()
    if teste:
        try:
            n = int(teste)
            esperado = "Par" if n % 2 == 0 else "Ímpar"
            return validator_input_print_final(code, teste + "\n", esperado)
        except Exception:
            return False, "Digite um número válido."
    casos = [("4\n", "Par"), ("7\n", "Ímpar"), ("0\n", "Par"), ("-3\n", "Ímpar")]
    for entrada, esperado in casos:
        ok, msg = validator_input_print_final(code, entrada, esperado)
        if not ok:
            return False, msg
    return True, "Correto!"

def validador_maior_de_dois(code, input_data=None):
    texto = (input_data or "").strip()
    if texto:
        try:
            a, b = map(int, texto.splitlines())
            esperado = str(max(a, b))
            return validator_input_print_final(code, texto, esperado)
        except Exception:
            return False, "Digite dois números válidos, um por linha."
    casos = [("2\n5\n", "5"), ("10\n3\n", "10"), ("7\n7\n", "7"), ("-1\n-5\n", "-1")]
    for entrada, esperado in casos:
        ok, msg = validator_input_print_final(code, entrada, esperado)
        if not ok:
            return False, msg
    return True, "Correto!"

def validador_negativo(code, input_data=None):
    texto = (input_data or "").strip()
    if texto:
        try:
            n = int(texto)
            esperado = "Negativo" if n < 0 else "Não negativo"
            return validator_input_print_final(code, texto + "\n", esperado)
        except Exception:
            return False, "Digite um número válido."
    casos = [("-1\n", "Negativo"), ("2\n", "Não negativo"), ("0\n", "Não negativo")]
    for entrada, esperado in casos:
        ok, msg = validator_input_print_final(code, entrada, esperado)
        if not ok:
            return False, msg
    return True, "Correto!"

def validador_vogal_consoante(code, input_data=None):
    texto = (input_data or "").strip()
    if texto:
        l = texto[0].lower()
        esperado = "Vogal" if l in "aeiou" else "Consoante"
        return validator_input_print_final(code, texto + "\n", esperado)
    casos = [("a\n", "Vogal"), ("E\n", "Vogal"), ("z\n", "Consoante"), ("b\n", "Consoante")]
    for entrada, esperado in casos:
        ok, msg = validator_input_print_final(code, entrada, esperado)
        if not ok:
            return False, msg
    return True, "Correto!"

# ========== Desafios Iniciantes CORRIGIDOS ==========
CHALLENGES_INICIANTES = [
    # =========================
    # Sintaxe básica (1 ponto)
    # =========================
    {
        "id": "ini-sintaxe-1",
        "level": "Iniciante",
        "topic": "Sintaxe básica",
        "icon": '<i class="fa-solid fa-keyboard"></i>',
        "description": '<i class="fa-solid fa-keyboard"></i> Exiba a mensagem Bem-vindo ao Python!',
        "starter_code": "print()",
        "tip": 'Use print("Bem-vindo ao Python!")',
        "validator": lambda code, input_data=None: validator_print(code, "Bem-vindo ao Python!"),
        "points": 1,
    },
    {
        "id": "ini-sintaxe-2",
        "level": "Iniciante",
        "topic": "Sintaxe básica",
        "icon": '<i class="fa-solid fa-quote-left"></i>',
        "description": '<i class="fa-solid fa-quote-left"></i> Crie uma variável chamada frase com o valor "Python é divertido".',
        "starter_code": "frase = ",
        "tip": 'frase = "Python é divertido"',
        "validator": lambda code, input_data=None: validator_var(code, "frase", "Python é divertido"),
        "points": 1,
    },
    {
        "id": "ini-sintaxe-3",
        "level": "Iniciante",
        "topic": "Sintaxe básica",
        "icon": '<i class="fa-solid fa-hashtag"></i>',
        "description": '<i class="fa-solid fa-hashtag"></i> Adicione um comentário com o texto: "Primeiro código Python".',
        "starter_code": "# ",
        "tip": 'Use # para comentários.',
        "validator": lambda code, input_data=None: validator_contains(code, ["Primeiro código Python"]),
        "points": 1,
    },
    {
        "id": "ini-sintaxe-4",
        "level": "Iniciante",
        "topic": "Sintaxe básica",
        "icon": '<i class="fa-solid fa-arrow-right"></i>',
        "description": '<i class="fa-solid fa-arrow-right"></i> Mostre o resultado de 2 + 3.',
        "starter_code": "print()",
        "tip": 'print(2 + 3)',
        "validator": lambda code, input_data=None: validator_print(code, "5"),
        "points": 1,
    },
    {
        "id": "ini-sintaxe-5",
        "level": "Iniciante",
        "topic": "Sintaxe básica",
        "icon": '<i class="fa-solid fa-arrow-down-1-9"></i>',
        "description": '<i class="fa-solid fa-arrow-down-1-9"></i> Mostre o tipo da variável x = 10.',
        "starter_code": "x = 10\nprint()",
        "tip": 'print(type(x))',
        "validator": lambda code, input_data=None: validator_print(code, "<class 'int'>"),
        "points": 1,
    },

    # =========================
    # Variáveis (1 ponto)
    # =========================
    {
        "id": "ini-var-1",
        "level": "Iniciante",
        "topic": "Variáveis",
        "icon": '<i class="fa-solid fa-box"></i>',
        "description": '<i class="fa-solid fa-box"></i> Crie uma variável chamada idade com o valor 15.',
        "starter_code": "idade = ",
        "tip": 'idade = 15',
        "validator": lambda code, input_data=None: validator_var(code, "idade", 15),
        "points": 1,
    },
    {
        "id": "ini-var-2",
        "level": "Iniciante",
        "topic": "Variáveis",
        "icon": '<i class="fa-solid fa-square-plus"></i>',
        "description": '<i class="fa-solid fa-square-plus"></i> Crie duas variáveis a=3, b=4 e mostre a soma.',
        "starter_code": "a = \nb = \nprint()",
        "tip": 'print(a + b)',
        "validator": lambda code, input_data=None: validator_print(code.replace(' ', ''), "7"),
        "points": 1,
    },
    {
        "id": "ini-var-3",
        "level": "Iniciante",
        "topic": "Variáveis",
        "icon": '<i class="fa-solid fa-arrows-spin"></i>',
        "description": '<i class="fa-solid fa-arrows-spin"></i> Altere o valor de uma variável x de 5 para 8 e mostre.',
        "starter_code": "x = 5\nx = \nprint()",
        "tip": 'x = 8\nprint(x)',
        "validator": lambda code, input_data=None: validator_print(code, "8"),
        "points": 1,
    },
    {
        "id": "ini-var-4",
        "level": "Iniciante",
        "topic": "Variáveis",
        "icon": '<i class="fa-solid fa-arrow-right-arrow-left"></i>',
        "description": '<i class="fa-solid fa-arrow-right-arrow-left"></i> Troque os valores de a=1 e b=2 e mostre.',
        "starter_code": "a = 1\nb = 2\na, b = \nprint(a, b)",
        "tip": 'a, b = b, a',
        "validator": lambda code, input_data=None: validator_print(code.replace(' ', ''), "2 1"),
        "points": 1,
    },
    {
        "id": "ini-var-5",
        "level": "Iniciante",
        "topic": "Variáveis",
        "icon": '<i class="fa-solid fa-code"></i>',
        "description": '<i class="fa-solid fa-code"></i> Crie uma variável texto com valor "abc" e mostre seu comprimento.',
        "starter_code": "texto = \nprint()",
        "tip": 'texto = "abc"\nprint(len(texto))',
        "validator": lambda code, input_data=None: validator_print(code, "3"),
        "points": 1,
    },

    # =========================
    # Entrada de dados (1 ponto)
    # =========================
    {
        "id": "ini-input-1",
        "level": "Iniciante",
        "topic": "Entrada de dados",
        "icon": '<i class="fa-solid fa-keyboard"></i>',
        "description": '<i class="fa-solid fa-keyboard"></i> Peça ao usuário para digitar o nome e mostre "Olá, nome!".',
        "starter_code": "nome = input()\nprint()",
        "tip": 'print("Olá, " + nome + "!")',
        "validator": validador_nome_ola,
        "points": 1,
    },
    {
        "id": "ini-input-2",
        "level": "Iniciante",
        "topic": "Entrada de dados",
        "icon": '<i class="fa-solid fa-arrow-up-9-1"></i>',
        "description": '<i class="fa-solid fa-arrow-up-9-1"></i> Peça dois números ao usuário e mostre a soma.',
        "starter_code": "a = int(input())\nb = int(input())\nprint()",
        "tip": 'print(a + b)',
        "validator": validador_soma_dois_numeros,
        "points": 1,
    },
    {
        "id": "ini-input-3",
        "level": "Iniciante",
        "topic": "Entrada de dados",
        "icon": '<i class="fa-solid fa-arrow-down-a-z"></i>',
        "description": '<i class="fa-solid fa-arrow-down-a-z"></i> Mostre o nome em maiúsculas digitado pelo usuário.',
        "starter_code": "nome = input()\nprint()",
        "tip": 'print(nome.upper())',
        "validator": validador_maiusculo,
        "points": 1,
    },
    {
        "id": "ini-input-4",
        "level": "Iniciante",
        "topic": "Entrada de dados",
        "icon": '<i class="fa-solid fa-arrow-turn-down"></i>',
        "description": '<i class="fa-solid fa-arrow-turn-down"></i> Peça um número e mostre o dobro.',
        "starter_code": "n = int(input())\nprint()",
        "tip": 'print(n * 2)',
        "validator": validador_dobro,
        "points": 1,
    },
    {
        "id": "ini-input-5",
        "level": "Iniciante",
        "topic": "Entrada de dados",
        "icon": '<i class="fa-solid fa-arrows-to-circle"></i>',
        "description": '<i class="fa-solid fa-arrows-to-circle"></i> Peça um texto e mostre a primeira letra.',
        "starter_code": 'texto = input("Digite um texto: ")\nprint(texto[0])',
        "tip": 'print(texto[0])',
        "validator": validador_primeira_letra,
        "points": 1,
    },

    # =========================
    # Condicionais (1 ponto)
    # =========================
    {
        "id": "ini-cond-1",
        "level": "Iniciante",
        "topic": "Condicionais",
        "icon": '<i class="fa-solid fa-code-branch"></i>',
        "description": '<i class="fa-solid fa-code-branch"></i> Peça a idade. Se >= 18, mostre "Maior de idade". Senão, "Menor de idade".',
        "starter_code": "idade = int(input())\n",
        "tip": 'if idade >= 18:\n    print("Maior de idade")\nelse:\n    print("Menor de idade")',
        "validator": validador_idade_maioridade,
        "points": 1,
    },
    {
        "id": "ini-cond-2",
        "level": "Iniciante",
        "topic": "Condicionais",
        "icon": '<i class="fa-solid fa-equals"></i>',
        "description": '<i class="fa-solid fa-equals"></i> Peça um número. Se for par, mostre "Par", senão "Ímpar".',
        "starter_code": "n = int(input())\n",
        "tip": 'if n % 2 == 0:\n    print("Par")\nelse:\n    print("Ímpar")',
        "validator": validador_par_ou_impar,
        "points": 1,
    },
    {
        "id": "ini-cond-3",
        "level": "Iniciante",
        "topic": "Condicionais",
        "icon": '<i class="fa-solid fa-less-than-equal"></i>',
        "description": '<i class="fa-solid fa-less-than-equal"></i> Peça dois números e mostre o maior.',
        "starter_code": "a = int(input())\nb = int(input())\n",
        "tip": 'print(max(a, b))',
        "validator": validador_maior_de_dois,
        "points": 1,
    },
    {
        "id": "ini-cond-4",
        "level": "Iniciante",
        "topic": "Condicionais",
        "icon": '<i class="fa-solid fa-arrows-left-right"></i>',
        "description": '<i class="fa-solid fa-arrows-left-right"></i> Peça um número. Se negativo, mostre "Negativo", senão "Não negativo".',
        "starter_code": "n = int(input())\n",
        "tip": 'if n < 0:\n    print("Negativo")\nelse:\n    print("Não negativo")',
        "validator": validador_negativo,
        "points": 1,
    },
    {
        "id": "ini-cond-5",
        "level": "Iniciante",
        "topic": "Condicionais",
        "icon": '<i class="fa-solid fa-circle-question"></i>',
        "description": '<i class="fa-solid fa-circle-question"></i> Peça uma letra. Se for vogal, mostre "Vogal", senão "Consoante".',
        "starter_code": "letra = input().lower()\n",
        "tip": 'if letra in "aeiou": print("Vogal") else: print("Consoante")',
        "validator": validador_vogal_consoante,
        "points": 1,
    },
]