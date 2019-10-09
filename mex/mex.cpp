#include "mex.hpp"

int main(int argc, char *argv[]) {
	for (int i = 0; i < argc; i++)
		cout << "argv[" << i << "]=" << argv[i] << endl;
	assert(argc == 2);

}
