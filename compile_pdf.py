import os
import base64
import subprocess

def img_to_base64(path):
    with open(path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode('utf-8')
        ext = os.path.splitext(path)[1].lower().replace('.', '')
        if ext == 'jpg': ext = 'jpeg'
        return f"data:image/{ext};base64,{encoded}"

# Load high-resolution charts as base64
img_master = img_to_base64("report_assets/master_comparison.png")
img_bilstm_curves = img_to_base64("report_assets/bilstm_learning_curves.png")
img_cms = img_to_base64("report_assets/all_confusion_matrices.png")
img_tuning = img_to_base64("report_assets/hyperparameter_tuning.png")
img_dt_feat = img_to_base64("report_assets/dt_feature_importance.png")
img_bilstm_arch = img_to_base64("report_assets/bilstm_architecture.png")

html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<title>รายงานการนำเสนอโครงงาน: การจำแนกข้อความภาวะซึมเศร้า (Group 10)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Prompt:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Sarabun:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
<style>
  @page {{
    size: A4 portrait;
    margin: 10mm 12mm 12mm 12mm;
  }}

  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}

  body {{
    font-family: 'Sarabun', 'Leelawadee UI', Tahoma, sans-serif;
    font-size: 13px;
    line-height: 1.5;
    color: #1e293b;
    background-color: #ffffff;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}

  h1, h2, h3, h4, .heading-font {{
    font-family: 'Prompt', 'Leelawadee UI', Tahoma, sans-serif;
    font-weight: 600;
  }}

  .header-card {{
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #0369a1 100%);
    color: #ffffff;
    padding: 20px 24px;
    border-radius: 10px;
    margin-bottom: 14px;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.12);
  }}

  .badge-container {{
    display: flex;
    gap: 8px;
    margin-bottom: 10px;
  }}

  .badge {{
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 10.5px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}

  .badge-primary {{
    background: rgba(255, 255, 255, 0.2);
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 0.3);
  }}

  .badge-accent {{
    background: #10b981;
    color: #ffffff;
  }}

  .header-title {{
    font-size: 22px;
    font-weight: 700;
    line-height: 1.25;
    margin-bottom: 4px;
  }}

  .header-subtitle {{
    font-size: 13px;
    color: #cbd5e1;
    font-weight: 400;
    margin-bottom: 10px;
  }}

  .header-meta {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid rgba(255, 255, 255, 0.2);
    padding-top: 10px;
    font-size: 11.5px;
    color: #e2e8f0;
  }}

  /* KPI Grid */
  .kpi-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin-bottom: 14px;
  }}

  .kpi-card {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 10px 12px;
    text-align: center;
    border-top: 3.5px solid #2563eb;
  }}

  .kpi-card.accent {{ border-top-color: #10b981; }}
  .kpi-card.purple {{ border-top-color: #8b5cf6; }}
  .kpi-card.amber {{ border-top-color: #f59e0b; }}

  .kpi-label {{
    font-size: 10.5px;
    color: #64748b;
    font-weight: 600;
    text-transform: uppercase;
    margin-bottom: 3px;
  }}

  .kpi-value {{
    font-family: 'Prompt', sans-serif;
    font-size: 19px;
    font-weight: 700;
    color: #0f172a;
  }}

  .kpi-subtext {{
    font-size: 10px;
    color: #64748b;
    margin-top: 2px;
  }}

  /* Section Styling */
  .section {{
    margin-bottom: 16px;
    page-break-inside: avoid;
  }}

  .section-title {{
    font-size: 15px;
    color: #0f172a;
    border-left: 4px solid #1e3a8a;
    padding-left: 8px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}

  .section-title-tag {{
    font-size: 10.5px;
    background: #e2e8f0;
    color: #475569;
    padding: 2px 7px;
    border-radius: 4px;
    font-weight: normal;
  }}

  /* Content Cards */
  .card {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 13px 15px;
    margin-bottom: 12px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
    page-break-inside: avoid;
  }}

  .card-header {{
    font-size: 13.5px;
    font-weight: 600;
    color: #1e3a8a;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
  }}

  p {{
    margin-bottom: 7px;
    text-align: justify;
  }}

  /* Tables */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0 10px 0;
    font-size: 11.5px;
  }}

  th {{
    background-color: #f1f5f9;
    color: #1e293b;
    font-weight: 600;
    text-align: center;
    padding: 6px 8px;
    border: 1px solid #cbd5e1;
    font-family: 'Prompt', sans-serif;
  }}

  td {{
    padding: 6px 8px;
    border: 1px solid #e2e8f0;
    text-align: center;
  }}

  tr:nth-child(even) {{
    background-color: #f8fafc;
  }}

  td.text-left {{
    text-align: left;
  }}

  td.highlight {{
    background-color: #ecfdf5;
    color: #065f46;
    font-weight: 700;
  }}

  td.best-score {{
    background-color: #eff6ff;
    color: #1d4ed8;
    font-weight: 700;
  }}

  /* Architecture Box */
  .arch-flow {{
    display: flex;
    flex-direction: column;
    gap: 6px;
    margin: 10px 0;
  }}

  .arch-step {{
    display: flex;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 3.5px solid #0284c7;
    border-radius: 5px;
    padding: 6px 10px;
  }}

  .arch-step-title {{
    width: 155px;
    font-weight: 600;
    color: #0369a1;
    font-size: 11.5px;
  }}

  .arch-step-desc {{
    flex: 1;
    font-size: 11px;
    color: #334155;
  }}

  /* Images */
  .img-container {{
    text-align: center;
    margin: 8px 0;
    page-break-inside: avoid;
  }}

  .img-container img {{
    max-width: 100%;
    height: auto;
    border-radius: 6px;
    border: 1px solid #e2e8f0;
  }}

  .img-caption {{
    font-size: 10.5px;
    color: #64748b;
    margin-top: 4px;
    font-style: italic;
  }}

  /* Two Column Layout */
  .two-col {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 10px;
    page-break-inside: avoid;
  }}

  /* Alert / Insight Box */
  .insight-box {{
    background-color: #f0fdf4;
    border-left: 4px solid #10b981;
    border-radius: 6px;
    padding: 8px 12px;
    margin: 8px 0;
    font-size: 11.5px;
    color: #166534;
  }}

  .insight-box.info {{
    background-color: #eff6ff;
    border-left-color: #3b82f6;
    color: #1e40af;
  }}

  .insight-box.warning {{
    background-color: #fffbeb;
    border-left-color: #f59e0b;
    color: #92400e;
  }}

  .insight-title {{
    font-weight: 700;
    margin-bottom: 2px;
    display: flex;
    align-items: center;
    gap: 6px;
    font-family: 'Prompt', sans-serif;
  }}

  /* Page Break Rule */
  .page-break {{
    page-break-before: always;
    margin-top: 10px;
  }}

  /* Footer */
  .report-footer {{
    margin-top: 15px;
    padding-top: 8px;
    border-top: 1px solid #e2e8f0;
    display: flex;
    justify-content: space-between;
    font-size: 10px;
    color: #94a3b8;
  }}

  ul, ol {{
    padding-left: 18px;
    margin-bottom: 6px;
    font-size: 12px;
  }}

  li {{
    margin-bottom: 2px;
  }}

  code {{
    font-family: Consolas, Monaco, monospace;
    background: #f1f5f9;
    padding: 1px 4px;
    border-radius: 3px;
    font-size: 11px;
    color: #0f172a;
  }}
</style>
</head>
<body>

  <!-- ==================== PAGE 1 ==================== -->
  <div class="header-card">
    <div class="badge-container">
      <span class="badge badge-accent">NLP Project 1</span>
      <span class="badge badge-primary">Technical Presentation Report</span>
      <span class="badge badge-primary">Group 10 (กลุ่มที่ 10)</span>
    </div>
    <div class="header-title">การจำแนกข้อความภาษาไทยเพื่อคัดกรองภาวะซึมเศร้า</div>
    <div class="header-subtitle">Thai Text Classification for Depression Detection: Architecture, Hyperparameter Tuning & Comparative Analysis</div>
    <div class="header-meta">
      <div><strong>กลุ่มผู้จัดทำ:</strong> กลุ่มที่ 10 (Group 10)</div>
      <div><strong>วิชา:</strong> การประมวลผลภาษาธรรมชาติ (Natural Language Processing)</div>
      <div><strong>ชุดข้อมูล:</strong> Depression_Dataset.csv (32,676 ข้อความ)</div>
    </div>
  </div>

  <!-- KPI CARDS -->
  <div class="kpi-grid">
    <div class="kpi-card accent">
      <div class="kpi-label">Best Accuracy</div>
      <div class="kpi-value">78.40%</div>
      <div class="kpi-subtext">BiLSTM + Word2Vec</div>
    </div>
    <div class="kpi-card purple">
      <div class="kpi-label">Highest Recall</div>
      <div class="kpi-value">85.85%</div>
      <div class="kpi-subtext">คัดกรองเคสซึมเศร้าได้สูงสุด</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Best Precision</div>
      <div class="kpi-value">78.31%</div>
      <div class="kpi-subtext">LR + TF-IDF (C = 3.0)</div>
    </div>
    <div class="kpi-card amber">
      <div class="kpi-label">Total Dataset</div>
      <div class="kpi-value">32,676</div>
      <div class="kpi-subtext">Balanced Classes (~50/50)</div>
    </div>
  </div>

  <!-- SECTION 1: PROBLEM & DATASET -->
  <div class="section">
    <div class="section-title">
      <span>1. บทนำและภาพรวมชุดข้อมูล (Problem Formulation & Dataset Overview)</span>
      <span class="section-title-tag">Data Preparation</span>
    </div>

    <div class="card">
      <p>
        <strong>ที่มาและความสำคัญ:</strong> ภาวะซึมเศร้า (Depression) เป็นปัญหาสุขภาพจิตที่ส่งผลกระทบต่อประชากรจำนวนมาก การตรวจจับสัญญาณความเสี่ยงผ่านข้อความบนสื่อสังคมออนไลน์เป็นงานวิจัยสำคัญในกลุ่ม <em>Natural Language Processing (NLP)</em> โดยโครงงานนี้มุ่งเน้นการพัฒนาระบบ <strong>Binary Text Classification</strong> เพื่อจำแนกข้อความภาษาไทยระหว่าง <code>Class 0 (ข้อความปกติ / Non-Depression)</code> และ <code>Class 1 (ข้อความบ่งชี้ภาวะซึมเศร้า / Depression)</code>
      </p>
      
      <div class="two-col" style="margin-top: 8px;">
        <div>
          <h4 style="color: #1e3a8a; font-size: 12px; margin-bottom: 5px;">กระบวนการทำความสะอาดข้อมูล (Text Cleaning Pipeline):</h4>
          <ul>
            <li><strong>ลบ URL / Web Links:</strong> ตัด Regular Expression <code>https?://\S+|www\.\S+</code> ออกเพื่อตัดสัญญาณรบกวน</li>
            <li><strong>จัดการช่องว่างส่วนเกิน:</strong> รวม White-space และตัดช่องว่างหัว-ท้ายด้วย <code>strip()</code></li>
            <li><strong>ตรวจสอบ Duplicate & Empty Text:</strong> ตรวจสอบแถวที่ซ้ำซ้อนและไม่มีข้อความว่างเปล่า (Empty Text = 0)</li>
            <li><strong>การแบ่งข้อมูล (Split Strategy):</strong> แบ่งแบบ 70% Train, 15% Validation, 15% Test</li>
          </ul>
        </div>

        <div>
          <h4 style="color: #1e3a8a; font-size: 12px; margin-bottom: 5px;">ตารางแจกแจงชุดข้อมูล (Data Split Distribution):</h4>
          <table>
            <thead>
              <tr>
                <th>ชุดข้อมูล (Set)</th>
                <th>จำนวนแถว</th>
                <th>ปกติ (0)</th>
                <th>ซึมเศร้า (1)</th>
                <th>สัดส่วน</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="text-left"><strong>Train Set</strong></td>
                <td>22,873</td>
                <td>11,297 (49.4%)</td>
                <td>11,576 (50.6%)</td>
                <td>70.0%</td>
              </tr>
              <tr>
                <td class="text-left"><strong>Validation Set</strong></td>
                <td>4,901</td>
                <td>2,420 (49.4%)</td>
                <td>2,481 (50.6%)</td>
                <td>15.0%</td>
              </tr>
              <tr>
                <td class="text-left"><strong>Test Set</strong></td>
                <td>4,902</td>
                <td>2,421 (49.4%)</td>
                <td>2,481 (50.6%)</td>
                <td>15.0%</td>
              </tr>
              <tr style="font-weight: bold; background-color: #f1f5f9;">
                <td class="text-left">รวมทั้งหมด (Total)</td>
                <td>32,676</td>
                <td>16,138 (49.39%)</td>
                <td>16,538 (50.61%)</td>
                <td>100.0%</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <!-- SECTION 2: BI-LSTM ARCHITECTURE -->
  <div class="section">
    <div class="section-title">
      <span>2. เทคนิคและโครงสร้างสถาปัตยกรรมโมเดล (Techniques & Architectures)</span>
      <span class="section-title-tag">Part 1: Deep Learning</span>
    </div>

    <!-- TECHNIQUE 1: BiLSTM + Word2Vec -->
    <div class="card">
      <div class="card-header">
        <span>2.1 เทคนิคที่ 1: Deep Learning — BiLSTM + Word2Vec Embedding (Sequential Architecture)</span>
      </div>
      <p>
        โมเดล Deep Learning ลำดับเวลา (Sequential Architecture) ที่ผสานการตัดคำภาษาไทยด้วย <strong>PyThaiNLP (engine: newmm)</strong> ร่วมกับการเทรน <strong>Word2Vec (Skip-gram, sg=1)</strong> บนคลังคำศัพท์ของชุดข้อมูล เพื่อแปลงคำเป็น Dense Vector ขนาด 100 มิติ โดยสามารถเรียนรู้ความสัมพันธ์ของบริบทคำทั้งทิศทางหน้าและหลัง (Bidirectional Context)
      </p>

      <div class="img-container">
        <img src="{img_bilstm_arch}" alt="BiLSTM Architecture Diagram">
        <div class="img-caption">รูปที่ 1: แผนผังสถาปัตยกรรมโครงข่ายประสาทเทียม Bidirectional LSTM (BiLSTM Pipeline)</div>
      </div>

      <div class="arch-flow">
        <div class="arch-step">
          <div class="arch-step-title">1. Tokenization & Mapping</div>
          <div class="arch-step-desc">ตัดคำด้วย PyThaiNLP, คำนวณความยาวข้อความ (Mean=16.59 คำ, 99th%=89 คำ) กำหนด <code>MAX_LEN = 100</code> และสร้าง Mapping Dict (Vocab: 9,200 คำ + PAD (0) + UNK (1) = 9,202 โทเค็น)</div>
        </div>
        <div class="arch-step">
          <div class="arch-step-title">2. Embedding Matrix</div>
          <div class="arch-step-desc">สร้าง Weight Matrix ขนาด <code>(9202, 100)</code> จาก Pre-trained Word2Vec, กำหนด <code>mask_zero=True</code> เพื่อข้าม Padding และเปิด <code>trainable=True</code> เพื่อ Fine-tuning</div>
        </div>
        <div class="arch-step">
          <div class="arch-step-title">3. Bidirectional LSTM</div>
          <div class="arch-step-desc">ใช้ LSTM 64 หน่วย ทั้งทิศทาง Forward และ Backward ได้ Hidden Representation ขนาด 128 มิติ เพื่อจับความสัมพันธ์ระยะยาวของประโยค</div>
        </div>
        <div class="arch-step">
          <div class="arch-step-title">4. Regularization & Dense</div>
          <div class="arch-step-desc">คั่นด้วย <code>Dropout(0.30)</code> → <code>Dense(32, activation='relu')</code> → <code>Dropout(0.20)</code> → <code>Dense(1, activation='sigmoid')</code></div>
        </div>
        <div class="arch-step">
          <div class="arch-step-title">5. Training Hyperparameters</div>
          <div class="arch-step-desc">Optimizer: Adam (lr=0.001), Loss: Binary Crossentropy, Batch Size: 64, Callbacks: <code>EarlyStopping(patience=3)</code> และ <code>ReduceLROnPlateau(factor=0.5, patience=2)</code></div>
        </div>
      </div>

      <div class="img-container">
        <img src="{img_bilstm_curves}" alt="BiLSTM Learning Curves">
        <div class="img-caption">รูปที่ 2: กราฟแสดงผลการเรียนรู้ (Loss & Accuracy Learning Curves) ตลอด 5 Epochs ของโมเดล BiLSTM</div>
      </div>
    </div>
  </div>

  <div class="report-footer">
    <div><strong>NLP Project 1:</strong> Text Classification for Depression Detection</div>
    <div>กลุ่มที่ 10 (Group 10)</div>
    <div>หน้า 1 / 3</div>
  </div>

  <!-- ==================== PAGE 2 ==================== -->
  <div class="page-break"></div>

  <div class="section">
    <div class="section-title">
      <span>2. เทคนิคและโครงสร้างสถาปัตยกรรมโมเดล (ต่อ)</span>
      <span class="section-title-tag">Part 2: Linear & Tree-based Models</span>
    </div>

    <!-- TECHNIQUE 2 & 3: Logistic Regression (BoW vs TF-IDF) -->
    <div class="card">
      <div class="card-header">
        <span>2.2 เทคนิคที่ 2 & 3: Linear Models — Logistic Regression (BoW vs TF-IDF)</span>
      </div>
      <p>
        การสกัดฟีเจอร์ระดับคำ (N-gram Features) ผสานกับการจำแนกด้วย Linear Classifier ผ่านฟังก์ชัน Sigmoid และ L₂ Regularization โดยทำการเปรียบเทียบระหว่างสองวิธีสกัดฟีเจอร์:
      </p>

      <div class="two-col">
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px;">
          <h4 style="color: #059669; font-size: 12px; margin-bottom: 5px;">เทคนิคที่ 2: Bag of Words (BoW)</h4>
          <ul style="font-size: 11.5px;">
            <li><strong>Feature Extractor:</strong> <code>CountVectorizer</code></li>
            <li><strong>N-gram Range:</strong> Unigram + Bigram <code>(1, 2)</code></li>
            <li><strong>Min Document Frequency:</strong> <code>min_df = 2</code></li>
            <li><strong>จำนวน Features:</strong> 55,860 มิติ</li>
            <li><strong>Tuning Hyperparameter:</strong> ค้นหา C ∈ [0.001, ..., 10.0] พบว่าค่าที่ดีที่สุดคือ <strong>C = 0.3</strong> (Validation Accuracy: 77.70%)</li>
          </ul>
        </div>

        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px;">
          <h4 style="color: #2563eb; font-size: 12px; margin-bottom: 5px;">เทคนิคที่ 3: TF-IDF Representation</h4>
          <ul style="font-size: 11.5px;">
            <li><strong>Feature Extractor:</strong> <code>TfidfVectorizer</code></li>
            <li><strong>Scaling:</strong> <code>sublinear_tf = True</code> (1 + log(tf))</li>
            <li><strong>N-gram Range:</strong> Unigram + Bigram <code>(1, 2)</code></li>
            <li><strong>จำนวน Features:</strong> 55,860 มิติ</li>
            <li><strong>Tuning Hyperparameter:</strong> ค้นหา C ∈ [0.001, ..., 10.0] พบว่าค่าที่ดีที่สุดคือ <strong>C = 3.0</strong> (Validation Accuracy: 78.13%)</li>
          </ul>
        </div>
      </div>

      <div class="insight-box info">
        <div class="insight-title">การวิเคราะห์คำบ่งชี้สำคัญจากค่าน้ำหนักสัมประสิทธิ์โมเดล (Top Informative Coefficients):</div>
        <div style="margin-top: 3px; font-size: 11px;">
          <strong>• ข้อความบ่งชี้ภาวะซึมเศร้า (Class 1):</strong> ยา, หมอ, เรา, ดรีม, คุณหมอ, โรค, อาการ, ซึมเศร้า, ป่วย, ฆ่าตัวตาย, การรักษา, ทำร้าย, จิตแพทย์<br>
          <strong>• ข้อความปกติ (Class 0):</strong> เธอ, ความรัก, เติบโต, พี่, เขา, กบ, ดอกไม้, แฮงค์, รัก, ยาย, ครู, เมี่ยง
        </div>
      </div>
    </div>

    <!-- TECHNIQUE 4: Decision Tree -->
    <div class="card">
      <div class="card-header">
        <span>2.3 เทคนิคที่ 4: Tree-based Model — Decision Tree + TF-IDF</span>
      </div>
      <p>
        โมเดลจำแนกแบบต้นไม้การตัดสินใจ (Non-linear Rule-based Model) บนเวกเตอร์ TF-IDF (47,578 ฟีเจอร์) มีจุดเด่นด้านความสามารถในการอธิบายผลลัพธ์ (Explainability / Interpretability) ผ่านค่า Gini Impurity และ Feature Importance
      </p>

      <div class="two-col">
        <div>
          <h4 style="color: #d97706; font-size: 12px; margin-bottom: 5px;">การปรับจูนความลึก (Hyperparameter Tuning):</h4>
          <ul style="font-size: 11.5px;">
            <li><strong>Parameter Grid:</strong> <code>max_depth</code> ∈ [5, 10, 15, 20, 25, 30, 50, None]</li>
            <li><strong>Best max_depth:</strong> <strong>25</strong> (Validation Acc = 67.66%, ใบ 899 ใบ)</li>
            <li><strong>การป้องกัน Overfitting:</strong> หากไม่จำกัดความลึก (<code>None</code>) ต้นไม้จะจำเพาะกับ Train Set ทำให้ Validation Acc ตกลงเหลือ 66.09%</li>
          </ul>
        </div>

        <div>
          <div class="img-container" style="margin: 0;">
            <img src="{img_dt_feat}" alt="Decision Tree Top Features" style="max-height: 170px;">
            <div class="img-caption">รูปที่ 3: Feature Importance 15 อันดับแรกของ Decision Tree</div>
          </div>
        </div>
      </div>

      <div class="img-container">
        <img src="{img_tuning}" alt="Hyperparameter Tuning Curves">
        <div class="img-caption">รูปที่ 4: กราฟแสดงผลการปรับจูน Hyperparameter: (ซ้าย) ค่า C ของ Logistic Regression, (ขวา) ค่า max_depth ของ Decision Tree</div>
      </div>
    </div>
  </div>

  <div class="report-footer">
    <div><strong>NLP Project 1:</strong> Text Classification for Depression Detection</div>
    <div>กลุ่มที่ 10 (Group 10)</div>
    <div>หน้า 2 / 3</div>
  </div>

  <!-- ==================== PAGE 3 ==================== -->
  <div class="page-break"></div>

  <!-- SECTION 3: EXPERIMENTAL RESULTS -->
  <div class="section">
    <div class="section-title">
      <span>3. ผลลัพธ์การทดลองและการเปรียบเทียบเชิงลึก (Results & Evaluation)</span>
      <span class="section-title-tag">Test Set (4,902 samples)</span>
    </div>

    <div class="card">
      <h4 style="color: #0f172a; font-size: 13px; margin-bottom: 6px;">ตารางสรุปผลการประเมินประสิทธิภาพทุกโมเดลบนชุดทดสอบ (Master Comparison Table):</h4>
      <table>
        <thead>
          <tr>
            <th>ชื่อโมเดล / สถาปัตยกรรม</th>
            <th>Accuracy</th>
            <th>Precision</th>
            <th>Recall</th>
            <th>F1-Score</th>
            <th>ROC-AUC</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="text-left"><strong>1. BiLSTM + Word2Vec</strong></td>
            <td class="best-score">0.7840 (78.40%)</td>
            <td>0.7505</td>
            <td class="highlight">0.8585 (85.85%)</td>
            <td class="best-score">0.8009 (80.09%)</td>
            <td class="best-score">0.8715 (87.15%)</td>
          </tr>
          <tr>
            <td class="text-left"><strong>2. Logistic Regression + BoW</strong></td>
            <td>0.7783 (77.83%)</td>
            <td>0.7574</td>
            <td>0.8267 (82.67%)</td>
            <td>0.7905 (79.05%)</td>
            <td>0.8660 (86.60%)</td>
          </tr>
          <tr>
            <td class="text-left"><strong>3. Logistic Regression + TF-IDF</strong></td>
            <td>0.7815 (78.15%)</td>
            <td class="best-score">0.7831 (78.31%)</td>
            <td>0.7860 (78.60%)</td>
            <td>0.7846 (78.46%)</td>
            <td>0.8676 (86.76%)</td>
          </tr>
          <tr>
            <td class="text-left"><strong>4. Decision Tree + TF-IDF</strong></td>
            <td>0.6681 (66.81%)</td>
            <td>0.6482</td>
            <td>0.7529 (75.29%)</td>
            <td>0.6966 (69.66%)</td>
            <td>0.7124 (71.24%)</td>
          </tr>
        </tbody>
      </table>

      <div class="img-container">
        <img src="{img_master}" alt="Master Comparison Bar Chart">
        <div class="img-caption">รูปที่ 5: แผนภูมิแท่งเปรียบเทียบค่า Metrics 5 ด้านของทั้ง 4 โมเดลบนชุดข้อมูลทดสอบ (Test Set)</div>
      </div>
    </div>

    <div class="card">
      <h4 style="color: #0f172a; font-size: 13px; margin-bottom: 6px;">การวิเคราะห์เมทริกซ์ความสับสน (Confusion Matrices Analysis):</h4>
      <div class="img-container">
        <img src="{img_cms}" alt="Confusion Matrices">
        <div class="img-caption">รูปที่ 6: เมทริกซ์ความสับสน (Confusion Matrices) ทั้ง 4 โมเดลบน Test Set (จำนวนตัวอย่างรวม 4,902 ตัวอย่าง)</div>
      </div>

      <div class="two-col" style="margin-top: 8px;">
        <div class="insight-box">
          <div class="insight-title">จุดเด่นด้าน Recall ของ BiLSTM:</div>
          <p style="font-size: 11px; margin-bottom: 0;">
            BiLSTM ทำนายผู้มีภาวะซึมเศร้าถูกต้องถึง <strong>2,130 เคสจาก 2,481 เคส</strong> (False Negative ต่ำเพียง 351 เคส) ส่งผลให้ Recall สูงถึง <strong>85.85%</strong> มีความปลอดภัยสูงสุดสำหรับเครื่องมือคัดกรองเบื้องต้น (Screening Tool)
          </p>
        </div>

        <div class="insight-box info">
          <div class="insight-title">ความแม่นยำสูง (Precision) ของ LR + TF-IDF:</div>
          <p style="font-size: 11px; margin-bottom: 0;">
            Logistic Regression ร่วมกับ TF-IDF มีอัตราการเตือนผิดพลาด (False Positive) ต่ำสุด โดยทายผิดเป็นซึมเศร้าเพียง 540 เคส ส่งผลให้มีค่า <strong>Precision สูงสุดที่ 78.31%</strong> และมีความสมดุลสูงสุดระหว่าง Precision และ Recall
          </p>
        </div>
      </div>
    </div>
  </div>

  <!-- SECTION 4: DISCUSSION & CONCLUSION -->
  <div class="section">
    <div class="section-title">
      <span>4. การอภิปรายผลและบทสรุป (Discussion, Clinical Implications & Conclusion)</span>
      <span class="section-title-tag">Final Summary</span>
    </div>

    <div class="card">
      <div class="card-header">
        <span>4.1 การวิเคราะห์เปรียบเทียบเชิงลึก (In-Depth Technical Insights)</span>
      </div>
      
      <ol style="font-size: 11.5px; line-height: 1.55;">
        <li>
          <strong>ทำไม BiLSTM ถึงให้ผลลัพธ์โดยรวมดีที่สุด (Accuracy 78.40%, F1 80.09%, AUC 87.15%):</strong>
          โมเดล Deep Sequential สามารถเข้าใจ <em>ลำดับของคำ (Word Order)</em> และ <em>บริบทความหมาย (Contextual Semantics)</em> ผ่าน Word2Vec Dense Vector ซึ่งข้อความแสดงภาวะซึมเศร้ามักมีการใช้คำปฏิเสธซับซ้อน (เช่น "ไม่อยากมีชีวิตอยู่", "รู้สึกว่างเปล่า") ซึ่งโมเดลแบบ Bag of Words ไม่สามารถจับลำดับคำได้สมบูรณ์เท่า
        </li>
        <li>
          <strong>การเปรียบเทียบ BoW vs TF-IDF บน Logistic Regression:</strong>
          TF-IDF ช่วยลดทอนน้ำหนักของคำทั่วไป (Stop Words) และเน้นคำเฉพาะอาการทางจิตเวช ส่งผลให้ Precision เพิ่มขึ้นจาก 75.74% เป็น <strong>78.31%</strong>
        </li>
        <li>
          <strong>สาเหตุที่ Decision Tree มีประสิทธิภาพต่ำกว่าโมเดลอื่น (Accuracy 66.81%):</strong>
          ข้อมูลข้อความที่ผ่านการแปลงเวกเตอร์มีมิติสูงมาก (> 47,000 มิติ) และเบาบาง (Extremely Sparse) ทำให้ Decision Tree ซึ่งแบ่งข้อมูลตามแกนตั้งฉาก (Axis-aligned Splits) ครั้งละ 1 ฟีเจอร์ เกิดความยากลำบากในการสร้าง Decision Boundary ที่มีประสิทธิภาพ
        </li>
      </ol>
    </div>

    <div class="card">
      <div class="card-header">
        <span>4.2 บทสรุปและข้อเสนอแนะสำหรับการพัฒนาต่อยอด (Conclusion & Future Directions)</span>
      </div>
      <p style="font-size: 12px;">
        โครงงานนี้ประสบความสำเร็จในการออกแบบและเปรียบเทียบระบบจำแนกข้อความภาษาไทยเพื่อคัดกรองภาวะซึมเศร้า โดยพบว่า <strong>BiLSTM + Pre-trained Word2Vec</strong> เป็นโมเดลที่มีประสิทธิภาพสูงสุด และ <strong>Logistic Regression + TF-IDF</strong> เป็นโมเดลทางเลือกที่ประมวลผลได้รวดเร็วและมีความแม่นยำสูง
      </p>

      <div class="insight-box warning" style="margin-top: 6px;">
        <div class="insight-title">แนวทางการพัฒนาต่อยอดในอนาคต (Future Directions):</div>
        <ul style="font-size: 11px; margin-bottom: 0;">
          <li><strong>Pre-trained Transformer Models:</strong> ทดลองประยุกต์ใช้โมเดลภาษาไทยระดับ State-of-the-Art เช่น <em>WangchanBERTa</em> หรือ <em>mBERT</em> เพื่อยกระดับความเข้าใจบริบทประโยคเชิงลึก</li>
          <li><strong>Ensemble Modeling:</strong> ผสานจุดเด่นของ BiLSTM (High Recall) และ Logistic Regression TF-IDF (High Precision) ด้วยวิธี Soft Voting เพื่อเพิ่มประสิทธิภาพรวม</li>
          <li><strong>Multi-Class Severity Classification:</strong> ขยายผลจากการจำแนก 2 คลาส (Binary) ไปสู่การจำแนกระดับความรุนแรงของภาวะซึมเศร้า (Minimal, Mild, Moderate, Severe)</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="report-footer">
    <div><strong>NLP Project 1:</strong> Text Classification for Depression Detection</div>
    <div>กลุ่มที่ 10 (Group 10)</div>
    <div>หน้า 3 / 3 (ฉบับสมบูรณ์)</div>
  </div>

</body>
</html>
"""

with open("Group_10.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Group_10.html updated and saved successfully!")

# Compile to PDF using Edge / Chrome Headless with absolute paths
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

print("Compiling PDF with Edge headless...")
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
