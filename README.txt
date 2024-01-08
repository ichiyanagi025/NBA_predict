make_player_data.py
-players.csvとgames_detailsから選手情報を抜き出すもの
使用方法
1.69行目で選手名を選択
2.23~37行目で該当プレイヤーが所属していたチームを新しい順に取得(書き換える部分はteams.csvからteam_idを調べる)
  ※ケビンデュラントは今回のチームでは2チームだったが他の選手では増減

Kevin Durant.csv
-ケビンデュラントのスタッツとマッチアップしたであろう選手のセット
-ゲームごとの詳しい判別は調べないと出来ないが、見分け方としては
GameID 11~:プレシーズンマッチ
       21~:シーズン戦
       41~:プレイオフ
       51~:プレイイントーナメント

predict_now_point.py
-単純な5値分類
calculate_and_export_stats
-データ作成用の関数
  入力:Kevin Durant.csv
  出力:Kevin_Durant_game_stats.csv
    [GAME_ID,PTS,GRADE,MIN_INT,FG_PCT,FG3_PCT,FT_PCT,OREB_KD,DREB_KD,STL_KD,BLK_KD,PF,OREB_OTHERS,DREB_OTHERS,STL_OTHERS,BLK_OTHERS]
    ※othersのスタッツはケビンデュラントのマッチチング相手のスタッツ　複数いる場合は、出場時間で按分
XGBClass
-分類用の関数
-グリットリサーチあり
　{'learning_rate':[0.1,0.01], 'max_depth': [2,3], 'min_child_weight':[2,3], 'reg_lambda':[0,10.0], 'gamma':[0, 0.25], 'colsample_bytree':[0.8,1.0]}
