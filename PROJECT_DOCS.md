# SmartPath — Project Documentation & Instruction Page

## 📋 What This Project Does

SmartPath is a **food delivery management system**. It connects three types of users:

| User Type | Role |
|-----------|------|
| **Distribution Centers** | Provide meals to deliver |
| **Recipients** | Receive meal deliveries |
| **Volunteers** | Drive and deliver meals from centers to recipients |

The system has two smart algorithms:
1. **Batch Matching** — Automatically matches which recipients get food from which distribution center
2. **VRP Route Solver** — Calculates the best delivery route for each volunteer

---

## 🛠 Tech Stack

| Layer | What We Use |
|-------|-------------|
| Language | Python 3 |
| Web Framework | Flask |
| Database | Microsoft SQL Server (`deliveryDB`) |
| ORM | SQLAlchemy with pyodbc |
| Maps | Google Maps API (Geocoding + Distance Matrix) |
| Frontend | React (separate project — `@react-google-maps/api`, `axios`) |

---

## 📁 Project File Structure

```
smartpath-project/
│
├── main.py                          # Entry point — starts the Flask server
├── db_connection.py                 # Database connection (SQLAlchemy + SQL Server)
├── package.json                     # Frontend JavaScript dependencies
│
├── controller/                      # API endpoints (Flask Blueprints)
│   ├── auth_controller.py           # Login endpoint
│   ├── volunteer_controller.py      # Volunteer CRUD
│   ├── recipient_controller.py      # Recipient CRUD
│   ├── recipient_request_controller.py
│   ├── dc_request_controller.py
│   ├── permission_controller.py
│   ├── vehicle_controller.py
│   ├── staff_member_controller.py
│   ├── distribution_center_controller.py
│   ├── delivery_assignment_controller.py
│   └── volunteer_request_controller.py
│
├── models/                          # Database table definitions
│   ├── base.py                      # Shared SQLAlchemy base
│   ├── volunteer.py
│   ├── recipient.py
│   ├── distribution_center.py
│   ├── delivery_assignment.py
│   ├── DC_request.py
│   ├── recipient_request.py
│   ├── volunteer_request.py
│   ├── vehicle.py
│   ├── staff_member.py
│   └── permission.py
│
├── repository/                      # Database access layer (CRUD operations)
│   ├── VolunteerRepository.py
│   ├── RecipientRepository.py
│   ├── DistributionCenterRepository.py
│   ├── DeliveryAssignmentRepository.py
│   ├── DCRequestRepository.py
│   ├── RecipientRequestRepository.py
│   ├── VolunteerRequestRepository.py
│   ├── VehicleRepository.py
│   ├── StaffMemberRepository.py
│   └── PermissionRepository.py
│
├── dto/                             # Data Transfer Objects (JSON serialization)
│   └── ... (10 DTO files)
│
├── services/                        # Business logic
│   ├── delivery_assignment_service.py    # Runs matching → saves to DB
│   ├── volunteer_route_service.py        # Runs VRP routing → saves to DB
│   ├── utils/
│   │   └── googleMaps.py                # Google Maps API functions
│   ├── batch_algoritm/
│   │   ├── main_algoritm.py             # Two-phase Gale-Shapley matching
│   │   ├── matching_algorithm.py        # Scoring & candidate building
│   │   ├── execute_full_matching.py     # Wrapper
│   │   └── print_results.py            # Debug output
│   └── vrp/
│       ├── solver.py                    # Greedy VRP route solver (active)
│       ├── vrp_state.py                 # State + feasibility checks
│       ├── engine.py                    # ⚠️ OLD — not used anymore
│       └── state.py                     # ⚠️ OLD — not used anymore
│
├── csvfiles/                        # Test data
├── tests/
│   └── test_repository.py           # Manual integration test
└── PROJECT_DOCS.md                  # ← THIS FILE
```

---

## 🗄 Database Tables

