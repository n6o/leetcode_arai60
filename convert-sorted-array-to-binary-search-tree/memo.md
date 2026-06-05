## 問題

[Convert Sorted Array to Binary Search Tree - LeetCode](https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/description/)

- 入力
    - `nums`: 昇順に整列した整数配列
        - 長さは1以上10^4以下
        - 値は-10^4以上10^4以下
        - 厳密に増加する順番
            - 重複している値はない
- 出力
    - 高さがバランスした2分木
        - 二つの木の高さの差が高々1である

## 解法

### 1. 真ん中で分割していく

- どうやって作るか
- 配列の真ん中をルートにして、左右の部分木を作る
    - mid = (len - 1) / 2
    - example 1 のもう一つの解の形になる
- 真ん中で分割していくため、木の構造は同じになる
    - 高さも2以上変わることはないはず
    - 証明っぽいことはできてないが
- 時間計算量はO(n)
    - すべての配列の要素を見ていく
- 空間計算量はO(n)
    - すべての配列の要素のノードを作成する
    - 再帰呼び出しもn回
    - スタックの深さは log n

## Step1

```go
/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
func sortedArrayToBST(nums []int) *TreeNode {
    if len(nums) == 0 {
        return nil
    }

    mid := (len(nums) - 1) / 2
    return &TreeNode{
        Val: nums[mid],
        Left: sortedArrayToBST(nums[:mid]),
        Right: sortedArrayToBST(nums[mid + 1:]),
    }
}
```

## Step2

- leetcode にある回答は基本的に同じだった
- mid の取り方でもう一方の構造の木になる
    - mid = len / 2
    - 0-indexで考えるか1-indexで考えるかの違いと理解した
    - 自分は基本0-indexで考える

```go
func sortedArrayToBST(nums []int) *TreeNode {
    if len(nums) == 0 {
        return nil
    }

    mid := (len(nums) - 1) / 2
    return &TreeNode{
        Val: nums[mid],
        Left: sortedArrayToBST(nums[:mid]),
        Right: sortedArrayToBST(nums[mid + 1:]),
    }
}
```

### レビューを依頼する方のPR

- [108._Convert_Sorted_Array_to_Binary_Search_Tree by arahi10 · Pull Request #3 · arahi10/coding-practice](https://github.com/arahi10/coding-practice/pull/3)
    - 反復型
- [108.Convert-Sorted-Array-to-Binary-Search-Tree by PafsCocotte · Pull Request #6 · PafsCocotte/leetcode](https://github.com/PafsCocotte/leetcode/pull/6/)
- [108. Convert Sorted Array to Binary Search Tree by TakayaShirai · Pull Request #24 · TakayaShirai/leetcode_practice](https://github.com/TakayaShirai/leetcode_practice/pull/24)
- [108. Convert Sorted Array to Binary Search Tree by dxxsxsxkx · Pull Request #24 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/24)
- [108. Convert Sorted Array to Binary Search Tree by dxxsxsxkx · Pull Request #24 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/24)
    - 親ノードと、子の範囲のインデックスを渡す
- [108-convert-sorted-array-to-binary-search-tree by 05ryt31 · Pull Request #15 · 05ryt31/leetcode](https://github.com/05ryt31/leetcode/pull/15)

### 反復版

- ノードの部品を渡していく
- スライスを伸ばしていくため、使用済みのポインタの参照をなくすようにした
- 時間計算量、空間計算量ともにO(n)
    - キューの長さはnまで伸びるかと思ったが、違った
        - [Appending to and copying slices](https://go.dev/ref/spec#Appending_and_copying_slices)
        - 基底配列を拡張する際に、スライスが参照している範囲が含まれる配列を新たに割り当てる
        - キューの長さは n / 2 程度まで
        - 8*3*5*10^3 -> 大体120KBくらい

```go
func sortedArrayToBST(nums []int) *TreeNode {
    if len(nums) == 0 {
        return nil
    }

    root := &TreeNode{}

    type Job struct {
        node *TreeNode
        start int
        end int
    }

    jobs := []Job{
        {
            node: root,
            start: 0,
            end: len(nums) - 1,
        },
    }

    for len(jobs) > 0 {
        job := jobs[0]
        // GC対象にするため
        jobs[0].node = nil
        jobs = jobs[1:]

        mid := job.start + (job.end - job.start) / 2
        job.node.Val = nums[mid]

        if job.start <= mid - 1 {
            job.node.Left = &TreeNode{}
            jobs = append(jobs, Job{
                node: job.node.Left,
                start: job.start,
                end: mid - 1,
            })
        }

        if mid + 1 <= job.end {
            job.node.Right = &TreeNode{}
            jobs = append(jobs, Job{
                node: job.node.Right,
                start: mid + 1,
                end: job.end,
            })
        }
    }

    return root
}
```

- 子の情報をキューに入れるときにチェックする必要があった
- 量が多くなるので、基本は再帰で実装すると思った
    - メモリ観点でも再帰の方が少なそう

## Step3

```go
func sortedArrayToBST(nums []int) *TreeNode {
    if len(nums) == 0 {
        return nil
    }

    mid := (len(nums) - 1) / 2
    return &TreeNode{
        Val: nums[mid],
        Left: sortedArrayToBST(nums[:mid]),
        Right: sortedArrayToBST(nums[mid + 1:]),
    }
}
```
