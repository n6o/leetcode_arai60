## 問題

[Two Sum - LeetCode](https://leetcode.com/problems/two-sum/description/)

- 入力
    - `nums`: 整数配列
        - 長さは2以上10^4以下
        - 値は-10^9以上10^9以下
    - `target`: 整数
        - 値は-10^9以上10^9以下
- 出力
    - 和が `target` となる2つの整数
        - 必ず1つだけ解が存在する
        - 同じ数を2回使用してはいけない
- follow-up
    - 時間計算量がO(n^2)より小さなアルゴリズムを思いつくか

## 解法

### 1. 相方を map で管理する

- ある数 `x` があると、それ以降に `target - x` があればそれが答え
- map のキーを `target - x` 、値を `x` のインデックスとする
- map に存在すれば、そのインデックスと現在のインデックスの配列を答えとする
- `nums` の各要素を1回ずつ参照するので、時間計算量は O(n) となる
- 空間計算量は map で使う分。`nums` の最初と最後がペアになる場合が最悪なので O(n)
    - int -> int だから 16バイト * 10^4 でざっくり160KBくらい
        - オーバーヘッドを考慮してざっくり2倍の300KBくらい

### 2. 総当たり

- あるインデックス `i` の値について、それ以降のインデックス `j` の値をチェックしていく
- (n-1)個のの要素に対し (n-2)回計算するので O(n^2)
    - 今回は10^4だから10^8程度になる
    - go だと 10^9 くらいまでなら leetcode 上では動きそう

## Step1

### 1.

```go
func twoSum(nums []int, target int) []int {
    candidates := map[int]int{}

    for i, n := range nums {
        if pairIndex, found := candidates[n]; found {
            return []int{ i, pairIndex }
        }

        candidates[target - n] = i
    }

    // MEMO: 今回の問題設定では解があるのでここには到達しない
    // 解がない場合は戻り値が空リストとなるようにする
    return nil
}
```

- map のキーを `x` にするか `target-x` にするか
- `target-x` にしたが、コード上からは意図が読み取りにくいと思った
- 値 `x` とそのインデックス `i` のマッピングとして宣言した方が、そのまま理解できる
    - 変数名も valueToIndex のように、それが表すものをダイレクトに表現できる

## Step2

```go
func twoSum(nums []int, target int) []int {
    valueToIndex := make(map[int]int, len(nums))

    for i, n := range nums {
        diff := target - n
        if index, found := valueToIndex[diff]; found {
            return []int{ index, i }
        }

        valueToIndex[n] = i
    }

    return nil
}
```

### レビューを依頼する方のPR

- [1. Two Sum by aki235 · Pull Request #11 · aki235/Arai60](https://github.com/aki235/Arai60/pull/11)
    - `complement` (補数) が出てこなかった
    - ソートしてから2ポインタを使って探索する方法もある
- [1. Two Sum by dxxsxsxkx · Pull Request #11 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/11)
    - `numToIndex` がよく使われる。そうかもしれない。わざわざ `value` という言葉を使う理由が特にない。
- [1_two_sum by Hiroto-Iizuka · Pull Request #11 · Hiroto-Iizuka/coding_practice](https://github.com/Hiroto-Iizuka/coding_practice/pull/11)
- [1. Two Sum by mamo3gr · Pull Request #11 · mamo3gr/arai60](https://github.com/mamo3gr/arai60/pull/11)
- [Ask a review for 001 Two Sum by yumyum116 · Pull Request #1 · yumyum116/LeetCode_Arai60](https://github.com/yumyum116/LeetCode_Arai60/pull/1)
    - [「手作業でやろう」](https://github.com/yumyum116/LeetCode_Arai60/pull/1#discussion_r2737069158)
        - まずソートして最初と最後から探すのが自然な発想になると思った
        - 「紙と鉛筆だけでやる方法」

### 2ポインタ版

- `nums` のインデックスを解決できるようにする必要がある
    -> `[2]int` を使う、あるいは構造体を定義する
- 構造体の型名やそれを格納するスライスの変数名に悩む
    - `Item` とかにしがち
    - 今回は `IndexedNum` としてみたが、あまりしっくりきていない

```go
func twoSum(nums []int, target int) []int {
    indexedNums := make([]IndexedNum, len(nums))
    for i, n := range nums {
        indexedNums[i] = IndexedNum{
            value: n,
            originalIndex: i,
        }
    }

    slices.SortFunc(indexedNums, func(a, b IndexedNum) int {
        return a.value - b.value
    })

    smallerIndex := 0
    largerIndex := len(indexedNums) - 1
    for smallerIndex < largerIndex {
        smaller := indexedNums[smallerIndex]
        larger := indexedNums[largerIndex]
        sum := smaller.value + larger.value
        if sum == target {
            return []int{
                smaller.originalIndex,
                larger.originalIndex,
            }
        }

        if sum < target {
            // sum が小さい -> 増やす必要がある -> smaller を増やす方向に進む
            smallerIndex++
            continue
        }

        // sum が大きい -> 減らす必要がある -> larger を減らす方向に進む
        largerIndex--
    }

    return nil
}

type IndexedNum struct {
    value int
    originalIndex int
}
```

## Step3

```go
func twoSum(nums []int, target int) []int {
    numToIndex := make(map[int]int, len(nums))

    for i, n := range nums {
        complement := target - n
        if index, found := numToIndex[complement]; found {
            return []int{ i, index }
        }

        numToIndex[n] = i
    }

    return nil
}
```