| Table | What It Stores | Key Fields |
|-------|---------------|------------|
| **Volunteer** | Delivery drivers | id, fname, lname, username, password, mail, phone |
| **Vehicle** | Volunteer's car | id, VolunteerID, capacity |
| **Recipient** | People receiving food | id, fname, lname, username, password, mail, phone, location_lat, location_lng |
| **Recipient_Request** | Food requests from recipients | id, RecipientID, amount_of_meals, request_date |
| **DistributionCenter** | Food distribution centers | id, fname, lname, username, password, mail, phone, location_lat, location_lng |
| **DC_Request** | Meal offerings from centers | id, DistributionCenterID, amount_of_meals, request_date, freshness_priority |
| **DeliveryAssignment** | Who delivers what to whom | id, DistributionCenterID, RecipientID, VolunteerID, amount_of_meals, freshness_priority |
| **volunteer_request** | Volunteer route requests | id, volunteer_id, location_lat, location_lng, available_time |
| **StaffMember** | System staff | id, fname, lname, username, password, mail, phone, PermissionID |
| **Permission** | Staff permission types | id, type |

---

## 🌐 API Endpoints (53 Total)

Every entity has these 5 standard endpoints: `GET /<entity>`, `GET /<entity>/<id>`, `POST /<entity>`, `PUT /<entity>/<id>`, `DELETE /<entity>/<id>`.

### Special Endpoints

| Method | Endpoint | What It Does |
|--------|----------|-------------|
| `POST` | `/auth/login` | Login — checks username/password against Volunteer → Recipient → DistributionCenter |
| `POST` | `/delivery_assignment/run_matching` | Runs the batch matching algorithm and creates assignments |
| `POST` | `/volunteer_request/run_route/<volunteer_id>` | Runs VRP route optimization for one volunteer |
| `DELETE` | `/vehicles/volunteer/<volunteer_id>` | Deletes all vehicles belonging to a volunteer |

### All Entity Endpoints

| Entity | Base URL |
|--------|----------|
| Volunteers | `/volunteers` |
| Recipients | `/recipients` |
| Recipient Requests | `/recipient_request` |
| DC Requests | `/dc_requests` |
| Permissions | `/permissions` |
| Vehicles | `/vehicles` |
| Staff Members | `/staff` |
| Distribution Centers | `/distribution_center` |
| Delivery Assignments | `/delivery_assignment` |
| Volunteer Requests | `/volunteer_request` |

---

## 🧠 How The Algorithms Work

### Algorithm 1 — Batch Matching

**File:** `services/batch_algoritm/main_algoritm.py`

This decides which distribution center serves each recipient.

