## 問題

[Permutations - LeetCode](https://leetcode.com/problems/permutations/)

- 入力
    - `nums`: 重複のない整数のリスト
        - 長さは0以上6以下
        - 値は-10以上10以下
- 出力
    - `nums` の順列のリスト

## 解法

### 1. 再帰で順列を構築する

- `nums` の長さは6なので、単純な方法でもパスしそう
- 「選択済み」と「選択前」のリストに分けて再帰する
    - 「選択前」のリストが空になったら終了
- 時間計算量: O(n * n!)
    - 再帰は O(n!)
        - `1 + n + n(n - 1) + ... +  n!`
    - 各再帰実行時にリストのコピーに O(n)
- 空間計算量: O(n * n!)
    - 戻り値のリストのサイズは O(n * n!)
    - 再帰の深さは O(n)
    - 各再帰で作るリストは O(n)
    - O(n * n! + n*n) -> O(n * n!)

## Step1

### 1. 

```python
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:

        result: List[List[int]] = []

        def _permute(selected: List[int], candidates: List[int]) -> None:
            if not candidates:
                result.append(selected)
                return

            for c in candidates:
                new_selected = selected + [c]
                new_candidates = [e for e in candidates if e != c]
                _permute(new_selected, new_candidates)

        _permute([], nums)

        return result
```

## Step2

- leetcode の解答を見た
- 各再帰でリストを作らなくても、スワップで同等の状況を実装できる

```py
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:

        result: List[List[int]] = []

        def _permute(start: int) -> None:
            if start == len(nums):
                result.append(nums[:])
                return

            for i in range(start, len(nums)):
                nums[start], nums[i] = nums[i], nums[start]
                _permute(start + 1)
                nums[start], nums[i] = nums[i], nums[start]

        _permute(0)

        return result
```

### レビューを依頼する方のPR

- [Permutations by Yuto729 · Pull Request #54 · Yuto729/LeetCode_arai60](https://github.com/Yuto729/LeetCode_arai60/pull/54)
    - バックトラック
    - Python のコピー周りを理解できていない
- [46. Permutations by tom4649 · Pull Request #47 · tom4649/Coding](https://github.com/tom4649/Coding/pull/47)
    - next permutationというアルゴリズムがある
    - `itertools.permutations` が使える
- [46. Permutations by dxxsxsxkx · Pull Request #50 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/50)
- [46. Permutations by mamo3gr · Pull Request #47 · mamo3gr/arai60](https://github.com/mamo3gr/arai60/pull/47)
    - `remaining` とか `used` とか
- いろいろやり方がある問題だった

## Step3

```py
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:

        result: List[List[int]] = []

        def _permute(start: int) -> None:
            if start == len(nums):
                result.append(nums[:])
                return

            for i in range(start, len(nums)):
                nums[start], nums[i] = nums[i], nums[start]
                _permute(start + 1)
                nums[start], nums[i] = nums[i], nums[start]

        _permute(0)

        return result
```
