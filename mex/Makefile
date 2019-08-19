.PHONY: all clean

all: mex.log

mex.log: ./mex$(EXE) mex.mex
	./$^ > $@ && tail $(TAIL) $@
	
C = mex.cpp mex.parser.cpp
H = mex.hpp

./mex$(EXE): $(C) $(H) Makefile
	$(CXX) $(CXXFLAGS) -o $@ $(C) $(L)

mex.parser.cpp: mex.ragel
	ragel -G2 -o $@ $<
