# pages/analysis.py
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from helpers import (
    require_clean_data,
    plot_confusion_matrix,
    plot_feature_importance,
    TARGET_COL,
)


def show_analysis():
    # Judul halaman Analisis / Training model
    st.title("🧠 Training Model & Evaluasi")

    require_clean_data()
    df_clean = st.session_state["clean_df"]

    # Card penjelasan singkat
    st.markdown(
        """
        <div class="data-card">
            <p style="font-size: 1rem; color: #555;">
                Pada halaman ini, model <strong>Random Forest Classifier</strong> akan dilatih menggunakan 
                data hasil preprocessing untuk memprediksi risiko Hipertensi.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------
    # Pengaturan Model
    # -----------------------------------------
    with st.expander("⚙️ Pengaturan Model (Opsional)"):
        col1, col2 = st.columns(2)
        with col1:
            n_estimators = st.slider(
                "🌳 Jumlah Trees (n_estimators)",
                50,
                500,
                200,
                step=50,
                help="Jumlah pohon keputusan dalam Random Forest",
            )
        with col2:
            test_size = st.slider(
                "📊 Proporsi Data Testing",
                0.1,
                0.4,
                0.2,
                step=0.05,
                help="Persentase data yang digunakan untuk testing",
            )

    # -----------------------------------------
    # Tombol Training
    # -----------------------------------------
    if st.button("🚀 Mulai Training Model", key="run_training"):
        with st.spinner("⏳ Sedang melatih model Random Forest..."):
            X = df_clean[st.session_state["features"]]
            y = df_clean[TARGET_COL]

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42, stratify=y
            )

            model = RandomForestClassifier(
                n_estimators=n_estimators,
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

        st.success("✅ Training model selesai!")
        st.rerun()

    # -------------------------------------------------
    # BLOK INI SELALU TAMPIL jika model sudah tersedia
    # -------------------------------------------------
    if st.session_state.get("rf_model") is not None:

        model = st.session_state["rf_model"]
        acc = st.session_state["acc"]
        cm = st.session_state["cm"]
        report = st.session_state["report"]
        X_cols = st.session_state["X_cols"]

        st.markdown("### 📊 Hasil Evaluasi Model")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("🎯 Akurasi", f"{acc*100:.2f}%")
        with c2:
            st.metric("🌳 Trees", f"{n_estimators}")
        with c3:
            st.metric("📊 Training", f"(otomatis)")
        with c4:
            st.metric("📊 Testing", f"(otomatis)")

        st.markdown("### 📊 Confusion Matrix")
        # Diubah label
        plot_confusion_matrix(cm, labels=["Tidak Hipertensi (0)", "Hipertensi (1)"]) 

        st.markdown("### 📈 Classification Report")
        report_df = pd.DataFrame(report).transpose()
        st.dataframe(report_df.style.background_gradient(cmap="Reds"), use_container_width=True)

        st.markdown("### 🎯 Feature Importance")
        plot_feature_importance(model, X_cols)

        # -----------------------------------------
        # TOMBOL LANJUT — selalu muncul
        # -----------------------------------------
        if st.button("➡️ Lanjut ke Visualisasi", key="goto_viz"):
            st.session_state["page"] = "Data Visualization"
            st.rerun()

        st.success("✅ Model sudah tersedia dan siap digunakan untuk prediksi.")