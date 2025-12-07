# helpers.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from matplotlib.backends.backend_pdf import PdfPages
import joblib

from sklearn.metrics import confusion_matrix 
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# --- KONSTANTA TARGET ---
# Nama kolom target (label) di dataset untuk risiko hipertensi
TARGET_COL = "hypertension"  # Diubah dari "heart_attack"


# --- HELPER: SAVE MODEL TO FILE ---
def save_model_to_file(model, features):
    """
    Menyimpan model dan daftar fitur ke dalam buffer BytesIO untuk download.
    Returns: BytesIO buffer containing the pickled model data.
    """
    model_data = {
        'model': model,
        'features': features
    }
    buf = BytesIO()
    joblib.dump(model_data, buf)
    buf.seek(0)
    return buf


# --- HELPER: LOAD MODEL FROM FILE ---
def load_model_from_file(uploaded_file):
    """
    Memuat model dan daftar fitur dari file .pkl yang diupload.
    Returns: tuple (model, features) atau (None, None) jika gagal.
    """
    try:
        model_data = joblib.load(uploaded_file)
        model = model_data.get('model')
        features = model_data.get('features', [])
        return model, features
    except Exception as e:
        st.error(f"❌ Gagal memuat model: {str(e)}")
        return None, None


# --- HELPER: APPLY STANDARDIZATION ---
def apply_standardization(df, columns):
    """
    Menerapkan StandardScaler pada kolom-kolom numerik yang dipilih.
    Returns: DataFrame yang sudah di-transform dan scaler object.
    """
    df = df.copy()
    scaler = StandardScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df, scaler


# --- HELPER: APPLY NORMALIZATION ---
def apply_normalization(df, columns):
    """
    Menerapkan MinMaxScaler (0-1) pada kolom-kolom numerik yang dipilih.
    Returns: DataFrame yang sudah di-transform dan scaler object.
    """
    df = df.copy()
    scaler = MinMaxScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df, scaler


# --- HELPER: CEK DATA RAW ---
def require_raw_data():
    """ ... (Tidak ada perubahan) ... """
    if st.session_state.get("raw_df") is None:
        st.warning("⚠️ Silakan upload dataset terlebih dahulu di menu **Input Dataset**.")
        st.info("📌 Gunakan menu sidebar di kiri untuk mengakses fitur aplikasi secara berurutan.")
        st.stop()


# --- HELPER: CEK DATA BERSIH ---
def require_clean_data():
    """ ... (Tidak ada perubahan) ... """
    if st.session_state.get("clean_df") is None:
        st.warning("⚠️ Silakan lakukan preprocessing data terlebih dahulu di menu **Preprocessing Data**.")
        st.info("📌 Gunakan menu sidebar di kiri untuk mengakses fitur aplikasi secara berurutan.")
        st.stop()


# --- HELPER: CEK MODEL ---
def require_model():
    """ ... (Tidak ada perubahan) ... """
    if st.session_state.get("rf_model") is None:
        st.warning("⚠️ Model belum dilatih. Silakan lakukan training di menu **Analisis Data**.")
        st.info("📌 Gunakan menu sidebar di kiri untuk mengakses fitur aplikasi secara berurutan.")
        st.stop()


# --- HELPER: PREPROCESSING DATA ---
def preprocess_data(df: pd.DataFrame, target_col: str = None):
    """
    Preprocessing data secara fleksibel - otomatis menggunakan semua kolom numerik
    dari dataset yang diupload.
    """
    df = df.copy()  # buat salinan agar tidak mengubah dataframe asli

    # simpan informasi awal sebelum dibersihkan
    rows_before = df.shape[0]          # jumlah baris sebelum preprocessing
    dup_count = df.duplicated().sum()  # jumlah baris duplikat
    missing_before = df.isna().sum()   # jumlah missing per kolom

    # hapus baris duplikat
    df = df.drop_duplicates()
    # hapus baris yang mengandung missing values
    df = df.dropna()

    # konversi kolom bertipe object -> kode kategori (numerik)
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype("category").cat.codes

    # Update features di session state dengan kolom dari dataset
    if target_col and target_col in df.columns:
        st.session_state["target_col"] = target_col
        st.session_state["features"] = [c for c in df.columns if c != target_col]
    else:
        # Jika target_col tidak dispesifikasi, gunakan semua kolom sebagai features
        st.session_state["features"] = list(df.columns)

    # ringkasan info preprocessing untuk ditampilkan di UI
    info = {
        "rows_before": int(rows_before),                 # baris sebelum preprocessing
        "rows_after": int(df.shape[0]),                  # baris setelah preprocessing
        "cols": int(df.shape[1]),                        # jumlah kolom aktif
        "duplicates_removed": int(dup_count),            # jumlah duplikat yang dihapus
        "missing_values_before": missing_before.to_dict(),  # missing value per kolom (sebelum)
        "missing_total_after": int(df.isna().sum().sum()),  # total missing setelah preprocessing (harusnya 0)
    }

    return df, info


