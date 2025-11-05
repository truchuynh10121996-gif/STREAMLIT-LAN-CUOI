# 🧪 HƯỚNG DẪN TEST CORS

## ✅ Kiểm tra CORS đã hoạt động chưa

### Bước 1: Chạy Backend và Frontend

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```
Chờ thấy: `Uvicorn running on http://0.0.0.0:8000`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
Chờ thấy: `Local: http://localhost:3000/`

### Bước 2: Test API trực tiếp

Mở trình duyệt và vào: http://localhost:8000

Bạn sẽ thấy:
```json
{
  "message": "Credit Risk Assessment API",
  "version": "1.0.0",
  "status": "running"
}
```

### Bước 3: Test CORS từ Frontend

1. Mở: http://localhost:3000
2. Mở **DevTools** (F12)
3. Vào tab **Console**
4. Chạy lệnh:

```javascript
fetch('http://localhost:8000/')
  .then(res => res.json())
  .then(data => console.log('✅ CORS OK:', data))
  .catch(err => console.error('❌ CORS Error:', err))
```

Nếu thấy `✅ CORS OK:` → **CORS hoạt động tốt!**

Nếu thấy lỗi CORS → Xem phần debug bên dưới

---

## 🐛 Debug lỗi CORS

### Lỗi phổ biến 1: "Access-Control-Allow-Origin"

```
Access to fetch at 'http://localhost:8000/...' from origin 'http://localhost:3000'
has been blocked by CORS policy
```

**Nguyên nhân:** Backend chưa cho phép origin của frontend

**Giải pháp:**
1. Kiểm tra backend/main.py đã có cấu hình CORS:
```python
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    ...
)
```

2. Restart backend sau khi sửa:
```bash
# Ctrl+C để dừng backend
python main.py
```

### Lỗi phổ biến 2: Port không khớp

**Nguyên nhân:** Frontend chạy ở port khác 3000

**Kiểm tra:**
```bash
# Xem frontend đang chạy ở port nào
npm run dev
```

Nếu thấy: `http://localhost:5173` thay vì `http://localhost:3000`

**Giải pháp:**
- Thêm port 5173 vào `origins` trong backend/main.py (đã có sẵn)
- Hoặc cấu hình frontend chạy ở port 3000 trong vite.config.js (đã có sẵn)

### Lỗi phổ biến 3: Backend không chạy

**Triệu chứng:** `net::ERR_CONNECTION_REFUSED`

**Giải pháp:**
1. Kiểm tra backend có chạy không:
```bash
curl http://localhost:8000
```

2. Nếu không có phản hồi, chạy lại backend:
```bash
cd backend
python main.py
```

---

## 🔍 Test từng endpoint

### Test /train (POST)

Trong console browser (F12):

```javascript
const formData = new FormData();
const file = new File(["X_1,X_2,...,default\n0.1,0.2,...,0"], "test.csv");
formData.append('file', file);

fetch('http://localhost:8000/train', {
  method: 'POST',
  body: formData
})
.then(res => res.json())
.then(data => console.log('✅ Train OK:', data))
.catch(err => console.error('❌ Train Error:', err))
```

### Test /predict (POST)

```javascript
fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    X_1: 0.025, X_2: 0.191, X_3: 0.160, X_4: 0.214,
    X_5: 0.297, X_6: 0.424, X_7: 2.662, X_8: 1.838,
    X_9: 25.833, X_10: -0.434, X_11: 0.353, X_12: 4.236,
    X_13: 82.317, X_14: 0.840
  })
})
.then(res => res.json())
.then(data => console.log('✅ Predict OK:', data))
.catch(err => console.error('❌ Predict Error:', err))
```

---

## 📋 Checklist CORS hoạt động

- [ ] Backend chạy tại http://localhost:8000
- [ ] Frontend chạy tại http://localhost:3000
- [ ] Mở http://localhost:8000 thấy JSON response
- [ ] Mở http://localhost:3000 thấy giao diện Vue
- [ ] Console không có lỗi CORS
- [ ] Test fetch từ console thành công
- [ ] Upload file CSV thành công
- [ ] Dự báo PD thành công

---

## 🎯 Cấu hình CORS hiện tại

### Backend (backend/main.py)

```python
origins = [
    "http://localhost:3000",      # Vue dev server
    "http://localhost:5173",      # Vite alternative port
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)
```

### Frontend (frontend/src/App.vue)

```javascript
const API_BASE = 'http://localhost:8000'
```

---

## 🚀 Nếu vẫn không được

1. **Clear browser cache**: Ctrl+Shift+Delete
2. **Hard reload**: Ctrl+Shift+R
3. **Thử trình duyệt khác** (Chrome, Firefox, Edge)
4. **Tắt extension** (AdBlock, Privacy Badger có thể chặn request)
5. **Kiểm tra firewall** có chặn port 8000 không

---

**Chúc bạn thành công! ✨**
