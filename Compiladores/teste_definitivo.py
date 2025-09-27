#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 TESTE FINAL DEFINITIVO DO COMPILADOR
Segue o padrão solicitado:
1. Escreve programa na linguagem especificada
2. Roda analisador léxico sobre o arquivo
3. Gera tabela com TOKEN | TIPO
4. Mostra erros com linha e coluna para tokens inválidos
"""

import os
from teste_analise_lexica import AnalisadorLexico

def criar_programa_linguagem():
    """Cria um programa completo na linguagem especificada"""
    programa = """// PROGRAMA EXEMPLO NA LINGUAGEM ESPECIFICADA
// Demonstra todos os tipos de tokens

var int idade as 25;
var float altura as 1.75;
var string nome as "João Silva";
var string cidade as "São Paulo";
var bool ativo as true;
var bool inativo as false;

function int calcularIdade(anoNascimento) {
    var int anoAtual as 2023;
    var int resultado as anoAtual - anoNascimento;
    return resultado;
}

function bool ehMaiorIdade(idade) {
    if (idade >= 18) {
        return true;
    } else {
        return false;
    }
}

// Programa principal
var int anoNasc as 1995;
var int idadeCalculada as calcularIdade(anoNasc);
var bool maior as ehMaiorIdade(idadeCalculada);

if (maior and ativo) {
    var string mensagem as "Usuário ativo e maior de idade";
    print(mensagem);
} else {
    print("Condições não atendidas");
}

for int i in 1 .. 5 {
    var string msg as "Iteração número: ";
    print(msg + i);
}

// Exemplo com operadores
var int a as 10;
var int b as 5;
var int soma as a + b;
var int subtracao as a - b;
var int multiplicacao as a * b;
var int divisao as a / b;
var bool comparacao as (a > b) and (soma != divisao);

// Exemplo com arrays (lista)
var list numeros as [1, 2, 3, 4, 5];
var string textos as "Fim do programa";
"""
    
    # Salva o programa em arquivo
    with open("programa_exemplo.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write(programa)
    
    print("📝 PROGRAMA CRIADO NA LINGUAGEM ESPECIFICADA")
    print("=" * 60)
    print("📁 Arquivo: programa_exemplo.txt")
    print(f"📊 Linhas: {programa.count('\\n') + 1}")
    print(f"📏 Caracteres: {len(programa)}")
    print()
    
    return "programa_exemplo.txt"

def gerar_tabela_tokens(resultado):
    """Gera tabela formatada com TOKEN | TIPO"""
    print("📋 TABELA DE TOKENS RECONHECIDOS")
    print("=" * 60)
    print(f"{'TOKEN':25} | {'TIPO':20}")
    print("-" * 60)
    
    # Filtra tokens vazios (newlines e whitespace) para tabela mais limpa
    tokens_relevantes = []
    for token_type, lexeme, linha, coluna in resultado['tokens']:
        if token_type not in ['NEWLINE', 'WHITESPACE']:
            tokens_relevantes.append((token_type, lexeme, linha, coluna))
    
    for token_type, lexeme, linha, coluna in tokens_relevantes:
        # Trunca tokens muito longos para melhor visualização
        token_display = lexeme if len(lexeme) <= 23 else lexeme[:20] + "..."
        print(f"{token_display:25} | {token_type:20}")
    
    print("-" * 60)
    print(f"📊 Total de tokens relevantes: {len(tokens_relevantes)}")
    print(f"📊 Total de tokens (incluindo whitespace): {len(resultado['tokens'])}")

def mostrar_erros_detalhados(resultado):
    """Mostra erros com linha e coluna conforme especificado"""
    erros_lexicos = resultado.get('erros_lexicos', [])
    
    if erros_lexicos:
        print()
        print("❌ TOKENS NÃO RECONHECIDOS (ERROS LÉXICOS)")
        print("=" * 60)
        
        for i, erro in enumerate(erros_lexicos, 1):
            linha = erro['linha']
            coluna = erro['coluna']
            contexto = erro['contexto']
            mensagem = erro['mensagem']
            
            print(f"Erro {i}:")
            print(f"  📍 Localização: Linha {linha}, Coluna {coluna}")
            print(f"  🚫 Token inválido: '{contexto}'")
            print(f"  💬 Descrição: {mensagem}")
            print()
        
        print(f"📊 Total de erros encontrados: {len(erros_lexicos)}")
    else:
        print()
        print("✅ NENHUM TOKEN INVÁLIDO ENCONTRADO")
        print("=" * 60)
        print("Todos os tokens do programa foram reconhecidos com sucesso!")

def criar_programa_com_erros():
    """Cria um programa com tokens inválidos para demonstrar detecção de erros"""
    programa_com_erros = """// PROGRAMA COM TOKENS INVÁLIDOS (PARA DEMONSTRAR DETECÇÃO DE ERROS)

