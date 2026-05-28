import csv
import os

from db_connection import get_session
from services.batch_algoritm.options_of_Inlay_filter_by_meals import (
dict_of_valid_divide_options
)


def test_filter():

    with get_session() as db:

        result = dict_of_valid_divide_options(db)

        print("\n========== VALID OPTIONS RESULT ==========\n")

        if not result:
            print("No valid options found")
            return

        os.makedirs("csvfiles", exist_ok=True)

        csv_path = os.path.join("csvfiles", "valid_divide_options2.csv")

        with open(csv_path, mode="w", newline="", encoding="utf-8-sig") as file:

            writer = csv.writer(file)

            writer.writerow([
                "center_id",
                "recipient_id",
                "distance_km",
                "capacity",
                "demand"
            ])

            for opt in result:

                print(
                    f"Center: {opt['center_id']} "
                    f"-> Recipient: {opt['recipient_id']} "
                    f"| Distance: {opt['distance_km']:.2f} km "
                    f"| Capacity: {opt['capacity']} "
                    f"| Demand: {opt['demand']}"
                )

                writer.writerow([
                    opt["center_id"],
                    opt["recipient_id"],
                    opt["distance_km"],
                    opt["capacity"],
                    opt["demand"]
                ])

        print(f"\nCSV file created successfully: {csv_path}")


if __name__ == "__main__":
    test_filter()