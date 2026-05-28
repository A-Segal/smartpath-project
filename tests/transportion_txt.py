import numpy as np
from scipy.optimize import linprog

# 1. הגדרת הנתונים שחולצו ממסד הנתונים
# מלאי המנות בכל מוקד (לדוגמה: מוקד ת"א, מוקד ר"ג)
supply = np.array([20, 15])

# דרישות המנות של כל משפחה (לדוגמה: משפחה א', ב', ג')
demand = np.array([10, 15, 10])

# מטריצת המרחקים/עלויות (שורות=מוקדים, עמודות=משפחות)
# למשל: המרחק ממוקד 1 למשפחה 3 הוא 15 ק"מ
costs = np.array([
    [5, 10, 15],
    [20, 8, 4]
])

# 2. שטיחת המטריצה למערך חד-ממדי עבור האלגוריתם
c = costs.flatten()

# 3. הגדרת אילוצי המוקדים (לא יכולים לתת יותר ממה שיש להם)
A_eq_supply = np.zeros((len(supply), len(c)))
for i in range(len(supply)):
    A_eq_supply[i, i*len(demand) : (i+1)*len(demand)] = 1

# 4. הגדרת אילוצי המשפחות (חייבות לקבל בדיוק את מה שהן צריכות)
A_eq_demand = np.zeros((len(demand), len(c)))
for j in range(len(demand)):
    A_eq_demand[j, j::len(demand)] = 1

# חיבור האילוצים
A_eq = np.vstack([A_eq_supply, A_eq_demand])
b_eq = np.concatenate([supply, demand])

# 5. הרצת אלגוריתם התחבורה
# שימוש בשיטת highs שהיא היעילה ביותר לבעיות זרימה ואופטימיזציה ליניארית כיום
result = linprog(c, A_eq=A_eq, b_eq=b_eq, method='highs')

# 6. פענוח התוצאות לשיבוץ בפועל
if result.success:
    optimal_allocation = np.round(result.x).reshape(costs.shape)
    print("שיבוץ אופטימלי (כמות מנות מכל מוקד לכל משפחה):")
    print(optimal_allocation)
else:
    print("לא נמצא פתרון. יש לבדוק אם סך ההיצע שווה או גדול לסך הביקוש.")