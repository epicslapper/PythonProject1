import pandas as pd
import os

def create_sample_database():
    db_file_csv = "football_ids.csv"
    db_file_excel = "football_ids.xlsx"

    # Only create files if they don't exist
    if not os.path.exists(db_file_csv) or not os.path.exists(db_file_excel):
        data = {
            "FootballID": [12345, 23456, 34567],
            "Name": ["John Doe", "Alice Smith", "Bob Johnson"],
            "Club": ["Ajax", "PSV", "Feyenoord"]
        }

        df = pd.DataFrame(data)

        # Save CSV and Excel
        df.to_csv(db_file_csv, index=False)
        df.to_excel(db_file_excel, index=False)

        print("✅ Sample database created!")
    else:
        print("ℹ️ Database already exists.")

if __name__ == "__main__":
    create_sample_database()
