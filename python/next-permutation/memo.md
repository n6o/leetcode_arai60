## 問題

[Next Permutation - LeetCode](https://leetcode.com/problems/next-permutation/description/)

- 入力
    - `nums`: 整数配列
        - 長さは1以上100以下
        - 値は0以上100以下
- 出力
    - 辞書順で次となる並び方
        - `nums` が最後尾の場合は最初の並び方

## 解法

方針を立てられなかったので leetcode の解答を参照した。

1. 配列の右側から走査して `nums[i] < nums[i+1]` となるピボット `i` を探す
    - ピボットが見つからない場合 => 全体が降順となっている
    - 逆順にして最小の順列に戻す
2. ピボットの右側で、ピボットでの値より大きい最小値を探し、交換する
3. ピボットの右側を逆順にする
    - ピボットの右側は降順となっているため

- 時間計算量はO(n)
- 空間計算量はO(1)

### 考え方

#### 「何を最小化/最大化するか」

- 「次の順列」を導出する方法を考えたい。
- 「次の順列」 => 「辞書順で増分が最小になるように並べ替える」
- 「増分が最小」 => 「できるだけ右側を変える」

#### 「観察する」

- 2桁の場合 => [1,2] と [2,1]
    - 昇順の場合と降順の場合
    - 降順の場合の方が大きい
- 3桁の場合 => [1,2,3] と [1,3,2]
    - 3桁目を固定すると、残りの2桁の順列で大小が決まる
    - 3桁目が変わるのは、残りの2桁が降順の場合
        - [1,3,2] => [2,1,3]
        - 1桁目と3桁目を交換し、そのあとで2桁目以降を反転している
            - MEMO: 自分で考えた時は、この操作に分解できなかった
    - 「降順」となっている => 「その配列での最大となる並び」 => 次は「桁上がり」みたいに考えられるといい
        - 「昇順」となるのが最小となる並び

## Step1

```py
class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        length = len(nums)
        pivot = -1
        
        for i in reversed(range(len(nums) - 1)):
            if nums[i] < nums[i + 1]:
                pivot = i
                break
            
        if pivot == -1:
            nums.reverse()
            return

        for j in reversed(range(pivot + 1, len(nums))):
            if nums[j] > nums[pivot]:
                nums[pivot], nums[j] = nums[j], nums[pivot]
                break
            
        start, end = pivot + 1, length - 1
        while start < end:
            nums[start], nums[end] = nums[end], nums[start]
            start += 1
            end -= 1
```

## Step2

- 関数を定義した

```py
class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """

        def search_pivot(nums: List[int]) -> int | None:
            for i in reversed(range(len(nums) - 1)):
                if nums[i] < nums[i + 1]:
                    return i
            return None

        def reverse(nums: List[int], start: int) -> None:
            end = len(nums) - 1
            while start < end:
                nums[start], nums[end] = nums[end], nums[start]
                start += 1
                end -= 1

        def swap_pivot_with_successor(nums: List[int], pivot: int) -> None:
            for i in reversed(range(pivot + 1, len(nums))):
                if nums[i] > nums[pivot]:
                    nums[i], nums[pivot] = nums[pivot], nums[i]
                    return

        pivot = search_pivot(nums)
        if pivot is None:
            reverse(nums, 0)
            return

        swap_pivot_with_successor(nums, pivot)
        reverse(nums, pivot + 1)
```

### レビューを依頼する方のPR

- [31. Next Permutation by tom4649 · Pull Request #53 · tom4649/Coding](https://github.com/tom4649/Coding/pull/53)
- [31. Next Permutation by garunitule · Pull Request #58 · garunitule/coding_practice](https://github.com/garunitule/coding_practice/pull/58)
    - `is_sorted_until` という関数がある
        - `next_permutation` という関数もある
    - python の標準ライブラリにはなかった
- [31. Next Permutation by dxxsxsxkx · Pull Request #58 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/58)
- [solve: 31.Next Permutation by t9a-dev · Pull Request #58 · t9a-dev/LeetCode_arai60](https://github.com/t9a-dev/LeetCode_arai60/pull/58)

## Step3

- `-> None` を忘れがち
- `reverse(nums, pivot + 1)` で `pivot + 1` となることを最初間違えた

```py
class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """

        def search_pivot(nums: List[int]) -> int | None:
            for i in reversed(range(len(nums) - 1)):
                if nums[i] < nums[i + 1]:
                    return i
            return None

        def reverse(nums: List[int], start: int) -> None:
            end = len(nums) - 1
            while start < end:
                nums[start], nums[end] = nums[end], nums[start]
                start += 1
                end -= 1

        def swap_pivot_with_successor(nums: List[int], pivot: int) -> None:
            for i in reversed(range(pivot + 1, len(nums))):
                if nums[i] > nums[pivot]:
                    nums[i], nums[pivot] = nums[pivot], nums[i]
                    return

        pivot = search_pivot(nums)
        if pivot is None:
            reverse(nums, 0)
            return

        swap_pivot_with_successor(nums, pivot)
        reverse(nums, pivot + 1)
```
