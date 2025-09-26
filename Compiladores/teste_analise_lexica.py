"""
SISTEMA DE TESTE DE ANÁLISE LÉXICA
Integrado com os autômatos existentes para testar a linguagem proposta

Este módulo permite:
1. Testar tokens individuais usando os autômatos DFA
2. Processar arquivos de código na linguagem proposta
3. Avaliar input do usuário interativamente
4. Gerar relatórios detalhados de análise léxica
"""

import re
import os
from typing import List, Dict, Tuple, Optional
from automatos import compile_regex_to_dfa
from automatos.constantes import TOKENS_COMUNS


class AnalisadorLexico:
    """Analisador léxico para a linguagem proposta"""
    
    def __init__(self):
        """Inicializa o analisador com tokens da linguagem proposta"""
        # Tokens específicos da linguagem (baseados na especificação GitHub)
        self.tokens_linguagem = {
            # Palavras-chave
            "KEYWORD": r"(if|else|for|while|function|var|in|class|return|string|int|float|bool|list|and|or|not|private|public|mutable|inherits|new)",
            
            # Identificadores (mais específico que o genérico)
            "IDENTIFIER": r"[A-Za-z_][A-Za-z0-9_]*",
            
            # Literais numéricos
            "INT_LITERAL": r"\d+",
            "FLOAT_LITERAL": r"\d+\.\d+([eE][+-]?\d+)?",
            
            # Literais de string (com escape)
            "STRING_LITERAL": r'"([^"\\]|\\[\\"])*"',
            
            # Literais booleanos
            "BOOL_LITERAL": r"(true|false)",
            
            # Operadores relacionais
            "RELOP": r"(==|!=|<=|>=|<|>)",
            
            # Operadores aritméticos
            "ARITHOP": r"[+\-*/%]",
            
            # Operador de atribuição
            "ASSIGN": r"=",
            
            # Delimitadores
            "LPAREN": r"\(",
            "RPAREN": r"\)",
            "LBRACE": r"\{",
            "RBRACE": r"\}",
            "LBRACKET": r"\[",
            "RBRACKET": r"\]",
            
            # Pontuação
            "SEMICOLON": r";",
            "COMMA": r",",
            "DOT": r"\.",
            "COLON": r":",
            
            # Quebra de linha e espaços
            "NEWLINE": r"\n",
            "WHITESPACE": r"[ \t\r]+",
            
            # Comentários (adicionando suporte)
            "COMMENT": r"//[^\n]*",
            
            # Operador de range
            "RANGE": r"\.\."
        }
        
        # Compilar todos os tokens para DFA
        self.dfas_compilados = {}
        self.compilar_tokens()
    
    def compilar_tokens(self):
        """Compila todos os tokens para autômatos DFA"""
        print("🔄 Compilando tokens para autômatos DFA...")
        
        for nome, regex in self.tokens_linguagem.items():
            try:
                dfa = compile_regex_to_dfa(regex)
                self.dfas_compilados[nome] = dfa
                print(f"  ✅ {nome}: {len(dfa.states)} estados")
            except Exception as e:
                print(f"  ❌ {nome}: ERRO → {e}")
        
        print(f"📊 Total de tokens compilados: {len(self.dfas_compilados)}")
    
    def tokenizar_codigo(self, codigo: str) -> List[Tuple[str, str, int, int]]:
        """
        Tokeniza código fonte da linguagem
        
        Returns:
            Lista de (token_type, lexeme, linha, coluna)
        """
        tokens_encontrados = []
        linha_atual = 1
        coluna_atual = 1
        posicao = 0
        
        while posicao < len(codigo):
            token_encontrado = False
            
            # Tenta encontrar o maior match possível
            melhor_match = None
            maior_comprimento = 0
            
            for nome_token, dfa in self.dfas_compilados.items():
                # Testa substring a partir da posição atual
                for fim in range(posicao + 1, len(codigo) + 1):
                    substring = codigo[posicao:fim]
                    
                    if dfa.accepts(substring):
                        if len(substring) > maior_comprimento:
                            maior_comprimento = len(substring)
                            melhor_match = (nome_token, substring)
                    else:
                        # Se não aceita, não precisa testar strings maiores
                        break
            
            if melhor_match:
                token_type, lexeme = melhor_match
                
                # Pula whitespace e comentários na saída (mas ainda processa)
                if token_type not in ["WHITESPACE", "COMMENT"]:
                    tokens_encontrados.append((token_type, lexeme, linha_atual, coluna_atual))
                
                # Atualiza posição
                posicao += len(lexeme)
                
                # Atualiza linha e coluna
                if token_type == "NEWLINE" or '\n' in lexeme:
                    linha_atual += lexeme.count('\n')
                    coluna_atual = 1
                else:
                    coluna_atual += len(lexeme)
                
                token_encontrado = True
            
            if not token_encontrado:
                # Caractere não reconhecido
                char = codigo[posicao]
                tokens_encontrados.append(("UNKNOWN", char, linha_atual, coluna_atual))
                posicao += 1
                coluna_atual += 1
        
        return tokens_encontrados
    
    def validar_token_individual(self, token_type: str, lexeme: str) -> bool:
        """Valida se um lexeme corresponde a um tipo de token específico"""
        if token_type in self.dfas_compilados:
            return self.dfas_compilados[token_type].accepts(lexeme)
        return False
    
    def processar_arquivo(self, caminho_arquivo: str) -> Dict:
        """Processa arquivo de código e retorna análise completa"""
        if not os.path.exists(caminho_arquivo):
            return {"erro": f"Arquivo não encontrado: {caminho_arquivo}"}
        
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                codigo = arquivo.read()
            
            tokens = self.tokenizar_codigo(codigo)
            
            # Estatísticas
            stats = {}
            for token_type, _, _, _ in tokens:
                stats[token_type] = stats.get(token_type, 0) + 1
            
            return {
                "arquivo": caminho_arquivo,
                "tokens": tokens,
                "estatisticas": stats,
                "total_tokens": len(tokens),
                "linhas_codigo": codigo.count('\n') + 1
            }
        
        except Exception as e:
            return {"erro": f"Erro ao processar arquivo: {e}"}
    
    def gerar_relatorio(self, resultado: Dict) -> str:
        """Gera relatório detalhado da análise"""
        if "erro" in resultado:
            return f"❌ ERRO: {resultado['erro']}"
        
        relatorio = []
        relatorio.append("=" * 80)
        relatorio.append("📋 RELATÓRIO DE ANÁLISE LÉXICA")
        relatorio.append("=" * 80)
        relatorio.append(f"📁 Arquivo: {resultado['arquivo']}")
        relatorio.append(f"📊 Total de tokens: {resultado['total_tokens']}")
        relatorio.append(f"📝 Linhas de código: {resultado['linhas_codigo']}")
        relatorio.append("")
        
        # Estatísticas por tipo
        relatorio.append("📈 ESTATÍSTICAS POR TIPO DE TOKEN:")
        relatorio.append("-" * 50)
        for token_type, count in sorted(resultado['estatisticas'].items()):
            relatorio.append(f"  {token_type:15}: {count:4d} ocorrências")
        
        relatorio.append("")
        
        # Todos os tokens encontrados
        relatorio.append("🔍 TOKENS ENCONTRADOS:")
        relatorio.append("-" * 50)
        relatorio.append(f"{'LINHA':>5} {'COL':>4} {'TIPO':15} {'LEXEME'}")
        relatorio.append("-" * 50)
        
        for token_type, lexeme, linha, coluna in resultado['tokens']:
            # Escape strings para display
            if token_type == "STRING_LITERAL":
                lexeme_display = repr(lexeme)
            else:
                lexeme_display = lexeme.replace('\n', '\\n').replace('\t', '\\t')
            
            relatorio.append(f"{linha:5d} {coluna:4d} {token_type:15} {lexeme_display}")
        
        return "\n".join(relatorio)


