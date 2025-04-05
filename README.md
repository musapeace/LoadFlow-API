# Load Flow API 🔌⚡

A simple Django REST API that performs load flow (power flow) analysis for a 3-bus power system using the Gauss-Seidel method.

---

## 🚀 Features

- Add, update, and delete:
  - Buses
  - Lines (with impedance)
  - Loads (real & reactive)
- Compute voltage magnitudes at each bus
- Uses Y-bus matrix and Gauss-Seidel iteration

---

## 📦 API Endpoints

| Method | Endpoint             | Description                 |
|--------|----------------------|-----------------------------|
| GET    | /buses/              | List all buses              |
| POST   | /buses/              | Add a new bus               |
| GET    | /buses/{id}/         | Retrieve a bus              |
| PUT    | /buses/{id}/         | Update a bus                |
| DELETE | /buses/{id}/         | Delete a bus                |
| GET    | /lines/              | List all lines              |
| POST   | /lines/              | Add a new line              |
| GET    | /loads/              | List all loads              |
| POST   | /loads/              | Add a new load              |
| GET    | /loadflow/           | Run load flow calculation   |

---

## 🛠 How to Run

```bash
# 1. Clone the project
git clone clone https://github.com/musapeace/loadflow-api.git
cd LoadFlow-API

# 2. Create virtual environment (optional)
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations and run server
python manage.py migrate
python manage.py runserver
