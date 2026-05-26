import csv
import os

from db_connection import get_session
from services.batch_algoritm.dict_of_all_options_divides import (
    dict_of_all_options_divides
)


def try_the_first():

    with get_session() as db:

        distances = dict_of_all_options_divides(db)

        if not distances:
            print("אין נתונים להיום.")
            return

        # יצירת תיקייה אם לא קיימת
        os.makedirs("csvfiles", exist_ok=True)

        csv_path = os.path.join(
            "csvfiles",
            "all_options_dist_rec_to_discenter_example.csv"
        )

        with open(csv_path, mode="w", newline="", encoding="utf-8-sig") as file:

            writer = csv.writer(file)

            # כותרות
            writer.writerow([
                "distribution_center_id",
                "recipient_id",
                "distance_km"
            ])

            # כתיבת הנתונים
            for item in distances:

                print(
                    f"center_id: {item['distribution_center_id']} "
                    f"-> recipient_id: {item['recipient_id']} "
                    f"| distance: {item['distance_km']:.2f} km"
                )

                writer.writerow([
                    item["distribution_center_id"],
                    item["recipient_id"],
                    item["distance_km"]
                ])

        print(f"\nCSV created successfully: {csv_path}")


if __name__ == "__main__":
    try_the_first()