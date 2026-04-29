## 問題

[Longest Substring Without Repeating Characters - LeetCode](https://leetcode.com/problems/longest-substring-without-repeating-characters/description/)

- 入力
    - `s`: 文字列
        - 長さは0以上5*10^4以下
        - 英数字、記号、スペースを含む
- 出力
    - 重複した文字を含まない最長部分文字列

## 解法

### 1. 辞書で文字ごとの位置を管理しながら範囲を動かす

- 文字列の先頭から見ていく
- 辞書に文字と最後に登場した位置を記録する
- 辞書にあった場合
    - その位置が範囲の開始位置より前の場合
        - 現在の範囲には含まれていないので、登場位置を更新する
    - それ以外の場合
        - 現在の範囲に含まれているので
            - 登場位置を更新する
            - 範囲の開始位置をその位置の次に更新する
- 現在の位置と範囲の開始位置を元に長さを求める
- 必要に応じて長さの最大値を更新する
- 時間計算量は O(n)
- 空間計算量は O(1)
    - 辞書に入る文字は英数字、記号、空白で有限
    - 定数と見做せる

## Step1

### 1. 

```py
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        if len(s) == 0:
            return 0

        start = 0
        maxLength = 0
        memo = {}
        for i in range(len(s)):
            c = s[i]

            if not c in memo:
                memo[c] = i
            else:
                lastAppearAt = memo[c]
                memo[c] = i
                if start <= lastAppearAt:
                    start = lastAppearAt + 1

            length = i - start + 1
            maxLength = length if length > maxLength else maxLength

        return maxLength
```

## Step2

- `len(s) == 0` の分岐は消しても問題ない
- `enumerate` を使う
- `memo[c] = i` は外に出せる
- `max` を使う

```py
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        start = 0
        maxLength = 0
        memo = {}
        for i, c in enumerate(s):
            if c in memo and memo[c] >= start:
                start = memo[c] + 1
            memo[c] = i
            maxLength = max(maxLength, i - start + 1)
        return maxLength
```

### レビューを依頼する方のPR

## Step3

```py
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        start = 0
        maxLength = 0
        memo = {}
        for i, c in enumerate(s):
            if c in memo and memo[c] >= start:
                start = memo[c] + 1
            memo[c] = i
            maxLength = max(maxLength, i - start + 1)
        return maxLength
```
