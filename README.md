# Project 1: Thai Text Classification for Depression Detection
## โครงงานการประมวลผลภาษาธรรมชาติ (Natural Language Processing - NLP) | กลุ่มที่ 10 (Group 10)

ระบบจำแนกข้อความภาษาไทยเพื่อคัดกรองภาวะซึมเศร้า (Binary Text Classification) โดยเปรียบเทียบสถาปัตยกรรม Deep Learning (BiLSTM + Word2Vec) และโมเดล Machine Learning (Logistic Regression BoW/TF-IDF, Decision Tree)

---

## 📊 ผลการทดลองบนชุดทดสอบ (Test Set: 4,902 ตัวอย่าง)

| สถาปัตยกรรม / โมเดล | Accuracy | Precision | Recall | F1-Score | ROC-AUC | จุดเด่น |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **1. BiLSTM + Word2Vec** | **78.40%** | 75.05% | **85.85%** | **80.09%** | **87.15%** | 🏆 คะแนนรวมสูงสุด และ Recall สูงสุด |
| **2. Logistic Regression + BoW** | 77.83% | 75.74% | 82.67% | 79.05% | 86.60% | โมเดล Baseline ความเร็วสูง |
| **3. Logistic Regression + TF-IDF** | 78.15% | **78.31%** | 78.60% | 78.46% | 86.76% | 🎯 Precision สูงสุด (False Positive ต่ำสุด) |
| **4. Decision Tree + TF-IDF** | 66.81% | 64.82% | 75.29% | 69.66% | 71.24% | Explainability ผ่าน Gini Feature Importance |

---

## 🏗️ โครงสร้างสถาปัตยกรรมโมเดล (Model Architectures)

### 1. BiLSTM + Word2Vec (Sequential Deep Learning)
* **Tokenization:** PyThaiNLP (engine: `newmm`)
* **Embedding:** Pre-trained Word2Vec (Skip-gram, `vector_size=100`, `window=5`, `min_count=2`, Vocab: 9,202)
* **Pipeline:**
  $$\text{Input (100 tokens)} \rightarrow \text{Embedding (9202, 100)} \rightarrow \text{Bidirectional(LSTM(64))} \rightarrow \text{Dropout(0.30)} \rightarrow \text{Dense(32, ReLU)} \rightarrow \text{Dropout(0.20)} \rightarrow \text{Dense(1, Sigmoid)}$$
* **Training:** Adam (lr=0.001), Binary Crossentropy, EarlyStopping (patience=3), ReduceLROnPlateau (factor=0.5)

### 2. Logistic Regression + Bag of Words (BoW)
* **Feature Extraction:** `CountVectorizer` (Unigram + Bigram `(1, 2)`, `min_df=2`, 55,860 features)
* **Hyperparameter:** $C = 0.3$ ($L_2$ Regularization)

### 3. Logistic Regression + TF-IDF
* **Feature Extraction:** `TfidfVectorizer` (Sublinear TF $1+\log(tf)$, `min_df=2`, 55,860 features)
* **Hyperparameter:** $C = 3.0$ ($L_2$ Regularization)
* **Top Informative Words:**
  * *Class 1 (ซึมเศร้า):* ยา, หมอ, เรา, ดรีม, คุณหมอ, โรค, อาการ, ซึมเศร้า, ป่วย, ฆ่าตัวตาย, การรักษา, ทำร้าย, จิตแพทย์
  * *Class 0 (ปกติ):* เธอ, ความรัก, เติบโต, พี่, เขา, กบ, ดอกไม้, นั้น, แฮงค์, รัก, ยาย, ครู, เมี่ยง

### 4. Decision Tree + TF-IDF
* **Feature Extraction:** `TfidfVectorizer` (47,578 features)
* **Hyperparameter:** `max_depth = 25` (899 ใบ)

---

## 📁 โครงสร้างโปรเจกต์ (Project Structure)

```text
├── Depression_Dataset.csv                      # ชุดข้อมูลต้นฉบับ (32,676 แถว)
├── NLP-train.csv                               # ชุดข้อมูล Train (70% - 22,873 แถว)
├── NLP-validation.csv                          # ชุดข้อมูล Validation (15% - 4,901 แถว)
├── NLP-test.csv                                # ชุดข้อมูล Test (15% - 4,902 แถว)
├── Project_1_Text_Classification_Group_10.ipynb # Jupyter Notebook หลัก
├── Group_10.pdf                                # เอกสารนำเสนอฉบับสมบูรณ์ (PDF)
├── Group_10.html                               # ไฟล์ HTML ต้นฉบับเอกสารนำเสนอ
├── generate_report_charts.py                   # สคริปต์สร้างภาพกราฟประกอบความละเอียดสูง
├── compile_pdf.py                              # สคริปต์คอมไพล์เอกสารเป็น PDF
├── figures/                                    # โฟลเดอร์รูปภาพจาก Notebook
└── report_assets/                              # โฟลเดอร์รูปภาพกราฟและผังสถาปัตยกรรม (300 DPI)
```

---

## 🚀 การติดตั้งและการใช้งาน (Installation & Setup)

1. ติดตั้งไลบรารีที่จำเป็น:
```bash
pip install numpy pandas matplotlib seaborn scikit-learn pythainlp gensim tensorflow
```

2. รัน Jupyter Notebook:
```bash
jupyter notebook Project_1_Text_Classification_Group_10.ipynb
```

3. สร้างเอกสารนำเสนอ PDF:
```bash
python generate_report_charts.py
python compile_pdf.py
```
