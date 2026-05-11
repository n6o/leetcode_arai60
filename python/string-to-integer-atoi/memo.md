## 問題

[String to Integer (atoi) - LeetCode](https://leetcode.com/problems/string-to-integer-atoi/)

- 入力
- 出力

## 解法

### 1. 素直に実装する

- 先頭の空白スキップ
    - O(n)
- 符号チェック
    - O(1)
- 数値チェック
    - O(n)

## Step1

```py
class Solution:
    def myAtoi(self, s: str) -> int:
        s = s.lstrip()
        if not s:
            return 0

        start_index = 0
        sign = 1
        if s[0] == "-":
            sign = -1
            start_index = 1
        elif s[0] == "+":
            start_index = 1

        upper = 2**31 - 1
        lower = -(2**31)

        result = 0
        for i in range(start_index, len(s)):
            if s[i] not in "0123456789":
                return result * sign

            value = int(s[i])
            if sign > 0 and result > (upper - value) / 10:
                return upper

            if sign < 0 and result > -(lower + value) / 10:
                return lower

            result = result * 10 + value

        return result * sign
```

## Step2

- コンパクトにした
- `string.digits` という定数がある
- Python の整数の特性を利用する実装にした
    - 最後の表現は思いつかなかった

```py
_INT_MAX: Final[int] = 2**31 - 1
_INT_MIN: Final[int] = -(2**31)


class Solution:
    def myAtoi(self, s: str) -> int:
        s = s.lstrip()
        if not s:
            return 0

        sign = -1 if s[0] == "-" else 1
        start = 1 if s[0] in "+-" else 0

        result = 0
        for i in range(start, len(s)):
            if s[i] not in string.digits:
                break
            result = result * 10 + int(s[i])

        return max(_INT_MIN, min(_INT_MAX, sign * result))
```


### レビューを依頼する方のPR

## Step3

```py
_INT_MAX: Final[int] = 2**31 - 1
_INT_MIN: Final[int] = -(2**31)


class Solution:
    def myAtoi(self, s: str) -> int:
        s = s.lstrip()
        if not s:
            return 0

        sign = -1 if s[0] == "-" else 1
        start = 1 if s[0] in "+-" else 0

        result = 0
        for i in range(start, len(s)):
            if s[i] not in string.digits:
                break
            result = result * 10 + int(s[i])

        return max(_INT_MIN, min(_INT_MAX, sign * result))
```
