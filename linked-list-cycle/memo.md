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
