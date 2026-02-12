## 問題

[Kth Largest Element in a Stream - LeetCode](https://leetcode.com/problems/kth-largest-element-in-a-stream/description/)

- 入力
    - `k`: ストリームに残す数
        - 1以上`num`の長さ+1以下
            - `+1` はnumすべてと1回足せる分? 
            - add したときに k 番目がないことはないという保証か
    - `nums`: ストリームに与える初期値
        - 長さは0以上10^4以下
            - 長さ0の場合はどうなるか
        - 値は-10^4以上10^4以下
    - `val`: ストリームに加える値
        - 値は-10^4以上10^4以下
    - `add` は高々10^4回呼ばれる
- 出力
    - `add` が呼ばれたあとのストリームのなかでk番目の数
    - 最初は null <-  コンストラクタ呼び出しに対応？

## 解法

### 1. ソートして縮める

- 初期化時点で `num` を降順にソートする
- `add` のたびにソートする

### 2. 最小ヒープを使う

- `add` で push / peek する

## Step1

### 1. ソート

```go
type KthLargest struct {
    nums []int
    limit int
}


func Constructor(k int, nums []int) KthLargest {
    localNums := append([]int{}, nums...)
    slices.SortFunc(localNums, func(i, j int) int {
        return b - a
    })

    return KthLargest{
        nums: localNums,
        limit: k,
    }
}


func (this *KthLargest) Add(val int) int {
    this.nums = append(this.nums, val)
    slices.SortFunc(this.nums, func(i, j int) int {
        return j - i
    })
    this.nums = this.nums[:this.limit]
    return this.nums[this.limit-1]
}


/**
 * Your KthLargest object will be instantiated and called as such:
 * obj := Constructor(k, nums);
 * param_1 := obj.Add(val);
 */
```

- copy と append の使い分けがパッとわからなかった
- 毎回ソートしているから遅い
    - BinarySearch して insert することもできそう

#### 2分探索版

```go
type KthLargest struct {
    nums []int
    limit int
}


func Constructor(k int, nums []int) KthLargest {
    localNums := append([]int{}, nums...)
    slices.Sort(localNums)
    if len(localNums) > k {
        localNums = localNums[len(nums)-k:]
    }

    return KthLargest{
        nums: localNums,
        limit: k,
    }
}


func (this *KthLargest) Add(val int) int {
    insertIndex, _ := slices.BinarySearch(this.nums, val)
    this.nums = slices.Insert(this.nums, insertIndex, val)
    if len(this.nums) > this.limit {
        this.nums = this.nums[1:]
    }

    return this.nums[0]
}
```

- 単純なソートよりかは早くなった
- 時間計算量
    - Constructor: O(n log n) / slices.Sort
    - Add:
        - 2分探索は O(log k)
        - 挿入は O(k)
        - よって O(k)

### 2. 最小ヒープ

```go
import "container/heap"

type IntMinHeap []int

func (h IntMinHeap) Len() int {
    return len(h)
}

func (h IntMinHeap) Less(i, j int) bool {
    return h[i] < h[j]
}

func (h IntMinHeap) Swap(i, j int) {
    h[i], h[j] = h[j], h[i]
}

func (h *IntMinHeap) Push(x any) {
    *h = append(*h, x.(int))
}

func (h *IntMinHeap) Pop() any {
    old := *h
    n := len(old)
    x := old[n-1]
    *h = old[:n-1]
    return x
}

func (h IntMinHeap) Peek() int {
    return h[0]
}

type KthLargest struct {
    minHeap *IntMinHeap
    limit int
}

func Constructor(k int, nums []int) KthLargest {
    minHeap := &IntMinHeap{}
    heap.Init(minHeap)

    for _, n := range nums {
        heap.Push(minHeap, n)
        if minHeap.Len() > k {
            heap.Pop(minHeap)
        }
    }

    return KthLargest{
        minHeap: minHeap,
        limit: k,
    }
}

func (this *KthLargest) Add(val int) int {
    heap.Push(this.minHeap, val)
    if this.minHeap.Len() > this.limit {
        heap.Pop(this.minHeap)
    }

    return this.minHeap.Peek()
}


/**
 * Your KthLargest object will be instantiated and called as such:
 * obj := Constructor(k, nums);
 * param_1 := obj.Add(val);
 */
```

- heap 版は何も見ずには書けなかった
    - https://pkg.go.dev/container/heap
- IntMinHeap のメソッドに heap パッケージを閉じ込めたい気がした
- 時間計算量
    - Constructor: O(n log k)
    - Add: O(log k)


## Step2


### レビューを依頼する方のPR
- [703. Kth Largest Element in a Stream by TrsmYsk · Pull Request #10 · TrsmYsk/leetcode](https://github.com/TrsmYsk/leetcode/pull/10)
    - クイックソートの常識は説明できるまで頭に入ってない
    - クイックセレクトは初めて知った
    - k が負の場合は考えていなかった
    - データ構造を表す `minHeap` より、何のデータかを表す `topK` のほうが理解しやすい
        - データ構造は型でわかる
- [703. Kth Largest Element in a Stream by DaisukeKikukawa · Pull Request #9 · DaisukeKikukawa/LeetCode_arai60](https://github.com/DaisukeKikukawa/LeetCode_arai60/pull/9)
- [703. Kth Largest Element in a Stream by liruly · Pull Request #10 · liruly/leetcode](https://github.com/liruly/leetcode/pull/10)
- [703. Kth Largest Element in a Stream by aki235 · Pull Request #8 · aki235/Arai60](https://github.com/aki235/Arai60/pull/8)
    - map を使った方法もある

```go
import "container/heap"

type IntMinHeap []int

func NewIntMinHeap() *IntMinHeap {
    h := &IntMinHeap{}
    heap.Init(h)
    return h
}

func (h IntMinHeap) Len() int {
    return len(h)
}

func (h IntMinHeap) Less(i, j int) bool {
    return h[i] < h[j]
}

func (h IntMinHeap) Swap(i, j int) {
    h[i], h[j] = h[j], h[i]
}

func (h *IntMinHeap) Push(x any) {
    *h = append(*h, x.(int))
}

func (h *IntMinHeap) Pop() any {
    old := *h
    n := len(old)
    x := old[n-1]
    *h = old[:n-1]
    return x
}

func (h *IntMinHeap) PushInt(x int) {
    heap.Push(h, x)
}
func (h *IntMinHeap) PopInt() int {
    return heap.Pop(h).(int)
}

func (h IntMinHeap) Peek() int {
    return h[0]
}

type KthLargest struct {
    topK *IntMinHeap
    limit int
}

func Constructor(k int, nums []int) KthLargest {
    kthLargest := KthLargest{
        topK: NewIntMinHeap(),
        limit: k,
    }

    for _, n := range nums {
        kthLargest.Add(n)
    }

    return kthLargest
}

func (this *KthLargest) Add(val int) int {
    this.topK.PushInt(val)
    if this.topK.Len() > this.limit {
        this.topK.PopInt()
    }

    return this.topK.Peek()
}
```

- 長い。が、ヒープは書けそう。
    - `heap` を閉じ込めた構造体を作るのは、一度書き上げた後にまとめるのがよさそう

## Step3

```go
type IntMinHeap []int

func (h IntMinHeap) Len() int {
    return len(h)
}

func (h IntMinHeap) Less(i, j int) bool {
    return h[i] < h[j]
}

func (h IntMinHeap) Swap(i, j int) {
    h[i], h[j] = h[j], h[i]
}

func (h *IntMinHeap) Push(x any) {
    *h = append(*h, x.(int))
}

func (h *IntMinHeap) Pop() any {
    old := *h
    n := len(old)
    x := old[n-1]
    *h = old[:n-1]
    return x
}

func (h IntMinHeap) Peek() int {
    return h[0]
}

type KthLargest struct {
    topK *IntMinHeap
    limit int
}

func Constructor(k int, nums []int) KthLargest {
    minHeap := &IntMinHeap{}
    heap.Init(minHeap)

    kthLargest := KthLargest{
        topK: minHeap,
        limit: k,
    }

    for _, n := range nums {
        kthLargest.Add(n)
    }

    return kthLargest
}

func (this *KthLargest) Add(val int) int {
    heap.Push(this.topK, val)
    if this.topK.Len() > this.limit {
        heap.Pop(this.topK)
    }

    return this.topK.Peek()
}

```
