# pages/prediction.py
import streamlit as st
import pandas as pd
import numpy as np
from helpers import load_model_from_file


# ===========================================
# FIELD MAPPING UNTUK USER-FRIENDLY FORM
# ===========================================

# Mapping nama kolom ke label yang lebih mudah dipahami
FIELD_LABELS = {
    # Gender/Sex fields
    "male": "Jenis Kelamin",
    "female": "Jenis Kelamin", 
    "gender": "Jenis Kelamin",
    "sex": "Jenis Kelamin",
    "is_male": "Jenis Kelamin",
    
    # Age fields
    "age": "Usia (Tahun)",
    "umur": "Usia (Tahun)",
    
    # Smoking fields
    "smoking": "Status Merokok",
    "smoking_status": "Status Merokok",
    "currentSmoker": "Perokok Aktif",
    "current_smoker": "Perokok Aktif",
    "is_smoking": "Status Merokok",
    "cigsPerDay": "Jumlah Rokok per Hari",
    "cigs_per_day": "Jumlah Rokok per Hari",
    
    # Blood pressure fields
    "sysBP": "Tekanan Darah Sistolik (mmHg)",
    "sys_bp": "Tekanan Darah Sistolik (mmHg)",
    "systolic": "Tekanan Darah Sistolik (mmHg)",
    "blood_pressure_systolic": "Tekanan Darah Sistolik (mmHg)",
    "diaBP": "Tekanan Darah Diastolik (mmHg)",
    "dia_bp": "Tekanan Darah Diastolik (mmHg)",
    "diastolic": "Tekanan Darah Diastolik (mmHg)",
    "blood_pressure_diastolic": "Tekanan Darah Diastolik (mmHg)",
    
    # Medical history fields
    "diabetes": "Riwayat Diabetes",
    "has_diabetes": "Riwayat Diabetes",
    "hypertension": "Riwayat Hipertensi",
    "has_hypertension": "Riwayat Hipertensi",
    "BPMeds": "Mengonsumsi Obat Tekanan Darah",
    "bp_meds": "Mengonsumsi Obat Tekanan Darah",
    "prevalentStroke": "Riwayat Stroke",
    "prevalent_stroke": "Riwayat Stroke",
    "stroke": "Riwayat Stroke",
    "prevalentHyp": "Riwayat Hipertensi",
    "prevalent_hyp": "Riwayat Hipertensi",
    "previous_heart_disease": "Riwayat Penyakit Jantung",
    "heart_disease": "Riwayat Penyakit Jantung",
    
    # Physical measurements
    "BMI": "Indeks Massa Tubuh (BMI)",
    "bmi": "Indeks Massa Tubuh (BMI)",
    "obesity": "Status Obesitas",
    "is_obese": "Status Obesitas",
    "weight": "Berat Badan (kg)",
    "height": "Tinggi Badan (cm)",
    "waist_circumference": "Lingkar Pinggang (cm)",
    
    # Lab values
    "totChol": "Kolesterol Total (mg/dL)",
    "tot_chol": "Kolesterol Total (mg/dL)",
    "cholesterol": "Kolesterol Total (mg/dL)",
    "cholesterol_level": "Tingkat Kolesterol",
    "cholesterol_hdl": "Kolesterol HDL (mg/dL)",
    "cholesterol_ldl": "Kolesterol LDL (mg/dL)",
    "triglycerides": "Trigliserida (mg/dL)",
    "glucose": "Kadar Glukosa (mg/dL)",
    "fasting_blood_sugar": "Gula Darah Puasa (mg/dL)",
    
    # Heart rate
    "heartRate": "Detak Jantung (bpm)",
    "heart_rate": "Detak Jantung (bpm)",
    
    # Activity
    "physical_activity": "Tingkat Aktivitas Fisik",
    "activity": "Tingkat Aktivitas Fisik",
    "exercise": "Frekuensi Olahraga",
    
    # Education
    "education": "Tingkat Pendidikan",
}

