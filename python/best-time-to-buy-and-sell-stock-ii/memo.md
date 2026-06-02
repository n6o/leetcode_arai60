## 問題

[Best Time to Buy and Sell Stock II - LeetCode](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/description/)

- 入力
    - `prices`: 株価の配列
        - 1日に何度も売買できる
        - ただし、保有できるのは最大1単元まで
        - 長さは1以上3*10^4以下
        - 値は0以上10^4以下
- 出力
    - 最大となる利益額

## 解法

### 1. 大きく勝つことを繰り返す

- 利益を伸ばせるだけ伸ばす
    - 未来がわかるから取れる戦略
- 利益が減少する前に売却する
    - いったん手仕舞いする
- 利益が出るタイミングで買う
    - 買った翌日に売って利益が出るなら買う
    - 金額が0円なら買う（0円とは）
- 握ったまま終わった場合はどうなるんだろう
    - 売れる場合に買う方針なので、大丈夫
- 時間計算量は O(n)
    - 配列を走査する
- 空間計算量は O(1)

## Step1

### 1.

ループを整理できず実装できなかった

### leetcode: 貪欲法

1. の方針は貪欲法と呼ばれている。
今回、1日に何度も売買していいので、利益が出るとわかったタイミングで売って買うことを繰り返せばいい

```py
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        total_profit = 0
        for i in range(len(prices) - 1):
            profit = prices[i + 1] - prices[i]
            if profit > 0:
                total_profit += profit

        return total_profit
```

### leetcode: DP

- i日目の取引終了時点の下記の場合での利益の最大値を求めていく
    - 株を持っている場合
    - 株を持っていない場合
- 購入したら利益は減ると考える
    - 一時的に負になることもある
- スワップを使うと一時変数を減らせるが、読みにくいと感じた
    - どうなんだろう
    - 一時変数もスワップも使わずにやっても動く
        - 問題設定によることな気がする

```py
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if not prices:
            return 0

        profit_with_stock = -prices[0]  # 初日に購入したら利益は減る
        profit_without_stock = 0  # 初日に購入しないとき利益は0
        for i in range(1, len(prices)):
            new_profit_with_stock = max(
                profit_with_stock, profit_without_stock - prices[i]
            )
            new_profit_without_stock = max(
                profit_without_stock, profit_with_stock + prices[i]
            )
            profit_with_stock = new_profit_with_stock
            profit_without_stock = new_profit_without_stock

        return max(profit_with_stock, profit_without_stock)
```

## Step2

### レビューを依頼する方のPR
- [122. Best Time to Buy and Sell Stock II by 5103246 · Pull Request #36 · 5103246/LeetCode_Arai60](https://github.com/5103246/LeetCode_Arai60/pull/36)
    - 買って売る場合(x円)と買わなかった場合(0円)の max を足し合わせる方法
        - 一番好み
- [122. Best Time to Buy and Sell Stock II by ryoooooory · Pull Request #41 · ryoooooory/LeetCode](https://github.com/ryoooooory/LeetCode/pull/41)
- [122. Best Time to Buy and Sell Stock II by mamo3gr · Pull Request #36 · mamo3gr/arai60](https://github.com/mamo3gr/arai60/pull/36)
    - 山と谷を探す方法
- [122. best time to buy and sell stock ii by 5ky7 · Pull Request #39 · 5ky7/arai60](https://github.com/5ky7/arai60/pull/39)
    - `return max_return_without_stock` でも正しい
        - ただ、パッとは理解できなかった
        - max を使うことによるペナルティは特に大きくない気がするので、何も考えずに書いてしまう気がする
            - 気を回せるようになるのがもちろん良い

## Step3

```py
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        total_profit = 0
        for i in range(len(prices) - 1):
            total_profit += max(0, prices[i + 1] - prices[i])

        return total_profit
```
