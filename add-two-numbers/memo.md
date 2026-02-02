## 問題

[Add Two Numbers - LeetCode](https://leetcode.com/problems/add-two-numbers/description/)

- 入力
    - `l1` / `l2`: 空でないリンクリストの先頭ノード
        - それぞれのリストは非負の整数を表す
        - リストの長さは1以上100以下
        - 値は0以上9以下
        - 0を除いて、0を始まる数ではない
- 出力
    - 2つの数の和を表すリンクリスト

## 解法

- 筆算っぽい
    - 書き順が逆
- l1 と l2 の長さに関連はない
- 担当者は白箱1つと黒箱2つと紙を渡される
    - 黒箱からは数字が書かれた紙を取り出せる
        - 取り出せない場合もある
    - 黒箱から取り出した紙に書かれている数字を足し合わせる
    - さらに、箱とは別に渡された紙の値を足す
        - その紙には0か1が書いてある
    - 足した値は0以上19以下となる
    - 足した値の1の位を紙に書いて白箱に入れる
    - 足した値が10以上であれば紙に1を書く
        - そうでなければ0を書く
    - 次の担当者に渡す
- 例
    - [0, 0, 1] と [0, 0, 9] => [0, 0, 0, 1]

## Step1

```go
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func addTwoNumbers(l1 *ListNode, l2 *ListNode) *ListNode {
    sentinel := &ListNode{}

    carry := 0
    node := sentinel

    for l1 != nil || l2 != nil || carry != 0 {
        l1Value := 0
        if l1 != nil {
            l1Value = l1.Val
            l1 = l1.Next
        }

        l2Value := 0
        if l2 != nil {
            l2Value = l2.Val
            l2 = l2.Next
        }

        sum := l1Value + l2Value + carry

        value := sum % 10
        carry = sum / 10

        node.Next = &ListNode{
            Val: value,
        }
        node = node.Next
    }

    return sentinel.Next
}
```

## Step2

- `node` を `digit` に変えてみた
    - 「桁」の意
    - 命名難しい
    - リンクリストを進んでいる感じは `node` のほうが伝わる気がした
        - リンクリストを扱っているという前提が共有されていれば

```go
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func addTwoNumbers(l1 *ListNode, l2 *ListNode) *ListNode {
    sentinel := &ListNode{}

    carry := 0
    digit := sentinel

    for l1 != nil || l2 != nil || carry != 0 {
        l1Value := 0
        if l1 != nil {
            l1Value = l1.Val
            l1 = l1.Next
        }

        l2Value := 0
        if l2 != nil {
            l2Value = l2.Val
            l2 = l2.Next
        }

        sum := l1Value + l2Value + carry

        value := sum % 10
        carry = sum / 10

        digit.Next = &ListNode{
            Val: value,
        }
        digit = digit.Next
    }

    return sentinel.Next
}
```

### 再帰版

- 再帰でも解ける
    - sentinel を使うものは再帰を使う方が好みな気がした
        - senntinel を使うのは（自分にとってはまだ）自然ではない感覚
            - イディオムとして覚える
            - エッジケースをうまく処理できる。余計な分岐が不要になる。
        - ただ、実務では反復版を使うだろうと思う
            - 反復版のほうが余計なメモリを使わない（スタックを使わない）
            - ロジックがわかりやすければ再帰を試してみるかもしれない
    - `l1` と `l2` と `carry` を渡して `ListNode` を返す
        - 現在の桁を計算する
        - 次の桁を計算し、帰ってきたノードを現在の桁の `Next` につなげる
    - 停止条件は l1 が nil かつ l2 が nil かつ carry が 0
    

```go
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func addTwoNumbers(l1 *ListNode, l2 *ListNode) *ListNode {

    var calc func(l1, l2 *ListNode, carry int) *ListNode
    calc = func(l1, l2 *ListNode, carry int) *ListNode {
        if  l1 == nil && l2 == nil && carry == 0 {
            return nil
        }

        l1Value := 0
        if l1 != nil {
            l1Value = l1.Val
            l1 = l1.Next
        }

        l2Value := 0
        if l2 != nil {
            l2Value = l2.Val
            l2 = l2.Next
        }

        sum := l1Value + l2Value + carry

        value := sum % 10
        carry = sum / 10

        return &ListNode{
            Val: value,
            Next: calc(l1, l2, carry),
        }
    }

    return calc(l1, l2, 0)
}
```

### 直近のPR

- [2_add_two_numbers by dxxsxsxkx · Pull Request #5 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/5)
    - 符号なし64ビット整数は何桁くらいか
        - log_10 2 が 0.301 程度であることを覚えておく
            - まずは 0.3 くらいと覚えてみる
        - log_10 2^64 = 64 * log_10 2 = 64 * 0.301 = 19.264
            - 10^19より大きく10^20より小さい => 20桁くらい
        - go の int64 だと符号ビット分減って63ビット
            - 0.3 * 63 = 18.9
            - 19桁くらい
- [2. Add Two Numbers by DaisukeKikukawa · Pull Request #6 · DaisukeKikukawa/LeetCode_arai60](https://github.com/DaisukeKikukawa/LeetCode_arai60/pull/6)
    - `root` という名前が宣言されたら「なにか重要なもの」だと感じる
- [2. add two numbers by Rinta-Rinta · Pull Request #4 · Rinta-Rinta/LeetCode_arai60](https://github.com/Rinta-Rinta/LeetCode_arai60/pull/4)
- [Create 2. Add Two Numbers.md by Kazuuuuuuu-u · Pull Request #8 · Kazuuuuuuu-u/arai60](https://github.com/Kazuuuuuuu-u/arai60/pull/8)
- [Arai60/2 by liruly · Pull Request #7 · liruly/leetcode](https://github.com/liruly/leetcode/pull/7)
    - `carry` を int にすると3つ以上のリストを扱うよう拡張できる

## Step3

```go
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func addTwoNumbers(l1 *ListNode, l2 *ListNode) *ListNode {
    sentinel := &ListNode{}
    node := sentinel
    carry := 0

    for l1 != nil || l2 != nil || carry != 0 {
        l1Value := 0
        if l1 != nil {
            l1Value = l1.Val
            l1 = l1.Next
        }

        l2Value := 0
        if l2 != nil {
            l2Value = l2.Val
            l2 = l2.Next
        }

        sum := l1Value + l2Value + carry
        value := sum % 10
        carry = sum / 10

        node.Next = &ListNode{
            Val: value,
        }
        node = node.Next
    }

    return sentinel.Next
}
```

## ふりかえり

- [type List](https://cs.opensource.google/go/go/+/refs/tags/go1.25.6:src/container/list/list.go;l=46-51)
    - `container/list` パッケージで sentinel が使われていることを知った
    - doubly linked list: 双方向リンクリスト
    - 先頭や末尾に挿入するときにここを起点にしている
    - 基準点として見ると便利な気がした
