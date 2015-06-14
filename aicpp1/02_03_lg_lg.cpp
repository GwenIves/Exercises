#include <iostream>

using namespace std;

static inline int lg_lg (int);

int main (int argc, char ** argv) {
	if (argc != 2) {
		cerr << argv[0] << " <N>" << endl;
		return 1;
	}

	int N = atoi (argv[1]);

	if (N <= 0)
		return 1;

	cout << lg_lg (N) << endl;

	return 0;
}

static inline int lg_lg (int N) {
	int y = 0;

	while (N > 0) {
		y++;
		N >>= 2;
	}

	return y;
}
