## 問題

[K-th Symbol in Grammar - LeetCode](https://leetcode.com/problems/k-th-symbol-in-grammar/description/)

- 入力
    - n: 整数
        - 1以上30以下
    - k: 整数
        - 1以上2^(n-1)以下
- 出力
    - n 行目の文字列のk番目の文字

## 解法

### 1. 並べてみた

図を書いて考えた。  
- `k` が n 行目の前半部分( 2^(n - 2) 以下)の場合、 n - 1 行目の `k` 番目になる
- `k` が後半部分の場合、n - 1 行目を2つに分けてスワップした文字列の `k - 2^(n - 2)` 番目になる
    - 後半部分を実装できなかった

## Step1

```py
class Solution:
    def kthGrammar(self, n: int, k: int) -> int:
        if n == 1:
            return 0
        if n == 2:
            return 0 if k == 1 else 1

        mid = pow(2, n - 2)
        if k <= mid:
            return self.kthGrammar(n - 1, k)

        # 書けなかった
```

## Step2

解答を見た。

n 行目の後半部分は n - 1 行目を反転した文字列となる。  
つまり、 n - 1 行目の文字列の `k - 2^(n - 2)` 番目を反転させたものとなる。
今回は 0 -> 1 と 1 -> 0 なので、 `1 - x` の形で書ける。

「反転」と認識することができてなかった。ビット演算みたいなものを思いつくのが苦手なので、練習する。

再帰での実装がしやすい。

```py
class Solution:
    def kthGrammar(self, n: int, k: int) -> int:
        if n == 1:
            return 0

        mid = 2 ** (n - 2)
        if k <= mid:
            return self.kthGrammar(n - 1, k)

        return 1 - self.kthGrammar(n - 1, k - mid)
```

- 時間計算量: O(n)
- 空間計算量: O(n)

反復でも実装してみた。反転回数を数える形にした。

```py
class Solution:
    def kthGrammar(self, n: int, k: int) -> int:
        flip_count = 0
        for i in range(n, 0, -1):
            mid = 2 ** (i - 1)
            if mid < k:
                k -= mid
                flip_count += 1

        return flip_count % 2
```

- 時間計算量: O(n)
- 空間計算量: O(1)

### レビューを依頼する方のPR

- [779. K-th Symbol in Grammar by tom4649 · Pull Request #44 · tom4649/Coding](https://github.com/tom4649/Coding/pull/44)
    - 入力値のケアを忘れていた
- [779. K-th Symbol in Grammar by dxxsxsxkx · Pull Request #46 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/46)
- [779. K-th Symbol in Grammar by mamo3gr · Pull Request #44 · mamo3gr/arai60](https://github.com/mamo3gr/arai60/pull/44)
- [solve: 779.K-th Symbol in Grammar by t9a-dev · Pull Request #46 · t9a-dev/LeetCode_arai60](https://github.com/t9a-dev/LeetCode_arai60/pull/46)


## Step3

入力値の検証部分も練習のため書いてみた。  
便利な書き方だと感じた。

```py
class Solution:
    def kthGrammar(self, n: int, k: int) -> int:
        if not (1 <= n <= 30):
            raise ValueError(f"n must be between 1 and 30, got {n}")
        if not (1 <= k <= 2 ** (n - 1)):
            raise ValueError(f"k must be between 1 and 2^(n-1), got {k}")

        if n == 1:
            return 0

        mid = 2 ** (n - 2)
        if k <= mid:
            return self.kthGrammar(n - 1, k)

        return 1 - self.kthGrammar(n - 1, k - mid)
```
