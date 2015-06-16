#include <iostream>
#include "point.hpp"

using namespace std;

int main () {
	Point a (cin), b (cin), c (cin);

	if (Point::collinear (a, b, c))
		cout << "Collinear" << endl;
	else
		cout << "Not collinear" << endl;

	return 0;
}
