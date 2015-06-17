#include <cmath>
#include "point.hpp"
#include "math_utils.hpp"

using namespace std;

Point::Point (istream & in) {
	in >> x >> y;
}

bool Point::collinear (const Point & a, const Point & b, const Point & c) {
	return fabs (a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y)) < 0.0001;
}

double Point::distance (const Point & a) {
	double dx = x - a.x;
	double dy = y - a.y;

	return sqrt (dx * dx + dy * dy);
}

PointMD::PointMD (int d = 0) {
	dimensions = d;

	if (dimensions <= 0) {
		coords = 0;
		return;
	}

	coords = new double[dimensions];

	for (int i = 0; i < dimensions; i++)
		coords[i] = frand ();
}

PointMD::PointMD (const PointMD & p) {
	copy_coords (p);
}

PointMD & PointMD::operator= (const PointMD & rhs) {
	if (this != &rhs) {
		delete[] coords;
		copy_coords (rhs);
	}

	return *this;
}

PointMD::~PointMD () {
	delete[] coords;
}

double PointMD::distance (const PointMD & a) {
	double d = 0.0;

	for (int i = 0; i < dimensions; i++) {
		double di = coords[i] - a.coords[i];

		d += di * di;
	}

	return sqrt (d);
}

void PointMD::copy_coords (const PointMD & obj) {
	dimensions = obj.dimensions;

	if (dimensions <= 0) {
		coords = 0;
		return;
	}

	coords = new double[dimensions];

	for (int i = 0; i < dimensions; i++)
		coords[i] = obj.coords[i];
}
