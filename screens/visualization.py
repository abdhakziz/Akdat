# pages/visualization.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def show_visualization():
    # Judul halaman
    st.markdown("<h1 style='text-align: center; color: #A67D45;'>Data Visualization</h1>", unsafe_allow_html=True)

    # Pastikan data sudah di-preprocess
    if st.session_state.get("clean_df") is None:
        st.warning("⚠️ Silakan lakukan preprocessing data terlebih dahulu di halaman **Preprocessing Data**.")
        if st.button("← Kembali ke Preprocessing"):
            st.session_state["page"] = "Preprocessing Data"
            st.rerun()
        return
    
    df = st.session_state["clean_df"]
    columns_list = df.columns.tolist()

    # -----------------------------------------
    # PILIH VISUALISASI
    # -----------------------------------------
    st.markdown("""
    <div style="background: #F0E9E1; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
        <div style="margin-bottom: 10px;">
            <span style="color: #A67D45; font-weight: 600;">Pilih Visualisasi</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Opsi visualisasi
    viz_options = [
        "Distribusi Data (Histogram)",
        "Korelasi Antar Fitur (Heatmap)",
        "Bar Chart - Perbandingan Kolom",
        "Scatter Plot - Hubungan 2 Variabel",
        "Box Plot - Distribusi per Kategori"
    ]
    
    selected_viz = st.selectbox(
        "Pilih jenis visualisasi",
        options=viz_options,
        key="viz_select",
        label_visibility="collapsed"
    )

    # -----------------------------------------
    # HASIL VISUALISASI
    # -----------------------------------------
    st.markdown("""
    <div style="background: #F0E9E1; border-radius: 12px; padding: 20px; margin-bottom: 20px; min-height: 300px;">
        <div style="margin-bottom: 10px;">
            <span style="color: #A67D45; font-weight: 600;">Hasil Visualisasi</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Render visualisasi berdasarkan pilihan
    if selected_viz == "Distribusi Data (Histogram)":
        # Pilih kolom untuk histogram
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            selected_col = st.selectbox("Pilih kolom untuk histogram:", numeric_cols, key="hist_col")
            
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.histplot(df[selected_col], bins=20, kde=True, ax=ax, color="#A67D45")
            ax.set_xlabel(selected_col, fontsize=12, fontweight="bold")
            ax.set_ylabel("Frekuensi", fontsize=12, fontweight="bold")
            ax.set_title(f"Distribusi {selected_col}", fontsize=14, fontweight="bold", pad=15)
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("ℹ️ Tidak ada kolom numerik untuk ditampilkan.")
    
    elif selected_viz == "Korelasi Antar Fitur (Heatmap)":
        fig, ax = plt.subplots(figsize=(12, 8))
        corr = df.corr()
        mask = np.triu(np.ones_like(corr, dtype=bool))
        sns.heatmap(
            corr,
            mask=mask,
            cmap="YlOrBr",
            ax=ax,
            annot=True if len(corr) <= 10 else False,
            fmt=".2f" if len(corr) <= 10 else None,
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": 0.8},
        )
        ax.set_title("Heatmap Korelasi Antar Fitur", fontsize=14, fontweight="bold", pad=20)
        plt.tight_layout()
        st.pyplot(fig)
    
    elif selected_viz == "Bar Chart - Perbandingan Kolom":
        selected_col = st.selectbox("Pilih kolom untuk bar chart:", columns_list, key="bar_col")
        
        fig, ax = plt.subplots(figsize=(10, 5))
        value_counts = df[selected_col].value_counts()
        colors = plt.cm.YlOrBr(np.linspace(0.4, 0.8, len(value_counts)))
        bars = ax.bar(value_counts.index.astype(str), value_counts.values, color=colors)
        ax.set_xlabel(selected_col, fontsize=12, fontweight="bold")
        ax.set_ylabel("Jumlah", fontsize=12, fontweight="bold")
        ax.set_title(f"Distribusi {selected_col}", fontsize=14, fontweight="bold", pad=15)
        
        # Tambahkan label di atas bar
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)
    
    elif selected_viz == "Scatter Plot - Hubungan 2 Variabel":
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                x_col = st.selectbox("Pilih variabel X:", numeric_cols, key="scatter_x")
            with col2:
                y_col = st.selectbox("Pilih variabel Y:", numeric_cols, index=1 if len(numeric_cols) > 1 else 0, key="scatter_y")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(df[x_col], df[y_col], alpha=0.6, color="#A67D45", edgecolors='white', linewidth=0.5)
            ax.set_xlabel(x_col, fontsize=12, fontweight="bold")
            ax.set_ylabel(y_col, fontsize=12, fontweight="bold")
            ax.set_title(f"Scatter Plot: {x_col} vs {y_col}", fontsize=14, fontweight="bold", pad=15)
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("ℹ️ Minimal 2 kolom numerik diperlukan untuk scatter plot.")
    
    elif selected_viz == "Box Plot - Distribusi per Kategori":
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            selected_col = st.selectbox("Pilih kolom numerik:", numeric_cols, key="box_col")
            
            fig, ax = plt.subplots(figsize=(10, 5))
            box = ax.boxplot(df[selected_col].dropna(), patch_artist=True)
            box['boxes'][0].set_facecolor('#A67D45')
            ax.set_ylabel(selected_col, fontsize=12, fontweight="bold")
            ax.set_title(f"Box Plot: {selected_col}", fontsize=14, fontweight="bold", pad=15)
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("ℹ️ Tidak ada kolom numerik untuk ditampilkan.")

    # -----------------------------------------
    # TOMBOL NAVIGASI: PREVIOUS & NEXT
    # -----------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    col_prev, col_spacer, col_next = st.columns([1, 2, 1])
    
    with col_prev:
        if st.button("← Previous", use_container_width=True, key="prev_btn"):
            st.session_state["page"] = "Analisis Data"
            st.rerun()
    
    with col_next:
        if st.button("Next →", use_container_width=True, key="next_btn"):
            st.session_state["page"] = "Prediction"
            st.rerun()