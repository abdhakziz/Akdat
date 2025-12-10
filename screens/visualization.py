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
    
    # Render visualisasi berdasarkan pilihan
    if selected_viz == "Distribusi Data (Histogram)":
        # Pilih kolom untuk histogram
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            selected_col = st.selectbox("Pilih kolom untuk histogram:", numeric_cols, key="hist_col")
            
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.histplot(df[selected_col], bins=20, kde=True, ax=ax, color="steelblue")
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
            cmap="coolwarm",
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
        
        fig, ax = plt.subplots(figsize=(10, 6))
        value_counts = df[selected_col].value_counts().sort_index()
        
        # Cek apakah kolom adalah binary (0/1)
        unique_vals = set(value_counts.index)
        is_binary = unique_vals.issubset({0, 1, 0.0, 1.0}) and len(unique_vals) == 2
        
        # Daftar kolom khusus
        gender_cols = ['gender', 'sex', 'male', 'female', 'jenis_kelamin', 'is_male', 'is_female']
        hypertension_cols = ['hypertension', 'hipertensi', 'target', 'diabetes', 'smoking', 'stroke', 'heart_disease']
        
        is_gender_col = selected_col.lower() in gender_cols and is_binary
        is_hypertension_col = selected_col.lower() in hypertension_cols or (is_binary and selected_col.lower() not in gender_cols)
        
        if is_gender_col:
            # Map 0/1 ke Perempuan/Laki-laki
            label_map = {0: 'Perempuan', 1: 'Laki-laki', 0.0: 'Perempuan', 1.0: 'Laki-laki'}
            labels = [label_map.get(x, str(x)) for x in value_counts.index]
            # Warna Pink untuk Perempuan, Biru untuk Laki-laki
            colors = ['#FF69B4', '#4169E1']
            title = f"Distribusi Jenis Kelamin"
            
            # Buat bar dengan label untuk legend
            for i, (label, val, color) in enumerate(zip(labels, value_counts.values, colors)):
                bar = ax.bar(label, val, color=color, edgecolor='white', linewidth=2, label=label)
                ax.text(i, val, f'{int(val):,}', ha='center', va='bottom', fontsize=14, fontweight='bold')
            
            ax.legend(title="Keterangan", loc='upper right', fontsize=11, title_fontsize=12)
            
        elif is_hypertension_col and is_binary:
            # Map 0/1 ke Tidak/Ya
            label_map = {0: 'Tidak', 1: 'Ya', 0.0: 'Tidak', 1.0: 'Ya'}
            labels = [label_map.get(x, str(x)) for x in value_counts.index]
            # Warna Biru tua untuk Tidak, Merah untuk Ya
            colors = ['#3498db', '#e74c3c']
            title = f"Distribusi Hipertensi (Ya/Tidak)" if selected_col.lower() in ['hypertension', 'hipertensi'] else f"Distribusi {selected_col}"
            
            # Buat bar dengan label untuk legend
            for i, (label, val, color) in enumerate(zip(labels, value_counts.values, colors)):
                bar = ax.bar(label, val, color=color, edgecolor='white', linewidth=2, label=label)
                ax.text(i, val, f'{int(val):,}', ha='center', va='bottom', fontsize=14, fontweight='bold')
            
            ax.legend(title="Keterangan", loc='upper right', fontsize=11, title_fontsize=12)
        else:
            labels = [str(x) for x in value_counts.index]
            colors = plt.cm.Blues(np.linspace(0.4, 0.8, len(value_counts)))
            bars = ax.bar(labels, value_counts.values, color=colors, edgecolor='white', linewidth=1)
            title = f"Distribusi {selected_col}"
            
            # Tambahkan jumlah di atas bar
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height, f'{int(height):,}',
                        ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        ax.set_xlabel(selected_col, fontsize=12, fontweight="bold")
        ax.set_ylabel("Jumlah", fontsize=12, fontweight="bold")
        ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
        
        plt.xticks(rotation=0)
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
            
            # Cek apakah Y column adalah gender-related (0/1 binary)
            y_data = df[y_col]
            y_unique = y_data.dropna().unique()
            gender_cols = ['gender', 'sex', 'male', 'female', 'jenis_kelamin', 'is_male', 'is_female']
            
            is_gender_col = y_col.lower() in gender_cols and len(y_unique) == 2 and set(y_unique).issubset({0, 1, 0.0, 1.0})
            
            if is_gender_col:
                # Map 0/1 ke Perempuan/Laki-laki
                y_mapped = y_data.map({0: 'Perempuan', 1: 'Laki-laki', 0.0: 'Perempuan', 1.0: 'Laki-laki'})
                
                # Buat scatter plot dengan categorical y-axis
                for i, (label, color) in enumerate([('Perempuan', '#FF69B4'), ('Laki-laki', '#4169E1')]):
                    mask = y_mapped == label
                    ax.scatter(df[x_col][mask], [i] * mask.sum(), alpha=0.6, color=color, edgecolors='white', linewidth=0.5, label=label)
                
                ax.set_yticks([0, 1])
                ax.set_yticklabels(['Perempuan', 'Laki-laki'])
                ax.legend()
            else:
                ax.scatter(df[x_col], df[y_col], alpha=0.6, color="steelblue", edgecolors='white', linewidth=0.5)
            
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
            box['boxes'][0].set_facecolor('steelblue')
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
            st.session_state["page"] = "Data Analysis"
            st.rerun()
    
    with col_next:
        if st.button("Next →", use_container_width=True, key="next_btn"):
            st.session_state["page"] = "Prediction"
            st.rerun()