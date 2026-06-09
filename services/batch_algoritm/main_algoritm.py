from collections import deque
from db_connection import get_session
from repository.recipient_request_repository import RecipientRequestRepository
from services.batch_algoritm.matching_algorithm import build_candidates_for_centers, sort_center_candidates

def run_full_matching(db):
    # 1️⃣ בונים את כל המועמדים
    candidates = build_candidates_for_centers(db)

    # 2️⃣ ממיינים את הרשימות לפי Score
    candidates = sort_center_candidates(candidates)

    # 3️⃣ מבני נתונים לאלגוריתם
    # תור המוקדים הרלוונטיים
    queue = deque(candidates.keys())
    # מצביע לכל רשימה שמצביע למועמד הנוכחי
    current_index = {center_id: 0 for center_id in candidates}
    # מנהל את כל השיבוצים בזמן אמת
    recipient_assignment = {}

    # session repo בתוך הפונקציה
    recipient_request_repo = RecipientRequestRepository(db)
    total_recipients = len(recipient_request_repo.get_all_requests())

    # 4️⃣ לולאת שיבוץ
    while queue and len(recipient_assignment) < total_recipients:
        center_id = queue.popleft()
        idx = current_index[center_id]

        if idx >= len(candidates[center_id]):
            continue

        recipient_id, score, recipient_meals, center_meals = candidates[center_id][idx]

        # אם הנזקק לא משובץ
        if recipient_id not in recipient_assignment:
            recipient_assignment[recipient_id] = {
                "center_id": center_id,
                "score": score,
                "recipient_meals": recipient_meals,
                "center_meals": center_meals
            }

        else:
            current_assignment = recipient_assignment[recipient_id]
            old_center = current_assignment["center_id"]
            old_score = current_assignment["score"]

            # החלפה אם Score טוב יותר
            if score < old_score:
                recipient_assignment[recipient_id] = {
                    "center_id": center_id,
                    "score": score,
                    "recipient_meals": recipient_meals,
                    "center_meals": center_meals
                }
                current_index[old_center] += 1
                queue.append(old_center)

            else:
                current_index[center_id] += 1
                queue.append(center_id)

    # dict: recipient_id -> {center_id, score, recipient_meals, center_meals}
    return recipient_assignment