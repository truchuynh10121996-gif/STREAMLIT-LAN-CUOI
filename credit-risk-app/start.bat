@echo off
REM Script khởi động Backend và Frontend trên Windows

echo 🚀 Đang khởi động Hệ thống Đánh giá Rủi ro Tín dụng...
echo.

REM Kiểm tra có trong thư mục credit-risk-app không
if not exist "backend\" (
    echo ❌ Lỗi: Vui lòng chạy script này từ thư mục credit-risk-app\
    echo    cd credit-risk-app ^&^& start.bat
    pause
    exit /b 1
)

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Lỗi: Python chưa được cài đặt hoặc không trong PATH
    echo    Tải Python tại: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Kiểm tra Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Lỗi: Node.js chưa được cài đặt hoặc không trong PATH
    echo    Tải Node.js tại: https://nodejs.org/
    pause
    exit /b 1
)

echo 📦 Kiểm tra dependencies...

REM Backend
if not exist "backend\venv\" (
    echo 📥 Tạo Python virtual environment...
    cd backend
    python -m venv venv
    cd ..
)

echo 📥 Cài đặt backend dependencies...
cd backend
call venv\Scripts\activate
pip install -q -r requirements.txt
cd ..

REM Frontend
if not exist "frontend\node_modules\" (
    echo 📥 Cài đặt frontend dependencies...
    cd frontend
    call npm install
    cd ..
)

echo.
echo ✅ Dependencies đã sẵn sàng!
echo.

REM Khởi động Backend
echo 🔧 Đang khởi động Backend (FastAPI)...
cd backend
start "Backend-FastAPI" cmd /k "venv\Scripts\activate && python main.py"
cd ..
timeout /t 3 /nobreak >nul

REM Khởi động Frontend
echo 🎨 Đang khởi động Frontend (Vue 3)...
cd frontend
start "Frontend-Vue3" cmd /k "npm run dev"
cd ..
timeout /t 3 /nobreak >nul

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 🎉 Hệ thống đã sẵn sàng!
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 🌐 Frontend: http://localhost:3000
echo 🔌 Backend:  http://localhost:8000
echo.
echo 📝 2 cửa sổ terminal mới đã được mở:
echo    - Backend-FastAPI (Python)
echo    - Frontend-Vue3 (Node.js)
echo.
echo ⚠️  Đóng các cửa sổ terminal để dừng service
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM Mở trình duyệt
timeout /t 2 /nobreak >nul
start http://localhost:3000

pause
