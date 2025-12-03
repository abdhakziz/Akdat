import streamlit as st
import pandas as pd

# Fungsi utama halaman "Input Dataset"
def show_upload_dataset():
    # Judul halaman
    st.title("📂 Input Dataset")
    
    # Card penjelasan singkat
    st.markdown(
        """
        <div class="data-card">
            <p style="font-size: 1 rem; color: #555; margin-bottom: 1rem;">
                Silakan unggah file <strong>CSV</strong> dataset <em>Hipertensi Prediction</em> atau data kesehatan pasien.
                Setelah upload berhasil, preview data akan ditampilkan.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Komponen untuk memilih & mengunggah file CSV
    uploaded_file = st.file_uploader(
        "Pilih file CSV",
        type=["csv"],
        help="Upload file CSV dengan format yang sesuai"
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state["raw_df"] = df
            st.success("✅ Dataset berhasil diupload!")
            
            # -----------------------------
            #  METRIK RINGKAS DATASET
            # -----------------------------
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Total Baris", f"{df.shape[0]:,}")
            with col2:
                st.metric("📋 Total Kolom", f"{df.shape[1]:,}")
            with col3:
                st.metric(
                    "💾 Ukuran Data",
                    f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB"
                )

            st.markdown("### 🔍 Preview Data (5 baris pertama)")
            st.dataframe(df.head(), use_container_width=True)
            
            # -----------------------------
            #  INFORMASI TIPE & MISSING
            # -----------------------------
            st.markdown("### 📈 Informasi Kolom")
            col_info = pd.DataFrame({
                'Kolom': df.columns,              
                'Tipe Data': df.dtypes.values,    
                'Non-Null Count': df.count().values,   
                'Null Count': df.isna().sum().values   
            })
            st.dataframe(col_info, use_container_width=True)

            # Tombol untuk langsung pindah ke halaman preprocessing
            if st.button("➡️ Lanjut ke Preprocessing", use_container_width=False):
                st.session_state["page"] = "Preprocessing Data"  
                st.rerun()  
                
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan saat membaca file CSV: {e}")
            st.info("💡 Pastikan file CSV Anda memiliki format yang benar dan tidak corrupt.")