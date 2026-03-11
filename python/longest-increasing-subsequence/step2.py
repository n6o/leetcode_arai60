class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        tails: list[int] = []

        for n in nums:
            i = self._find_insertion_index(tails, n)
            if len(tails) == i:
                tails.append(n)
            else:
                tails[i] = n

        return len(tails)

    def _find_insertion_index(self, tails: list[int], target: int) -> int:
        min_index = 0
        max_index = len(tails)

        while min_index < max_index:
            mid = (min_index + max_index) // 2

            if tails[mid] < target:
                min_index = mid + 1
            else:
                max_index = mid

        return min_index
