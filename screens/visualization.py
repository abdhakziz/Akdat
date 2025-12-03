# pages/visualization.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Import helper functions dan konstanta dari helpers.py
from helpers import (
    require_clean_data,           
    generate_pdf_visualizations,  
    plot_feature_importance,      
    TARGET_COL,                   # TARGET_COL = "hypertension"
)


def show_visualization():
    # Judul halaman utama
    st.title("📊 Visualisasi & Eksplorasi Data Hipertensi")

    require_clean_data()
    df = st.session_state["clean_df"]

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📈 Distribusi Data", "🔥 Korelasi Fitur", "🎯 Feature Importance", "💾 Export PDF"]
    )

    # ==========================================================
    # --- TAB 1: Distribusi Data & Proporsi Hipertensi ---
    # ==========================================================
    with tab1:
        st.markdown("### 📊 Distribusi Usia")

        fig1, ax1 = plt.subplots(figsize=(10, 5))
        sns.histplot(df["age"], bins=20, kde=True, ax=ax1, color="#A67D45") # Ganti warna
        ax1.set_xlabel("Usia (tahun)", fontsize=12, fontweight="bold")
        ax1.set_ylabel("Frekuensi", fontsize=12, fontweight="bold")
        ax1.set_title("Distribusi Usia Pasien", fontsize=14, fontweight="bold", pad=15)
        plt.tight_layout()
        st.pyplot(fig1)

        st.markdown("### 🏥 Proporsi Hipertensi") # Diubah

        col1, col2 = st.columns([2, 1])
        with col1:
            fig2, ax2 = plt.subplots(figsize=(8, 5))
            heart_counts = df[TARGET_COL].value_counts()
            colors = ["#899581", "#A67D45"] # Warna baru
            bars = ax2.bar(heart_counts.index, heart_counts.values, color=colors)
            ax2.set_xticks([0, 1])
            ax2.set_xticklabels(["Tidak (0)", "Ya (1)"], fontsize=11, fontweight="bold") # Diubah
            ax2.set_ylabel("Jumlah", fontsize=12, fontweight="bold")
            ax2.set_title(
                "Distribusi Label Hipertensi", fontsize=14, fontweight="bold", pad=15 # Diubah
            )

            for bar in bars:
                height = bar.get_height()
                ax2.text(
                    bar.get_x() + bar.get_width() / 2.0,  
                    height,                               
                    f"{int(height)}",                     
                    ha="center",
                    va="bottom",
                    fontsize=11,
                    fontweight="bold",
                )
            plt.tight_layout()
            st.pyplot(fig2)

        with col2:
            st.metric(
                "✅ Tidak Hipertensi", # Diubah
                f"{heart_counts.get(0, 0):,}",
                help="Jumlah kasus tanpa Hipertensi",
            )
            st.metric(
                "⚠️ Risiko Hipertensi", # Diubah
                f"{heart_counts.get(1, 0):,}",
                help="Jumlah kasus risiko Hipertensi",
            )
            ratio = (
                (heart_counts.get(1, 0) / heart_counts.get(0, 1)) * 100
                if heart_counts.get(0, 1) > 0
                else 0
            )
            st.metric("📊 Rasio", f"{ratio:.1f}%", help="Persentase kasus risiko Hipertensi")

    # =====================================
    # --- TAB 2: Heatmap Korelasi Fitur ---
    # =====================================
    with tab2:
        st.markdown("### 🔥 Heatmap Korelasi Fitur")

        fig3, ax3 = plt.subplots(figsize=(12, 10))
        corr = df.corr()
        mask = np.triu(np.ones_like(corr, dtype=bool))
        sns.heatmap(
            corr,
            mask=mask,
            cmap="Reds",
            ax=ax3,
            annot=False,
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": 0.8},
        )
        ax3.set_title("Heatmap Korelasi Antar Fitur", fontsize=14, fontweight="bold", pad=20)
        plt.tight_layout()
        st.pyplot(fig3)

        st.markdown("### 🔍 Top 10 Korelasi dengan Target")

        target_corr = (
            corr[TARGET_COL]                 
            .drop(TARGET_COL)                
            .abs()                           
            .sort_values(ascending=False)    
            .head(10)                        
        )

        fig_corr, ax_corr = plt.subplots(figsize=(10, 6))
        colors_corr = plt.cm.Reds(np.linspace(0.4, 0.8, len(target_corr)))
        ax_corr.barh(target_corr.index, target_corr.values, color=colors_corr)
        ax_corr.set_xlabel("Korelasi (Absolut)", fontsize=12, fontweight="bold")
        ax_corr.set_title(
            "Top 10 Fitur Berkorelasi dengan Hipertensi", # Diubah
            fontsize=14,
            fontweight="bold",
            pad=15,
        )
        plt.tight_layout()
        st.pyplot(fig_corr)

    # ========================================
    # --- TAB 4: Export Visualisasi PDF ---
    # =====================================
    with tab4:
        st.markdown("### 📥 Export Visualisasi ke PDF")
        st.info("💾 Unduh semua visualisasi dalam satu file PDF untuk dokumentasi atau presentasi.")

        if st.button("📄 Generate PDF", use_container_width=False):
            with st.spinner("⏳ Sedang membuat file PDF..."):
                buf = generate_pdf_visualizations(df, st.session_state.get("rf_model"))

            st.success("✅ File PDF berhasil dibuat!")
            st.download_button(
                label="📥 Unduh Visualisasi PDF",
                data=buf,
                file_name="visualisasi_hipertensi_indonesia.pdf", # Diubah
                mime="application/pdf",
                use_container_width=False,
            )