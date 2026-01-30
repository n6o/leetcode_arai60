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

- map version はできた
- O(1) を考える
    - 何も思いつかなかった
    - 2 pointers で解いている
    - slow と fast が出会ったら slow を head に戻している
        - slowとfastが一致するまでそれぞれをひとつずつ進める
        - slow == fast になったら slow が答え
    - サイクルがある場合、slowとfastが出会った時に下記が成り立つ
        - [slowが通った距離] = a + b
        - [fastが通った距離] = a + b + c + b = 2(a + b)
            - fastはslowの2倍の距離進むから
        - これを解くと a = c となる
            - a: head から出会ったノードまでのノード数
            - c: 出会ったノードからサイクルの起点までのノード数
            - fastがサイクルをn周して出会う場合も同様
        - だから片方を head に戻して同じだけ進めれば、サイクルの起点で出会うはず
        - 思いつけないな

## Step 2

- 2 pointers version

```go
func detectCycle(head *ListNode) *ListNode {
    fast := head
    slow := head

    for fast != nil && fast.Next != nil {
        fast = fast.Next.Next
        slow = slow.Next

        if fast == slow {
            fast = head
            for fast != slow {
                fast = fast.Next
                slow = slow.Next
            }
            return slow
        }
    }

    return nil
}
```

## Step3

- fast を動かすよう統一した

```go
func detectCycle(head *ListNode) *ListNode {
    fast := head
    slow := head

    for fast != nil && fast.Next != nil {
        fast = fast.Next.Next
        slow = slow.Next

        if fast == slow {
            fast = head
            for fast != slow {
                fast = fast.Next
                slow = slow.Next
            }
            return fast
        }
    }

    return nil
}
```

---

- ネストを浅くする
- 変数名を意味のあるものにする

```go
func detectCycle(head *ListNode) *ListNode {
    fast := head
    slow := head
    var met bool

    for fast != nil && fast.Next != nil {
        fast = fast.Next.Next
        slow = slow.Next

        if fast == slow {
            met = true
            break
        }
    }

    if !met {
        return nil
    }

    fromHead := head
    fromMeet := fast
    for fromHead != fromMeet {
        fromHead = fromHead.Next
        fromMeet = fromMeet.Next
    }

    return fromHead
}
```

- 無限ループを使って書ける
    - met が要らなくなる
    - ぱっと見で少し驚く気がする
        - どちらを選ぶかと言われると、 met 使うコードを採用すると思う
            - 処理が素直に追えるから

```go
func detectCycle(head *ListNode) *ListNode {
    fast := head
    slow := head

    for {
        // There is no cycle.
        if fast == nil || fast.Next == nil {
            return nil
        }

        fast = fast.Next.Next
        slow = slow.Next

        // Detected.
        if fast == slow {
            break
        }
    }

    fromHead := head
    fromMeet := fast
    for fromHead != fromMeet {
        fromHead = fromHead.Next
        fromMeet = fromMeet.Next
    }

    return fromHead
}
```
