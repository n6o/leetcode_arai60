## 問題

[Subsets - LeetCode](https://leetcode.com/problems/subsets/description/)

- 入力
    - `nums`: 重複していない整数のリスト
        - 長さは1以上10以下
        - 値は-10以上10以下
- 出力
    - すべての部分集合のリスト
        - 重複した集合は含まない
        - 順序は任意

## 解法

### 1. n ビットで表せる整数に対応する集合を考える

- `num` は重複のない整数のリスト
- 各インデックスをn ビット整数の桁に見立てて、ビットが1となっている場所の要素を含む集合を列挙する
- 時間計算量はO(2^n * n)
- 空間計算量はO(2^n * n)

### 2. 木構造を使って集合を考える

- 「要素xを含む場合」と「要素xを含まない場合」を考えていく

## Step1

### 1.

```py
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        bitSize = len(nums)
        result = []
        for n in range(2 << (bitSize - 1)):
            subset = []
            for i in range(bitSize):
                if n & (1 << i):
                    subset.append(nums[i])

            result.append(subset)

        return result
```

### 2.

```py
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        if not nums:
            return [[]]

        head = nums[0]
        subset_list = self.subsets(nums[1:])

        subset_list_copy = [subset[:] for subset in subset_list]
        for subset in subset_list_copy:
            subset.append(head)
        
        subset_list.extend(subset_list_copy)
        return subset_list
```

## Step2

- leetcode の解答を見る
- 下記のコードがシンプルで

```py
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result = [[]]

        for num in nums:
            length = len(result)
            for i in range(length):
                result.append(result[i] + [num])

        return result
```

### レビューを依頼する方のPR

## Step3

```py
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result = [[]]

        for num in nums:
            length = len(result)
            for i in range(length):
                result.append(result[i] + [num])

        return result
```
