## 問題

[Top K Frequent Elements - LeetCode](https://leetcode.com/problems/top-k-frequent-elements/description/)

- 入力
    - `nums`: 整数配列
        - 長さは1以上10^5以下
        - 値は-10^4以上10^4以下
    - `k`: 整数
- 出力
    - 登場回数が多い上位 `k` 個の要素を返す
        - 順番は任意

## 解法

### ソートを使う

- `nums` を走査し、値と登場回数の map を作る
    - O(n)
- 値と登場回数の構造体を定義し、map からリストを作る
    - O(u): uはユニークな値の種類
- 登場回数の昇順でソートし、末尾のk個を返す
    - O(u log u)
- 全体で O(n + u log u) <= O(n + n log n)

### 最小ヒープを使う

- ソートの代わりにヒープを使うのが違い？
    - 優先度付きキュー

## Step1

### ソート版

```go
func topKFrequent(nums []int, k int) []int {
    counts := map[int]int{}
    for _, n := range nums {
        counts[n]++
    }

    counters := make([]counter, 0, len(counts))
    for n, c := range counts {
        counters = append(counters, counter{
            num: n,
            count: c,
        })
    }

    slices.SortFunc(counters, func(a, b counters) int {
        return a.count - b.count
    })

    counters = counters[len(counters) - k:]
    result := make([]int, k)
    for i := range counters {
        result[i] = counters[i].num
    }

    return result
}

type counter struct {
    num int
    count int
}
```

- 構造体を定義しなくても固定長配列でも可能
    - ただ、意味が異なる値が並ぶ形になるので、構造体の方が意味を取りやすいと思う
- 値 to 回数の map から 回数 to 値のリストのmap を作って、登場回数のスライスを作る
    - そのスライスをソートして、登場回数の多い順に k 個の値を取り出す、という方法もある
    - ちょっと作業が多い気がした
- バケットソートという方法で解いた人もいた
    - 時間計算量はO(n)、空間計算量もO(n)

### ヒープ版

```go
import "container/heap"

func topKFrequent(nums []int, k int) []int {
    counts := map[int]int{}
    for _, n := range nums {
        counts[n]++
    }

    topK := &PriorityQueue{}
    heap.Init(topK)

    for n, c := range counts {
        heap.Push(topK, counter{
            num: n,
            count: c,
        })
        if topK.Len() > k {
            heap.Pop(topK)
        }
    }

    result := make([]int, 0, k)
    for _, counter := range *topK {
        result = append(result, counter.num)
    }

    return result
}

type counter struct {
    num int
    count int
}

type PriorityQueue []counter

func (pq PriorityQueue) Len() int {
    return len(pq)
}

func (pq PriorityQueue) Less(i, j int) bool {
    return pq[i].count < pq[j].count
}

func (pq PriorityQueue) Swap(i, j int) {
    pq[i], pq[j] = pq[j], pq[i]
}

func (pq *PriorityQueue) Push(x any) {
    *pq = append(*pq, x.(counter))
}

func (pq *PriorityQueue) Pop() any {
    old := *pq
    n := len(old)
    x := old[n-1]
    *pq = old[:n-1]
    return x
}
```

- プライオリティキューから取り出す時、順序を気にするなら `Pop` を使うといい
- 配列の実体を指す `*topK` を使うのは、認知負荷を上げる気がする

### レビューを依頼する人のPRを見る

- [347. Top K Frequent Elements by mamo3gr · Pull Request #9 · mamo3gr/arai60](https://github.com/mamo3gr/arai60/pull/9)
    - [実際の仕事の時を想像する](https://github.com/potrue/leetcode/pull/9#discussion_r2083755650)のはまだ徹底できていない
- [347_top_k_frequent_elements by Hiroto-Iizuka · Pull Request #9 · Hiroto-Iizuka/coding_practice](https://github.com/Hiroto-Iizuka/coding_practice/pull/9)
- [347. Top k frequent elements by dxxsxsxkx · Pull Request #9 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/9)
- [347. Top K Frequent Elements by aki235 · Pull Request #9 · aki235/Arai60](https://github.com/aki235/Arai60/pull/9)
- [347. Top K Frequent Elements by TrsmYsk · Pull Request #11 · TrsmYsk/leetcode](https://github.com/TrsmYsk/leetcode/pull/11)
    - LRU / LinkedHashMap 
    - 平衡木も一度 go で実装して見る、かも

## Step2

- ヒープ版を書く

```go
import "container/heap"

func topKFrequent(nums []int, k int) []int {
    counts := map[int]int{}
    for _, n := range nums {
        counts[n]++
    }

    topK := &PriorityQueue{}
    heap.Init(topK)

    for value, count := range counts {
        heap.Push(topK, counter{
            value: value,
            count: count,
        })
        if topK.Len() > k {
            heap.Pop(topK)
        }
    }

    result := make([]int, 0, k)
    for topK.Len() > 0 {
        c := topK.Pop().(counter)
        result = append(result, c.value)
    }

    return result
}

type PriorityQueue []counter

type counter struct {
    value int
    count int
}

func (pq PriorityQueue) Len() int {
    return len(pq)
}

func (pq PriorityQueue) Less(i, j int) bool {
    return pq[i].count < pq[j].count
}

func (pq PriorityQueue) Swap (i, j int) {
    pq[i], pq[j] = pq[j], pq[i]
}

func (pq *PriorityQueue) Push(x any) {
    *pq = append(*pq, x.(counter))
}

func (pq *PriorityQueue) Pop() any {
    old := *pq
    n := len(old)
    x := old[n-1]
    *pq = old[:n-1]
    return x
}
```

## Step3

```go
import "container/heap"

func topKFrequent(nums []int, k int) []int {
    counts := map[int]int{}
    for _, n := range nums {
        counts[n]++
    }

    topK := &PriorityQueue{}
    heap.Init(topK)

    for value, count := range counts {
        heap.Push(topK, counter{
            value: value,
            count: count,
        })
        if topK.Len() > k {
            heap.Pop(topK)
        }
    }

    result := make([]int, 0, k)
    for topK.Len() > 0 {
        c := topK.Pop().(counter)
        result = append(result, c.value)
    }

    return result
}

type PriorityQueue []counter

type counter struct {
    value int
    count int
}

func (pq PriorityQueue) Len() int {
    return len(pq)
}

func (pq PriorityQueue) Less(i, j int) bool {
    return pq[i].count < pq[j].count
}

func (pq PriorityQueue) Swap (i, j int) {
    pq[i], pq[j] = pq[j], pq[i]
}

func (pq *PriorityQueue) Push(x any) {
    *pq = append(*pq, x.(counter))
}

func (pq *PriorityQueue) Pop() any {
    old := *pq
    n := len(old)
    x := old[n-1]
    *pq = old[:n-1]
    return x
}
```