# --- HELPER: CONFUSION MATRIX PLOT ---
def plot_confusion_matrix(cm, labels):
    """
    Membuat visualisasi confusion matrix dalam bentuk heatmap,
    lalu menampilkannya di Streamlit.
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        cm,
        annot=True,       
        fmt="d",          
        cmap="Reds",      
        cbar=True,        
        ax=ax,
        square=True,
        linewidths=1,
        linecolor="white",
    )
    ax.set_xlabel("Predicted", fontsize=12, fontweight="bold")  
    ax.set_ylabel("Actual", fontsize=12, fontweight="bold")     
    ax.set_xticklabels(labels, fontsize=10)                     
    ax.set_yticklabels(labels, fontsize=10)                     
    ax.set_title("Confusion Matrix Prediksi Hipertensi", fontsize=14, fontweight="bold", pad=20) # Diubah judul
    plt.tight_layout()
    st.pyplot(fig)  
    return fig      


# --- HELPER: FEATURE IMPORTANCE ---
def plot_feature_importance(model, feature_names):
    """
    Menampilkan 10 fitur teratas berdasarkan nilai feature_importances_ dari model Random Forest.
    """
    importances = model.feature_importances_
    idx = np.argsort(importances)[-10:]  
    sorted_features = np.array(feature_names)[idx]      
    sorted_importances = importances[idx]              

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.cm.Reds(np.linspace(0.4, 0.8, len(sorted_features)))
    ax.barh(sorted_features, sorted_importances, color=colors)  
    ax.set_title(
        "Top 10 Feature Importance - Random Forest (Hipertensi)", # Diubah judul
        fontsize=14,
        fontweight="bold",
        pad=20,
    )
    ax.set_xlabel("Importance Score", fontsize=12, fontweight="bold")
    ax.set_ylabel("Features", fontsize=12, fontweight="bold")
    plt.tight_layout()
    st.pyplot(fig)  
    return fig      


# --- HELPER: GENERATE PDF VISUALISASI ---
def generate_pdf_visualizations(df: pd.DataFrame, model):
    """
    Membuat file PDF yang berisi beberapa visualisasi.
    """
    buf = BytesIO()  

    with PdfPages(buf) as pdf:
        # Plot 1: Age Distribution
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.histplot(df["age"], kde=True, ax=ax1, bins=20, color="#A67D45") # Ganti warna
        ax1.set_title("Distribusi Usia", fontsize=14, fontweight="bold")
        ax1.set_xlabel("Usia (tahun)", fontsize=12)
        ax1.set_ylabel("Frekuensi", fontsize=12)
        plt.tight_layout()
        pdf.savefig(fig1)  
        plt.close(fig1)    

        # Plot 2: Hypertension Distribution
        fig2, ax2 = plt.subplots(figsize=(8, 6))
        hypertension_counts = df[TARGET_COL].value_counts() # Menggunakan TARGET_COL baru
        colors = ["#899581", "#A67D45"]  # Warna baru
        ax2.bar(hypertension_counts.index, hypertension_counts.values, color=colors)
        ax2.set_title("Distribusi Label Hipertensi", fontsize=14, fontweight="bold") # Diubah judul
        ax2.set_xlabel("Label", fontsize=12)
        ax2.set_ylabel("Jumlah", fontsize=12)
        ax2.set_xticks([0, 1])
        ax2.set_xticklabels(["Tidak (0)", "Ya (1)"]) # Diubah label
        plt.tight_layout()
        pdf.savefig(fig2)
        plt.close(fig2)

        # Plot 3: Correlation Heatmap
        fig3, ax3 = plt.subplots(figsize=(12, 10))
        corr = df.corr()  
        sns.heatmap(
            corr,
            cmap="Reds",
            ax=ax3,
            annot=False,
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": 0.8},
        )
        ax3.set_title("Heatmap Korelasi Fitur", fontsize=14, fontweight="bold")
        plt.tight_layout()
        pdf.savefig(fig3)
        plt.close(fig3)

        # Plot 4: Feature Importance 
        if model is not None and hasattr(model, "feature_importances_"):
            fig4, ax4 = plt.subplots(figsize=(10, 8))
            importances = model.feature_importances_
            idx = np.argsort(importances)  
            sorted_features = np.array(st.session_state["features"])[idx]
            sorted_importances = importances[idx]
            colors = plt.cm.Reds(np.linspace(0.4, 0.8, len(sorted_features)))
            ax4.barh(sorted_features, sorted_importances, color=colors)
            ax4.set_title("Feature Importance - Random Forest (Hipertensi)", fontsize=14, fontweight="bold") # Diubah judul
            ax4.set_xlabel("Importance Score", fontsize=12)
            plt.tight_layout()
            pdf.savefig(fig4)
            plt.close(fig4)

    buf.seek(0)
    return buf