## 問題

[First Unique Character in a String - LeetCode](https://leetcode.com/problems/first-unique-character-in-a-string/description/)

- 入力
    - `s`: 文字列
        - 長さは1以上10^5以下
        - 英語の小文字で構成されている
- 出力
    - 1回しか登場しない最初の文字のインデックス

## 解法

### 1. 登場回数と初登場時のインデックスを持つ構造体を定義してmapで管理する

キーを文字、値を登場回数と初登場時のインデックスを持つ構造体とする map を使う
ある文字が map に存在してなければ追加する
存在する場合は登場回数のみインクリメントする
登場回数が1の文字のうち最小のインデックスを返す

- 時間計算量
    - `s` を走査する: O(n), nは`s`の長さ
    - map の検索はO(1)
    - map を走査する: O(m), mは登場する文字の種類, n より小さい
    - よって O(n)
- 空間計算量
    - 登場回数などを管理する map: O(1)
        - 今回の問題設定ではキーはアルファベット小文字のみ26個
        - メモリ使用量は問題にならない

## Step1

### 1.

```go
func firstUniqChar(s string) int {
    characterToCount := map[byte]*Count{}
    for i := range s {
        if count, found := characterToCount[s[i]]; found {
            count.value++
            continue
        }

        characterToCount[s[i]] = &Count{
            value: 1,
            firstIndex: i,
        }
    }

    minIndex := len(s)
    for _, count := range characterToCount {
        if count.value > 1 {
            continue
        }

        if count.firstIndex < minIndex {
            minIndex = count.firstIndex
        }
    }

    if minIndex == len(s) {
        return -1
    }
    
    return minIndex
}

type Count struct {
    value int
    firstIndex int
}
```

## Step2

- leetcode の解答
- シンプルに `s` の文字を数えて map に保存する
    - rune でも対応可能なので、汎用性が高い
- もう一度 `s` を走査する
    - そのときに回数が1であれば、そのときのインデックスが答えとなる
- 走査が終わったら1回しか登場しない文字はなかったということなので -1 を返す
- 時間計算量: O(n)
- 空間計算量: O(1)

```go
func firstUniqChar(s string) int {
    counts := map[byte]int{}

    for i := range s {
        counts[s[i]]++
    }

    for i := range s {
        if counts[s[i]] == 1 {
            return i
        }
    }

    return -1
}
```

### レビューを依頼する方のPR

- [387. First Unique Character in a String by mamo3gr · Pull Request #15 · mamo3gr/arai60](https://github.com/mamo3gr/arai60/pull/15)
- [387_first_unique_character_in_a_string by Hiroto-Iizuka · Pull Request #15 · Hiroto-Iizuka/coding_practice](https://github.com/Hiroto-Iizuka/coding_practice/pull/15)
- [387. First Unique Character in a String by TakayaShirai · Pull Request #15 · TakayaShirai/leetcode_practice](https://github.com/TakayaShirai/leetcode_practice/pull/15)
    - "重複がないことの証明として、「左から読んだときと右から読んだときで、添字が変わらない」ことを使っていた。"
        - こんなやり方もあるのか
- [Create 387.First Unique Character in a String.md by achotto · Pull Request #3 · achotto/arai60](https://github.com/achotto/arai60/pull/3)
- [387. First Unique Character in a String by aki235 · Pull Request #15 · aki235/Arai60](https://github.com/aki235/Arai60/pull/15)
- [コメント集](https://docs.google.com/document/d/11HV35ADPo9QxJOpJQ24FcZvtvioli770WWdZZDaLOfg/edit?tab=t.0#heading=h.hdbcrwo3urck)

## Step3

```go
func firstUniqChar(s string) int {
    counts := map[rune]int{}

    for _, r := range s {
        counts[r]++
    }

    for i, r := range s {
        if counts[r] == 1 {
            return i
        }
    }
    
    return -1
}
```
