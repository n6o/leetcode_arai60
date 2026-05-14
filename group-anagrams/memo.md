## 問題

[Group Anagrams - LeetCode](https://leetcode.com/problems/group-anagrams/description/)

- 入力
    - `strs`: 文字列配列
        - 長さは1以上10^4以下
        - 要素の文字列の長さは0以上100以下
        - 要素の文字列は英語小文字
- 出力
    - `strs` の要素をアナグラムのグループごとにまとめた配列
        - 順序は任意

## 解法

### 文字列要素をソートして map のキーとし、スライスに追加していく

- 時間計算量
    - ソートの時間計算量は O(N log N): N は文字列要素の長さで最大値10^2
    - これを各要素ごとに行う O(M): M は文字列要素の数で最大10^4
    - ざっくり O(MN log N)
- 空間計算量
    - 文字列のコピーが必要: O(MN)
    - map のキーでO(M)、値でO(MN)
    - ざっくりO(MN)
    - 最大で10^4*10^2 = 1MB程度
    - map でざっくり2倍の2MBくらい

### 文字列の登場回数を map のキーとし、スライスに追加していく

- 英語小文字という問題設定上 `byte` として処理する
    - `rune` を使う必要がある場合は使えない
    - ソートのほうが汎用的
- 時間計算量
    - 各文字列について各文字ごとにカウント
    - O(MN)
- 空間計算量
    - 文字要素の長さは最大100だから各文字の登場回数は `byte` に収まる
    - 長さ26の固定長配列を最大10^4個用意する
        - 260KB
        - go の map はざっくり2倍で520KB
        - 大丈夫そう

## Step1

### ソート版

```go
func groupAnagrams(strs []string) [][]string {
    groups := make(map[string][]string, len(strs))

    for _, str := range strs {
        strBytes := []byte(str)
        slices.Sort(strBytes)
        groups[string(strBytes)] = append(groups[string(strBytes)], str)
    }

    anagramGroups := make([][]string, 0, len(groups))
    for _, anagrams := range groups {
        anagramGroups = append(anagramGroups, anagrams)
    }
    
    return anagramGroups
}
```

### 配列版

```go
func groupAnagrams(strs []string) [][]string {
    groups := make(map[[26]byte][]string, len(strs))

    for _, str := range strs {
        var counts [26]byte
        for i := 0; i < len(str); i++ {
            counts[str[i]-'a']++
        }

        groups[counts] = append(groups[counts], str)
    }

    anagramGroups := make([][]string, len(groups))
    i := 0
    for _, anagrams := range groups {
        anagramGroups[i] = anagrams
        i++
    }
    
    return anagramGroups
}
```

## Step2

### ソート版

```go
func groupAnagrams(strs []string) [][]string {
    keyToAnagramGroup := make(map[string][]string, len(strs))

    for _, str := range strs {
        key := generateKey(str)
        keyToAnagramGroup[key] = append(keyToAnagramGroup[key], str)
    }

    return slices.Collect(maps.Values(keyToAnagramGroup))
}

func generateKey(s string) string {
    sBytes := []byte(s)
    slices.Sort(sBytes)
    return string(sBytes)
}
```

### 配列版

```go
func groupAnagrams(strs []string) [][]string {
    keyToAnagramGroup := make(map[[26]byte][]string, len(strs))

    for _, str := range strs {
        key := generateKey(str)
        keyToAnagramGroup[key] = append(keyToAnagramGroup[key], str)
    }

    return slices.Collect(maps.Values(keyToAnagramGroup))
}

func generateKey(s string) [26]byte {
    var counts [26]byte
    for _, b := range []byte(s) {
        counts[b-'a']++
    }

    return counts
}
```

- [slices package - slices - Go Packages](https://pkg.go.dev/slices#Collect)
- [maps package - maps - Go Packages](https://pkg.go.dev/maps#Values)
- 英語小文字を前提としているコード

### レビューを依頼する方のPR

- [49. Group Anagrams by mamo3gr · Pull Request #12 · mamo3gr/arai60](https://github.com/mamo3gr/arai60/pull/12)
    - 単語の数を `N` 、単語の長さを `W` とおくとわかりやすい
- [49_group_anagrams by Hiroto-Iizuka · Pull Request #12 · Hiroto-Iizuka/coding_practice](https://github.com/Hiroto-Iizuka/coding_practice/pull/12)
- [49. Group Anagrams by TakayaShirai · Pull Request #12 · TakayaShirai/leetcode_practice](https://github.com/TakayaShirai/leetcode_practice/pull/12)
    - Dart
- [49. Group Anagram by dxxsxsxkx · Pull Request #12 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/12)
    - ハッシュを使われていた
- [49. Group Anagrams by aki235 · Pull Request #12 · aki235/Arai60](https://github.com/aki235/Arai60/pull/12)

## Step3

```go
func groupAnagrams(strs []string) [][]string {
    keyToAnagramGroup := make(map[string][]string, len(strs))

    for _, s := range strs {
        key := generateKey(s)
        keyToAnagramGroup[key] = append(keyToAnagramGroup[key], s)
    }

    return slices.Collect(maps.Values(keyToAnagramGroup))
}

func generateKey(s string) string {
    sBytes := []byte(s)
    slices.Sort(sBytes)
    return string(sBytes)
}
```
