## 問題

[Binary Tree Level Order Traversal - LeetCode](https://leetcode.com/problems/binary-tree-level-order-traversal/description/)

- 入力
    - `root`: 二分木のルート
        - ノードの数は0以上2000以下
        - ノードの値は-1000以上1000以下
- 出力
    - 各レベルのノードの値をリストとして返す
        - 左から右の順番

## 解法

### 1. BFSでレベルごとにノードを処理する

- キューを使って、各レベルのノードを順番に処理する
    - 各レベルでリストを作成する
- 時間計算量は O(n)
    - 各ノードを一度ずつ処理するため
- 空間計算量は O(n)
    - 最悪の場合、最後のレベルにノードが n/2 個存在するため

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
func levelOrder(root *TreeNode) [][]int {
    if root == nil {
        return nil
    }
    
    visiting := []*TreeNode{root}
    var groups [][]int

    for len(visiting) > 0 {
        var nextVisiting []*TreeNode
        var group []int

        for _, node := range visiting {
            group = append(group, node.Val)

            if node.Left != nil {
                nextVisiting = append(nextVisiting, node.Left)
            }
            if node.Right != nil {
                nextVisiting = append(nextVisiting, node.Right)
            }
        }

        groups = append(groups, group)
        visiting = nextVisiting
    }

    return groups
}
```

## Step2

### レビューを依頼する方のPR

## Step3

## ふりかえり
