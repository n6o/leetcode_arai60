## 問題

[Number of Islands - LeetCode](https://leetcode.com/problems/number-of-islands/)

- 入力
    - `grid`
        - 高さ `m` と幅 `n` は1以上300以下
        - `grid[i][j]` の値は `0`(水) か `1`(陸)
- 出力
    - 島の数

## 解法

### BFSで島を数える

- grid のコピーを用意する
    - 時間計算量、空間計算量ともにO(mn)
    - 今回は最大で 9*10^4 なので問題ない
    - go は 10^8 step/秒で推定
        - 9*10^-4秒 -> 0.9ms 程度と推定
- grid[0][0]から走査する: 時間計算量O(mn)
    - 土地を見つけたら、隣接する土地を探索する
    - 探索済みの土地はマークする
        - 水にする
    - 隣接する土地がなくなったら count を増やす
- gridをすべて操作したら count を返す

### DFSで島を数える

- DFSでもやってみる

## Step1

### 1.

```go
func numIslands(grid [][]byte) int {
    copyOfGrid := copyGrid(grid)

    var count int
    for i := range copyOfGrid {
        for j := range copyOfGrid[i] {
            if copyOfGrid[i][j] == '1' {
                explore(i, j, copyOfGrid)
                count++
            }
        }
    }
    return count
}

func copyGrid(g [][]byte) [][]byte {
    grid := make([][]byte, len(g))
    for i := range grid {
        grid[i] = slices.Clone(g[i])
    }

    return grid
}

func explore(i, j int, grid [][]byte) {
    queue := []Point{{i: i, j: j}}
    grid[i][j] = '0'

    dx := []int{-1, 0, 1, 0}
    dy := []int{0, 1, 0, -1}

    for len(queue) > 0 {
        p := queue[0]
        queue = queue[1:]

        for k := range dx {
            x := p.i + dx[k]
            y := p.j + dy[k]

            if x < 0 || y < 0 {
                continue
            }
            if x >= len(grid) || y >= len(grid[0]) {
                continue
            }

            if grid[x][y] == '1' {
                grid[x][y] = '0'
                queue = append(queue, Point{i: x, j: y})
            }
        }
    }
}

type Point struct {
    i int
    j int
}
```

- `Point` は `x`, `y` を使いたくなる
- ただインデックスは `i`, `j`
- どう整理すると読みやすいのだろう
    - `Point` で整理してみる?
- `explore` は `exploreIsland` のほうが何してるかわかりやすい気がした

### 2.

```go
func numIslands(grid [][]byte) int {
    copyOfGrid := copyGrid(grid)

    var count int
    for i := range copyOfGrid {
        for j := range copyOfGrid[i] {
            if copyOfGrid[i][j] == '1' {
                explore(i, j, copyOfGrid)
                count++
            }
        }
    }
    return count
}

func copyGrid(g [][]byte) [][]byte {
    grid := make([][]byte, len(g))
    for i := range grid {
        grid[i] = slices.Clone(g[i])
    }

    return grid
}

func explore(i, j int, grid [][]byte) {
    if i < 0 || j < 0 {
        return
    }
    if i >= len(grid) || j >= len(grid[0]) {
        return
    }
    if grid[i][j] != '1' {
        return
    }

    grid[i][j] = '0'

    explore(i - 1, j, grid)
    explore(i, j + 1, grid)
    explore(i + 1, j, grid)
    explore(i, j - 1, grid)
}
```

## Step2

```go
const (
    WATER = '0'
    LAND = '1'
)

func numIslands(grid [][]byte) int {
    copyOfGrid := copyGrid(grid)

    var count int
    for i := range copyOfGrid {
        for j := range copyOfGrid[i] {
            if copyOfGrid[i][j] == LAND {
                exploreIsland(i, j, copyOfGrid)
                count++
            }
        }
    }
    return count
}

func copyGrid(g [][]byte) [][]byte {
    grid := make([][]byte, len(g))
    for i := range grid {
        grid[i] = slices.Clone(g[i])
    }

    return grid
}

func exploreIsland(i, j int, grid [][]byte) {
    queue := []Point{{i: i, j: j}}
    grid[i][j] = WATER

    offsets := []Point{
        // up
        {i: -1, j: 0},
        // right
        {i: 0, j: 1},
        // down
        {i: 1, j: 0},
        // left
        {i: 0, j: -1},
    }

    for len(queue) > 0 {
        p := queue[0]
        queue = queue[1:]

        for _, offset := range offsets {
            adjacent := Point{
                i: p.i + offset.i,
                j: p.j + offset.j,
            }

            if adjacent.i < 0 || adjacent.j < 0 {
                continue
            }
            if adjacent.i >= len(grid) || adjacent.j >= len(grid[0]) {
                continue
            }
            if grid[adjacent.i][adjacent.j] == WATER {
                continue
            }

            // 同じ陸を数えないようにする
            grid[adjacent.i][adjacent.j] = WATER
            queue = append(queue, adjacent)
        }
    }
}

type Point struct {
    i int
    j int
}
```

- 「訪問済み」を管理する `visited [][]bool` を使うと意味がわかりやすいと思った
    - それだと2つのグリッドを管理しないといけない
    - 構造体のメソッドにするか、クロージャーでやるか

### レビューを依頼する方のPR

- [LeetCode 200. Number of Islands by huyfififi · Pull Request #40 · huyfififi/coding-challenges](https://github.com/huyfififi/coding-challenges/pull/40)
    - `visited` を使用されていた
- [200. Number of Islands by TakayaShirai · Pull Request #17 · TakayaShirai/leetcode_practice](https://github.com/TakayaShirai/leetcode_practice/pull/17)
    - `directions` という名前の配列を使われていた
    - `traverseIsland` という名前
    - Union-Find
        - 2次元を管理するので少し注意が必要そう
- [200. Number of islands by dxxsxsxkx · Pull Request #17 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/17)
    - こちらでもUnion-Find
- [200_number_of_islands by Hiroto-Iizuka · Pull Request #17 · Hiroto-Iizuka/coding_practice](https://github.com/Hiroto-Iizuka/coding_practice/pull/17)
    - `x と y は、言語やライブラリによって縦横への対応がバラバラなので、row, col とか、取り違えのないインデックスを使うのが良さそうです。`
        - 思い込みを持っていた。
    - `二次元座標に (i, j) を使うのは違和感を感じます`
        - row, colomn のほうがすぐ意味がわかる
    - 再帰の呼び出し回数は考えてなかった
        - go のスタックは2KBから1GBまで(64bit版)
        - 9万回呼び出してもスタックオーバーフローは起きなそう
- [200. Number of Islands by aki235 · Pull Request #17 · aki235/Arai60](https://github.com/aki235/Arai60/pull/17)

### UnionFind版

- 何も見ずに書くにはまだまだ練習が必要

```go
const (
    WATER = '0'
    LAND = '1'
)

func numIslands(grid [][]byte) int {
    uf := NewUnionFind(grid)

    m := len(grid)
    n := len(grid[0])
    for r := range grid {
        for c := range grid[r] {
            if grid[r][c] != LAND {
                continue
            }

            index := r*n + c
            // right
            if c + 1 < n  && grid[r][c + 1] == LAND {
                uf.Union(index, index + 1)
            }
            // bottom
            if r + 1 < m && grid[r + 1][c] == LAND {
                uf.Union(index, index + n)
            }
        }
    }

    return uf.Count()
}

type UnionFind struct {
    parents []int
    ranks []int
    count int
}

func NewUnionFind(grid [][]byte) *UnionFind {
    m := len(grid)
    n := len(grid[0])

    parents := make([]int, m*n)
    ranks := make([]int, len(parents))
    var count int
    for r := range grid {
        for c := range grid[r] {
            if grid[r][c] == LAND {
                index := r*n + c

                parents[index] = index
                ranks[index] = 1
                count++
            }
        }
    }

    return &UnionFind{
        parents: parents,
        ranks: ranks,
        count: count,
    }
}

func (uf *UnionFind) Find(x int) int {
    if uf.parents[x] != x {
        uf.parents[x] = uf.Find(uf.parents[x])
    }
    return uf.parents[x]
}

func (uf *UnionFind) Union(x, y int) {
    rootX := uf.Find(x)
    rootY := uf.Find(y)

    if rootX != rootY {
        if uf.ranks[rootX] == uf.ranks[rootY] {
            uf.parents[rootX] = rootY
            uf.ranks[rootY]++
        } else if uf.ranks[rootX] < uf.ranks[rootY] {
            uf.parents[rootX] = rootY
        } else {
            uf.parents[rootY] = rootX
        }
        uf.count--
    }
}

func (uf *UnionFind) Count() int {
    return uf.count
}
```

## Step3

```go
const (
    WATER = '0'
    LAND = '1'
)

func numIslands(grid [][]byte) int {
    copyOfGrid := copyGrid(grid)

    var count int
    for i := range copyOfGrid {
        for j := range copyOfGrid[i] {
            if copyOfGrid[i][j] == LAND {
                exploreIsland(i, j, copyOfGrid)
                count++
            }
        }
    }
    return count
}

func copyGrid(g [][]byte) [][]byte {
    grid := make([][]byte, len(g))
    for i := range grid {
        grid[i] = slices.Clone(g[i])
    }

    return grid
}

func exploreIsland(i, j int, grid [][]byte) {
    queue := []Point{{i: i, j: j}}
    grid[i][j] = WATER

    offsets := []Point{
        // up
        {i: -1, j: 0},
        // right
        {i: 0, j: 1},
        // down
        {i: 1, j: 0},
        // left
        {i: 0, j: -1},
    }

    for len(queue) > 0 {
        p := queue[0]
        queue = queue[1:]

        for _, offset := range offsets {
            adjacent := Point{
                i: p.i + offset.i,
                j: p.j + offset.j,
            }

            if adjacent.i < 0 || adjacent.j < 0 {
                continue
            }
            if adjacent.i >= len(grid) || adjacent.j >= len(grid[0]) {
                continue
            }
            if grid[adjacent.i][adjacent.j] == WATER {
                continue
            }

            // 同じ陸を数えないようにする
            grid[adjacent.i][adjacent.j] = WATER
            queue = append(queue, adjacent)
        }
    }
}

type Point struct {
    i int
    j int
}
```
