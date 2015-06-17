#ifndef TRIANGLE_H_
#define TRIANGLE_H_

#include "point.hpp"
#include "math_utils.hpp"

class Triangle {
	public:
		Triangle (): x (frand (), frand ()), y (frand (), frand ()), z (frand (), frand ()) {}

		double area ();
	private:
		Point x;
		Point y;
		Point z;
};

#endif
