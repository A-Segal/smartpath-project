import csv
import os

from db_connection import get_session
from services.batch_algoritm.filter_all_divides_by_mealAccount import (
    filter_all_divides_by_mealAccount
)


def test_filter():

    with get_session() as db:

        result = filter_all_divides_by_mealAccount(db)

        print("\n========== FILTER RESULT ==========\n")

        if not result:
            print("No valid options found")
            return

        os.makedirs("csvfiles", exist_ok=True)

        csv_path = os.path.join("csvfiles", "filtered_results.csv")

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