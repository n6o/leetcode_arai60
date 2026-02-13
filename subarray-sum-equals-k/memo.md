## 問題

[Subarray Sum Equals K - LeetCode](https://leetcode.com/problems/subarray-sum-equals-k/description/)

- 入力
    - `nums`: 整数配列
        - 長さは1以上2*10^4以下
        - 値は-1000以上1000以下
    - `k`: 整数
        - 値は-10^7以上10^7以下
- 出力
    - 合計が `k` となる部分配列の数
        - 部分配列: 空でない連続した配列

## 解法

### 累積和を使う

- `cumsum`: 累積和の配列
    - `cumsum[i]` = `cumsum[i-1]` + `num[i-1]` ( i >= 1, cumsum[0] = 0)
- i = 0 から len(nums) まで
    - j = i + 1 から len(nums) + 1 まで
    - 時間計算量はO(n^2)
        - n = 2*10^4 なので n^2 = 4*10^8
            - go は 10^8ステップ/秒とする
            - TLEとなる可能性が高い
- 他の解法は思いつかなかった


## Step1

```go
func subarraySum(nums []int, k int) int {
    prefixSums := make([]int, len(nums)+1)
    for i := range nums {
        prefixSums[i + 1] = prefixSums[i] + nums[i]
    }

    var count int
    for i := 0; i < len(nums); i++ {
        for j := i + 1; j < len(nums) + 1; j++ {
            if prefixSums[j] - prefixSums[i] == k {
                count++
            }
        }
    }

    return count
}
```

- 通ったが、遅い
- leetcode の解答を見る
- 累積和を作る
- 自分より前に、自分の相方となる累積和が登場していたら、それがペアの個数となる
    - わかるような
    - 以前取り組んだ、和がkとなる問題の累積和バージョンみたいなイメージ
        - 部分配列だから、累積和を使ってやる、みたいな
- 2重ループ版では `i < j` の関係が成り立っているのだから、そこから着想できるようになれるだろうか
- 引き継ぎシミュレーション
    - [コメント集より](https://docs.google.com/document/d/11HV35ADPo9QxJOpJQ24FcZvtvioli770WWdZZDaLOfg/edit?tab=t.0#heading=h.bp0g0ai41eln)
    - **まあ、というわけで、別に私もややこしいものを理解するときに、分からないといって腕組をしているわけではなくて、こういうふうに自明な変形を組み合わせて理解しようとしています。**

## Step2

```go
func subarraySum(nums []int, k int) int {
    prefixSumToCount := map[int]int{
        0: 1,
    }

    var prefixSum, count int
    for _, num := range nums {
        prefixSum += num
        if c, found := prefixSumToCount[prefixSum - k]; found {
            count += c
        }
        prefixSumToCount[prefixSum]++
    }

    return count
}
```

### レビューを依頼する方のPR

- [560. Subarray Sum Equals K by mamo3gr · Pull Request #17 · mamo3gr/arai60](https://github.com/mamo3gr/arai60/pull/17)
    - *二重ループを一重ループにしたいのでそのためにループ間で何の情報を保持したら良いかを考える*
    - i のループで prefixSum を作ることをまず考えられるようにならないと
- [560_subarray_sum_equals_k by Hiroto-Iizuka · Pull Request #16 · Hiroto-Iizuka/coding_practice](https://github.com/Hiroto-Iizuka/coding_practice/pull/16)
- [560. Subarray Sum Equals K by TakayaShirai · Pull Request #16 · TakayaShirai/leetcode_practice](https://github.com/TakayaShirai/leetcode_practice/pull/16)
    - こういった抽象的な概念の具体化、もしくは抽象化から別の具体的なものに結びつけるのが自然にできるようになりたいな。意識する。
    - (問題とは関係ない)最近思うが、「いかにして問題をとくか」という本に書かれていることを意識するのがいい。
    - **抽象的な概念の具体化**
- [560. Subarray sum equals k by dxxsxsxkx · Pull Request #16 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/16)
- [560. Subarray Sum Equals K by aki235 · Pull Request #16 · aki235/Arai60](https://github.com/aki235/Arai60/pull/16)
    - https://github.com/ryosuketc/leetcode_arai60/pull/16#discussion_r2109771699
        - 累積和を標高に例えている
    - https://github.com/plushn/SWE-Arai60/pull/15#discussion_r2060646138
        - 「連想する内容を増やし視野を広げる」ことを目的とした練習


## Step3

```go
func subarraySum(nums []int, k int) int {
    prefixSumToCount := map[int]int{
        0: 1,
    }

    var prefixSum, count int
    for _, num := range nums {
        prefixSum += num
        if c, found := prefixSumToCount[prefixSum - k]; found {
            count += c
        }
        prefixSumToCount[prefixSum]++
    }

    return count
}
```
