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
	int * sizes = new int[N];

	for (int i = 0; i < N; i++) {
		ids[i] = i;
		sizes[i] = 1;
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

		for (int ii = p; ids[ii] != ii;) {
			int t = ii;
			ii = ids[ii];
			ids[t] = i;
		}

		for (int jj = p; ids[jj] != jj;) {
			int t = jj;
			jj = ids[jj];
			ids[t] = j;
		}

		if (i == j)
			continue;

		if (sizes[i] < sizes[j]) {
			ids[i] = j;
			sizes[j] += sizes[i];
		} else {
			ids[j] = i;
			sizes[i] += sizes[j];
		}

		connections++;
	}

	cout << "Random edges required to connect " << N << " vertices: " << edges << endl;

	delete[] ids;
	delete[] sizes;

	return 0;
}
