# RBAC Platform — Centralized Authorization System

## What Is This?

Most companies build multiple apps — a Reports App, HR App, Finance App. Each one needs to answer the same question:

> **"Is this user allowed to do this action?"**

Without a central system, every app builds its own permission logic. That means:
- 3 apps = 3 separate permission systems to maintain
- If Alice gets promoted, you update 3 places
- Bugs and inconsistencies creep in

**This platform solves that.** One central place manages all roles, permissions, and users. Every app just asks: *"Does user X have permission Y?"* — and gets a Yes or No.

---

## How It Works (Simple Version)

```
Your App  →  imports SDK  →  SDK calls Backend  →  Backend checks Database  →  returns Yes/No
```

**Example:**
```python
from rbac_sdk import RBACClient

client = RBACClient()
client.has_permission("bob@org.com", "delete_user")   # → False
client.has_permission("alice@org.com", "delete_user") # → True
client.get_permissions("charlie@org.com")             # → ["view_reports"]
```

Any app in your organization imports the SDK and gets authorization in 2 lines of code.

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│           Streamlit Admin UI (Port 8501)         │
│   Create roles, permissions, assign users        │
└────────────────────┬────────────────────────────┘
                     │ HTTP + API Key
                     ▼
┌─────────────────────────────────────────────────┐
│           FastAPI Backend (Port 8000)            │
│                                                  │
│  Endpoints:                                      │
│  GET  /roles                                     │
│  POST /roles                                     │
│  GET  /permissions                               │
│  POST /permissions                               │
│  POST /role-permissions  (assign perms to role)  │
│  POST /user-roles        (assign user to role)   │
│  GET  /query/user-permissions?user_id=X  ← SDK  │
│                                                  │
│  All requests require: X-API-Key: dev-key-12345  │
└────────────────────┬────────────────────────────┘
                     │ SQLAlchemy ORM
                     ▼
┌─────────────────────────────────────────────────┐
│           SQLite Database (backend/rbac.db)      │
│                                                  │
│  Tables:                                         │
│  - roles            (id, name, description)      │
│  - permissions      (id, name, description)      │
│  - user_roles       (user_id, role_id)           │
│  - role_permissions (role_id, permission_id)     │
└─────────────────────────────────────────────────┘
                     ▲
                     │ HTTP calls
┌─────────────────────────────────────────────────┐
│           Python SDK (rbac_sdk/)                 │
│                                                  │
│  get_permissions(user_id) → List[str]            │
│  has_permission(user_id, permission) → bool      │
│                                                  │
│  Features: local caching, error handling         │
└────────────────────┬────────────────────────────┘
                     │ imported by
                     ▼
┌─────────────────────────────────────────────────┐
│           Demo Consumer App (Port 8001)          │
│                                                  │
│  GET /dashboard/{user_id}                        │
│  GET /check/{user_id}/{permission}               │
│                                                  │
│  Shows SDK working in a real app context         │
└─────────────────────────────────────────────────┘
```

---

## Project Structure

```
rbac-platform/
├── backend/
│   ├── config.py            # API key, database URL
│   ├── database.py          # SQLAlchemy engine setup
│   ├── models.py            # ORM models (Role, Permission, etc.)
│   ├── schemas.py           # Pydantic validation models
│   ├── middleware.py        # API key authentication
│   ├── main.py              # FastAPI app entry point
│   ├── rbac.db              # SQLite database (auto-created)
│   ├── routes/
│   │   ├── roles.py         # GET/POST /roles
│   │   ├── permissions.py   # GET/POST /permissions
│   │   ├── role_permissions.py  # POST /role-permissions
│   │   ├── user_roles.py    # POST/GET /user-roles
│   │   └── query.py         # GET /query/user-permissions
│   └── services/
│       ├── role_service.py
│       ├── permission_service.py
│       └── user_permission_service.py
│
├── rbac_sdk/
│   ├── __init__.py          # Exports RBACClient + exceptions
│   ├── client.py            # RBACClient class
│   └── exceptions.py        # RBACAuthError, RBACConnectionError, etc.
│
├── init_db.py               # Creates tables + seeds test data
├── demo_app.py              # Demo FastAPI app using the SDK
├── admin_ui.py              # Streamlit admin dashboard
└── .venv/                   # Virtual environment
```

---

## Seed Data (Pre-loaded)

### Users
| User | Role | 
|------|------|
| alice@org.com | Admin |
| bob@org.com | Manager |
| charlie@org.com | Employee |

### Roles & Permissions
| Role | view_reports | approve_requests | delete_user | edit_role |
|------|:---:|:---:|:---:|:---:|
| Admin | ✅ | ✅ | ✅ | ✅ |
| Manager | ✅ | ✅ | ❌ | ❌ |
| Employee | ✅ | ❌ | ❌ | ❌ |

---

## How to Run

### Prerequisites
```powershell
cd E:\prudential\rbac-platform
.venv\Scripts\Activate.ps1
```

### Terminal 1 — Backend
```powershell
uvicorn backend.main:app --reload
# Running at http://localhost:8000
```

### Terminal 2 — Demo App
```powershell
uvicorn demo_app:app --reload --port 8001
# Running at http://localhost:8001
```

### Terminal 3 — Admin UI
```powershell
streamlit run admin_ui.py
# Running at http://localhost:8501
```

---

## How to Add a New User

Users are added by assigning them to a role. You can do this in 2 ways:

### Option 1 — Admin UI (No code needed)
1. Go to `http://localhost:8501`
2. Click **Tab 3 — User Assignments**
3. Type the user ID (e.g. `dave@org.com`)
4. Select a role (Admin / Manager / Employee)
5. Click **Assign User**
6. Done — dave now has all permissions of that role

