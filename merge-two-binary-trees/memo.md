## 問題

[Merge Two Binary Trees - LeetCode](https://leetcode.com/problems/merge-two-binary-trees/description/)

- 入力
    - `root1` / `root2`: 2分木のルート
        - ノード数は0以上2000以下
        - ノードの値は-10^4以上10^4以下
            - 合計値は-2*10^4以上2*10^4以下
- 出力
    - 2つの2分木をマージした木

## 解法

### 1. 部分木をマージしていく

- 同期してマージすることをまず考えた
    - null ノードがあると難しそうだった
- 再帰を使うことを考えた
- ルート同士をマージする
- 左の部分木をマージする
- 右の部分木をマージする
- 片方が null ノードの場合、そこでマージ作業はストップできる
    - null じゃないほうの木を返せばいい
- ノード数をn1, n2とすると
    - 時間計算量は O(min(n1, n2))
        - 途中で再帰が止まるケースがあるから
    - 空間計算量は O(min(log n1, log n2))
        - スタックの深さ分

## Step1

### 1.

```go
/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
func mergeTrees(root1 *TreeNode, root2 *TreeNode) *TreeNode {
    if root1 == nil && root2 == nil {
        return nil
    } else if root1 == nil {
        return root2
    } else if root2 == nil {
        return root1
    }

    newValue := root1.Val + root2.Val
    newLeft := mergeTrees(root1.Left, root2.Left)
    newRight := mergeTrees(root1.Right, root2.Right)
    
    return &TreeNode{
        Val: newValue,
        Left: newLeft,
        Right: newRight,
    }
}
```

- newX は変数化しなくてもよさそう
- `root1 == nil && root2 == nil` はなくても動く
    - ただ、明示的に記載する方が読みやすいと感じた
- 反復を使う方法もある
    - コード量が多くなる
    - 構造体を定義して書くと思った

## Step2

```go
/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
func mergeTrees(root1 *TreeNode, root2 *TreeNode) *TreeNode {
    if root1 == nil && root2 == nil {
        return nil
    } else if root1 == nil {
        return root2
    } else if root2 == nil {
        return root1
    }

    return &TreeNode{
        Val: root1.Val + root2.Val,
        Left: mergeTrees(root1.Left, root2.Left),
        Right: mergeTrees(root1.Right, root2.Right),
    }
}
```

### レビューを依頼する方のPR

- [617. Merge Two Binary Trees by TakayaShirai · Pull Request #23 · TakayaShirai/leetcode_practice](https://github.com/TakayaShirai/leetcode_practice/pull/23)
- [617. Merge Two Binary Trees by dxxsxsxkx · Pull Request #23 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/23)
- [617. Merge Two Binary Trees by Yuto729 · Pull Request #28 · Yuto729/LeetCode_arai60](https://github.com/Yuto729/LeetCode_arai60/pull/28)
- [617-merge-two-binary-trees by 05ryt31 · Pull Request #14 · 05ryt31/leetcode](https://github.com/05ryt31/leetcode/pull/14)
- [617. Merge Two Binary Trees by mamo3gr · Pull Request #22 · mamo3gr/arai60](https://github.com/mamo3gr/arai60/pull/22)

### 反復版

- 方針は2つ
    - 自分を作って親につなげる
    - 子を作る
- 子を作る方が、左右の判定が不要になるので読みやすかった

```go
/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
func mergeTrees(root1 *TreeNode, root2 *TreeNode) *TreeNode {
    if root1 == nil && root2 == nil {
        return nil
    } else if root1 == nil {
        return root2
    } else if root2 == nil {
        return root1
    }

    type Job struct {
        newNode *TreeNode
        node1 *TreeNode
        node2 *TreeNode
    }

    newRoot := &TreeNode{
        Val: root1.Val + root2.Val,
    }

    jobs := []Job{{
        newNode: newRoot,
        node1: root1,
        node2: root2,
    }}
    for len(jobs) > 0 {
        job := jobs[len(jobs) - 1]
        jobs = jobs[:len(jobs) - 1]

        newLeft, leftHasNewChild := newNode(job.node1.Left, job.node2.Left)
        job.newNode.Left = newLeft
        if leftHasNewChild {
            jobs = append(jobs, Job{
                newNode: newLeft,
                node1: job.node1.Left,
                node2: job.node2.Left,
            })            
        }

        newRight, rightHasNewChild := newNode(job.node1.Right, job.node2.Right)
        job.newNode.Right = newRight
        if rightHasNewChild {
            jobs = append(jobs, Job{
                newNode: newRight,
                node1: job.node1.Right,
                node2: job.node2.Right,
            })            
        }
    }

    return newRoot
}

// 新しいノードを作成する
// 新しいノードの子ノードを作成する必要がある場合は true を返す
func newNode(node1 *TreeNode, node2 *TreeNode) (*TreeNode, bool) {
    if node1 == nil && node2 == nil {
        return nil, false
    } else if node1 == nil {
        return node2, false
    } else if node2 == nil {
        return node1, false
    }

    return &TreeNode{
        Val: node1.Val + node2.Val,
    }, true
}
```

## Step3

```go
/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
func mergeTrees(root1 *TreeNode, root2 *TreeNode) *TreeNode {
    if root1 == nil && root2 == nil {
        return nil
    } else if root1 == nil {
        return root2
    } else if root2 == nil {
        return root1
    }

    return &TreeNode{
        Val: root1.Val + root2.Val,
        Left: mergeTrees(root1.Left, root2.Left),
        Right: mergeTrees(root1.Right, root2.Right),
    }
}
```
