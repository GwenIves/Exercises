#include <iostream>

using namespace std;

int main (int argc, char ** argv) {
	if (argc != 2) {
		cerr << argv[0] << " <N>" << endl;
		return 1;
	}

	int N = atoi (argv[1]);

	if (N <= 0)
		return 1;

	int count = 0;

	for (int i = 0; i < N; i++)
		for (int j = 0; j < N; j++)
			for (int k = 0; k < N; k++)
				count += k;

	return count;
}
