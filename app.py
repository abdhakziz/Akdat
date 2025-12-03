import streamlit as st

# load external modules
from style import add_custom_css      
from state import init_session_state  
from helpers import TARGET_COL        

# import screens (Asumsi folder sudah diubah namanya menjadi 'screens')
from screens.home import show_home                      
from screens.upload_dataset import show_upload_dataset  
from screens.preprocessing import show_preprocessing    
from screens.analysis import show_analysis              
from screens.visualization import show_visualization    
from screens.prediction import show_prediction          
from screens.about import show_about   


# ----------------------------
#   STREAMLIT CONFIG
# ----------------------------
st.set_page_config(
    page_title="Prediksi Risiko Hipertensi",  
    layout="wide"                                   
)


# ----------------------------
#   INIT SESSION STATE
# ----------------------------
init_session_state()


# ----------------------------
#   LOAD GLOBAL CSS
# ----------------------------
add_custom_css()


# ----------------------------
#   SIDEBAR NAVIGATION (Fixed Logic)
# ----------------------------
with st.sidebar:
    # Logo TensiCare+
    st.markdown("""
    <div class="logo-container">
        <div class="logo-text">TensiCare+</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Daftar menu FINAL
    menu_options = (
        "Home",
        "Input Dataset",       
        "Preprocessing Data",
        "Analisis Data",
        "Data Visualization",
        "Use Model",           
    )
    
    # Mapping label menu di sidebar ke nama page/file yang sebenarnya
    menu_map = {
        "Input Dataset": "Upload Dataset",
        "Use Model": "Prediction",
    }
    
    # 1. Simpan kunci halaman saat ini sebelum diupdate oleh st.radio
    current_page_key = st.session_state.get("page", "Home")

    # 2. Tampilkan st.radio
    menu = st.radio(
        '',
        menu_options,
        index=menu_options.index(current_page_key) if current_page_key in menu_options else 0,
    )
    
    # 3. Tentukan kunci halaman yang baru dipilih
    new_page_key = menu_map.get(menu, menu)

# --- LOGIKA PERBAIKAN DOUBLE-CLICK ---
# Cek apakah menu yang dipilih berbeda dari halaman yang sedang tampil
if new_page_key != current_page_key:
    # Update session state dengan halaman baru
    st.session_state["page"] = new_page_key
    
    # FORCE RERUN: Ini yang memastikan perpindahan halaman terjadi dalam satu klik
    st.rerun()

# --- Jika tidak ada perubahan atau setelah st.rerun() (rerun terjadi), 
# maka router di bawah akan dieksekusi berdasarkan nilai terbaru dari st.session_state["page"] ---

# ----------------------------
#   PAGE ROUTER
# ----------------------------
current_page_to_show = st.session_state.get("page", "Home")

if current_page_to_show == "Home":
    show_home()
elif current_page_to_show == "Upload Dataset": 
    show_upload_dataset()
elif current_page_to_show == "Preprocessing Data":
    show_preprocessing()
elif current_page_to_show == "Analisis Data":
    show_analysis()
elif current_page_to_show == "Data Visualization":
    show_visualization()
elif current_page_to_show == "Prediction": 
    show_prediction()

# Note: Jika Anda melihat sisa-sisa tampilan menu "About" di tempat lain,
# itu karena st.session_state["page"] pernah berisi "About". Anda bisa mengabaikannya
# atau mereset session state jika diperlukan.