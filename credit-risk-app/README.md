# 🏦 Hệ thống Đánh giá Rủi ro Tín dụng Doanh nghiệp - Agribank

Ứng dụng web hiện đại đánh giá rủi ro tín dụng sử dụng **Stacking Classifier** (Logistic Regression + Random Forest + XGBoost) với giao diện **Vue 3** và backend **FastAPI**.

## 🌟 Tính năng

- ✅ **Huấn luyện mô hình AI** từ file CSV (14 chỉ số tài chính)
- ✅ **Dự báo xác suất vỡ nợ (PD)** cho doanh nghiệp
- ✅ **4 Models dự báo**: Stacking, Logistic, Random Forest, XGBoost
- ✅ **Biểu đồ bar** so sánh PD từ 4 models với màu sắc theo ngưỡng
- ✅ **Phân tích bằng Gemini AI** - Giải thích kết quả và đưa ra khuyến nghị
- ✅ **Giao diện pastel ngọt ngào** với logo Agribank

## 🎨 Màu sắc theo ngưỡng PD

- 🟢 **Xanh**: PD < 5% → Rủi ro Thấp
- 🟡 **Vàng**: 5% ≤ PD < 15% → Rủi ro Trung bình
- 🔴 **Đỏ**: PD ≥ 15% → Rủi ro Cao

## 📁 Cấu trúc Dự án

```
credit-risk-app/
├── backend/              # FastAPI Backend
│   ├── main.py          # API endpoints
│   ├── model.py         # Stacking Model logic
│   ├── gemini_api.py    # Gemini AI integration
│   ├── requirements.txt # Python dependencies
│   └── .env.example     # Environment variables template
├── frontend/            # Vue 3 Frontend
│   ├── src/
│   │   ├── App.vue      # Main component
│   │   ├── components/
│   │   │   └── RiskChart.vue  # Chart component
│   │   ├── main.js
│   │   └── style.css    # Pastel theme CSS
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 🚀 Hướng dẫn Cài đặt và Chạy

### Yêu cầu hệ thống

- Python 3.8+
- Node.js 16+ và npm
- VS Code (khuyến nghị)

### Bước 1: Cài đặt Backend (FastAPI)

```bash
# Di chuyển vào thư mục backend
cd credit-risk-app/backend

# Tạo môi trường ảo Python (khuyến nghị)
python -m venv venv

# Kích hoạt môi trường ảo
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt

# (Tùy chọn) Tạo file .env và thêm Gemini API Key
# Sao chép .env.example thành .env và điền API key
cp .env.example .env
# Chỉnh sửa .env và thêm: GEMINI_API_KEY=your_api_key_here
```

### Bước 2: Cài đặt Frontend (Vue 3)

```bash
# Mở terminal mới, di chuyển vào thư mục frontend
cd credit-risk-app/frontend

# Cài đặt dependencies
npm install
```

### Bước 3: Chạy Ứng dụng

**Terminal 1 - Backend:**

```bash
cd credit-risk-app/backend
# Kích hoạt venv nếu chưa
python main.py
# Hoặc: uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend sẽ chạy tại: `http://localhost:8000`

**Terminal 2 - Frontend:**

```bash
cd credit-risk-app/frontend
npm run dev
```

Frontend sẽ chạy tại: `http://localhost:3000`

### Bước 4: Mở trình duyệt

Truy cập: **http://localhost:3000**

## 📝 Hướng dẫn Sử dụng

### 1. Cấu hình Gemini API Key

- Lấy API key tại: https://makersuite.google.com/app/apikey
- Nhập API key vào form và click "Lưu API Key"
- Hoặc đặt trong file `.env` của backend

### 2. Huấn luyện Mô hình

- Click vào "Tải lên file CSV để huấn luyện mô hình"
- Chọn file CSV có cấu trúc:
  - 14 cột: `X_1, X_2, X_3, ..., X_14` (các chỉ số tài chính)
  - 1 cột: `default` (0 = Không vỡ nợ, 1 = Vỡ nợ)
- Click "🚀 Huấn luyện Mô hình"
- Đợi khoảng 10-30 giây để mô hình huấn luyện
- Kết quả sẽ hiển thị: số mẫu train/test, Accuracy, AUC

**Ví dụ file CSV:**

```csv
X_1,X_2,X_3,X_4,X_5,X_6,X_7,X_8,X_9,X_10,X_11,X_12,X_13,X_14,default
0.025,0.191,0.160,0.214,0.297,0.424,2.662,1.838,25.833,-0.434,0.353,4.236,82.317,0.840,0
0.042,0.045,0.039,0.055,0.298,0.425,2.368,1.720,3.162,-0.356,0.366,3.859,86.196,0.870,0
...
```

