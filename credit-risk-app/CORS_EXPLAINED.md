# 🌐 CORS - Cross-Origin Resource Sharing

## ❓ CORS là gì?

**CORS** (Cross-Origin Resource Sharing) là cơ chế bảo mật của trình duyệt để ngăn chặn các trang web gọi API từ domain khác.

### Ví dụ:

- **Frontend**: `http://localhost:3000` (Vue)
- **Backend**: `http://localhost:8000` (FastAPI)

Đây là 2 **origins khác nhau** (khác port) → Trình duyệt sẽ **chặn** request mặc định!

---

## 🔧 Cấu hình CORS trong dự án này

### Backend (FastAPI) - `backend/main.py`

```python
from fastapi.middleware.cors import CORSMiddleware

# Danh sách origins được phép
origins = [
    "http://localhost:3000",      # Vue dev server (port mặc định)
    "http://localhost:5173",      # Vite alternative port
    "http://127.0.0.1:3000",      # IPv4 localhost
    "http://127.0.0.1:5173",
]

# Thêm CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,              # Chỉ cho phép các origins này
    allow_credentials=True,             # Cho phép cookies
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Các HTTP methods
    allow_headers=["*"],                # Cho phép mọi header
    expose_headers=["*"],               # Expose mọi header
)
```

### Frontend (Vue) - `frontend/src/App.vue`

```javascript
// Base URL của API
const API_BASE = 'http://localhost:8000'

// Gọi API
axios.post(`${API_BASE}/predict`, data)
```

---

## 🚦 Luồng hoạt động CORS

### 1. Preflight Request (OPTIONS)

Khi frontend gọi POST/PUT/DELETE, trình duyệt sẽ gửi **preflight request** trước:

```
OPTIONS http://localhost:8000/predict
Origin: http://localhost:3000
```

Backend phản hồi:

```
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: *
```

### 2. Actual Request

Nếu preflight OK, trình duyệt mới gửi request thật:

```
POST http://localhost:8000/predict
Origin: http://localhost:3000
Content-Type: application/json

{ "X_1": 0.025, ... }
```

---

## ✅ Khi nào CORS hoạt động?

CORS hoạt động khi:

1. ✅ Backend đã thêm `CORSMiddleware`
2. ✅ Origin của frontend nằm trong `allow_origins`
3. ✅ HTTP method nằm trong `allow_methods`
4. ✅ Backend đang chạy (port 8000)
5. ✅ Frontend đang chạy (port 3000 hoặc 5173)

---

## ❌ Lỗi CORS phổ biến

### Lỗi 1: Origin not allowed

```
Access to fetch at 'http://localhost:8000/predict' from origin 'http://localhost:3000'
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present
```

**Nguyên nhân:**
- Backend chưa cấu hình CORS
- Origin không nằm trong `allow_origins`

**Giải pháp:**
- Kiểm tra `backend/main.py` đã có `CORSMiddleware`
- Thêm `http://localhost:3000` vào `origins`

### Lỗi 2: Method not allowed

```
has been blocked by CORS policy: Method POST is not allowed
```

**Nguyên nhân:** Method POST không nằm trong `allow_methods`

**Giải pháp:**
- Thêm `"POST"` vào `allow_methods`

### Lỗi 3: Connection refused

```
net::ERR_CONNECTION_REFUSED
```

**Nguyên nhân:** Backend không chạy

**Giải pháp:**
```bash
cd backend
python main.py
```

---

## 🔐 CORS trong Production

### ⚠️ Không nên:

```python
# Cho phép TẤT CẢ origins (không an toàn!)
allow_origins=["*"]
```

### ✅ Nên:

```python
# Chỉ cho phép domain cụ thể
origins = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]
```

---

## 🧪 Test CORS

### Cách 1: Browser Console

Mở http://localhost:3000, nhấn F12, chạy:

```javascript
fetch('http://localhost:8000/')
  .then(res => res.json())
  .then(data => console.log('✅ CORS OK:', data))
  .catch(err => console.error('❌ CORS Error:', err))
```

### Cách 2: cURL (không bị CORS)

```bash
curl http://localhost:8000/
```

**Lưu ý:** cURL không bị CORS vì CORS chỉ áp dụng cho **trình duyệt**!

### Cách 3: Postman (không bị CORS)

Postman cũng không bị CORS vì không phải trình duyệt.

---

## 📚 Tài nguyên tham khảo

- [MDN - CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [FastAPI CORS Middleware](https://fastapi.tiangolo.com/tutorial/cors/)
- [Vue.js + API Integration](https://vuejs.org/guide/extras/ways-of-using-vue.html#fullstack-spa)

---

## 🆘 Vẫn gặp lỗi CORS?

Xem file **TEST_CORS.md** để debug chi tiết!

```bash
cat TEST_CORS.md
```

---

**Tóm lại:**
- CORS = Bảo mật của trình duyệt
- Backend phải cho phép frontend gọi API
- Đã cấu hình xong trong dự án này! ✅
