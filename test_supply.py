import numpy as np

from db_connection import get_session
from services.batch_algoritm.options_of_Inlay_filter_by_meals import dict_of_valid_divide_options

# =========================
# Connect to DB
# =========================
db = get_session()

# =========================
# Fetch all valid options
# =========================
results = dict_of_valid_divide_options(db)

# =========================
# Build Supply array
# =========================
supply = np.array([
    next(
        r["capacity"]
        for r in results
        if r["center_id"] == center_id
    )
    for center_id in sorted({r["center_id"] for r in results})
])

# =========================
# Print Supply
# =========================
centers = sorted({r["center_id"] for r in results})
print("SUPPLY ARRAY")
print("=" * 70)
for i, center_id in enumerate(centers):
    print(f"Center {center_id:<2}: {supply[i]}")
print("\n")

# =========================
# Build Demand array
# =========================
demand = np.array([
    sum(r["demand"] for r in results if r["recipient_id"] == recipient_id)
    for recipient_id in sorted({r["recipient_id"] for r in results})
])

# =========================
# Print Demand
# =========================
recipients = sorted({r["recipient_id"] for r in results})
print("DEMAND ARRAY")
print("=" * 70)
for i, recipient_id in enumerate(recipients):
    print(f"Recipient {recipient_id:<2}: {demand[i]}")
print("\n")

# =========================
# Build Costs / Distance matrix
# =========================
costs = np.array([
    [
        next(
            (
                r["distance_km"]
                for r in results
                if r["center_id"] == center_id
                and r["recipient_id"] == recipient_id
            ),
            np.inf
        )
        for recipient_id in recipients
    ]
    for center_id in centers
])

# =========================
# Print Costs matrix nicely
# =========================
print("COSTS MATRIX")
print("=" * 70)

# Header
header = " " * 10 + "".join([f"{'Recipient '+str(r):>15}" for r in recipients])
print(header)
print("-" * len(header))

# Rows
for i, center_id in enumerate(centers):
    row_values = "".join(f"{costs[i][j]:>15.2f}" for j in range(len(recipients)))
    print(f"{'Center '+str(center_id):<10}{row_values}")

print("\n")


# 2. שטיחת מטריצת העלויות למערך חד-ממדי עבור האלגוריתם
c = costs.flatten()

print("COSTS ARRAY (flattened)")
print("=" * 70)
print(c)
print("\n")