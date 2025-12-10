import streamlit as st

def show_home():
    """Halaman Home dengan desain modern: Hero Section, Alur Kerja, dan Footer."""
    
    # --- HERO SECTION ---
    st.markdown(
        """
        <div class="hero-section">
            <h1 class="hero-title">Prediksi Risiko Hipertensi<br/>Berbasis Machine Learning</h1>
            <p class="hero-subtitle" style="text-align: center; margin-left: auto; margin-right: auto;">
                Deteksi dini risiko tekanan darah tinggi dengan algoritma <strong>Random Forest</strong>. Masukkan 
                data medis Anda, dapatkan hasil prediksi dalam sekejap.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # --- ALUR KERJA SISTEM ---
    st.markdown(
        """
        <div class="workflow-header">
            <h2>Alur Kerja Sistem</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Workflow steps dengan 5 kolom
    cols = st.columns(5, gap="medium")
    
    workflow_steps = [
        {"num": "1", "icon": "📥", "title": "Input Dataset", "desc": "Upload file CSV data kesehatan"},
        {"num": "2", "icon": "🔄", "title": "Preprocessing", "desc": "Pembersihan & persiapan data"},
        {"num": "3", "icon": "📊", "title": "Analisis Data", "desc": "Training model Random Forest"},
        {"num": "4", "icon": "📉", "title": "Visualisasi", "desc": "Eksplorasi data interaktif"},
        {"num": "5", "icon": "🎯", "title": "Prediksi", "desc": "Hasil risiko hipertensi"},
    ]
    
    for i, step in enumerate(workflow_steps):
        with cols[i]:
            st.markdown(
                f"""
                <div class="workflow-card">
                    <div class="step-number">{step['num']}</div>
                    <div class="step-icon">{step['icon']}</div>
                    <div class="step-title">{step['title']}</div>
                    <div class="step-desc">{step['desc']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    
    # --- TOMBOL CTA ---
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        # Custom styled button for home page only
        button_clicked = st.button("Mulai Prediksi Sekarang", use_container_width=True, key="cta_button")
        
        # Apply custom burgundy color to this specific button
        st.markdown("""
            <style>
            div[data-testid="stVerticalBlock"] div[data-testid="column"]:nth-child(2) .stButton > button {
                background-color: #5D1C34 !important;
            }
            div[data-testid="stVerticalBlock"] div[data-testid="column"]:nth-child(2) .stButton > button:hover {
                background-color: #4a1629 !important;
            }
            </style>
        """, unsafe_allow_html=True)
        
        if button_clicked:
            st.session_state["page"] = "Upload Dataset"
            st.rerun()
    
    # --- FOOTER ---
    st.markdown(
        """
        <div class="home-footer">
            <p>© 2024 <span class="footer-brand">TensiCare+</span> — Sistem Prediksi Risiko Hipertensi</p>
            <p>Dibuat oleh <strong>Tim Pengembang Kelompok 6</strong></p>
        </div>
        """,
        unsafe_allow_html=True,
    )