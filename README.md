# 📦 Django Digital Inventory and Asset Tracking System (API Only)

## 🎯 Project Purpose
A digital inventory management system used to track devices and assets in physical spaces such as offices, schools, and workshops. Most organizations either track this in Excel or don't track it at all. This API shows who has which device, when it was acquired, and its current status.

## 🧱 Technologies Used
- Django 4.2.7
- Django REST Framework 3.14.0
- drf-spectacular (API Documentation)
- SQLite (sufficient for development)
- django-filter

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- pip

### Installation
1. Clone the repository
```bash
git clone <repository-url>
cd digital_inventoryApi
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```


4. Apply migrations
```bash
python manage.py migrate
```

5. Create a superuser
```bash
python manage.py createsuperuser
```

6. Run the development server
```bash
python manage.py runserver
```


## 🔑 Models

### 1. User
- `email` (unique)
- `full_name`
- `role` (choices: admin, staff)

### 2. Category
- `name` (e.g., Computer, Furniture, Electronics, Tools, etc.)
- `description`

### 3. Item (Asset/Inventory)
- `name`
- `serial_number` (unique)
- `category` → Category
- `assigned_to` → User (staff)
- `status` (choices: available, assigned, broken, maintenance, retired)
- `purchase_date`
- `warranty_until`
- `notes`

### 4. Assignment History
- `item` → Item
- `assigned_to` → User
- `assigned_by` → User (admin)
- `assigned_at`
- `returned_at`
- `condition_on_return`

## 🔌 API Endpoints

### 🔐 Auth
- [POST] `/api/auth/register/` (Admin only)
- [POST] `/api/auth/login/`
- [POST] `/api/auth/logout/`

### 👤 Users
- [GET] `/api/auth/` → admin
- [GET, PUT] `/api/auth/me/`

### 📁 Categories
- [GET, POST] `/api/categories/`
- [GET, PUT, DELETE] `/api/categories/{id}/`

### 📦 Inventory
- [GET, POST] `/api/items/`
- [GET, PUT, DELETE] `/api/items/{id}/`
- [GET] `/api/items/?status=assigned` → filtering supported

### 🔄 Asset Assignment
- [POST] `/api/assignments/` → item, user, date
- [GET] `/api/assignments/` → historical log
- [PATCH] `/api/assignments/{id}/return/` → return process and condition

## 🧠 Business Rules

- The same item cannot be assigned to multiple users.
- An assigned device cannot be reassigned; it must be returned first.
- `serial_number` must be unique.
- Only admin users can make assignments.
- If the `assigned_to` field is empty, the device is available.

## 📚 API Documentation
- Detailed documentation with drf-spectacular
- Access Swagger UI: `/api/docs/`
- Access ReDoc: `/api/redoc/`
- Access Schema: `/api/schema/`

## ✅ Test Scenarios
- Create a new category.
- Add a new asset.
- As an admin, assign a device to a user.
- User logs in and sees their devices.
- Admin takes back a device and assigns it to another user.
- Mark a broken device with status "broken".

## 🛠️ Future Improvements
1. JWT token-based authentication
2. Enhanced filtering and search capabilities
3. Reporting features
4. Frontend user interface
5. Image upload for items
6. Barcode/QR code generation and scanning

## 📄 License
This project is licensed under the MIT License. 
