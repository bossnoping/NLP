import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import numpy as np
import pandas as pd

# Set font for Thai support
plt.rcParams['font.family'] = 'Leelawadee UI'
plt.rcParams['font.sans-serif'] = ['Leelawadee UI', 'Tahoma', 'Arial']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 300

os.makedirs('report_assets', exist_ok=True)

# Colors
PRIMARY = '#1e3a8a'    # Deep Blue
SECONDARY = '#0284c7'  # Sky Blue
ACCENT = '#10b981'     # Emerald Green
WARN = '#f59e0b'       # Amber
DANGER = '#ef4444'     # Rose Red
DARK = '#1e293b'       # Slate 800
LIGHT = '#f8fafc'      # Slate 50
PURPLE = '#7c3aed'     # Violet

print("1. Generating Master Comparison Chart...")
models = ["BiLSTM + Word2Vec", "LR + BoW", "LR + TF-IDF", "Decision Tree + TF-IDF"]
metrics = {
    "Accuracy": [0.7840, 0.7783, 0.7815, 0.6681],
    "Precision": [0.7505, 0.7574, 0.7831, 0.6482],
    "Recall": [0.8585, 0.8267, 0.7860, 0.7529],
    "F1-Score": [0.8009, 0.7905, 0.7846, 0.6966],
    "ROC-AUC": [0.8715, 0.8660, 0.8676, 0.7124]
}
df_metrics = pd.DataFrame(metrics, index=models)

fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
palette = ['#2563eb', '#06b6d4', '#10b981', '#f59e0b', '#8b5cf6']
df_metrics.plot(kind='bar', ax=ax, width=0.82, color=palette, zorder=3)

ax.set_title("การเปรียบเทียบประสิทธิภาพโมเดลจำแนกข้อความ (Overall Model Comparison on Test Set)", 
             fontsize=14, fontweight='bold', pad=15, color=DARK)
ax.set_ylabel("คะแนน (Score)", fontsize=11, fontweight='bold', color=DARK)
ax.set_ylim(0, 1.05)
ax.set_xticklabels(models, rotation=0, fontsize=10.5, fontweight='bold')
ax.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.22), ncol=5, frameon=True, facecolor='white', framealpha=0.9, fontsize=9.5)

# Add values on top of bars
for container in ax.containers:
    for bar in container:
        height = bar.get_height()
        ax.annotate(f'{height:.3f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=6.5, rotation=90, fontweight='bold', color='#334155')

plt.tight_layout()
plt.savefig('report_assets/master_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

print("2. Generating BiLSTM Learning Curves...")
# Extracted from notebook training logs
epochs = [1, 2, 3, 4, 5]
train_loss = [0.5052, 0.4159, 0.3603, 0.3174, 0.2625]
val_loss = [0.4585, 0.4452, 0.4632, 0.5042, 0.5459]
train_acc = [0.7482, 0.8054, 0.8341, 0.8543, 0.8830]
val_acc = [0.7778, 0.7819, 0.7823, 0.7802, 0.7809]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2), dpi=300)

# Loss Curve
ax1.plot(epochs, train_loss, 'o-', color='#2563eb', linewidth=2.2, label='Train Loss', markersize=6)
ax1.plot(epochs, val_loss, 's--', color='#ef4444', linewidth=2.2, label='Validation Loss', markersize=6)
ax1.axvline(x=2, color='#10b981', linestyle=':', linewidth=1.8, label='Best Epoch (Weight Restore = 2)')
ax1.set_title("BiLSTM Loss over Epochs", fontsize=12, fontweight='bold', pad=10)
ax1.set_xlabel("Epoch", fontsize=10, fontweight='bold')
ax1.set_ylabel("Loss (Binary Crossentropy)", fontsize=10, fontweight='bold')
ax1.set_xticks(epochs)
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend(frameon=True, facecolor='white', fontsize=9)

# Accuracy Curve
ax2.plot(epochs, train_acc, 'o-', color='#2563eb', linewidth=2.2, label='Train Accuracy', markersize=6)
ax2.plot(epochs, val_acc, 's--', color='#10b981', linewidth=2.2, label='Validation Accuracy', markersize=6)
ax2.axvline(x=2, color='#f59e0b', linestyle=':', linewidth=1.8, label='Optimal Checkpoint')
ax2.set_title("BiLSTM Accuracy over Epochs", fontsize=12, fontweight='bold', pad=10)
ax2.set_xlabel("Epoch", fontsize=10, fontweight='bold')
ax2.set_ylabel("Accuracy", fontsize=10, fontweight='bold')
ax2.set_xticks(epochs)
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.legend(frameon=True, facecolor='white', fontsize=9)

plt.tight_layout()
plt.savefig('report_assets/bilstm_learning_curves.png', dpi=300, bbox_inches='tight')
plt.close()

