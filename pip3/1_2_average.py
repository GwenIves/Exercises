#!/bin/env python3

def get_int():
    while True:
        try:
            inp = input("Enter a number: ")

            if not inp:
                return None
            else:
                return int(inp)
        except ValueError as err:
            print(err)
        except EOFError:
            print()
            return None

def get_median(nums):
    nums = sorted(nums)
    size = len(nums)

    if size % 2 == 1:
        return nums[size // 2]
    else:
        return(nums[size // 2] + nums[size // 2 - 1]) / 2

def main():
    numbers = []

    while True:
        i = get_int()

        if not i:
            break

        numbers.append(i)

    if numbers:
        print(numbers)

        count = len(numbers)
        num_sum = sum(numbers)
        median = get_median(numbers)

        fmt = "Count = {} Sum = {} Lowest = {} Highest = {} Mean = {} Median = {}"
        print(fmt.format(count, num_sum, min(numbers), max(numbers), num_sum / count, median))

if __name__ == '__main__':
    main()
