## 問題

[Combination Sum - LeetCode](https://leetcode.com/problems/combination-sum/solutions/429538/general-backtracking-questions-solutions-j8bd/)

- 入力
    - `candidates`: 重複のない整数リスト
        - 長さは1以上30以下
        - 値は2以上40以下
    - `target`: 整数
        - 値は1以上40以下
- 出力
    - 合計が `target` となる組み合わせのリスト

## 解法

### 1. ある数を使う場合と使わない場合とをそれぞれ探索する

- `candidates` の先頭を使う場合/使わない場合を探索する
    - 組み合わせに使う数のサイズと `target` を小さくしていく
    - `target == 0` となったら解としてリストに追加する
- (計算量の見積もりはできなかったので、実装してから考えた)
- 時間計算量
    - `candidates` の長さを N 、最小値を M とする
    - `target` を T とする
    - 再帰の深さは最大 T/M + N
    - 各再帰で2つに分岐する
    - 探索回数は O(2^(T/M + N))
        - 今回は最大T=40, M=2, N=30-> 2^50 -> 10^15 程度
            - 動かなそうだが、実際にはもっと少なくなるはず
- 空間計算量
    - 再帰の深さは最大 T/M + N
    - 各再帰で組み合わせと候補を保つため、O(T/M + N)
    - ざっくり O((T/M + N)^2)
        - 今回は50^2 -> 2*10^3程度
        - そんなに大きくないから大丈夫そう(?)
        - gemini に聞いてみた
            - スタック: 50フレーム * 400バイト -> 20KB
            - リスト: 2500要素 * 36バイト -> 90KB
            - 合計110KB
            - 算出方法は別途学習する

## Step1

### 1.

```py
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        combinations: List[List[int]] = []

        def search_combination(
            combination: List[int], candidates: List[int], target: int
        ) -> None:
            if target == 0:
                combinations.append(combination)
                return

            if target < 0:
                return

            if not candidates:
                return

            # a case using candidates[0]
            search_combination(
                combination + [candidates[0]],
                candidates,
                target - candidates[0],
            )
            # a case not using candidates[0]
            search_combination(
                combination,
                candidates[1:],
                target,
            )

        search_combination([], candidates, target)

        return combinations
```

## Step2

- スライスのコピーを渡すのは無駄
- `candidates` をソートしておけば探索を省ける

```py
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        combinations: List[List[int]] = []
        candidates = sorted(candidates)

        def search_combination(
            combination: List[int], candidate_index: int, target: int
        ) -> None:
            if target == 0:
                combinations.append(combination)
                return

            if candidate_index >= len(candidates):
                return

            if candidates[candidate_index] > target:
                return

            search_combination(
                combination + [candidates[candidate_index]],
                candidate_index,
                target - candidates[candidate_index],
            )
            search_combination(
                combination,
                candidate_index + 1,
                target,
            )

        search_combination([], 0, target)

        return combinations
```

### レビューを依頼する方のPR

- [Combination Sum by Yuto729 · Pull Request #56 · Yuto729/LeetCode_arai60](https://github.com/Yuto729/LeetCode_arai60/pull/56)
    - バックトラック
        - 3つに分類して考えることができる
    - `candidates` を降順にソートすると速くなる
    - generator を使うケース
- [39. Combination Sum by tom4649 · Pull Request #49 · tom4649/Coding](https://github.com/tom4649/Coding/pull/49)
    - 分割数というものがある
    - append/pop して解に追加するときにコピーする
- [39. Combination Sum by dxxsxsxkx · Pull Request #52 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/52)
- [39. Combination Sum by mamo3gr · Pull Request #49 · mamo3gr/arai60](https://github.com/mamo3gr/arai60/pull/49)

## Step3

- 再帰ごとに新しいリストを作るのではなく、同じリストを使い回すようにした

```py
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        combinations: List[List[int]] = []
        candidates = sorted(candidates)

        def search_combination(
            combination: List[int], candidate_index: int, target: int
        ) -> None:
            if target == 0:
                combinations.append(combination[:])
                return

            if candidate_index >= len(candidates):
                return

            if candidates[candidate_index] > target:
                return

            search_combination(
                combination,
                candidate_index + 1,
                target,
            )

            combination.append(candidates[candidate_index])
            search_combination(
                combination,
                candidate_index,
                target - candidates[candidate_index],
            )
            combination.pop()

        search_combination([], 0, target)

        return combinations
```
