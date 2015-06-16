#ifndef POINT_H_
#define POINT_H_

#include <iostream>

class Point {
	public:
		Point (std::istream &);
		Point (double xx, double yy): x (xx), y (yy) {}

		double distance (const Point &);

		static bool collinear (const Point &, const Point &, const Point &);
	private:
		double x;
		double y;
};

#endif
