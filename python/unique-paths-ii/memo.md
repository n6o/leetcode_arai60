## 問題

[Unique Paths II - LeetCode](https://leetcode.com/problems/unique-paths-ii/description/)

- 入力
    - `obstacleGrid`: 障害物が存在する grid
        - grid の縦横の数は1以上100以下
        - 各マスの値は 0 または 1（障害物）。
- 出力
    - 左上から右下までいける経路の総数
        - 2 * 10^9以下

## 解法

### 1. 各マスに至る経路の総数を計算していく

- 1行目: 左から走査したときにx番目に初めて `1` が現れる場合
    - x-1番目のマスまでは各マスの経路の総数は `1`、以降は `0`
- 1列目: 上から走査したときにy番目に初めて `1` が現れる場合
    - y-1番目のマスまでは各マスの経路の総数は `1`、以降は `0`
- それ以外のマス
    - マスの値が `1` の場合は、経路の総数は `0`
    - マスの値が `0` の場合は、一つ上のマスと一つ左のマスのそれぞれの経路の総数の和
- 時間計算量
    - O(m*n)
- 空間計算量
    - O(m*n)
        - 経路の総数を保存する2次元配列を利用する

## Step1

```py
class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        rows = len(obstacleGrid)
        columns = len(obstacleGrid[0])

        pathCountMatrix = [[0] * columns for _ in range(rows)]

        # gridの1行目を確認する
        for column in range(columns):
            # 障害物が現れたら抜ける
            if obstacleGrid[0][column] == 1:
                break
            pathCountMatrix[0][column] = 1

        # gridの1列目を確認する
        for row in range(rows):
            # 障害物が現れたら抜ける
            if obstacleGrid[row][0] == 1:
                break
            pathCountMatrix[row][0] = 1

        for row in range(1, rows):
            for column in range(1, columns):
                if obstacleGrid[row][column] == 1:
                    continue
                pathCountMatrix[row][column] = (
                    pathCountMatrix[row - 1][column] + pathCountMatrix[row][column - 1]
                )

        return pathCountMatrix[rows - 1][columns - 1]
```

## Step2

- `obstacleGrid` が存在しない場合を考慮すべきだった
- スタート地点が障害物の場合も特別に考えてよい
- 1次元のDPの解法が多かった
- インデックスを `r` / `c` にした
    - 書き間違い防止のため
- `pathCounts` でいいか
- 障害物の値を定数で表現する
- 番兵的に行と列を1つ余分に足すと初期化が不要になる
    - インデックスの扱いが多少複雑になる気がした
    - ので採用はしない

```py
class Solution:
    OBSTACLE: Final[int] = 1

    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        if not obstacleGrid or not obstacleGrid[0]:
            return 0

        rows = len(obstacleGrid)
        columns = len(obstacleGrid[0])

        pathCounts = [[0] * columns for _ in range(rows)]

        # gridの1行目を確認する
        for c in range(columns):
            # 障害物が現れたら抜ける
            if obstacleGrid[0][c] == self.OBSTACLE:
                break
            pathCounts[0][c] = 1

        # gridの1列目を確認する
        for r in range(rows):
            # 障害物が現れたら抜ける
            if obstacleGrid[r][0] == self.OBSTACLE:
                break
            pathCounts[r][0] = 1

        for r in range(1, rows):
            for c in range(1, columns):
                if obstacleGrid[r][c] == self.OBSTACLE:
                    continue
                pathCounts[r][c] = (
                    pathCounts[r - 1][c] + pathCounts[r][c - 1]
                )

        return pathCounts[r - 1][c - 1]
```

### レビューを依頼する方のPR

- [63. Unique Paths II by colorbox · Pull Request #47 · colorbox/leetcode](https://github.com/colorbox/leetcode/pull/47)
- [63. Unique Paths II by TakayaShirai · Pull Request #33 · TakayaShirai/leetcode_practice](https://github.com/TakayaShirai/leetcode_practice/pull/33)
- [63. Unique Paths II by 5ky7 · Pull Request #35 · 5ky7/arai60](https://github.com/5ky7/arai60/pull/35)
    - 再帰を使う方法もある
- [63. Unique Paths II by mamo3gr · Pull Request #32 · mamo3gr/arai60](https://github.com/mamo3gr/arai60/pull/32)
    - `@functools.cache` を使っている
    - 例外を投げるデザイン

## Step3

```py
class Solution:
    OBSTACLE: Final[int] = 1

    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        if not obstacleGrid or not obstacleGrid[0]:
            return 0

        rows = len(obstacleGrid)
        columns = len(obstacleGrid[0])

        pathCounts = [[0] * columns for _ in range(rows)]

        for c in range(columns):
            if obstacleGrid[0][c] == self.OBSTACLE:
                break
            pathCounts[0][c] = 1

        for r in range(rows):
            if obstacleGrid[r][0] == self.OBSTACLE:
                break
            pathCounts[r][0] = 1

        for r in range(1, rows):
            for c in range(1, columns):
                if obstacleGrid[r][c] == self.OBSTACLE:
                    continue
                pathCounts[r][c] = pathCounts[r - 1][c] + pathCounts[r][c - 1]

        return pathCounts[rows - 1][columns - 1]
```
