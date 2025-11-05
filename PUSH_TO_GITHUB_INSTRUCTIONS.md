# 🚀 Hướng dẫn Push Credit Risk App lên GitHub Repository Mới

## Thông tin Repository
- **Repository URL**: https://github.com/truchuynh10121996-gif/FAST-API-TH
- **Repository Name**: FAST-API-TH
- **Branch**: main

---

## Cách 1: Sử dụng Archive File (Đơn giản nhất - Khuyến nghị)

### Bước 1: Download archive file
File đã được đóng gói sẵn: `credit-risk-app-standalone.tar.gz`

### Bước 2: Extract và push lên GitHub

```bash
# Tạo thư mục tạm
mkdir -p ~/temp-credit-risk
cd ~/temp-credit-risk

# Copy và extract file archive (thay đổi đường dẫn nếu cần)
cp /path/to/credit-risk-app-standalone.tar.gz .
tar -xzf credit-risk-app-standalone.tar.gz

# Kiểm tra nội dung
ls -la

# Repository đã được cấu hình sẵn, chỉ cần push
git push -u origin main
```

### Bước 3: Nhập credentials khi được yêu cầu
- **Username**: `truchuynh10121996-gif`
- **Password**: Sử dụng **Personal Access Token** thay vì mật khẩu thông thường

**Tạo Personal Access Token:**
1. Truy cập: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Chọn quyền: `repo` (full control)
4. Copy token và sử dụng làm password khi git yêu cầu

---

## Cách 2: Clone từ thư mục credit-risk-app hiện có

```bash
# Di chuyển vào thư mục STREAMLIT-LAN-CUOI
cd /path/to/STREAMLIT-LAN-CUOI

# Tạo bản sao độc lập
cp -r credit-risk-app ~/credit-risk-standalone
cd ~/credit-risk-standalone

# Xóa git history cũ (nếu có)
rm -rf .git

# Khởi tạo git mới
git init
git branch -m main

# Add và commit
git add .
git commit -m "🎉 Initial commit: Credit Risk Assessment System

- FastAPI backend with ML model integration
- Vue.js frontend with interactive UI
- Complete CORS configuration
- Automated startup scripts
- Comprehensive documentation"

# Add remote và push
git remote add origin https://github.com/truchuynh10121996-gif/FAST-API-TH.git
git push -u origin main
```

---

## Cách 3: Sử dụng GitHub Desktop (Dễ nhất cho người mới)

1. Download GitHub Desktop: https://desktop.github.com/
2. Đăng nhập với tài khoản GitHub của bạn
3. File → Add Local Repository → chọn thư mục đã extract
4. Publish repository hoặc push to existing remote
5. Nhập URL: `https://github.com/truchuynh10121996-gif/FAST-API-TH.git`

---

## Kiểm tra sau khi push thành công

1. Truy cập: https://github.com/truchuynh10121996-gif/FAST-API-TH
2. Bạn sẽ thấy toàn bộ code với cấu trúc:
   ```
   FAST-API-TH/
   ├── backend/
   │   ├── main.py
   │   ├── model.py
   │   ├── gemini_api.py
   │   └── requirements.txt
   ├── frontend/
   │   ├── src/
   │   ├── package.json
   │   └── vite.config.js
   ├── README.md
   ├── start.sh
   └── start.bat
   ```

---

## Troubleshooting

### Lỗi: Authentication failed
**Giải pháp**: Sử dụng Personal Access Token thay vì password

### Lỗi: Repository not found
**Giải pháp**: Kiểm tra lại URL repository và đảm bảo bạn có quyền truy cập

### Lỗi: Permission denied
**Giải pháp**: Đảm bảo bạn đã đăng nhập với tài khoản `truchuynh10121996-gif`

---

## File đã chuẩn bị sẵn
- ✅ `credit-risk-app-standalone.tar.gz` - Archive file chứa toàn bộ code
- ✅ Git repository đã được khởi tạo với commit đầu tiên
- ✅ Remote origin đã được cấu hình sẵn

**Bạn chỉ cần extract và push!**

---

## Liên hệ hỗ trợ
Nếu gặp vấn đề, vui lòng kiểm tra:
1. Git đã được cài đặt: `git --version`
2. Đã đăng nhập GitHub
3. Có quyền truy cập repository
