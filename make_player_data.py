import csv

#選手idを取得
def get_id(player_data_csv, player_name):
    with open(player_data_csv, encoding='utf8', newline='') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            if row[0] == player_name:
                return row[2]

#都合のいい関数(ゲームidからインデックス番号を取得)
def search(game_id, player_data):
    for i in range(len(player_data)):
        if player_data[i][0] == game_id:
            return i

#選手データを作成
def make_data(input_csv, player_id, output_csv, OUTPUT):
    player_data = list()
    enemy_data = list()
    column_name_data = list()
    output_data = list()
    #該当選手取得
    #BKN時のデータ取得
    with open(input_csv, encoding='utf8', newline="") as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            if column_name_data == []:
                column_name_data = row
            if row[1] == "1610612751" and row[4] == player_id and row[9] != "":
                player_data.append(row)
    #GSW時のデータ取得
    with open(input_csv, encoding='utf8', newline="") as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            if row[1] == "1610612744" and row[4] == player_id and row[9] != "":
                player_data.append(row)
    player_data.reverse()
    
    #該当選手のマッチアップ相手取得
    with open(input_csv, encoding='utf8', newline="") as f:
        game_id_list = [r[0] for r in player_data]
        team_id_list = [r[1] for r in player_data]
        csvreader = csv.reader(f)
        #条件を絞る
        for row in csvreader:
            if row[0] in game_id_list and row[1] not in team_id_list and row[7] == player_data[0][7]:
                enemy_data.append(row)
            else:
                if type(search(row[0], player_data)) is int:
                    if player_data[search(row[0], player_data)][1] != row[1] and row[7] == player_data[0][7]:
                        enemy_data.append(row)
    
    #データ格納
    output_data.append(column_name_data)
    for p_data in player_data:
        output_data.append(p_data)
        for e_data in enemy_data:
            if p_data[0] == e_data[0]:
                output_data.append(e_data)

    if OUTPUT:
        with open(output_csv, encoding="utf8", mode = "w", newline="") as f:
            csvwriter = csv.writer(f)
            csvwriter.writerows(output_data)

def main():
    player_data_csv = "archive/players.csv" #選手データが格納されたcsvファイル名
    player_name = "Kevin Durant" #データを取得したい選手名
    input_csv = 'archive/games_details.csv' #スタッツが記録されたcsvファイル名
    output_csv = f"{player_name}.csv" #取得したデータを出力したいcsvファイル名
    OUTPUT = True #選手データを出力するか否か
    player_id = get_id(player_data_csv, player_name)
    player_data = make_data(input_csv, player_id, output_csv, OUTPUT)

if __name__ == "__main__":
    main()