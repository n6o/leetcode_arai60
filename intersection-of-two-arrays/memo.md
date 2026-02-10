## 問題

[Intersection of Two Arrays - LeetCode](https://leetcode.com/problems/intersection-of-two-arrays/)

- 入力
    - `nums1` / `nums2`: 整数配列
        - 長さは1以上1000以下
        - 値は0以上1000以下
        - 値は重複している可能性がある
- 出力
    - `nums1` と `nums2` の共通部分

## 解法

### 1. 長さが短いほうの配列を基準に map で管理する

`nums1` と `nums2` の共通部分を求める。
長さが短い配列に含まれている要素を基準に長い方をフィルタする。

- Ns: 短い方の配列の長さ
- Nl: 長い方の配列の長さ
- map の作成
    - 時間計算量: O(Ns), O(Nl)
    - 空間計算量: O(Ns), O(Nl)
    - キーだけが欲しいので `map[int]struct{}` とする
        - `struct{}{}` はメモリを使用しないため
- 共通部分のスライスの作成
    - 時間計算量: O(Nl) 
    - 空間計算量: O(Ns)
        - 共通部分の最大の長さは Ns となる
- 実行時間の推定
    - どちらも長さ10^3として推定する
    - map の作成: 10^3
    - 共通部分のスライスの作成: 10^3
    - 全体で 10^3
    - go の処理速度を 10^8/秒とすると
    - 10^3 / 10^8 = 10^-5 -> 0.01ms くらい

## Step1

### 1.

```go
func intersection(nums1 []int, nums2 []int) []int {
    var numsShort, numsLong []int
    if len(nums1) < len(nums2) {
        numsShort = nums1
        numsLong = nums2
    } else {
        numsShort = nums2
        numsLong = nums1
    }

    candidates := toIntSet(numsShort)

    intersection := make(map[int]struct{})
    for _, num := range numsLong {
        if _, found := candidates[num]; found {
            intersection[num] = struct{}{}
        }
    }

    return slices.Collect(maps.Keys(intersection))
}

func toIntSet(nums []int) map[int]struct{} {
    set := make(map[int]struct{}, len(nums))
    for _, num := range nums {
        set[num] = struct{}{}
    }
    return set
}
```

- この場合、結果の並びはランダムになる
    - go の map の使用
    - 必要であれば呼び出し元でソートすればいい
        - `[]int` を返すようにしているのは leetcode の環境由来
    - 共通部分が欲しいなら `map[int]struct{}` を返すようにする

## Step2

```go
func intersection(nums1 []int, nums2 []int) []int {
    if len(nums2) < len(nums1) {
        return intersection(nums2, nums1)
    }

    candidates := toIntSet(nums1)

    intersection := make(map[int]struct{})
    for _, num := range nums2 {
        if _, found := candidates[num]; found {
            intersection[num] = struct{}{}
        }
    }

    return slices.Collect(maps.Keys(intersection))
}

func toIntSet(nums []int) map[int]struct{} {
    set := make(map[int]struct{}, len(nums))
    for _, num := range nums {
        set[num] = struct{}{}
    }
    return set
}
```

- 長さを比較して引数の順序を入れ替えて呼び出す実装を見た
- MEMO: ソートして `slices.Compact` を使うと重複を排除したスライスが得られる

### レビューを依頼する方のPR

- [349. Intersection of Two Arrays by aki235 · Pull Request #13 · aki235/Arai60](https://github.com/aki235/Arai60/pull/13)
    - 色々な方針があった
    - ソートして2分探索は思いつきもしなかった
- [Ask a review for LeetCode 349. Intersection of Two Arrays by yumyum116 · Pull Request #2 · yumyum116/LeetCode_Arai60](https://github.com/yumyum116/LeetCode_Arai60/pull/2)
- [349-Intersection-of-Two-Arrays by kunimomo · Pull Request #7 · kunimomo/leetcode](https://github.com/kunimomo/leetcode/pull/7)
- [349. Intersection of two arrays by dxxsxsxkx · Pull Request #13 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/13)
- [349_intersection_of_two_arrays by Hiroto-Iizuka · Pull Request #13 · Hiroto-Iizuka/coding_practice](https://github.com/Hiroto-Iizuka/coding_practice/pull/13)
- [コメント集](https://docs.google.com/document/d/11HV35ADPo9QxJOpJQ24FcZvtvioli770WWdZZDaLOfg/edit?tab=t.0#heading=h.o0jquy48e6cy)

#### 2ポインタを利用する方法

- `nums1` と `nums2` をソートし、重複を排除する
- それぞれを先頭から走査する
    - 値が同じなら共通要素として採用し、両方のポインタを進める
    - 値が違う場合、小さい方のみ進める
    - どちらかが終端に達したら終了
- 時間計算量
    - sortAndCompact: Ns/Nl のどちらに対しても行う
        - コピー: O(N)
        - ソート: O(N log N)
        - コンパクト: O(N)
    - 走査: O(Ns)
    - 全体で O(Nl log Nl + Ns log Ns)
- 空間計算量
    - ソート&コンパクトな配列
        - O(Nl + Ns)

```go
func intersection(nums1 []int, nums2 []int) []int {
    nums1 := sortAndCompact(nums1)
    nums2 := sortAndCompact(nums2)

    var intersection []int
    var index1, index2 int
    for index1 < len(nums1) && index2 < len(nums2) {
        n1 := nums1[index1]
        n2 := nums2[index2]

        if n1 == n2 {
            intersection = append(intersection, n1)
            index1++
            index2++
            continue
        }

        if n1 < n2 {
            index1++
        } else {
            index2++
        }
    }

    return intersection
}

func sortAndCompact(nums []int) []int {
    clone := slices.Clone(nums)
    slices.Sort(clone)
    return slices.Compact(clone)
}
```

#### 2分探索を利用する方法

- `nums1` (短い方)をソートし、重複を排除する
- 時間計算量
    - コピー: O(Ns)
    - ソート: O(Ns log Ns)
    - コンパクト: O(Ns)
    - 走査: O(Nl)
    - 2分探索: O(lon Ns)
    - 全体で O(Nl log Ns)
- 空間計算量
    - ソート&コンパクトな配列: O(Ns)
    - 使用済み配列: O(Ns)
    - 全体でO(Ns)

```go
func intersection(nums1 []int, nums2 []int) []int {
    if len(nums2) < len(nums1) {
        return intersection(nums2, nums1)
    }

    candidates := slices.Clone(numsShort)
    slices.Sort(candidates)
    candidates = slices.Compact(candidates)

    used := make([]bool, len(candidates))

    var intersection []int
    for _, num := range nums2 {
        index, found := slices.BinarySearch(candidates, num)
        if found && !used[index] {
            intersection = append(intersection, num)
            used[index] = true
        }
    }

    return intersection
}
```

## Step3

```go
func intersection(nums1 []int, nums2 []int) []int {
    if len(nums2) < len(nums1) {
        return intersection(nums2, nums1)
    }

    candidates := toIntSet(nums1)

    intersection := make(map[int]struct{})
    for _, num := range nums2 {
        if _, found := candidates[num]; found {
            intersection[num] = struct{}{}
        }
    }

    return slices.Collect(maps.Keys(intersection))
}

func toIntSet(nums []int) map[int]struct{} {
    set := make(map[int]struct{}, len(nums))
    for _, num := range nums {
        set[num] = struct{}{}
    }
    return set
}
```
