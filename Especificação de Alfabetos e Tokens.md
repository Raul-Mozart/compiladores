**Especificação completa do alfabeto da linguagem**

Alfabeto:{a-z,A-Z,0-9,\!,@,\#,$,&,.,+,-,\*,/,%,(,),\>,\<,=,”,’,{,},\[,\],;,,,:,\\};  
camelCase;

Definição formal de todos os tipos de tokens

Tokens: if,else, else if,for,while,function,string,int,float,bool,list,var,in,class,return,+,-,\*,/,%,and,or,\<,\>,\<=,\>=,=,==,{,},\[,\],(,),.,**,**,;,:,\\n,\\,not

Exemplos concretos de programas válidos na linguagem

1\)  
float numero \= 10.0;

function parImpar(num)  
{  
  if (num % 2 \== 0\)  
{  
return “É par”;  
} else  
{  
	return “É impar”  
}  
}

print(parImpar(numero));

2\)

list numeros \= \[1,2,3,4,5\];

for (var i \= 0; i \< 5; i \= i \+ 1\)  
{  
	numeros\[i\] \= numeros\[i\] \+ 1;  
}

print(numeros)  
