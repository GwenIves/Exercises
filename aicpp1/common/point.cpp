#include <cmath>
#include "point.hpp"

using namespace std;

Point::Point (istream & in) {
	in >> x >> y;
}

bool Point::collinear (const Point & a, const Point & b, const Point & c) {
	return fabs (a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y)) < 0.0001;
}
