# pages/prediction.py
import streamlit as st
import pandas as pd

from helpers import require_model  


def show_prediction():
    # Judul utama halaman prediksi individu
    st.title("🩺 Prediksi Risiko Hipertensi") # Diubah

    require_model()

    # Card penjelasan singkat tentang fungsi halaman ini
    st.markdown(
        """
        <div class="data-card">
            <p style="font-size: 1rem; color: #555;">
                Masukkan data kesehatan individu di bawah ini untuk memprediksi risiko Hipertensi 
                berdasarkan model Random Forest yang sudah dilatih.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------
    # FORM INPUT DATA PASIEN
    # -----------------------------------------
    with st.form("form_prediksi"):
        st.markdown("### 📋 Data Kesehatan Pasien")

        col1, col2 = st.columns(2)

        # -----------------------------
        # KOLOM KIRI: Usia & Tekanan Darah + Profil Lipid
        # -----------------------------
        with col1:
            st.markdown("#### 👤 Data Demografis & Tekanan Darah")
            age = st.number_input(
                "Usia (tahun)",
                min_value=18,
                max_value=100,
                value=40,
                help="Masukkan usia dalam tahun",
            )
            # Tekanan darah sistolik
            systolic = st.number_input(
                "Tekanan Darah Sistolik (mmHg)",
                min_value=80,
                max_value=250,
                value=120,
                help="Tekanan darah saat jantung memompa (batas normal < 120)",
            )
            # Tekanan darah diastolik
            diastolic = st.number_input(
                "Tekanan Darah Diastolik (mmHg)",
                min_value=50,
                max_value=150,
                value=80,
                help="Tekanan darah saat jantung rileks (batas normal < 80)",
            )

            st.markdown("#### 💉 Data Kolesterol & Gula Darah")
            cholesterol_level = st.number_input(
                "Kolesterol Total (mg/dL)", min_value=80, max_value=400, value=200
            )
            hdl = st.number_input(
                "Kolesterol HDL (mg/dL)",
                min_value=10,
                max_value=120,
                value=40,
                help="Kolesterol baik",
            )
            ldl = st.number_input(
                "Kolesterol LDL (mg/dL)",
                min_value=10,
                max_value=300,
                value=120,
                help="Kolesterol jahat",
            )
            triglycerides = st.number_input(
                "Trigliserida (mg/dL)", min_value=30, max_value=600, value=150
            )
            fasting_blood_sugar = st.number_input(
                "Gula Darah Puasa (mg/dL)", min_value=50, max_value=400, value=100
            )

        # -----------------------------
        # KOLOM KANAN: Kondisi Kesehatan & Gaya Hidup
        # -----------------------------
        with col2:
            st.markdown("#### 🏥 Kondisi Kesehatan")
            # Status hipertensi (jika ini sudah hipertensi, maka model memprediksi risiko komplikasi/keparahan)
            hypertension = st.selectbox(
                "Riwayat Hipertensi Sebelumnya", # Diubah
                ["Tidak (0)", "Ya (1)"],
                help="Apakah memiliki riwayat diagnosis Hipertensi?",
            )
            # Status diabetes (0 / 1)
            diabetes = st.selectbox(
                "Diabetes", ["Tidak (0)", "Ya (1)"], help="Apakah memiliki riwayat diabetes?"
            )
            # Status obesitas (0 / 1)
            obesity = st.selectbox(
                "Obesitas", ["Tidak (0)", "Ya (1)"], help="Apakah termasuk kategori obesitas?"
            )
            # Riwayat penyakit jantung sebelumnya (0 / 1) - dibiarkan karena terkait kardiovaskular
            prev_hd = st.selectbox(
                "Riwayat Penyakit Jantung",
                ["Tidak (0)", "Ya (1)"],
                help="Apakah pernah mengalami penyakit jantung sebelumnya?",
            )
            # Lingkar pinggang sebagai indikator risiko
            waist = st.number_input(
                "Lingkar Pinggang (cm)",
                min_value=50,
                max_value=200,
                value=85,
                help="Ukuran lingkar pinggang dalam cm",
            )

            st.markdown("#### 🚭 Gaya Hidup")
            # Status merokok (dikodekan 0/1/2)
            smoking = st.selectbox(
                "Status Merokok",
                ["Tidak Pernah (0)", "Mantan Perokok (1)", "Aktif Merokok (2)"],
            )
            # Tingkat aktivitas fisik (dikodekan 0/1/2)
            physical_activity = st.selectbox(
                "Aktivitas Fisik",
                ["Rendah (0)", "Sedang (1)", "Tinggi (2)"],
                help="Tingkat aktivitas fisik sehari-hari",
            )

        st.markdown("---")
        submitted = st.form_submit_button("🔍 Prediksi Sekarang", use_container_width=True)

    # -----------------------------------------
    # LOGIKA PREDIKSI
    # -----------------------------------------
    if submitted:
        hypertension_val = 1 if "Ya" in hypertension else 0
        diabetes_val = 1 if "Ya" in diabetes else 0
        obesity_val = 1 if "Ya" in obesity else 0
        prev_hd_val = 1 if "Ya" in prev_hd else 0

        smoking_map = {
            "Tidak Pernah (0)": 0, "Mantan Perokok (1)": 1, "Aktif Merokok (2)": 2,
        }
        physical_map = {
            "Rendah (0)": 0, "Sedang (1)": 1, "Tinggi (2)": 2,
        }

        smoking_val = smoking_map[smoking]
        physical_val = physical_map[physical_activity]

        # Menyusun data input ke dalam DataFrame 1 baris
        input_data = pd.DataFrame(
            [
                {
                    "age": age,
                    "hypertension": hypertension_val,
                    "blood_pressure_systolic": systolic,
                    "blood_pressure_diastolic": diastolic,
                    "diabetes": diabetes_val,
                    "cholesterol_level": cholesterol_level,
                    "cholesterol_hdl": hdl,
                    "cholesterol_ldl": ldl,
                    "triglycerides": triglycerides,
                    "fasting_blood_sugar": fasting_blood_sugar,
                    "obesity": obesity_val,
                    "waist_circumference": waist,
                    "previous_heart_disease": prev_hd_val,
                    "smoking_status": smoking_val,
                    "physical_activity": physical_val,
                }
            ]
        )

        model = st.session_state["rf_model"]
        proba = model.predict_proba(input_data)[0, 1]
        pred = model.predict(input_data)[0]

        # -----------------------------------------
        # TAMPILKAN HASIL PREDIKSI
        # -----------------------------------------
        st.markdown("---")
        st.markdown("## 📊 Hasil Prediksi")

        col_left, col_right = st.columns([1, 1], gap="large")

        # -----------------------------
        # KARTU HASIL PROBABILITAS
        # -----------------------------
        with col_left:
            if pred == 1:
                # Jika model memprediksi BERISIKO (1)
                st.markdown(
                    f"""
                    <div style="background: linear-gradient(135deg, #dc3545 0%, #8B0000 100%); 
                               padding: 2rem; border-radius: 12px; color: white; text-align: center;">
                        <h2 style="color: white; margin-bottom: 1rem;">🚨 BERISIKO TINGGI</h2>
                        <h1 style="color: white; font-size: 3rem; margin: 0;">{proba*100:.1f}%</h1>
                        <p style="color: white; margin-top: 1rem; font-size: 1.1rem;">
                            Probabilitas Risiko Hipertensi # Diubah
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                # Jika model memprediksi TIDAK BERISIKO (0)
                st.markdown(
                    f"""
                    <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                               padding: 2rem; border-radius: 12px; color: white; text-align: center;">
                        <h2 style="color: white; margin-bottom: 1rem;">✅ RISIKO RENDAH</h2>
                        <h1 style="color: white; font-size: 3rem; margin: 0;">{proba*100:.1f}%</h1>
                        <p style="color: white; margin-top: 1rem; font-size: 1.1rem;">
                            Probabilitas Risiko Hipertensi # Diubah
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # -----------------------------
        # REKOMENDASI UMUM (NON-MEDIS)
        # -----------------------------
        with col_right:
            st.markdown("### 💡 Rekomendasi Umum")
            if proba >= 0.6:
                # Jika probabilitas tinggi → rekomendasi lebih serius
                st.error("⚠️ **Perhatian Serius Diperlukan**")
                st.markdown( # Diubah untuk Hipertensi
                    """
                    - 🏥 **Segera konsultasi** ke dokter untuk pengecekan tekanan darah
                    - 🧂 Batasi konsumsi garam dan makanan olahan
                    - 💊 Ikuti saran dokter, mungkin butuh terapi obat penurun tekanan darah
                    - 🏃 Tingkatkan aktivitas fisik secara bertahap dan teratur
                    - 📉 Turunkan berat badan jika Obesitas
                    """
                )
            elif proba >= 0.3:
                # Risiko menengah → mulai perbaiki gaya hidup
                st.warning("⚠️ **Perlu Perhatian**")
                st.markdown( # Diubah untuk Hipertensi
                    """
                    - 👨‍⚕️ Konsultasi dengan dokter untuk kontrol tekanan darah berkala
                    - 🍎 Terapkan diet DASH (Dietary Approaches to Stop Hypertension)
                    - 🚶 Olahraga ringan secara teratur (minimal 30 menit/hari)
                    - 🚭 Hindari merokok dan alkohol
                    - 😌 Kelola stres dengan teknik relaksasi
                    """
                )
            else:
                # Risiko rendah → tetap jaga pola hidup sehat
                st.success("✅ **Kondisi Baik**")
                st.markdown( # Diubah untuk Hipertensi
                    """
                    - 💪 Pertahankan pola hidup sehat yang sudah ada
                    - 🌿 Jaga pola makan seimbang (rendah lemak & garam)
                    - 📅 Cek tekanan darah secara rutin (minimal 6 bulan sekali)
                    - 😊 Kelola stress dengan baik dan istirahat cukup
                    """
                )

        st.markdown("---")
        st.caption(
            "⚕️ **Disclaimer:** Hasil prediksi ini bersifat informatif dan tidak menggantikan diagnosis medis profesional. "
            "Selalu konsultasikan kondisi kesehatan Anda dengan dokter."
        )