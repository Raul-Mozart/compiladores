"""
SISTEMA DE TESTE DE ANÁLISE LÉXICA E SEMÂNTICA
Integrado com os autômatos existentes para testar a linguagem proposta

Este módulo permite:
1. Testar tokens individuais usando os autômatos DFA
2. Processar arquivos de código na linguagem proposta
3. Avaliar input do usuário interativamente
4. Gerar relatórios detalhados de análise léxica
5. Validar compatibilidade semântica de tipos (análise semântica básica)
"""

import re
import os
from typing import List, Dict, Tuple, Optional, NamedTuple
from automatos import compile_regex_to_dfa
from automatos.constantes import TOKENS_COMUNS


class ErroSemantico(NamedTuple):
    """Representa um erro semântico encontrado durante a análise"""
    tipo: str
    mensagem: str
    linha: int
    coluna: int
    contexto: str


class ValidadorSemantico:
    """Validador semântico básico para verificar compatibilidade de tipos"""
    
    def __init__(self):
        """Inicializa o validador semântico"""
        self.tipos_validos = {"int", "float", "string", "bool", "list"}
        self.erros_semanticos = []
    
    def limpar_erros(self):
        """Limpa a lista de erros semânticos"""
        self.erros_semanticos = []
    
    def eh_literal_valido_para_tipo(self, tipo: str, token_type: str, lexeme: str) -> bool:
        """
        Verifica se um literal é compatível com um tipo declarado
        
        Args:
            tipo: tipo declarado (int, float, string, bool, list)
            token_type: tipo do token encontrado
            lexeme: valor do token
            
        Returns:
            True se compatível, False caso contrário
        """
        if tipo == "int":
            return token_type == "INT_LITERAL"
        elif tipo == "float":
            return token_type in ["FLOAT_LITERAL", "INT_LITERAL"]  # int pode ser promovido para float
        elif tipo == "string":
            return token_type == "STRING_LITERAL"
        elif tipo == "bool":
            return token_type == "BOOL_LITERAL"
        elif tipo == "list":
            # Para lista, aceitamos arrays literais [1,2,3] - simplificado
            return lexeme.startswith("[") and lexeme.endswith("]")
        
        return False
    
    def validar_declaracao_variavel(self, tokens: List[Tuple[str, str, int, int]], posicao: int) -> Optional[ErroSemantico]:
        """
        Valida uma declaração de variável: var Type identificador as valor
        
        Args:
            tokens: lista completa de tokens
            posicao: posição do token 'var'
            
        Returns:
            ErroSemantico se encontrar problema, None caso contrário
        """
        try:
            # Padrão esperado: var Type identificador as valor
            if posicao + 4 >= len(tokens):
                return ErroSemantico(
                    "DECLARACAO_INCOMPLETA",
                    "Declaração de variável incompleta",
                    tokens[posicao][2],
                    tokens[posicao][3],
                    "var ... (incompleta)"
                )
            
            var_token = tokens[posicao]
            type_token = tokens[posicao + 1]
            identifier_token = tokens[posicao + 2]
            as_token = tokens[posicao + 3]
            value_token = tokens[posicao + 4]
            
            # Verifica se segue o padrão básico
            if (var_token[0] != "KEYWORD" or var_token[1] != "var" or
                type_token[0] != "KEYWORD" or type_token[1] not in self.tipos_validos or
                identifier_token[0] != "IDENTIFIER" or
                as_token[0] != "KEYWORD" or as_token[1] != "as"):
                return None  # Não é uma declaração de variável válida
            
            # Verifica compatibilidade de tipos
            tipo_declarado = type_token[1]
            valor_token_type = value_token[0]
            valor_lexeme = value_token[1]
            
            if not self.eh_literal_valido_para_tipo(tipo_declarado, valor_token_type, valor_lexeme):
                contexto = f"var {tipo_declarado} {identifier_token[1]} as {valor_lexeme}"
                
                # Mensagem específica baseada no tipo de erro
                if valor_token_type == "IDENTIFIER":
                    mensagem = f"Tipo incompatível: variável '{identifier_token[1]}' declarada como '{tipo_declarado}' mas recebeu identificador '{valor_lexeme}' (esperado literal {tipo_declarado})"
                else:
                    mensagem = f"Tipo incompatível: variável '{identifier_token[1]}' declarada como '{tipo_declarado}' mas recebeu {valor_token_type} '{valor_lexeme}'"
                
                return ErroSemantico(
                    "TIPO_INCOMPATIVEL",
                    mensagem,
                    value_token[2],
                    value_token[3],
                    contexto
                )
            
            return None  # Tudo OK
            
        except Exception as e:
            return ErroSemantico(
                "ERRO_VALIDACAO",
                f"Erro durante validação: {e}",
                tokens[posicao][2] if posicao < len(tokens) else 0,
                tokens[posicao][3] if posicao < len(tokens) else 0,
                "erro interno"
            )
    
    def validar_tokens(self, tokens: List[Tuple[str, str, int, int]]) -> List[ErroSemantico]:
        """
        Valida a lista completa de tokens para erros semânticos
        
        Args:
            tokens: lista de tokens (token_type, lexeme, linha, coluna)
            
        Returns:
            Lista de erros semânticos encontrados
        """
        self.limpar_erros()
        
        i = 0
        while i < len(tokens):
            token_type, lexeme, linha, coluna = tokens[i]
            
            # Procura por declarações de variáveis (var)
            if token_type == "KEYWORD" and lexeme == "var":
                erro = self.validar_declaracao_variavel(tokens, i)
                if erro:
                    self.erros_semanticos.append(erro)
                # Pula a declaração completa
                i += 5  # var Type id as value
            else:
                i += 1
        
        return self.erros_semanticos


