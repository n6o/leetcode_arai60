## 問題

[Find K Pairs with Smallest Sums - LeetCode](https://leetcode.com/problems/find-k-pairs-with-smallest-sums/description/)

- 入力
    - `num1`: 整数配列
    - `num2`: 整数配列
        - どちらも非減少な順番
        - 長さは1以上10^5以下
        - 値は-10^9以上10^9以下
    - `k`: 整数
        - 1以上10^4以下
        - また num1の長さとnum2の長さの積以下
- 出力
    - 2つの配列から1つずつ選んだペアの和の合計が小さい順に並べた時の最初の `k` 個のペアのリスト

## 解法

- ペアは最大で10^10個できる
    - 10^9くらいまでしかできない?
    - すべてのペアを見るとタイムオーバーしそう
        - 小さい順に入れていきたい
            - どうやって？
        - k をどこかで使いたい
    - go でのだいたいのオーダーを覚えておく
        - [以前のメモ](https://github.com/n6o/leetcode_arai60/pull/1/changes#diff-ba72373db372dc7a3dad0d582c3dc579dd71784278c3b94966f613f023045603R146)
- ペアの和は-10^9 * 2以上2 * 10^9以下
    - int で保持できる

### 1. 最大ヒープを使う

- k個の要素を保持する最大ヒープに入れていく
- go では ["container/heap"](https://pkg.go.dev/container/heap) モジュールを使う
    - 指定されているインターフェースを実装した構造体を定義するとヒープ操作をしてくれる関数が用意されている

### 

## Step1

### 1.

とりあえず総当たりで実装した。
TLE になった。

```go
import "container/heap"

func kSmallestPairs(nums1 []int, nums2 []int, k int) [][]int {
    minK := &maxPairHeap{}
    heap.Init(minK)

    for _, value1 := range nums1 {
        for _, value2 := range nums2 {
            heap.Push(minK, pair{
                value1: value1,
                value2: value2,
                sum: value1 + value2,
            })
            if minK.Len() > k {
                heap.Pop(minK)
            }
        }
    }
    
    result := make([][]int, k)
    for i := range result {
        pair := heap.Pop(minK).(pair)
        row := []int{
            pair.value1,
            pair.value2,
        }
        result[i] = row
    }

    return result
}

type pair struct {
    value1 int
    value2 int
    sum int
}

type maxPairHeap []pair

func (h maxPairHeap) Len() int {
    return len(h)
}

func (h maxPairHeap) Less(i, j int) bool {
    return h[j].sum < h[i].sum
}

func (h maxPairHeap) Swap(i, j int) {
    h[i], h[j] = h[j], h[i]
}

func (h *maxPairHeap) Push(x any) {
    *h = append(*h, x.(pair))
}

func (h *maxPairHeap) Pop() any {
    old := *h
    n := len(old)
    x := old[n-1]
    *h = old[:n-1]
    return x
}
```

- leetcode の解答例を見た
- 小さい順に最小ヒープに入れるようにしていた
- `nums1` も `nums2` も非減少な順番なので、 `nums1` の各要素と `nums2[0]` をスタートとするリストのリストを使うイメージ
    - 最小ヒープに入れる
    - ヒープから取り出した要素はその時点での最小
    - その要素の次に大きな要素は何かわからない
    - しかし、各行で見ると非減少の列になっている
    - だから、取り出したペアの `nums2` のインデックスをインクリメントしたペアをヒープに入れる
        - 値ではなくインデックスを保持しておく必要がある
    - それが現時点での最小ペアの候補の集合となる
    - これをk回繰り返す
- `nums1` * `nums2` の行列で0列を最初の最小ペアの候補として、その集合を動かしていくイメージ
    - スイムレーンみたいな。リレーしている感じ

## Step2

```go
import "container/heap"

func kSmallestPairs(nums1 []int, nums2 []int, k int) [][]int {
    minCandidates := &minPairHeap{}
    heap.Init(minCandidates)

    for i := range nums1 {
        heap.Push(minCandidates, pair{
            index1: i,
            index2: 0,
            sum: nums1[i] + nums2[0],
        })
    }

    result := make([][]int, 0, k)
    for len(result) < k && minCandidates.Len() > 0 {
        minPair := heap.Pop(minCandidates).(pair)
        result = append(result, []int{ nums1[minPair.index1], nums2[minPair.index2] })

        nextIndex2 := minPair.index2 + 1
        if nextIndex2 < len(nums2) {
            heap.Push(minCandidates, pair{
                index1: minPair.index1,
                index2: nextIndex2,
                sum: nums1[minPair.index1] + nums2[nextIndex2],
            })
        }
    }
 
    return result
}

type pair struct {
    index1 int
    index2 int
    sum int
}

type minPairHeap []pair

func (h minPairHeap) Len() int {
    return len(h)
}

func (h minPairHeap) Less(i, j int) bool {
    return h[i].sum < h[j].sum
}

func (h minPairHeap) Swap(i, j int) {
    h[i], h[j] = h[j], h[i]
}

func (h *minPairHeap) Push(x any) {
    *h = append(*h, x.(pair))
}

func (h *minPairHeap) Pop() any {
    old := *h
    n := len(old)
    x := old[n-1]
    *h = old[:n-1]
    return x
}
```

- 時間計算量:
    - ヒープサイズは最大でnum1
    - 最初の候補を入れるのに O(num1 log num1)
    - 最小のk個のループで O(k log num1)
    - 全体では O( (num1+k) log num1 )
- 空間計算量: O(k)

### レビューを依頼する方のPR

- [373.find k pairs with smallest sums by PafsCocotte · Pull Request #1 · PafsCocotte/leetcode](https://github.com/PafsCocotte/leetcode/pull/1)
- [373. Find K Pairs with Smallest Sums by aki235 · Pull Request #10 · aki235/Arai60](https://github.com/aki235/Arai60/pull/10)
- [373. Find K Pairs With Smallest Sums by xbam326 · Pull Request #12 · xbam326/leetcode](https://github.com/xbam326/leetcode/pull/12)
- [373_find_k_pairs_with_smallest_sums by Hiroto-Iizuka · Pull Request #10 · Hiroto-Iizuka/coding_practice](https://github.com/Hiroto-Iizuka/coding_practice/pull/10)
- [373. Find K Pairs with Smallest Sums by mamo3gr · Pull Request #10 · mamo3gr/arai60](https://github.com/mamo3gr/arai60/pull/10)
- [コメント集](https://docs.google.com/document/d/11HV35ADPo9QxJOpJQ24FcZvtvioli770WWdZZDaLOfg/edit?tab=t.0#heading=h.527w0lse8gbd)

## Step3

```go
import "container/heap"

func kSmallestPairs(nums1 []int, nums2 []int, k int) [][]int {
    minPairCandidates := &minPairHeap{}
    heap.Init(minPairCandidates)

    for i := range nums1 {
        heap.Push(minPairCandidates, pair{
            index1: i,
            index2: 0,
            sum: nums1[i] + nums2[0],
        })
    }

    result := make([][]int, 0, k)
    for len(result) < k && minPairCandidates.Len() > 0 {
        minPair := heap.Pop(minPairCandidates).(pair)
        result = append(result, []int{ nums1[minPair.index1], nums2[minPair.index2] })

        nextIndex2 := minPair.index2 + 1
        if nextIndex2 < len(nums2) {
            heap.Push(minPairCandidates, pair{
                index1: minPair.index1,
                index2: nextIndex2,
                sum: nums1[minPair.index1] + nums2[nextIndex2],
            })
        }
    }

    return result
}

type pair struct {
    index1 int
    index2 int
    sum int
}

type minPairHeap []pair

func (h minPairHeap) Len() int {
    return len(h)
}

func (h minPairHeap) Less(i, j int) bool {
    return h[i].sum < h[j].sum
}

func (h minPairHeap) Swap(i, j int) {
    h[i], h[j] = h[j], h[i]
}

func (h *minPairHeap) Push(x any) {
    *h = append(*h, x.(pair))
}

func (h *minPairHeap) Pop() any {
    old := *h
    n := len(old)
    x := old[n-1]
    *h = old[:n-1]
    return x
}
```
