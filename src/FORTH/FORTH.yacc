%{
#include "FORTH.h"
%}

%defines %union { char *sym; }

%token <sym> SYM

%%
REPL : | REPL SYM { printf("<%s>\n",$2); }
