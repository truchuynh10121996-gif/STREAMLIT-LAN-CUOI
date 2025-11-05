"""
Gemini API Module - Tích hợp Google Gemini để phân tích kết quả dự báo PD
"""

import os
from typing import Dict, Any
import google.generativeai as genai


class GeminiAnalyzer:
    """Class để tích hợp Gemini API phân tích kết quả dự báo rủi ro tín dụng"""

    def __init__(self, api_key: str = None):
        """
        Khởi tạo Gemini API

        Args:
            api_key: API key của Google Gemini. Nếu không truyền, sẽ lấy từ biến môi trường GEMINI_API_KEY
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Không tìm thấy GEMINI_API_KEY. Vui lòng cung cấp API key hoặc set biến môi trường.")

        # Cấu hình Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def analyze_credit_risk(self, prediction_data: Dict[str, Any]) -> str:
        """
        Phân tích kết quả dự báo rủi ro tín dụng bằng Gemini

        Args:
            prediction_data: Dict chứa thông tin dự báo (PD, chỉ số tài chính, v.v.)

        Returns:
            Kết quả phân tích dạng text từ Gemini
        """
        # Tạo prompt chi tiết
        prompt = self._create_analysis_prompt(prediction_data)

        try:
            # Gọi Gemini API
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Lỗi khi gọi Gemini API: {str(e)}"

    def _create_analysis_prompt(self, data: Dict[str, Any]) -> str:
        """
        Tạo prompt chi tiết để gửi tới Gemini

        Args:
            data: Dữ liệu dự báo

        Returns:
            Prompt string
        """
        pd_stacking = data.get('pd_stacking', 0) * 100
        pd_logistic = data.get('pd_logistic', 0) * 100
        pd_rf = data.get('pd_random_forest', 0) * 100
        pd_xgboost = data.get('pd_xgboost', 0) * 100
        prediction_label = data.get('prediction_label', 'N/A')

        # Phân loại rủi ro
        if pd_stacking < 5:
            risk_level = "RỦI RO THẤP 🟢"
            risk_desc = "doanh nghiệp có tình hình tài chính tốt"
        elif pd_stacking < 15:
            risk_level = "RỦI RO TRUNG BÌNH 🟡"
            risk_desc = "doanh nghiệp cần theo dõi thêm"
        else:
            risk_level = "RỦI RO CAO 🔴"
            risk_desc = "doanh nghiệp có nguy cơ vỡ nợ cao"

        prompt = f"""
Bạn là một chuyên gia phân tích rủi ro tín dụng của Agribank.

Dựa trên kết quả dự báo xác suất vỡ nợ (PD - Probability of Default) từ mô hình AI Stacking Classifier, hãy phân tích chi tiết và đưa ra khuyến nghị cho khách hàng doanh nghiệp.

**KẾT QUẢ DỰ BÁO:**
- Xác suất Vỡ nợ (PD) - Stacking Model: {pd_stacking:.2f}%
- Xác suất Vỡ nợ (PD) - Logistic Regression: {pd_logistic:.2f}%
- Xác suất Vỡ nợ (PD) - Random Forest: {pd_rf:.2f}%
- Xác suất Vỡ nợ (PD) - XGBoost: {pd_xgboost:.2f}%
- Dự đoán: {prediction_label}
- Mức độ rủi ro: {risk_level}

**YÊU CẦU PHÂN TÍCH:**

Hãy phân tích theo cấu trúc sau (bằng tiếng Việt, ngắn gọn, chuyên nghiệp):

1. **Tổng quan rủi ro**: Đánh giá chung về mức độ rủi ro tín dụng của doanh nghiệp này ({risk_desc})

2. **Phân tích chi tiết**:
   - So sánh kết quả PD từ 3 models (Logistic, Random Forest, XGBoost)
   - Giải thích sự khác biệt giữa các models (nếu có)
   - Mức độ đồng thuận giữa các models

3. **Khuyến nghị**:
   - Đối với Ngân hàng: Nên cho vay hay từ chối? Điều kiện nào cần thêm?
   - Đối với Doanh nghiệp: Cần cải thiện chỉ số nào để giảm rủi ro?

4. **Lưu ý**: Các yếu tố cần theo dõi thêm

Hãy trình bày ngắn gọn, rõ ràng, dễ hiểu, tối đa 300 từ.
"""

        return prompt


# Khởi tạo instance global
gemini_analyzer = None


def get_gemini_analyzer(api_key: str = None) -> GeminiAnalyzer:
    """
    Lấy instance của GeminiAnalyzer (singleton pattern)

    Args:
        api_key: API key của Gemini

    Returns:
        GeminiAnalyzer instance
    """
    global gemini_analyzer
    if gemini_analyzer is None:
        gemini_analyzer = GeminiAnalyzer(api_key)
    return gemini_analyzer
