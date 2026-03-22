## 問題

[Best Time to Buy and Sell Stock - LeetCode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/description/)

- 入力
    - `prices`: 価格の配列
        - 長さは1以上10^5以下
        - 値は0以上10^4以下
- 出力
    - 最大となる利益
        - 利益: 売却時の価格 - 購入時の価格
        - 購入時と売却日は別
            - それぞれ1回ずつ

## 解法

### 1. 値の差が最大となるインデックスのペアを探す

- 売却日は購入日より後
- ある日に売却した際に差が最大となるのは、過去の中で一番価格が安かった日
    - 過去の最小の価格を引き継いでいく
- 差がわかればいいので、インデックスは不要
- 時間計算量は O(n)
    - 価格列を1回ずつ参照する
- 空間計算量は O(1)
    - 利益の最大値と価格の最小値を管理する

## Step1

```py
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if not prices or len(prices) == 1:
            return 0

        max_profit = 0
        min_price = prices[0]
        for i in range(1, len(prices)):
            profit = prices[i] - min_price
            if prices[i] < min_price:
                min_price = prices[i]

            if profit < 0:
                continue

            if max_profit < profit:
                max_profit = profit

        return max_profit
```

## Step2

leetcode の解答を確認した。
- `max` を使う解答が多かった
- `profit` が負の場合を特別扱いしたが、それにより処理の流れに制約が必要だった
    - 特別扱いしなくてもロジックとしては問題ない
    - 特別扱いする動機も特段ないので、ないほうがよさそう
- 長さ1のケースも特別扱いしなくても問題はない
    - `range(1, len(prices))` で考慮しているといえる
    - 先にその可能性を潰しておいても別に構わない
        - 意味はすぐわかるので
        - 趣味の範囲、だろうか

```py
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if not prices:
            return 0

        max_profit = 0
        min_price = prices[0]
        for i in range(1, len(prices)):
            max_profit = max(max_profit, prices[i] - min_price)
            min_price = min(min_price, prices[i])

        return max_profit
```

### レビューを依頼する方のPR

- [121. Best Time to Buy and Sell Stock by TakayaShirai · Pull Request #36 · TakayaShirai/leetcode_practice](https://github.com/TakayaShirai/leetcode_practice/pull/36)
    - 両端から見ていくこともできる模様
    - CPUクロックの話が過去にあった
- [121. Best Time to Buy and Sell Stock by dxxsxsxkx · Pull Request #37 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/37)
    - 分割統治法でも解ける模様
        - 前半で売買
        - 後半で売買
        - 前半で購入、後半で売却
        - こんな感じで求めている？
- [121. Best Time to Buy and Sell Stock by mamo3gr · Pull Request #35 · mamo3gr/arai60](https://github.com/mamo3gr/arai60/pull/35)
    - `itertools.accumulate` が使える
    - 今回は `len` が不要なので `itertools.islice` を使うことができる
- [121-Best-Time-to-Buy-and-Sell-Stock by kunimomo · Pull Request #3 · kunimomo/arai60](https://github.com/kunimomo/arai60/pull/3)
    - DPを使う方針もある模様
        - 今回のコードはそれの空間計算量を定数化したもののよう
        - 自然に思いつく場合とそうでない場合の違いが気になった
            - 自分がイメージしやすい題材かどうかもかんけいしているのだろうか

## Step3

```py
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if not prices:
            return 0

        max_profit = 0
        min_price = prices[0]
        for i in range(1, len(prices)):
            max_profit = max(max_profit, prices[i] - min_price)
            min_price = min(min_price, prices[i])

        return max_profit
```
