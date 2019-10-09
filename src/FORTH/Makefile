run: ./FORTH$(EXE)
	./FORTH$(EXE)

C = FORTH.c parser.c lexer.c
H = FORTH.h parser.h

./FORTH$(EXE): $(C) $(H)
	$(CC) $(CFLAGS) -o $@ $(C) $(L)
	
#lexer.c: FORTH.ragel
#	ragel -G2 -o $@ $<

lexer.c: FORTH.lex
	flex -o $@ $<

parser.c: FORTH.yacc
	bison -o $@ $<
