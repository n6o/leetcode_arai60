## 問題

[Is Subsequence - LeetCode](https://leetcode.com/problems/is-subsequence/solutions/)

- 入力
    - `s`: 文字列
        - 長さは0以上100以下
    - `t`: 文字列
        - 長さは0以上10^4以下
    - `s` も `t` も英語の小文字て構成されている
- 出力
    - `s` が `t` の部分列なら `True`

## 解法

### 1. 2ポインタで探索する

- `t` を走査しながら、 `s` の文字かどうか確認しながら進める
    - `s` が空文字の場合は常に `True`
- `s` を最後まで走査したら `True`
- 先に `t` の走査が終わったら `False`
- 時間計算量は O(n)
    - n: `t` の長さ
- 空間計算量は O(1)

## Step1

### 1.

```py
class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        if len(s) == 0:
            return True

        s_index = 0
        for t_char in t:
            if s[s_index] != t_char:
                continue

            s_index += 1
            if s_index == len(s):
                return True

        return False
```

## Step2

- leetcode では下記のような回答が多かった

```py
class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        i, j = 0, 0
        while i < len(s) and j < len(t):
            if s[i] == t[j]:
                i += 1
            j += 1
        return i == len(s)
```

### レビューを依頼する方のPR

## Step3

```py
class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        if len(s) == 0:
            return True

        s_index = 0
        for t_char in t:
            if s[s_index] != t_char:
                continue

            s_index += 1
            if s_index == len(s):
                return True

        return False
```
