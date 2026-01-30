- 入力
    - `head`: リンクリストの先頭ノード
        - リストの長さは0以上10^4以下
        - ノードの値は-10^5以上10^5以下
- 出力
    - サイクルが始まるノード
        - サイクルがない場合は `null`
- 方針
    - ポインタを記録して、再び同じポインタを見つけたらそれが答え
        - 同じ？
        - follow up で空間計算量O(1)で解けるか聞かれている
            - まずは map を使ってみる

## Step1

```go
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func detectCycle(head *ListNode) *ListNode {
    seen := map[*ListNode]bool{}

    node := head
    for node != nil {
        if seen[node] {
            return node
        }

        seen[node] = true
        node = node.Next
    }

    return nil
}
```

