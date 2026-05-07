## 問題

[Generate Parentheses - LeetCode](https://leetcode.com/problems/generate-parentheses/description/)

- 入力
    - `n`: 整数
- 出力
    - `n` ペアのかっこで構成する正しい形の括弧の組み合わせのリスト

## 解法

### 1. バックトラックで条件にある組み合わせを生成する

- 左かっこは、残っていれば使える
- 右かっこは、左かっこの数が右かっこの数より小さい場合に使える
- 左右のかっこの数がともに0となった場合、リストに追加する
- 時間計算量は、ざっくり構成できる文字列のパターンが 2^2n -> 4^n だからO(4^n)
- 空間計算量は、再帰回数は最大2n、必要なスタックの大きさも最大2n、だからO(n)

## Step1

### 1.

```py
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:

        result = []
        pattern = []

        def generate_pattern(remaining_open: int, remaining_close: int) -> None:
            if remaining_open == 0 and remaining_close == 0:
                result.append("".join(pattern))
                return

            if remaining_open > 0:
                pattern.append("(")
                generate_pattern(remaining_open - 1, remaining_close)
                pattern.pop()

            if remaining_close > remaining_open:
                pattern.append(")")
                generate_pattern(remaining_open, remaining_close - 1)
                pattern.pop()

        generate_pattern(n, n)

        return result
```

## Step2

- leetcode の解答はあまりピンとくるものは見当たらなかった

### レビューを依頼する方のPR

- [Generate Parentheses by Yuto729 · Pull Request #57 · Yuto729/LeetCode_arai60](https://github.com/Yuto729/LeetCode_arai60/pull/57)
    - いろんな解法があった
- [22. Generate Parentheses by atmaxstar · Pull Request #6 · atmaxstar/coding_practice](https://github.com/atmaxstar/coding_practice/pull/6)
- [22.Generate Parentheses by tom4649 · Pull Request #50 · tom4649/Coding](https://github.com/tom4649/Coding/pull/50)
- [22. Generate Parentheses by dxxsxsxkx · Pull Request #53 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/53)

## Step3

```py
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:

        result = []
        pattern = []

        def generate_pattern(remaining_open: int, remaining_close: int) -> None:
            if remaining_open == 0 and remaining_close == 0:
                result.append("".join(pattern))
                return

            if remaining_open > 0:
                pattern.append("(")
                generate_pattern(remaining_open - 1, remaining_close)
                pattern.pop()

            if remaining_close > remaining_open:
                pattern.append(")")
                generate_pattern(remaining_open, remaining_close - 1)
                pattern.pop()

        generate_pattern(n, n)

        return result
```
