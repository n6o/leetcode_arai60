## 問題

[Path Sum - LeetCode](https://leetcode.com/problems/path-sum/description/)

- 入力
    - `root`: 2分木のルート
        - ノード数は0以上5000以下
        - ノードの値は-1000以上1000以下
        - 合計値は `-5*10^6` 以上 `5*10^6` 以下
    - `targetSum`: 整数
        - 値は-1000以上1000以下
- 出力
    - ルートから葉までのパスのノードの合計が `targetSum` となるパスがあれば `true`

## 解法

### 1. DFS

- DFSを使って探索する
    - それまでの合計値と現在のノードの情報をもらう
    - 現在のノードが葉であれば合計値を計算し `targetSum` であればおしまい
    - 子がある場合はスタックに積む
- 時間計算量は O(n)
- 空間計算量は O(n)
    - 最悪の場合はスタックにn個積まれる

### 2. 再帰

- 再帰を使って書けそう
- あとでやる

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
func hasPathSum(root *TreeNode, targetSum int) bool {
    if root == nil {
        return false
    }

    type Job struct {
        node *TreeNode
        sum int
    }

    jobs := []Job{
        {
            node: root,
            sum: 0,
        },
    }

    for len(jobs) > 0 {
        job := jobs[len(jobs) - 1]
        jobs = jobs[:len(jobs) - 1]

        node := job.node
        sum := job.sum + node.Val
        if node.Right == nil && node.Left == nil {
            if sum == targetSum {
                return true
            }

            continue
        }

        if node.Right != nil {
            jobs = append(jobs, Job{
                node: node.Right,
                sum: sum,
            })
        }
        if node.Left != nil {
            jobs = append(jobs, Job{
                node: node.Left,
                sum: sum,
            })
        }
    }

    return false
}
```

## Step2

### レビューを依頼する方のPR

- [112.path-sum by PafsCocotte · Pull Request #7 · PafsCocotte/leetcode](https://github.com/PafsCocotte/leetcode/pull/7)
    - 再帰を使う
- [112. Path Sum by TakayaShirai · Pull Request #25 · TakayaShirai/leetcode_practice](https://github.com/TakayaShirai/leetcode_practice/pull/25)
    - スタックに積む前に nil チェックするか
    - スタックから取り出した後に nil チェックするか
    - 取り出した後にするコードをよく見る気がする
    - 分岐が減らせる & ガード節で認知負荷減る、から好まれているのだろうか
- [112. Path Sum by dxxsxsxkx · Pull Request #25 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/25)
    - sum の計算タイミングが自分と異なっていた
        - 引き継ぎの感覚の違いだろうか
- [112-path-sum by 05ryt31 · Pull Request #16 · 05ryt31/leetcode](https://github.com/05ryt31/leetcode/pull/16)
- [112. Path Sum by mamo3gr · Pull Request #24 · mamo3gr/arai60](https://github.com/mamo3gr/arai60/pull/24)
    - `is_leaf` の変数化
        - 1度しか参照しない場合の是非はチームによるか
        - インラインにするレビューを見たことがあるので
        - 読みやすいので練習会では採用する

### 再帰版

```go
func hasPathSum(root *TreeNode, targetSum int) bool {
    if root == nil {
        return false
    }

    remaining := targetSum - root.Val
    isLeaf := root.Left == nil && root.Right == nil

    if isLeaf {
        return remaining == 0    
    }

    return hasPathSum(root.Left, remaining) || hasPathSum(root.Right, remaining)
}
```

## Step3

```go
func hasPathSum(root *TreeNode, targetSum int) bool {
    if root == nil {
        return false
    }

    remaining := targetSum - root.Val
    isLeaf := root.Left == nil && root.Right == nil

    if isLeaf {
        return remaining == 0    
    }

    return hasPathSum(root.Left, remaining) || hasPathSum(root.Right, remaining)
}
```
