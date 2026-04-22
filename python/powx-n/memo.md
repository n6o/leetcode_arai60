## 問題

[Pow(x, n) - LeetCode](https://leetcode.com/problems/powx-n/description/)

- 入力
    - `x`:  -100.0以上100.0以下の小数
    - `n`: -2^31以上n^31-1の整数
    - `x` は0でない、または `n` は0より大きい
- 出力
    - `x` の `n` 乗を返す
        - `x^n` は-10^4以上10^4以下

## 解法

### 再帰

- `n` の正負で分岐する
    - `n < 0` の場合は逆数を返す
- `n == 0` の場合は1を返す
- `n` の偶奇で分岐する
    - `n` が奇数の場合は `x * pow(x, (n - 1) / 2) * pow(x, (n - 1) / 2)` を返す
    - `n` が偶数の場合は `pow(x, n // 2) * pow(x, n // 2)` を返す
- 時間計算量は `O(log n)`
- 空間計算量は `O(1)`: 不正解 => `O(log n)` が正解
    - 再帰でのコールスタック分


## Step1

### 再帰

```py
class Solution:
    def myPow(self, x: float, n: int) -> float:
        if n < 0:
            return 1 / self.myPow(x, -n)

        if n == 0:
            return 1

        if n % 2 == 1:
            pow = self.myPow(x, (n - 1) // 2)
            return x * pow * pow

        pow = self.myPow(x, n // 2)
        return pow * pow
```

## Step2

- `x` も変えるとスッキリ書ける
- TODO: 反復版にすると空間計算量を1にできる

```py
class Solution:
    def myPow(self, x: float, n: int) -> float:
        if n < 0:
            return 1 / self.myPow(x, -n)

        if n == 0:
            return 1

        if n % 2 == 1:
            return x * self.myPow(x * x, (n - 1) // 2)

        return self.myPow(x * x, n // 2)
```

### レビューを依頼する方のPR
省略

## Step3

```py
class Solution:
    def myPow(self, x: float, n: int) -> float:
        if n < 0:
            return 1 / self.myPow(x, -n)
        
        if n == 0:
            return 1
        
        if n % 2 == 1:
            return x * self.myPow(x * x, (n - 1) // 2)

        return self.myPow(x * x, n // 2)
```
