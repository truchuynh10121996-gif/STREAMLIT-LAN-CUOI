<template>
  <div id="app">
    <!-- Header -->
    <header class="header">
      <div class="logo-container">
        <img
          src="https://upload.wikimedia.org/wikipedia/commons/9/93/Logo_Agribank.svg"
          alt="Agribank Logo"
          class="logo"
        />
      </div>
      <h1 class="app-title">🏦 Hệ thống Đánh giá Rủi ro Tín dụng Doanh nghiệp</h1>
    </header>

    <!-- Main Container -->
    <div class="container">
      <!-- API Key Section -->
      <div class="card" v-if="!geminiKeySet">
        <h2 class="card-title">🔑 Cấu hình Gemini API Key</h2>
        <div class="input-group">
          <label class="input-label">Nhập Gemini API Key của bạn:</label>
          <input
            v-model="geminiApiKey"
            type="password"
            class="input-field"
            placeholder="AIzaSy..."
          />
        </div>
        <button @click="setGeminiKey" class="btn btn-primary" :disabled="!geminiApiKey">
          Lưu API Key
        </button>
        <p class="upload-hint" style="margin-top: 1rem;">
          Lấy API key tại: <a href="https://makersuite.google.com/app/apikey" target="_blank">https://makersuite.google.com/app/apikey</a>
        </p>
      </div>

      <!-- Training Section -->
      <div class="card">
        <h2 class="card-title">📚 Bước 1: Huấn luyện Mô hình</h2>
        <div class="upload-area" @click="$refs.trainFileInput.click()">
          <div class="upload-icon">📤</div>
          <p class="upload-text">{{ trainFileName || 'Tải lên file CSV để huấn luyện mô hình' }}</p>
          <p class="upload-hint">File CSV cần có 14 cột (X_1 đến X_14) và cột 'default' (0 hoặc 1)</p>
        </div>
        <input
          ref="trainFileInput"
          type="file"
          accept=".csv"
          @change="handleTrainFile"
          style="display: none"
        />
        <button
          @click="trainModel"
          class="btn btn-primary"
          :disabled="!trainFile || isTraining"
          style="margin-top: 1rem; width: 100%;"
        >
          {{ isTraining ? 'Đang huấn luyện...' : '🚀 Huấn luyện Mô hình' }}
        </button>

        <!-- Training Results -->
        <div v-if="trainResult" style="margin-top: 2rem;">
          <h3 style="color: var(--agribank-green); margin-bottom: 1rem;">✅ Kết quả Huấn luyện</h3>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
            <div class="pd-card risk-low">
              <div class="pd-label">Số mẫu Train</div>
              <div class="pd-value" style="font-size: 1.5rem;">{{ trainResult.train_samples }}</div>
            </div>
            <div class="pd-card risk-low">
              <div class="pd-label">Số mẫu Test</div>
              <div class="pd-value" style="font-size: 1.5rem;">{{ trainResult.test_samples }}</div>
            </div>
            <div class="pd-card risk-low">
              <div class="pd-label">Accuracy (Test)</div>
              <div class="pd-value" style="font-size: 1.5rem;">{{ (trainResult.metrics_test.accuracy * 100).toFixed(2) }}%</div>
            </div>
            <div class="pd-card risk-low">
              <div class="pd-label">AUC (Test)</div>
              <div class="pd-value" style="font-size: 1.5rem;">{{ (trainResult.metrics_test.auc * 100).toFixed(2) }}%</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Prediction Section -->
      <div class="card">
        <h2 class="card-title">🔮 Bước 2: Dự báo Rủi ro Tín dụng</h2>

        <!-- Manual Input Form -->
        <div style="margin-bottom: 2rem;">
          <h3 style="margin-bottom: 1rem; color: var(--agribank-green);">Nhập 14 Chỉ số Tài chính (X1 - X14)</h3>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
            <div v-for="i in 14" :key="i" class="input-group">
              <label class="input-label">X{{ i }}</label>
              <input
                v-model.number="inputData[`X_${i}`]"
                type="number"
                step="0.000001"
                class="input-field"
                placeholder="0.0"
              />
            </div>
          </div>
          <button
            @click="predict"
            class="btn btn-primary"
            :disabled="!isInputValid || isPredicting"
            style="margin-top: 1rem; width: 100%;"
          >
            {{ isPredicting ? 'Đang dự báo...' : '🎯 Dự báo PD' }}
          </button>
        </div>

        <!-- Prediction Results -->
        <div v-if="predictionResult">
          <h3 style="margin-bottom: 1.5rem; color: var(--agribank-green);">📊 Kết quả Dự báo</h3>

          <!-- PD Cards -->
          <div class="pd-grid">
            <div
              class="pd-card"
              :class="getRiskClass(predictionResult.pd_stacking)"
            >
              <div class="pd-label">🎯 PD - Stacking (Kết quả chính)</div>
              <div class="pd-value">{{ (predictionResult.pd_stacking * 100).toFixed(2) }}%</div>
              <div class="pd-status">{{ getRiskLabel(predictionResult.pd_stacking) }}</div>
            </div>

            <div
              class="pd-card"
              :class="getRiskClass(predictionResult.pd_logistic)"
            >
              <div class="pd-label">📈 PD - Logistic Regression</div>
              <div class="pd-value">{{ (predictionResult.pd_logistic * 100).toFixed(2) }}%</div>
              <div class="pd-status">{{ getRiskLabel(predictionResult.pd_logistic) }}</div>
            </div>

            <div
              class="pd-card"
              :class="getRiskClass(predictionResult.pd_random_forest)"
            >
              <div class="pd-label">🌳 PD - Random Forest</div>
              <div class="pd-value">{{ (predictionResult.pd_random_forest * 100).toFixed(2) }}%</div>
              <div class="pd-status">{{ getRiskLabel(predictionResult.pd_random_forest) }}</div>
            </div>

            <div
              class="pd-card"
              :class="getRiskClass(predictionResult.pd_xgboost)"
            >
              <div class="pd-label">⚡ PD - XGBoost</div>
              <div class="pd-value">{{ (predictionResult.pd_xgboost * 100).toFixed(2) }}%</div>
              <div class="pd-status">{{ getRiskLabel(predictionResult.pd_xgboost) }}</div>
            </div>
          </div>

          <!-- Chart -->
          <div class="chart-container">
            <RiskChart :prediction="predictionResult" />
          </div>

          <!-- Gemini Analysis -->
          <div v-if="geminiKeySet">
            <button
              @click="analyzeWithGemini"
              class="btn btn-primary"
              :disabled="isAnalyzing"
              style="width: 100%; margin-top: 1rem;"
            >
              {{ isAnalyzing ? 'Đang phân tích...' : '🤖 Phân tích bằng Gemini AI' }}
            </button>

            <div v-if="geminiAnalysis" class="analysis-box">
              <h3 style="margin-bottom: 1rem; color: var(--agribank-green);">🧠 Phân tích từ Gemini AI</h3>
              {{ geminiAnalysis }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import axios from 'axios'
import RiskChart from './components/RiskChart.vue'

export default {
  name: 'App',
  components: {
    RiskChart
  },
  setup() {
    // State
    const geminiApiKey = ref('')
    const geminiKeySet = ref(false)
    const trainFile = ref(null)
    const trainFileName = ref('')
    const isTraining = ref(false)
    const trainResult = ref(null)

    const inputData = ref({
      X_1: null, X_2: null, X_3: null, X_4: null, X_5: null,
      X_6: null, X_7: null, X_8: null, X_9: null, X_10: null,
      X_11: null, X_12: null, X_13: null, X_14: null
    })

    const isPredicting = ref(false)
    const predictionResult = ref(null)
    const isAnalyzing = ref(false)
    const geminiAnalysis = ref('')

    // API Base URL
    const API_BASE = 'http://localhost:8000'

    // Computed
    const isInputValid = computed(() => {
      return Object.values(inputData.value).every(v => v !== null && v !== '')
    })

    // Methods
    const setGeminiKey = async () => {
      try {
        await axios.post(`${API_BASE}/set-gemini-key`, {
          api_key: geminiApiKey.value
        })
        geminiKeySet.value = true
        alert('✅ Gemini API Key đã được lưu thành công!')
      } catch (error) {
        alert('❌ Lỗi khi lưu API Key: ' + error.message)
      }
    }

    const handleTrainFile = (event) => {
      const file = event.target.files[0]
      if (file) {
        trainFile.value = file
        trainFileName.value = file.name
      }
    }

    const trainModel = async () => {
      if (!trainFile.value) return

      isTraining.value = true
      trainResult.value = null

      try {
        const formData = new FormData()
        formData.append('file', trainFile.value)

        const response = await axios.post(`${API_BASE}/train`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })

        trainResult.value = response.data
        alert('✅ Huấn luyện mô hình thành công!')
      } catch (error) {
        alert('❌ Lỗi khi huấn luyện: ' + (error.response?.data?.detail || error.message))
      } finally {
        isTraining.value = false
      }
    }

    const predict = async () => {
      if (!isInputValid.value) return

      isPredicting.value = true
      predictionResult.value = null
      geminiAnalysis.value = ''

      try {
        const response = await axios.post(`${API_BASE}/predict`, inputData.value)
        predictionResult.value = response.data
      } catch (error) {
        alert('❌ Lỗi khi dự báo: ' + (error.response?.data?.detail || error.message))
      } finally {
        isPredicting.value = false
      }
    }

    const analyzeWithGemini = async () => {
      if (!predictionResult.value) return

      isAnalyzing.value = true
      geminiAnalysis.value = ''

      try {
        const response = await axios.post(`${API_BASE}/analyze`, predictionResult.value)
        geminiAnalysis.value = response.data.analysis
      } catch (error) {
        alert('❌ Lỗi khi phân tích bằng Gemini: ' + (error.response?.data?.detail || error.message))
      } finally {
        isAnalyzing.value = false
      }
    }

    const getRiskClass = (pd) => {
      if (pd < 0.05) return 'risk-low'
      if (pd < 0.15) return 'risk-medium'
      return 'risk-high'
    }

    const getRiskLabel = (pd) => {
      if (pd < 0.05) return '🟢 Rủi ro Thấp'
      if (pd < 0.15) return '🟡 Rủi ro Trung bình'
      return '🔴 Rủi ro Cao'
    }

    return {
      geminiApiKey,
      geminiKeySet,
      trainFile,
      trainFileName,
      isTraining,
      trainResult,
      inputData,
      isInputValid,
      isPredicting,
      predictionResult,
      isAnalyzing,
      geminiAnalysis,
      setGeminiKey,
      handleTrainFile,
      trainModel,
      predict,
      analyzeWithGemini,
      getRiskClass,
      getRiskLabel
    }
  }
}
</script>
