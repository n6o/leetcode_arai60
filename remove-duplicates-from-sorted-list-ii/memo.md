- 入力
    - `head`: リンクリストの先頭
        - リストの長さは0以上300以下
        - ノードの値は-100以上100以下
        - リストは昇順にソート済み
- 出力
    - 元のリストから重複している値のノードをすべて取り除いたリスト

## 方針

### [1, 2, 3, 3, 4, 4, 5]

1. 今は1、次は2
    - 1は重複していない。返すリストに追加
    - リストを進む
1. 今は2, 次は3
    - 2は重複していない。返すリストに追加
    - リストを進む
1. 今は3, 次は3
    - 3は重複している。返すリストには追加しない
        - 返すリストの末尾を保持しておく必要がありそう
    - 3でない値がでるまでリストを進む
        - 4のノードに到達
1. 今は4, 次は4
    - 同様にして5に進む
1. 今は5, 次はなし
    - 5は重複していない。返すリストに追加
    - 次はないのでおしまい

### [1, 1, 1, 2, 3]

- 先頭ノードを取り除く必要がある
    - 返すリストの末尾を持っておく必要がある
    - 返すリストにいつノードが追加されるか
        - 今の次のノードの値が異なる時

## Step1

```go
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
 // 動かない
func deleteDuplicates(head *ListNode) *ListNode {
    // いったんガード
    if head == nil {
        return nil
    }
    if head.Next == nil {
        return head
    }

    resultHead := &ListNode{}
    result := resultHead
    node := head

    for node != nil && node.Next != nil {
        if node.Val == node.Next.Val {
            for node.Val == node.Next.Val {
                node.Next = node.Next.Next
            }
            node = node.Next
            continue
        }

        result.Next = &ListNode{
            Val: node.Val,
        }
        result = result.Next
        node = node.Next
    }

    return resultHead.Next
}
```

- ミス
    - struct のカンマ漏れ
    - result の `:=` 漏れ
    - result を更新していたので、結果が空リストになった
    - 2つ先のノードを見る、ということができていなかった
- 解答を確認する
    - 「ダミーノード」「センチネルノード」というものを使っていた
        - センチネルはイメージしやすい。先頭だけど。
- [解説動画](https://youtu.be/Y2gxc-p-KsI?si=jLMQoo4OK6FV9SvC)をみた
    - 重複をどう見つけるか
        - 今いるノードの次と、その次を見る
        - 重複していたら、異なる値のノードが出るまで進む
        - 今のノードの次を、異なる値のノードに繋げる
    - 先頭に重複があった場合どうするか
        - 新しいリンクリストの先頭を自分で作る
            - 返す時に、自分で作ったリストの先頭の次のノードを返せばいい
- 「ノードの追加」ではなく、「リンクの繋ぎ変え」

```go
func deleteDuplicates(head *ListNode) *ListNode {
    sentinel := &ListNode{
        Next: head,
    }

    node := sentinel
    // 今いるノードの次とその次を見る
    for node.Next != nil && node.Next.Next != nil {
        if node.Next.Val == node.Next.Next.Val {
            // 重複ノードなので、次の値まですべてスキップする
            // 今のノードの次のノードに視点を移す
            duplicated := node.Next
            // duplicated.Next: node の2つ先のノード
            for duplicated.Next != nil && duplicated.Val == duplicated.Next.Val {
                duplicated = duplicated.Next
            }
            // 今のノードの次を、重複ノードをスキップした次のノードにつなぎ変える
            node.Next = duplicated.Next
        } else {
            node = node.Next
        }
    }

    return sentinel.Next
}
```

## Step2

- 重複しない場合を先に処理する
    - 短いから
- 重複ノードに視線を移し、重複ノードと一つずつ取り除く
- 値が異なるノードを見つけたら、今のノードの次をそのノードにつなぎかえる
    - これで重複ノードをスキップする

```go
func deleteDuplicates(head *ListNode) *ListNode {
    sentinel := &ListNode{
        Next: head,
    }

    node := sentinel
    for node.Next != nil && node.Next.Next != nil {
        if node.Next.Val != node.Next.Next.Val {
            node = node.Next
            continue
        }

        duplicated := node.Next
        for duplicated.Next != nil && duplicated.Val == duplicated.Next.Val {
            duplicated = duplicated.Next
        }
        node.Next = duplicated.Next
    }

    return sentinel.Next
}
```

### レビュー依頼する方のPRを読む
りり
- [Arai60/82 by liruly · Pull Request #6 · liruly/leetcode](https://github.com/liruly/leetcode/pull/6)
    - 再帰を使ってできる
        - リストの長さが0または1の場合が停止条件
        - 重複ノードをスキップするケース
        - 重複ノードを削除したリストをつなげるケース
        - 思いつかなかった
            - 素直に読めると思った
            - 全て重複していない場合にスタックが深くなる
- [Create 82.RemoveDuplicatesFromSortedListII.md by Kazuuuuuuu-u · Pull Request #7 · Kazuuuuuuu-u/arai60](https://github.com/Kazuuuuuuu-u/arai60/pull/7/changes)
- [082-remove-duplicates-from-sorted-list-II by 05ryt31 · Pull Request #12 · 05ryt31/leetcode](https://github.com/05ryt31/leetcode/pull/12)
- [Remove duplicated form sorted list ⅱ by Rinta-Rinta · Pull Request #3 · Rinta-Rinta/LeetCode_arai60](https://github.com/Rinta-Rinta/LeetCode_arai60/pull/3)
- [82.Remove Duplicates from Sorted List II by sasakisyun · Pull Request #6 · sasakisyun/Arai60](https://github.com/sasakisyun/Arai60/pull/6/commits)

## Step3

- 解説動画にあったように、自分で追加したノードからスタートする画を頭に描いておく
    - ノートにも書く

```go
func deleteDuplicates(head *ListNode) *ListNode {
    sentinel := &ListNode{
        Next: head,
    }

    node := sentinel
    for node.Next != nil && node.Next.Next != nil {
        if node.Next.Val != node.Next.Next.Val {
            node = node.Next
            continue
        }

        duplicated := node.Next
        for duplicated.Next != nil && duplicated.Val == duplicated.Next.Val {
            duplicated = duplicated.Next
        }
        node.Next = duplicated.Next
    }

    return sentinel.Next
}
```

### 再帰版

```go
func deleteDuplicates(head *ListNode) *ListNode {
    if head == nil || head.Next == nil {
        return head
    }

    if head.Val != head.Next.Val {
        head.Next = deleteDuplicates(head.Next)
        return head
    }

    duplicated := head
    for duplicated.Next != nil && duplicated.Val == duplicated.Next.Val {
        duplicated = duplicated.Next
    }
    return deleteDuplicates(duplicated.Next)
}
```
