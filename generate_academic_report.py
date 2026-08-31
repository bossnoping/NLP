import os
import base64
import subprocess

def img_to_base64(path):
    with open(path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode('utf-8')
        ext = os.path.splitext(path)[1].lower().replace('.', '')
        if ext == 'jpg': ext = 'jpeg'
        return f"data:image/{ext};base64,{encoded}"

# Load base64 charts
img_master = img_to_base64("report_assets/master_comparison.png")
img_bilstm_curves = img_to_base64("report_assets/bilstm_learning_curves.png")
img_cms = img_to_base64("report_assets/all_confusion_matrices.png")
img_tuning = img_to_base64("report_assets/hyperparameter_tuning.png")
img_dt_feat = img_to_base64("report_assets/dt_feature_importance.png")
img_bilstm_arch = img_to_base64("report_assets/bilstm_architecture.png")

html_template = """<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<title>รายงานโครงงาน: การจำแนกข้อความภาษาไทยเพื่อระบุภาวะซึมเศร้าด้วยเทคนิค Machine Learning และ Deep Learning (Group 10)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Sarabun:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Prompt:ital,wght@0,400;0,500;0,600;0,700&display=swap" rel="stylesheet">
<style>
  @page {
    size: A4 portrait;
    margin: 18mm 18mm 18mm 18mm;
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    font-family: 'Sarabun', 'Leelawadee UI', Tahoma, sans-serif;
    font-size: 13.5px;
    line-height: 1.65;
    color: #111827;
    background-color: #ffffff;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  h1, h2, h3, h4, .heading {
    font-family: 'Prompt', 'Sarabun', 'Leelawadee UI', Tahoma, sans-serif;
    color: #0f172a;
    font-weight: 600;
  }

  /* Cover Page */
  .cover-page {
    min-height: 840px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-align: center;
    padding: 40px 20px 20px 20px;
    page-break-after: always;
    border: 1.5px solid #cbd5e1;
    border-radius: 4px;
    background: #ffffff;
  }

  .cover-header {
    margin-top: 40px;
  }

  .cover-inst {
    font-size: 15px;
    font-weight: 500;
    color: #475569;
    letter-spacing: 0.5px;
    margin-bottom: 25px;
  }

  .cover-title {
    font-size: 23px;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.4;
    margin-bottom: 12px;
  }

  .cover-subtitle {
    font-size: 15px;
    font-weight: 500;
    color: #2563eb;
    margin-bottom: 30px;
  }

  .cover-divider {
    width: 80px;
    height: 3px;
    background: #1e3a8a;
    margin: 0 auto 35px auto;
  }

  .cover-meta-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 24px 30px;
    max-width: 480px;
    margin: 0 auto;
    text-align: left;
    font-size: 13.5px;
    line-height: 1.9;
  }

  .cover-meta-row {
    display: flex;
    justify-content: space-between;
    border-bottom: 1px dashed #e2e8f0;
    padding: 4px 0;
  }

  .cover-meta-row:last-child {
    border-bottom: none;
  }

  .cover-meta-label {
    font-weight: 600;
    color: #334155;
    width: 140px;
  }

  .cover-meta-val {
    color: #0f172a;
    flex: 1;
  }

  .cover-footer {
    margin-bottom: 30px;
    font-size: 13px;
    color: #64748b;
  }

  /* Content Sections */
  .section {
    margin-bottom: 22px;
    page-break-inside: auto;
  }

  .section-title {
    font-size: 15.5px;
    font-weight: 600;
    color: #0f172a;
    border-bottom: 1.5px solid #0f172a;
    padding-bottom: 4px;
    margin-top: 22px;
    margin-bottom: 12px;
    page-break-after: avoid;
  }

  .subsection-title {
    font-size: 14px;
    font-weight: 600;
    color: #1e3a8a;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }

  p {
    margin-bottom: 10px;
    text-align: justify;
    text-justify: inter-word;
    line-height: 1.65;
  }

  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0 16px 0;
    font-size: 12.5px;
    page-break-inside: avoid;
  }

  th {
    background-color: #f1f5f9;
    color: #0f172a;
    font-weight: 600;
    text-align: center;
    padding: 7px 10px;
    border: 1px solid #cbd5e1;
    font-family: 'Prompt', sans-serif;
  }

  td {
    padding: 6.5px 10px;
    border: 1px solid #cbd5e1;
    text-align: center;
  }

  tr:nth-child(even) {
    background-color: #f8fafc;
  }

  td.text-left {
    text-align: left;
  }

  td.bold {
    font-weight: 600;
  }

  /* Architecture & Code Blocks */
  pre, code {
    font-family: 'Consolas', 'Courier New', monospace;
  }

  .pipeline-box {
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 12px 16px;
    margin: 10px 0 14px 0;
    font-family: 'Consolas', monospace;
    font-size: 12px;
    line-height: 1.5;
    color: #1e293b;
    page-break-inside: avoid;
    white-space: pre;
    overflow-x: auto;
  }

  /* Math Equations */
  .equation-box {
    background-color: #fafafa;
    border-left: 3.5px solid #1e3a8a;
    border-radius: 4px;
    padding: 10px 16px;
    margin: 10px 0 14px 0;
    font-size: 13.5px;
    page-break-inside: avoid;
  }

  .equation-title {
    font-family: 'Prompt', sans-serif;
    font-size: 13px;
    font-weight: 600;
    color: #0f172a;
    margin-bottom: 4px;
  }

  .equation-formula {
    font-family: 'Cambria Math', 'Times New Roman', serif;
    font-size: 15px;
    font-weight: bold;
    color: #1e3a8a;
    margin: 4px 0;
  }

  /* Callouts & Quotes */
  blockquote {
    background-color: #f8fafc;
    border-left: 3.5px solid #2563eb;
    padding: 10px 16px;
    margin: 10px 0 14px 0;
    font-size: 13px;
    font-style: normal;
    color: #1e293b;
    page-break-inside: avoid;
    border-radius: 0 6px 6px 0;
  }

  /* Images */
  .figure-container {
    text-align: center;
    margin: 14px 0 18px 0;
    page-break-inside: avoid;
  }

  .figure-container img {
    max-width: 96%;
    height: auto;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
  }

  .figure-caption {
    font-size: 11.5px;
    color: #475569;
    margin-top: 5px;
    font-style: italic;
  }

  ul, ol {
    padding-left: 22px;
    margin-bottom: 10px;
  }

  li {
    margin-bottom: 4px;
  }

  .page-break {
    page-break-before: always;
  }

  .badge-pending {
    display: inline-block;
    padding: 2px 8px;
    background: #e2e8f0;
    color: #475569;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
  }
</style>
</head>
<body>

  <!-- ==================== COVER PAGE ==================== -->
  <div class="cover-page">
    <div class="cover-header">
      <div class="cover-inst">โครงงานรายวิชาการประมวลผลภาษาธรรมชาติ (Natural Language Processing)</div>
      <div class="cover-title">รายงานการจำแนกข้อความภาษาไทยเพื่อระบุภาวะซึมเศร้า<br>ด้วยเทคนิค Machine Learning และ Deep Learning</div>
      <div class="cover-subtitle">Thai Text Classification for Depression Detection: A Comparative Study</div>
      <div class="cover-divider"></div>
    </div>

    <div class="cover-meta-box">
      <div class="cover-meta-row">
        <span class="cover-meta-label">กลุ่มผู้จัดทำ:</span>
        <span class="cover-meta-val">Group 10 (กลุ่มที่ 10)</span>
      </div>
      <div class="cover-meta-row">
        <span class="cover-meta-label">รายวิชา:</span>
        <span class="cover-meta-val">[ชื่อรายวิชา]</span>
      </div>
      <div class="cover-meta-row">
        <span class="cover-meta-label">สมาชิกกลุ่ม:</span>
        <span class="cover-meta-val">[ใส่ภายหลัง]</span>
      </div>
      <div class="cover-meta-row">
        <span class="cover-meta-label">อาจารย์ผู้สอน:</span>
        <span class="cover-meta-val">[ใส่ภายหลัง]</span>
      </div>
      <div class="cover-meta-row">
        <span class="cover-meta-label">ภาคการศึกษา / ปี:</span>
        <span class="cover-meta-val">ภาคการศึกษาที่ 1 / 2026</span>
      </div>
    </div>

    <div class="cover-footer">
      เอกสารรายงานวิชาการสำหรับการนำเสนอและประเมินผลการเรียนรู้
    </div>
  </div>

  <!-- ==================== SECTION 1: ที่มาและความสำคัญ ==================== -->
  <div class="section">
    <div class="section-title">1. ที่มาและความสำคัญ (Background & Significance)</div>
    <p>
      ภาวะซึมเศร้า (Depression) เป็นปัญหาสุขภาพจิตที่ส่งผลกระทบต่อคุณภาพชีวิตของประชากรทั่วโลกอย่างมีนัยสำคัญ ในยุคดิจิทัล ผู้คนจำนวนมากเลือกที่จะระบายความรู้สึก อารมณ์ และประสบการณ์ส่วนตัวผ่านสื่อสังคมออนไลน์หรือแพลตฟอร์มสนทนา การประมวลผลภาษาธรรมชาติ (Natural Language Processing: NLP) และเทคนิคการจำแนกข้อความ (Text Classification) จึงมีบทบาทสำคัญในการนำมาใช้วิเคราะห์และคัดกรองข้อความภาษาไทยที่มีลักษณะบ่งชี้ถึงความเสี่ยงของภาวะซึมเศร้า
    </p>
    <p>
      โครงงานนี้เป็นการพัฒนาระบบจำแนกข้อความภาษาไทยแบบสองคลาส (Binary Text Classification) โดยมีนิยามของคลาสเป้าหมายดังนี้:
    </p>
    <ul>
      <li><strong>Class 0 (ไม่ป่วย / Non-Depression):</strong> ข้อความสนทนาทั่วไป ข้อความเชิงบวก หรือข้อความที่ไม่มีลักษณะบ่งชี้ถึงภาวะซึมเศร้า</li>
      <li><strong>Class 1 (ป่วย / Depression):</strong> ข้อความที่มีการบรรยายอารมณ์เศร้า ความสิ้นหวัง ความรู้สึกไร้ค่า อาการผิดปกติทางจิตใจ หรือพฤติกรรมเสี่ยง</li>
    </ul>
    <p>
      <strong>ข้อความระวังทางวิชาการ:</strong> ระบบที่พัฒนาขึ้นในโครงงานนี้มีวัตถุประสงค์เพื่อการศึกษา ค้นคว้า และวิเคราะห์ทางเทคนิคด้าน NLP และ Text Classification เท่านั้น <em>ห้ามนำผลลัพธ์ของแบบจำลองไปใช้ในการวินิจฉัยทางการแพทย์หรือตัดสินภาวะทางจิตเวชโดยตรง</em> โดยระบบทำหน้าที่เป็นเพียงเครื่องมือวิเคราะห์เชิงสถิติและคัดกรองเบื้องต้น
    </p>
  </div>

  <!-- ==================== SECTION 2: วัตถุประสงค์ ==================== -->
  <div class="section">
    <div class="section-title">2. วัตถุประสงค์ (Objectives)</div>
    <p>โครงงานนี้มีวัตถุประสงค์หลักในการดำเนินงานดังต่อไปนี้:</p>
    <ol>
      <li>เพื่อพัฒนาและประเมินประสิทธิภาพของแบบจำลองการจำแนกข้อความภาษาไทย (Thai Text Classification) สำหรับระบุข้อความที่มีลักษณะบ่งชี้ภาวะซึมเศร้า</li>
      <li>เพื่อศึกษาและเปรียบเทียบเทคนิคการแปลงข้อความเป็นฟีเจอร์ (Feature Extraction / Representation) ทั้งรูปแบบ Bag-of-Words (BoW), TF-IDF และ Pre-trained Word2Vec Embedding</li>
      <li>เพื่อศึกษาและออกแบบสถาปัตยกรรมโครงข่ายประสาทเทียมแบบ Deep Sequential Model ด้วย Bidirectional Long Short-Term Memory (BiLSTM) ร่วมกับการตัดคำภาษาไทย</li>
      <li>เพื่อเปรียบเทียบประสิทธิภาพของแบบจำลองการเรียนรู้ของเครื่องแบบดั้งเดิม (Traditional Machine Learning) ได้แก่ Logistic Regression และ Decision Tree ร่วมกับการปรับจูน Hyperparameter</li>
      <li>เพื่อประเมินประสิทธิภาพของแบบจำลองผ่านตัวชี้วัดมาตรฐาน (Accuracy, Precision, Recall, F1-score, ROC-AUC) และวิเคราะห์ความเหมาะสมในการประยุกต์ใช้งาน</li>
      <li>เพื่อเตรียมโครงสร้างและแนวทางสำหรับการขยายผลไปสู่แบบจำลอง Transformer-based Language Model (BERT) ในขั้นตอนต่อไป</li>
    </ol>
  </div>

  <!-- ==================== SECTION 3: DATASET ==================== -->
  <div class="section">
    <div class="section-title">3. ข้อมูลชุดข้อมูล (Dataset)</div>
    <p>
      ข้อมูลที่นำมาใช้ในการทดลองคือชุดข้อมูลข้อความภาษาไทยจากไฟล์ <code>Depression_Dataset.csv</code> โดยข้อมูลทั้งหมดถูกตรวจสอบและสกัดค่าทางสถิติจริงจาก Jupyter Notebook ของ Group 10 ดังแสดงในตารางที่ 1
    </p>

    <table>
      <thead>
        <tr>
          <th>รายการ (Attribute)</th>
          <th>จำนวน / ค่าทางสถิติที่พบใน Notebook</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="text-left"><strong>จำนวนข้อมูลทั้งหมด (Total Dataset)</strong></td>
          <td class="bold">32,676 แถว</td>
        </tr>
        <tr>
          <td class="text-left"><strong>จำนวนข้อมูล Class 0 (ไม่ป่วย / Non-Depression)</strong></td>
          <td>16,138 แถว (49.39%)</td>
        </tr>
        <tr>
          <td class="text-left"><strong>จำนวนข้อมูล Class 1 (ป่วย / Depression)</strong></td>
          <td>16,538 แถว (50.61%)</td>
        </tr>
        <tr>
          <td class="text-left"><strong>ค่าสูญหาย (Missing Values ในคอลัมน์ text)</strong></td>
          <td>0 แถว (ไม่พบค่าว่าง)</td>
        </tr>
        <tr>
          <td class="text-left"><strong>จำนวนแถวซ้ำซ้อนใน Raw Data (Duplicate Rows)</strong></td>
          <td>5,096 แถว</td>
        </tr>
        <tr>
          <td class="text-left"><strong>จำนวนแถวซ้ำซ้อนหลังทำความสะอาด (Duplicate Clean Texts)</strong></td>
          <td>5,096 แถว</td>
        </tr>
        <tr>
          <td class="text-left"><strong>ความยาวข้อความต่ำสุด (Min Character Length)</strong></td>
          <td>3 ตัวอักษร</td>
        </tr>
        <tr>
          <td class="text-left"><strong>ความยาวข้อความสูงสุด (Max Character Length)</strong></td>
          <td>4,496 ตัวอักษร</td>
        </tr>
        <tr>
          <td class="text-left"><strong>ความยาวข้อความเฉลี่ย (Mean Character Length)</strong></td>
          <td>91.95 ตัวอักษร (มัธยฐาน = 61.0 ตัวอักษร)</td>
        </tr>
      </tbody>
    </table>
    <p style="font-size: 12px; color: #475569;">
      <em>หมายเหตุ:</em> สัดส่วนของข้อมูลระหว่าง Class 0 (49.39%) และ Class 1 (50.61%) มีความสมดุลสูง (Balanced Class Distribution) จึงไม่ก่อให้เกิดปัญหา Class Imbalance ขั้นรุนแรง
    </p>
  </div>

  <!-- ==================== SECTION 4: DATA PREPROCESSING ==================== -->
  <div class="section">
    <div class="section-title">4. การเตรียมข้อมูลก่อนการประมวลผล (Data Preprocessing)</div>
    <p>
      กระบวนการเตรียมข้อมูลตามที่มีการดำเนินการจริงใน Notebook ประกอบด้วยขั้นตอนที่เป็นระบบดังต่อไปนี้:
    </p>
    <ol>
      <li><strong>การตรวจสอบ Missing Values:</strong> ตรวจสอบค่าว่างในคอลัมน์ <code>text</code> พบว่าไม่มีค่าว่าง (Empty Text = 0)</li>
      <li><strong>การตรวจสอบและจัดการข้อมูลซ้ำซ้อน (Duplicate Handling):</strong> ตรวจสอบแถวที่ซ้ำซ้อนในชุดข้อมูลเพื่อวิเคราะห์ความขัดแย้งของ Label</li>
      <li><strong>การทำความสะอาดข้อความ (Text Cleaning):</strong>
        <ul>
          <li>ลบ URL / Hyperlinks ด้วย Regular Expression: <code>re.sub(r'https?://\\S+|www\\.\\S+', '', text)</code></li>
          <li>ลบช่องว่างส่วนเกิน (Excessive Whitespace): <code>re.sub(r'\\s+', ' ', text)</code></li>
          <li>ตัดช่องว่างหัวและท้ายข้อความด้วย <code>text.strip()</code></li>
        </ul>
      </li>
      <li><strong>การตัดคำภาษาไทย (Thai Tokenization):</strong> ใช้ไลบรารี <code>pythainlp.tokenize.word_tokenize</code> ด้วย engine <code>newmm</code> (Maximal Matching) สำหรับแยกคำในประโยคภาษาไทย</li>
      <li><strong>การแบ่งชุดข้อมูล (Dataset Splitting):</strong> แบ่งข้อมูลออกเป็น 3 ส่วนในสัดส่วน <strong>70% : 15% : 15%</strong> แบบคงสัดส่วนคลาส</li>
    </ol>

    <div class="pipeline-box">Raw Dataset (32,676 แถว)
    ↓
Data Cleaning (ลบ URL, จัดการ Whitespace, Strip)
    ↓
Duplicate & Label Verification (ตรวจสอบความถูกต้องของข้อความ)
    ↓
Thai Tokenization (PyThaiNLP: newmm)
    ↓
Train / Validation / Test Split (สัดส่วน 70% / 15% / 15%)
    ↓
Feature Extraction (Word2Vec / Bag-of-Words / TF-IDF)
    ↓
Model Training (BiLSTM / Logistic Regression / Decision Tree)
    ↓
Evaluation on Test Set (Accuracy, Precision, Recall, F1-score, ROC-AUC)</div>

    <table>
      <thead>
        <tr>
          <th>ชุดข้อมูล (Dataset Split)</th>
          <th>จำนวนแถว</th>
          <th>Class 0 (ปกติ)</th>
          <th>Class 1 (ซึมเศร้า)</th>
          <th>สัดส่วน (%)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="text-left"><strong>Train Set</strong></td>
          <td>22,873</td>
          <td>11,297 (49.39%)</td>
          <td>11,576 (50.61%)</td>
          <td>70.0%</td>
        </tr>
        <tr>
          <td class="text-left"><strong>Validation Set</strong></td>
          <td>4,901</td>
          <td>2,420 (49.38%)</td>
          <td>2,481 (50.62%)</td>
          <td>15.0%</td>
        </tr>
        <tr>
          <td class="text-left"><strong>Test Set</strong></td>
          <td>4,902</td>
          <td>2,421 (49.39%)</td>
          <td>2,481 (50.61%)</td>
          <td>15.0%</td>
        </tr>
        <tr style="font-weight: 600; background-color: #f1f5f9;">
          <td class="text-left">รวมทั้งหมด (Total)</td>
          <td>32,676</td>
          <td>16,138 (49.39%)</td>
          <td>16,538 (50.61%)</td>
          <td>100.0%</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="page-break"></div>

  <!-- ==================== SECTION 5: EXPERIMENTAL SETUP ==================== -->
  <div class="section">
    <div class="section-title">5. สภาพแวดล้อมและการตั้งค่าการทดลอง (Experimental Setup)</div>
    <p>
      การทดลองทั้งหมดในโครงงานดำเนินการภายใต้สภาพแวดล้อมซอฟต์แวร์และไลบรารีมาตรฐานที่ระบุใน Notebook ดังนี้:
    </p>
    <ul>
      <li><strong>ภาษาและแพลตฟอร์ม:</strong> Python (ผ่าน Jupyter Notebook / Google Colab Environment)</li>
      <li><strong>การจัดการข้อมูลและการคำนวณ:</strong> <code>pandas</code>, <code>numpy</code></li>
      <li><strong>การประมวลผลภาษาไทย:</strong> <code>pythainlp</code> (Tokenization engine: <code>newmm</code>)</li>
      <li><strong>การสร้าง Word Embedding:</strong> <code>gensim.models.Word2Vec</code></li>
      <li><strong>Machine Learning:</strong> <code>scikit-learn</code> (Logistic Regression, Decision Tree, CountVectorizer, TfidfVectorizer, Metrics)</li>
      <li><strong>Deep Learning:</strong> <code>tensorflow</code> / <code>keras</code> (Sequential, Embedding, Bidirectional, LSTM, Dense, Dropout)</li>
      <li><strong>การสร้างภาพกราฟิก:</strong> <code>matplotlib</code>, <code>seaborn</code></li>
      <li><strong>Random State:</strong> มีการกำหนด <code>seed = 42</code> ใน Word2Vec และ <code>random_state = 42</code> ใน Decision Tree เพื่อให้ผลการทดลองสามารถทำซ้ำได้ (Reproducibility)</li>
      <li><strong>การประมวลผลฮาร์ดแวร์:</strong> รันบน CPU / Standard Execution Environment (พบข้อความ TensorFlow แจ้งเตือน native Windows CPU fallback)</li>
    </ul>
  </div>

  <!-- ==================== SECTION 6: MODEL 1 ==================== -->
  <div class="section">
    <div class="section-title">6. Model 1: Word2Vec Embedding + BiLSTM (Deep Sequential Model)</div>
    <p>
      <strong>แนวคิดและหลักการ:</strong> แบบจำลองโครงข่ายประสาทเทียมแบบลำดับเวลา (Sequential Neural Network) ที่ใช้เทคนิค <strong>Word2Vec (Skip-gram)</strong> ในการแปลงคำศัพท์เป็นเวกเตอร์ความหมายหนาแน่น (Dense Vector) ขนาด 100 มิติ จากนั้นส่งต่อไปยังโครงข่าย <strong>Bidirectional LSTM (BiLSTM)</strong> ซึ่งมีความสามารถในการประมวลผลลำดับคำทั้งทิศทางไปข้างหน้า (Forward) และย้อนกลับ (Backward) ทำให้เข้าใจความสัมพันธ์ของคำและบริบทประโยคได้อย่างครอบคลุม
    </p>

    <div class="subsection-title">ค่า Hyperparameters จริงจาก Notebook:</div>
    <ul>
      <li><strong>Word2Vec:</strong> <code>sentences=BIMD_train_tokens</code>, <code>vector_size=100</code>, <code>window=5</code>, <code>min_count=2</code>, <code>sg=1</code> (Skip-gram), <code>epochs=10</code>, <code>seed=42</code> (ขนาด Vocabulary = 9,200 คำ + PAD + UNK = 9,202 โทเค็น)</li>
      <li><strong>Sequence Length:</strong> <code>MAX_LEN = 100</code> (Mean token length = 16.59, 99th percentile = 89 คำ) โดยทำการ Padding แบบ Post-padding</li>
      <li><strong>BiLSTM Layer:</strong> LSTM Units = 64 หน่วย (ผลลัพธ์แบบต่อกัน 2 ทิศทาง = 128 มิติ)</li>
      <li><strong>Regularization:</strong> Dropout Layer 1 = 0.30, Dropout Layer 2 = 0.20</li>
      <li><strong>Dense Hidden Layer:</strong> 32 หน่วย พร้อมฟังก์ชันกระตุ้น (Activation) แบบ <code>ReLU</code></li>
      <li><strong>Output Layer:</strong> 1 หน่วย พร้อมฟังก์ชันกระตุ้นแบบ <code>Sigmoid</code> สำหรับการจำแนกแบบ Binary</li>
      <li><strong>Training Settings:</strong> Optimizer = <code>Adam</code> (Learning Rate = 0.001), Loss = <code>binary_crossentropy</code>, Batch Size = 64, Epochs = 15</li>
      <li><strong>Callbacks:</strong> <code>EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)</code> และ <code>ReduceLROnPlateau(monitor='val_loss', patience=2, factor=0.5, min_lr=1e-6)</code> (หยุดที่ Epoch ที่ 5 และคืนค่าน้ำหนักที่ดีที่สุดจาก Epoch ที่ 2)</li>
    </ul>

    <div class="pipeline-box">Thai Text
   ↓
Thai Tokenization (PyThaiNLP newmm)
   ↓
Word2Vec Representation (Skip-gram, dim=100)
   ↓
Vocabulary Mapping (Vocab Size = 9,202 โทเค็น)
   ↓
Padding (MAX_LEN = 100, Post-padding)
   ↓
Embedding Layer (Input: [None, 100], Output: [None, 100, 100], Trainable=True)
   ↓
Bidirectional LSTM Layer (64 units × 2 = 128 dimensions)
   ↓
Dropout (Rate = 0.30)
   ↓
Dense Hidden Layer (32 units, Activation = ReLU)
   ↓
Dropout (Rate = 0.20)
   ↓
Dense Output Layer (1 unit, Activation = Sigmoid)
   ↓
Class Prediction (0: ปกติ / 1: ซึมเศร้า)</div>

    <div class="figure-container">
      <img src="REPLACE_IMG_BILSTM_ARCH" alt="BiLSTM Architecture Diagram">
      <div class="figure-caption">รูปที่ 1: สถาปัตยกรรมโครงข่ายประสาทเทียม BiLSTM ร่วมกับ Word2Vec Embedding</div>
    </div>

    <div class="subsection-title">ผลการทดลองจริงบนชุดทดสอบ (Test Set: 4,902 ตัวอย่าง):</div>
    <table>
      <thead>
        <tr>
          <th>Metric</th>
          <th>ผลการทดลองจริง (Result)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="text-left"><strong>Accuracy</strong></td>
          <td class="bold">0.7840 (78.40%)</td>
        </tr>
        <tr>
          <td class="text-left"><strong>Precision (Class 1)</strong></td>
          <td>0.7505 (75.05%)</td>
        </tr>
        <tr>
          <td class="text-left"><strong>Recall (Class 1)</strong></td>
          <td class="bold" style="background-color: #ecfdf5; color: #065f46;">0.8585 (85.85%) — สูงสุดในทุกโมเดล</td>
        </tr>
        <tr>
          <td class="text-left"><strong>F1-score (Class 1)</strong></td>
          <td class="bold" style="background-color: #eff6ff; color: #1d4ed8;">0.8009 (80.09%) — สูงสุดในทุกโมเดล</td>
        </tr>
        <tr>
          <td class="text-left"><strong>ROC-AUC</strong></td>
          <td class="bold">0.8715 (87.15%)</td>
        </tr>
      </tbody>
    </table>

    <div class="figure-container">
      <img src="REPLACE_IMG_BILSTM_CURVES" alt="BiLSTM Learning Curves">
      <div class="figure-caption">รูปที่ 2: กราฟแสดงผลการเรียนรู้ Loss และ Accuracy ตลอด Epochs ของโมเดล BiLSTM</div>
    </div>
  </div>

  <div class="page-break"></div>

  <!-- ==================== SECTION 7: MODEL 2 ==================== -->
  <div class="section">
    <div class="section-title">7. Model 2: Bag-of-Words (BoW) + Logistic Regression</div>
    <p>
      <strong>แนวคิดและหลักการ:</strong> เทคนิคพื้นฐานด้าน NLP โดยการแปลงข้อความเป็นเวกเตอร์ความถี่ของการปรากฏของคำ (Word Count Representation) ผ่าน <code>CountVectorizer</code> โดยไม่คำนึงถึงลำดับของคำ จากนั้นใช้แบบจำลองการจำแนกเชิงเส้น <strong>Logistic Regression</strong> ร่วมกับการควบคุมความซับซ้อนด้วย L₂ Regularization
    </p>

    <div class="pipeline-box">Thai Text
   ↓
Tokenization (PyThaiNLP newmm)
   ↓
Bag-of-Words (CountVectorizer: Unigram + Bigram)
   ↓
Feature Vector (ขนาด 55,860 มิติ)
   ↓
Logistic Regression (C = 0.3, solver = lbfgs, max_iter = 1000)
   ↓
Class Prediction (0: ปกติ / 1: ซึมเศร้า)</div>

    <div class="subsection-title">การปรับจูน Hyperparameter (C Tuning บน Validation Set):</div>
    <table>
      <thead>
        <tr>
          <th>ค่า C ที่ทดสอบ</th>
          <th>Validation Accuracy</th>
          <th>Validation Precision</th>
          <th>Validation Recall</th>
          <th>Validation F1-score</th>
          <th>Validation ROC-AUC</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>0.001</td><td>0.6015</td><td>0.5607</td><td>0.8412</td><td>0.6729</td><td>0.7226</td></tr>
        <tr><td>0.010</td><td>0.7248</td><td>0.6976</td><td>0.7811</td><td>0.7371</td><td>0.8142</td></tr>
        <tr><td>0.100</td><td>0.7745</td><td>0.7516</td><td>0.8247</td><td>0.7865</td><td>0.8624</td></tr>
        <tr style="background-color: #eff6ff; font-weight: 600;">
          <td>0.300 (Best C)</td>
          <td>0.7770</td>
          <td>0.7577</td>
          <td>0.8267</td>
          <td>0.7906</td>
          <td>0.8643</td>
        </tr>
        <tr><td>0.500</td><td>0.7760</td><td>0.7588</td><td>0.8222</td><td>0.7892</td><td>0.8624</td></tr>
        <tr><td>1.000</td><td>0.7735</td><td>0.7589</td><td>0.8142</td><td>0.7854</td><td>0.8581</td></tr>
        <tr><td>3.000</td><td>0.7690</td><td>0.7581</td><td>0.8025</td><td>0.7797</td><td>0.8491</td></tr>
        <tr><td>5.000</td><td>0.7668</td><td>0.7580</td><td>0.7977</td><td>0.7773</td><td>0.8441</td></tr>
        <tr><td>10.000</td><td>0.7635</td><td>0.7562</td><td>0.7912</td><td>0.7733</td><td>0.8364</td></tr>
      </tbody>
    </table>

    <div class="subsection-title">ผลการทดลองจริงบนชุดทดสอบ (Test Set: 4,902 ตัวอย่าง) ที่ค่า C = 0.3:</div>
    <table>
      <thead>
        <tr>
          <th>Metric</th>
          <th>ผลการทดลองจริง (Result)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="text-left"><strong>Accuracy</strong></td>
          <td class="bold">0.7783 (77.83%)</td>
        </tr>
        <tr>
          <td class="text-left"><strong>Precision (Class 1)</strong></td>
          <td>0.7574 (75.74%)</td>
        </tr>
        <tr>
          <td class="text-left"><strong>Recall (Class 1)</strong></td>
          <td class="bold">0.8267 (82.67%)</td>
        </tr>
        <tr>
          <td class="text-left"><strong>F1-score (Class 1)</strong></td>
          <td class="bold">0.7905 (79.05%)</td>
        </tr>
        <tr>
          <td class="text-left"><strong>ROC-AUC</strong></td>
          <td>0.8660 (86.60%)</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- ==================== SECTION 8: MODEL 3 ==================== -->
  <div class="section">
    <div class="section-title">8. Model 3: TF-IDF + Logistic Regression</div>
    <p>
      <strong>แนวคิดและหลักการ:</strong> การแปลงข้อความเป็นเวกเตอร์โดยใช้น้ำหนัก <strong>Term Frequency-Inverse Document Frequency (TF-IDF)</strong> ร่วมกับ <code>sublinear_tf=True</code> ซึ่งช่วยลดทอนค่าน้ำหนักของคำที่ปรากฏบ่อยทั่วไปในทุกเอกสาร และเน้นคำเฉพาะเจาะจงที่มีความสำคัญต่อการจำแนกคลาส
    </p>

    <div class="pipeline-box">Thai Text
   ↓
Tokenization (PyThaiNLP newmm)
   ↓
TF-IDF Vectorizer (ngram_range=(1,2), min_df=2, sublinear_tf=True)
   ↓
Feature Vector (ขนาด 55,860 มิติ)
   ↓
Logistic Regression (C = 3.0, solver = lbfgs, max_iter = 1000)
   ↓
Class Prediction (0: ปกติ / 1: ซึมเศร้า)</div>

    <div class="subsection-title">การปรับจูน Hyperparameter (C Tuning บน Validation Set):</div>
    <table>
      <thead>
        <tr>
          <th>ค่า C ที่ทดสอบ</th>
          <th>Validation Accuracy</th>
          <th>Validation Precision</th>
          <th>Validation Recall</th>
          <th>Validation F1-score</th>
          <th>Validation ROC-AUC</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>0.001</td><td>0.5892</td><td>0.5524</td><td>0.9960</td><td>0.7107</td><td>0.6974</td></tr>
        <tr><td>0.010</td><td>0.7180</td><td>0.6698</td><td>0.8783</td><td>0.7601</td><td>0.8164</td></tr>
        <tr><td>0.100</td><td>0.7725</td><td>0.7441</td><td>0.8388</td><td>0.7885</td><td>0.8601</td></tr>
        <tr><td>0.300</td><td>0.7790</td><td>0.7618</td><td>0.8186</td><td>0.7892</td><td>0.8671</td></tr>
        <tr><td>0.500</td><td>0.7802</td><td>0.7686</td><td>0.8090</td><td>0.7883</td><td>0.8679</td></tr>
        <tr><td>1.000</td><td>0.7811</td><td>0.7788</td><td>0.7944</td><td>0.7865</td><td>0.8682</td></tr>
        <tr style="background-color: #eff6ff; font-weight: 600;">
          <td>3.000 (Best C)</td>
          <td>0.7813</td>
          <td>0.7844</td>
          <td>0.7848</td>
          <td>0.7846</td>
          <td>0.8673</td>
        </tr>
        <tr><td>5.000</td><td>0.7805</td><td>0.7854</td><td>0.7815</td><td>0.7834</td><td>0.8663</td></tr>
        <tr><td>10.000</td><td>0.7796</td><td>0.7866</td><td>0.7775</td><td>0.7820</td><td>0.8643</td></tr>
      </tbody>
    </table>

    <div class="subsection-title">ผลการทดลองจริงบนชุดทดสอบ (Test Set: 4,902 ตัวอย่าง) ที่ค่า C = 3.0:</div>
    <table>
      <thead>
        <tr>
          <th>Metric</th>
          <th>ผลการทดลองจริง (Result)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="text-left"><strong>Accuracy</strong></td>
          <td class="bold">0.7815 (78.15%)</td>
        </tr>
        <tr>
          <td class="text-left"><strong>Precision (Class 1)</strong></td>
          <td class="bold" style="background-color: #ecfdf5; color: #065f46;">0.7831 (78.31%) — สูงสุดในทุกโมเดล</td>
        </tr>
        <tr>
          <td class="text-left"><strong>Recall (Class 1)</strong></td>
          <td>0.7860 (78.60%)</td>
        </tr>
        <tr>
          <td class="text-left"><strong>F1-score (Class 1)</strong></td>
          <td>0.7846 (78.46%)</td>
        </tr>
        <tr>
          <td class="text-left"><strong>ROC-AUC</strong></td>
          <td>0.8676 (86.76%)</td>
        </tr>
      </tbody>
    </table>

    <p style="margin-top: 6px; font-size: 12.5px;">
      <strong>คำสำคัญที่มีค่าน้ำหนักสัมประสิทธิ์สูงสุดในโมเดล (Top Words):</strong><br>
      • <em>Class 1 (ซึมเศร้า):</em> ยา, หมอ, เรา, ดรีม, คุณหมอ, โรค, อาการ, ซึมเศร้า, ค่ะ, ป่วย, ชั้น, ฆ่าตัวตาย, การรักษา, ทำร้าย, จิตแพทย์<br>
      • <em>Class 0 (ปกติ):</em> เธอ, ความรัก, เติบโต, พี่, เขา, กบ, ดอกไม้, นั้น, แฮงค์, รัก, ของ, นาย, ยาย, ครู, เมี่ยง
    </p>
  </div>

  <div class="page-break"></div>

  <!-- ==================== SECTION 9: MODEL 4 ==================== -->
  <div class="section">
    <div class="section-title">9. Model 4: TF-IDF + Decision Tree</div>
    <p>
      <strong>แนวคิดและหลักการ:</strong> แบบจำลองแบบต้นไม้การตัดสินใจ (Decision Tree) ซึ่งสร้างกฎการแบ่งข้อมูลแบบไม่เป็นเส้นตรง (Non-linear Rules) โดยเนื่องจาก Decision Tree ไม่สามารถรับข้อความดิบได้ จึงต้องแปลงข้อความเป็นเวกเตอร์ TF-IDF (จำนวนฟีเจอร์ 47,578 มิติ) ก่อนนำเข้าสู่กระบวนการตัดสินใจ
    </p>

    <div class="pipeline-box">Thai Text
   ↓
Tokenization (PyThaiNLP newmm)
   ↓
TF-IDF Vectorizer (ngram_range=(1,2), min_df=2, sublinear_tf=True)
   ↓
Feature Vector (ขนาด 47,578 มิติ)
   ↓
Decision Tree Classifier (max_depth = 25, random_state = 42)
   ↓
Class Prediction (0: ปกติ / 1: ซึมเศร้า)</div>

    <div class="subsection-title">การปรับจูน Hyperparameter (max_depth Tuning บน Validation Set):</div>
    <table>
      <thead>
        <tr>
          <th>max_depth ที่ทดสอบ</th>
          <th>Validation Accuracy</th>
          <th>Validation Precision</th>
          <th>Validation Recall</th>
          <th>Validation F1-score</th>
          <th>Validation ROC-AUC</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>5</td><td>0.6293</td><td>0.5857</td><td>0.9141</td><td>0.7140</td><td>0.6869</td></tr>
        <tr><td>10</td><td>0.6621</td><td>0.6393</td><td>0.7630</td><td>0.6957</td><td>0.7190</td></tr>
        <tr><td>15</td><td>0.6678</td><td>0.6504</td><td>0.7432</td><td>0.6938</td><td>0.7206</td></tr>
        <tr><td>20</td><td>0.6744</td><td>0.6517</td><td>0.7662</td><td>0.7043</td><td>0.7153</td></tr>
        <tr style="background-color: #eff6ff; font-weight: 600;">
          <td>25 (Best max_depth)</td>
          <td>0.6766</td>
          <td>0.6576</td>
          <td>0.7533</td>
          <td>0.7022</td>
          <td>0.7056</td>
        </tr>
        <tr><td>30</td><td>0.6725</td><td>0.6477</td><td>0.7743</td><td>0.7053</td><td>0.6956</td></tr>
        <tr><td>50</td><td>0.6707</td><td>0.6468</td><td>0.7699</td><td>0.7030</td><td>0.6815</td></tr>
        <tr><td>None (ไม่จำกัดความลึก)</td><td>0.6609</td><td>0.6579</td><td>0.6840</td><td>0.6707</td><td>0.6607</td></tr>
      </tbody>
    </table>

    <div class="subsection-title">ผลการทดลองจริงบนชุดทดสอบ (Test Set: 4,902 ตัวอย่าง) ที่ค่า max_depth = 25:</div>
    <table>
      <thead>
        <tr>
          <th>Metric</th>
          <th>ผลการทดลองจริง (Result)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="text-left"><strong>Accuracy</strong></td>
          <td class="bold">0.6681 (66.81%)</td>
        </tr>
        <tr>
          <td class="text-left"><strong>Precision (Class 1)</strong></td>
          <td>0.6482 (64.82%)</td>
        </tr>
        <tr>
          <td class="text-left"><strong>Recall (Class 1)</strong></td>
          <td>0.7529 (75.29%)</td>
        </tr>
        <tr>
          <td class="text-left"><strong>F1-score (Class 1)</strong></td>
          <td>0.6966 (69.66%)</td>
        </tr>
        <tr>
          <td class="text-left"><strong>ROC-AUC</strong></td>
          <td>0.7124 (71.24%)</td>
        </tr>
      </tbody>
    </table>

    <div class="figure-container">
      <img src="REPLACE_IMG_DT_FEAT" alt="Decision Tree Feature Importance">
      <div class="figure-caption">รูปที่ 3: แผนภูมิแสดง Feature Importance 15 อันดับแรกของโมเดล Decision Tree</div>
    </div>
  </div>

  <!-- ==================== SECTION 10: MODEL 5 ==================== -->
  <div class="section">
    <div class="section-title">10. Model 5: BERT (Transformer-based Architecture)</div>
    <p>
      <strong>แนวคิดและหลักการ:</strong> BERT (Bidirectional Encoder Representations from Transformers) เป็นโมเดลภาษาขนาดใหญ่ที่ใช้สถาปัตยกรรม Transformer Encoder ซึ่งสามารถเรียนรู้บริบทประโยคแบบรอบทิศทางในระดับลึก (Self-Attention Mechanism) เพื่อนำมา Fine-tune สำหรับงาน Binary Text Classification
    </p>

    <div class="pipeline-box">Thai Text
   ↓
BERT Tokenizer (e.g. WangchanBERTa / mBERT)
   ↓
Input IDs + Attention Mask
   ↓
Pre-trained BERT Encoder
   ↓
[CLS] Token Representation
   ↓
Classification Head (Dense Layer + Sigmoid/Softmax)
   ↓
Class Prediction (0: ปกติ / 1: ซึมเศร้า)</div>

    <div class="subsection-title">สถานะและผลการทดลอง:</div>
    <blockquote>
      <strong>ส่วนของ BERT จะดำเนินการเพิ่มเติมและเติมผลการทดลองหลังจากพัฒนาและฝึกโมเดลเสร็จสิ้น</strong>
    </blockquote>

    <table>
      <thead>
        <tr>
          <th>Metric</th>
          <th>ผลการทดลอง (Result)</th>
        </tr>
      </thead>
      <tbody>
        <tr><td class="text-left"><strong>Accuracy</strong></td><td><span class="badge-pending">Pending</span></td></tr>
        <tr><td class="text-left"><strong>Precision</strong></td><td><span class="badge-pending">Pending</span></td></tr>
        <tr><td class="text-left"><strong>Recall</strong></td><td><span class="badge-pending">Pending</span></td></tr>
        <tr><td class="text-left"><strong>F1-score</strong></td><td><span class="badge-pending">Pending</span></td></tr>
      </tbody>
    </table>
  </div>

  <div class="page-break"></div>

  <!-- ==================== SECTION 11: EVALUATION METRICS ==================== -->
  <div class="section">
    <div class="section-title">11. ตัวชี้วัดประสิทธิภาพ (Evaluation Metrics)</div>
    <p>
      การประเมินผลการจำแนกข้อความใช้ตัวชี้วัดมาตรฐาน 4 ตัวหลัก โดยอ้างอิงจากตารางความสับสน (Confusion Matrix) ซึ่งมีองค์ประกอบดังนี้:
    </p>
    <ul>
      <li><strong>True Positive (TP):</strong> จำนวนข้อความที่บ่งชี้ภาวะซึมเศร้า (Class 1) และโมเดลทำนายได้ถูกต้องเป็น Class 1</li>
      <li><strong>True Negative (TN):</strong> จำนวนข้อความปกติ (Class 0) และโมเดลทำนายได้ถูกต้องเป็น Class 0</li>
      <li><strong>False Positive (FP):</strong> จำนวนข้อความปกติ (Class 0) แต่โมเดลทำนายผิดพลาดว่าเป็น Class 1 (เกิด False Alarm)</li>
      <li><strong>False Negative (FN):</strong> จำนวนข้อความที่บ่งชี้ภาวะซึมเศร้า (Class 1) แต่โมเดลทำนายผิดพลาดว่าเป็น Class 0 (พลาดเคสเสี่ยง)</li>
    </ul>

    <div class="equation-box">
      <div class="equation-title">1. Accuracy (ความถูกต้องรวม):</div>
      <div class="equation-formula">Accuracy = (TP + TN) / (TP + TN + FP + FN)</div>
      <p style="font-size: 11.5px; color: #475569; margin-top: 2px;">สัดส่วนของข้อความทั้งหมดที่โมเดลทำนายถูกต้องทั้ง Class 0 และ Class 1</p>
    </div>

    <div class="equation-box">
      <div class="equation-title">2. Precision (ความแม่นยำในการทำนายเชิงบวก):</div>
      <div class="equation-formula">Precision = TP / (TP + FP)</div>
      <p style="font-size: 11.5px; color: #475569; margin-top: 2px;">สัดส่วนความถูกต้องเมื่อโมเดลทำนายว่าเป็นภาวะซึมเศร้า (Class 1)</p>
    </div>

    <div class="equation-box">
      <div class="equation-title">3. Recall (ความสามารถในการตรวจจับ / Sensitivity):</div>
      <div class="equation-formula">Recall = TP / (TP + FN)</div>
      <p style="font-size: 11.5px; color: #475569; margin-top: 2px;">สัดส่วนของข้อความซึมเศร้าจริงทั้งหมดที่โมเดลสามารถตรวจจับได้</p>
    </div>

    <div class="equation-box">
      <div class="equation-title">4. F1-score (ค่าเฉลี่ยฮาร์มอนิกของ Precision และ Recall):</div>
      <div class="equation-formula">F1-score = 2 × (Precision × Recall) / (Precision + Recall)</div>
      <p style="font-size: 11.5px; color: #475569; margin-top: 2px;">ตัวชี้วัดความสมดุลระหว่างความแม่นยำและการตรวจจับ</p>
    </div>

    <p>
      <strong>ความสำคัญของ Recall สำหรับงานคัดกรองภาวะซึมเศร้า:</strong> ในบริบทของการคัดกรองสุขภาพจิต ค่า <strong>Recall ของ Class 1 มีความสำคัญอย่างยิ่งยวด</strong> เนื่องจากเป้าหมายหลักคือการลด False Negative (การปล่อยให้ผู้ที่มีภาวะเสี่ยงซึมเศร้าหลุดรอดไปโดยไม่ได้รับการช่วยเหลือ) ให้เหลือน้อยที่สุด
    </p>
  </div>

  <!-- ==================== SECTION 12: ผลการทดลองรวม ==================== -->
  <div class="section">
    <div class="section-title">12. ผลการทดลองรวม (Overall Experimental Results)</div>
    <p>
      ตารางเปรียบเทียบผลลัพธ์จริงที่ได้จากการประเมินบนชุดข้อมูลทดสอบ (Test Set: 4,902 ตัวอย่าง) ของทุกโมเดล:
    </p>

    <table>
      <thead>
        <tr>
          <th>โมเดล / สถาปัตยกรรม (Model)</th>
          <th>Accuracy</th>
          <th>Precision (Class 1)</th>
          <th>Recall (Class 1)</th>
          <th>F1-score (Class 1)</th>
          <th>ROC-AUC</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="text-left"><strong>1. Word2Vec + BiLSTM</strong></td>
          <td class="bold" style="background-color: #eff6ff; color: #1d4ed8;">0.7840 (78.40%)</td>
          <td>0.7505 (75.05%)</td>
          <td class="bold" style="background-color: #ecfdf5; color: #065f46;">0.8585 (85.85%)</td>
          <td class="bold" style="background-color: #eff6ff; color: #1d4ed8;">0.8009 (80.09%)</td>
          <td class="bold" style="background-color: #eff6ff; color: #1d4ed8;">0.8715 (87.15%)</td>
        </tr>
        <tr>
          <td class="text-left"><strong>2. BoW + Logistic Regression</strong></td>
          <td>0.7783 (77.83%)</td>
          <td>0.7574 (75.74%)</td>
          <td>0.8267 (82.67%)</td>
          <td>0.7905 (79.05%)</td>
          <td>0.8660 (86.60%)</td>
        </tr>
        <tr>
          <td class="text-left"><strong>3. TF-IDF + Logistic Regression</strong></td>
          <td>0.7815 (78.15%)</td>
          <td class="bold" style="background-color: #ecfdf5; color: #065f46;">0.7831 (78.31%)</td>
          <td>0.7860 (78.60%)</td>
          <td>0.7846 (78.46%)</td>
          <td>0.8676 (86.76%)</td>
        </tr>
        <tr>
          <td class="text-left"><strong>4. TF-IDF + Decision Tree</strong></td>
          <td>0.6681 (66.81%)</td>
          <td>0.6482 (64.82%)</td>
          <td>0.7529 (75.29%)</td>
          <td>0.6966 (69.66%)</td>
          <td>0.7124 (71.24%)</td>
        </tr>
        <tr>
          <td class="text-left"><strong>5. BERT (Transformer)</strong></td>
          <td><span class="badge-pending">Pending</span></td>
          <td><span class="badge-pending">Pending</span></td>
          <td><span class="badge-pending">Pending</span></td>
          <td><span class="badge-pending">Pending</span></td>
          <td><span class="badge-pending">Pending</span></td>
        </tr>
      </tbody>
    </table>

    <div class="figure-container">
      <img src="REPLACE_IMG_MASTER" alt="Overall Model Comparison">
      <div class="figure-caption">รูปที่ 4: แผนภูมิแท่งเปรียบเทียบผลการทดลองบน Test Set ทุกตัวชี้วัด</div>
    </div>
  </div>

  <div class="page-break"></div>

  <!-- ==================== SECTION 13: MODEL COMPARISON ==================== -->
  <div class="section">
    <div class="section-title">13. การวิเคราะห์เปรียบเทียบโมเดล (Model Comparison)</div>
    <p>
      การวิเคราะห์เชิงเปรียบเทียบความแตกต่างระหว่างคุณลักษณะของแต่ละโมเดลทั้งในแง่ของ Feature Extraction, ความเข้าใจบริบท, การเรียงลำดับคำ และความซับซ้อน:
    </p>

    <table>
      <thead>
        <tr>
          <th>Model</th>
          <th>Feature Type</th>
          <th>Context Awareness</th>
          <th>Sequence Modeling</th>
          <th>Complexity</th>
          <th>จุดเด่น / ข้อจำกัด</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="text-left"><strong>BoW + LR</strong></td>
          <td>Word Count (BoW)</td>
          <td>ต่ำ</td>
          <td>ไม่รองรับ</td>
          <td>ต่ำ</td>
          <td class="text-left">เทรนเร็วมาก แต่ไม่คำนึงถึงบริบทและลำดับคำ</td>
        </tr>
        <tr>
          <td class="text-left"><strong>TF-IDF + LR</strong></td>
          <td>Weighted TF-IDF</td>
          <td>ต่ำ</td>
          <td>ไม่รองรับ</td>
          <td>ต่ำ</td>
          <td class="text-left">ตัดคำรบกวนได้ดี Precision สูง แต่ไม่เข้าใจไวยากรณ์ประโยค</td>
        </tr>
        <tr>
          <td class="text-left"><strong>TF-IDF + DT</strong></td>
          <td>Weighted TF-IDF</td>
          <td>ต่ำ</td>
          <td>ไม่รองรับ</td>
          <td>ต่ำ-กลาง</td>
          <td class="text-left">อธิบายการตัดสินใจได้ง่าย แต่ประสิทธิภาพต่ำบน Sparse Text</td>
        </tr>
        <tr>
          <td class="text-left"><strong>Word2Vec + BiLSTM</strong></td>
          <td>Dense Embedding</td>
          <td>สูง</td>
          <td>รองรับ (2 ทิศทาง)</td>
          <td>สูง</td>
          <td class="text-left">จับความสัมพันธ์ของคำและความหมายแฝงได้ดี Recall สูงสุด</td>
        </tr>
        <tr>
          <td class="text-left"><strong>BERT</strong></td>
          <td>Contextual Token</td>
          <td>สูงมาก</td>
          <td>รองรับ (Self-Attention)</td>
          <td>สูงมาก</td>
          <td class="text-left">เข้าใจภาษาระดับ State-of-the-Art (อยู่ระหว่างดำเนินการ)</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- ==================== SECTION 14: BEST MODEL ==================== -->
  <div class="section">
    <div class="section-title">14. การเลือกโมเดลที่ดีที่สุด (Best Model Selection)</div>
    <p>
      จากการวิเคราะห์ผลการทดลองจริงที่มีอยู่ใน Notebook สามารถสรุปโมเดลที่ดีที่สุดในชุดการทดลองปัจจุบันได้ดังนี้:
    </p>
    <blockquote>
      จากผลการทดลองพบว่าโมเดล <strong>Word2Vec Embedding + BiLSTM</strong> ให้ผลลัพธ์ดีที่สุดในชุดการทดลองที่มีอยู่ โดยมี <strong>Accuracy = 0.7840 (78.40%)</strong>, <strong>Precision = 0.7505 (75.05%)</strong>, <strong>Recall = 0.8585 (85.85%)</strong> และ <strong>F1-score = 0.8009 (80.09%)</strong> รวมถึงมีค่า <strong>ROC-AUC สูงสุดที่ 0.8715</strong>
    </blockquote>
    <p>
      อย่างไรก็ตาม เมื่อพิจารณาตามข้อกำหนดของโครงงานที่ต้องเปรียบเทียบร่วมกับโมเดลกลุ่ม Transformer:
    </p>
    <blockquote>
      <strong>ยังไม่สามารถสรุป Best Model ขั้นสุดท้ายได้ เนื่องจากการทดลอง BERT ยังไม่เสร็จสมบูรณ์</strong>
    </blockquote>
  </div>

  <!-- ==================== SECTION 15: CONFUSION MATRIX ==================== -->
  <div class="section">
    <div class="section-title">15. เมทริกซ์ความสับสน (Confusion Matrix Analysis)</div>
    <p>
      เมทริกซ์ความสับสน (Confusion Matrix) แสดงโครงสร้างการจำแนกตัวอย่างจริงเทียบกับค่าทำนาย:
    </p>

    <div class="pipeline-box">                Predicted Class
                 0 (ปกติ)    1 (ซึมเศร้า)
Actual Class 0     TN           FP
             1     FN           TP</div>

    <div class="figure-container">
      <img src="REPLACE_IMG_CMS" alt="All Confusion Matrices">
      <div class="figure-caption">รูปที่ 5: เมทริกซ์ความสับสนจริงของทั้ง 4 โมเดลบน Test Set (จำนวนตัวอย่างรวม 4,902 ตัวอย่าง)</div>
    </div>

    <div class="subsection-title">การวิเคราะห์ False Positive และ False Negative:</div>
    <ul>
      <li><strong>BiLSTM + Word2Vec:</strong> ให้ค่า <code>FN ต่ำที่สุดเพียง 351 ตัวอย่าง</code> (ตรวจจับเคสซึมเศร้าสำเร็จ 2,130 จาก 2,481 ตัวอย่าง) มีความปลอดภัยสูงสุดในการนำไปเป็นเครื่องมือคัดกรองเบื้องต้น</li>
      <li><strong>Logistic Regression + TF-IDF:</strong> ให้ค่า <code>FP ต่ำที่สุดเพียง 540 ตัวอย่าง</code> (ทำนาย Class 0 ถูกต้อง 1,881 ตัวอย่าง) ลดปัญหาการแจ้งเตือนผิดพลาด (False Alarm)</li>
      <li><strong>Decision Tree + TF-IDF:</strong> มีความผิดพลาดทั้ง FP (1,014 ตัวอย่าง) และ FN (613 ตัวอย่าง) ในระดับสูงกว่าโมเดลอื่น</li>
    </ul>
  </div>

  <div class="page-break"></div>

  <!-- ==================== SECTION 16: HYPERPARAMETER TUNING ==================== -->
  <div class="section">
    <div class="section-title">16. การปรับจูนพารามิเตอร์ (Hyperparameter Tuning Summary)</div>
    <p>
      ตารางสรุปค่า Hyperparameters ที่ทำการทดลองปรับจูนจริงใน Notebook เพื่อค้นหาค่าที่เหมาะสมที่สุด:
    </p>

    <table>
      <thead>
        <tr>
          <th>ชื่อโมเดล (Model)</th>
          <th>พารามิเตอร์ที่ทำการจูน</th>
          <th>ช่วงค่าที่ทดสอบ (Values Tested)</th>
          <th>ค่าที่ดีที่สุด (Best Value)</th>
          <th>คะแนนอ้างอิงบน Validation Set</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="text-left"><strong>BoW + Logistic Regression</strong></td>
          <td>Regularization Strength (C)</td>
          <td>[0.001, 0.01, 0.1, 0.3, 0.5, 1.0, 3.0, 5.0, 10.0]</td>
          <td class="bold">C = 0.3</td>
          <td>Val Accuracy: 0.7770 (F1: 0.7906)</td>
        </tr>
        <tr>
          <td class="text-left"><strong>TF-IDF + Logistic Regression</strong></td>
          <td>Regularization Strength (C)</td>
          <td>[0.001, 0.01, 0.1, 0.3, 0.5, 1.0, 3.0, 5.0, 10.0]</td>
          <td class="bold">C = 3.0</td>
          <td>Val Accuracy: 0.7813 (F1: 0.7846)</td>
        </tr>
        <tr>
          <td class="text-left"><strong>TF-IDF + Decision Tree</strong></td>
          <td>Maximum Tree Depth (max_depth)</td>
          <td>[5, 10, 15, 20, 25, 30, 50, None]</td>
          <td class="bold">max_depth = 25</td>
          <td>Val Accuracy: 0.6766 (F1: 0.7022)</td>
        </tr>
        <tr>
          <td class="text-left"><strong>Word2Vec + BiLSTM</strong></td>
          <td>LSTM Units & Architecture</td>
          <td>LSTM units: 64, Dense: 32, Dropout: 0.3/0.2</td>
          <td class="bold">Fixed 64 units</td>
          <td>Val Accuracy: 0.7819 (Epoch 2 Checkpoint)</td>
        </tr>
      </tbody>
    </table>

    <div class="figure-container">
      <img src="REPLACE_IMG_TUNING" alt="Hyperparameter Tuning Curves">
      <div class="figure-caption">รูปที่ 6: กราฟแสดงความสัมพันธ์ระหว่างค่า Hyperparameter และคะแนนการประเมินบน Validation Set</div>
    </div>
  </div>

  <!-- ==================== SECTION 17: ข้อจำกัดของงาน ==================== -->
  <div class="section">
    <div class="section-title">17. ข้อจำกัดของงาน (Limitations)</div>
    <p>
      จากการวิเคราะห์เชิงลึกของชุดข้อมูลและกระบวนการทดลอง พบข้อจำกัดสำคัญดังนี้:
    </p>
    <ol>
      <li><strong>ความซับซ้อนของภาษาไทยบนสื่อออนไลน์:</strong> ข้อความภาษาไทยบน Social Media มีการใช้คำแสลง คำย่อ การเขียนสะกดคำแบบไม่เป็นทางการ และการละเว้นเครื่องหมายวรรคตอน ซึ่งอาจส่งผลต่อความแม่นยำในการตัดคำ (Word Tokenization Errors)</li>
      <li><strong>ข้อความสั้นและบริบทจำกัด:</strong> ข้อความบางส่วนในชุดข้อมูลมีความยาวสั้นมาก (เช่น มีความยาวเพียง 3–10 ตัวอักษร) ทำให้ไม่มีข้อมูลบริบทเพียงพอสำหรับแบบจำลองในการตัดสินอารมณ์ที่แท้จริง</li>
      <li><strong>ข้อจำกัดด้านบริบทของโมเดล BoW และ TF-IDF:</strong> โมเดลกลุ่ม Bag-of-Words และ TF-IDF ไม่สามารถเข้าใจลำดับของคำ (Word Order) และความหมายที่เปลี่ยนไปตามการใช้คำปฏิเสธ (Negation Handling) เช่น ความแตกต่างระหว่างคำว่า "อยากตาย" กับ "ไม่อยากตาย"</li>
      <li><strong>ทรัพยากรการประมวลผลของโมเดล Deep Learning:</strong> โครงข่าย BiLSTM ใช้เวลาและทรัพยากรในการฝึกมากกว่า Linear Models อย่างมีนัยสำคัญ</li>
      <li><strong>การทดลองของโมเดล BERT ยังไม่สมบูรณ์:</strong> แบบจำลอง Transformer-based Language Model (BERT) ยังอยู่ระหว่างขั้นตอนการพัฒนา ทำให้ยังไม่สามารถเปรียบเทียบผลลัพธ์กับโมเดลยุคปัจจุบันได้อย่างครบถ้วน</li>
    </ol>
  </div>

  <!-- ==================== SECTION 18: สรุป ==================== -->
  <div class="section">
    <div class="section-title">18. บทสรุปโครงงาน (Conclusion)</div>
    <p>
      กลุ่มที่ 10 (Group 10) ได้ดำเนินการศึกษา ออกแบบ และเปรียบเทียบแบบจำลองการจำแนกข้อความภาษาไทยเพื่อระบุภาวะซึมเศร้า ครอบคลุมตั้งแต่แบบจำลอง Traditional Machine Learning (Logistic Regression, Decision Tree) ไปจนถึง Deep Sequential Model (BiLSTM ร่วมกับ Pre-trained Word2Vec) บนชุดข้อมูลขนาด 32,676 ข้อความ
    </p>
    <p>
      จากผลการทดลองจริงบนชุดทดสอบ (Test Set: 4,902 ตัวอย่าง) สามารถสรุปสาระสำคัญได้ดังนี้:
    </p>
    <ul>
      <li><strong>BiLSTM + Word2Vec</strong> เป็นโมเดลที่มีประสิทธิภาพสูงสุดในชุดการทดลองปัจจุบัน โดยได้ <strong>Accuracy = 78.40%</strong>, <strong>Recall = 85.85%</strong>, <strong>F1-score = 80.09%</strong> และ <strong>ROC-AUC = 87.15%</strong> เนื่องจากสามารถจับลำดับคำและความสัมพันธ์เชิงบริบทสองทิศทางได้ดี</li>
      <li><strong>Logistic Regression + TF-IDF (C = 3.0)</strong> เป็นโมเดลเชิงเส้นที่มีความสมดุลสูงมาก โดยให้ค่า <strong>Precision สูงที่สุดที่ 78.31%</strong> และ <strong>Accuracy = 78.15%</strong> ด้วยข้อได้เปรียบด้านความเร็วในการประมวลผล</li>
      <li><strong>Logistic Regression + BoW (C = 0.3)</strong> ให้ผลลัพธ์ในเกณฑ์ดี (Accuracy = 77.83%, Recall = 82.67%)</li>
      <li><strong>Decision Tree + TF-IDF (max_depth = 25)</strong> มีประสิทธิภาพต่ำที่สุดในกลุ่มการทดลอง (Accuracy = 66.81%, F1 = 69.66%) เนื่องจากข้อจำกัดในการแบ่งข้อมูลแบบ Axis-aligned บนเวกเตอร์ข้อความที่มีมิติสูงและเบาบาง (High-dimensional Sparse Data)</li>
      <li><strong>BERT:</strong> อยู่ในสถานะ Pending ซึ่งจะดำเนินการเพิ่มเติมในลำดับถัดไปเพื่อนำมาเปรียบเทียบและสรุป Best Model ขั้นสุดท้ายต่อไป</li>
    </ul>
  </div>

</body>
</html>
"""

# Replace placeholders
final_html = html_template.replace("REPLACE_IMG_BILSTM_ARCH", img_bilstm_arch) \
                          .replace("REPLACE_IMG_BILSTM_CURVES", img_bilstm_curves) \
                          .replace("REPLACE_IMG_DT_FEAT", img_dt_feat) \
                          .replace("REPLACE_IMG_MASTER", img_master) \
                          .replace("REPLACE_IMG_CMS", img_cms) \
                          .replace("REPLACE_IMG_TUNING", img_tuning)

with open("Group_10.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("Group_10.html (Academic Report Version) generated successfully!")

# Compile to PDF using Edge headless
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
html_path = os.path.abspath("Group_10.html")
pdf_path = os.path.abspath("Group_10.pdf")

cmd = [
    edge_path,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={pdf_path}",
    f"file:///{html_path}"
]

print("Compiling Academic Report to PDF with Edge headless...")
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0 and os.path.exists(pdf_path):
    print(f"Successfully created {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes)")
    
    # Also create aliases
    for alias in ["กลุ่ม 10.pdf", "Group10.pdf", "Project_1_Text_Classification_Group_10.pdf"]:
        dst_path = os.path.abspath(alias)
        with open(pdf_path, "rb") as src, open(dst_path, "wb") as dst:
            dst.write(src.read())
        print(f"Created alias: {alias} (Size: {os.path.getsize(dst_path)} bytes)")
else:
    print("Error generating PDF:", res.stderr)
