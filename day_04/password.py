from collections import Counter


def digits(num):
    return tuple(map(int, str(num)))


def validator(num):
    nums = digits(num)
    adjacent = False
    monotonic = True
    for i, dig in enumerate(nums):
        if i < 5:
            if dig == nums[i + 1]:
                adjacent = True
        if any(dig > y for y in nums[i + 1 :]):
            monotonic = False
    return adjacent & monotonic


assert validator(111111)
assert ~validator(223450)
assert ~validator(123789)

passes = [x for x in range(172_930, 683_083) if validator(x)]
print(len(passes))


def validator2(num):
    nums = digits(num)
    adjacent = False
    monotonic = True
    for i, dig in enumerate(nums):
        if any(dig > y for y in nums[i + 1 :]):
            monotonic = False
    if any(val == 2 for val in Counter(nums).values()):
        adjacent = True
    return adjacent & monotonic


assert validator2(112233)
assert ~validator2(123444)
assert validator2(111122)

passes = [x for x in range(172_930, 683_083) if validator2(x)]
print(len(passes))