### Option 2 — API call
```powershell
Invoke-WebRequest -UseBasicParsing -Uri "http://localhost:8000/user-roles" `
  -Method POST `
  -Headers @{"X-API-Key"="dev-key-12345"; "Content-Type"="application/json"} `
  -Body '{"user_id": "dave@org.com", "role_id": 2}'
```
`role_id`: 1 = Admin, 2 = Manager, 3 = Employee

### Option 3 — Python SDK (from any app)
```python
# After assigning via UI or API, the SDK instantly picks it up
client = RBACClient()
client.get_permissions("dave@org.com")  # → returns Manager permissions
```

---

## Testing the System

### Test 1 — Backend Health
```powershell
(Invoke-WebRequest -UseBasicParsing -Uri "http://localhost:8000/roles" -Headers @{"X-API-Key"="dev-key-12345"}).Content
```
✅ Expected: JSON list of 3 roles

### Test 2 — Permission Query
```powershell
(Invoke-WebRequest -UseBasicParsing -Uri "http://localhost:8000/query/user-permissions?user_id=alice@org.com" -Headers @{"X-API-Key"="dev-key-12345"}).Content
```
✅ Expected: `["approve_requests","delete_user","edit_role","view_reports"]`

### Test 3 — SDK
```powershell
python -c "from rbac_sdk import RBACClient; c = RBACClient(); print(c.get_permissions('bob@org.com')); print(c.has_permission('bob@org.com', 'delete_user'))"
```
✅ Expected: `['approve_requests', 'view_reports']` then `False`

### Test 4 — Demo App Dashboard
```powershell
(Invoke-WebRequest -UseBasicParsing -Uri "http://localhost:8001/dashboard/charlie@org.com").Content
```
✅ Expected: charlie has only `can_view_reports: true`

### Test 5 — Auth Protection
```powershell
(Invoke-WebRequest -UseBasicParsing -Uri "http://localhost:8000/roles").Content
```
✅ Expected: 401 error — no API key = blocked

---

## Key API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/roles` | List all roles |
| POST | `/roles` | Create a role |
| GET | `/permissions` | List all permissions |
| POST | `/permissions` | Create a permission |
| POST | `/role-permissions` | Assign permission to role |
| POST | `/user-roles` | Assign user to role |
| GET | `/user-roles/by-user/{user_id}` | Get roles for a user |
| GET | `/query/user-permissions?user_id=X` | **Get all permissions for user (SDK uses this)** |

All requests require header: `X-API-Key: dev-key-12345`

---

## SDK Reference

```python
from rbac_sdk import RBACClient

# Initialize (defaults to localhost:8000)
client = RBACClient()

# Or point to a different server
client = RBACClient(base_url="http://your-server.com", api_key="your-key")

# Get all permissions for a user
permissions = client.get_permissions("alice@org.com")
# → ["approve_requests", "delete_user", "edit_role", "view_reports"]

# Check a single permission
can_delete = client.has_permission("bob@org.com", "delete_user")
# → False
```

**Exceptions the SDK raises:**
- `RBACAuthError` — wrong API key
- `RBACConnectionError` — backend is unreachable
- `RBACNotFoundError` — user doesn't exist

---

## What Makes This Useful

Without this platform, if you have 5 apps and need to change Bob's permissions, you update 5 systems. With this platform, you update one role in one place — all 5 apps reflect it instantly because they all query the same backend via the SDK.