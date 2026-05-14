## 問題

[Coin Change - LeetCode](https://leetcode.com/problems/coin-change/description/)

- 入力
    - `coins`: 硬貨の一覧
        - 長さは1以上12以下
        - 値は1以上2^31-1以下
    - `amount`: 金額
        - 0以上10^4以下
- 出力
    - `amount` となる硬貨の組み合わせ枚数の最小値

## 解法

### 1. DP

- 0 から 10^4 までの金額の最小値を求めていく
- その金額となる枚数を各コインごとに計算し最小値を記録していく
    - 現在考えている金額
    - 担当する硬貨
    - これまでの記録
    - 担当する硬貨で金額の合計に達する際の枚数を求める
    - すでに記録されている枚数と比べて、小さい方を記録する
        - 初期値は大きな値で埋めておく
- 時間計算量: O(nm)
    - n: 金額
    - m: コインの枚数
    - 今回は10^4*12 = 10^5 なので問題なさそう
- 空間計算量: O(n)

## Step1

### 1.

実装はできなかった
- 整数の最大値、みたいなのを使うつもりだったが、Pythonではなさそうで調べた
    - `float('inf')` が使われることが多いよう
        - Python らしいのだろうが、型を意識してしまってちょっと使いづらいと感じる
    - amount 以上になる可能性はないので、 amount + 1 とすれば十分だった
        - ただ読みづらいのでコメントが必要そう

```py
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        # Use amount + 1 as max value because the max number of coins needed is amount
        min_coins = [amount + 1] * (amount + 1)
        min_coins[0] = 0

        for i in range(1, amount + 1):
            for coin in coins:
                if i - coin >= 0:
                    min_coins[i] = min(min_coins[i], 1 + min_coins[i - coin])

        if min_coins[amount] == amount + 1:
            return -1

        return min_coins[amount]
```

## Step2

- `i` はインデックスでもあるが、「今考えている金額」であることを表すような名前にした
- `amount + 1` を変数にしたい気持ちになったが、長さと最大値の2種類の意味で使用しているので、いい名前が思いつかなかった

```py
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        min_coins = [amount + 1] * (amount + 1)
        min_coins[0] = 0

        for sub_amount in range(1, amount + 1):
            for coin in coins:
                if sub_amount - coin >= 0:
                    min_coins[sub_amount] = min(
                        min_coins[sub_amount], 1 + min_coins[sub_amount - coin]
                    )

        if min_coins[amount] == amount + 1:
            return -1

        return min_coins[amount]
```

### レビューを依頼する方のPR

- [322. Coin Change by tom4649 · Pull Request #38 · tom4649/Coding](https://github.com/tom4649/Coding/pull/38)
    - `min(array)` で再帰していく形が面白いと思った
- [322. Coin Change by dxxsxsxkx · Pull Request #40 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/40)
    - `coins` の要素を降順で処理していくとDFSで素直に実装できる
- [322. coin change by 5ky7 · Pull Request #30 · 5ky7/arai60](https://github.com/5ky7/arai60/pull/30)
- [322. Coin Change by mamo3gr · Pull Request #38 · mamo3gr/arai60](https://github.com/mamo3gr/arai60/pull/38)

## Step3

```py
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        min_coins = [amount + 1] * (amount + 1)
        min_coins[0] = 0

        for sub_amount in range(1, amount + 1):
            for coin in coins:
                if sub_amount - coin >= 0:
                    min_coins[sub_amount] = min(
                        min_coins[sub_amount], 1 + min_coins[sub_amount - coin]
                    )
        if min_coins[amount] == amount + 1:
            return -1

        return min_coins[amount]
```
