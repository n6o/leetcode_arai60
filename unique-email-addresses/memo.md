## 問題

[Unique Email Addresses - LeetCode](https://leetcode.com/problems/unique-email-addresses/description/)

- 入力
    - `emails`: メールアドレスのリスト
        - 長さは1以上100以下
        - アドレスの長さは1以上100以下
        - `@` はただ一つ持つ
        - local name と domain name は空ではない
        - domain name の接尾辞は `.com`
        - domain name は `.com` の前に最低1文字ある
- 出力
    - メールを受け取るメールアドレスの数
- ルール
    - local name で文字の間に `.` があると、送信先のアドレスでは無視される
    - local name に `+` があると、それ以降は無視される

## 解法

### 1. ルールを適用して送信先アドレスを組み立てる

- 各メールアドレスごとに以下の処理を行う
    - O(n): n はメールアドレスの数。1以上100以下
- メールアドレスを `@` で分離する
- local name にある `+` 以降を除外する
- local name にある `.` は除外する
    - `@` と `+` と `.` は一つのループで処理する
    - 計算量は O(m): m はメールアドレスの長さ。1以上100以下
- 送信先メールアドレスとする
    - メールアドレスとしての妥当性チェックもあるとよりよい
- map で管理する
- map のキーの数を返す
- 時間計算量はO(nm)
    - 今回はn,mは最大100なので10^4
    - 処理速度を 10^8 ステップ/秒とすると
    - 10^4 / 10^8 = 10^-4 : 0.1ms くらいか
- 空間計算量はO(nm)
    - すべてのアドレスが異なり`.`も`+`もないケース
        - 100 * 100 = 10KB
        - map のオーバーヘッドを加味して20KB程度

## Step1

### 1.

- 問題の制約を前提としたコード
    - `@` がない場合はエラーとする
    - メールアドレスの正確な定義は知らない
        - [メールアドレス - Wikipedia](https://ja.wikipedia.org/wiki/%E3%83%A1%E3%83%BC%E3%83%AB%E3%82%A2%E3%83%89%E3%83%AC%E3%82%B9)

```go
func numUniqueEmails(emails []string) int {
    uniqueAddressSet := map[string]struct{}{}
    for _, email := range emails {
        forwarded := buildForwardedAddress(email)
        uniqueAddressSet[forwarded] = struct{}{}
    }
    
    return len(uniqueAddressSet)
}

func buildForwardedAddress(email string) string {
    splitted := strings.Split(email, "@")

    localName := splitted[0]
    forwardedLocalName := make([]byte, 0, len(email))
    for i := range localName {
        if localName[i] == '.' {
            continue
        }
        if localName[i] == '+' {
            break
        }

        forwardedLocalName = append(forwardedLocalName, localName[i])
    }

    return fmt.Sprintf("%s@%s", string(forwardedLocalName), splitted[1])
}
```

## Step2

- 入力文字列の簡易な検証を行う
    - `net/mail` の `ParseAddress` を使う
        - [mail package - net/mail - Go Packages](https://pkg.go.dev/net/mail#ParseAddress)
        - [複雑](https://cs.opensource.google/go/go/+/refs/tags/go1.25.7:src/net/mail/message.go;l=392-474)
            - [local-partとdomain-part](https://cs.opensource.google/go/go/+/refs/tags/go1.25.7:src/net/mail/message.go;l=512-572)
- `strings.Builder` と `strings.Index` を使う
    - [strings package - strings - Go Packages](https://pkg.go.dev/strings#Builder)
    - [strings package - strings - Go Packages](https://pkg.go.dev/strings#example-Index)
        - `IndexByte` でもいい
- 標準ライブラリを使うと可読性は上がる
    - 内部でバッファを使っている
    - 性能要件がシビアな場合は `[]byte` で処理することを選択する
- エラーの場合はスキップする
    - 実務では `error` を返すが、この環境では表現できないため
    - `panic` も基本的には使わないので、そのようにする

```go
func numUniqueEmails(emails []string) int {
    uniqueEmailSet := map[string]struct{}{}

    for _, email := range emails {
        if _, err := mail.ParseAddress(email); err != nil {
            fmt.Printf("invalid email: %s\n", email)
            continue
        }
        
        canonicalized, err := canonicalize(email)
        if err != nil {
            fmt.Printf("canonicalize: %v\n", err)
            continue
        }
        uniqueEmailSet[canonicalized] = struct{}{}
    }

    return len(uniqueEmailSet)
}

func canonicalize(email string) (string, error) {
    atIndex := strings.Index(email, "@")
    if atIndex == -1 {
        return "", fmt.Errorf("@ not found: %s", email)
    }

    localName := email[:atIndex]

    if plusIndex := strings.Index(localName, "+"); plusIndex != -1 {
        localName = localName[:plusIndex]
    }

    localName = strings.ReplaceAll(localName, ".", "")

    var b strings.Builder
    b.WriteString(localName)
    b.WriteString(email[atIndex:])

    return b.String(), nil
}
```

### レビューを依頼する方のPR

- [929_unique_email_addresses by Hiroto-Iizuka · Pull Request #14 · Hiroto-Iizuka/coding_practice](https://github.com/Hiroto-Iizuka/coding_practice/pull/14)
- [929. Unique Email Addresses by TakayaShirai · Pull Request #14 · TakayaShirai/leetcode_practice](https://github.com/TakayaShirai/leetcode_practice/pull/14)
- [929. Unique email address by dxxsxsxkx · Pull Request #14 · dxxsxsxkx/leetcode](https://github.com/dxxsxsxkx/leetcode/pull/14)
    - `canonicalized` というワードが今回の文脈だと適切
- [929. Unique Email Addresses by aki235 · Pull Request #14 · aki235/Arai60](https://github.com/aki235/Arai60/pull/14)
    - `@` が2個以上含まれる可能性があるのか
    - `strings.LastIndex` を使った方が安全か
        - [strings package - strings - Go Packages](https://pkg.go.dev/strings#example-LastIndex)
- [Create 929_Unique_Email_Addresses.md by achotto · Pull Request #4 · achotto/arai60](https://github.com/achotto/arai60/pull/4)


## Step3

```go
func numUniqueEmails(emails []string) int {
    uniqueEmailSet := map[string]struct{}{}

    for _, email := range emails {
        if _, err := mail.ParseAddress(email); err != nil {
            continue
        }
        
        canonicalized, err := canonicalize(email)
        if err != nil {
            continue
        }
        uniqueEmailSet[canonicalized] = struct{}{}
    }

    return len(uniqueEmailSet)
}

func canonicalize(email string) (string, error) {
    atIndex := strings.LastIndex(email, "@")
    if atIndex == -1 {
        return "", fmt.Errorf("@ not found: %s", email)
    }

    localName := email[:atIndex]

    if plusIndex := strings.Index(localName, "+"); plusIndex != -1 {
        localName = localName[:plusIndex]
    }

    localName = strings.ReplaceAll(localName, ".", "")

    var b strings.Builder
    b.WriteString(localName)
    b.WriteString(email[atIndex:])

    return b.String(), nil
}
```