def testar_tokens_individuais():
    """Testa tokens individuais usando os autômatos"""
    print("\n" + "=" * 60)
    print("🧪 TESTANDO TOKENS INDIVIDUAIS")
    print("=" * 60)
    
    analisador = AnalisadorLexico()
    
    casos_teste = {
        "KEYWORD": ["if", "else", "function", "var", "while", "for", "invalid_keyword"],
        "IDENTIFIER": ["variavel", "_private", "contador1", "9invalid", "valid_name"],
        "INT_LITERAL": ["123", "0", "007", "12.5", "abc"],
        "FLOAT_LITERAL": ["3.14", "0.0", "1.5e10", "123", ".5"],
        "STRING_LITERAL": ['"hello"', '"world \\"quoted\\""', '""', '"unterminated', '"valid"'],
        "BOOL_LITERAL": ["true", "false", "True", "FALSE", "maybe"],
        "RELOP": ["==", "!=", "<=", ">=", "<", ">", "==="],
        "ARITHOP": ["+", "-", "*", "/", "%", "++", "--"],
    }
    
    for token_type, exemplos in casos_teste.items():
        print(f"\n🏷️  {token_type}:")
        for exemplo in exemplos:
            valido = analisador.validar_token_individual(token_type, exemplo)
            status = "✅" if valido else "❌"
            print(f"  {status} '{exemplo}'")


