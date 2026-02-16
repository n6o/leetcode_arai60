## 問題

[Max Area of Island - LeetCode](https://leetcode.com/problems/max-area-of-island/description/)

- 入力
    - `grid`: バイナリ行列
        - `1` は陸を表す
        - 高さ `m`
            - 1以上50以下
        - 幅: `n`
            - 1以上50以下
- 出力
    - 島の最大面積

## 解法

### 1. 幅優先探索で島を探索し、面積の最大値を求める

- 以前やった島を数えるのとだいたい同じ
- grid をコピーする
- 島を探索し、面積を出す
- 面積の最大値を更新する
- grid の探索が終わったら面積の最大値を返す
    - 島がない場合は `0` を返す
- 時間計算量はO(mn)
- 空間計算量はO(mn)
    - grid のコピー

## Step1

### 1.

```go
const (
    WATER = 0
    LAND = 1
)

func maxAreaOfIsland(grid [][]int) int {
    // コピーした grid を扱う
    grid = copyGrid(grid)

    var maxArea int
    for row := range grid {
        for column := range grid[row] {
            // 陸でなければスキップ
            if grid[row][column] != LAND {
                continue
            }

            startCell := Cell{
                row: row,
                column: column,
            }
            area := exploreIsland(startCell, grid)
            maxArea = max(maxArea, area)
        }
    }

    return maxArea
}

func copyGrid(grid [][]int) [][]int {
    g := make([][]int, len(grid))
    for row := range g {
        g[row] = slices.Clone(grid[row])
    }

    return g
}

type Cell struct {
    row int
    column int
}

// 島を探索する
// 探索した島の大きさを返す
func exploreIsland(startCell Cell, grid [][]int) int {
    rowSize := len(grid)
    columnSize := len(grid[0])

    offsets := []Cell{
        // up
        {row: -1, column: 0},
        // right
        {row: 0, column: 1},
        // down
        {row: 1, column: 0},
        // left
        {row: 0, column: -1},
    }

    // 最初の土地を登録する
    // 重複して訪問しないよう水にする
    area := 1
    grid[startCell.row][startCell.column] = WATER

    queue := []Cell{startCell}
    for len(queue) > 0 {
        cell := queue[0]
        queue = queue[1:]

        for _, offset := range offsets {
            // 隣接セル
            adjacent := Cell{
                row: cell.row + offset.row,
                column: cell.column + offset.column,
            }

            // 行が範囲外
            if adjacent.row < 0 || rowSize <= adjacent.row {
                continue
            }
            // 列が範囲外
            if adjacent.column < 0 || columnSize <= adjacent.column {
                continue
            }
            // 陸でない
            if grid[adjacent.row][adjacent.column] != LAND {
                continue
            }

            // エリアとgridを更新する
            area++
            grid[adjacent.row][adjacent.column] = WATER
            
            queue = append(queue, adjacent)
        }
    }

    return area
}
```

## Step2

- グリッド内か判定する処理を関数にまとめる
- スタックを使うようにするとメモリ効率が多少改善される

```go
const (
    WATER = 0
    LAND = 1
)

func maxAreaOfIsland(grid [][]int) int {
    grid = copyGrid(grid)

    var maxArea int
    for row := range grid {
        for column := range grid[row] {
            if grid[row][column] != LAND {
                continue
            }

            startCell := Cell{
                row: row,
                column: column,
            }
            area := exploreIsland(startCell, grid)
            maxArea = max(maxArea, area)
        }
    }

    return maxArea
}

func copyGrid(grid [][]int) [][]int {
    g := make([][]int, len(grid))
    for row := range g {
        g[row] = slices.Clone(grid[row])
    }

    return g
}

type Cell struct {
    row int
    column int
}

func exploreIsland(startCell Cell, grid [][]int) int {
    rowSize := len(grid)
    columnSize := len(grid[0])
    isValidLand := func(row, column int) bool {
        if row < 0 || rowSize <= row {
            return false
        }
        if column < 0 || columnSize <= column {
            return false
        }

        return grid[row][column] == LAND
    }

    offsets := []Cell{
        {row: -1, column: 0},
        {row: 0, column: 1},
        {row: 1, column: 0},
        {row: 0, column: -1},
    }

    area := 1
    grid[startCell.row][startCell.column] = WATER

    nextLands := []Cell{startCell}
    for len(nextLands) > 0 {
        land := nextLands[len(nextLands) - 1]
        nextLands = nextLands[:len(nextLands) - 1]

        for _, offset := range offsets {
            adjacent := Cell{
                row: land.row + offset.row,
                column: land.column + offset.column,
            }

            if !isValidLand(adjacent.row, adjacent.column) {
                continue
            }

            area++
            grid[adjacent.row][adjacent.column] = WATER
            
            nextLands = append(nextLands, adjacent)
        }
    }

    return area
}
```

### レビューを依頼する方のPR

- [695. Max Area of Island by mamo3gr · Pull Request #18 · mamo3gr/arai60](https://github.com/mamo3gr/arai60/pull/18)
    - DFS
- [695. Max Area of Island by dxxsxsxkx · Pull Request #18 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/18)
    - DFS
- [695. Max Area of Island by TakayaShirai · Pull Request #18 · TakayaShirai/leetcode_practice](https://github.com/TakayaShirai/leetcode_practice/pull/18)
    - BFS
- [695_max_area_of_island by Hiroto-Iizuka · Pull Request #18 · Hiroto-Iizuka/coding_practice](https://github.com/Hiroto-Iizuka/coding_practice/pull/18)
    - `frontier` という言葉がよく使われている
    - 再帰版
- [695.max area of island by PafsCocotte · Pull Request #2 · PafsCocotte/leetcode](https://github.com/PafsCocotte/leetcode/pull/2)

## Step3

- 10分ギリギリ

```go
const (
    WATER = 0
    LAND = 1
)

func maxAreaOfIsland(grid [][]int) int {
    grid = copyGrid(grid)

    var maxArea int
    for row := range grid {
        for column := range grid[row] {
            if grid[row][column] != LAND {
                continue
            }

            area := exploreIsland(Cell{row: row, column: column}, grid)
            maxArea = max(area, maxArea)
        }
    }

    return maxArea
}

func copyGrid(grid [][]int) [][]int {
    g := make([][]int, len(grid))
    for row := range grid {
        g[row] = slices.Clone(grid[row])
    }
    return g
}

type Cell struct {
    row int
    column int
}

func exploreIsland(start Cell, grid [][]int) int {
    rowSize := len(grid)
    columnSize := len(grid[0])
    isValidLand := func(cell Cell) bool {
        if cell.row < 0 || rowSize <= cell.row {
            return false
        }
        if cell.column < 0 || columnSize <= cell.column {
            return false
        }

        return grid[cell.row][cell.column] == LAND 
    }
    offsets := []Cell{
        {row: -1, column: 0},
        {row: 0, column: 1},
        {row: 1, column: 0},
        {row: 0, column: -1},
    }

    area := 1
    grid[start.row][start.column] = WATER

    nextLands := []Cell{start}
    for len(nextLands) > 0 {
        land := nextLands[len(nextLands) - 1]
        nextLands = nextLands[:len(nextLands) - 1]

        for _, offset := range offsets {
            adjacent := Cell{
                row: land.row + offset.row,
                column: land.column + offset.column,
            }

            if !isValidLand(adjacent) {
                continue
            }

            area++
            grid[adjacent.row][adjacent.column] = WATER

            nextLands = append(nextLands, adjacent)
        }
    }

    return area
}
```
