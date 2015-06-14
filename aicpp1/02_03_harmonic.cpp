#include <iostream>
#include <cmath>

using namespace std;

static inline double harmonic_number (int);

int main (int argc, char ** argv) {
	if (argc != 2) {
		cerr << argv[0] << " <N>" << endl;
		return 1;
	}

	int N = atoi (argv[1]);

	if (N <= 0)
		return 1;

	cout << harmonic_number (N) << endl;

	return 0;
}

static inline double harmonic_number (int N) {
	static const double gamma = 0.57721;

	return log (N) + gamma + 1.0 / (12 * N);
}
