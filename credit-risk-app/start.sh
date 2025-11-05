#!/bin/bash

# Script khởi động Backend và Frontend

echo "🚀 Đang khởi động Hệ thống Đánh giá Rủi ro Tín dụng..."
echo ""

# Kiểm tra có trong thư mục credit-risk-app không
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Lỗi: Vui lòng chạy script này từ thư mục credit-risk-app/"
    echo "   cd credit-risk-app && ./start.sh"
    exit 1
fi

# Hàm dọn dẹp khi thoát
cleanup() {
    echo ""
    echo "🛑 Đang dừng các service..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Kiểm tra và cài đặt dependencies
echo "📦 Kiểm tra dependencies..."

# Backend
if [ ! -d "backend/venv" ]; then
    echo "📥 Tạo Python virtual environment..."
    cd backend
    python -m venv venv
    cd ..
fi

echo "📥 Cài đặt backend dependencies..."
cd backend
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi
pip install -q -r requirements.txt
cd ..

# Frontend
if [ ! -d "frontend/node_modules" ]; then
    echo "📥 Cài đặt frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

echo ""
echo "✅ Dependencies đã sẵn sàng!"
echo ""

# Khởi động Backend
echo "🔧 Đang khởi động Backend (FastAPI)..."
cd backend
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi
python main.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..
sleep 3

if ps -p $BACKEND_PID > /dev/null; then
    echo "✅ Backend đang chạy tại: http://localhost:8000 (PID: $BACKEND_PID)"
else
    echo "❌ Lỗi khởi động Backend. Kiểm tra backend.log"
    cat backend.log
    exit 1
fi

# Khởi động Frontend
echo "🎨 Đang khởi động Frontend (Vue 3)..."
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..
sleep 3

if ps -p $FRONTEND_PID > /dev/null; then
    echo "✅ Frontend đang chạy tại: http://localhost:3000 (PID: $FRONTEND_PID)"
else
    echo "❌ Lỗi khởi động Frontend. Kiểm tra frontend.log"
    cat frontend.log
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 Hệ thống đã sẵn sàng!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔌 Backend:  http://localhost:8000"
echo ""
echo "📝 Logs:"
echo "   Backend:  tail -f backend.log"
echo "   Frontend: tail -f frontend.log"
echo ""
echo "⚠️  Nhấn Ctrl+C để dừng tất cả service"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Giữ script chạy
wait
