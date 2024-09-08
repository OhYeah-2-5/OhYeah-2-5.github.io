import os
import csv
import sys
from datetime import datetime
import requests
from io import StringIO
import logging

def main():
    # ログの設定
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    output_folder = os.path.join(root_dir, 'holiday_data')
    os.makedirs(output_folder, exist_ok=True)
    log_file = os.path.join(output_folder, 'holiday_script.log')
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(message)s')

    input_url = 'https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv'
    output_file_name = 'filtered_holidays.csv'

    try:
        response = requests.get(input_url)
        response.raise_for_status()
        content = response.content.decode('shift-jis')
    except requests.RequestException as e:
        logging.error(f"CSVファイルのダウンロードに失敗しました: {str(e)}")
        sys.exit(1)

    csv_reader = csv.reader(StringIO(content))
    rows = list(csv_reader)
    current_year = datetime.now().year

    # ヘッダー行を保持し、前年以降のデータを抽出
    filtered_rows = [rows[0]] + [row for row in rows[1:] if row and datetime.strptime(row[0].strip(), '%Y/%m/%d').year >= current_year - 1]

    filtered_content = '\n'.join([','.join(row) for row in filtered_rows])

    output_path = os.path.join(output_folder, output_file_name)
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(filtered_content)
        logging.info(f"フィルタリングされたファイルが保存されました: {os.path.realpath(output_path)}")
    except IOError as e:
        logging.error(f"ファイルの書き込みに失敗しました: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