class AnalisadorLexico:
    """Analisador léxico e semântico para a linguagem proposta"""
    
    def __init__(self):
        """Inicializa o analisador com tokens da linguagem proposta"""
        # Tokens específicos da linguagem (baseados na especificação GitHub)
        self.tokens_linguagem = {
            # Palavras-chave (incluindo 'as' que estava faltando)
            "KEYWORD": r"(if|else|for|while|function|var|in|class|return|string|int|float|bool|list|and|or|not|private|public|mutable|inherits|new|as)",
            
            # Identificadores (mais específico que o genérico)
            "IDENTIFIER": r"[A-Za-z_][A-Za-z0-9_]*",
            
            # Literais numéricos
            "INT_LITERAL": r"\d+",
            "FLOAT_LITERAL": r"\d+\.\d+([eE][+-]?\d+)?",
            
            # Literais de string (com escape)
            "STRING_LITERAL": r'"[^"]*"',
            
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
        self.validador_semantico = ValidadorSemantico()
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
        
        # Ordem de prioridade para tokens (mais específicos primeiro)
        ordem_prioridade = [
            "KEYWORD", "BOOL_LITERAL", "FLOAT_LITERAL", "INT_LITERAL", 
            "STRING_LITERAL", "RELOP", "ARITHOP", "ASSIGN", "RANGE",
            "LPAREN", "RPAREN", "LBRACE", "RBRACE", "LBRACKET", "RBRACKET",
            "SEMICOLON", "COMMA", "DOT", "COLON", "COMMENT",
            "IDENTIFIER", "NEWLINE", "WHITESPACE"
        ]
        
        while posicao < len(codigo):
            token_encontrado = False
            
            # Tenta encontrar o melhor match com base na prioridade
            melhor_match = None
            maior_comprimento = 0
            
            # Testa tokens na ordem de prioridade
            for nome_token in ordem_prioridade:
                if nome_token not in self.dfas_compilados:
                    continue
                    
                dfa = self.dfas_compilados[nome_token]
                
                # Testa substring a partir da posição atual
                # NÃO para na primeira rejeição - continua testando
                for fim in range(posicao + 1, len(codigo) + 1):
                    substring = codigo[posicao:fim]
                    
                    if dfa.accepts(substring):
                        # Se encontrou match maior ou de mesma prioridade, atualiza
                        if len(substring) > maior_comprimento:
                            maior_comprimento = len(substring)
                            melhor_match = (nome_token, substring)
                    # REMOVIDO: else break - isso estava causando o problema!
                
                # Se já encontrou um token de alta prioridade, para
                if melhor_match and nome_token in ["KEYWORD", "BOOL_LITERAL", "FLOAT_LITERAL", "INT_LITERAL", "STRING_LITERAL"]:
                    break
            
            if melhor_match:
                token_type, lexeme = melhor_match
                
                # Pós-processamento: verifica se IDENTIFIER é na verdade uma KEYWORD
                if token_type == "IDENTIFIER" and lexeme in ["if", "else", "for", "while", "function", "var", "in", "class", "return", "string", "int", "float", "bool", "list", "and", "or", "not", "private", "public", "mutable", "inherits", "new", "as"]:
                    token_type = "KEYWORD"
                
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
    
    def processar_codigo_completo(self, codigo: str) -> Dict:
        """
        Processa código fonte com análise léxica E semântica
        
        Args:
            codigo: código fonte a ser analisado
            
        Returns:
            Dicionário com tokens, erros léxicos, erros semânticos e estatísticas
        """
        # Análise léxica
        tokens = self.tokenizar_codigo(codigo)
        
        # Separar tokens válidos dos inválidos
        tokens_validos = []
        erros_lexicos = []
        
        for token_type, lexeme, linha, coluna in tokens:
            if token_type == "UNKNOWN":
                erros_lexicos.append({
                    "tipo": "CARACTERE_INVALIDO",
                    "mensagem": f"Caractere inválido: '{lexeme}'",
                    "linha": linha,
                    "coluna": coluna,
                    "contexto": lexeme
                })
            else:
                tokens_validos.append((token_type, lexeme, linha, coluna))
        
        # Análise semântica (apenas se não há erros léxicos críticos)
        erros_semanticos = []
        if not erros_lexicos:
            erros_semanticos = self.validador_semantico.validar_tokens(tokens_validos)
        
        # Estatísticas
        stats_tokens = {}
        for token_type, _, _, _ in tokens_validos:
            stats_tokens[token_type] = stats_tokens.get(token_type, 0) + 1
        
        return {
            "tokens": tokens_validos,
            "erros_lexicos": erros_lexicos,
            "erros_semanticos": [erro._asdict() for erro in erros_semanticos],
            "estatisticas_tokens": stats_tokens,
            "total_tokens": len(tokens_validos),
            "total_erros": len(erros_lexicos) + len(erros_semanticos),
            "linhas_codigo": codigo.count('\n') + 1,
            "analise_ok": len(erros_lexicos) == 0 and len(erros_semanticos) == 0
        }
    def processar_arquivo(self, caminho_arquivo: str) -> Dict:
        """Processa arquivo de código e retorna análise completa (léxica + semântica)"""
        if not os.path.exists(caminho_arquivo):
            return {"erro": f"Arquivo não encontrado: {caminho_arquivo}"}
        
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                codigo = arquivo.read()
            
            resultado = self.processar_codigo_completo(codigo)
            resultado["arquivo"] = caminho_arquivo
            
            return resultado
        
        except Exception as e:
            return {"erro": f"Erro ao processar arquivo: {e}"}
    
    def gerar_relatorio(self, resultado: Dict) -> str:
        """Gera relatório detalhado da análise léxica e semântica"""
        if "erro" in resultado:
            return f"❌ ERRO: {resultado['erro']}"
        
        relatorio = []
        relatorio.append("=" * 80)
        relatorio.append("📋 RELATÓRIO DE ANÁLISE LÉXICA E SEMÂNTICA")
        relatorio.append("=" * 80)
        
        # Informações básicas
        if "arquivo" in resultado:
            relatorio.append(f"📁 Arquivo: {resultado['arquivo']}")
        relatorio.append(f"📊 Total de tokens: {resultado['total_tokens']}")
        relatorio.append(f"📝 Linhas de código: {resultado['linhas_codigo']}")
        relatorio.append(f"🔍 Status da análise: {'✅ OK' if resultado.get('analise_ok', False) else '❌ ERROS ENCONTRADOS'}")
        relatorio.append("")
        
        # Erros léxicos
        erros_lexicos = resultado.get('erros_lexicos', [])
        if erros_lexicos:
            relatorio.append("🚫 ERROS LÉXICOS ENCONTRADOS:")
            relatorio.append("-" * 50)
            for i, erro in enumerate(erros_lexicos, 1):
                relatorio.append(f"  {i}. [{erro['linha']}:{erro['coluna']}] {erro['tipo']}")
                relatorio.append(f"     {erro['mensagem']}")
                relatorio.append(f"     Contexto: {erro['contexto']}")
                relatorio.append("")
        
        # Erros semânticos
        erros_semanticos = resultado.get('erros_semanticos', [])
        if erros_semanticos:
            relatorio.append("⚠️  ERROS SEMÂNTICOS ENCONTRADOS:")
            relatorio.append("-" * 50)
            for i, erro in enumerate(erros_semanticos, 1):
                relatorio.append(f"  {i}. [{erro['linha']}:{erro['coluna']}] {erro['tipo']}")
                relatorio.append(f"     {erro['mensagem']}")
                relatorio.append(f"     Contexto: {erro['contexto']}")
                relatorio.append("")
        
        # Estatísticas por tipo (apenas se não há erros)
        if resultado.get('analise_ok', False) or not (erros_lexicos or erros_semanticos):
            relatorio.append("📈 ESTATÍSTICAS POR TIPO DE TOKEN:")
            relatorio.append("-" * 50)
            stats = resultado.get('estatisticas_tokens', resultado.get('estatisticas', {}))
            for token_type, count in sorted(stats.items()):
                relatorio.append(f"  {token_type:15}: {count:4d} ocorrências")
            relatorio.append("")
        
        # Todos os tokens encontrados (apenas se análise OK)
        if resultado.get('analise_ok', False):
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
        print("🔬 ANALISADOR LÉXICO E SEMÂNTICO - MENU INTERATIVO")
        print("=" * 60)
        print("1. Testar arquivo de código")
        print("2. Testar código digitado")
        print("3. Criar arquivo de exemplo")
        print("4. Testar tokens individuais")
        print("5. Testar declarações específicas")
        print("6. Sair")
        
        opcao = input("\n📝 Escolha uma opção (1-6): ").strip()
        
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
                resultado = analisador.processar_codigo_completo(codigo)
                relatorio = analisador.gerar_relatorio(resultado)
                print("\n" + relatorio)
        
        elif opcao == "3":
            caminho = criar_arquivo_exemplo()
            print(f"✅ Arquivo de exemplo criado: {caminho}")
        
        elif opcao == "4":
            testar_tokens_individuais()
        
        elif opcao == "5":
            testar_declaracoes_especificas(analisador)
        
        elif opcao == "6":
            print("👋 Saindo do analisador. Até logo!")
            break
        
        else:
            print("❌ Opção inválida. Tente novamente.")


def testar_declaracoes_especificas(analisador: AnalisadorLexico):
    """Testa declarações específicas para validação semântica"""
    print("\n" + "=" * 60)
    print("🧪 TESTE DE DECLARAÇÕES DE VARIÁVEIS")
    print("=" * 60)
    
    casos_teste = [
        # Casos válidos
        ("var int idade as 25;", "✅ VÁLIDO"),
        ("var float altura as 1.75;", "✅ VÁLIDO"),
        ("var string nome as \"João\";", "✅ VÁLIDO"),
        ("var bool ativo as true;", "✅ VÁLIDO"),
        ("var int numero as 42;", "✅ VÁLIDO"),
        
        # Casos inválidos (o que você quer que dê erro)
        ("var int idade as b;", "❌ ERRO ESPERADO"),
        ("var float altura as nome;", "❌ ERRO ESPERADO"),
        ("var string texto as 123;", "❌ ERRO ESPERADO"),
        ("var bool flag as \"false\";", "❌ ERRO ESPERADO"),
        ("var int valor as 3.14;", "❌ ERRO ESPERADO"),
    ]
    
    for codigo, expectativa in casos_teste:
        print(f"\n🔍 Testando: {codigo}")
        print(f"   Expectativa: {expectativa}")
        
        resultado = analisador.processar_codigo_completo(codigo)
        
        if resultado['erros_semanticos']:
            print("   � Resultado: ERRO SEMÂNTICO encontrado")
            for erro in resultado['erros_semanticos']:
                print(f"      • {erro['mensagem']}")
        elif resultado['erros_lexicos']:
            print("   🚫 Resultado: ERRO LÉXICO encontrado")
            for erro in resultado['erros_lexicos']:
                print(f"      • {erro['mensagem']}")
        else:
            print("   ✅ Resultado: Análise OK")
        
        print("   " + "-" * 50)


def main():
    """Função principal do sistema de teste"""
    print("🚀 SISTEMA DE TESTE DE ANÁLISE LÉXICA E SEMÂNTICA")
    print("Baseado na linguagem especificada em github.com/Raul-Mozart/compiladores")
    print("Integrado com os autômatos DFA existentes")
    print("✨ Agora com validação semântica de tipos!")
    
    # Executa menu interativo
    menu_interativo()


if __name__ == "__main__":
    main()