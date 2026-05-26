# ------------------------------------------------------------
# Batch Algorithm Main Controller
# תפקיד:
# הרצת תהליך שיבוץ מלא:
# 1. שליפת כל האפשרויות
# 2. סינון לפי קיבולת וביקוש
# 3. הרצת מנוע שיבוץ (Score + Greedy Optimization)
# מטרת המערכת:
# להגיע למקסימום התאמות תקינות תוך מינימום מרחק
# ------------------------------------------------------------

from services.batch_algoritm.filter_all_divides_by_mealAccount import filter_all_divides_by_mealAccount
from services.batch_algoritm.engine import build_batch_allocation


def run_batch_algorithm(db):

    filtered_options = filter_all_divides_by_mealAccount(db)

    result = build_batch_allocation(filtered_options)

    return result