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

passes = [x for x in range(172_930, 683083) if validator(x)]
print(len(passes))
