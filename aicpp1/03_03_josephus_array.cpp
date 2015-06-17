#include <iostream>

using namespace std;

int main (int argc, char ** argv) {
	if (argc != 3) {
		cerr << argv[0] << " <M> <N>" << endl;
		return 1;
	}

	int M = atoi (argv[1]);
	int N = atoi (argv[2]);

	if (M <= 0 || N <= 0)
		return 1;

	int * items = new int[N];
	int * next = new int[N];

	for (int i = 0; i < N; i++) {
		items[i] = i + 1;
		next[i] = (i + 1) % N;
	}

	int i = N - 1;

	while (i != next[i]) {
		for (int j = 1; j < M; j++)
			i = next[i];

		next[i] = next[next[i]];
	}

	cout << items[i] << endl;

	delete[] items;
	delete[] next;

	return 0;
}
