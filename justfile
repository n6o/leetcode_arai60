template := '## 問題

[example](example.com)

- 入力
- 出力

## 解法

## Step1

## Step2

### レビューを依頼する方のPR

## Step3

## ふりかえり'

new-memo dir_name="memo":
    mkdir -p {{dir_name}}
    echo "{{template}}" > {{dir_name}}/memo.md
    @echo "Created {{dir_name}}/memo.md"

new-memo-py dir_name="memo":
    mkdir -p python/{{dir_name}}
    echo "{{template}}" > python/{{dir_name}}/memo.md
    @echo "Created python/{{dir_name}}/memo.md"
