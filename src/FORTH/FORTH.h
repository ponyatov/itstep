#ifndef _H_FORTH
#define _H_FORTH

							// память программ/данных
#define Msz 0x1000
							// стек возвратов
#define Rsz 0x100
							// стек данных
#define Dsz	0x10

#define CELL (int)
#define BYTE (uint8_t)

#include <stdio.h>
#include <stdlib.h>

							// интерфейс лексера
extern int yylex();
extern int yylineno;
extern char *yytext;
							// интерфейс парсера
extern int yyparse();
extern void yyerror(char*);
#include "parser.h"

#endif // _H_FORTH
