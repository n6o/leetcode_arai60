## 問題

[Validate Binary Search Tree - LeetCode](https://leetcode.com/problems/validate-binary-search-tree/description/)

- 入力
    - `root`: ルートノード
        - 木のノード数は1以上10^4以下
        - 各ノードの値は-2^31以上2^31-1以下
            - 32bit整数
- 出力
    - 2分探索木ならtrue

## 解法

### 1. 各ノードで左と右の子の値を見る（動かない）

- 左の子の値と右の子の値と自分の値がわかる
    - 左の子の値 < 自分の値 < 右の子の値 になっているか確認する
    - なっていたら、左の子、右の子それぞれに、確認を依頼する
    - どちらもOKならOKと返す
- 各ノードを1回ずつ見るから時間計算量はO(n)
- 2分探索木の定義をわかっていなかった
    - NG: [5,4,6,null,null,3,7]
    - ルートの右の部分木のすべてのノードの値はルートの値より大きくなければならない
    - ルートの左の部分木のすべてのノードの値はルートの値より小さくなければならない

### 2. 木のノードの取りうる範囲を渡して判定する

- ルートの値が数直線上にのるイメージ
- 部分木のルートも数直線上にのる
- 部分木のノードはある範囲内に収まっている必要がある
    - 範囲が書かれたメモをもらうイメージ
- 各ノードを1回ずつ見るから時間計算量はO(n)
- 再帰呼び出しするから、空間計算量はO(log n)?
    - 木の高さ分だけスタックを積む

## Step1

### 1. 動かない

```go
/**
 * Definition for a binary tree node.
 * type TreeNode struct {
 *     Val int
 *     Left *TreeNode
 *     Right *TreeNode
 * }
 */
func isValidBST(root *TreeNode) bool {
    if root == nil {
        return true
    }

    leftNode := root.Left
    if leftNode != nil && leftNode.Val >= root.Val {
        return false
    }

    rightNode := root.Right
    if rightNode != nil && rightNode.Val <= root.Val {
        return false
    }

    return isValidBST(leftNode) && isValidBST(rightNode)
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
func isValidBST(root *TreeNode) bool {
    if root == nil {
        // 問題設定上はこの分岐には入らない
        // 空の木は2分探索木とする
        return true
    }

    leftNodeRange := NodeRange{start: math.MinInt, end: root.Val}
    rightNodeRange := NodeRange{start: root.Val, end: math.MaxInt}

    leftIsValid := isValidBSTWithNodeRange(root.Left, leftNodeRange)
    rightIsValid := isValidBSTWithNodeRange(root.Right, rightNodeRange)

    return leftIsValid && rightIsValid
}

type NodeRange struct {
    start int
    end int
}

func (r NodeRange) leftNodeRange(rootValue int) NodeRange {
    return NodeRange{
        start: r.start,
        end: rootValue,
    }
}

func (r NodeRange) rightNodeRange(rootValue int) NodeRange {
    return NodeRange{
        start: rootValue,
        end: r.end,
    }
}

func (r NodeRange) contains(value int) bool {
    return r.start < value && value < r.end
}

func isValidBSTWithNodeRange(root *TreeNode, nodeRange NodeRange) bool {
    if root == nil {
        return true
    }

    if !nodeRange.contains(root.Val) {
        return false
    }

    leftIsValid := isValidBSTWithNodeRange(root.Left, nodeRange.leftNodeRange(root.Val))
    rightIsValid := isValidBSTWithNodeRange(root.Right, nodeRange.rightNodeRange(root.Val))

    return leftIsValid && rightIsValid
}
```

## Step2

- leetcode の解答例を見る
    - 記述量少ない
    - validate
    - lower / upper を使う
- 参考に改変する
    - `NodeRange` 構造体はほしくなる
        - `range` は go の予約語
        - `Contains` だと境界上も含まれそうな感じなので `IsBetween` にした
            - 何かのアサーションライブラリになかったかな
            - コメントで補足する
        - `IsBetween` の引数を `TreeNode` にしてもいいかも
            - パッケージ次第。今回は int で十分と考えた

```go
func isValidBST(root *TreeNode) bool {
    return validate(root, NodeRange{
        lower: math.MinInt,
        upper: math.MaxInt,
    })
}

func validate(node *TreeNode, nodeRange NodeRange) bool {
    if node == nil {
        return true
    }

    if !nodeRange.IsBetween(node.Val) {
        return false
    }
    
    leftIsValid := validate(node.Left, NodeRange{
        lower: nodeRange.lower,
        upper: node.Val,
    })
    rightIsValid := validate(node.Right, NodeRange{
        lower: node.Val,
        upper: nodeRange.upper,
    })

    return leftIsValid && rightIsValid
}

type NodeRange struct {
    lower int
    upper int
}

func (r *NodeRange) IsBetween(v int) bool {
    return r.lower < v && v < r.upper
}
```

### レビューを依頼する方のPR

- [98. validate binary search tree by 5ky7 · Pull Request #21 · 5ky7/arai60](https://github.com/5ky7/arai60/pull/21)
    - cpp
    - シンプルなデータ構造 => 処理速度が速くメモリ使用量が少なくなる可能性がある
    - TraverseInorder が何をしているのかわからなかった
        - inorder でノードの値を格納していき、並び順をチェックするみたい
    - BFSっぽいコードもあった。node と range を送ってチェックする感じ
- [Validate Binary Search Tree by plushn · Pull Request #28 · plushn/SWE-Arai60](https://github.com/plushn/SWE-Arai60/pull/28)
    - `itertools`
        - https://docs.python.org/ja/3/library/itertools.html
    - 問題が変わったのか、制約などが異なっていた
    - BFS
        - 木構造のときにBFSを使うという発想が出てこないので、練習しようと思った
        - グラフの一種なんだし
- [Leetcode 98. Validate Binary Search Tree by huyfififi · Pull Request #39 · huyfififi/coding-challenges](https://github.com/huyfififi/coding-challenges/pull/39)
    - `if not (lower_bound < node.val < upper_bound):`
        - こんな書き方できるんだ
- [98. Validate Binary Search Tree by mamo3gr · Pull Request #26 · mamo3gr/arai60](https://github.com/mamo3gr/arai60/pull/26)
    - ボトムアップの解法もある。読みにくいらしい。あとで読めたら読もう。
- [98. Validate Binary Search Tree by dxxsxsxkx · Pull Request #28 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/28)
    - 木の形でスタックオーバーフローする可能性がある
        - go は1GBまで伸びるので、この問題設定では大丈夫そう

## Step3

```go
func isValidBST(root *TreeNode) bool {
    return validate(root, NodeRange{
        lower: math.MinInt,
        upper: math.MaxInt,
    })
}

func validate(node *TreeNode, nodeRange NodeRange) bool {
    if node == nil {
        return true
    }

    if !nodeRange.Contains(node.Val) {
        return false
    }
    
    leftIsValid := validate(node.Left, NodeRange{
        lower: nodeRange.lower,
        upper: node.Val,
    })
    rightIsValid := validate(node.Right, NodeRange{
        lower: node.Val,
        upper: nodeRange.upper,
    })

    return leftIsValid && rightIsValid
}

type NodeRange struct {
    lower int
    upper int
}

func (r *NodeRange) Contains(v int) bool {
    return r.lower < v && v < r.upper
}
```