def criar_arquivo_exemplo():
    """Cria arquivo de exemplo com código na linguagem proposta"""
    codigo_exemplo = '''// PROGRAMA DE EXEMPLO - Linguagem Proposta
// Testando todos os tipos de tokens

var int idade as 25;
var float altura as 1.75;
var string nome as "João Silva";
var bool ativo as true;
var list numeros as [1, 2, 3, 4, 5];

function string verificarIdade(idade) {
    if (idade >= 18) {
        return "Maior de idade";
    } else if (idade >= 13) {
        return "Adolescente";  
    } else {
        return "Criança";
    }
}

function float calcularMedia(a, b, c) {
    var float soma as a + b + c;
    var float media as soma / 3.0;
    return media;
}

class Pessoa {
    var string nome as "";
    var int idade as 0;
    
    function void setNome(novoNome) {
        nome = novoNome;
    }
}
return

// Programa principal
var int numeroA as 10;
var int numeroB as 20; 
var float resultado as calcularMedia(numeroA, numeroB, 15);

if (resultado > 15.0 and numeroA != numeroB) {
    print("Resultado válido: " + resultado);
} else {
    print("Resultado inválido");
}

for int i in 1 .. 5 {
    print("Número: " + i);
}
'''
    
    caminho = "codigo_exemplo.txt"
    with open(caminho, 'w', encoding='utf-8') as arquivo:
        arquivo.write(codigo_exemplo)
    
    return caminho


def menu_interativo():
    """Menu interativo para o usuário testar o analisador"""
    analisador = AnalisadorLexico()
    
    while True:
        print("\n" + "=" * 60)
        print("🔬 ANALISADOR LÉXICO - MENU INTERATIVO")
        print("=" * 60)
        print("1. Testar arquivo de código")
        print("2. Testar código digitado")
        print("3. Criar arquivo de exemplo")
        print("4. Testar tokens individuais")
        print("5. Sair")
        
        opcao = input("\n📝 Escolha uma opção (1-5): ").strip()
        
        if opcao == "1":
            caminho = input("📁 Digite o caminho do arquivo: ").strip()
            if not caminho:
                caminho = "codigo_exemplo.txt"
                print(f"📋 Usando arquivo padrão: {caminho}")
            
            resultado = analisador.processar_arquivo(caminho)
            relatorio = analisador.gerar_relatorio(resultado)
            print("\n" + relatorio)
            
            # Salvar relatório
            with open("relatorio_analise.txt", "w", encoding="utf-8") as f:
                f.write(relatorio)
            print(f"\n💾 Relatório salvo em: relatorio_analise.txt")
        
        elif opcao == "2":
            print("📝 Digite o código (termine com linha vazia):")
            linhas = []
            while True:
                linha = input()
                if linha.strip() == "":
                    break
                linhas.append(linha)
            
            codigo = "\n".join(linhas)
            if codigo.strip():
                tokens = analisador.tokenizar_codigo(codigo)
                
                print("\n🔍 TOKENS ENCONTRADOS:")
                print("-" * 50)
                for token_type, lexeme, linha, coluna in tokens:
                    print(f"{linha:3d}:{coluna:3d} {token_type:15} '{lexeme}'")
        
        elif opcao == "3":
            caminho = criar_arquivo_exemplo()
            print(f"✅ Arquivo de exemplo criado: {caminho}")
        
        elif opcao == "4":
            testar_tokens_individuais()
        
        elif opcao == "5":
            print("👋 Saindo do analisador léxico. Até logo!")
            break
        
        else:
            print("❌ Opção inválida. Tente novamente.")


def main():
    """Função principal do sistema de teste"""
    print("🚀 SISTEMA DE TESTE DE ANÁLISE LÉXICA")
    print("Baseado na linguagem especificada em github.com/Raul-Mozart/compiladores")
    print("Integrado com os autômatos DFA existentes")
    
    # Executa menu interativo
    menu_interativo()


if __name__ == "__main__":
    main()