## 問題

[Maximum Subarray - LeetCode](https://leetcode.com/problems/maximum-subarray/)

- 入力
    - `nums`: 整数配列
        - 長さは1以上10^5以下
        - 値は-10^4以上10^4以下
        - 和の範囲は-10^9以上10^9以下
            - Pythonでは整数の範囲は無制限
- 出力
    - 和が最大となる部分配列を探す
    - その和を返す
    - 部分配列: 元の配列の、連続した空でない列

## 解法

### 1. DP

- 2次元配列 `sum[i, j]` を考える
    - 行のインデックス `i` は部分配列の先頭
    - 列のインデックス `j` は部分配列の末尾
- `sum[i, j] = sum[i, j - 1] + num[j]`
    - `j > 0`
- 和の最大値を更新していく
- 時間計算量
    - O(n^2) となる
    - 今回だと10^10
    - 10^7 ステップ/秒とすると10^3秒
        - TLEしそう
- 空間計算量
    - O(n^2) となる
    - 今回だと10^10
    - python の int のサイズは最低28バイトらしい
        - あとで調べる
    - 28バイトの場合28*10^10 = 280GB
        - 動かない

### 2. DP改

- 上の空間計算量をO(n)にする
    - 時間計算量は変わらないのでTLEしそう

## Step1

### 1.

Memory Limit Exceeded した。

```py
import math

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        if not nums:
            return 0

        n = len(nums)
        sums_table: list[list[int]] = [[0] * n for _ in range(n)]
        max_sum: float | int = -math.inf

        for i in range(n):
            sums_table[i][i] = nums[i]
            max_sum = max(max_sum, sums_table[i][i])

            for j in range(1, i):
                sums_table[i][j] = sums_table[i][j - 1] + nums[j]
                max_sum = max(max_sum, sums_table[i][j])

        return int(max_sum)
```

### 2.

Time Limit Exceeded した

```py
import math


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        if not nums:
            return 0

        n = len(nums)
        sums: list[int] = [0] * n
        max_sum: float | int = -math.inf

        for i in range(n):
            sums[i] = nums[i]
            max_sum = max(max_sum, sums[i])

            for j in range(i):
                sums[j] = sums[j] + nums[i]
                max_sum = max(max_sum, sums[j])

        return int(max_sum)
```

## Step2

leetcode の解答を見た。
- 引き継いだ和
- 現在の値
- 「引き継いだ和 + 現在の値」と「現在の値」を比較して、大きい方を和とする

```py
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        if not nums:
            return 0

        max_sum = nums[0]
        running_sum = nums[0]
        for num in nums[1:]:
            running_sum = max(num, running_sum + num)
            max_sum = max(max_sum, running_sum)

        return max_sum
```

- `running_sum + num > num` は `running_sum > 0` と同じ
- python スライスはコピーされる
    - go と異なる
    - インデックスでループする

```py
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        if not nums:
            return 0

        max_sum = nums[0]
        running_sum = nums[0]
        for i in range(1, len(nums)):
            running_sum = max(nums[i], running_sum + nums[i])
            max_sum = max(max_sum, running_sum)

        return max_sum
```

### レビューを依頼する方のPR

- [53. Maximum Subarray by TakayaShirai · Pull Request #31 · TakayaShirai/leetcode_practice](https://github.com/TakayaShirai/leetcode_practice/pull/31)
    - 分割統治の解法もある
    - Kadane のアルゴリズムと呼ばれている
- [53. maximum subarray by 5ky7 · Pull Request #33 · 5ky7/arai60](https://github.com/5ky7/arai60/pull/33)
- [53. Maximum Subarray by dxxsxsxkx · Pull Request #32 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/32)
- [53. Maximum Subarray by mamo3gr · Pull Request #30 · mamo3gr/arai60](https://github.com/mamo3gr/arai60/pull/30)
- [solve: 53.Maximum Subarray by t9a-dev · Pull Request #32 · t9a-dev/LeetCode_arai60](https://github.com/t9a-dev/LeetCode_arai60/pull/32)
- まだ理解できてないので、時間を空けて考えてみる

## Step3

```py
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        if not nums:
            return 0

        max_sum = nums[0]
        running_sum = nums[0]
        for i in range(1, len(nums)):
            running_sum = max(nums[i], running_sum + nums[i])
            max_sum = max(max_sum, running_sum)
        
        return max_sum
```
