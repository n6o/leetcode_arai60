## 問題

[Unique Paths - LeetCode](https://leetcode.com/problems/unique-paths/description/)

- 入力
    - `m`: グリッドの行数
    - `n`: グリッドの列数
    - どちらも1以上100以下
- 出力
    - 右下の到達するユニークなパスの総数

## Step1

必要な移動の並び方の数を求める

必要な↓と→の並び方の数を計算する。
m,n の上限が100だから、必要なサイズの上限は200程度。
Ex1 (m=3, n=7) の場合、 8!/(2!*6!) = 28 となる。
- 時間計算量は O(m+n)
- 空間計算量は O(m+n)
- 今回は m+n < 200 なので動きそう

```py
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        down_steps = m - 1
        right_steps = n - 1
        total_steps = down_steps + right_steps

        factorials = [1] * (total_steps + 1) # 0! を含めるため +1 している
        for i in range(1, total_steps + 1):
            factorials[i] = factorials[i - 1] * i

        return factorials[total_steps] // (
            factorials[down_steps] * factorials[right_steps]
        )
```

## Step2

- leetcode の解答例を確認した。
- Maximum Subarray と同じ方式が使えそう
    - 各マスに、左上のマスからの到達パスの数を入れていく
    - サイズmの配列を使って更新していく（レーン）
        - あるマスは一つ上のマスの数 + 自分自身の数に更新する
            - 一番上のマスは常に1
- m, n の少ないほうを基準にする
- 時間計算量は O(m*n)
- 空間計算量は O(min(m, n))

```py
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        if n < m:
            # 再帰を使うことも考えたが、こちらのほうがシンプルに感じた
            m, n = n, m

        path_counts = [1] * m

        # 空間計算量を O(m) に抑えるため、1次元配列を再利用する。
        # 外側のループが `i` 列目を処理している最中、配列の各要素は以下の状態を保つ：
        # path_counts[k] (k < row)  : すでに計算が完了した `i` 列目の経路数
        # path_counts[k] (k >= row) : まだ計算されていない、1つ左の `i-1` 列目の経路数
        for _ in range(1, n):
            for row in range(1, m):
                path_counts[row] += path_counts[row - 1]

        return path_counts[m - 1]
```

### レビューを依頼する方のPR

- [62. Unique Paths by dxxsxsxkx · Pull Request #33 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/33)
    - 階乗の値の最大値を考慮してなかった。Pythonだから動いていた。
- [62. unique paths by 5ky7 · Pull Request #34 · 5ky7/arai60](https://github.com/5ky7/arai60/pull/34)
- [62. Unique Paths by TakayaShirai · Pull Request #32 · TakayaShirai/leetcode_practice](https://github.com/TakayaShirai/leetcode_practice/pull/32)
- [LeetCode 62. Unique Paths by huyfififi · Pull Request #57 · huyfififi/coding-challenges](https://github.com/huyfififi/coding-challenges/pull/57)
    - `@functools.cache` というデコレーターがある。あとで読む。
        - https://docs.python.org/3.14/library/functools.html#functools.cache
    - `math.comb` という関数がある。あとで読む。
        - https://docs.python.org/3.14/library/math.html#math.comb
- いろんな解法があった

## Step3

- DPの問題だったので、DPの方針を用いる。

```py
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        if n < m:
            m, n = n, m

        path_counts = [1] * m

        for _ in range(1, n):
            for row in range(1, m):
                path_counts[row] += path_counts[row - 1]

        return path_counts[m - 1]
```
