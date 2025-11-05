# 🚀 HƯỚNG DẪN CHẠY NHANH

## 🎯 CÁCH NHANH NHẤT (Khuyến nghị)

### Linux / macOS:

```bash
cd credit-risk-app
./start.sh
```

### Windows:

```bash
cd credit-risk-app
start.bat
```

Script sẽ tự động:
- Tạo virtual environment cho Python
- Cài đặt tất cả dependencies (backend + frontend)
- Chạy Backend tại http://localhost:8000
- Chạy Frontend tại http://localhost:3000
- Mở trình duyệt

**Nhấn Ctrl+C để dừng tất cả service**

---

## 📝 CÁCH CHẠY THỦ CÔNG

### Bước 1: Cài đặt Backend

Mở Terminal 1 trong VS Code:

```bash
cd credit-risk-app/backend

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy server
python main.py
```

✅ Backend chạy tại: **http://localhost:8000**

### Bước 2: Cài đặt Frontend

Mở Terminal 2 trong VS Code:

```bash
cd credit-risk-app/frontend

# Cài đặt dependencies
npm install

# Chạy dev server
npm run dev
```

✅ Frontend chạy tại: **http://localhost:3000**

### Bước 3: Truy cập ứng dụng

Mở trình duyệt: **http://localhost:3000**

## Bước 4: Sử dụng

1. **Nhập Gemini API Key** (nếu muốn dùng AI phân tích):
   - Lấy tại: https://makersuite.google.com/app/apikey
   - Paste vào form và click "Lưu API Key"

2. **Huấn luyện mô hình**:
   - Click "Tải lên file CSV"
   - Chọn file `DATASET.csv` trong thư mục `credit-risk-app/`
   - Click "🚀 Huấn luyện Mô hình"
   - Đợi 10-30 giây

3. **Dự báo PD**:
   - Nhập 14 chỉ số tài chính (X1-X14)
   - Click "🎯 Dự báo PD"
   - Xem kết quả với màu sắc và biểu đồ

4. **Phân tích bằng AI**:
   - Click "🤖 Phân tích bằng Gemini AI"
   - Đọc phân tích và khuyến nghị

---

**Chúc bạn thành công! 🎉**
