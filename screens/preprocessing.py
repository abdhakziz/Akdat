import streamlit as st
import pandas as pd
from helpers import preprocess_data


def show_preprocessing():
    # Judul utama halaman preprocessing
    st.markdown("<h1 style='text-align: center; color: #A67D45;'>Preprocessing Data</h1>", unsafe_allow_html=True)

    # Pastikan dataset mentah sudah di-upload
    if st.session_state.get("raw_df") is None:
        st.warning("⚠️ Silakan upload dataset terlebih dahulu di halaman **Input Dataset**.")
        if st.button("← Kembali ke Input Dataset"):
            st.session_state["page"] = "Upload Dataset"
            st.rerun()
        return
    
    df_raw = st.session_state["raw_df"]

    # -----------------------------------------
    # INFORMASI DATASET - Jumlah Baris & Kolom
    # -----------------------------------------
    st.markdown("""
    <div style="background: #F0E9E1; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; gap: 20px;">
            <div style="flex: 1; display: flex; align-items: center; gap: 15px;">
                <span style="color: #A67D45; font-weight: 600;">Jumlah Baris:</span>
                <div style="background: #E8E0D5; border-radius: 8px; padding: 10px 30px; flex: 1; text-align: center; font-weight: 600; color: #555;">
                    """ + f"{df_raw.shape[0]:,}" + """
                </div>
            </div>
            <div style="flex: 1; display: flex; align-items: center; gap: 15px;">
                <span style="color: #A67D45; font-weight: 600;">Jumlah Kolom:</span>
                <div style="background: #E8E0D5; border-radius: 8px; padding: 10px 30px; flex: 1; text-align: center; font-weight: 600; color: #555;">
                    """ + f"{df_raw.shape[1]:,}" + """
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------
    # JUMLAH BARIS DUPLIKAT
    # -----------------------------------------
    duplicates_count = df_raw.duplicated().sum()
    st.markdown("""
    <div style="background: #F0E9E1; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
        <div style="text-align: center; margin-bottom: 10px;">
            <span style="color: #A67D45; font-weight: 600;">Jumlah Baris Duplikat:</span>
        </div>
        <div style="background: #E8E0D5; border-radius: 8px; padding: 12px; text-align: center; font-weight: 600; color: #555;">
            """ + f"{duplicates_count:,}" + """
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------
    # JUMLAH TOTAL NILAI NULL
    # -----------------------------------------
    null_count = df_raw.isna().sum().sum()
    st.markdown("""
    <div style="background: #F0E9E1; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
        <div style="text-align: center; margin-bottom: 10px;">
            <span style="color: #A67D45; font-weight: 600;">Jumlah Total Nilai Null:</span>
        </div>
        <div style="background: #E8E0D5; border-radius: 8px; padding: 12px; text-align: center; font-weight: 600; color: #555;">
            """ + f"{null_count:,}" + """
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------
    # TOMBOL HAPUS DUPLIKAT DAN NILAI NULL
    # -----------------------------------------
    col_btn = st.columns([1, 2, 1])
    with col_btn[1]:
        if st.button("🧹 Hapus Duplikat dan Nilai Null", use_container_width=True, key="run_preprocess"):
            with st.spinner("⏳ Sedang memproses data..."):
                # Panggil fungsi preprocess_data dari helpers (tanpa kolom target spesifik)
                clean_df, info = preprocess_data(df_raw)
                
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
        st.markdown("<h3 style='color: #A67D45;'>📈 Hasil Preprocessing</h3>", unsafe_allow_html=True)
        
        # Tampilkan ringkasan hasil
        st.markdown("""
        <div style="background: #d4edda; border-radius: 12px; padding: 20px; margin-bottom: 20px; border-left: 4px solid #28a745;">
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 15px;">
                <div style="text-align: center;">
                    <div style="font-weight: 600; color: #155724;">Baris Setelah</div>
                    <div style="font-size: 1.5rem; color: #155724;">""" + f"{info['rows_after']:,}" + """</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-weight: 600; color: #155724;">Duplikat Dihapus</div>
                    <div style="font-size: 1.5rem; color: #155724;">""" + f"{info['duplicates_removed']:,}" + """</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-weight: 600; color: #155724;">Missing Value Setelah</div>
                    <div style="font-size: 1.5rem; color: #155724;">""" + f"{info['missing_total_after']:,}" + """</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Preview data hasil preprocessing
        with st.expander("🔍 Preview Data Hasil Preprocessing"):
            st.dataframe(clean_df.head(10), use_container_width=True)

    # -----------------------------------------
    # TOMBOL NAVIGASI: PREVIOUS & NEXT
    # -----------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    col_prev, col_spacer, col_next = st.columns([1, 2, 1])
    
    with col_prev:
        if st.button("← Previous", use_container_width=True, key="prev_btn"):
            st.session_state["page"] = "Upload Dataset"
            st.rerun()
    
    with col_next:
        # Tombol Next hanya aktif jika preprocessing sudah dilakukan
        if st.session_state.get("clean_df") is not None:
            if st.button("Next →", use_container_width=True, key="next_btn"):
                st.session_state["page"] = "Analisis Data"
                st.rerun()
        else:
            st.button("Next →", use_container_width=True, key="next_btn_disabled", disabled=True)