## 下書き
- この本を読んで得られること
    - データ分析の失敗あるある
- この本を読んで得られないこと
    - データ分析の手法の詳細
    - システムの構成/実装の仕方
- 対象者
    - データ分析の失敗ストーリーを短編小説のように楽しみたい人
    - 社会人になる前に、データ分析の失敗あるあるがどんなものなのかを把握しておきたい学生
    - データ分析の失敗あるあるを知って、自分の分析に活かしたい人




- 技術的な話はあまりない。 読み物として面白い。
    - ただ広く浅い知識があるとより良い。BERT, 傾向スコア, Redshift, Tydyverseといった単語を聞いたときに、どんなものかを知っていると、読みやすいと思う。
-  著者の社会性フィルターが良い意味で外れてて読んでて 物事をオブラートに包まずに記述している点が、この本の価値であると感じた。
    - 「調整役ばかりでものづくりをリードする人物がいない」「そのような理由ではBERTをやめられるわけがなかった。このプロジェクトはY氏による『BERTを使ってなにかできないか』プロジェクトだからである。」「半年後には想定以上の値を示すことができた。しかし一旦ダウンした査定が回復することはなく担当データサイエンティストは退職した。」「効果検証分析の真の目的はすでに決定済みの社内意志の統一化であり、意思決定に寄与することではなかった。」(意訳)
- 私もそんな著者に敬意を表して、この本のレビューでは社会性フィルターを外して書こうと思う。
    - 何か問題があったらコメント欄で教えてください(コメントは公開前に自分にメールが来るようになってます)
- まずははじめにだけでも読むと、この本の雰囲気がわかるのではないかと思う。
-  はじめにでは、ビジネス側を非難するような内容が含まれる的なことを書いてあるが、中身では、分析側の非難もビシバシ書いてあった。
- 失敗談の短編集のようになっていて、合計25個の事例が紹介されている。1事例は8から10ページぐらいで説明されているので、短くテンポよく読むことができるだろう。
- 各事例では冒頭で、登場人物の立場や所属会社がイラストで整理されていて、その点がわかりやすい。
- 失敗の事例だけではなく、コラム では、データサイエンティストの 人事事情なども紹介されていて面白い。
-  社会人としてデータに携わったことのある人だったら「わかる〜」となる事例が多く紹介されていると思う。



- 印象に残った事例
    - CASE9 そんな目的変数で大丈夫か？
    - CASE15 プロダクトアウトでもドメイン知識は大事
    - CASE21 頑張って予測していたのは...
    - CASE10 成功した報告しか聞きたくない ではデータサイエンティストが不遇で読んでてお腹が痛くなる感じがした。
    - コラム データサイエンティストの人事事情
    - コラム 絶対失敗しないデータ分析


## 本編

### はじめに

2023/08/03発売の「データ分析失敗事例集 ―失敗から学び、成功を手にする―」を知り合いのご厚意により頂いたので、読んでみたところ非常に面白かったので、感想をブログにまとめようと思います。

[https://www.kyoritsu-pub.co.jp/book/b10032587.html:embed:cite]

全編通していい意味で社会性フィルターが外れていて、これを出版することは非常な苦労があったと察します。著者に敬意を評して、本ブログでも特に配慮などはせずに感想を書いていこうと思います。(何か問題があったらコメント欄で教えてください。コメントは公開前に自分にメールが来るようになってます。)

### 本書の概要
- 本書ではデータ分析の失敗談を短編小説のように楽しむことができる。
- 技術的な話はあまりないが、一部の専門用語については基本的な理解があると読みやすい。
    - 例えば、BERT, 傾向スコア, Redshift, Tydyverseと聞いて、どういうものでどういう使われ方をするのか知っているとより良い。
- 著者は社会性フィルターを外し、物事をオブラートに包まずに記述している。この点が本書の価値でもあると感じた。
    - 本書の冒頭に「ビジネス側を非難するような内容が含まれる」と書いてある。
    - 全体を通じてビジネス側だけでなく、分析側の問題点も明確に指摘している。
- データ分析の具体的な手法の詳細やシステムの構成・実装の方法については言及されていない。
- 大体十数時間で読める分量である。ただし自分は読むのが遅い方なので、人によっては10時間もかからないかもしれない。

### 読むべき対象者

- データ分析の失敗あるあるを把握しておきたい学生
- 失敗を予め知り、自分の分析に活かしたい人
- 短編小説のような形でデータ分析の失敗談を楽しみたい人


### 本書の内容と特徴

本書は失敗談の短編集で、合計25個の事例が紹介されている。1事例は8から10ページで説明されていて、テンポよく読むことができる。
各事例の冒頭では、登場人物の立場や所属会社がイラストで整理されているため、各事例の背景がわかりやすい。
各事例では内容をオブラートに包まずに、失敗の原因を明確に指摘しているので痛快な文章である。一部を抜粋すると、以下のような内容である。

- 「調整役ばかりでものづくりをリードする人物がいない」
- 「そのような理由ではBERTをやめられるわけがなかった。このプロジェクトはY氏による『BERTを使ってなにかできないか』プロジェクトだからである。」
- 「半年後には想定以上の値を示すことができた。しかし一旦ダウンした査定が回復することはなく担当データサイエンティストは退職した。」
- 「効果検証分析の真の目的はすでに決定済みの社内意志の統一化であり、新たな意思決定に寄与することではなかった。」(意訳)


データ分析の失敗事例だけでなく、データサイエンティストの人事事情などもコラムとして紹介されていて興味深かった。「コラム データサイエンティストの人事事情」は皆様も気になるところではないだろうか？

### 印象に残った事例

以下の事例が特に印象的であった。
- CASE9 そんな目的変数で大丈夫か？
- CASE15 プロダクトアウトでもドメイン知識は大事
- CASE21 頑張って予測していたのは...
- コラム 絶対失敗しないデータ分析
- CASE10 成功した報告しか聞きたくない

上4つに関しては、個人的に学びが多いという点で印象に残った。ネタバレは避けるが「そんなところに分析上の罠が...」といった感想だ。特に「コラム 絶対失敗しないデータ分析」は本書の最終章であるが、今までとは異なり非常に真面目な文章で(いやずっと真面目だったろ)、データ分析にかける思いがアツく書かれている。

最後の一つCASE10に関しては、あまりにもデータサイエンティストが不遇で読んでてお腹が痛くなる感じがした。そういう意味で印象に残った。


### おすすめです
全体として、本書はデータ分析の「失敗談」に焦点を当てた短編集という特異なアプローチで、データ分析の現場で起きる様々な問題をリアルに描き出している。読者がデータ分析の現場で犯しやすい間違いや誤解を理解し、それらを避けるための手がかりを得ることができる点で非常に価値がある。
この本を読むことで、データ分析の現場での課題や困難がどのようなものかを理解し、それを避けるための知識を身につけることができるだろう。それにより、より高品質な分析結果を生み出すことができるようになるに違いない。


[https://www.kyoritsu-pub.co.jp/book/b10032587.html:embed:cite]