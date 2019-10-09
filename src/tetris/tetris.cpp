#include "tetris.hpp"

int main() {

	if (SDL_Init(SDL_INIT_VIDEO)) {
		cerr << "\n\n SDL_Init error:\t" << SDL_GetError() << endl;
		exit(-1);
	}

	SDL_Window *wnMain = SDL_CreateWindow("Hello", SDL_WINDOWPOS_CENTERED,
			SDL_WINDOWPOS_CENTERED, 800, 600, 0);

	if (!wnMain) {
		cerr << "\n\n SDL_CreateWindow error:\t" << SDL_GetError() << endl;
		SDL_Quit();
		exit(-1);
	}

	SDL_Renderer *render = SDL_CreateRenderer(wnMain, -1,
			SDL_RENDERER_ACCELERATED);
	if (!render) {
		cerr << "\n\n SDL_CreateRenderer error:\t" << SDL_GetError() << endl;
		SDL_DestroyWindow(wnMain); SDL_Quit();
		exit(-1);
	}

	SDL_Surface *back = IMG_Load("back.jpg");
	if (!back) {
		cerr << "\n\n SDL_Load error:\t" << SDL_GetError() << endl;
		SDL_DestroyWindow(wnMain); SDL_Quit();
		exit(-1);
	}

	SDL_Texture *txback = SDL_CreateTextureFromSurface(render, back);
	SDL_FreeSurface(back);
	if (!txback) {
		cerr << "\n\n SDL_CreateTextureFromSurface error:\t" << SDL_GetError() << endl;
		SDL_DestroyWindow(wnMain); SDL_Quit();
		exit(-1);
	}

	SDL_RenderClear(render);
	SDL_RenderCopy(render, txback, NULL, NULL);
	SDL_RenderPresent(render);

	SDL_Delay(5555);

	SDL_DestroyWindow(wnMain); SDL_Quit();
}
