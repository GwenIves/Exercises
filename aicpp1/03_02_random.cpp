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

	bool * found = new bool[N];

	for (int i = 0; i < N; i++)
		found[i] = false;

	int count_before_duplicate = 0;
	int count_before_all = 0;
	int count = 0;
	int encountered = 0;

	while (count_before_duplicate == 0 || count_before_all == 0) {
		int val = rand () % N;

		count++;

		if (found[val]) {
			if (count_before_duplicate == 0)
				count_before_duplicate = count;
		} else {
			found[val] = true;

			if (++encountered == N)
				count_before_all = count;
		}
	}

	cout << "Random numbers before repeat          : " << count_before_duplicate << endl;
	cout << "Random numbers before each value found: " << count_before_all << endl;

	delete[] found;

	return 0;
}
