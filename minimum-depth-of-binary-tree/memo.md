## 問題

[Minimum Depth of Binary Tree - LeetCode](https://leetcode.com/problems/minimum-depth-of-binary-tree/)

- 入力
    - `root`: 2分木のルート
    - 木のノード数は0以上10^5以下
    - ノードの値は-1000以上1000以下
- 出力
    - ルートから一番近い葉へのノードの数

## 解法

### 1. BFSで一番近い葉を探す

- 深さごとにBFSで葉を探していく
- ノード数をnとすると
    - 時間計算量はO(n)
        - すべてのノードを1回ずつ訪問するため
    - 空間計算量はO(m): m はある深さにあるノードの数で n より小さい
        - キューに入れるノードの数の最大数

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
func minDepth(root *TreeNode) int {
    if root == nil {
        return 0
    }

    var depth int
    nodes := []*TreeNode{root}

    for len(nodes) > 0 {
        var nextNodes []*TreeNode
        depth++

        for _, node := range nodes {
            if node.Left == nil && node.Right == nil {
                return depth
            }

            if node.Left != nil {
                nextNodes = append(nextNodes, node.Left)
            }
            if node.Right != nil {
                nextNodes = append(nextNodes, node.Right)
            }
        }

        nodes = nextNodes
    }

    // invalid
    return -1
}
```

## Step2

- DFSでも最小値は求められる
    - 木全体を走査する
    - 実装はラク

### レビューを依頼する方のPR

- [111.Minimum-Depth-of-Binary-Tree by PafsCocotte · Pull Request #4 · PafsCocotte/leetcode](https://github.com/PafsCocotte/leetcode/pull/4/)
    - depth のインクリメントのタイミングについて
        - 内部のループをある深さの処理として見ているから、ということを考えた
    - ノードと深さをまとめてBFSするのもある
        - ネストが1段で済む
- [111. Minimum Depth of Binary Tree by TakayaShirai · Pull Request #22 · TakayaShirai/leetcode_practice](https://github.com/TakayaShirai/leetcode_practice/pull/22)
- [111. Minimum Depth of Binary Tree by dxxsxsxkx · Pull Request #22 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/22)
    - DFSで minDepth を更新しながら進める方法
- [111. Minimum Depth of Binary Tree by Yuto729 · Pull Request #27 · Yuto729/LeetCode_arai60](https://github.com/Yuto729/LeetCode_arai60/pull/27)
- [111. Minimum Depth of Binary Tree by mamo3gr · Pull Request #20 · mamo3gr/arai60](https://github.com/mamo3gr/arai60/pull/20)

### 深さを持つ構造体を使った場合

- 長いのと、参照を取り除く処理が入るのがノイズに感じた
    - go だとネストが深くても2重ループにするほうが好み

```go
/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
func minDepth(root *TreeNode) int {
    if root == nil {
        return 0
    }

    type nodeWithDepth struct {
        node *TreeNode
        depth int
    }

    nodes := []nodeWithDepth{
        {
            node: root,
            depth: 1,
        },
    }

    for len(nodes) > 0 {
        current := nodes[0]
        // GC対象にするため参照を外す
        nodes[0].node = nil
        nodes = nodes[1:]

        node := current.node
        depth := current.depth

        if node.Left == nil && node.Right == nil {
            return depth
        }

        if node.Left != nil {
            nodes = append(nodes, nodeWithDepth{
                node: node.Left,
                depth: depth + 1,
            })
        }
        if node.Right != nil {
            nodes = append(nodes, nodeWithDepth{
                node: node.Right,
                depth: depth + 1,
            })
        }
    }

    // invalid
    return -1
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
func minDepth(root *TreeNode) int {
    if root == nil {
        return 0
    }

    nodes := []*TreeNode{root}
    depth := 1

    for len(nodes) > 0 {
        var nextNodes []*TreeNode
        for _, node := range nodes {
            if node.Left == nil && node.Right == nil {
                return depth
            }

            if node.Left != nil {
                nextNodes = append(nextNodes, node.Left)
            }
            if node.Right != nil {
                nextNodes = append(nextNodes, node.Right)
            }

            nodes = nextNodes
        }

        depth++
    }

    // invalid
    return -1
}
```