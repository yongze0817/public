import pandas as pd
import os

folder_path = 'post_data'

all_files = os.listdir(folder_path)

csv_files = [file for file in all_files if file.endswith('.csv')]

for csv_file in csv_files:
    csv_file = os.path.join(folder_path, csv_file)

    xlsx_file = 'faculty_linkedin post.xlsx'

    df = pd.read_csv(csv_file, encoding='utf-8', na_filter=False)
    print(df)

    sheet_name = 'post_data'

    with pd.ExcelWriter(xlsx_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=writer.sheets[sheet_name].max_row, header=False)