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
            text-align: center;
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
        
        /* Style untuk Tombol Aktif - menggunakan :has() untuk target label langsung */
        [data-testid="stSidebar"] .stRadio label:has(input:checked) {{
            /* Background Khaki - full coverage */
            background-color: {PRIMARY_COLOR} !important; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
        }}
        
        /* Style Teks Tombol Aktif */
        [data-testid="stSidebar"] .stRadio label:has(input:checked) p {{
            font-weight: 700;
            color: white !important;
        }}
        
        /* Fallback untuk browser yang tidak support :has() */
        [data-testid="stSidebar"] .stRadio input:checked + div {{
            background-color: {PRIMARY_COLOR} !important; 
            margin: -0.9rem -1.5rem !important; 
            padding: 0.9rem 1.5rem !important; 
            box-shadow: none !important; 
            border-radius: 8px;
        }}
        
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
        
        /* Custom Button Styles */
        /* Tombol utama - semua button dengan border-radius */
        .stButton > button {{
            border-radius: 8px !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            padding: 12px 24px !important;
        }}
        
        /* Primary button - Brown style (matching sidebar) */
        .stButton > button[kind="primary"] {{
            background-color: {PRIMARY_COLOR} !important;
            color: white !important;
            border: none !important;
        }}
        .stButton > button[kind="primary"]:hover {{
            background-color: #8B6914 !important;
        }}
        
        /* Secondary/default buttons - Brown (matching sidebar) */
        .stButton > button[kind="secondary"],
        .stButton > button:not([kind="primary"]) {{
            background-color: {PRIMARY_COLOR} !important;
            color: white !important;
            border: none !important;
        }}
        .stButton > button[kind="secondary"]:hover,
        .stButton > button:not([kind="primary"]):hover {{
            background-color: #8B6914 !important;
        }}
        
        /* === HOME PAGE STYLES === */
        
        /* Hero Section */
        .hero-section {{
            background: linear-gradient(135deg, {LIGHT_BEIGE} 0%, #E8DFD5 100%);
            padding: 3rem 2rem;
            border-radius: 16px;
            text-align: center;
            margin-bottom: 2rem;
            border: 1px solid rgba(166, 125, 69, 0.2);
        }}
        
        .hero-title {{
            color: {PRIMARY_COLOR} !important;
            font-size: 2.2rem !important;
            font-weight: 700 !important;
            margin-bottom: 1rem !important;
            line-height: 1.3 !important;
        }}
        
        .hero-subtitle {{
            color: #555;
            font-size: 1.1rem;
            line-height: 1.6;
            max-width: 700px;
            margin: 0 auto;
            text-align: center !important;
        }}
        
        /* Workflow Section */
        .workflow-header {{
            text-align: center;
            margin: 2rem 0 1.5rem 0;
        }}
        
        .workflow-header h2 {{
            color: #333;
            font-size: 1.6rem;
            font-weight: 600;
            position: relative;
            display: inline-block;
        }}
        
        /* Workflow Cards */
        .workflow-card {{
            background: white;
            padding: 1.5rem 1rem;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            border: 1px solid #eee;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            min-height: 180px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
        }}
        
        .workflow-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        }}
        
        .step-number {{
            background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, #8B6914 100%);
            color: white;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 0.95rem;
            margin-bottom: 0.8rem;
        }}
        
        .step-icon {{
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }}
        
        .step-title {{
            color: #333;
            font-weight: 600;
            font-size: 1rem;
            margin-bottom: 0.4rem;
        }}
        
        .step-desc {{
            color: #777;
            font-size: 0.85rem;
            line-height: 1.4;
        }}
        
        /* Home Footer */
        .home-footer {{
            text-align: center;
            margin-top: 3rem;
            padding: 1.5rem;
            border-top: 1px solid #ddd;
            color: #666;
        }}
        
        .home-footer p {{
            margin: 0.3rem 0;
            font-size: 0.9rem;
        }}
        
        .footer-brand {{
            color: {PRIMARY_COLOR};
            font-weight: 600;
        }}
        
        /* === ABOUT US PAGE STYLES (TABLE LAYOUT) === */
        
        /* Team Table Container */
        .team-table-container {{
            display: flex;
            justify-content: center;
            padding: 1rem 0;
        }}
        
        .team-table {{
            border-collapse: separate;
            border-spacing: 30px 0;
            margin: 0 auto;
        }}
        
        /* Member Cell */
        .member-cell {{
            background: white;
            padding: 2rem 2.5rem;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border: 1px solid #eee;
            vertical-align: top;
            min-width: 200px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .member-cell:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        }}
        
        /* Photo Wrapper - Circular */
        .photo-wrapper {{
            width: 130px;
            height: 130px;
            margin: 0 auto 1.2rem auto;
            border-radius: 50%;
            border: 4px solid {PRIMARY_COLOR};
            overflow: hidden;
            background: {LIGHT_BEIGE};
        }}
        
        .photo-wrapper img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }}
        
        .photo-placeholder {{
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.5rem;
            font-weight: 700;
            color: {PRIMARY_COLOR};
            background: {LIGHT_BEIGE};
        }}
        
        /* Name Text */
        .name-text {{
            color: #333;
            font-weight: 700;
            font-size: 1.15rem;
            margin-bottom: 0.8rem;
        }}
        
        /* NIM Badge */
        .nim-badge {{
            display: inline-block;
            background: {LIGHT_BEIGE};
            color: {PRIMARY_COLOR};
            padding: 0.5rem 1.2rem;
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: 500;
            border: 2px solid {PRIMARY_COLOR};
        }}
        
        /* About Info Section */
        .about-info-section {{
            background: {LIGHT_BEIGE};
            padding: 1.5rem 2rem;
            border-radius: 12px;
            text-align: center;
            margin-top: 1rem;
        }}
        
        .about-info-section p {{
            margin: 0.3rem 0;
            color: #555;
            font-size: 0.95rem;
        }}
        
        /* Member Card with Hover Animation */
        .member-card-hover {{
            background: white;
            padding: 25px 20px;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            border: 1px solid #eee;
            margin: 0 5px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .member-card-hover:hover {{
            transform: translateY(-8px);
            box-shadow: 0 12px 35px rgba(0,0,0,0.15);
        }}
        
        </style>
        """,
        unsafe_allow_html=True,
    )