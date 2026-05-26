# ------------------------------------------------------------
# Batch Test Runner
# תפקיד:
# - הרצת אלגוריתם מלא
# - בדיקות תוצאה
# - יצירת CSV לניתוח
#
# מטרת CSV:
# להציג:
# - התאמות בפועל
# - ביקוש מקורי
# - קיבולת מקורית
# - מרחק בין נקודות
# ------------------------------------------------------------

from db_connection import SessionLocal
import csv
import os

from services.batch_algoritm.batch_main import run_batch_algorithm


def save_to_csv(allocations):

    folder = "csvfiles"
    os.makedirs(folder, exist_ok=True)

    path = os.path.join(folder, "batch_result.csv")

    with open(path, "w", newline="", encoding="utf-8") as f:

        writer = csv.writer(f)

        writer.writerow([
            "DistributionCenterID",
            "RecipientID",
            "amount_of_meals",
            "distance_km",
            "center_requested_meals",
            "recipient_requested_meals"
        ])

        for a in allocations:

            writer.writerow([
                a["DistributionCenterID"],
                a["RecipientID"],
                a["amount_of_meals"],
                a["distance_km"],
                a["center_requested_meals"],
                a["recipient_requested_meals"]
            ])

    print("\nCSV CREATED:", path)


def run_test():

    print("TEST STARTED")

    db = SessionLocal()

    try:

        result = run_batch_algorithm(db)

        allocations = result["allocations"]

        print("\nTOTAL ALLOCATIONS:", len(allocations))

        print("\nSAMPLE RESULT:")
        if allocations:
            print(allocations[0])

        print("\nREMAINING DEMAND:")
        print(result["recipient_demand_status"])

        print("\nREMAINING CAPACITY:")
        print(result["center_capacity_status"])

        save_to_csv(allocations)

        print("\nTEST FINISHED")

    except Exception as e:
        print("ERROR:", e)

    finally:
        db.close()


run_test()