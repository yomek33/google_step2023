# 宿題 1

ほぼ O(1) で動くハッシュテーブルを自分で実装してみよう
[サンプルコード](https://github.com/xharaken/step2/blob/master/hash_table.py)

## hash_table.py

### 実行

```
python3 hash_table.py
Functional tests passed!
0 0.056589
1 0.047186
2 0.036353
3 0.060237
~
97 0.038030
98 0.037891
99 0.037933
Performance tests passed!

```

### calculate_hash 関数

良い関数ではない理由

- 異なる文字列が同じハッシュ値を生成した場合は衝突する可能性がある
  解決策
- 乗算と加算を組み合わせてハッシュ値を計算する
  乗算で 31 をかける
- ハッシュ値がばらつき、パフォーマンスがいいから。（← 内部的には「元の数」を「５ビット左にシフト」して、そこから元の数を引き算する処理として扱われるため、計算が早くなるらしい。理解していないのでまた調べる。）

#　宿題　２
木構造を使えば O(log N)、ハッシュテーブルを使えばほぼ O(1) で検索・追加・削除を実現することができて、これだけ見ればハッシュテーブルのほうが優れているように見える。ところが現実の大規模なデータベースでは、ハッシュテーブルではなく木構造が使われることが多い。その理由を考えよ。

- ハッシュテーブルの場合、データの追加や削除によってテーブルを再構築する必要がある可能性があるが、木構造はポインタを変更すれば良い
- ハッシュテーブルはバケット数に応じてメモリを使用するが、無駄にメモリを消費する可能性がある。木構造ではメモリを動的に確保し解放できる

#　宿題３
全然分からなかった