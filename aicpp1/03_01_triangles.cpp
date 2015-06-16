#include <iostream>
#include "triangle.hpp"

using namespace std;

int main (int argc, char ** argv) {
	if (argc != 2) {
		cerr << argv[0] << " <N>" << endl;
		return 1;
	}

	int N = atoi (argv[1]);

	if (N <= 0)
		return 1;

	for (int i = 0; i < N; i++) {
		Triangle t;

		cout << "Area: " << t.area () << endl;
	}

	return 0;
}
