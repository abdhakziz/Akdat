import streamlit as st
import pandas as pd

# Fungsi utama halaman "Input Dataset"
def show_upload_dataset():
    # Judul halaman - centered seperti halaman lainnya
    st.markdown("<h1 style='text-align: center; color: #A67D45;'>Input Dataset</h1>", unsafe_allow_html=True)
    
    # Custom CSS untuk styling file uploader yang lebih besar dan menarik
    st.markdown("""
        <style>
        /* Container utama upload */
        .upload-container {
            background: #ffffff;
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        }
        
        .upload-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: #333;
            margin-bottom: 20px;
        }
        
        /* Area drag & drop */
        .upload-dropzone {
            border: 2px dashed #ccc;
            border-radius: 12px;
            padding: 50px 30px;
            text-align: center;
            background: #fafafa;
            transition: all 0.3s ease;
        }
        
        .upload-dropzone:hover {
            border-color: #4A90D9;
            background: #f0f7ff;
        }
        
        /* Ikon cloud */
        .cloud-icon {
            width: 70px;
            height: 70px;
            margin: 0 auto 20px;
            background: linear-gradient(135deg, #e8e8e8 0%, #d0d0d0 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .cloud-icon svg {
            width: 40px;
            height: 40px;
            fill: #888;
        }
        
        .upload-main-text {
            font-size: 1.25rem;
            font-weight: 600;
            color: #333;
            margin-bottom: 8px;
        }
        
        .upload-sub-text {
            font-size: 0.95rem;
            color: #888;
            margin-bottom: 20px;
        }
        
        /* File info badges */
        .file-info-container {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-bottom: 25px;
            flex-wrap: wrap;
        }
        
        .file-info-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }
        
        .badge-csv {
            background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
            color: #155724;
            border: 1px solid #28a745;
        }
        
        .badge-size {
            background: linear-gradient(135deg, #fff3cd 0%, #ffeeba 100%);
            color: #856404;
            border: 1px solid #ffc107;
        }
        
        /* Styling untuk Streamlit file uploader */
        [data-testid="stFileUploader"] {
            padding: 0 !important;
        }
        
        [data-testid="stFileUploader"] > div {
            padding: 0 !important;
        }
        
        [data-testid="stFileUploader"] section {
            padding: 0 !important;
        }
        
        [data-testid="stFileUploader"] section > div {
            display: none !important;
        }
        
        [data-testid="stFileUploader"] section {
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            align-items: stretch !important;
            width: 100% !important;
        }
        
        /* Make all containers full width */
        [data-testid="stFileUploader"],
        [data-testid="stFileUploader"] > div,
        [data-testid="stFileUploader"] > div > div,
        [data-testid="stFileUploader"] section,
        [data-testid="stFileUploader"] section > div {
            width: 100% !important;
            max-width: 100% !important;
        }
        
        [data-testid="stFileUploader"] section > button {
            background: linear-gradient(135deg, #899581 0%, #7a8672 100%) !important;
            color: white !important;
            border: none !important;
            padding: 14px 30px !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(137, 149, 129, 0.3) !important;
            width: 100% !important;
            max-width: 100% !important;
        }
        
        [data-testid="stFileUploader"] section > button:hover {
            background: linear-gradient(135deg, #7a8672 0%, #6b7763 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(137, 149, 129, 0.4) !important;
        }
        
        /* Hide default drag & drop text */
        [data-testid="stFileUploader"] small {
            display: none !important;
        }
        
        /* Browse button styling - multiple selectors for compatibility */
        [data-testid="stFileUploader"] button,
        [data-testid="stFileUploadDropzone"] button,
        [data-testid="baseButton-secondary"],
        .stFileUploader button,
        .uploadedFile button,
        div[data-testid="stFileUploader"] button[kind="secondary"],
        div[data-testid="stFileUploader"] button[data-testid="baseButton-secondary"] {
            background: linear-gradient(135deg, #899581 0%, #7a8672 100%) !important;
            background-color: #899581 !important;
            color: white !important;
            border: none !important;
            padding: 14px 30px !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(137, 149, 129, 0.3) !important;
            width: 100% !important;
        }
        
        [data-testid="stFileUploader"] button:hover,
        [data-testid="stFileUploadDropzone"] button:hover,
        [data-testid="baseButton-secondary"]:hover,
        .stFileUploader button:hover,
        div[data-testid="stFileUploader"] button:hover {
            background: linear-gradient(135deg, #7a8672 0%, #6b7763 100%) !important;
            background-color: #7a8672 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(137, 149, 129, 0.4) !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Card Upload File Data dengan desain yang lebih menarik
    st.markdown("""
        <div class="upload-container">
            <div class="upload-title">📂 Upload File Data</div>
            <div class="upload-dropzone">
                <div class="cloud-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96zM14 13v4h-4v-4H7l5-5 5 5h-3z"/>
                    </svg>
                </div>
                <div class="upload-main-text">Drag & Drop file di sini</div>
                <div class="upload-sub-text">atau klik tombol di bawah untuk memilih file</div>
                <div class="file-info-container">
                    <span class="file-info-badge badge-csv">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6zm4 18H6V4h7v5h5v11z"/>
                        </svg>
                        Didukung file .CSV
                    </span>
                    <span class="file-info-badge badge-size">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
                        </svg>
                        Maks. 200MB
                    </span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Komponen untuk memilih & mengunggah file CSV (dengan label tersembunyi)
    uploaded_file = st.file_uploader(
        "Pilih File Dataset",
        type=["csv"],
        help="Upload file CSV dengan format yang sesuai",
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state["raw_df"] = df
            st.success("✅ Dataset berhasil diupload!")
            
            # -----------------------------
            #  METRIK RINGKAS DATASET (STYLED)
            # -----------------------------
            st.markdown(
                f"""
                <div style="display: flex; gap: 20px; margin: 1.5rem 0;">
                    <div style="flex: 1; background: linear-gradient(135deg, #A67D45 0%, #8B6914 100%); padding: 20px; border-radius: 12px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(166, 125, 69, 0.3);">
                        <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 5px;">📊 Total Baris</div>
                        <div style="font-size: 2rem; font-weight: 700;">{df.shape[0]:,}</div>
                    </div>
                    <div style="flex: 1; background: linear-gradient(135deg, #A67D45 0%, #8B6914 100%); padding: 20px; border-radius: 12px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(166, 125, 69, 0.3);">
                        <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 5px;">📋 Total Kolom</div>
                        <div style="font-size: 2rem; font-weight: 700;">{df.shape[1]:,}</div>
                    </div>
                    <div style="flex: 1; background: linear-gradient(135deg, #A67D45 0%, #8B6914 100%); padding: 20px; border-radius: 12px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(166, 125, 69, 0.3);">
                        <div style="font-size: 0.9rem; opacity: 0.9; margin-bottom: 5px;">💾 Ukuran Data</div>
                        <div style="font-size: 2rem; font-weight: 700;">{df.memory_usage(deep=True).sum() / 1024:.2f} KB</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("###  Preview Data (5 baris pertama)")
            st.dataframe(df.head(), use_container_width=True)
            
            # -----------------------------
            #  INFORMASI TIPE & MISSING
            # -----------------------------
            st.markdown("###  Informasi Kolom")
            col_info = pd.DataFrame({
                'Kolom': df.columns,              
                'Tipe Data': df.dtypes.values,    
                'Non-Null Count': df.count().values,   
                'Null Count': df.isna().sum().values   
            })
            st.dataframe(col_info, use_container_width=True)

            # Tombol untuk langsung pindah ke halaman preprocessing (positioned right)
            col1, col2, col3 = st.columns([3, 1, 1])
            with col3:
                if st.button("Lanjut ke Preprocessing →", use_container_width=True, key="btn_lanjut"):
                    st.session_state["page"] = "Preprocessing Data"  
                    st.rerun()  
                
        except Exception as e:
            st.error(f"❌ Terjadi kesalahan saat membaca file CSV: {e}")
            st.info("💡 Pastikan file CSV Anda memiliki format yang benar dan tidak corrupt.")