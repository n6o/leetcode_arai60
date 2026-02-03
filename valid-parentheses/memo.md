## 問題

[Valid Parentheses - LeetCode](https://leetcode.com/problems/valid-parentheses/description/)

- 入力
    - `s`: 文字列
        - 長さは1以上10^4以下
        - `(){}[]` で構成されている
- 出力
    - `s` が有効なら `true`
        - 有効
            - 開きかっこは同じ種類のかっこで閉じられている
            - 開きかっこは正しい順番で閉じられている
            - すべての閉じかっこには対応する開きかっこがある

## 解法

### 1. スタックで管理する

- 開きかっこを見つけたらスタックに積む
- 閉じかっこを見つけたらスタックの先頭を見る
    - 対応する開きかっこならスタックから出す
    - そうでないなら `false` を返す
- `s` が有効ならすべての文字を見た後スタックは空になっている

## Step1

### 1. 

```go
func isValid(s string) bool {
    closeBracketPair := map[byte]byte{
        ')': '(',
        '}': '{',
        ']': '[',
    }
    openBrackets := make([]byte, 0, len(s))

    for i := 0; i < len(s); i++ {
        if ob, found := closeBracketPair[s[i]]; found {
            l := len(openBrackets)
            if l == 0 {
                // 開きかっこがない
                return false
            }

            if ob != openBrackets[l-1] {
                // 開きかっこの種類が異なる
                return false
            }

            // 開きかっこをスタックから取り除く
            openBrackets = openBrackets[:l-1]
            continue
        }

        // 開きかっこをスタックに積む
        openBrackets = append(openBrackets, s[i])
    }
    
    return len(openBrackets) == 0
}
```

- 文字の種類が限定されていたので `byte` を用いた
    - ascii 以外が含まれている場合は `rune` を使う
- 閉じかっこから対応する開きかっこを取り出すために map を用いた
    - `closeBracketPair` という名前はもっといいものがありそう
    - 対応する開きかっこを `ob` とした
        - `openBracket` とすると `s` のあるなしで似た変数が登場するため
        - でも `ob` を見たときなんだこれとなりそう
- 開きかっこを管理するスタックを `openBrackets` とした
    - `stack` という名前とどちらがいいのか
- ペアを逆にした map でもいい
    - 自然な流れで書ける
        - 開きかっこならスタックに積む
        - 閉じかっこなら
            - スタックが空なら false
            - スタックの先頭が対応する開きかっこでないなら false
            - それ以外ならスタックの先頭から取り出す

```go
openBracketPair := map[byte]byte{
    '(': ')',
    '{': '}',
    '[': ']',
}
openBrackets := make([]byte, 0, len(s))

for i := 0; i < len(s); i++ {
    if _, found := openBracketPair[s[i]]; found {
        openBrackets = append(openBrackets, s[i])
        continue
    }

    l := len(openBrackets)
    if l == 0 {
        // 開きかっこがない
        return false
    }

    lastOpenBracket := openBrackets[l-1]
    if openBracketPair[lastOpenBracket] != s[i] {
        // 開きかっこの種類が異なる
        return false
    }

    // 開きかっこをスタックから取り除く
    openBrackets = openBrackets[:l-1]
}
```

### レビューを依頼する方のPR

- [20.ValidParentheses by xbam326 · Pull Request #8 · xbam326/leetcode](https://github.com/xbam326/leetcode/pull/8)
    - `(){}[]` 以外が含まれていた場合の考慮をするべきだった
        - for loop の先頭で switch で弾く
        - rune を使う
        - go だと error を返すが、問題の形式上 `false` を返す実装にはなる
    - `bracket_pairs` や `open_to_close` など
        - `x_to_y` 形式は便利
- [26. Valid Parentheses by dxxsxsxkx · Pull Request #6 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/6)
    - [チョムスキー階層 - Wikipedia](https://ja.wikipedia.org/wiki/%E3%83%81%E3%83%A7%E3%83%A0%E3%82%B9%E3%82%AD%E3%83%BC%E9%9A%8E%E5%B1%A4)
    - [プッシュダウン・オートマトン - Wikipedia](https://ja.wikipedia.org/wiki/%E3%83%97%E3%83%83%E3%82%B7%E3%83%A5%E3%83%80%E3%82%A6%E3%83%B3%E3%83%BB%E3%82%AA%E3%83%BC%E3%83%88%E3%83%9E%E3%83%88%E3%83%B3)
- [020-valid-parentheses by 05ryt31 · Pull Request #7 · 05ryt31/leetcode](https://github.com/05ryt31/leetcode/pull/7)
- [Create 20. Valid Parentheses.md by Kazuuuuuuu-u · Pull Request #9 · Kazuuuuuuu-u/arai60](https://github.com/Kazuuuuuuu-u/arai60/pull/9)
- [Arai60/20 by liruly · Pull Request #8 · liruly/leetcode](https://github.com/liruly/leetcode/pull/8)

## Step2

```go
func isValid(s string) bool {
    openToClose := map[rune]rune{
        '(': ')',
        '{': '}',
        '[': ']',
    }
    openBrackets := make([]rune, 0, len(s))

    for _, r := range s {
        switch r {
            case '(', ')', '{', '}', '[', ']':
                // valid
            default:
                return false
        }

        if _, found := openToClose[r]; found {
            openBrackets = append(openBrackets, r)
            continue
        }

        l := len(openBrackets)
        if l == 0 {
            // 開きかっこがない
            return false
        }

        lastOpenBracket := openBrackets[l-1]
        if openToClose[lastOpenBracket] != r {
            // 開きかっこの種類が異なる
            return false
        }

        // 開きかっこをスタックから取り除く
        openBrackets = openBrackets[:l-1]
    }
    
    return len(openBrackets) == 0
}
```

## Step3

```go
func isValid(s string) bool {
    openToClose := map[rune]rune{
        '(': ')',
        '{': '}',
        '[': ']',
    }
    openBrackets := make([]rune, 0, len(s))

    for _, r := range s {
        switch r {
            case '(', ')', '{', '}', '[', ']':
                // skip
            default:
                return false
        }

        if _, found := openToClose[r]; found {
            openBrackets = append(openBrackets, r)
            continue
        }

        l := len(openBrackets)
        if l == 0 {
            return false
        }

        if openToClose[openBrackets[l-1]] != r {
            return false
        }

        openBrackets = openBrackets[:l-1]
    }

    return len(openBrackets) == 0
}
```

## ふりかえり

- 問題の想定だけではなく、一般に起こりそうな入力の検証を考慮する
- 命名パターンを増やす
    - `xToY` など
    - 標準ライブラリ読んでマネするのがよさそう
