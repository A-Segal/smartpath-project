import numpy as np
from scipy.optimize import linprog
from sqlalchemy.testing import db

from services.batch_algoritm.options_of_Inlay_filter_by_meals import dict_of_valid_divide_options

# 1. הגדרת הנתונים שחולצו ממסד הנתונים
# מלאי המנות בכל מוקד (DistributionCenter) לפי הנתונים התקפים של היום
# שליפת כל האפשרויות מהמערכת
results = dict_of_valid_divide_options(db)

# בניית קיבולת לכל מוקד (Supply)
supply = np.array([
    next(r["capacity"] for r in results if r["center_id"] == center_id)
    for center_id in sorted({r["center_id"] for r in results})
])


# דרישות המנות (Demand) לכל נזקק / משפחה
# כל ערך במערך מייצג את סך המנות שנדרשות עבור recipient_id מסוים
# מבוסס על הנתונים שחולצו מ-results, תוך איחוד דרישות לפי מזהה נזקק
demand = np.array([
    next(
        r["demand"]
        for r in results
        if r["recipient_id"] == recipient_id
    )
    for recipient_id in sorted({r["recipient_id"] for r in results})
])



# מטריצת העלויות / מרחקים בין מוקדים לנזקקים
# כל שורה מייצגת DistributionCenter
# כל עמודה מייצגת Recipient
# הערך בכל תא הוא המרחק (בק"מ) בין המוקד לנזקק
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
        for recipient_id in sorted({r["recipient_id"] for r in results})
    ]
    for center_id in sorted({r["center_id"] for r in results})
])

# 2. שטיחת מטריצת העלויות למערך חד-ממדי עבור האלגוריתם
c = costs.flatten()



