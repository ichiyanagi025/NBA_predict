import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
import numpy as np

def calculate_and_export_stats(file_path, output_file_path):
    df = pd.read_csv(file_path)
    kevin_durant_id = 201142

    #分類に時間が入らないため代わりに保存
    df['MIN_INT'] = df['MIN'].str.split(':').str[0].astype(float)

    df['MINUTES'] = df['MIN'].str.split(':').str[0].astype(float)
    df['SECONDS'] = df['MIN'].str.split(':').str[1].astype(float)
    df['TOTAL_SECONDS'] = df['MINUTES'] * 60 + df['SECONDS']

    # 試合ごとの合計出場時間を計算
    total_seconds_by_game = df.groupby('GAME_ID')['TOTAL_SECONDS'].sum().reset_index()

    # 各選手の出場時間の割合を計算
    df = df.merge(total_seconds_by_game, on='GAME_ID', suffixes=('', '_TOTAL'))
    df['TIME_RATIO'] = df['TOTAL_SECONDS'] / df['TOTAL_SECONDS_TOTAL']

    # Kevin Durantのスタッツを選択
    kd_stats = df[df['PLAYER_ID'] == kevin_durant_id][['GAME_ID', 'MIN_INT', 'FG_PCT', 'FG3_PCT', 'FT_PCT', 'OREB', 'DREB', 'STL', 'BLK', 'PF', 'PTS']]

    # ポイントに基づいて評価を行う関数
    def grade_points(pts):
        if pts < 15:
            return '0'
        elif pts < 20:
            return '1'
        elif pts < 25:
            return '2'
        elif pts < 30:
            return '3'
        else:
            return '4'

    # 'GRADE'列を追加
    kd_stats['GRADE'] = kd_stats['PTS'].apply(grade_points)

    # 他の選手のスタッツ（出場時間の割合で按分）
    other_players_stats = df[df['PLAYER_ID'] != kevin_durant_id].copy()
    other_players_stats[['OREB', 'DREB', 'STL', 'BLK']] = other_players_stats[['OREB', 'DREB', 'STL', 'BLK']].multiply(other_players_stats['TIME_RATIO'], axis="index")
    other_players_stats_summed = other_players_stats.groupby('GAME_ID')[['OREB', 'DREB', 'STL', 'BLK']].sum().reset_index()

    final_stats = kd_stats.merge(other_players_stats_summed, on='GAME_ID', suffixes=('_KD', '_OTHERS'))
    columns_order = ['GAME_ID', 'PTS', 'GRADE'] + [col for col in final_stats.columns if col not in ['GAME_ID', 'PTS', 'GRADE']]
    final_stats = final_stats[columns_order]
    final_stats.to_csv(output_file_path, index=False)

def XGBClass(file_path):
    df_kd = pd.read_csv(file_path,encoding='utf_8_sig')

    #目的変数の取得
    y = df_kd['GRADE']
    X = df_kd.iloc[:,0:4]
    X_cols = X.columns.to_list()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=False)  #今回は、未来の要素を想定したいためシャッフルしない

    clf_xgb = xgb.XGBClassifier(objective='multi:softprob',
                            eval_metric='mlogloss') # 予測器インスタンス生成

    # ハイパーパラメータ探索
    hyper_param = {'learning_rate':[0.1,0.01],
                'max_depth': [2,3], 
                'min_child_weight':[2,3],
                'reg_lambda':[0,10.0],
                'gamma':[0, 0.25],
                'colsample_bytree':[0.8,1.0]
                }
    gs = GridSearchCV(estimator=clf_xgb, 
                    param_grid = hyper_param, 
                    cv=5, 
                    scoring='accuracy')
    gs.fit(X_train, y_train)

    print("scoring:",    gs.scorer_)
    print("best_score:", gs.best_score_)
    print("best_param:", gs.best_params_)

    # ベストパラメータによる学習
    clf_xgb_best = xgb.XGBClassifier(objective='multi:softprob',
                                    eval_metric='mlogloss')
    clf_xgb_best.fit(X_train, y_train)

    # 性能評価
    pred = clf_xgb_best.predict(X_test)    
    true = y_test
    print(classification_report(np.hstack(true), np.hstack(pred), digits=3))



def main():
    file_path = 'Kevin Durant.csv'
    output_file_path = 'Kevin_Durant_game_stats.csv'
    calculate_and_export_stats(file_path, output_file_path)

    use_stats_path = 'Kevin_Durant_game_stats.csv'
    XGBClass(use_stats_path)

    
if __name__ == "__main__":
    main()