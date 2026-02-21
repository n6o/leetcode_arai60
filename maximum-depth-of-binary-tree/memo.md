## 問題

[Maximum Depth of Binary Tree - LeetCode](https://leetcode.com/problems/maximum-depth-of-binary-tree/description/)

- 入力
    - `root`: ルートノード
        - 木のノードの数は0以上10^4以下
        - ノードの値は -100以上100以下
- 出力
    - 木の深さ

## 解法

### 1. 再帰DFS

- 左右の部分木の深さを聞いて、大きい方に1を足して返すイメージ
- ノードが nil なら深さは 0 
- nil でなければ左右の部分木の深さを求め、1を足す
- 大きい方の値を返す
- 木のノードの数を n とすると
    - 時間計算量は O(n)
        - 各ノードを訪れるので
        - ノード数は10^4以下なので問題なさそう
    - 空間計算量は O(n)
        - スタックの深さ
        - 最悪の場合は一直線

### 2. 反復DFS

- nilでない子ノードをスタックに積んでいく
    - 左から見ていきたいので、右から積む
    - そのノードの深さを一緒に管理する
- 計算量は同じ

### 3. BFS

- 木の深さごとにノードをキューに入れていく
- 計算量は同じ
    - 空間計算量が最大になるのは子の数が最も多い深さのとき

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
func maxDepth(root *TreeNode) int {
    if root == nil {
        return 0
    }

    leftDepth := maxDepth(root.Left)
    rightDepth := maxDepth(root.Right)
    
    return max(leftDepth, rightDepth) + 1
}
```

### 2.

```go
/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
func maxDepth(root *TreeNode) int {
    if root == nil {
        return 0
    }

    var maxDepth int
    nodesToVisit := []NodeWithDepth{
        {node: root, depth: 1},
    }

    for len(nodesToVisit) > 0 {
        topIndex := len(nodesToVisit) - 1 
        nodeWithDepth := nodesToVisit[topIndex]
        // GC対象にするため参照を外す
        nodesToVisit[topIndex].node = nil
        nodesToVisit = nodesToVisit[:topIndex]

        maxDepth = max(nodeWithDepth.depth, maxDepth)

        node := nodeWithDepth.node

        if node.Right != nil {
            nodesToVisit = append(nodesToVisit, NodeWithDepth{
                node: node.Right,
                depth: nodeWithDepth.depth + 1,
            })
        }
        if node.Left != nil {
            nodesToVisit = append(nodesToVisit, NodeWithDepth{
                node: node.Left,
                depth: nodeWithDepth.depth + 1,
            })
        }
    }

    return maxDepth
}

type NodeWithDepth struct {
    node *TreeNode
    depth int
}
```

### 3.

```go
/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
func maxDepth(root *TreeNode) int {
    if root == nil {
        return 0
    }

    var maxDepth int
    nodes := []*TreeNode{root}

    for len(nodes) > 0 {
        var nextNodes []*TreeNode
        maxDepth++

        for _, node := range nodes {
            if node.Left != nil {
                nextNodes = append(nextNodes, node.Left)
            }
            if node.Right != nil {
                nextNodes = append(nextNodes, node.Right)
            }
        }

        nodes = nextNodes
    }

    return maxDepth
}
```

## Step2

- 再帰版がいちばんしっくりくる

```go
func maxDepth(root *TreeNode) int {
    if root == nil {
        return 0
    }

    leftDepth := maxDepth(root.Left)
    rightDepth := maxDepth(root.Right)
    
    return max(leftDepth, rightDepth) + 1
}
```

### レビューを依頼する方のPR

- [104. Maximum Depth of Binary Tree by TakayaShirai · Pull Request #21 · TakayaShirai/leetcode_practice](https://github.com/TakayaShirai/leetcode_practice/pull/21)
- [104_maximum_depth_of_binary_tree by Hiroto-Iizuka · Pull Request #21 · Hiroto-Iizuka/coding_practice](https://github.com/Hiroto-Iizuka/coding_practice/pull/21)
    - 左右の部分木の深さを変数にしないほうを好む人もいる
        - 変数を使う箇所が1箇所しかない場合、変数を使わないようにするというレビューになるケースはある
    - `return max(maxDepth(root.Left), maxDepth(root.Right)) + 1`
        - 読みにくいと感じたので分けたけど、そこまで読みにくいというわけではない
        - そういうレビューが付いたらまとめてもいい程度
- [104. Maximum Depth of Binary Tree by dxxsxsxkx · Pull Request #21 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/21)
- [104. Maximum Depth of Binary Tree by mamo3gr · Pull Request #21 · mamo3gr/arai60](https://github.com/mamo3gr/arai60/pull/21)
- [104. Maximum Depth of Binary Tree by Yuto729 · Pull Request #26 · Yuto729/LeetCode_arai60](https://github.com/Yuto729/LeetCode_arai60/pull/26)

## Step3

```go
func maxDepth(root *TreeNode) int {
    if root == nil {
        return 0
    }

    return max(maxDepth(root.Left), maxDepth(root.Right)) + 1
}
```
