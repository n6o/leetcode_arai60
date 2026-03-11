## 問題

[Longest Increasing Subsequence - LeetCode](https://leetcode.com/problems/longest-increasing-subsequence/description/)

- 入力
    - `nums`: 整数配列
        - 長さは1以上2500以下
        - 値は-10^4以上10^4以下
- 出力
    - 最長となる増加部分列

## 解法

### 1. 配列で長さと最小値を持っておく

- 配列のindexを部分列の長さ（より1小さくなる）として、その長さの部分列となる最小の値を記録する
- その配列の中で注目している値が入る場所を探す
    - 追加する場合と更新する場合がある
- 時間計算量は O(n log n)
    - `nums` の要素ごとに2分探索するため
- 空間計算量は O(n)
    - 最悪のケースは `nums` そのものが単調増加している場合

## Step1

## Step2

- leetcode の solutions を見た
- 2分探索は自分で実装した方がよさそう
- DPを使える
- ループの一時変数を `n` にした
    - `nums` から取り出すため
    - `v` より具体的だと思った

### レビューを依頼する方のPR

## Step3

## ふりかえり
