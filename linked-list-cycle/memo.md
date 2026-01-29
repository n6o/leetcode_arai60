# linked-list-cycle

[Linked List Cycle - LeetCode](https://leetcode.com/problems/linked-list-cycle/description/)

- 入力
    - `head`: リンクリストの先頭ノード
        - リストの長さは0以上10^4以下
        - リストの値は-10^5以上10^5以下
- 出力
    - サイクルがあれば `true`、なければ `false`
- 方針
    - 2ポインタを使えば解けることを知っていた
        - 周回遅れを見つけたらいい
    - 他の解法はないか考える
        - map で管理ができそうだけど、ノードの値が重複してたら誤検出する？
            - 制約はなさそう


```go
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func hasCycle(head *ListNode) bool {
    fast := head
    slow := head

    for fast != nil {
        if fast.Next != nil {
            fast = fast.Next.Next
        } else {
            return false
        }
        slow = slow.Next

        if fast == slow {
            return true
        }
    }

    return false
}
```

---

## Step2

- `for` の条件式を「fast の指すノードと次のノードが `nil` でない」とするとスッキリ書ける。
- fast と slow を同時に初期化してる解答もあった。
- コメントを書くとしたら変数の初期化の箇所だろうか

```go
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func hasCycle(head *ListNode) bool {
    // Move fast pointer by two steps
    fast, slow := head, head

    for fast != nil && fast.Next != nil {
        fast = fast.Next.Next
        slow = slow.Next

        if fast == slow {
            return true
        }
    }

    return false
}
```

---

## Step3

```go
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func hasCycle(head *ListNode) bool {
    fast, slow := head, head

    for fast != nil && fast.Next != nil {
        fast = fast.Next.Next
        slow = slow.Next

        if fast == slow {
            return true
        }
    }

    return false
}
```
