#include <iostream>
#include <cstdlib>

using namespace std;

int main (int argc, char ** argv) {
	if (argc != 2) {
		cerr << argv[0] << " <N>" << endl;
		return 1;
	}

	int N = atoi (argv[1]);

	if (N <= 0)
		return 1;

	int * ids = new int[N];
	int * heights = new int[N];

	for (int i = 0; i < N; i++) {
		ids[i] = i;
		heights[i] = 1;
	}

	int connections = 0;
	int edges = 0;

	while (connections < N - 1) {
		int p = rand () % N;
		int q = rand () % N;

		edges++;

		int i = 0;
		int j = 0;

		for (i = p; ids[i] != i; i = ids[i])
			;
		for (j = q; ids[j] != j; j = ids[j])
			;

		if (i == j)
			continue;

		if (heights[i] < heights[j]) {
			ids[i] = j;
		} else {
			ids[j] = i;

			if (heights[i] == heights[j])
				heights[i] += 1;
		}

		connections++;
	}

	cout << "Random edges required to connect " << N << " vertices: " << edges << endl;

	delete[] ids;
	delete[] heights;

	return 0;
}
