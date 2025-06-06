import io
import sys
import threading
import traceback

# ================ NOVOS VALIDADORES RECOMENDADOS ==================

def validator_input_print_final(code, input_data, expected_output, timeout=4):
    """
    Executa o código, ignora os prompts de input e compara apenas a saída final.
    """
    output, error = _exec_code_capture_output(code, input_data, timeout)
    if error:
        return False, error
    # Divide linhas, ignora as linhas dos inputs (prompts)
    out_lines = output.strip().splitlines()
    input_count = len(input_data.strip().splitlines()) if input_data.strip() else 0
    out_lines = out_lines[input_count:] if input_count > 0 else out_lines
    output_final = "\n".join(out_lines).strip()
    ok = output_final == expected_output.strip()
    return (ok, f'Saída incorreta! Sua saída: "{output_final}" Esperado: "{expected_output.strip()}"' if not ok else "Correto!")

def robust_validator_final(code, test_cases=None, custom_check=None, timeout=4):
    """
    Valida vários casos de teste, sempre ignorando os prompts de input.
    """
    if test_cases:
        for case in test_cases:
            output, error = _exec_code_capture_output(code, case["input"], timeout)
            if error:
                return False, error
            out_lines = output.strip().splitlines()
            input_count = len(case["input"].strip().splitlines()) if case["input"].strip() else 0
            out_lines = out_lines[input_count:] if input_count > 0 else out_lines
            output_final = "\n".join(out_lines).strip()
            ok = any(output_final == expected.strip() for expected in case["outputs"])
            if not ok:
                return False, f"Saída incorreta para input `{case['input']}`.\nSua saída: \"{output_final}\"\nEsperado: {case['outputs']}"
        if custom_check:
            ok, msg = custom_check(code)
            if not ok:
                return False, msg
        return True, "Correto!"
    return False, "Nenhum caso de teste definido."

# ================ VALIDADORES ANTIGOS PARA COMPATIBILIDADE ==================

def validator_print(code, expected_output, timeout=4):
    output, error = _exec_code_capture_output(code, "", timeout)
    ok = output.strip() == expected_output.strip()
    return (ok, error or ("Correto!" if ok else f'Saída incorreta!\nSua saída: "{output.strip()}"\nEsperado: "{expected_output.strip()}"'))

def validator_var(code, var_name, expected_value, timeout=4):
    try:
        local_vars = {}
        def exec_code():
            exec(code, {}, local_vars)
        _run_with_timeout(exec_code, timeout=timeout)
        ok = var_name in local_vars and local_vars[var_name] == expected_value
        return (ok, "Correto!" if ok else f"Valor da variável '{var_name}' incorreto. Esperado: {expected_value}, Encontrado: {local_vars.get(var_name)}")
    except Exception as e:
        return False, f"Erro ao executar seu código: {e}"

def validator_input_print(code, input_data, expected_output, timeout=4):
    output, error = _exec_code_capture_output(code, input_data, timeout)
    ok = output.strip() == expected_output.strip()
    return (ok, error or ("Correto!" if ok else f'Saída incorreta!\nSua saída: "{output.strip()}"\nEsperado: "{expected_output.strip()}"'))

def validator_contains(code, must_contain):
    if isinstance(must_contain, str):
        must_contain = [must_contain]
    for item in must_contain:
        if item not in code:
            return False, f"Seu código deve conter: {item}"
    return True, "Correto!"

def robust_validator(
    code,
    test_cases=None,
    accepted_outputs=None,
    custom_check=None,
    timeout=4
):
    if test_cases:
        for case in test_cases:
            output, error = _exec_code_capture_output(code, case["input"], timeout)
            if error:
                return False, error
            out_clean = output.strip().lower()
            ok = any(expected.lower() in out_clean for expected in case["outputs"])
            if not ok:
                return False, f"Saída incorreta para o input `{case['input']}`.\nSua saída: \"{output.strip()}\"\nEsperado: {case['outputs']}"
        if custom_check:
            ok, msg = custom_check(code)
            if not ok:
                return False, msg
        return True, "Correto!"
    else:
        output, error = _exec_code_capture_output(code, "", timeout)
        if error:
            return False, error
        out_clean = output.strip().lower()
        for expected in (accepted_outputs or []):
            if expected.lower() in out_clean:
                return True, "Correto!"
        return False, f"Saída incorreta!\nSua saída: {output.strip()}\nEsperado: {accepted_outputs[0]}"

# ================ UTILITÁRIOS DE EXECUÇÃO ==================

def _exec_code_capture_output(code, input_data="", timeout=4):
    output, error = "", ""
    def run():
        nonlocal output, error
        buf_out = io.StringIO()
        buf_err = io.StringIO()
        sys_stdout, sys_stderr, sys_stdin = sys.stdout, sys.stderr, sys.stdin
        sys.stdout = buf_out
        sys.stderr = buf_err
        sys.stdin = io.StringIO(input_data)
        try:
            exec(code, {})
        except EOFError:
            error = "[ERRO] Faltou entrada para o(s) comando(s) input()."
        except Exception:
            error = buf_err.getvalue() + traceback.format_exc(limit=2)
        finally:
            output = buf_out.getvalue()
            sys.stdout = sys_stdout
            sys.stderr = sys_stderr
            sys.stdin = sys_stdin

    t = threading.Thread(target=run)
    t.daemon = True
    t.start()
    t.join(timeout)
    if t.is_alive():
        return "Tempo excedido ou loop infinito.", "Timeout"
    return output, error

def _run_with_timeout(func, args=(), kwargs={}, timeout=4):
    result = [None]
    def wrapper():
        try:
            result[0] = func(*args, **kwargs)
        except Exception as e:
            result[0] = e
    t = threading.Thread(target=wrapper)
    t.daemon = True
    t.start()
    t.join(timeout)
    if t.is_alive():
        raise TimeoutError("Seu código demorou muito para rodar (possível loop infinito).")
    if isinstance(result[0], Exception):
        raise result[0]
    return result[0]