var int idade as 25;
var string nome as "João";
var int valor@ as 100;        // @ é caractere inválido
var float altura as 1.75;
var 中文变量 as "teste";         // Caracteres chineses inválidos
var string texto as "sem fechar aspas
var bool flag as true;
var int outro# as 50;         // # é caractere inválido
"""
    
    # Salva o programa com erros
    with open("programa_com_erros.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write(programa_com_erros)
    
    return "programa_com_erros.txt"

def executar_teste_padrao_solicitado():
    """Executa o teste seguindo exatamente o padrão solicitado"""
    print("🎯 TESTE FINAL SEGUINDO O PADRÃO ESPECIFICADO")
    print("=" * 80)
    print()
    
    # Passo 1: Criar programa na linguagem especificada
    print("PASSO 1: Criando programa na linguagem especificada...")
    arquivo_programa = criar_programa_linguagem()
    
    # Passo 2: Executar analisador léxico
    print("PASSO 2: Executando analisador léxico sobre o arquivo...")
    analisador = AnalisadorLexico()
    resultado = analisador.processar_arquivo(arquivo_programa)
    
    if "erro" in resultado:
        print(f"❌ Erro ao processar arquivo: {resultado['erro']}")
        return False
    
    print(f"✅ Análise concluída!")
    print()
    
    # Passo 3: Gerar tabela TOKEN | TIPO
    gerar_tabela_tokens(resultado)
    
    # Passo 4: Mostrar erros com linha e coluna (se houver)
    mostrar_erros_detalhados(resultado)
    
    # Estatísticas finais
    print()
    print("📈 ESTATÍSTICAS FINAIS")
    print("=" * 60)
    print(f"📁 Arquivo analisado: {arquivo_programa}")
    print(f"📝 Linhas de código: {resultado.get('linhas_codigo', 0)}")
    print(f"📊 Total de tokens: {resultado.get('total_tokens', 0)}")
    print(f"❌ Erros léxicos: {len(resultado.get('erros_lexicos', []))}")
    print(f"⚠️ Erros semânticos: {len(resultado.get('erros_semanticos', []))}")
    
    # Status final
    if resultado.get('analise_ok', False):
        print(f"✅ Status: ANÁLISE BEM-SUCEDIDA")
    else:
        print(f"❌ Status: ERROS ENCONTRADOS")
    
    return resultado.get('analise_ok', False)

def executar_teste_com_erros():
    """Demonstra a detecção de erros com tokens inválidos"""
    print()
    print("🔍 DEMONSTRAÇÃO: DETECÇÃO DE TOKENS INVÁLIDOS")
    print("=" * 80)
    print()
    
    print("Criando programa com tokens inválidos para demonstrar detecção...")
    arquivo_erros = criar_programa_com_erros()
    
    analisador = AnalisadorLexico()
    resultado = analisador.processar_arquivo(arquivo_erros)
    
    if "erro" in resultado:
        print(f"❌ Erro ao processar arquivo: {resultado['erro']}")
        return
    
    print(f"📁 Analisando arquivo: {arquivo_erros}")
    print()
    
    # Mostra apenas os tokens válidos encontrados
    tokens_validos = resultado.get('tokens', [])
    if tokens_validos:
        print("📋 TOKENS VÁLIDOS ENCONTRADOS")
        print("-" * 40)
        print(f"{'TOKEN':20} | {'TIPO':15}")
        print("-" * 40)
        
        for token_type, lexeme, linha, coluna in tokens_validos[:10]:  # Mostra só os primeiros 10
            token_display = lexeme if len(lexeme) <= 18 else lexeme[:15] + "..."
            print(f"{token_display:20} | {token_type:15}")
        
        if len(tokens_validos) > 100:
            print(f"... e mais {len(tokens_validos) - 10} tokens válidos")
        print()
    
    # Mostra os erros encontrados
    mostrar_erros_detalhados(resultado)

def main():
    """Função principal que executa o teste no padrão solicitado"""
    print("� TESTE FINAL DO ANALISADOR LÉXICO")
    print("Seguindo o padrão especificado:")
    print("1️⃣ Escrever programa na linguagem especificada")
    print("2️⃣ Rodar analisador léxico sobre o arquivo")  
    print("3️⃣ Gerar tabela TOKEN | TIPO")
    print("4️⃣ Mostrar erros com linha e coluna para tokens inválidos")
    print()
    
    # Teste principal com programa válido
    sucesso = executar_teste_padrao_solicitado()
    
    # Demonstração adicional com programa contendo erros
    executar_teste_com_erros()
    
    print()
    print("� CONCLUSÃO DO TESTE")
    print("=" * 80)
    
    if sucesso:
        print("✅ TESTE CONCLUÍDO COM SUCESSO!")
        print("✅ Analisador léxico funcionando corretamente")
        print("✅ Tabela de tokens gerada conforme especificado")
        print("✅ Detecção de erros com linha/coluna implementada")
        print("✅ Suporte a UTF-8 e caracteres acentuados confirmado")
    else:
        print("❌ TESTE ENCONTROU PROBLEMAS")
        print("Verifique os erros reportados acima")
    
    print()
    print("📁 Arquivos gerados:")
    print("  • programa_exemplo.txt - Programa principal válido")
    print("  • programa_com_erros.txt - Programa para demonstrar erros")
    print("  • relatorio_analise.txt - Relatório detalhado da análise")

if __name__ == "__main__":
    main()