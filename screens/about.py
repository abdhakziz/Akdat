# screens/about.py
import streamlit as st
import base64
from pathlib import Path


def get_image_base64(image_path):
    """Convert image to base64 string for embedding in HTML."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None


def show_about():
    """Halaman About Us dengan desain modern: Tim Pengembang dalam 3 kartu."""
    
    # --- HEADER ---
    st.markdown(
        """
        <div style="text-align: center; padding: 1rem 0 2rem 0;">
            <h1 style="color: #A67D45; font-size: 2.3rem; font-weight: 700; margin-bottom: 0.5rem;">Tim Pengembang</h1>
            <p style="color: #666; font-size: 1rem; margin: 0;">Kelompok 6 Sistem Informasi, Universitas Andalas</p>
             <p style="color: #666; font-size: 1rem; margin: 0; margin-top: 10px; font-weight: 700;">Dosen Pengampu : Rahmatika Pratama Santi, M.T.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # --- TEAM MEMBER DATA (urutan: Loly, Abdul, Della) ---
    team_members = [
        {"name": "Loly Amelia Nurza", "nim": "2311521016", "img": "loly.jpg"},
        {"name": "Abdul Hakim Aziz", "nim": "2311523020", "img": "abdul.jpg"},
        {"name": "Della Khairunnisa", "nim": "2311523032", "img": "della.jpg"},
    ]
    
    # Get base path for images
    base_path = Path(__file__).parent.parent / "images"
    
    # Create 3 equal columns with spacing
    col1, col2, col3 = st.columns([1, 1, 1], gap="large")
    columns = [col1, col2, col3]
    
    for i, member in enumerate(team_members):
        with columns[i]:
            # Get image as base64
            img_path = base_path / member["img"]
            img_base64 = get_image_base64(img_path)
            
            if img_base64:
                img_html = f'<img src="data:image/jpeg;base64,{img_base64}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%;">'
            else:
                initials = "".join([n[0] for n in member["name"].split()[:2]])
                img_html = f'<div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-size: 2rem; font-weight: 700; color: #A67D45; background: #F0E9E1; border-radius: 50%;">{initials}</div>'
            
            st.markdown(
                f"""
                <div class="member-card-hover">
                    <div style="width: 300px; height: 300px; margin: 0 auto 15px auto; border-radius: 50%; border: 4px solid #A67D45; overflow: hidden; background: #F0E9E1;">
                        {img_html}
                    </div>
                    <div style="color: #333; font-weight: 700; font-size: 1.1rem; margin-bottom: 10px;">{member['name']}</div>
                    <div style="display: inline-block; background: #F0E9E1; color: #A67D45; padding: 8px 16px; border-radius: 25px; font-size: 0.85rem; font-weight: 600; border: 2px solid #A67D45;">NIM: {member['nim']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    
    # --- SPACER ---
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    
    # --- INFO SECTION ---
    st.markdown(
        """
        <div style="background: #F0E9E1; padding: 25px 40px; text-align: center; border-radius: 16px;">
            <p style="margin: 5px 0; color: #555; font-size: 0.95rem;">Website ini dikembangkan sebagai Tugas Besar Mata Kuliah <strong>Akuisisi Data</strong></p>
            <p style="margin: 5px 0; color: #555; font-size: 0.95rem;">Program Studi Sistem Informasi, Fakultas Teknologi Informasi</p>
            <p style="margin: 5px 0; color: #A67D45; font-weight: 600; font-size: 0.95rem;">Universitas Andalas</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # --- FOOTER ---
    st.markdown(
        """
        <div style="text-align: center; margin-top: 2.5rem; padding: 1.5rem; border-top: 1px solid #ddd; color: #666;">
            <p style="margin: 5px 0; font-size: 0.9rem;">© 2024 <span style="color: #A67D45; font-weight: 600;">TensiCare+</span> — Sistem Prediksi Risiko Hipertensi</p>
            <p style="margin: 5px 0; font-size: 0.9rem;">Dibuat oleh <strong>Tim Pengembang Kelompok 6</strong></p>
        </div>
        """,
        unsafe_allow_html=True,
    )
