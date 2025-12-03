# pages/about.py
import streamlit as st


def show_about():
    # Judul utama halaman "About"
    st.title("ℹ️ Tentang Aplikasi")

    # Card deskripsi umum aplikasi
    st.markdown(
        """
        <div class="welcome-card">
            <h3>📱 Sistem Prediksi Risiko Hipertensi di Indonesia</h3> # Diubah
            <p style="line-height: 1.8; color: #555;">
                Aplikasi ini dikembangkan sebagai tugas besar mata kuliah <strong>Akuisisi Data</strong> 
                di Program Studi Sistem Informasi, Fakultas Teknologi Informasi, Universitas Andalas.
            </p>
            <p style="line-height: 1.8; color: #555;">
                Memanfaatkan algoritma <strong>Random Forest Classifier</strong> untuk memprediksi 
                probabilitas risiko Hipertensi berdasarkan data kesehatan dan gaya hidup pasien. # Diubah
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="large")

    # =======================
    # KOLOM KIRI: TIM & DOSEN
    # =======================
    with col1:
        st.markdown("### 👥 Kelompok 4 - Tim Pengembang")
        st.markdown(
            """
            <div class="data-card">
                <ul style="list-style: none; padding: 0; line-height: 2.5;">
                    <li>👤 <strong>Della Khairunnisa</strong> — 2311523032</li>
                    <li>👤 <strong>Loly Amelia Nurza</strong> — 2311521016</li>
                    <li>👤 <strong>Abdul Hakim Aziz</strong> — 2311523020</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### 👨‍🏫 Dosen Pengampu")
        st.markdown(
            """
            <div class="data-card">
                <p style="font-size: 1.1rem; color: #555;">
                    <strong>Rahmatika Pratama Santi, M.T</strong>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ==========================
    # KOLOM KANAN: TEKNOLOGI
    # ==========================
    with col2:
        st.markdown("### 🛠️ Teknologi yang Digunakan")
        st.markdown(
            """
            <div class="data-card">
                <ul style="line-height: 2;">
                    <li>🐍 <strong>Python</strong> - Bahasa pemrograman</li>
                    <li>🎨 <strong>Streamlit</strong> - Framework web interaktif</li>
                    <li>📊 <strong>Pandas & NumPy</strong> - Pengolahan data</li>
                    <li>🤖 <strong>Scikit-learn</strong> - Machine learning</li>
                    <li>📈 <strong>Matplotlib & Seaborn</strong> - Visualisasi</li>
                    <li>🌳 <strong>Random Forest</strong> - Algoritma prediksi</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### 🔄 Alur Kerja Aplikasi")

    # List berisi tahapan alur kerja, diperbarui labelnya
    steps = [
        ("1️⃣", "Home", "Pengenalan aplikasi TensiCare+ dan tombol mulai"),
        ("2️⃣", "Input Dataset", "Unggah file CSV dataset kesehatan (Diubah)"),
        ("3️⃣", "Preprocessing Data", "Pembersihan data dan penanganan missing values"),
        ("4️⃣", "Analisis Data", "Training model Random Forest dan evaluasi performa"),
        ("5️⃣", "Data Visualization", "Eksplorasi grafik distribusi, korelasi, dan feature importance"),
        ("6️⃣", "Use Model", "Input data kesehatan personal dan prediksi risiko Hipertensi (Diubah)"),
        ("7️⃣", "About", "Informasi tim pengembang dan teknologi"),
    ]

    # Loop untuk menampilkan setiap step
    for icon, title, desc in steps:
        st.markdown(
            f"""
            <div class="data-card" style="margin-bottom: 1rem;">
                <h4 style="color: #A67D45; margin-bottom: 0.5rem;">{icon} {title}</h4> # Ganti warna teks
                <p style="color: #666; margin: 0;">{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    # Footer ucapan terima kasih dengan warna baru
    st.markdown(
        """
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #A67D45 0%, #837057 100%); 
                    border-radius: 12px; color: white;">
            <h3 style="color: white;">❤️ Terima kasih telah menggunakan aplikasi ini!</h3>
            <p style="color: white; margin-top: 1rem;">
                Dikembangkan dengan ❤️ oleh Kelompok 4 - Sistem Informasi UNAND
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )