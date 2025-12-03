import streamlit as st

# Mendefinisikan warna sesuai skema
PRIMARY_COLOR = "#A67D45"    # Khaki/Brown (Warna Tombol Aktif)
SECONDARY_COLOR = "#899581"  # Muted Green (Warna Background Sidebar)
LIGHT_BEIGE = "#F0E9E1"      # Lighter Beige (Warna Tombol Non-Aktif)
TEXT_INACTIVE = "#333333"    # Warna Teks Tombol Non-Aktif

def add_custom_css():
    """
    Menyuntikkan CSS kustom untuk tampilan sidebar yang bersih, menghilangkan lingkaran,
    dan memperbaiki masalah duplikasi warna/shadow.
    """
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        * {{ font-family: 'Inter', sans-serif; }}
        
        /* Styling untuk sidebar (Background Muted Green) */
        [data-testid="stSidebar"] {{
            background-color: {SECONDARY_COLOR}; 
            padding-top: 2rem;
        }}
        
        /* Teks logo TensiCare+ */
        .logo-text {{
            font-size: 2rem;
            font-weight: 700;
            color: white;
            letter-spacing: 2px;
            padding-bottom: 10px;
            border-bottom: 2px solid white; 
            margin-bottom: 1rem;
        }}

        /* Container radio button */
        [data-testid="stSidebar"] .stRadio > div {{
            display: flex;
            flex-direction: column;
            gap: 10px; 
            padding-left: 1rem;
            padding-right: 1rem;
        }}
        
        /* 1. FIX LINGKARAN LIST (BULAT-BULAT) */
        /* Menyembunyikan semua elemen internal yang membentuk lingkaran list */
        [data-testid="stSidebar"] .stRadio input[type="radio"], 
        [data-testid="stSidebar"] .stRadio label > div:first-child {{
            display: none !important;
        }}
        
        /* 2. FIX DUPLIKASI WARNA & LAYERED SHADOW/COLOR */
        
        /* Style untuk setiap label opsi radio (Tombol Non-Aktif) */
        [data-testid="stSidebar"] .stRadio label {{
            background-color: {LIGHT_BEIGE}; 
            padding: 0.9rem 1.5rem; 
            border-radius: 8px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2); 
            width: 100%;
            margin: 0;
            /* Pastikan elemen internal tidak bocor */
            overflow: hidden; 
        }}
        
        /* Efek hover pada label radio (Menggunakan warna Khaki gelap) */
        [data-testid="stSidebar"] .stRadio label:hover {{
            background-color: #837057; 
            color: white !important;
            box-shadow: 0 6px 10px rgba(0,0,0,0.3);
        }}
        
        /* Style Teks saat hover */
        [data-testid="stSidebar"] .stRadio label:hover p {{
            color: white !important;
        }}
        
        /* Style untuk Tombol Aktif (Menggunakan Trik Margin Negatif untuk menutupi lapisan beige) */
        [data-testid="stSidebar"] .stRadio input:checked + div {{
            /* Background Khaki */
            background-color: {PRIMARY_COLOR} !important; 
            
            /* Gunakan margin negatif: Angka ini harus menutupi padding label 0.9rem x 1.5rem */
            margin: -0.9rem -1.5rem !important; 
            padding: 0.9rem 1.5rem !important; 
            
            /* Reset shadow pada elemen internal yang aktif agar tidak double */
            box-shadow: none !important; 
            border-radius: 8px;
        }}
        
        /* Style Teks Tombol Aktif */
        [data-testid="stSidebar"] .stRadio input:checked + div p {{
            font-weight: 700;
            color: white !important;
        }}

        /* FIX TEKS MEMBUNGKUS ("Preprocessing Data") */
        [data-testid="stSidebar"] .stRadio p {{
            font-size: 1.05rem; 
            color: #333 !important;
            white-space: normal; /* Memastikan teks bisa membungkus tanpa memotong */
            margin: 0;
            line-height: 1.2;
        }}
        
        /* Menghilangkan elemen sidebar yang tidak perlu */
        [data-testid="stSidebar"] h3, .stRadio > label {{
             display: none !important;
        }}
        
        /* --- STYLING UMUM LAINNYA --- */
        .welcome-card {{
            background: {LIGHT_BEIGE}; 
            padding: 2.5rem;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border-left: 5px solid {PRIMARY_COLOR}; 
            margin-bottom: 2rem;
        }}
        h1 {{ color: {PRIMARY_COLOR}; font-weight: 700; margin-bottom: 1.5rem; }}
        </style>
        """,
        unsafe_allow_html=True,
    )