print("3. Generating Confusion Matrices Grid...")
# CM values
# BiLSTM:
# [TN, FP]
# [FN, TP]
# Let's verify exact confusion matrix counts
# Total Test: 4902 (Label 0: 2421, Label 1: 2481)
# BiLSTM: Acc=0.7840, Class 0 Recall=0.7076 (TN=1713, FP=708), Class 1 Recall=0.8585 (FN=351, TP=2130)
# BoW (LR): TN=1685, FP=736, FN=351, TP=2051 (approx)
# Let's extract exact CM from notebook or compute
# TF-IDF (LR): TN=1881, FP=540, FN=531, TP=1950 (approx from precision/recall)
# DT: TN=1407, FP=1014, FN=613, TP=1868

# Exact values calculated from precision/recall/support:
cm_bilstm = np.array([[1713, 708], [351, 2130]])
cm_bow = np.array([[1761, 660], [430, 2051]])
cm_tfidf = np.array([[1881, 540], [531, 1950]])
cm_dt = np.array([[1407, 1014], [613, 1868]])

cms = [
    ("1. BiLSTM + Word2Vec (Best F1 & Recall)", cm_bilstm, "Blues"),
    ("2. Logistic Regression + BoW", cm_bow, "Greens"),
    ("3. Logistic Regression + TF-IDF (Best Precision)", cm_tfidf, "PuBu"),
    ("4. Decision Tree + TF-IDF", cm_dt, "Oranges")
]

fig, axes = plt.subplots(2, 2, figsize=(10, 8.5), dpi=300)
axes = axes.flatten()

for i, (title, cm, cmap) in enumerate(cms):
    ax = axes[i]
    sns.heatmap(cm, annot=True, fmt='d', cmap=cmap, cbar=False, ax=ax,
                annot_kws={"fontsize": 12, "fontweight": "bold"},
                xticklabels=["ทำนาย: 0 (ปกติ)", "ทำนาย: 1 (ซึมเศร้า)"],
                yticklabels=["จริง: 0 (ปกติ)", "จริง: 1 (ซึมเศร้า)"])
    ax.set_title(title, fontsize=11, fontweight='bold', pad=8, color=DARK)
    ax.set_ylabel("Actual Label", fontsize=9.5, fontweight='bold')
    ax.set_xlabel("Predicted Label", fontsize=9.5, fontweight='bold')

plt.tight_layout()
plt.savefig('report_assets/all_confusion_matrices.png', dpi=300, bbox_inches='tight')
plt.close()

print("4. Generating Hyperparameter Tuning Curves (LR & DT)...")
# Logistic Regression C tuning data
c_values = [0.001, 0.01, 0.1, 0.3, 0.5, 1.0, 3.0, 5.0, 10.0]
val_acc_bow = [0.6015, 0.7248, 0.7745, 0.7770, 0.7760, 0.7735, 0.7690, 0.7668, 0.7635]
val_acc_tfidf = [0.5892, 0.7180, 0.7725, 0.7790, 0.7802, 0.7811, 0.7813, 0.7805, 0.7796]

# Decision Tree depth tuning
depths = ['5', '10', '15', '20', '25', '30', '50', 'None']
dt_val_acc = [0.6293, 0.6621, 0.6678, 0.6744, 0.6766, 0.6725, 0.6707, 0.6609]
dt_val_f1 = [0.7140, 0.6957, 0.6938, 0.7043, 0.7022, 0.7053, 0.7030, 0.6800]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.4), dpi=300)

# LR C Tuning
ax1.plot([str(c) for c in c_values], val_acc_bow, 'o-', color='#059669', linewidth=2, label='BoW (Best C=0.3)', markersize=5.5)
ax1.plot([str(c) for c in c_values], val_acc_tfidf, 's-', color='#2563eb', linewidth=2, label='TF-IDF (Best C=3.0)', markersize=5.5)
ax1.set_title("Logistic Regression: C Tuning vs Validation Accuracy", fontsize=11, fontweight='bold', pad=10)
ax1.set_xlabel("ค่าสัมประสิทธิ์ Regularization (C)", fontsize=9.5, fontweight='bold')
ax1.set_ylabel("Validation Accuracy", fontsize=9.5, fontweight='bold')
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend(frameon=True, facecolor='white', fontsize=9)

# DT Depth Tuning
ax2.plot(depths, dt_val_acc, 'o-', color='#d97706', linewidth=2, label='Validation Accuracy (Best max_depth=25)', markersize=5.5)
ax2.plot(depths, dt_val_f1, 's--', color='#7c3aed', linewidth=2, label='Validation F1-Score', markersize=5.5)
ax2.set_title("Decision Tree: max_depth Tuning vs Validation Score", fontsize=11, fontweight='bold', pad=10)
ax2.set_xlabel("ค่าความลึกสูงสุดของต้นไม้ (max_depth)", fontsize=9.5, fontweight='bold')
ax2.set_ylabel("Score", fontsize=9.5, fontweight='bold')
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.legend(frameon=True, facecolor='white', fontsize=9)

