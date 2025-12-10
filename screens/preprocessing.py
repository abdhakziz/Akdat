import streamlit as st
import pandas as pd
import numpy as np
from helpers import preprocess_data, apply_standardization, apply_normalization


def show_preprocessing():
    # Judul utama halaman preprocessing - sesuai gambar
    st.markdown("<h1 style='text-align: center; color: #A67D45;'>Preprocessing Data</h1>", unsafe_allow_html=True)

    # Pastikan dataset mentah sudah di-upload
    if st.session_state.get("raw_df") is None:
        st.warning("⚠️ Silakan upload dataset terlebih dahulu di halaman **Input Dataset**.")
        if st.button("← Kembali ke Input Dataset"):
            st.session_state["page"] = "Upload Dataset"
            st.rerun()
        return
    
    df_raw = st.session_state["raw_df"]
    duplicates_count = df_raw.duplicated().sum()
    null_count = df_raw.isna().sum().sum()

    # -----------------------------------------
    # CARD 1: Jumlah Baris & Jumlah Kolom (side by side)
    # -----------------------------------------
    st.markdown("""
    <div style="background: #F0E9E1; border-radius: 12px; padding: 25px 30px; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; gap: 40px;">
            <div style="flex: 1; display: flex; align-items: center; gap: 15px;">
                <span style="color: #A67D45; font-weight: 600; white-space: nowrap;">Jumlah Baris:</span>
                <div style="background: #E8E0D5; border-radius: 8px; padding: 12px 20px; flex: 1; text-align: center; font-weight: 500; color: #666;">
                    """ + f"{df_raw.shape[0]:,}" + """
                </div>
            </div>
            <div style="flex: 1; display: flex; align-items: center; gap: 15px;">
                <span style="color: #A67D45; font-weight: 600; white-space: nowrap;">Jumlah Kolom:</span>
                <div style="background: #E8E0D5; border-radius: 8px; padding: 12px 20px; flex: 1; text-align: center; font-weight: 500; color: #666;">
                    """ + f"{df_raw.shape[1]:,}" + """
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------
    # CARD 2: Jumlah Baris Duplikat
    # -----------------------------------------
    st.markdown("""
    <div style="background: #F0E9E1; border-radius: 12px; padding: 25px 30px; margin-bottom: 20px;">
        <div style="text-align: center; margin-bottom: 12px;">
            <span style="color: #A67D45; font-weight: 600;">Jumlah Baris Duplikat:</span>
        </div>
        <div style="background: #E8E0D5; border-radius: 8px; padding: 12px 20px; text-align: center; font-weight: 500; color: #666;">
            """ + f"{duplicates_count:,}" + """
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------
    # CARD 3: Jumlah Total Nilai Null
    # -----------------------------------------
    st.markdown("""
    <div style="background: #F0E9E1; border-radius: 12px; padding: 25px 30px; margin-bottom: 25px;">
        <div style="text-align: center; margin-bottom: 12px;">
            <span style="color: #A67D45; font-weight: 600;">Jumlah Total Nilai Null:</span>
        </div>
        <div style="background: #E8E0D5; border-radius: 8px; padding: 12px 20px; text-align: center; font-weight: 500; color: #666;">
            """ + f"{null_count:,}" + """
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------
    # OPSI TRANSFORMASI DATA (dalam expander agar tidak mengganggu layout utama)
    # -----------------------------------------
    with st.expander("⚙️ Opsi Transformasi Data (Opsional)", expanded=False):
        transform_option = st.radio(
            "Pilih metode transformasi:",
            options=["Tidak ada transformasi", "Standarisasi (StandardScaler)", "Normalisasi (MinMaxScaler)"],
            index=0,
            key="transform_option",
            horizontal=True
        )
        st.caption("ℹ️ **Standarisasi**: Mengubah data ke skala dengan mean=0 dan std=1. **Normalisasi**: Mengubah data ke skala 0-1.")
    
    # Default jika tidak dibuka expander
    if "transform_option" not in st.session_state:
        transform_option = "Tidak ada transformasi"
    else:
        transform_option = st.session_state.get("transform_option", "Tidak ada transformasi")

    # -----------------------------------------
    # TOMBOL HAPUS DUPLIKAT DAN NILAI NULL - warna hijau sidebar
    # -----------------------------------------
    # Custom CSS for green button
    st.markdown("""
        <style>
        /* Green button for preprocessing page */
        button[kind="primary"] {
            background-color: #899581 !important;
        }
        button[kind="primary"]:hover {
            background-color: #7a8672 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    button_clicked = st.button("Hapus Duplikat dan Nilai Null", use_container_width=True, key="run_preprocess", type="primary")
    
    if button_clicked:
        with st.spinner("⏳ Sedang memproses data..."):
            # Panggil fungsi preprocess_data dari helpers
            clean_df, info = preprocess_data(df_raw)
            
            # Terapkan transformasi jika dipilih
            transform_applied = "Tidak ada"
            if transform_option == "Standarisasi (StandardScaler)":
                numeric_cols = clean_df.select_dtypes(include=[np.number]).columns.tolist()
                if numeric_cols:
                    clean_df, scaler = apply_standardization(clean_df, numeric_cols)
                    st.session_state["scaler"] = scaler
                    transform_applied = "StandardScaler"
            elif transform_option == "Normalisasi (MinMaxScaler)":
                numeric_cols = clean_df.select_dtypes(include=[np.number]).columns.tolist()
                if numeric_cols:
                    clean_df, scaler = apply_normalization(clean_df, numeric_cols)
                    st.session_state["scaler"] = scaler
                    transform_applied = "MinMaxScaler"
            
            info["transform_applied"] = transform_applied
            
            # Simpan hasil preprocessing ke session_state
            st.session_state["clean_df"] = clean_df
            st.session_state["preprocess_info"] = info
        
        st.success("✅ Preprocessing selesai!")
        st.rerun()

    # -----------------------------------------
    # HASIL PREPROCESSING (jika sudah dijalankan)
    # -----------------------------------------
    if st.session_state.get("clean_df") is not None:
        clean_df = st.session_state["clean_df"]
        info = st.session_state["preprocess_info"]
        
        st.markdown("---")
        st.markdown("<h3 style='color: #A67D45;'> Hasil Preprocessing</h3>", unsafe_allow_html=True)
        
        # Tampilkan ringkasan hasil
        transform_applied = info.get('transform_applied', 'Tidak ada')
        cols_before = info.get('cols_before', info.get('cols', 0))
        cols_after = info.get('cols_after', info.get('cols', 0))
        cols_dropped = info.get('cols_dropped', [])
        cols_dropped_count = info.get('cols_dropped_count', 0)
        
        st.markdown("""
        <div style="background: #d4edda; border-radius: 12px; padding: 20px; margin-bottom: 20px; border-left: 4px solid #28a745;">
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 15px;">
                <div style="text-align: center;">
                    <div style="font-weight: 600; color: #155724;">Baris Setelah</div>
                    <div style="font-size: 1.5rem; color: #155724;">""" + f"{info['rows_after']:,}" + """</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-weight: 600; color: #155724;">Kolom Tersisa</div>
                    <div style="font-size: 1.5rem; color: #155724;">""" + f"{cols_after:,}" + """</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-weight: 600; color: #155724;">Duplikat Dihapus</div>
                    <div style="font-size: 1.5rem; color: #155724;">""" + f"{info['duplicates_removed']:,}" + """</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-weight: 600; color: #155724;">Missing Value</div>
                    <div style="font-size: 1.5rem; color: #155724;">""" + f"{info['missing_total_after']:,}" + """</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-weight: 600; color: #155724;">Transformasi</div>
                    <div style="font-size: 1.5rem; color: #155724;">""" + transform_applied + """</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Tampilkan kolom yang dihapus jika ada
        if cols_dropped_count > 0:
            st.markdown("""
            <div style="background: #fff3cd; border-radius: 12px; padding: 15px; margin-bottom: 20px; border-left: 4px solid #ffc107;">
                <div style="font-weight: 600; color: #856404; margin-bottom: 8px;">⚠️ Kolom Tidak Relevan yang Dihapus (""" + str(cols_dropped_count) + """ kolom):</div>
                <div style="color: #856404; font-size: 0.95rem;">""" + ", ".join(cols_dropped) + """</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Preview data hasil preprocessing
        with st.expander("🔍 Preview Data Hasil Preprocessing"):
            st.dataframe(clean_df.head(10), use_container_width=True)

    # -----------------------------------------
    # TOMBOL NAVIGASI: PREVIOUS & NEXT - sesuai gambar
    # -----------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_prev, col_spacer, col_next = st.columns([1, 2, 1])
    
    with col_prev:
        if st.button("← Previous", use_container_width=True, key="prev_btn"):
            st.session_state["page"] = "Upload Dataset"
            st.rerun()
    
    with col_next:
        # Tombol Next dengan warna coklat (type=primary akan menggunakan warna primer)
        if st.session_state.get("clean_df") is not None:
            if st.button("Next →", use_container_width=True, key="next_btn", type="primary"):
                st.session_state["page"] = "Data Analysis"
                st.rerun()
        else:
            st.button("Next →", use_container_width=True, key="next_btn_disabled", disabled=True)