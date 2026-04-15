# Given an array of integers, find the k-th largest number in it.
#
# Example One
# {
# "numbers": [5, 1, 10, 3, 2],
# "k": 2
# }



def pair_sum_sorted_array(numbers, target):
    # solve using hashmap
    freq = {} # to store the numbers and teh difference
    for i in range(len(numbers)):
        diff = target - numbers[i]
        if diff in freq:
            return [numbers.index(diff), i]
        freq[numbers[i]] = freq.get(numbers[i], 0) + 1
    return[-1 ,-1]

print(pair_sum_sorted_array(numbers, target))