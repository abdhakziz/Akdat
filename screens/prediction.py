# pages/prediction.py
import streamlit as st
import pandas as pd
import numpy as np


def show_prediction():
    # Judul halaman
    st.markdown("<h1 style='text-align: center; color: #A67D45;'>Use Model</h1>", unsafe_allow_html=True)

    # Pastikan model sudah ditraining
    if st.session_state.get("rf_model") is None:
        st.warning("⚠️ Model belum dilatih. Silakan lakukan training di halaman **Analisis Data** terlebih dahulu.")
        if st.button("← Kembali ke Analisis Data"):
            st.session_state["page"] = "Analisis Data"
            st.rerun()
        return
    
    # Ambil model dan fitur yang digunakan saat training
    model = st.session_state["rf_model"]
    features = st.session_state.get("X_cols", st.session_state.get("features", []))
    
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
        
        for idx, feature in enumerate(features):
            col_idx = idx % num_cols
            with cols[col_idx]:
                # Tentukan tipe input berdasarkan data
                if df_clean is not None and feature in df_clean.columns:
                    col_data = df_clean[feature]
                    unique_vals = col_data.nunique()
                    
                    # Jika kolom memiliki sedikit nilai unik (kemungkinan kategorikal)
                    if unique_vals <= 5:
                        options = sorted(col_data.unique().tolist())
                        input_values[feature] = st.selectbox(
                            f"📌 {feature}",
                            options=options,
                            key=f"input_{feature}"
                        )
                    else:
                        # Kolom numerik
                        min_val = float(col_data.min())
                        max_val = float(col_data.max())
                        mean_val = float(col_data.mean())
                        
                        input_values[feature] = st.number_input(
                            f"📌 {feature}",
                            min_value=min_val,
                            max_value=max_val,
                            value=mean_val,
                            key=f"input_{feature}"
                        )
                else:
                    # Fallback jika tidak ada data referensi
                    input_values[feature] = st.number_input(
                        f"📌 {feature}",
                        value=0.0,
                        key=f"input_{feature}"
                    )
        
        st.markdown("---")
        submitted = st.form_submit_button("🔍 Prediksi Sekarang", use_container_width=True)

    # -----------------------------------------
    # HASIL PREDIKSI
    # -----------------------------------------
    st.markdown("""
    <div style="background: #F0E9E1; border-radius: 12px; padding: 20px; margin-bottom: 20px; min-height: 150px;">
        <div style="margin-bottom: 10px;">
            <span style="color: #A67D45; font-weight: 600;">Hasil Prediksi</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
                        - � Hindari kebiasaan tidak sehat
                        """
                    )
                else:
                    st.success("✅ **Kondisi Baik**")
                    st.markdown(
                        """
                        - � Pertahankan pola hidup sehat
                        - 📅 Lakukan pemeriksaan rutin
                        - 🌿 Jaga pola makan seimbang
                        - � Kelola stress dengan baik
                        """
                    )
            
            st.markdown("---")
            st.caption(
                "⚕️ **Disclaimer:** Hasil prediksi ini bersifat informatif dan tidak menggantikan diagnosis medis profesional. "
                "Selalu konsultasikan kondisi kesehatan Anda dengan dokter."
            )
            
        except Exception as e:
            st.error(f"❌ Error saat melakukan prediksi: {str(e)}")
            st.info("💡 Pastikan semua input telah diisi dengan benar.")

    # -----------------------------------------
    # TOMBOL NAVIGASI: PREVIOUS
    # -----------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    col_prev, col_spacer, col_next = st.columns([1, 2, 1])
    
    with col_prev:
        if st.button("← Previous", use_container_width=True, key="prev_btn"):
            st.session_state["page"] = "Data Visualization"
            st.rerun()