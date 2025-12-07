# pages/analysis.py
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from helpers import (
    plot_confusion_matrix,
    plot_feature_importance,
    save_model_to_file,
)


def show_analysis():
    # Judul halaman
    st.markdown("<h1 style='text-align: center; color: #A67D45;'>Data Analysis</h1>", unsafe_allow_html=True)

    # Pastikan data sudah di-preprocess
    if st.session_state.get("clean_df") is None:
        st.warning("⚠️ Silakan lakukan preprocessing data terlebih dahulu di halaman **Preprocessing Data**.")
        if st.button("← Kembali ke Preprocessing"):
            st.session_state["page"] = "Preprocessing Data"
            st.rerun()
        return
    
    df_clean = st.session_state["clean_df"]
    columns_list = df_clean.columns.tolist()

    # -----------------------------------------
    # PILIH VARIABEL PREDIKTOR
    # -----------------------------------------
    st.markdown("""
    <div style="background: #F0E9E1; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
        <div style="margin-bottom: 10px;">
            <span style="color: #A67D45; font-weight: 600;">Pilih Variabel Prediktor</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Dropdown untuk memilih variabel prediktor (multiselect)
    # Default: semua kolom kecuali kolom terakhir (biasanya target)
    default_predictors = columns_list[:-1] if len(columns_list) > 1 else columns_list
    selected_predictors = st.multiselect(
        "Pilih kolom prediktor (fitur)",
        options=columns_list,
        default=st.session_state.get("selected_predictors", default_predictors),
        key="predictor_select",
        label_visibility="collapsed"
    )
    st.session_state["selected_predictors"] = selected_predictors

    # -----------------------------------------
    # PILIH VARIABEL TARGET
    # -----------------------------------------
    st.markdown("""
    <div style="background: #F0E9E1; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
        <div style="margin-bottom: 10px;">
            <span style="color: #A67D45; font-weight: 600;">Pilih Variabel Target</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter kolom yang tidak dipilih sebagai prediktor untuk opsi target
    available_targets = [col for col in columns_list if col not in selected_predictors] if selected_predictors else columns_list
    
    # Default target: kolom terakhir atau kolom yang tersisa
    default_target = columns_list[-1] if columns_list else None
    if default_target in selected_predictors and available_targets:
        default_target = available_targets[0]
    
    selected_target = st.selectbox(
        "Pilih kolom target (label)",
        options=available_targets if available_targets else columns_list,
        index=0,
        key="target_select",
        label_visibility="collapsed"
    )
    st.session_state["target_col"] = selected_target

    # -----------------------------------------
    # HASIL ANALISIS
    # -----------------------------------------


    # Tombol untuk menjalankan analisis
    if selected_predictors and selected_target:
        if st.button("🚀 Jalankan Analisis", use_container_width=True, key="run_analysis"):
            with st.spinner("⏳ Sedang melatih model Random Forest..."):
                try:
                    X = df_clean[selected_predictors]
                    y = df_clean[selected_target]
                    
                    # Simpan features untuk digunakan di halaman lain
                    st.session_state["features"] = selected_predictors
                    
                    X_train, X_test, y_train, y_test = train_test_split(
                        X, y, test_size=0.2, random_state=42
                    )
                    
                    model = RandomForestClassifier(
                        n_estimators=200,
                        random_state=42,
                        class_weight="balanced",
                        n_jobs=-1,
                    )
                    
                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_test)
                    
                    acc = accuracy_score(y_test, y_pred)
                    cm = confusion_matrix(y_test, y_pred)
                    report = classification_report(y_test, y_pred, output_dict=True)
                    
                    st.session_state["rf_model"] = model
                    st.session_state["acc"] = acc
                    st.session_state["cm"] = cm
                    st.session_state["report"] = report
                    st.session_state["X_cols"] = X.columns.tolist()
                    
                    st.success("✅ Analisis selesai!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error saat analisis: {str(e)}")
    else:
        st.info("ℹ️ Pilih variabel prediktor dan target terlebih dahulu untuk menjalankan analisis.")

    # -----------------------------------------
    # TAMPILKAN HASIL JIKA SUDAH ADA
    # -----------------------------------------
    if st.session_state.get("rf_model") is not None:
        acc = st.session_state["acc"]
        cm = st.session_state["cm"]
        report = st.session_state["report"]
        X_cols = st.session_state["X_cols"]
        model = st.session_state["rf_model"]
        
        # Tampilkan hasil dalam card hijau
        st.markdown("""
        <div style="background: #d4edda; border-radius: 12px; padding: 20px; margin-bottom: 20px; border-left: 4px solid #28a745;">
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 15px;">
                <div style="text-align: center;">
                    <div style="font-weight: 600; color: #155724;">Akurasi Model</div>
                    <div style="font-size: 1.8rem; color: #155724;">""" + f"{acc*100:.2f}%" + """</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-weight: 600; color: #155724;">Jumlah Fitur</div>
                    <div style="font-size: 1.8rem; color: #155724;">""" + f"{len(X_cols)}" + """</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Expander untuk detail
        with st.expander("📊 Lihat Confusion Matrix"):
            unique_labels = df_clean[selected_target].unique()
            labels = [f"Class {i}" for i in sorted(unique_labels)]
            plot_confusion_matrix(cm, labels=labels)
        
        with st.expander("📈 Lihat Classification Report"):
            report_df = pd.DataFrame(report).transpose()
            st.dataframe(report_df.style.background_gradient(cmap="Greens"), use_container_width=True)
        
        with st.expander("🎯 Lihat Feature Importance"):
            plot_feature_importance(model, X_cols)
        
        # -----------------------------------------
        # TOMBOL SIMPAN MODEL
        # -----------------------------------------
        st.markdown("---")
        st.markdown("### 💾 Simpan Model")
        st.info("ℹ️ Simpan model terlatih ke file `.pkl` untuk digunakan nanti di halaman Use Model.")
        
        model_buffer = save_model_to_file(model, X_cols)
        st.download_button(
            label="📥 Download Model (.pkl)",
            data=model_buffer,
            file_name="tensicare_model.pkl",
            mime="application/octet-stream",
            use_container_width=True,
            key="download_model_btn"
        )

    # -----------------------------------------
    # TOMBOL NAVIGASI: PREVIOUS & NEXT
    # -----------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    col_prev, col_spacer, col_next = st.columns([1, 2, 1])
    
    with col_prev:
        if st.button("← Previous", use_container_width=True, key="prev_btn"):
            st.session_state["page"] = "Preprocessing Data"
            st.rerun()
    
    with col_next:
        if st.session_state.get("rf_model") is not None:
            if st.button("Next →", use_container_width=True, key="next_btn"):
                st.session_state["page"] = "Data Visualization"
                st.rerun()
        else:
            st.button("Next →", use_container_width=True, key="next_btn_disabled", disabled=True)