## 問題

https://leetcode.com/problems/search-in-rotated-sorted-array/description/

- 入力
    - `nums`: 昇順に並んだ数字の列を回転させた配列
        - 長さは1以上5000以下
        - 値は-10^4以上10^4以下
        - 値は重複していない
    - `target`: 数字
        - -10^4以上10^4以下
- 出力
    - `target` のインデックス
        - `nums` に含まれていない場合は `-1`

## 解法

### 1. 最小値を探して2分探索する

- 最小値のインデックスを探す
- 最小値を元に `nums` 上で `target` が含まれている範囲を2分探索する
    - なさそうであれば -1 を返す
- 時間計算量
    - 最小値を探すのに O(log n)
    - `target` の探索に O(log n)
    - 合計 O(log n)
- 空間計算量
    - 最小値を探すのに O(1)
    - `target` の探索に O(1)
    - 合計 O(1)

## Step1

### 1.

```py
class Solution:
    def search(self, nums: list[int], target: int) -> int:
        index_of_minimum = self.search_minimum(nums)

        if nums[0] <= target <= nums[index_of_minimum - 1]:
            return self.search_target(nums, target, 0, index_of_minimum - 1)
        elif nums[index_of_minimum] <= target <= nums[-1]:
            return self.search_target(nums, target, index_of_minimum, len(nums) - 1)
        else:
            return -1

    def search_minimum(self, nums: list[int]) -> int:
        start_index = 0
        end_index = len(nums) - 1
        while start_index < end_index:
            middle_index = (start_index + end_index) // 2

            if nums[middle_index] > nums[end_index]:
                start_index = middle_index + 1
            else:
                end_index = middle_index
        return start_index

    def search_target(
        self, nums: list[int], target: int, start_index: int, end_index: int
    ) -> int:
        while start_index <= end_index:
            middle_index = (start_index + end_index) // 2

            if nums[middle_index] == target:
                return middle_index
            elif nums[middle_index] < target:
                start_index = middle_index + 1
            else:
                end_index = middle_index - 1

        return -1
```

- 動かなかった
    - `nums` の長さが1のときの考慮が漏れていた
    - 整列済みの場合を考慮する必要がある
- 末尾と比較してどちらの範囲を調べるか決めるといい

```py
        if target <= nums[-1]:
            return self.search_target(nums, target, index_of_minimum, len(nums) - 1)
        else:
            return self.search_target(nums, target, 0, index_of_minimum - 1)
```

## Step2

- 解答を見た
- 昇順に並んだ列を回転しているので、 `mid` で分けた時に片方の範囲は昇順にソートされている
- `target` がソート済みの範囲に含まれているかどうかをチェックし、次の探索範囲を決める

```py
class Solution:
    def search(self, nums: list[int], target: int) -> int:
        left = 0
        right = len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid

            if nums[left] <= nums[mid]:
                # 左半分がソートされている場合
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                # 右半分がソートされている場合
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1

        return -1
```

### レビューを依頼する方のPR

- [33. search in rotated sorted array by 5ky7 · Pull Request #43 · 5ky7/arai60](https://github.com/5ky7/arai60/pull/43)
    - タプルをキーにして bisect で挿入位置を探す的なやり方が紹介されていた
- [33. Search in Rotated Sorted Array by tom4649 · Pull Request #41 · tom4649/Coding](https://github.com/tom4649/Coding/pull/41)
- [Ask for a review for 33. Search in Rotated Sorted Array by yumyum116 · Pull Request #9 · yumyum116/LeetCode_Arai60](https://github.com/yumyum116/LeetCode_Arai60/pull/9)
- [33. Search in Rotated Sorted Array by 5103246 · Pull Request #41 · 5103246/LeetCode_Arai60](https://github.com/5103246/LeetCode_Arai60/pull/41)


## Step3

```py
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid

            if nums[left] <= nums[mid]:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1

        return -1
```
