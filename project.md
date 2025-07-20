# 📦 Django Dijital Envanter ve Demirbaş Takip Sistemi (API Only)

## 🎯 Proje Amacı
Ofis, okul, atölye gibi fiziksel alanlarda bulunan cihazların ve demirbaşların takibini yapmak için kullanılan bir envanter yönetim sistemi. Çoğu kurum bunu ya Excel’de ya da hiç yapmıyor. Bu API, her cihazın kimde olduğunu, ne zaman alındığını ve durumunu gösterir.

---

## 🧱 Kullanılan Teknolojiler
- Django
- Django REST Framework
- drf-spectacular
- SQLite (dev için yeterli)

---

## 🔑 Modeller

### 1. User (Kullanıcı)
- `username`
- `email`
- `full_name`
- `role` (choices: admin, staff)

---

### 2. Category (Kategori)
- `name` (örnek: Bilgisayar, Mobilya, Elektronik, Alet, vb.)
- `description`

---

### 3. Item (Demirbaş/Envanter)
- `name`
- `serial_number` (benzersiz)
- `category` → Category
- `assigned_to` → User (staff)
- `status` (choices: available, assigned, broken, maintenance, retired)
- `purchase_date`
- `warranty_until`
- `notes`

---

### 4. Assignment History (İşlem Geçmişi)
- `item` → Item
- `assigned_to` → User
- `assigned_by` → User (admin)
- `assigned_at`
- `returned_at`
- `condition_on_return`

---

## 🔌 API Endpoint'leri

### 🔐 Auth
- [POST] `/api/auth/register/` (Sadece admin)
- [POST] `/api/auth/login/`
- [POST] `/api/auth/logout/`

---

### 👤 Kullanıcılar
- [GET] `/api/users/` → admin
- [GET] `/api/users/me/`
- [PUT] `/api/users/me/`

---

### 📁 Kategoriler
- [GET, POST] `/api/categories/`
- [GET, PUT, DELETE] `/api/categories/{id}/`

---

### 📦 Envanter
- [GET, POST] `/api/items/`
- [GET, PUT, DELETE] `/api/items/{id}/`
- [GET] `/api/items/?status=assigned` → filtreleme desteklenmeli

---

### 🔄 Demirbaş Atama
- [POST] `/api/assignments/` → item, user, tarih
- [GET] `/api/assignments/` → tarihsel log
- [PATCH] `/api/assignments/{id}/return/` → return işlemi ve durumu girilir

---

## 🧠 İş Kuralları

- Aynı item birden fazla kullanıcıya atanamaz.
- Atanan bir cihaz tekrar atanamaz, önce iade edilmeli.
- `serial_number` benzersiz olmalı.
- Sadece admin kullanıcılar atama yapabilir.
- `assigned_to` alanı boşsa cihaz boştadır.

---

## 📚 Swagger Dökümantasyonu
- drf-spectacular ile her endpoint detaylı olmalı.
- Enum alanlar açıklamalı olmalı.
- Tüm örnek istek ve cevaplar belgelensin.

---

## ✅ Test Senaryoları
- [ ] Yeni kategori oluştur.
- [ ] Yeni demirbaş ekle.
- [ ] Admin olarak kullanıcıya cihaz ata.
- [ ] Kullanıcı login olsun ve cihazlarını görsün.
- [ ] Admin cihazı iade alıp başka kullanıcıya atasın.
- [ ] Kırık cihaz için status "broken" yapılabilsin.

---

## 📂 Klasör Yapısı Önerisi

