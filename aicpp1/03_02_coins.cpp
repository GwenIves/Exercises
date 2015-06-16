#include <iostream>
#include <cstdlib>

using namespace std;

static inline bool heads (int x = 1, int y = 2);

int main (int argc, char ** argv) {
	if (argc != 5) {
		cerr << argv[0] << " <M> <N> <X> <Y>" << endl;
		return 1;
	}

	int M = atoi (argv[1]);
	int N = atoi (argv[2]);
	int X = atoi (argv[3]);
	int Y = atoi (argv[4]);

	if (M <= 0 || N <= 0 || X <= 0 || Y <= 0)
		return 1;

	int * f = new int[M + 1];

	for (int i = 0; i <= M; i++)
		f[i] = 0;

	for (int i = 0; i < N; i++) {
		int count = 0;

		for (int j = 0; j < M; j++)
			if (heads (X, Y))
				count++;

		f[count] += 1;
	}

	for (int i = 0; i <= M; i++) {
		if (f[i] == 0)
			cout << ".";

		for (int j = 0; j < f[i]; j += 10)
			cout << "*";

		cout << endl;
	}

	delete[] f;

	return 0;
}

static inline bool heads (int x, int y) {
	return rand () < RAND_MAX / y * x;
}
