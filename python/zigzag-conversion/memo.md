## 問題

[Zigzag Conversion - LeetCode](https://leetcode.com/problems/zigzag-conversion/description/)

- 入力
    - `s`: 文字列
        - 長さは1以上1000以下
        - アルファベットと `,` と `.` で構成されている
    - `numRows`: 行数
        - 値は1以上1000以下
- 出力
    - 変換後の文字列

## 解法

### 1. 1文字ずつ移動する

- `numRows` 行 `numColumns` 列の配列を用意して、値を埋めていく
    - `numColumns` は `len(s) // 2 + 1` とできる
        - 繰り返しの文字数が `numRows + (numRows - 2)` -> `2 * (numRows - 1)`
        - 繰り返しに必要な列数が `1 + (numRows - 2)` -> `numRows - 1`
        - 必要な列数は `len(s) // (2 * (numRows - 1) * (numRows - 1) + 1` -> `len(s) // 2 + 1`
- 時間計算量はO(n^2)
    - 文字を埋めるのにO(n): n は `s` の長さ
    - 出力文字を作るのにO(n^2): 10^5
- 空間計算量はO(n^2)
    - 制約では行数の最大値は10^3、列の最大値は5 * 10^2
        - 要素数は5 * 10^5 -> ポインタは8byteだから 4 * 10^6 -> 4MBくらい

## Step1

```py
class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1:
            return s

        numColumns = len(s) // 2 + 1

        matrix = [[None] * numColumns for i in range(numRows)]

        row = 0
        column = 0
        row_direction = 1
        column_direction = 0
        for i in range(len(s)):
            if row_direction == 1:
                matrix[row][column] = s[i]
                if row == numRows - 1:
                    row_direction = -1
                    column_direction = 1
                row += row_direction
                column += column_direction
                continue
            if row_direction == -1:
                matrix[row][column] = s[i]
                if row == 0:
                    row_direction = 1
                    column_direction = 0
                row += row_direction
                column += column_direction

        result_array = []
        for row in matrix:
            for c in row:
                if c is not None:
                    result_array.append(c)

        return "".join(result_array)
```

## Step2

- 方向の更新部分を整理した

```py
class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1:
            return s

        numColumns = len(s) // 2 + 1

        matrix = [[None] * numColumns for i in range(numRows)]

        row = 0
        column = 0
        row_direction = 1
        column_direction = 0
        for i in range(len(s)):
            matrix[row][column] = s[i]

            if row == numRows - 1:
                row_direction = -1
                column_direction = 1
            elif row == 0:
                row_direction = 1
                column_direction = 0

            row += row_direction
            column += column_direction

        result_array = []
        for row in matrix:
            for c in row:
                if c is not None:
                    result_array.append(c)

        return "".join(result_array)
```

- leetcode の解答を見た
- 各行ごとに文字を管理する方針
- 時間計算量はO(n + r)
    - n は `s` の長さ
    - r は `numRows`
    - 配列の作成: O(r)
    - 文字の処理: O(n)
    - 文字列の結合: O(r)
- 空間計算量はO(n + r)
    - 配列の作成: O(r)
    - 文字列の保存: O(n)

```py
class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1:
            return s

        rows = [[] for _ in range(numRows)]

        index = 0
        direction = 1
        for c in s:
            rows[index].append(c)
            if index == 0:
                direction = 1
            if index == numRows - 1:
                direction = -1
            index += direction

        result_array = []
        for r in rows:
            result_array.append("".join(r))
        return "".join(result_array)
```

### レビューを依頼する方のPR

- [Zigzag Conversion by Yuto729 · Pull Request #64 · Yuto729/leetcode](https://github.com/Yuto729/leetcode/pull/64)
    - 「何かを改善する時に何かが悪くなる程度に良いコード」
    - 「`len(s) <= numRows` のときも入力をそのまま返せる」
    - `return "".join("".join(row) for row in rows)`
        - `result_array` を使わずに書ける
        - 内包表記が頭に浮かぶよう練習する
- [6. Zigzag Conversion by tom4649 · Pull Request #55 · tom4649/Coding](https://github.com/tom4649/Coding/pull/55)
    - 「標準ライブラリを読む」
- [55 6. zigzag conversion by h1rosaka · Pull Request #59 · h1rosaka/arai60](https://github.com/h1rosaka/arai60/pull/59)
    - `if 1 <= row_num + direction <= numRows:`
        - Python での書き方
     - [Programming FAQ — Python 3.14.5 documentation](https://docs.python.org/3/faq/programming.html)
        - 読む
- [6. Zigzag Conversion by garunitule · Pull Request #60 · garunitule/coding_practice](https://github.com/garunitule/coding_practice/pull/60)

## Step3

```py
class Solution:
    def convert(self, s: str, numRows: int) -> str:
        if numRows == 1 or len(s) <= numRows:
            return s

        rows = [[] for _ in range(numRows)]

        index = 0
        direction = 1
        for c in s:
            rows[index].append(c)
            if index == 0:
                direction = 1
            if index == numRows - 1:
                direction = -1
            index += direction

        return "".join("".join(row) for row in rows)
```
