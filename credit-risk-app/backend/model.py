"""
Model Module - Stacking Classifier cho Đánh giá Rủi ro Tín dụng
Sử dụng 3 Base Models: Logistic Regression + Random Forest + XGBoost
Meta-model: Logistic Regression
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from xgboost import XGBClassifier
import pickle
import os
from typing import Dict, Tuple, Any

# Danh sách 14 chỉ số tài chính
MODEL_COLS = [f'X_{i}' for i in range(1, 15)]


class CreditRiskModel:
    """Class quản lý mô hình Stacking Classifier cho đánh giá rủi ro tín dụng"""

    def __init__(self):
        self.model = None
        self.model_logistic = None
        self.model_rf = None
        self.model_xgb = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.metrics_in = {}
        self.metrics_out = {}

    def build_model(self):
        """Xây dựng mô hình Stacking Classifier"""
        # Định nghĩa 3 Base Models
        self.model_logistic = LogisticRegression(
            random_state=42,
            max_iter=1000,
            class_weight="balanced",
            solver="lbfgs"
        )

        self.model_rf = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=10,
            class_weight="balanced"
        )

        self.model_xgb = XGBClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=6,
            learning_rate=0.1,
            use_label_encoder=False,
            eval_metric='logloss'
        )

        # Tạo StackingClassifier với LogisticRegression làm meta-model
        estimators = [
            ('logistic', self.model_logistic),
            ('random_forest', self.model_rf),
            ('xgboost', self.model_xgb)
        ]

        self.model = StackingClassifier(
            estimators=estimators,
            final_estimator=LogisticRegression(random_state=42, max_iter=1000),
            cv=5,  # Cross-validation 5-fold
            stack_method='predict_proba',  # Dùng probability để stack
            n_jobs=-1  # Sử dụng tất cả CPU cores
        )

    def train(self, csv_file_path: str) -> Dict[str, Any]:
        """
        Huấn luyện mô hình từ file CSV

        Args:
            csv_file_path: Đường dẫn đến file CSV chứa dữ liệu huấn luyện

        Returns:
            Dict chứa metrics và thông tin huấn luyện
        """
        # Đọc dữ liệu
        df = pd.read_csv(csv_file_path)

        # Kiểm tra cột cần thiết
        required_cols = ['default'] + MODEL_COLS
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            raise ValueError(f"Thiếu cột: {missing}. Vui lòng kiểm tra lại file CSV.")

        # Chuẩn bị dữ liệu
        X = df[MODEL_COLS]
        y = df['default'].astype(int)

        # Chia train/test
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Xây dựng mô hình
        self.build_model()

        # Train mô hình Stacking
        print("🚀 Đang huấn luyện mô hình Stacking Classifier...")
        self.model.fit(self.X_train, self.y_train)

        # Train riêng 3 base models để lấy PD riêng biệt
        print("🔧 Đang huấn luyện 3 base models riêng biệt...")
        self.model_logistic.fit(self.X_train, self.y_train)
        self.model_rf.fit(self.X_train, self.y_train)
        self.model_xgb.fit(self.X_train, self.y_train)

        # Đánh giá mô hình
        y_pred_in = self.model.predict(self.X_train)
        y_proba_in = self.model.predict_proba(self.X_train)[:, 1]
        y_pred_out = self.model.predict(self.X_test)
        y_proba_out = self.model.predict_proba(self.X_test)[:, 1]

        # Tính metrics
        self.metrics_in = {
            "accuracy": accuracy_score(self.y_train, y_pred_in),
            "precision": precision_score(self.y_train, y_pred_in, zero_division=0),
            "recall": recall_score(self.y_train, y_pred_in, zero_division=0),
            "f1": f1_score(self.y_train, y_pred_in, zero_division=0),
            "auc": roc_auc_score(self.y_train, y_proba_in),
        }

        self.metrics_out = {
            "accuracy": accuracy_score(self.y_test, y_pred_out),
            "precision": precision_score(self.y_test, y_pred_out, zero_division=0),
            "recall": recall_score(self.y_test, y_pred_out, zero_division=0),
            "f1": f1_score(self.y_test, y_pred_out, zero_division=0),
            "auc": roc_auc_score(self.y_test, y_proba_out),
        }

        print("✅ Huấn luyện hoàn tất!")

        return {
            "status": "success",
            "message": "Mô hình đã được huấn luyện thành công!",
            "train_samples": len(self.X_train),
            "test_samples": len(self.X_test),
            "metrics_train": self.metrics_in,
            "metrics_test": self.metrics_out
        }

    def predict(self, X_new: pd.DataFrame) -> Dict[str, Any]:
        """
        Dự báo PD cho dữ liệu mới

        Args:
            X_new: DataFrame chứa 14 chỉ số X_1 đến X_14

        Returns:
            Dict chứa PD từ 4 models và kết quả dự đoán
        """
        if self.model is None:
            raise ValueError("Mô hình chưa được huấn luyện. Vui lòng huấn luyện trước khi dự báo.")

        # Đảm bảo thứ tự cột đúng
        X_new = X_new[MODEL_COLS]

        # 1. PD từ Stacking Model (kết quả chính)
        probs_stacking = self.model.predict_proba(X_new)[:, 1]

        # 2. PD từ 3 Base Models
        probs_logistic = self.model_logistic.predict_proba(X_new)[:, 1]
        probs_rf = self.model_rf.predict_proba(X_new)[:, 1]
        probs_xgb = self.model_xgb.predict_proba(X_new)[:, 1]

        # Ngưỡng phân loại: PD >= 15% = Default
        preds = (probs_stacking >= 0.15).astype(int)

        return {
            "pd_stacking": float(probs_stacking[0]),
            "pd_logistic": float(probs_logistic[0]),
            "pd_random_forest": float(probs_rf[0]),
            "pd_xgboost": float(probs_xgb[0]),
            "prediction": int(preds[0]),
            "prediction_label": "Default (Vỡ nợ)" if preds[0] == 1 else "Non-Default (Không vỡ nợ)"
        }

    def save_model(self, filepath: str = "model_stacking.pkl"):
        """Lưu mô hình ra file"""
        if self.model is None:
            raise ValueError("Không có mô hình để lưu.")

        model_data = {
            "model": self.model,
            "model_logistic": self.model_logistic,
            "model_rf": self.model_rf,
            "model_xgb": self.model_xgb,
            "metrics_in": self.metrics_in,
            "metrics_out": self.metrics_out
        }

        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)

        print(f"✅ Mô hình đã được lưu tại: {filepath}")

    def load_model(self, filepath: str = "model_stacking.pkl"):
        """Load mô hình từ file"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Không tìm thấy file mô hình: {filepath}")

        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)

        self.model = model_data["model"]
        self.model_logistic = model_data["model_logistic"]
        self.model_rf = model_data["model_rf"]
        self.model_xgb = model_data["model_xgb"]
        self.metrics_in = model_data["metrics_in"]
        self.metrics_out = model_data["metrics_out"]

        print(f"✅ Mô hình đã được load từ: {filepath}")


# Khởi tạo instance global
credit_model = CreditRiskModel()
