#include <iostream>
#include <cstdlib>
#include <cmath>
#include <unistd.h>

using namespace std;

int main (int argc, char ** argv) {
	bool transform = false;

	int arg = 0;

	while ((arg = getopt (argc, argv, "t")) != -1) {
		switch (arg) {
			case 't':
				transform = true;
				break;
			case '?':
			default:
				break;
		}
	}

	if (argc - optind != 2) {
		cerr << argv[0] << " <N> <R>" << endl;
		return 1;
	}

	int N = atoi (argv[optind]);
	int R = atoi (argv[optind + 1]);

	if (N <= 0 || R <= 0)
		return 1;

	long sum = 0;
	long sum_squares = 0;

	for (int i = 0; i < N; i++) {
		int r = 0;

		if (transform) {
			double rd = (double) rand () / RAND_MAX;
			r = rd * R;
		} else {
			r = rand () % R;
		}

		sum += r;
		sum_squares += r * r;
	}

	double avg = (double) sum / N;

	cout << " Average: " << avg << endl;
	cout << "Std. dev: " << sqrt ((double) sum_squares / N - avg * avg) << endl;

	return 0;
}