**Phase 1 (Gale-Shapley style):**
- Each center builds a list of candidates (recipients within 100km who need ≤ the center's meal count)
- Score formula: `(distance / 100) × 0.8 + ((center_meals − recipient_meals) / center_meals) × 0.2`
- Lower score = better match
- Centers take turns proposing to their best-scored recipient
- If a recipient gets a better offer, they switch — and the old center goes back in the queue

**Phase 2 (Fill remaining capacity):**
- Unassigned recipients get matched to centers that still have meals left
- Limited to 10km from the center's first assigned recipient

### Algorithm 2 — VRP Route Solver

**File:** `services/vrp/solver.py`

This calculates the best delivery route for one volunteer.

- **Greedy best-first search** with limits: 50 max iterations, 3 branches per state
- Checks each candidate group for **feasibility** (enough time + enough vehicle capacity)
- Optimizes for: **most deliveries** (families), with shortest time as tiebreaker
- Uses **Google Distance Matrix API** for real travel times between locations
- Returns an ordered route: Start → Center 1 → Recipients → Center 2 → Recipients → ...

---

## 🐛 Known Bugs & Issues

### 🔴 CRITICAL — Will Crash

| # | Problem | Where | What Happens |
|---|---------|-------|-------------|
| 1 | Volunteer model has no `location_lat`/`location_lng` fields | `models/volunteer.py` vs `services/volunteer_route_service.py:99-100` | When running a route WITHOUT a `start_address`, the code tries to read `volunteer.location_lat` which doesn't exist → **AttributeError crash** |
| 2 | `travel_time_between_points` returns `0` on error | `services/utils/googleMaps.py:69` | When Google API fails, it returns 0 instead of a big number. The solver thinks travel takes 0 minutes → impossible routes get created |
| 3 | Google API key hardcoded | `services/utils/googleMaps.py:5` | `AIzaSyAKmXqHHc8_vOP30aKSKvV2C3sH2c67fqY` is in the source code — security risk, visible in git, can't rotate without code change |

### 🟠 HIGH — Security & Design

| # | Problem | Where | What Happens |
|---|---------|-------|-------------|
| 4 | Passwords stored as plaintext | All models + `controller/auth_controller.py` | No hashing at all. Anyone with DB access can read every password |
| 5 | No authentication after login | All controllers | The login returns user info but there's no token/JWT/session. Every API endpoint is completely public |
| 6 | Matching creates its own DB session | `services/batch_algoritm/execute_full_matching.py` | `execute_full_matching()` opens a separate DB session from the matching algorithm — data inconsistency risk |
| 7 | Duplicate imports | `db_connection.py:10-15` | `Permission`, `Vehicle`, `Volunteer` imported twice — messy but harmless |
| 8 | 187 lines of commented-out duplicate code | `services/volunteer_route_service.py:179-366` | Nearly the entire service is duplicated and commented out at the bottom of the file |

### 🟡 MEDIUM — Functionality Issues

| # | Problem | Where | What Happens |
|---|---------|-------|-------------|
| 9 | Legacy dead code files | `services/vrp/engine.py`, `services/vrp/state.py` | Old VRP engine using class-based groups. Never imported — just adds confusion |
| 10 | No database migrations | `db_connection.py:23` | `create_all()` runs on every import. No Alembic. Schema changes need manual SQL |
| 11 | No input validation | All controllers | Bad data → unhandled SQLAlchemy errors → 500 crashes instead of helpful error messages |
| 12 | No error handler | `main.py` | Uncaught exceptions return HTML 500 page, not JSON. API clients get garbage |
| 13 | Inconsistent table naming | `models/volunteer_request.py` | Table is `volunteer_request` (lowercase) but all others are PascalCase. FK is `volunteer_id` but others are `VolunteerID` |
| 14 | No logging — only `print()` | Whole project | Debug messages go to console with no levels, no file output, no way to disable |
| 15 | `Vehicle.type` doesn't exist | `services/volunteer_route_service.py:125` | Code reads `vehicle.type` but Vehicle model has no `type` column. Always falls back to default `3` |

### 🔵 LOW — Code Quality

| # | Problem | Where |
|---|---------|-------|
| 16 | Almost no tests | `tests/` — only one manual integration test |
| 17 | Sessions could leak | All controllers use manual `try/finally` — no context manager |
| 18 | Debug mode hardcoded | `main.py:37` — `debug=True` always on |
| 19 | No `.env` / config file | All settings hardcoded in source |
| 20 | Debug prints in production code | `services/vrp/solver.py`, `services/utils/googleMaps.py` |

---

## 🚀 How To Run

### Prerequisites
- Python 3 installed
- Microsoft SQL Server running locally
- `deliveryDB` database created
- ODBC Driver 17 for SQL Server installed

### Steps
```bash
# 1. Install Python dependencies
pip install flask flask-cors sqlalchemy pyodbc requests

# 2. Run the server
python main.py

# 3. Server starts at http://localhost:5000
# 4. Test: GET http://localhost:5000/ → "Server is running!"
```

### Database
- Connection: Windows Trusted Authentication to `localhost\deliveryDB`
- Tables are auto-created on startup via `Base.metadata.create_all()`
- No seed data included — populate via the API endpoints

---

## ✅ What's Good About This Project

- Clean **3-tier architecture** (Controller → Service → Repository)
- Well-designed **matching and routing algorithms**
- Comprehensive REST API covering all entities
- Real **Google Maps integration** for actual travel times
- Consistent CRUD patterns across all controllers
- Good separation of concerns

---

## 🔧 Recommended Fix Priority

1. **Fix the Volunteer model** — add `location_lat`/`location_lng` columns
2. **Fix `travel_time_between_points`** — return `999999` on error instead of `0`
3. **Move API key** to environment variable
4. **Hash passwords** with bcrypt
5. **Add JWT authentication** middleware
6. **Remove commented-out code** in `volunteer_route_service.py`
7. **Clean up** duplicate imports and legacy VRP files

---

*Generated: July 2026 | Project: SmartPath Server*