# Mapping untuk field binary (0/1) ke opsi yang lebih ramah
BINARY_OPTIONS = {
    # Gender fields - 1 biasanya = male
    "male": {0: "Perempuan", 1: "Laki-laki"},
    "is_male": {0: "Perempuan", 1: "Laki-laki"},
    "sex": {0: "Perempuan", 1: "Laki-laki"},
    "female": {0: "Laki-laki", 1: "Perempuan"},
    
    # Yes/No fields
    "smoking": {0: "Tidak Merokok", 1: "Merokok"},
    "currentSmoker": {0: "Tidak", 1: "Ya"},
    "current_smoker": {0: "Tidak", 1: "Ya"},
    "is_smoking": {0: "Tidak Merokok", 1: "Merokok"},
    "diabetes": {0: "Tidak", 1: "Ya"},
    "has_diabetes": {0: "Tidak", 1: "Ya"},
    "hypertension": {0: "Tidak", 1: "Ya"},
    "has_hypertension": {0: "Tidak", 1: "Ya"},
    "BPMeds": {0: "Tidak", 1: "Ya"},
    "bp_meds": {0: "Tidak", 1: "Ya"},
    "prevalentStroke": {0: "Tidak", 1: "Ya"},
    "prevalent_stroke": {0: "Tidak", 1: "Ya"},
    "stroke": {0: "Tidak", 1: "Ya"},
    "prevalentHyp": {0: "Tidak", 1: "Ya"},
    "prevalent_hyp": {0: "Tidak", 1: "Ya"},
    "previous_heart_disease": {0: "Tidak", 1: "Ya"},
    "heart_disease": {0: "Tidak", 1: "Ya"},
    "obesity": {0: "Tidak Obesitas", 1: "Obesitas"},
    "is_obese": {0: "Tidak", 1: "Ya"},
}

# Mapping untuk field kategorikal dengan nilai tertentu
CATEGORICAL_OPTIONS = {
    "smoking_status": {
        0: "Tidak Pernah Merokok",
        1: "Mantan Perokok",
        2: "Perokok Aktif"
    },
    "physical_activity": {
        0: "Tidak Aktif",
        1: "Sedikit Aktif",
        2: "Cukup Aktif",
        3: "Sangat Aktif"
    },
    "cholesterol_level": {
        0: "Normal",
        1: "Tinggi"
    },
    "education": {
        1: "SD/Sederajat",
        2: "SMP/Sederajat",
        3: "SMA/Sederajat",
        4: "Diploma/Sarjana"
    }
}


def get_friendly_label(feature_name):
    """Mendapatkan label yang ramah pengguna untuk nama kolom."""
    # Cek di mapping
    if feature_name.lower() in {k.lower(): v for k, v in FIELD_LABELS.items()}:
        for key, label in FIELD_LABELS.items():
            if key.lower() == feature_name.lower():
                return label
    
    # Fallback: format nama kolom agar lebih readable
    # Ubah snake_case atau camelCase ke Title Case
    formatted = feature_name.replace("_", " ").replace("-", " ")
    # Handle camelCase
    import re
    formatted = re.sub('([a-z])([A-Z])', r'\1 \2', formatted)
    return formatted.title()


def get_friendly_options(feature_name, unique_values):
    """Mendapatkan opsi yang ramah pengguna untuk field."""
    feature_lower = feature_name.lower()
    
    # Cek apakah binary field (0 dan 1)
    if set(unique_values) == {0, 1} or set(unique_values) == {0.0, 1.0}:
        # Cek di mapping binary
        for key, options in BINARY_OPTIONS.items():
            if key.lower() == feature_lower:
                return options
        # Default untuk binary yang tidak dikenal
        return {0: "Tidak", 1: "Ya"}
    
    # Cek di mapping kategorikal
    for key, options in CATEGORICAL_OPTIONS.items():
        if key.lower() == feature_lower:
            return options
    
    # Default: return None untuk menggunakan nilai asli
    return None


