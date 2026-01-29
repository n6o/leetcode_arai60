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
        - フロイドの循環検出法と呼ばれている
    - 他の解法はないか考える
        - map で管理ができそうだけど、ノードの値が重複してたら誤検出する？
            - 制約はなさそう
            - ポインタで比較しているから、それを map に保存すれば検出できる


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

---

## map バージョン

- 空間計算量はO(n)になる

```go
/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func hasCycle(head *ListNode) bool {
    seen := map[*ListNode]bool{}

    currentNode := head
    for currentNode != nil {
        if seen[currentNode] {
            return true
        }

        seen[currentNode] = true
        currentNode = currentNode.Next
    }

    return false
}
```

---

## 補足

- [実行時間の概算について](https://github.com/Yuto729/LeetCode_arai60/pull/16#discussion_r2602118324)
    - Go は C++ より4倍くらい遅い
    - 概算: 2000万~2億ステップ/秒と思っておく
- [変数名中の英単語の省略については](https://github.com/hemispherium/LeetCode_Arai60/pull/10#discussion_r2618518592)
- goのポインタはuintptrで、アドレスを表現するのに十分な幅を持つ符号なし整数
    - [ドキュメント](https://go.dev/ref/spec#Numeric_types) には具体的な値は記載されていなかった
    - サイズはCPUアーキテクチャごとに異なるらしい
    - 64bit環境なら 64bit = 8byte らしい
        - [Go Playground](https://go.dev/play/p/TS2_rcQ1SQX) だと `8` だった
    - Bool のサイズは 1byte
    - 今回全ノードの情報がmapに保存されたとすると 9*10^4 byte = 90KB 程度必要となる
- [変数名について](https://github.com/Hiroto-Iizuka/coding_practice/pull/1#discussion_r2642270692)
    - `currentNode` ではなく `node` で十分伝わると思った
    - `読む助けになる情報がない`
