import numpy as np
from scipy.optimize import linprog


# 1. הגדרת הנתונים שחולצו ממסד הנתונים
# מלאי המנות בכל מוקד (DistributionCenter) לפי הנתונים התקפים של היום
supply = np.array([r["capacity"] for r in results])


