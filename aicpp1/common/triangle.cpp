#include <cstdlib>
#include <cmath>
#include "triangle.hpp"

double Triangle::area () {
	double a = x.distance (y);
	double b = y.distance (z);
	double c = z.distance (x);

	double s = (a + b + c) / 2;

	return sqrt (s * (s - a) * (s - b) * (s - c));
}
