#include <iostream>
#include <vector>
#include <unistd.h>

using namespace std;

template <typename t> static void test_integral_sieve (size_t);
static void test_vector_sieve (size_t);

int main (int argc, char ** argv) {
	char method = 'i';

	int arg = 0;

	while ((arg = getopt (argc, argv, "t:")) != -1) {
		switch (arg) {
			case 't':
				method = optarg[0];
				break;
			case '?':
			default:
				break;
		}
	}

	if (argc - optind != 1) {
		cerr << argv[0] << " <N> -t <i:integer|c:char|v:vector>" << endl;
		return 1;
	}

	int N = atoi (argv[optind]);

	if (N <= 0 || (method != 'i' && method != 'c' && method != 'v'))
		return 1;

	switch (method) {
		case 'i':
			test_integral_sieve <int> (N);
			break;
		case 'c':
			test_integral_sieve <char> (N);
			break;
		case 'v':
			test_vector_sieve (N);
			break;
		default:
			break;
	}

	return 0;
}

template <typename t> static void test_integral_sieve (size_t size) {
	t * primes = new t[size];

	for (size_t i = 2; i < size; i++)
		primes[i] = 1;

	for (size_t i = 2; i < size; i++) {
		if (!primes[i])
			continue;

		for (size_t j = i * i; j < size; j += i)
			primes[j] = 0;
	}

	int count = 0;

	for (size_t i = 2; i < size; i++)
		if (primes[i])
			count++;

	cout << count << " primes under " << size << endl;

	delete[] primes;
}

static void test_vector_sieve (size_t size) {
	vector<int> primes (size, 1);

	for (size_t i = 2; i < size; i++) {
		if (!primes[i])
			continue;

		for (size_t j = i * i; j < size; j += i)
			primes[j] = 0;
	}

	int count = 0;

	for (size_t i = 2; i < size; i++)
		if (primes[i])
			count++;

	cout << count << " primes under " << size << endl;
}