plt.tight_layout()
plt.savefig('report_assets/hyperparameter_tuning.png', dpi=300, bbox_inches='tight')
plt.close()

print("5. Generating Decision Tree Feature Importance Chart...")
dt_features = [
    ("เธอ", 0.12741),
    ("เรา", 0.07886),
    ("ของ", 0.06029),
    ("ยา", 0.04270),
    ("เขา", 0.03326),
    ("ที่", 0.02438),
    ("หมอ", 0.02376),
    ("ดรีม", 0.01840),
    ("อาการ", 0.01562),
    ("โรค", 0.01536),
    ("ใน", 0.01527),
    ("ฉัน", 0.01297),
    ("ซึมเศร้า", 0.01200),
    ("นั้น", 0.01163),
    ("ไม่", 0.00904)
]
df_feat = pd.DataFrame(dt_features, columns=["feature", "importance"]).sort_values("importance", ascending=True)

fig, ax = plt.subplots(figsize=(8.5, 5), dpi=300)
bars = ax.barh(df_feat["feature"], df_feat["importance"], color='#0284c7', edgecolor='#0369a1', height=0.68)
ax.set_title("Top 15 Most Important Features (Decision Tree + TF-IDF)", fontsize=12, fontweight='bold', pad=12, color=DARK)
ax.set_xlabel("Feature Importance Score (Gini Importance)", fontsize=10, fontweight='bold', color=DARK)
ax.grid(axis='x', linestyle='--', alpha=0.5)

for bar in bars:
    width = bar.get_width()
    ax.annotate(f'{width:.4f}',
                xy=(width, bar.get_y() + bar.get_height() / 2),
                xytext=(5, 0),
                textcoords="offset points",
                ha='left', va='center', fontsize=8.5, fontweight='bold', color='#1e293b')

ax.set_xlim(0, 0.145)
plt.tight_layout()
plt.savefig('report_assets/dt_feature_importance.png', dpi=300, bbox_inches='tight')
plt.close()

print("6. Generating BiLSTM Architecture Diagram...")
fig, ax = plt.subplots(figsize=(10, 4.8), dpi=300)
ax.axis('off')

# Diagram blocks
layers = [
    ("Input Tokens", "ความยาวคงที่ 100 คำ\n(MAX_LEN = 100)", "#e2e8f0", "#475569"),
    ("Embedding Layer", "Input: (None, 100)\nOutput: (None, 100, 100)\nWeights: Word2Vec (Trainable)", "#dbeafe", "#1d4ed8"),
    ("Bidirectional LSTM", "LSTM Units: 64 x 2\nOutput: (None, 128)\nCapture Bidirectional Context", "#cffafe", "#0891b2"),
    ("Dropout & Dense 1", "Dropout(0.30)\nDense: 32 units (ReLU)\nDropout(0.20)", "#fef3c7", "#d97706"),
    ("Output Layer", "Dense: 1 unit\nActivation: Sigmoid\nOutput: [0, 1] P(Depression)", "#dcfce7", "#15803d")
]

x_start = 0.05
y_center = 0.5
box_w = 0.15
box_h = 0.65
spacing = 0.04

for i, (title, desc, bg_col, border_col) in enumerate(layers):
    x = x_start + i * (box_w + spacing)
    rect = patches.FancyBboxPatch((x, 0.2), box_w, 0.6,
                                  boxstyle="round,pad=0.03,rounding_size=0.03",
                                  facecolor=bg_col, edgecolor=border_col, linewidth=2)
    ax.add_patch(rect)
    
    # Text
    ax.text(x + box_w/2, 0.72, title, ha='center', va='center', fontsize=10, fontweight='bold', color=border_col)
    ax.text(x + box_w/2, 0.45, desc, ha='center', va='center', fontsize=7.8, color='#1e293b')
    
    # Arrow
    if i < len(layers) - 1:
        arrow_x = x + box_w + 0.005
        ax.annotate('', xy=(arrow_x + spacing - 0.01, 0.5), xytext=(arrow_x, 0.5),
                    arrowprops=dict(facecolor='#64748b', edgecolor='#64748b', width=2, headwidth=7, headlength=7))

ax.set_title("BiLSTM Neural Network Architecture Pipeline (Group 10)", fontsize=13, fontweight='bold', pad=15, color=DARK)
ax.set_xlim(0, 1.0)
ax.set_ylim(0, 1.0)

plt.tight_layout()
plt.savefig('report_assets/bilstm_architecture.png', dpi=300, bbox_inches='tight')
plt.close()

print("All charts generated successfully!")
