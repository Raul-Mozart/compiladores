# Mensagens de erro para usuários

### Caractere inválido
```txt
LEX001 [L8:12] Caractere inválido: '@'.
x = 10 @ 20
       ^
Erro: '@' não pertence ao alfabeto (Σ) nem a nenhuma ER de token definida.
```

---

### String não terminada
```txt
LEX002 [L3:5] String não terminada.
nome = "Maria
        ^
Erro: feche o delimitador para reconhecer a cadeia na linguagem de strings (ER).
```

---

### Número malformado
```txt
LEX003 [L5:9] Número malformado: '12.3.4'.
num = 12.3.4
          ^
Erro: a expressão regular do número permite no máximo um ponto decimal.
```

### Comentário de bloco não fechado
```txt
LEX004 [L7:1] Comentário de bloco não terminado.
/* este é um comentário
^
Erro: feche o comentário com '*/' para pertencer à linguagem de comentários de bloco.
```
