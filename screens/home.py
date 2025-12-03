import streamlit as st

# Fungsi utama untuk menampilkan halaman Home
def show_home():
    # Judul utama di tengah halaman
    st.markdown("<h1 style='text-align: center;'>❤️ Selamat Datang di TensiCare+!</h1>", unsafe_allow_html=True)
    
    # Membuat layout 2 kolom
    col1, col2 = st.columns([2, 1], gap="large")
    
    # -----------------------------------------
    # KONTEN KIRI: Penjelasan aplikasi & Alur
    # -----------------------------------------
    with col1:
        # Card sambutan utama dengan judul yang mencerminkan gambar yang dikirim user
        st.markdown(
            """
            <div class="welcome-card">
                <div class="welcome-title" style="color: #A67D45; margin-bottom: 2rem; font-size: 2.5rem;">
                    Cegah Lebih Awal, Kenali Risiko Hipertensi Anda Sekarang!
                </div>
                <div class="welcome-text">
                    Aplikasi ini dikembangkan untuk membantu masyarakat mengenali risiko 
                    <strong>tekanan darah tinggi (Hipertensi)</strong> sejak dini. 
                    Dengan memanfaatkan algoritma Classification, sistem ini dapat memberikan prediksi akurat.
                </div>
                <div class="welcome-text">
                    <strong>Alur Kerja Prediksi Hipertensi:</strong>
                    <ol style="margin-top: 1rem; line-height: 2;">
                        <li><strong>Input Dataset</strong> - Unggah file CSV data kesehatan pasien</li>
                        <li><strong>Preprocessing Data</strong> - Bersihkan dan persiapkan data</li>
                        <li><strong>Analisis Data</strong> - Latih model Machine Learning</li>
                        <li><strong>Data Visualization</strong> - Eksplorasi visualisasi data</li>
                        <li><strong>Use Model</strong> - Prediksi risiko untuk data individu</li>
                    </ol>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Tombol untuk memulai alur aplikasi
        if st.button("🚀 Mulai Sekarang", use_container_width=False):
            st.session_state["page"] = "Upload Dataset" 
            st.rerun()
    
    # -----------------------------------------
    # KONTEN KANAN: Tim Pengembang
    # -----------------------------------------
    with col2:
        # Card yang berisi daftar tim pengembang
        st.markdown(
            """
            <div class="info-card">
                <h4>👥 Tim Pengembang</h4>
                <ul style="list-style: none; padding: 0;">
                    <li><span style="font-size: 1.2rem;">👤</span> <strong>Della Khairunnisa</strong> – 2311523032</li>
                    <li><span style="font-size: 1.2rem;">👤</span> <strong>Loly Amelia Nurza</strong> – 2311521016</li>
                    <li><span style="font-size: 1.2rem;">👤</span> <strong>Abdul Hakim Aziz</strong> – 2311523020</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # Card info ringkas (opsional)
        st.markdown(
            """
            <div class="data-card" style="background: #F0E9E1; border-left: 3px solid #899581; margin-top: 2rem;">
                <p style="font-weight: 600; color: #A67D45;">
                    💡 Target Prediksi: Hipertensi
                </p>
                <p style="font-size: 0.9rem; color: #555;">
                    Tekanan darah normal adalah di bawah 120/80 mmHg.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )