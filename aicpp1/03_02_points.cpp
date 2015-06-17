#include <iostream>
#include <cstdlib>
#include <vector>
#include "point.hpp"

using namespace std;

int main (int argc, char ** argv) {
	if (argc != 3) {
		cerr << argv[0] << " <M> <N>" << endl;
		return 1;
	}

	int M = atoi (argv[1]);
	int N = atoi (argv[2]);

	if (M <= 0 || N <= 1)
		return 1;

	vector<PointMD> points;
	points.reserve (N);

	for (int i = 0; i < N; i++)
		points.push_back (PointMD (M));

	double min_distance = points[0].distance (points[1]);

	for (int i = 0; i < N; i++)
		for (int j = i + 1; j < N; j++) {
			double distance = points[i].distance (points[j]);

			if (distance < min_distance)
				min_distance = distance;
		}

	cout << "Min. distance: " << min_distance << endl;

	return 0;
}
