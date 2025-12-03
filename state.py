# state.py
import streamlit as st

def init_session_state():
    """
    Inisialisasi semua variabel st.session_state yang dibutuhkan aplikasi Prediksi Hipertensi.
    """

    if "page" not in st.session_state:
        st.session_state["page"] = "Home"

    if "raw_df" not in st.session_state:
        st.session_state["raw_df"] = None

    if "clean_df" not in st.session_state:
        st.session_state["clean_df"] = None

    if "rf_model" not in st.session_state:
        st.session_state["rf_model"] = None

    # Menyimpan daftar nama fitur yang digunakan sebagai input model
    if "features" not in st.session_state:
        st.session_state["features"] = [
            "age",
            "hypertension",  # Kolom ini bisa menjadi fitur, atau kolom target (tergantung dataset)
            "blood_pressure_systolic",
            "blood_pressure_diastolic",
            "diabetes",
            "cholesterol_level",
            "cholesterol_hdl",
            "cholesterol_ldl",
            "triglycerides",
            "fasting_blood_sugar",
            "obesity",
            "waist_circumference",
            "previous_heart_disease", # Biarkan ini sebagai fitur pendukung risiko kardio
            "smoking_status",
            "physical_activity",
        ]


def reset_state():
    """ ... (Tidak ada perubahan) ... """
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    init_session_state()