"""
COMPILADOR DE EXPRESSÕES REGULARES PARA AUTÔMATOS

Arquivo principal que demonstra o uso do compilador de regex.
Testa diversos padrões e mostra como o autômato funciona.

Para usar em seus próprios projetos:
    from automatos import compile_regex_to_dfa
    dfa = compile_regex_to_dfa("sua_regex")
    resultado = dfa.accepts("sua_string")
"""

from automatos import compile_regex_to_dfa
from automatos.constantes import TOKENS_COMUNS


def main():
    """Função principal que executa todos os testes"""
    print("COMPILADOR DE EXPRESSÕES REGULARES PARA AUTÔMATOS")
    print("=" * 60)
    print("Este programa converte padrões de texto (regex) em máquinas que")
    print("verificam se strings correspondem ao padrão.\n")

    print("TESTANDO TOKENS COMUNS:")
    print("-" * 30)

    exemplos = {
        "IDENT": ["abc", "_var1", "9bad", "x"],
        "INT": ["0", "123", "0012a", ""],
        "FLOAT": ["3.14", "0.0", ".5", "5.", "1.2.3"],
        "STRING": ['"hello"', '"he\\"llo"', '""', '"unterminated', '"with\nnewline"'],
        "OP": ["+", "-", "==", ">=", "!", "!?"],
    }

    compilados = {}
    for nome, regex in TOKENS_COMUNS.items():
        try:
            dfa = compile_regex_to_dfa(regex)
            compilados[nome] = dfa
            print(f"✅ {nome:6}: '{regex}' → {len(dfa.states)} estados no DFA")
        except Exception as ex:
            print(f"❌ {nome:6}: ERRO → {ex}")

    print(f"\nRESULTADOS DOS TESTES:")
    print("-" * 30)
    for tipo, testes in exemplos.items():
        dfa = compilados.get(tipo)
        if not dfa:
            continue
        print(f"\n{tipo}:")
        for texto in testes:
            aceita = dfa.accepts(texto)
            status = "✅ ACEITA" if aceita else "❌ REJEITA"
            print(f"  '{texto}' → {status}")

    print(f"\nTESTES EXTRAS:")
    print("-" * 20)
    
    # Teste 1: Strings binárias
    print("Padrão: [01]* (sequências de 0s e 1s)")
    dfa_binario = compile_regex_to_dfa(r"[01]*")
    for s in ["", "0", "10101", "102", "abc"]:
        resultado = "✅" if dfa_binario.accepts(s) else "❌"
        print(f"  '{s}' → {resultado}")
    
    print()
    
    # Teste 2: Números
    print("Padrão: \\d+ (um ou mais dígitos)")
    dfa_numeros = compile_regex_to_dfa(r"\d+")
    for s in ["123", "abc", "12a", "0"]:
        resultado = "✅" if dfa_numeros.accepts(s) else "❌"
        print(f"  '{s}' → {resultado}")
        
    print(f"\nEXPLICAÇÃO DO OUTPUT:")
    print("-" * 25)
    print("• ✅ ACEITA: a string corresponde ao padrão")
    print("• ❌ REJEITA: a string NÃO corresponde ao padrão")
    print("• Estados no DFA: quantos estados o autômato tem")
    print("  (menos estados = mais eficiente)")
    print("\nO autômato funciona como uma máquina que:")
    print("1. Lê cada caractere da string, um por vez")
    print("2. Muda de estado baseado no caractere lido")
    print("3. Se terminar em um estado 'final', aceita a string")


def exemplo_simples():
    """Exemplo básico de uso da API"""
    print("\n" + "="*50)
    print("EXEMPLO SIMPLES DE USO:")
    print("-" * 25)
    
    # Cria autômato para emails simples
    email_pattern = r"\w+@\w+\.\w+"
    dfa_email = compile_regex_to_dfa(email_pattern)
    
    # Testa algumas strings
    emails = ["user@domain.com", "invalid.email", "test@site.org", "@domain.com"]
    
    print(f"Padrão: {email_pattern} (email simples)")
    for email in emails:
        aceita = dfa_email.accepts(email)
        status = "✅ VÁLIDO" if aceita else "❌ INVÁLIDO"
        print(f"  '{email}' → {status}")


if __name__ == "__main__":
    main()
    exemplo_simples()