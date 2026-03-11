import bisect


class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        tails: list[int] = []

        for v in nums:
            i = bisect.bisect_left(tails, v)
            if len(tails) == i:
                tails.append(v)
            else:
                tails[i] = v

        return len(tails)
