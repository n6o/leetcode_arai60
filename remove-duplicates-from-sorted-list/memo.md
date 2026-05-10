- 入力
    - `head`: リンクリストの先頭
        - リストの長さは0以上300以下
        - ノードの値は-100以上100以下
        - リストは昇順でソートされている
- 出力
    - 重複した値を持つノードが削除されたリンクリスト

## 方針

- `[1, 1, 2]` => `[1, 2]`
- `[1, 1, 2, 3, 3]` => `[1, 2, 3]`
- 昇順でソートされている => 重複している数字は並んでいる
    - 引き継ぎ方法は「前のノードの値」
        - 前のノードの情報があればいい
        - 次のノードの情報はわかるので、前のノードの情報を別に保存しなくていい
        - 今のノードと次のノードの情報がわかればよさそう
    - 自分が見ているノードの値と、次のノードの値が同じなら重複していると判断できる
        - 3つ以上の可能性もある
        - 異なる値のノードが出てくるまで繰り返す
        - 異なる値のノードが出てきたら、そのノードに進む
    - 今のノードのリンク先を次の次のノードのリンク先に変える
- リストの長さが0の場合
    - `head` は `nil` になる。`nil` を返す。つまり `head` を返せばいい。

## Step1

```go
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func deleteDuplicates(head *ListNode) *ListNode {
    node := head
    for node != nil {
        for node.Next != nil && node.Val == node.Next.Val {
            node.Next = node.Next.Next
        }

        node = node.Next
    }

    return head
}
```

- for の2重ループが気になった
    - 外側のループ: ノードを確定してリストを進めるループ
    - 内側のループ: 値が重複しているノードを取り除くループ
    - 役割が異なるから、これはこれで問題ない、と考えた
        - 各ノードを参照するのは1回ずつだから、時間計算量はO(n)となる

## Step2

レビューをお願いする方のPRを読む

- [Create 83. Remove Duplicates from Sorted List.md by Rinta-Rinta · Pull Request #2 · Rinta-Rinta/LeetCode_arai60](https://github.com/Rinta-Rinta/LeetCode_arai60/pull/2)
    - 解説動画があったので見た。1重ループで処理していた。
        - if-else にすれば、値が変わった時にのみリストを進めることができる。
        - head が nil となるケースを先に処理しておくと ループ条件を `node.Next != nil` にでき、次のノードだけ気にすればよくなる
- [083-remove-duplicates-from-sorted-list by 05ryt31 · Pull Request #11 · 05ryt31/leetcode](https://github.com/05ryt31/leetcode/pull/11)
    - ループの不変条件
        - 自分のstep1のコードだと2つ
            - 今いるノードが `nil` でない
            - 次のノードがあり、値が等しい
        - 1重ループ版の場合は「次のノードがある」
- [83_remove_duplicates by dxxsxsxkx · Pull Request #3 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/3)
    - 読み手の認知負荷を上げる可能性を考慮して省略形を使うかどうか判断する
- [83. Remove Duplicates from Sorted List by Hiroto-Iizuka · Pull Request #3 · Hiroto-Iizuka/coding_practice](https://github.com/Hiroto-Iizuka/coding_practice/pull/3)
- [83. Remove Duplicates from Sorted List by mamo3gr · Pull Request #3 · mamo3gr/arai60](https://github.com/mamo3gr/arai60/pull/3)

```go
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func deleteDuplicates(head *ListNode) *ListNode {
    if head == nil {
        return nil
    }

    node := head
    for node.Next != nil {
        if node.Val == node.Next.Val {
            node.Next = node.Next.Next
        } else {
            node = node.Next
        }
    }

    return head
}
```

- こちらのほうが読みやすい
    - 2重ループがあるとそれぞれが何をしているのか読み解く必要があるから
    - if を使って、リストを進むケースと次のノードを変えるケースに分ける

## Step3

```go
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func deleteDuplicates(head *ListNode) *ListNode {
    if head == nil {
        return nil
    }

    node := head
    for node.Next != nil {
        if node.Val == node.Next.Val {
            node.Next = node.Next.Next
        } else {
            node = node.Next
        }
    }

    return head
}
```
