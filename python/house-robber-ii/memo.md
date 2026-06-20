## 問題

[House Robber II - LeetCode](https://leetcode.com/problems/house-robber-ii/description/)

- 入力
    - `nums`: 家から盗める金額のリスト
        - 最初の家は最後の家の隣にある(環状に並んでいる)
        - 長さは1以上100以下
        - 値は0以上1000以下
- 出力
    - 警報を鳴らさずに盗める金額の最大値
        - 隣り合う家から盗むと警報が鳴る

## 解法

### 1. DP

- 最後の家から盗む場合、最初の家からは盗めない
- 最後の家から盗まない場合、最初の家から盗める
- 最初の家から盗む場合と最初の家から盗まない場合を考える
- 時間計算量
    - 各場合の時間計算量は O(n)
    - 全体でも O(n)
- 空間計算量
    - O(n)

## Step1

### 1.

- とりあえず `helper` という名前にした
    - `_rob` くらいしか思いつかなかった

```py
class Solution:
    def helper(self, nums: List[int], robFromLast: bool) -> int:
        max_amounts = [0] * len(nums)
        max_amounts[0] = 0 if robFromLast else nums[0]
        max_amounts[1] = max(max_amounts[0], nums[1])
        for i in range(2, len(nums)):
            max_amounts[i] = max(max_amounts[i - 1], max_amounts[i - 2] + nums[i])
        return max_amounts[-1] if robFromLast else max_amounts[-2]

    def rob(self, nums: List[int]) -> int:
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]

        return max(
            self.helper(nums, True),
            self.helper(nums, False),
        )
```

## Step2

### レビューを依頼する方のPR

- [213. House Robber II by TakayaShirai · Pull Request #35 · TakayaShirai/leetcode_practice](https://github.com/TakayaShirai/leetcode_practice/pull/35)
    - 0 - n-1 の範囲での値と 1 - n の範囲での値を比べれば良かった
    - `helper` を `rob_with_range` とかにできそう
    - `islice` が使える
        - イテレーターなので `len` が使えなかった
- [213. house robber ii by 5ky7 · Pull Request #37 · 5ky7/arai60](https://github.com/5ky7/arai60/pull/37)
- [213. House Robber II by mamo3gr · Pull Request #34 · mamo3gr/arai60](https://github.com/mamo3gr/arai60/pull/34)
    - `linearly` はよさそうと思った
- [213. House Robber II by garunitule · Pull Request #36 · garunitule/coding_practice](https://github.com/garunitule/coding_practice/pull/36)

```py
class Solution:
    def rob(self, nums: List[int]) -> int:
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]

        def rob_with_range(start, end: int) -> int:
            max_robbed_two_houses_ago = 0
            max_robbed_one_house_ago = 0
            for i in range(start, end):
                amount = max(
                    max_robbed_one_house_ago, max_robbed_two_houses_ago + nums[i]
                )
                max_robbed_two_houses_ago = max_robbed_one_house_ago
                max_robbed_one_house_ago = amount
            return max_robbed_one_house_ago

        return max(
            rob_with_range(0, len(nums) - 1),
            rob_with_range(1, len(nums)),
        )
```

## Step3

```py
class Solution:
    def rob(self, nums: List[int]) -> int:
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]

        def rob_with_range(start, end: int) -> int:
            max_robbed_two_houses_ago = 0
            max_robbed_one_house_ago = 0
            for i in range(start, end):
                amount = max(
                    max_robbed_one_house_ago, max_robbed_two_houses_ago + nums[i]
                )
                max_robbed_two_houses_ago = max_robbed_one_house_ago
                max_robbed_one_house_ago = amount
            return max_robbed_one_house_ago

        return max(
            rob_with_range(0, len(nums) - 1),
            rob_with_range(1, len(nums)),
        )
```
