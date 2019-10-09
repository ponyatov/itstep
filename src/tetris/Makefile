all: go

go: ./tetris$(EXE)
	./tetris$(EXE)

C += tetris.cpp
H += tetris.hpp
L += -lSDL2 -lSDL2_image
	
./tetris$(EXE): $(C) $(H) Makefile
	$(CXX) $(CXXFLAGS) -o $@ $(C) $(L)
	