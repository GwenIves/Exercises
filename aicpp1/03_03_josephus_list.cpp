#include <iostream>

using namespace std;

struct node {
	int item;
	node * next;

	node (int i): item (i) {};
};

typedef node * link;

int main (int argc, char ** argv) {
	if (argc != 3) {
		cerr << argv[0] << " <M> <N>" << endl;
		return 1;
	}

	int M = atoi (argv[1]);
	int N = atoi (argv[2]);

	if (M <= 0 || N <= 0)
		return 1;

	link t = new node (1);
	t->next = t;

	link x = t;

	for (int i = 2; i <= N; i++) {
		x->next = new node (i);
		x = x->next;
	}

	x->next = t;

	while (x != x->next) {
		for (int i = 1; i < M; i++)
			x = x->next;

		t = x->next;
		x->next = t->next;
		delete t;
	}

	cout << x->item << endl;

	delete x;

	return 0;
}
