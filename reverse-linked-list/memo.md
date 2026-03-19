## 問題

[Reverse Linked List - LeetCode](https://leetcode.com/problems/reverse-linked-list/description/)

- 入力
    - `head`: リンクリストの先頭ノード
        - リストの長さは0以上5000以下
        - ノードの値は-5000以上5000以下
- 出力
    - 反転したリンクリストの先頭ノード

## 解法

### 今のノードの次を前のノードに変えていく

- sentinel を使う
- reversed が反転後のリンクリスト
- node の次 nextをいったん退避して、node.Next を reversed に変える
- 退避した next を node にしてループ

### スタックを使う

- 見て行った順にスタックに積んでいく
    - 今見ているノードの next をスタックの先頭に向けてからスタックに積む
- 全部見たらスタックの先頭を返す

## Step1

### sentinel 版

```go
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func reverseList(head *ListNode) *ListNode {
    var reversed *ListNode

    node := head
    for node != nil {
        // 次のノードをいったん退避
        next := node.Next
        // 今のノードの次を reversed に向ける
        node.Next = reversed
        // 今のノードを反転済みリストの先頭にする
        reversed = node
        // 次のノードに進む
        node = next
    }

    return reversed
}
```

- 最初 `sentinel` を使って実装したが、 sentinel が不要だったことに気づいた

### stack 版

```go
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func reverseList(head *ListNode) *ListNode {
    if head == nil {
        return nil
    }

    reversed := []*ListNode{}

    node := head
    for node != nil {
        // 次のノードをいったん退避
        next := node.Next
        // ノードのリンクを反転
        if len(reversed) > 0 {
            node.Next = reversed[len(reversed)-1]
        } else {
            // 反転後のリンクリストの末尾
            node.Next = nil
        }
        // スタックに積む
        reversed = append(reversed, node)
        // 次のノードに進む
        node = next
    }

    return reversed[len(reversed)-1]
}
```

- `head == nil` のケースを弾く必要があった
- こっちのほうがシンプルかと思ったが、複雑になった
    - もっとシンプルに書けるのか。思いつかなかった。

### 再帰版

- 「sentinel が使えるケースは再帰で書ける」と以前学んだが、まだ身についておらず思いつけなかった
    - leetcode の解答例を見て知った
    - 実装しようとしたが、うまくできなかった
        - `tailOfReversed` になっていることに気づけなかった

```go
func reverseList(head *ListNode) *ListNode {
    if head == nil || head.Next == nil {
        return head
    }

    // 反転リストの先頭ノードが返ってくる
    reversed := reverseList(head.Next)
    // 今のノードの次のノードは反転リストの末尾
    tailOfReversed := head.Next
    // 反転リストの末尾を今いるノードに変える
    tailOfReversed.Next = head
    // 反転リストの末尾となるので、次のノードを消す
    head.Next = nil

    return reversed
}
```

### 再帰版(別関数として定義)

```go
func reverseList(head *ListNode) *ListNode {
    if head == nil || head.Next == nil {
        return head
    }

    var reverse func(head *ListNode) (*ListNode, *ListNode)
    reverse = func(head *ListNode) (reversedHead , reversedTail *ListNode) {
        // 反転リストの先頭
        if head.Next == nil {
            reversedHead = head
            reversedTail = head
            return
        }

        reversedHead, reversedTail = reverse(head.Next)

        // 反転リストの末尾の更新
        head.Next = nil
        reversedTail.Next = head
        reversedTail = head

        return
    }

    reversedHead, _ := reverse(head)

    return reversedHead
}
```

- 名前付き戻り値を使わなくても書けるが、型が同じだから名前が決まっていた方がわかりやすい、のかもしれない

## Step2

### レビュー依頼を依頼する方のPR

- [206. Reverse Linked List by dxxsxsxkx · Pull Request #7 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/7)
    - [例え話](https://github.com/philip82148/leetcode-swejp/pull/2#discussion_r1845974084)
    - ポインタの付け替え以外は「お手玉」と呼ばれている
- [206.ReverseLinkedList by komdoroid · Pull Request #13 · komdoroid/arai60](https://github.com/komdoroid/arai60/pull/13)
- [206-reverse-linked-list by 05ryt31 · Pull Request #8 · 05ryt31/leetcode](https://github.com/05ryt31/leetcode/pull/8)
- [# 206. Reverse Linked List by liruly · Pull Request #9 · liruly/leetcode](https://github.com/liruly/leetcode/pull/9)
    - [再帰の組み立て方](https://docs.google.com/document/d/11HV35ADPo9QxJOpJQ24FcZvtvioli770WWdZZDaLOfg/edit?tab=t.0#heading=h.x5w37bodndgj)
        - 引き継ぎの仕方
        - 関数それ自体で再帰するか、別に再帰関数を定義するか
        - とりあえずスタックに積んで、取り出しながら次を付け替えるやり方もある
- [Create 206. Reverse Linked List.md by Kazuuuuuuu-u · Pull Request #10 · Kazuuuuuuu-u/arai60](https://github.com/Kazuuuuuuu-u/arai60/pull/10)

## Step3

```go
func reverseList(head *ListNode) *ListNode {
    var reversed *ListNode

    node := head
    for node != nil {
        next := node.Next
        node.Next = reversed
        reversed = node
        node = next
    }

    return reversed
}
```
