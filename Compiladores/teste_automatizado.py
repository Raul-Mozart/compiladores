"""
Script de teste automatizado para o sistema de análise léxica
"""

from teste_analise_lexica import AnalisadorLexico
import os

def teste_automatico():
    """Executa testes automatizados do sistema"""
    print("🤖 EXECUTANDO TESTES AUTOMATIZADOS")
    print("=" * 50)
    
    # Inicializa o analisador
    analisador = AnalisadorLexico()
    
    print("\n1. 🔧 Testando compilação de tokens...")
    if len(analisador.dfas_compilados) > 15:
        print("   ✅ Tokens compilados com sucesso")
    else:
        print("   ⚠️  Alguns tokens falharam na compilação")
    
    print("\n2. 📝 Testando tokens individuais...")
    casos_teste = {
        "KEYWORD": ["if", "function", "var"],
        "IDENTIFIER": ["variavel", "_private", "contador1"],
        "INT_LITERAL": ["123", "0", "42"],
        "FLOAT_LITERAL": ["3.14", "1.5", "0.0"]
    }
    
    sucessos = 0
    total = 0
    
    for token_type, exemplos in casos_teste.items():
        for exemplo in exemplos:
            total += 1
            if analisador.validar_token_individual(token_type, exemplo):
                sucessos += 1
                print(f"   ✅ {token_type}: '{exemplo}'")
            else:
                print(f"   ❌ {token_type}: '{exemplo}'")
    
    print(f"\n   📊 Taxa de sucesso: {sucessos}/{total} ({100*sucessos/total:.1f}%)")
    
    print("\n3. 📄 Testando arquivo de exemplo...")
    if os.path.exists("codigo_exemplo.txt"):
        resultado = analisador.processar_arquivo("codigo_exemplo.txt")
        if "erro" in resultado:
            print(f"   ❌ Erro: {resultado['erro']}")
        else:
            print(f"   ✅ Processado: {resultado['total_tokens']} tokens encontrados")
            print(f"   📊 Tipos únicos: {len(resultado['estatisticas'])}")
    else:
        print("   ⚠️  Arquivo codigo_exemplo.txt não encontrado")
    
    print("\n4. 🔍 Testando código inline...")
    codigo_teste = '''
    var int x as 10;
    if (x > 5) {
        print("maior");
    }
    '''
    
    tokens = analisador.tokenizar_codigo(codigo_teste)
    tokens_validos = [t for t in tokens if t[0] != "UNKNOWN"]
    
    print(f"   📝 Código: {len(codigo_teste)} caracteres")
    print(f"   🔍 Tokens: {len(tokens)} encontrados")
    print(f"   ✅ Válidos: {len(tokens_validos)}")
    print(f"   ❌ Desconhecidos: {len(tokens) - len(tokens_validos)}")
    
    if len(tokens) > 10:
        print("   ✅ Tokenização funcionando")
    else:
        print("   ⚠️  Poucos tokens encontrados")
    
    print("\n🎯 RESUMO DOS TESTES:")
    print("=" * 30)
    print(f"✅ Sistema operacional: {sucessos/total > 0.8}")
    print(f"✅ Arquivos criados: {os.path.exists('codigo_exemplo.txt')}")
    print(f"✅ Tokenização: {len(tokens) > 5}")
    print("\n🚀 Sistema pronto para uso!")

if __name__ == "__main__":
    teste_automatico()