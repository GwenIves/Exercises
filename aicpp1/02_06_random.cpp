#include <iostream>
#include <cstdlib>

using namespace std;

static ssize_t search (const int *, size_t, size_t, int);

int main (int argc, char ** argv) {
	if (argc != 3) {
		cerr << argv[0] << " <M> <N>" << endl;
		return 1;
	}

	int M = atoi (argv[1]);
	int N = atoi (argv[2]);

	if (N <= 0 || M <= 0)
		return 1;

	int * vals = new int[M];

	for (int i = 0; i < M; i++)
		vals[i] = rand ();

	int found = 0;

	for (int i = 0; i < N; i++)
		if (search (vals, 0, M - 1, rand ()) != -1)
			found++;

	cout << "Found " << found << "/" << N << " out of " << M << endl;

	delete[] vals;

	return 0;
}

static ssize_t search (const int * a, size_t l, size_t r, int val) {
	for (size_t i = l; i <= r; i++)
		if (a[i] == val)
			return i;

	return -1;
}
