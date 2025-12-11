# pages/visualization.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def show_visualization():
    # Judul halaman
    st.markdown("<h1 style='text-align: center; color: #A67D45;'>Data Visualization</h1>", unsafe_allow_html=True)

    # Pastikan sudah ada model (setelah analisis)
    if st.session_state.get("rf_model") is None:
        st.warning("⚠️ Silakan lakukan analisis data terlebih dahulu di halaman **Data Analysis**.")
        if st.button("← Kembali ke Data Analysis"):
            st.session_state["page"] = "Data Analysis"
            st.rerun()
        return
    
    # Ambil data dari session state
    df = st.session_state.get("clean_df")
    model = st.session_state.get("rf_model")
    acc = st.session_state.get("acc", 0)
    X_cols = st.session_state.get("X_cols", [])
    target_col = st.session_state.get("target_col", "target")
    
    # -----------------------------------------
    # RINGKASAN HASIL ANALISIS
    # -----------------------------------------
    st.markdown("""
    <div style="background: linear-gradient(135deg, #A67D45 0%, #8B6914 100%); border-radius: 12px; padding: 25px; margin-bottom: 25px; color: white;">
        <h3 style="color: white; margin-bottom: 15px; text-align: center;">📊 Ringkasan Hasil Analisis</h3>
        <p style="color: rgba(255,255,255,0.9); text-align: center; font-size: 0.95rem;">
            Visualisasi berikut menampilkan hasil analisis model Random Forest yang telah dilatih.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="background: #d4edda; border-radius: 12px; padding: 20px; text-align: center;">
            <div style="color: #155724; font-size: 0.9rem; font-weight: 600;">🎯 Akurasi Model</div>
            <div style="color: #155724; font-size: 2.2rem; font-weight: bold;">{acc*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background: #e8f4f8; border-radius: 12px; padding: 20px; text-align: center;">
            <div style="color: #0c5460; font-size: 0.9rem; font-weight: 600;">📋 Jumlah Fitur</div>
            <div style="color: #0c5460; font-size: 2.2rem; font-weight: bold;">{len(X_cols)}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style="background: #fff3cd; border-radius: 12px; padding: 20px; text-align: center;">
            <div style="color: #856404; font-size: 0.9rem; font-weight: 600;">📁 Total Data</div>
            <div style="color: #856404; font-size: 2.2rem; font-weight: bold;">{len(df):,}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------------------
    # PILIH JENIS VISUALISASI
    # -----------------------------------------
    st.markdown("""
    <div style="background: #F0E9E1; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
        <div style="margin-bottom: 10px;">
            <span style="color: #A67D45; font-weight: 600;">📈 Pilih Jenis Visualisasi</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    viz_options = ["Histogram - Sebaran Fitur", "Pie Chart - Distribusi Target"]
    
    selected_viz = st.radio(
        "Pilih jenis visualisasi:",
        options=viz_options,
        key="viz_select",
        horizontal=True,
        label_visibility="collapsed"
    )

    st.markdown("---")

    # -----------------------------------------
    # VISUALISASI: HISTOGRAM
    # -----------------------------------------
    if selected_viz == "Histogram - Sebaran Fitur":
        st.markdown("""
        <div style="background: #e8f4f8; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
            <h3 style="color: #0c5460; margin-bottom: 10px;">📊 Histogram - Sebaran Fitur yang Digunakan Model</h3>
            <p style="color: #0c5460; font-size: 0.95rem; margin: 0;">
                Visualisasi ini menunjukkan <b>bagaimana nilai-nilai tersebar</b> pada fitur yang digunakan untuk melatih model. 
                Anda dapat melihat distribusi nilai berdasarkan status target (berisiko atau tidak berisiko).
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Hanya tampilkan fitur numerik yang cocok untuk histogram (bukan binary/kategorikal)
        # Filter: harus numerik DAN memiliki lebih dari 5 nilai unik (bukan binary atau kategori sederhana)
        numeric_features = []
        for col in X_cols:
            if df[col].dtype in ['int64', 'float64']:
                unique_count = df[col].nunique()
                # Hanya tampilkan jika nilai unik lebih dari 5 (bukan binary atau kategorikal sederhana)
                if unique_count > 5:
                    numeric_features.append(col)
        
        if numeric_features:
            selected_feature = st.selectbox(
                "🔢 Pilih fitur yang ingin divisualisasikan:",
                options=numeric_features,
                key="hist_feature"
            )
            
            # Pisahkan data berdasarkan target
            if target_col in df.columns:
                df_risiko = df[df[target_col] == 1]
                df_tidak_risiko = df[df[target_col] == 0]
                
                fig, ax = plt.subplots(figsize=(12, 6))
                
                # Histogram untuk kedua kelompok
                ax.hist(df_tidak_risiko[selected_feature].dropna(), bins=20, alpha=0.7, 
                        label=f'Tidak Berisiko (n={len(df_tidak_risiko):,})', color='#3498db', edgecolor='white')
                ax.hist(df_risiko[selected_feature].dropna(), bins=20, alpha=0.7, 
                        label=f'Berisiko (n={len(df_risiko):,})', color='#e74c3c', edgecolor='white')
                
                # Garis rata-rata
                mean_tidak = df_tidak_risiko[selected_feature].mean()
                mean_risiko = df_risiko[selected_feature].mean()
                ax.axvline(mean_tidak, color='#2980b9', linestyle='--', linewidth=2, label=f'Rata-rata Tidak Berisiko: {mean_tidak:.1f}')
                ax.axvline(mean_risiko, color='#c0392b', linestyle='--', linewidth=2, label=f'Rata-rata Berisiko: {mean_risiko:.1f}')
                
                ax.set_xlabel(selected_feature, fontsize=12, fontweight='bold')
                ax.set_ylabel('Jumlah Pasien', fontsize=12, fontweight='bold')
                ax.set_title(f'Perbandingan Sebaran {selected_feature}\nBerdasarkan Status Risiko', fontsize=14, fontweight='bold')
                ax.legend(loc='upper right', fontsize=10)
                ax.grid(axis='y', alpha=0.3)
                plt.tight_layout()
                st.pyplot(fig)
                
                # Insight
                st.markdown("#### 💡 Insight")
                
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    st.markdown(f"""
                    <div style="background: #d6eaf8; border-radius: 10px; padding: 15px; border-left: 4px solid #3498db;">
                        <div style="font-weight: 600; color: #2471a3; margin-bottom: 8px;">🟦 Tidak Berisiko</div>
                        <div style="color: #1a5276;">
                            • Rata-rata: <b>{mean_tidak:.2f}</b><br>
                            • Median: <b>{df_tidak_risiko[selected_feature].median():.2f}</b><br>
                            • Min - Max: <b>{df_tidak_risiko[selected_feature].min():.1f} - {df_tidak_risiko[selected_feature].max():.1f}</b>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_s2:
                    st.markdown(f"""
                    <div style="background: #fadbd8; border-radius: 10px; padding: 15px; border-left: 4px solid #e74c3c;">
                        <div style="font-weight: 600; color: #922b21; margin-bottom: 8px;">🟥 Berisiko</div>
                        <div style="color: #78281f;">
                            • Rata-rata: <b>{mean_risiko:.2f}</b><br>
                            • Median: <b>{df_risiko[selected_feature].median():.2f}</b><br>
                            • Min - Max: <b>{df_risiko[selected_feature].min():.1f} - {df_risiko[selected_feature].max():.1f}</b>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Interpretasi perbedaan
                diff = mean_risiko - mean_tidak
                diff_pct = abs(diff / mean_tidak * 100) if mean_tidak != 0 else 0
                
                if diff > 0:
                    interpretation = f"Kelompok <b>Berisiko</b> cenderung memiliki nilai <b>{selected_feature}</b> yang lebih <b>tinggi</b> dibanding kelompok Tidak Berisiko (selisih {diff:.2f} atau {diff_pct:.1f}% lebih tinggi)."
                else:
                    interpretation = f"Kelompok <b>Berisiko</b> cenderung memiliki nilai <b>{selected_feature}</b> yang lebih <b>rendah</b> dibanding kelompok Tidak Berisiko (selisih {abs(diff):.2f} atau {diff_pct:.1f}% lebih rendah)."
                
                st.markdown(f"""
                <div style="background: #f8f9fa; border-radius: 10px; padding: 15px; margin-top: 15px; border-left: 4px solid #A67D45;">
                    <div style="font-weight: 600; color: #A67D45; margin-bottom: 8px;">📌 Interpretasi</div>
                    <div style="color: #333;">{interpretation}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Kolom target tidak ditemukan.")
        else:
            st.warning("⚠️ Tidak ada fitur numerik yang tersedia.")

    # -----------------------------------------
    # VISUALISASI: PIE CHART
    # -----------------------------------------
    elif selected_viz == "Pie Chart - Distribusi Target":
        st.markdown("""
        <div style="background: #e8f4f8; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
            <h3 style="color: #0c5460; margin-bottom: 10px;">🥧 Pie Chart - Distribusi Target (Berisiko vs Tidak Berisiko)</h3>
            <p style="color: #0c5460; font-size: 0.95rem; margin: 0;">
                Visualisasi ini menunjukkan <b>proporsi data</b> antara pasien yang berisiko dan tidak berisiko 
                berdasarkan hasil analisis.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if target_col in df.columns:
            value_counts = df[target_col].value_counts().sort_index()
            total = len(df)
            
            # Hitung jumlah dan persentase
            tidak_risiko = value_counts.get(0, 0) + value_counts.get(0.0, 0)
            risiko = value_counts.get(1, 0) + value_counts.get(1.0, 0)
            
            labels = ['Tidak Berisiko', 'Berisiko']
            sizes = [tidak_risiko, risiko]
            colors = ['#3498db', '#e74c3c']
            explode = (0.02, 0.05)  # Sedikit menonjolkan yang berisiko
            
            # Buat pie chart (ukuran lebih kecil agar muat satu layar)
            fig, ax = plt.subplots(figsize=(4, 3))
            
            wedges, texts, autotexts = ax.pie(
                sizes,
                labels=labels,
                autopct=lambda pct: f'{pct:.1f}%\n({int(pct/100*total):,} pasien)',
                colors=colors,
                startangle=90,
                explode=explode,
                shadow=True,
                textprops={'fontsize': 12, 'fontweight': 'bold'}
            )
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(11)
            
            ax.set_title('Proporsi Pasien Berdasarkan Status Risiko', fontsize=14, fontweight='bold', pad=20)
            plt.tight_layout()
            st.pyplot(fig)
            
            # Insight
            st.markdown("#### 💡 Insight")
            
            pct_risiko = risiko / total * 100
            pct_tidak = tidak_risiko / total * 100
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div style="background: #d6eaf8; border-radius: 12px; padding: 20px; text-align: center; border-left: 4px solid #3498db;">
                    <div style="font-weight: 600; color: #2471a3; font-size: 1rem;">✅ Tidak Berisiko</div>
                    <div style="color: #1a5276; font-size: 2rem; font-weight: bold; margin: 10px 0;">{tidak_risiko:,}</div>
                    <div style="color: #2471a3; font-size: 1.2rem;">({pct_tidak:.1f}%)</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="background: #fadbd8; border-radius: 12px; padding: 20px; text-align: center; border-left: 4px solid #e74c3c;">
                    <div style="font-weight: 600; color: #922b21; font-size: 1rem;">⚠️ Berisiko</div>
                    <div style="color: #78281f; font-size: 2rem; font-weight: bold; margin: 10px 0;">{risiko:,}</div>
                    <div style="color: #922b21; font-size: 1.2rem;">({pct_risiko:.1f}%)</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Interpretasi
            if pct_risiko > 50:
                balance_text = f"Data <b>tidak seimbang</b> dengan mayoritas pasien (<b>{pct_risiko:.1f}%</b>) masuk kategori <b>berisiko</b>."
                recommendation = "Perhatian: Proporsi pasien berisiko lebih banyak dari yang tidak berisiko."
            elif pct_risiko < 20:
                balance_text = f"Data <b>tidak seimbang</b> dengan hanya <b>{pct_risiko:.1f}%</b> pasien yang masuk kategori <b>berisiko</b>."
                recommendation = "Ini adalah kondisi yang diharapkan karena sebagian besar pasien tidak berisiko."
            else:
                balance_text = f"Data cukup <b>seimbang</b> dengan <b>{pct_risiko:.1f}%</b> pasien berisiko."
                recommendation = "Proporsi data cukup seimbang untuk analisis."
            
            st.markdown(f"""
            <div style="background: #f8f9fa; border-radius: 10px; padding: 15px; margin-top: 20px; border-left: 4px solid #A67D45;">
                <div style="font-weight: 600; color: #A67D45; margin-bottom: 8px;">📌 Interpretasi</div>
                <div style="color: #333;">
                    {balance_text}<br><br>
                    <b>Kesimpulan:</b> {recommendation}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Kolom target tidak ditemukan dalam data.")

    # -----------------------------------------
    # TOMBOL NAVIGASI
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