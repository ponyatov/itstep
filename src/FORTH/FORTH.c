#include "FORTH.h"

extern void yyerror(char* msg) {
	fprintf(stderr, "\n\n%i\t%s\t[%s]\n\n", yylineno, msg, yytext);
	exit(-1);
}

int main() {
	return yyparse();
}