Bạn có thể sử dụng file **DATASET.csv** trong repo gốc để test.

### 3. Dự báo Rủi ro

- Nhập 14 chỉ số tài chính (X1 đến X14) vào form
- Click "🎯 Dự báo PD"
- Kết quả hiển thị:
  - 4 thẻ PD với màu sắc theo ngưỡng (Xanh/Vàng/Đỏ)
  - Biểu đồ bar so sánh PD từ 4 models
- Click "🤖 Phân tích bằng Gemini AI" để nhận phân tích chi tiết

## 🔌 API Endpoints (Backend)

### GET `/`
Health check

### POST `/train`
Huấn luyện mô hình từ file CSV
- **Body**: multipart/form-data với file CSV
- **Response**: Metrics (accuracy, AUC, v.v.)

### POST `/predict`
Dự báo PD từ 14 chỉ số
- **Body**: JSON với X_1 đến X_14
```json
{
  "X_1": 0.025,
  "X_2": 0.191,
  ...
  "X_14": 0.840
}
```
- **Response**: PD từ 4 models

### POST `/analyze`
Phân tích kết quả bằng Gemini
- **Body**: JSON kết quả từ `/predict`
- **Response**: Phân tích dạng text

### POST `/set-gemini-key`
Set Gemini API key
- **Body**: `{"api_key": "your_key"}`

### GET `/model-info`
Lấy thông tin mô hình hiện tại

## 🧪 Test với VS Code

### Mở dự án trong VS Code

```bash
code credit-risk-app
```

### Sử dụng VS Code Terminal

1. **Mở 2 Terminal split** (Ctrl + ` để mở terminal)
2. **Terminal 1**: Chạy backend
3. **Terminal 2**: Chạy frontend

### Debug Backend (Python)

Tạo file `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI Backend",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
      "cwd": "${workspaceFolder}/backend",
      "env": {
        "GEMINI_API_KEY": "your_api_key_here"
      }
    }
  ]
}
```

## 📊 Mô hình AI - Stacking Classifier

### Kiến trúc

```
┌─────────────────────────────────────────┐
│         INPUT: 14 Chỉ số (X1-X14)      │
└────────────────┬────────────────────────┘
                 │
        ┌────────┴────────┐
        │  LAYER 1 (Base) │
        └────────┬────────┘
                 │
   ┌─────────────┼─────────────┐
   │             │             │
┌──▼───┐   ┌────▼────┐   ┌───▼────┐
│ LR   │   │   RF    │   │  XGB   │
└──┬───┘   └────┬────┘   └───┬────┘
   │            │            │
   └────────────┼────────────┘
                │
        ┌───────▼────────┐
        │ LAYER 2 (Meta) │
        │  Logistic Reg  │
        └───────┬────────┘
                │
        ┌───────▼────────┐
        │   OUTPUT: PD   │
        └────────────────┘
```

### 3 Base Models

1. **Logistic Regression**: Mô hình tuyến tính đơn giản, dễ giải thích
2. **Random Forest**: Ensemble của nhiều decision trees, chống overfitting
3. **XGBoost**: Gradient boosting mạnh mẽ, độ chính xác cao

### Meta-model

- **Logistic Regression**: Kết hợp kết quả từ 3 base models để cho ra dự báo cuối cùng

## 🎨 Giao diện

- **Theme**: Pastel ngọt ngào (hồng, xanh, tím nhạt)
- **Logo Agribank**: Góc trên trái
- **Responsive**: Tương thích mobile và desktop
- **Animations**: Hover effects, smooth transitions

## 🐛 Troubleshooting

### Lỗi: "Mô hình chưa được huấn luyện"
- Đảm bảo bạn đã upload CSV và huấn luyện mô hình trước khi dự báo

### Lỗi: "Không tìm thấy GEMINI_API_KEY"
- Set API key qua giao diện hoặc file `.env`

### Port đã được sử dụng
- Backend (8000): Đổi port trong `main.py` hoặc `uvicorn --port 8001`
- Frontend (3000): Đổi port trong `vite.config.js`

### Module not found
- Backend: `pip install -r requirements.txt`
- Frontend: `npm install`

## 📚 Tài liệu tham khảo

- **FastAPI**: https://fastapi.tiangolo.com/
- **Vue 3**: https://vuejs.org/
- **Scikit-learn**: https://scikit-learn.org/
- **XGBoost**: https://xgboost.readthedocs.io/
- **Gemini API**: https://ai.google.dev/

## 👨‍💻 Tác giả

Phát triển bởi Claude với yêu cầu từ người dùng.

## 📄 License

MIT License - Tự do sử dụng cho mục đích học tập và thương mại.

---

**Chúc bạn sử dụng thành công! 🎉**

Nếu có lỗi, vui lòng mở issue trên GitHub repo.