def show_prediction():
    # Judul halaman
    st.markdown("<h1 style='text-align: center; color: #A67D45;'>Use Model</h1>", unsafe_allow_html=True)

    # -----------------------------------------
    # TABS: INPUT MANUAL vs BATCH PREDICTION
    # -----------------------------------------
    tab1, tab2 = st.tabs(["📝 Input Manual", "📂 Batch Prediction"])
    
    # ===========================================
    # TAB 1: INPUT MANUAL (existing functionality)
    # ===========================================
    with tab1:
        show_manual_prediction()
    
    # ===========================================
    # TAB 2: BATCH PREDICTION (new functionality)
    # ===========================================
    with tab2:
        show_batch_prediction()

    # -----------------------------------------
    # TOMBOL NAVIGASI: PREVIOUS
    # -----------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    col_prev, col_spacer, col_next = st.columns([1, 2, 1])
    
    with col_prev:
        if st.button("← Previous", use_container_width=True, key="prev_btn"):
            st.session_state["page"] = "Data Visualization"
            st.rerun()


def show_manual_prediction():
    """Menampilkan form input manual untuk prediksi 1 data."""
    
    # Pastikan model sudah ditraining atau load dari file
    model = st.session_state.get("rf_model")
    features = st.session_state.get("X_cols", st.session_state.get("features", []))
    
    if model is None:
        st.warning("⚠️ Tidak ada model aktif. Silakan training model di halaman **Analisis Data** atau upload model `.pkl` di tab **Batch Prediction**.")
        if st.button("← Kembali ke Analisis Data", key="back_analysis_manual"):
            st.session_state["page"] = "Analisis Data"
            st.rerun()
        return
    
    if not features:
        st.error("❌ Tidak dapat menemukan daftar fitur yang digunakan saat training model.")
        return

    # -----------------------------------------
    # CARD INPUT DATA
    # -----------------------------------------
    st.markdown("""
    <div style="background: #F0E9E1; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
        <div style="margin-bottom: 10px;">
            <span style="color: #A67D45; font-weight: 600;">Input Data untuk Prediksi</span>
        </div>
        <p style="color: #666; font-size: 0.9rem;">
            Masukkan nilai untuk setiap fitur di bawah ini. Fitur-fitur ini sesuai dengan yang digunakan saat training model.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Ambil data clean untuk referensi nilai min/max
    df_clean = st.session_state.get("clean_df")
    
    # Dictionary untuk menyimpan input values
    input_values = {}
    
    # Buat form input dinamis berdasarkan fitur
    with st.form("form_prediksi"):
        # Bagi fitur ke dalam kolom-kolom
        num_cols = 2
        cols = st.columns(num_cols)
        
        # Dictionary untuk konversi balik dari label ramah ke nilai asli
        reverse_mappings = {}
        
        for idx, feature in enumerate(features):
            col_idx = idx % num_cols
            with cols[col_idx]:
                # Dapatkan label yang ramah pengguna
                friendly_label = get_friendly_label(feature)
                
                # Tentukan tipe input berdasarkan data
                if df_clean is not None and feature in df_clean.columns:
                    col_data = df_clean[feature]
                    unique_vals = sorted(col_data.unique().tolist())
                    unique_count = len(unique_vals)
                    
                    # Jika kolom memiliki sedikit nilai unik (kemungkinan kategorikal)
                    if unique_count <= 5:
                        # Coba dapatkan opsi yang ramah pengguna
                        friendly_options = get_friendly_options(feature, unique_vals)
                        
                        if friendly_options:
                            # Gunakan opsi yang ramah pengguna
                            display_options = [friendly_options.get(v, str(v)) for v in unique_vals]
                            reverse_mappings[feature] = {friendly_options.get(v, str(v)): v for v in unique_vals}
                            
                            selected_display = st.selectbox(
                                f"📌 {friendly_label}",
                                options=display_options,
                                key=f"input_{feature}",
                                help=f"Kolom asli: {feature}"
                            )
                            # Konversi kembali ke nilai asli
                            input_values[feature] = reverse_mappings[feature][selected_display]
                        else:
                            # Tidak ada mapping, gunakan nilai asli
                            input_values[feature] = st.selectbox(
                                f"📌 {friendly_label}",
                                options=unique_vals,
                                key=f"input_{feature}",
                                help=f"Kolom asli: {feature}"
                            )
                    else:
                        # Kolom numerik
                        min_val = float(col_data.min())
                        max_val = float(col_data.max())
                        mean_val = float(col_data.mean())
                        
                        input_values[feature] = st.number_input(
                            f"📌 {friendly_label}",
                            min_value=min_val,
                            max_value=max_val,
                            value=mean_val,
                            key=f"input_{feature}",
                            help=f"Kolom asli: {feature} | Rentang: {min_val:.1f} - {max_val:.1f}"
                        )
                else:
                    # Fallback jika tidak ada data referensi
                    input_values[feature] = st.number_input(
                        f"📌 {friendly_label}",
                        value=0.0,
                        key=f"input_{feature}",
                        help=f"Kolom asli: {feature}"
                    )
        
        st.markdown("---")
        submitted = st.form_submit_button("🔍 Prediksi Sekarang", use_container_width=True)

    # -----------------------------------------
    # HASIL PREDIKSI
    # -----------------------------------------
    if submitted:
        try:
            # Buat DataFrame dari input dengan urutan kolom yang benar
            input_data = pd.DataFrame([input_values], columns=features)
            
            # Lakukan prediksi
            pred = model.predict(input_data)[0]
            
            # Cek apakah model mendukung predict_proba
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(input_data)[0]
                # Ambil probabilitas untuk kelas positif (biasanya kelas 1)
                if len(proba) > 1:
                    risk_proba = proba[1] * 100
                else:
                    risk_proba = proba[0] * 100
            else:
                risk_proba = pred * 100
            
            # Tampilkan hasil
            display_prediction_result(pred, risk_proba)
            
        except Exception as e:
            st.error(f"❌ Error saat melakukan prediksi: {str(e)}")
            st.info("💡 Pastikan semua input telah diisi dengan benar.")


def show_batch_prediction():
    """Menampilkan form untuk batch prediction dari file CSV."""
    
    # -----------------------------------------
    # UPLOAD MODEL (OPSIONAL)
    # -----------------------------------------
    st.markdown("""
    <div style="background: #F0E9E1; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
        <div style="margin-bottom: 10px;">
            <span style="color: #A67D45; font-weight: 600;">📦 Upload Model (Opsional)</span>
        </div>
        <p style="color: #666; font-size: 0.9rem;">
            Upload file model <code>.pkl</code> yang sudah disimpan sebelumnya. Jika sudah training model di sesi ini, Anda bisa langsung upload CSV.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_model = st.file_uploader(
        "Pilih file model (.pkl)",
        type=["pkl"],
        help="Upload file model yang sudah disimpan dari halaman Analisis Data",
        key="upload_model_batch"
    )
    
    # Load model jika diupload
    if uploaded_model is not None:
        loaded_model, loaded_features = load_model_from_file(uploaded_model)
        if loaded_model is not None:
            st.session_state["rf_model"] = loaded_model
            st.session_state["X_cols"] = loaded_features
            st.session_state["features"] = loaded_features
            st.success(f"✅ Model berhasil dimuat! ({len(loaded_features)} fitur)")
    
    # Cek apakah ada model aktif
    model = st.session_state.get("rf_model")
    features = st.session_state.get("X_cols", st.session_state.get("features", []))
    
    if model is None:
        st.warning("⚠️ Tidak ada model aktif. Upload file `.pkl` atau training model di halaman **Analisis Data**.")
        return
    
    # Tampilkan info model aktif
    st.success(f"✅ Model aktif dengan {len(features)} fitur: `{', '.join(features[:5])}{'...' if len(features) > 5 else ''}`")
    
    # -----------------------------------------
    # UPLOAD CSV DATA BARU
    # -----------------------------------------
    st.markdown("""
    <div style="background: #F0E9E1; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
        <div style="margin-bottom: 10px;">
            <span style="color: #A67D45; font-weight: 600;">📂 Upload Data CSV</span>
        </div>
        <p style="color: #666; font-size: 0.9rem;">
            Upload file CSV dengan kolom yang sama seperti saat training model untuk prediksi batch.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_csv = st.file_uploader(
        "Pilih file CSV untuk prediksi",
        type=["csv"],
        help="File CSV harus memiliki kolom yang sesuai dengan fitur model",
        key="upload_csv_batch"
    )
    
    if uploaded_csv is not None:
        try:
            df_new = pd.read_csv(uploaded_csv)
            st.info(f"📊 Data dimuat: {df_new.shape[0]} baris, {df_new.shape[1]} kolom")
            
            # Preview data
            with st.expander("🔍 Preview Data (5 baris pertama)"):
                st.dataframe(df_new.head(), use_container_width=True)
            
            # Cek apakah semua fitur ada di CSV
            missing_features = [f for f in features if f not in df_new.columns]
            if missing_features:
                st.error(f"❌ Kolom berikut tidak ditemukan di CSV: `{', '.join(missing_features)}`")
                st.info("💡 Pastikan file CSV memiliki kolom yang sama seperti data training.")
                return
            
            # Tombol prediksi batch
            if st.button("🚀 Prediksi Batch", use_container_width=True, key="run_batch_pred"):
                with st.spinner("⏳ Sedang melakukan prediksi..."):
                    # Ambil hanya kolom fitur yang diperlukan
                    X_new = df_new[features]
                    
                    # Prediksi
                    predictions = model.predict(X_new)
                    
                    # Probabilitas jika tersedia
                    if hasattr(model, 'predict_proba'):
                        proba = model.predict_proba(X_new)
                        risk_proba = proba[:, 1] * 100 if proba.shape[1] > 1 else proba[:, 0] * 100
                    else:
                        risk_proba = predictions * 100
                    
                    # Tambahkan hasil ke dataframe
                    df_result = df_new.copy()
                    df_result['Prediksi'] = predictions
                    df_result['Label_Prediksi'] = df_result['Prediksi'].map({0: 'Tidak Berisiko', 1: 'Berisiko'})
                    df_result['Probabilitas_Risiko (%)'] = risk_proba.round(2)
                    
                    # Simpan hasil ke session state
                    st.session_state["batch_result"] = df_result
                    st.session_state["batch_stats"] = {
                        "total": len(predictions),
                        "berisiko": int((predictions == 1).sum()),
                        "tidak_berisiko": int((predictions == 0).sum())
                    }
                    
                st.success("✅ Prediksi batch selesai!")
                st.rerun()
        
        except Exception as e:
            st.error(f"❌ Error saat membaca CSV: {str(e)}")
    
    # -----------------------------------------
    # TAMPILKAN HASIL BATCH PREDICTION
    # -----------------------------------------
    if st.session_state.get("batch_result") is not None:
        df_result = st.session_state["batch_result"]
        stats = st.session_state.get("batch_stats", {})
        
        st.markdown("---")
        st.markdown("### 📊 Hasil Prediksi Batch")
        
        # -----------------------------------------
        # STATISTIK PREDIKSI
        # -----------------------------------------
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div style="background: #E8E0D5; border-radius: 12px; padding: 20px; text-align: center;">
                <div style="color: #A67D45; font-weight: 600; font-size: 0.9rem;">Total Data</div>
                <div style="color: #555; font-size: 2rem; font-weight: bold;">""" + f"{stats.get('total', 0):,}" + """</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: #f8d7da; border-radius: 12px; padding: 20px; text-align: center;">
                <div style="color: #721c24; font-weight: 600; font-size: 0.9rem;">🚨 Berisiko</div>
                <div style="color: #721c24; font-size: 2rem; font-weight: bold;">""" + f"{stats.get('berisiko', 0):,}" + """</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: #d4edda; border-radius: 12px; padding: 20px; text-align: center;">
                <div style="color: #155724; font-weight: 600; font-size: 0.9rem;">✅ Tidak Berisiko</div>
                <div style="color: #155724; font-size: 2rem; font-weight: bold;">""" + f"{stats.get('tidak_berisiko', 0):,}" + """</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # -----------------------------------------
        # TABEL HASIL PREDIKSI
        # -----------------------------------------
        st.markdown("#### 📋 Tabel Hasil Prediksi")
        
        # Highlight rows based on prediction
        def highlight_risk(row):
            if row['Prediksi'] == 1:
                return ['background-color: #f8d7da'] * len(row)
            else:
                return ['background-color: #d4edda'] * len(row)
        
        st.dataframe(
            df_result.style.apply(highlight_risk, axis=1),
            use_container_width=True,
            height=400
        )
        
        # -----------------------------------------
        # DOWNLOAD HASIL CSV
        # -----------------------------------------
        st.markdown("#### 📥 Download Hasil")
        
        # Convert to CSV
        csv_buffer = df_result.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📥 Download Hasil Prediksi (CSV)",
            data=csv_buffer,
            file_name="hasil_prediksi_batch.csv",
            mime="text/csv",
            use_container_width=True,
            key="download_batch_result"
        )
        
        # Tombol reset hasil
        if st.button("🔄 Reset Hasil", key="reset_batch"):
            st.session_state["batch_result"] = None
            st.session_state["batch_stats"] = None
            st.rerun()


def display_prediction_result(pred, risk_proba):
    """Menampilkan hasil prediksi dalam format yang menarik."""
    st.markdown("""
    <div style="background: #F0E9E1; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
        <div style="margin-bottom: 10px;">
            <span style="color: #A67D45; font-weight: 600;">Hasil Prediksi</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1, 1], gap="large")
    
    with col_left:
        if pred == 1:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #dc3545 0%, #8B0000 100%); 
                           padding: 2rem; border-radius: 12px; color: white; text-align: center;">
                    <h2 style="color: white; margin-bottom: 1rem;">🚨 BERISIKO TINGGI</h2>
                    <h1 style="color: white; font-size: 3rem; margin: 0;">{risk_proba:.1f}%</h1>
                    <p style="color: white; margin-top: 1rem; font-size: 1.1rem;">
                        Probabilitas Risiko
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                           padding: 2rem; border-radius: 12px; color: white; text-align: center;">
                    <h2 style="color: white; margin-bottom: 1rem;">✅ RISIKO RENDAH</h2>
                    <h1 style="color: white; font-size: 3rem; margin: 0;">{100 - risk_proba:.1f}%</h1>
                    <p style="color: white; margin-top: 1rem; font-size: 1.1rem;">
                        Probabilitas Aman
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    
    with col_right:
        st.markdown("### 💡 Rekomendasi")
        if pred == 1:
            st.error("⚠️ **Perhatian Diperlukan**")
            st.markdown(
                """
                - 🏥 **Konsultasi ke dokter** untuk pengecekan lebih lanjut
                - 🍎 Jaga pola makan sehat
                - 🏃 Tingkatkan aktivitas fisik
                - 🚭 Hindari kebiasaan tidak sehat
                """
            )
        else:
            st.success("✅ **Kondisi Baik**")
            st.markdown(
                """
                - 💪 Pertahankan pola hidup sehat
                - 📅 Lakukan pemeriksaan rutin
                - 🌿 Jaga pola makan seimbang
                - 😌 Kelola stress dengan baik
                """
            )
    
    st.markdown("---")
    st.caption(
        "⚕️ **Disclaimer:** Hasil prediksi ini bersifat informatif dan tidak menggantikan diagnosis medis profesional. "
        "Selalu konsultasikan kondisi kesehatan Anda dengan dokter."
    )