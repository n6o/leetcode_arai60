## 問題

[House Robber - LeetCode](https://leetcode.com/problems/house-robber/description/)

- 入力
    - `nums`: 整数配列
        - 各家で奪える金額
        - 長さは1以上100以下
        - 値は0以上400以下
- 出力
    - 警報を鳴らさずに奪える金額の最大値

## 解法

### 1. いわゆる動的計画法

- 長さが0の場合
    - 設定上は起きない
- 長さが1の場合
    - 負の値はないので奪う場合が答え
- 長さが2の場合
    - 0番目の金額と1番目の金額の大きい方
- 長さが3の場合
    - 0番目の金額と3番目の金額の和と1番目の金額の大きい方
    - 漸化式が書ける
- 時間計算量
    - O(n)
- 空間計算量
    - O(n)
        - 2個前だけが必要なためO(1)にもできそう

## Step1

```py
class Solution:
    def rob(self, nums: List[int]) -> int:
        if not nums:
            return 0

        if len(nums) == 1:
            return nums[0]

        max_robbed_amounts = [0] * len(nums)
        max_robbed_amounts[0] = nums[0]
        max_robbed_amounts[1] = max(nums[0], nums[1])

        for i in range(2, len(nums)):
            max_robbed_amounts[i] = max(
                max_robbed_amounts[i - 1], max_robbed_amounts[i - 2] + nums[i]
            )

        return max_robbed_amounts[-1]        
```

### 空間計算量O(1)の方法

```py
class Solution:
    def rob(self, nums: List[int]) -> int:
        max_robbed_two_houses_ago = 0 # 2つ前の家までで得られた最大金額
        max_robbed_one_house_ago = 0  # 1つ前の家までで得られた最大金額
        for n in nums:
            amount = max(max_robbed_one_house_ago, max_robbed_two_houses_ago + n)
            max_robbed_two_houses_ago = max_robbed_one_house_ago
            max_robbed_one_house_ago = amount
            
        return max_robbed_one_house_ago
```

## Step2

配列を利用する方が読みやすいと思った。

### レビューを依頼する方のPR

- [198. House Robber by TakayaShirai · Pull Request #34 · TakayaShirai/leetcode_practice](https://github.com/TakayaShirai/leetcode_practice/pull/34)
- [198. house robber by 5ky7 · Pull Request #36 · 5ky7/arai60](https://github.com/5ky7/arai60/pull/36)
    - 再帰も使える
- [198. House Robber by dxxsxsxkx · Pull Request #35 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/35)
- [198. House Robber by mamo3gr · Pull Request #33 · mamo3gr/arai60](https://github.com/mamo3gr/arai60/pull/33)
    - `itertools.islice` というものがある
        - `i` は iterator の `i` なのだろうか。馴染みがない。
    - 再帰では `@functools.cache` を使う必要があるよう
    - `xxxtools` を調べてみる

## Step3

```py
class Solution:
    def rob(self, nums: List[int]) -> int:
        if not nums:
            return 0

        if len(nums) == 1:
            return nums[0]

        max_robbed_amounts = [0] * len(nums)
        max_robbed_amounts[0] = nums[0]
        max_robbed_amounts[1] = max(nums[0], nums[1])

        for i in range(2, len(nums)):
            max_robbed_amounts[i] = max(
                max_robbed_amounts[i - 1], max_robbed_amounts[i - 2] + nums[i]
            )

        return max_robbed_amounts[-1]        
```
