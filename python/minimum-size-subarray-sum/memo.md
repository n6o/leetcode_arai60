## 問題

[Minimum Size Subarray Sum - LeetCode](https://leetcode.com/problems/minimum-size-subarray-sum/)

- 入力
    - `nums`: 正の整数の配列
        - 長さは1以上10^5以下
        - 要素の値は1以上10^4以下
    - `target`: 正の整数
        - 値は1以上10^9以下
- 出力
    - 和が `target` 以上となる最小の部分配列の長さ

## 解法

### 1. スライディングウインドウ

- `nums` の要素は正の整数
- ウインドウを広げながら和を加算
- 和が `target` 以上になったらウインドウサイズの最小長を更新し、ウインドウの和が `target` 未満になるまで縮める

## Step1

### 1. 

```py
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        min_subarray_length = len(nums) + 1
        window_start = 0
        subarray_sum = 0
        for i, n in enumerate(nums):
            subarray_sum += n
            while subarray_sum >= target:
                subarray_length = i - window_start + 1
                min_subarray_length = min(min_subarray_length, subarray_length)
                subarray_sum -= nums[window_start]
                window_start += 1

        if min_subarray_length == len(nums) + 1:
            return 0

        return min_subarray_length
```

## Step2

- `subarray_start` / `subarray_end` に揃える

```py
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        min_subarray_length = len(nums) + 1
        subarray_start = 0
        subarray_sum = 0
        for subarray_end, num in enumerate(nums):
            subarray_sum += num
            while subarray_sum >= target:
                subarray_length = subarray_end - subarray_start + 1
                min_subarray_length = min(min_subarray_length, subarray_length)
                subarray_sum -= nums[subarray_start]
                subarray_start += 1

        if min_subarray_length == len(nums) + 1:
            return 0

        return min_subarray_length
```

### follow-up

- O(n log n) の解法
- prefix_sum を求め、部分配列の和が `target` を越える最小の位置を探す
- 2分探索を使う部分で `prefix_sum[search_start] >= target_prefix_sum` のチェックを実装できなかった

```py
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        n = len(nums)
        prefix_sum = [0] * (n + 1)
        for i in range(n):
            prefix_sum[i + 1] = prefix_sum[i] + nums[i]

        min_subarray_length = n + 1

        for subarray_start in range(n):
            target_prefix_sum = prefix_sum[subarray_start] + target
            search_start = subarray_start + 1
            search_end = n
            while search_start < search_end:
                mid = (search_start + search_end) // 2
                if prefix_sum[mid] >= target_prefix_sum:
                    search_end = mid
                else:
                    search_start = mid + 1

            if prefix_sum[search_start] >= target_prefix_sum:
                min_subarray_length = min(
                    min_subarray_length, search_start - subarray_start
                )

        return 0 if min_subarray_length == n + 1 else min_subarray_length
```


### レビューを依頼する方のPR

## Step3

```py
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        min_subarray_length = len(nums) + 1
        subarray_start = 0
        subarray_sum = 0
        for subarray_end, num in enumerate(nums):
            subarray_sum += num
            while subarray_sum >= target:
                subarray_length = subarray_end - subarray_start + 1
                min_subarray_length = min(min_subarray_length, subarray_length)
                subarray_sum -= nums[subarray_start]
                subarray_start += 1

        if min_subarray_length == len(nums) + 1:
            return 0

        return min_subarray_length
```
