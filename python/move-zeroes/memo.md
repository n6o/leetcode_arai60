## 問題

[example](example.com)

- 入力
- 出力

## 解法

### 1. ひとつずつ移動する

- 末尾から検索し、0を見つけたら0でない位置まで移動する
- 時間計算量はO(n^2)
- 時間計算量はO(1)

## Step1

### 1.

```py
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        for i in range(len(nums) - 1, -1, -1):
            if nums[i] != 0:
                continue
            
            for j in range(i, len(nums) - 1):
                if nums[j + 1] == 0:
                    break
                
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
```

## Step2

- スワップする方針
- 時間計算量はO(n)
- 空間計算量はO(1)

```py
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        zero_start = 0
        for num in nums:
            if num == 0:
                continue
            
            nums[zero_start] = num
            zero_start += 1
        
        for i in range(zero_start, len(nums)):
            nums[i] = 0
```

無駄なスワップを減らす

```py
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        zero_start = 0
        for i in range(len(nums)):
            if nums[i] == 0:
                continue

            if zero_start != i:
                nums[zero_start], nums[i] = nums[i], nums[zero_start]
            zero_start += 1
```

### レビューを依頼する方のPR

## Step3

```py
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        zero_start = 0
        for i in range(len(nums)):
            if nums[i] == 0:
                continue

            if zero_start != i:
                nums[zero_start], nums[i] = nums[i], nums[zero_start]
            zero_start += 1
```
