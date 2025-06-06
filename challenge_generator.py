import random
import textwrap

# Definição dos desafios disponíveis
CHALLENGES = [
    {
        "topic": "strings",
        "difficulty": "fácil",
        "description": "Crie uma função que recebe uma string e retorna a string invertida.",
        "function_name": "reverse_string",
        "test_cases": [("python", "nohtyp"), ("abc", "cba"), ("", "")]
    },
    {
        "topic": "listas",
        "difficulty": "fácil",
        "description": "Crie uma função que recebe uma lista de números e retorna a soma de todos os elementos.",
        "function_name": "sum_list",
        "test_cases": [([1, 2, 3], 6), ([0, 0, 0], 0), ([10, -2], 8)]
    },
    {
        "topic": "laços",
        "difficulty": "médio",
        "description": "Crie uma função que recebe um número inteiro n e retorna uma lista com os n primeiros números pares.",
        "function_name": "even_numbers",
        "test_cases": [(3, [0,2,4]), (0, []), (1, [0])]
    },
    # Adicione mais desafios conforme necessário
]

def select_challenge(difficulty=None, topic=None):
    filtered = CHALLENGES
    if difficulty:
        filtered = [c for c in filtered if c['difficulty'] == difficulty]
    if topic:
        filtered = [c for c in filtered if c['topic'] == topic]
    return random.choice(filtered) if filtered else None

def show_challenge(challenge):
    print("\n=== DESAFIO ===")
    print(f"Tópico: {challenge['topic'].capitalize()}")
    print(f"Dificuldade: {challenge['difficulty'].capitalize()}")
    print("Descrição:")
    print(textwrap.fill(challenge['description'], width=80))
    print(f"\nImplemente a função: def {challenge['function_name']}(...):\n")

def test_student_code(function_name, user_code, test_cases):
    # Monta o código completo com a função do aluno
    global_namespace = {}
    try:
        exec(user_code, global_namespace)
    except Exception as e:
        print(f"Erro ao executar o código: {e}")
        return False

    func = global_namespace.get(function_name)
    if not callable(func):
        print(f"Função '{function_name}' não encontrada ou não é válida.")
        return False

    for i, (inp, expected) in enumerate(test_cases, 1):
        try:
            result = func(inp) if not isinstance(inp, tuple) else func(*inp)
            if result != expected:
                print(f"Teste {i} falhou: Entrada {inp} -> Esperado {expected}, obteve {result}")
                return False
        except Exception as e:
            print(f"Erro no teste {i} com entrada {inp}: {e}")
            return False
    return True

def main():
    print("Bem-vindo ao Gerador de Desafios Python!\n")
    diff = input("Escolha a dificuldade (fácil, médio, difícil ou Enter para aleatório): ").strip().lower() or None
    topic = input("Escolha o tópico (strings, listas, laços ou Enter para aleatório): ").strip().lower() or None

    challenge = select_challenge(diff, topic)
    if not challenge:
        print("Nenhum desafio encontrado com esses parâmetros.")
        return

    show_challenge(challenge)
    print("Digite sua função abaixo (finalize com uma linha contendo apenas 'EOF'):")

    # Captura o código do usuário
    user_lines = []
    while True:
        line = input()
        if line.strip() == "EOF":
            break
        user_lines.append(line)
    user_code = "\n".join(user_lines)

    print("\n=== RESULTADO DA AVALIAÇÃO ===")
    if test_student_code(challenge['function_name'], user_code, challenge['test_cases']):
        print("Parabéns! Todos os testes passaram. ✅")
    else:
        print("Alguns testes falharam. Tente novamente. ❌")

if __name__ == "__main__":
    main()