"""
REVA-ID — Regional Economic Vulnerability Analytic - Indonesia
Main Streamlit Application
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
import pandas as pd
import numpy as np

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="REVA-ID | Regional Economic Vulnerability Analytic",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Imports ───────────────────────────────────────────────────────────────────
from utils.theme import CUSTOM_CSS, hero_html, section_header, metric_card, placeholder_box, insight_box, cluster_badge
from utils.charts import (
    evi_bar_chart, evi_histogram, pca_scatter, variance_chart, loadings_heatmap,
    correlation_heatmap, elbow_chart, silhouette_chart, variable_dist, evi_bubble,
    forecast_chart, radar_chart,
)
from data.generate_data import get_sample_data

# ── Inject CSS ────────────────────────────────────────────────────────────────
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(uploaded=None):
    if uploaded is not None:
        try:
            if uploaded.name.endswith(".csv"):
                return pd.read_csv(uploaded)
            else:
                return pd.read_excel(uploaded)
        except Exception:
            st.error("Gagal membaca file. Gunakan dataset bawaan.")
    return get_sample_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1rem 0 0.5rem;text-align:center;">
        <p style="font-size:1.4rem;font-weight:800;color:#FFFFFF;margin:0;letter-spacing:0.06em;">REVA-ID</p>
        <p style="font-size:0.72rem;color:#64748B;margin:0;text-transform:uppercase;letter-spacing:0.1em;">
            Regional Economic Vulnerability Analytic
        </p>
    </div>
    <hr style="border-color:rgba(255,255,255,0.08);margin:0.8rem 0;"/>
    """, unsafe_allow_html=True)

    nav = st.radio(
        "NAVIGASI",
        [
            "Beranda",
            "Tentang Proyek",
            "Data & Variabel",
            "Preprocessing",
            "Analisis PCA",
            "Economic Vulnerability Index",
            "Clustering",
            "Peta Interaktif",
            "Forecasting",
            "Rekomendasi Kebijakan",
            "AI Insight",
        ],
        label_visibility="visible",
    )

    st.markdown("<hr style='border-color:rgba(255,255,255,0.08);margin:1rem 0 0.8rem'/>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.75rem;color:#475569;text-align:center;'>All rights reserved.</p>", unsafe_allow_html=True)

    # ── Dataset uploader in sidebar ──
    st.markdown("---")
    st.markdown("<p style='font-size:0.8rem;color:#94A3B8;font-weight:600;'>📂 DATASET</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload dataset (.csv / .xlsx)", type=["csv", "xlsx"], label_visibility="collapsed")

df = load_data(uploaded_file)

FEATURES = [
    "lama_sekolah","pengangguran","pengeluaran_per_kapita",
    "AHH","IPM","kemiskinan","akses_internet",
    "laju_pertumbuhan","kepadatan",
]
FEATURE_LABELS = {
    "lama_sekolah": "Rata-rata Lama Sekolah (Tahun)",
    "pengangguran": "Tingkat Pengangguran Terbuka (%)",
    "pengeluaran_per_kapita": "Pengeluaran per Kapita (Ribu Rp/Orang/Tahun)",
    "AHH": "Angka Harapan Hidup (Tahun)",
    "IPM": "Indeks Pembangunan Manusia",
    "kemiskinan": "Persentase Penduduk Miskin (%)",
    "akses_internet": "Akses Internet (% Perkotaan+Perdesaan)",
    "laju_pertumbuhan": "Laju Pertumbuhan Penduduk per Tahun (%)",
    "kepadatan": "Kepadatan Penduduk (Jiwa/km²)",
}

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: BERANDA
# ═══════════════════════════════════════════════════════════════════════════════
if nav == "Beranda":
    st.markdown(hero_html(
        badge="Platform Analitik Statistik Nasional · 2024",
        title="Pemetaan Kerentanan Ekonomi",
        title_accent="Regional Indonesia",
        subtitle=(
            "Platform analitik berbasis <b>Principal Component Analysis (PCA)</b>, "
            "<b>K-Means Clustering</b>, dan <b>Economic Vulnerability Index (EVI)</b> "
            "untuk memahami struktur kerentanan ekonomi 38 provinsi di Indonesia."
        ),
        quote=(
            "Ketahanan ekonomi daerah tidak hanya ditentukan oleh pertumbuhan ekonomi, "
            "tetapi juga oleh kemampuan wilayah menghadapi tekanan sosial-ekonomi "
            "dan ketidakpastian pembangunan."
        ),
    ), unsafe_allow_html=True)

    # Metric cards
    n_prov = df["Provinsi"].nunique()
    n_feat = len(FEATURES)
    n_clust = df["cluster"].nunique()
    avg_evi = df["EVI"].mean()

    st.markdown(f"""
    <div class="metric-grid">
        {{metric_card("Provinsi Dianalisis", n_prov)}
        {metric_card("Indikator Sosial-Ekonomi", n_feat)}
        {metric_card("Cluster / Kategori", n_clust)}
        {metric_card("Rata-rata Skor EVI Nasional", f"{avg_evi:.2f}")}
    </div>
    """, unsafe_allow_html=True)

    st.markdown(section_header("Distribusi Cluster Provinsi", "Gambaran cepat pengelompokan wilayah berdasarkan tingkat kerentanan ekonomi"), unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        st.plotly_chart(pca_scatter(df), use_container_width=True)
    with col2:
        # Cluster summary table
        summary = df.groupby("cluster_label").agg(
            Jumlah_Provinsi=("Provinsi","count"),
            Rata_EVI=("EVI","mean"),
            Rata_IPM=("IPM","mean"),
            Rata_Kemiskinan=("kemiskinan","mean"),
        ).round(2).reset_index()
        st.markdown("#### Profil Tiap Cluster")
        for _, row in summary.iterrows():
            badge = cluster_badge(row["cluster_label"])
            st.markdown(f"""
            <div class="info-card" style="margin-bottom:0.8rem;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem;">
                    <h4 style="margin:0;">{row['cluster_label']}</h4>
                    {badge}
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.4rem;font-size:0.85rem;color:#475569;">
                    <div>Provinsi: <strong>{int(row['Jumlah_Provinsi'])}</strong></div>
                    <div>EVI: <strong>{row['Rata_EVI']:.2f}</strong></div>
                    <div>IPM: <strong>{row['Rata_IPM']:.2f}</strong></div>
                    <div>Kemiskinan: <strong>{row['Rata_Kemiskinan']:.2f}%</strong></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(section_header("Skor EVI — Seluruh Provinsi", "Hover untuk detail indikator"), unsafe_allow_html=True)
    st.plotly_chart(evi_bubble(df), use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: TENTANG PROYEK
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "Tentang Proyek":
    st.markdown(hero_html(
        badge="Project Overview",
        title="Tentang",
        title_accent="REVA-ID",
        subtitle="Latar belakang, tujuan, dan kerangka metodologi platform analitik kerentanan ekonomi regional Indonesia.",
        quote="Disparitas ekonomi antar daerah di Indonesia bukan sekadar angka — ia adalah cerminan dari perbedaan struktur sosial, kualitas modal manusia, dan keterbatasan akses infrastruktur.",
    ), unsafe_allow_html=True)

    st.markdown(section_header("Latar Belakang", "Mengapa analisis kerentanan ekonomi regional penting?"), unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="info-card info-card-accent">
            <h4>🌏 Konteks Pembangunan</h4>
            <p>Indonesia sebagai negara kepulauan dengan 38 provinsi menghadapi tantangan
            disparitas ekonomi yang kompleks. Pertumbuhan ekonomi agregat tidak selalu
            mencerminkan kondisi riil tiap wilayah. Beberapa daerah dengan PDRB tinggi
            masih memiliki tingkat kemiskinan dan kerentanan yang signifikan.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="info-card info-card-accent">
            <h4>🧑‍🎓 Tujuan Analisis</h4>
            <p>Platform ini bertujuan memetakan secara komprehensif kerentanan ekonomi
            tiap provinsi menggunakan pendekatan multivariat — mengintegrasikan dimensi
            kesejahteraan, human capital, akses infrastruktur digital, dan tekanan
            demografis dalam satu indeks komposit berbasis data resmi BPS.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(section_header("Konsep Economic Vulnerability", "Definisi dan dimensi kerentanan ekonomi"), unsafe_allow_html=True)
    cols = st.columns(3)
    cards = [
        ("Dimensi Kesejahteraan", "Diukur melalui IPM, pengeluaran per kapita, dan persentase penduduk miskin. Menggambarkan kapasitas ekonomi dasar masyarakat."),
        ("Dimensi Human Capital", "Diukur melalui rata-rata lama sekolah dan angka harapan hidup. Mencerminkan kualitas SDM yang menopang produktivitas jangka panjang."),
        ("Dimensi Akses & Infrastruktur", "Diukur melalui tingkat akses internet. Mewakili konektivitas digital sebagai prasyarat ekonomi modern."),
        ("Dimensi Demografis", "Diukur melalui laju pertumbuhan penduduk dan kepadatan. Menggambarkan tekanan struktural terhadap kapasitas layanan publik."),
        ("Dimensi Pasar Tenaga Kerja", "Diukur melalui tingkat pengangguran terbuka. Mencerminkan ketidakseimbangan antara penawaran dan permintaan tenaga kerja."),
        ("Indeks Komposit (EVI)", "Mengintegrasikan seluruh dimensi melalui PCA menjadi satu skor tunggal yang memungkinkan komparasi antar wilayah secara objektif."),
    ]
    for i, (icon, title, desc) in enumerate(cards):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="info-card" style="margin-bottom:1rem;">
                <div style="font-size:1.8rem;margin-bottom:0.5rem;">{icon}</div>
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(section_header("Kerangka Metodologi", "Alur analisis dari raw data hingga rekomendasi kebijakan"), unsafe_allow_html=True)
    steps = ["Data Collection\n(BPS Official Statistics)", "Data Cleaning &\nPreprocessing", "Standardisasi\n(Z-Score)", "PCA\n(Reduksi Dimensi)", "EVI Construction\n(PC1-based Index)", "K-Means\nClustering (k=3)", "Policy\nRecommendation"]
    cols2 = st.columns(len(steps))
    for i, (col, step) in enumerate(zip(cols2, steps)):
        with col:
            st.markdown(f"""
            <div style="text-align:center;padding:0.8rem 0.5rem;">
                <div style="width:40px;height:40px;border-radius:50%;background:{'#0E7B6C' if i%2==0 else '#0B1F3A'};
                color:white;font-weight:700;font-size:1rem;display:flex;align-items:center;
                justify-content:center;margin:0 auto 0.6rem;">
                {i+1}
                </div>
                <p style="font-size:0.76rem;font-weight:600;color:#334155;margin:0;white-space:pre-line;line-height:1.4;">{step}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(section_header("Sumber Data", "Official statistics yang digunakan"), unsafe_allow_html=True)
    st.markdown("""
    <div class="info-card">
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;font-size:0.88rem;color:#475569;">
            <div><strong>📁 BPS — Indikator Pembangunan Manusia</strong><br>IPM, lama sekolah, AHH, pengeluaran per kapita</div>
            <div><strong>📁 BPS — Survei Angkatan Kerja Nasional</strong><br>Tingkat pengangguran terbuka (TPT)</div>
            <div><strong>📁 BPS — Data Kemiskinan Regional</strong><br>Persentase penduduk miskin & KPM</div>
            <div><strong>📁 BPS — Survei Sosial Ekonomi Nasional</strong><br>Akses internet perkotaan dan perdesaan</div>
            <div><strong>📁 BPS — Sensus & Proyeksi Penduduk</strong><br>Jumlah, laju pertumbuhan, kepadatan penduduk</div>
            <div><strong>📁 Kemensos — Data KPM PKH</strong><br>Jumlah Keluarga Penerima Manfaat</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: DATA & VARIABEL
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "Data & Variabel":
    st.markdown(section_header("Dataset Analisis", "38 provinsi · 9 indikator sosial-ekonomi"), unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["Tabel Data", "Deskripsi Variabel", "Distribusi", "Korelasi"])

    with tab1:
        display_cols = ["Provinsi","cluster_label"] + [c for c in FEATURES if c in df.columns]
        display_df = df[display_cols].copy()
        display_df["cluster_label"] = display_df["cluster_label"]
        st.dataframe(
            display_df.rename(columns={**FEATURE_LABELS, "cluster_label": "Kategori"}),
            use_container_width=True,
            height=520,
        )
        st.download_button(
            "⬇️ Unduh Dataset",
            data=display_df.to_csv(index=False),
            file_name="reva_id_dataset.csv",
            mime="text/csv",
        )

    with tab2:
        var_info = [
            ("lama_sekolah","Rata-rata Lama Sekolah","Tahun","Kesejahteraan / Human Capital","Positif → resilient","Rata-rata jumlah tahun pendidikan formal penduduk ≥15 tahun."),
            ("pengangguran","Tingkat Pengangguran Terbuka (TPT)","%","Ketenagakerjaan","Negatif → rentan","Persentase angkatan kerja yang tidak memiliki pekerjaan."),
            ("pengeluaran_per_kapita","Pengeluaran per Kapita","Ribu Rp/Orang/Tahun","Ekonomi","Positif → resilient","Ukuran kemampuan daya beli dan standar hidup masyarakat."),
            ("AHH","Angka Harapan Hidup","Tahun","Kesehatan","Positif → resilient","Perkiraan rata-rata tahun hidup penduduk sejak lahir."),
            ("IPM","Indeks Pembangunan Manusia","Skor 0–100","Komposit","Positif → resilient","Indeks komposit dimensi kesehatan, pendidikan, dan standar hidup."),
            ("kemiskinan","Persentase Penduduk Miskin","%","Kemiskinan","Negatif → rentan","Proporsi penduduk di bawah garis kemiskinan BPS."),
            ("akses_internet","Akses Internet","%","Infrastruktur Digital","Positif → resilient","Persentase rumah tangga dengan akses internet (perkotaan+perdesaan)."),
            ("laju_pertumbuhan","Laju Pertumbuhan Penduduk","%/tahun","Demografi","Konteks","Laju pertambahan penduduk per tahun hasil proyeksi BPS."),
            ("kepadatan","Kepadatan Penduduk","Jiwa/km²","Demografi","Konteks","Jumlah penduduk per satuan luas wilayah."),
        ]
        for var, label, unit, cat, arah, desc in var_info:
            with st.expander(f"**{label}** ({unit})"):
                c1, c2, c3 = st.columns(3)
                c1.metric("Kategori", cat)
                c2.metric("Arah EVI", arah)
                c3.metric("Rata-rata", f"{df[var].mean():.2f}")
                st.write(desc)

    with tab3:
        selected_var = st.selectbox("Pilih Variabel:", list(FEATURE_LABELS.keys()),
                                     format_func=lambda x: FEATURE_LABELS[x])
        st.plotly_chart(variable_dist(df, selected_var, FEATURE_LABELS[selected_var]),
                        use_container_width=True)

    with tab4:
        st.plotly_chart(correlation_heatmap(df, FEATURES), use_container_width=True)
        st.markdown(insight_box(
            "Korelasi positif kuat antara IPM, pengeluaran per kapita, dan akses internet menunjukkan "
            "bahwa ketiga indikator ini bergerak bersama membentuk dimensi kesejahteraan. "
            "Kemiskinan berkorelasi negatif dengan IPM (r ≈ -0.80) — konfirmasi validitas data."
        ), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: PREPROCESSING
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "Preprocessing":
    st.markdown(section_header("Preprocessing Data", "Validasi, cleaning, dan standardisasi sebelum analisis"), unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Validasi Data", "Standardisasi", "Kode Preprocessing"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Missing Values per Kolom**")
            mv = df.isnull().sum().reset_index()
            mv.columns = ["Kolom", "Missing"]
            mv["Status"] = mv["Missing"].apply(lambda x: "✅ Lengkap" if x == 0 else f"⚠️ {x} missing")
            st.dataframe(mv, use_container_width=True, hide_index=True)
        with col2:
            st.markdown("**Statistik Deskriptif**")
            st.dataframe(df[FEATURES].describe().round(2), use_container_width=True)

    with tab2:
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        Z = scaler.fit_transform(df[FEATURES])
        Z_df = pd.DataFrame(Z, columns=FEATURES)
        Z_df.insert(0, "Provinsi", df["Provinsi"].values)
        st.markdown("**Data Setelah Standardisasi Z-Score** (mean=0, std=1)")
        st.dataframe(Z_df.round(3), use_container_width=True, height=400)
        st.markdown(insight_box(
            "Standardisasi Z-Score memastikan semua variabel berada pada skala yang sama "
            "sehingga variabel dengan unit besar (seperti pengeluaran per kapita) tidak mendominasi "
            "hasil PCA dan clustering."
        ), unsafe_allow_html=True)

    with tab3:
        st.markdown("<h4 style='margin-bottom:0.5rem;'>Kode Preprocessing</h4>", unsafe_allow_html=True)
        st.code("""
# ── Contoh kode preprocessing data REVA-ID ──
import pandas as pd
from sklearn.preprocessing import StandardScaler

# 1. Load data mentah
df1 = pd.read_excel("data_ipm.xlsx")
df2 = pd.read_excel("data_internet.xlsx")
df3 = pd.read_excel("data_penduduk.xlsx")

# 2. Samakan format nama provinsi
for df_ in [df1, df2, df3]:
    df_['Provinsi'] = df_['Provinsi'].astype(str).str.upper().str.strip()

# 3. Fix format angka (koma → titik)
cols = ['AHH (tahun)', 'jumlah_penduduk', 'IPM', 'kemiskinan (%)']
for col in cols:
    df1[col] = pd.to_numeric(
        df1[col].astype(str).str.replace(',', '.'), errors='coerce'
    )

# 4. Merge data
df = df1.merge(df2, on='Provinsi', how='left')
df = df.merge(df3, on='Provinsi', how='left')

# 5. Handle missing value (isi dengan median)
df = df.fillna(df.median(numeric_only=True))

# 6. Standardisasi
scaler = StandardScaler()
features = ['lama_sekolah','pengangguran','pengeluaran_per_kapita',
            'AHH','IPM','kemiskinan','akses_internet',
            'laju_pertumbuhan','kepadatan']
Z = scaler.fit_transform(df[features])
        """, language="python")
        st.markdown(placeholder_box("TEMPAT MENEMPELKAN KODE PREPROCESSING ANDA"), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: PCA
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "Analisis PCA":
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA

    scaler = StandardScaler()
    Z = scaler.fit_transform(df[FEATURES])
    pca_full = PCA()
    pca_full.fit(Z)
    ev_ratio = pca_full.explained_variance_ratio_
    ev_cum = np.cumsum(ev_ratio)

    st.markdown(section_header("Principal Component Analysis", "Reduksi dimensi dan identifikasi struktur laten data"), unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["Variance Explained", "PCA Loadings", "Biplot", "Kode PCA"])

    with tab1:
        st.plotly_chart(variance_chart(ev_ratio, ev_cum), use_container_width=True)

        n_comp = int(np.argmax(ev_cum >= 0.70)) + 1
        col1, col2, col3 = st.columns(3)
        col1.metric("PC1 Variansi", f"{ev_ratio[0]*100:.2f}%")
        col2.metric("PC1+PC2 Kumulatif", f"{ev_cum[1]*100:.2f}%")
        col3.metric("Komponen ≥70%", f"{n_comp} komponen")

        st.markdown("""
        <div class="info-card" style="margin-top:1rem;">
            <h4>Interpretasi Komponen Utama</h4>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;font-size:0.88rem;color:#475569;margin-top:0.5rem;">
                <div>
                    <strong style="color:#0B1F3A;">PC1 — Kesejahteraan & Akses</strong><br>
                    Menangkap variasi terbesar (53.94%). Didominasi IPM, pengeluaran,
                    akses internet, dan lama sekolah. Semakin tinggi PC1 → semakin
                    maju dan resilien.
                </div>
                <div>
                    <strong style="color:#0B1F3A;">PC2 — Demografi & Tekanan Sosial</strong><br>
                    Menangkap 15.96% variansi. Didominasi laju pertumbuhan,
                    pengangguran, dan AHH. Menggambarkan tekanan demografis
                    dan dinamika pasar kerja.
                </div>
                <div>
                    <strong style="color:#0B1F3A;">PC3 — Kesehatan & Infrastruktur</strong><br>
                    Menangkap 11.23% variansi. Didominasi AHH dan kepadatan.
                    Mewakili kualitas kesehatan vs keterbatasan akses
                    infrastruktur.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        pca3 = PCA(n_components=3)
        pca3.fit(Z)
        loadings = pd.DataFrame(
            pca3.components_.T,
            columns=["PC1","PC2","PC3"],
            index=[FEATURE_LABELS[f] for f in FEATURES],
        )
        st.plotly_chart(loadings_heatmap(loadings), use_container_width=True)
        st.dataframe(loadings.round(4), use_container_width=True)
        st.markdown(insight_box(
            "Variabel dengan loading tinggi pada PC1 (IPM, pengeluaran, akses internet, lama sekolah) "
            "merupakan faktor pembentuk utama EVI. Loading negatif pada kemiskinan dan laju pertumbuhan "
            "mengkonfirmasi bahwa kedua variabel ini bergerak berlawanan arah dengan kesejahteraan."
        ), unsafe_allow_html=True)

    with tab3:
        st.plotly_chart(pca_scatter(df), use_container_width=True)
        st.markdown(insight_box(
            "Cluster Resilient (hijau) terkonsentrasi di kuadran kanan atas — nilai PC1 tinggi. "
            "Cluster Vulnerable (merah) terletak di kuadran kiri — indikasi keterbatasan multidimensi. "
            "Cluster Transitional (kuning) menyebar di tengah, mencerminkan heterogenitas wilayah."
        ), unsafe_allow_html=True)

    with tab4:
        st.code("""
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np

# Standardisasi
scaler = StandardScaler()
Z = scaler.fit_transform(X)

# PCA penuh
pca_full = PCA()
pca_full.fit(Z)

# Variance explained
ev_ratio = pca_full.explained_variance_ratio_
ev_cum = np.cumsum(ev_ratio)
n_comp = np.argmax(ev_cum >= 0.70) + 1
print(f"Komponen optimal: {n_comp}")

# PCA dengan n komponen terpilih
pca = PCA(n_components=n_comp)
Z_pca = pca.fit_transform(Z)

# Loadings
loadings = pd.DataFrame(
    pca.components_.T,
    columns=[f'PC{i+1}' for i in range(n_comp)],
    index=features
)
print(loadings)

# EVI = PC1 (skor kesejahteraan, inverse → rentan)
df['PC1'] = Z_pca[:, 0]
df['EVI'] = -df['PC1']
        """, language="python")
        st.markdown(placeholder_box("TEMPAT MENEMPELKAN KODE ANALISIS PCA ANDA"), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: EVI
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "Economic Vulnerability Index":
    st.markdown(section_header("Economic Vulnerability Index (EVI)", "Skor komposit kerentanan ekonomi berbasis PC1 — PCA"), unsafe_allow_html=True)

    # Formula
    st.markdown("""
    <div class="formula-box">
        EVI<sub>i</sub> = −(w₁·Z<sub>i1</sub> + w₂·Z<sub>i2</sub> + ··· + w<sub>p</sub>·Z<sub>ip</sub>)<br><br>
        Z<sub>ij</sub> = (X<sub>ij</sub> − μ<sub>j</sub>) / σ<sub>j</sub>   &nbsp;&nbsp;|&nbsp;&nbsp;
        w<sub>j</sub> = Loading PCA PC1   &nbsp;&nbsp;|&nbsp;&nbsp;
        EVI↑ → Lebih Rentan
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Tabel & Ranking", "Visualisasi", "Kode EVI"])

    with tab1:
        evi_df = df[["Provinsi","EVI","cluster_label","IPM","kemiskinan","akses_internet","pengeluaran_per_kapita"]].copy()
        evi_df = evi_df.sort_values("EVI", ascending=False).reset_index(drop=True)
        evi_df.index += 1

        # classify
        def classify(v):
            if v > 1.5: return "🔴 Vulnerable"
            elif v < -1.5: return "🟢 Resilient"
            else: return "🟡 Transitional"
        evi_df["Klasifikasi EVI"] = evi_df["EVI"].apply(classify)

        st.dataframe(
            evi_df.rename(columns={
                "EVI":"Skor EVI","cluster_label":"Cluster",
                "IPM":"IPM","kemiskinan":"Kemiskinan (%)","akses_internet":"Akses Internet (%)",
                "pengeluaran_per_kapita":"Pengeluaran/Kapita"
            }),
            use_container_width=True, height=480,
        )

    with tab2:
        col1, col2 = st.columns([3,2])
        with col1:
            st.plotly_chart(evi_bar_chart(df), use_container_width=True)
        with col2:
            st.plotly_chart(evi_histogram(df), use_container_width=True)
            top5_vuln = df.nlargest(5, "EVI")[["Provinsi","EVI"]].reset_index(drop=True)
            top5_resil = df.nsmallest(5, "EVI")[["Provinsi","EVI"]].reset_index(drop=True)
            st.markdown("**🔴 5 Provinsi Paling Rentan**")
            st.dataframe(top5_vuln.round(2), hide_index=True, use_container_width=True)
            st.markdown("**🟢 5 Provinsi Paling Resilien**")
            st.dataframe(top5_resil.round(2), hide_index=True, use_container_width=True)

        st.markdown(insight_box(
            "Rentang EVI yang lebar (~14 poin) mengindikasikan disparitas struktural yang signifikan. "
            "Provinsi di Papua Pegunungan dan Papua Tengah mencatat EVI tertinggi — dipengaruhi oleh "
            "kombinasi kemiskinan ekstrem, akses internet <10%, dan lama sekolah <7 tahun. "
            "Sebaliknya, DKI Jakarta, DI Yogyakarta, dan Bali mencatat EVI negatif (paling resilien)."
        ), unsafe_allow_html=True)

    with tab3:
        st.code("""
# Setelah PCA dijalankan:
# EVI = negatif PC1 (karena PC1 tinggi = makmur, EVI tinggi = rentan)
df['EVI'] = -df['PC1']

# Klasifikasi
def classify_evi(v):
    if v > 1.5:  return "Vulnerable"
    elif v < -1.5: return "Resilient"
    else: return "Transitional"

df['cluster_label'] = df['EVI'].apply(classify_evi)
df_sorted = df.sort_values('EVI', ascending=False)
print(df_sorted[['Provinsi','EVI','cluster_label']].to_string())
        """, language="python")
        st.markdown(placeholder_box("TEMPAT MENEMPELKAN KODE PERHITUNGAN EVI ANDA"), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: CLUSTERING
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "Clustering":
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score

    scaler = StandardScaler()
    Z = scaler.fit_transform(df[FEATURES])

    st.markdown(section_header("K-Means Clustering", "Segmentasi provinsi berdasarkan profil kerentanan ekonomi multidimensi"), unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["Penentuan k", "Profil Cluster", "Visualisasi", "Kode K-Means"])

    with tab1:
        @st.cache_data
        def compute_elbow_silhouette(Z_arr):
            Z_arr = np.array(Z_arr)
            inertias, sil = [], []
            for k in range(1, 10):
                km = KMeans(n_clusters=k, random_state=42, n_init=10)
                km.fit(Z_arr)
                inertias.append(km.inertia_)
                if k >= 2:
                    labels = km.labels_
                    sil.append(silhouette_score(Z_arr, labels))
            return inertias, sil

        inertias, sil_scores = compute_elbow_silhouette(Z.tolist())

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(elbow_chart(inertias, range(1,10)), use_container_width=True)
            st.markdown(insight_box("Titik siku (elbow) terlihat jelas pada k=3, menandakan penurunan inertia mulai melandai setelah titik ini."), unsafe_allow_html=True)
        with col2:
            st.plotly_chart(silhouette_chart(sil_scores, range(2,10)), use_container_width=True)
            st.markdown(insight_box("Silhouette score tertinggi di k=2 (0.573), namun k=3 dipilih karena lebih informatif untuk segmentasi kebijakan."), unsafe_allow_html=True)

    with tab2:
        profile = df.groupby("cluster_label")[FEATURES].mean().round(2)
        st.dataframe(profile.rename(columns=FEATURE_LABELS), use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        cols3 = st.columns(3)
        cluster_info = [
            ("Resilient","🟢","#D1FAE5","#065F46",
             "DKI Jakarta, DI Yogyakarta, Bali",
             "IPM tinggi · Akses internet luas · Kemiskinan rendah · Ekonomi terdiversifikasi",
             "Wilayah dengan struktur ekonomi kompleks dan adaptif. Paling tahan terhadap shock ekonomi."),
            ("Transitional","🟡","#FFFBEB","#92400E",
             "30 provinsi (mayoritas Sumatra, Jawa non-core, Kalimantan, Sulawesi, Maluku)",
             "Indikator moderat · Sedang transformasi · Belum fully industrialized",
             "Berada di titik kritis — dapat naik menjadi resilient atau turun menjadi vulnerable tergantung kebijakan."),
            ("Vulnerable","🔴","#FFF1F2","#991B1B",
             "NTT, Papua Barat, Papua Selatan, Papua Tengah, Papua Pegunungan",
             "IPM rendah · Kemiskinan sangat tinggi · Akses internet terbatas · Human capital rendah",
             "Paling rentan terhadap krisis. Ketergantungan sektor primer, shock kecil dapat berdampak besar."),
        ]
        for col, (label, emoji, bg, txt, provs, chars, interp) in zip(cols3, cluster_info):
            with col:
                st.markdown(f"""
                <div class="info-card" style="background:{bg};border-color:{txt}30;">
                    <div style="font-size:1.5rem;margin-bottom:0.4rem;">{emoji}</div>
                    <h4 style="color:{txt};">{label}</h4>
                    <p style="color:{txt};font-size:0.8rem;font-weight:600;margin-bottom:0.5rem;">{provs}</p>
                    <p style="font-size:0.8rem;"><strong>Karakteristik:</strong><br>{chars}</p>
                    <p style="font-size:0.82rem;color:#374151;margin-top:0.5rem;">{interp}</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>**Anggota Cluster:**", unsafe_allow_html=True)
        for label in ["Resilient","Transitional","Vulnerable"]:
            with st.expander(f"{label} ({len(df[df['cluster_label']==label])} provinsi)"):
                provs = df[df["cluster_label"]==label]["Provinsi"].tolist()
                st.write(", ".join(provs))

    with tab3:
        st.plotly_chart(pca_scatter(df), use_container_width=True)

    with tab4:
        st.code("""
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Elbow
inertia = []
for k in range(1, 10):
    km = KMeans(n_clusters=k, random_state=42)
    km.fit(Z)
    inertia.append(km.inertia_)

# Silhouette
sil = [silhouette_score(Z, KMeans(n_clusters=k, random_state=42).fit_predict(Z))
       for k in range(2, 10)]

# Final clustering k=3
kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(Z)

# Map cluster index to label (perlu disesuaikan)
cluster_map = {0:"Resilient", 1:"Vulnerable", 2:"Transitional"}
df['cluster_label'] = df['cluster'].map(cluster_map)
        """, language="python")
        st.markdown(placeholder_box("TEMPAT MENEMPELKAN KODE K-MEANS CLUSTERING ANDA"), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: PETA INTERAKTIF
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "Peta Interaktif":
    st.markdown(section_header("Peta Kerentanan Ekonomi Regional", "Visualisasi spasial EVI dan kategori cluster per provinsi"), unsafe_allow_html=True)

    import plotly.express as px

    filter_cluster = st.multiselect(
        "Filter berdasarkan Cluster:",
        ["Resilient","Transitional","Vulnerable"],
        default=["Resilient","Transitional","Vulnerable"],
    )
    df_map = df[df["cluster_label"].isin(filter_cluster)].copy()

    # Approximate lat/lon for each province
    coords = {
        "ACEH":(4.6951,96.7494),"SUMATERA UTARA":(2.1154,99.5451),"SUMATERA BARAT":(-0.7399,100.8000),
        "RIAU":(0.2933,101.7068),"JAMBI":(-1.4852,102.4381),"SUMATERA SELATAN":(-3.3194,104.9144),
        "BENGKULU":(-3.7928,102.2601),"LAMPUNG":(-4.5586,105.4068),"KEP. BANGKA BELITUNG":(-2.7411,106.4406),
        "KEP. RIAU":(3.9457,108.1428),"DKI JAKARTA":(-6.2088,106.8456),"JAWA BARAT":(-6.9175,107.6191),
        "JAWA TENGAH":(-7.1500,110.1403),"DI YOGYAKARTA":(-7.8754,110.4262),"JAWA TIMUR":(-7.5360,112.2384),
        "BANTEN":(-6.4058,106.0640),"BALI":(-8.4095,115.1889),"NUSA TENGGARA BARAT":(-8.6529,117.3616),
        "NUSA TENGGARA TIMUR":(-8.6574,121.0794),"KALIMANTAN BARAT":(0.0000,110.0000),
        "KALIMANTAN TENGAH":(-1.6814,113.3823),"KALIMANTAN SELATAN":(-3.0926,115.2838),
        "KALIMANTAN TIMUR":(1.6407,116.4194),"KALIMANTAN UTARA":(3.0731,116.0414),
        "SULAWESI UTARA":(0.6270,123.9750),"SULAWESI TENGAH":(-1.4300,121.4456),
        "SULAWESI SELATAN":(-3.6688,119.9741),"SULAWESI TENGGARA":(-4.1449,122.1746),
        "GORONTALO":(0.6999,122.4467),"SULAWESI BARAT":(-2.8441,119.2321),
        "MALUKU":(-3.2385,130.1453),"MALUKU UTARA":(1.5710,127.8087),
        "PAPUA BARAT DAYA":(-1.3361,133.1747),"PAPUA BARAT":(-1.3361,133.1747),
        "PAPUA":(-4.2699,138.0804),"PAPUA SELATAN":(-6.5000,140.0000),
        "PAPUA TENGAH":(-4.0000,136.5000),"PAPUA PEGUNUNGAN":(-4.5000,139.5000),
    }
    df_map["lat"] = df_map["Provinsi"].map(lambda x: coords.get(x, (0,118))[0])
    df_map["lon"] = df_map["Provinsi"].map(lambda x: coords.get(x, (0,118))[1])

    CLUSTER_COLORS_MAP = {"Resilient":"#1A7F4B","Transitional":"#D4850A","Vulnerable":"#C0392B"}

    fig_map = px.scatter_mapbox(
        df_map,
        lat="lat", lon="lon",
        color="cluster_label",
        color_discrete_map=CLUSTER_COLORS_MAP,
        size=df_map["EVI"].abs() + 3,
        size_max=35,
        hover_name="Provinsi",
        hover_data={
            "EVI": ":.2f",
            "IPM": ":.2f",
            "kemiskinan": ":.2f",
            "akses_internet": ":.2f",
            "lat": False, "lon": False,
        },
        zoom=3.8,
        center={"lat": -2.5, "lon": 118},
        mapbox_style="carto-positron",
        title="Peta Kerentanan Ekonomi Regional Indonesia",
        labels={"cluster_label": "Kategori"},
    )
    fig_map.update_layout(
        height=580,
        margin=dict(t=50, b=10, l=10, r=10),
        legend=dict(orientation="h", y=0.02, x=0.02),
        font=dict(family="Plus Jakarta Sans, sans-serif"),
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # Legend
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="rec-card rec-resilient">
            <strong>🟢 Resilient</strong><br>
            <small>DKI Jakarta · DI Yogyakarta · Bali</small><br>
            <small>EVI &lt; −1.5 · IPM &gt; 80</small>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="rec-card rec-transitional">
            <strong>🟡 Transitional</strong><br>
            <small>30 Provinsi (Mayoritas)</small><br>
            <small>−1.5 ≤ EVI ≤ 1.5</small>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="rec-card rec-vulnerable">
            <strong>🔴 Vulnerable</strong><br>
            <small>NTT · Papua Tengah · Papua Pegunungan · dll</small><br>
            <small>EVI &gt; 1.5 · Kemiskinan &gt; 17%</small>
        </div>""", unsafe_allow_html=True)

    st.markdown(insight_box(
        "Peta menunjukkan pola spasial yang jelas: wilayah Jawa-Bali cenderung resilien, "
        "sementara Papua bagian tengah dan pegunungan merupakan zona paling rentan. "
        "Ukuran gelembung mencerminkan magnitude EVI absolut."
    ), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: FORECASTING
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "Forecasting":
    st.markdown(section_header("Forecasting EVI", "Proyeksi kerentanan ekonomi berbasis tren historis"), unsafe_allow_html=True)
    st.markdown("""<div class="info-card" style="margin-bottom:1.5rem;">
        <h4>ℹ️ Catatan Metodologis</h4>
        <p>Halaman ini menyediakan simulasi forecasting EVI menggunakan pendekatan
        <strong>Exponential Smoothing (ETS)</strong> dan <strong>Linear Trend</strong>.
        Data historis EVI disimulasikan berdasarkan tren indikator BPS 2019–2024.
        Untuk forecasting aktual, tempelkan kode ARIMA/ETS Anda di placeholder yang tersedia.</p>
    </div>""", unsafe_allow_html=True)

    prov_sel = st.selectbox("Pilih Provinsi:", df["Provinsi"].sort_values().tolist())
    row = df[df["Provinsi"] == prov_sel].iloc[0]
    base_evi = row["EVI"]
    trend = 0.05 if row["cluster_label"] == "Vulnerable" else (-0.12 if row["cluster_label"] == "Resilient" else -0.04)

    np.random.seed(42)
    years_hist = list(range(2019, 2025))
    hist_vals = [base_evi + trend * (y - 2024) + np.random.normal(0, 0.15) for y in years_hist]
    years_fc = list(range(2025, 2029))
    fc_vals = [base_evi + trend * (y - 2024) for y in years_fc]

    st.plotly_chart(forecast_chart(years_hist, hist_vals, years_fc, fc_vals, prov_sel), use_container_width=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("EVI 2024", f"{base_evi:.2f}")
    col2.metric("Prediksi EVI 2028", f"{fc_vals[-1]:.2f}", delta=f"{fc_vals[-1]-base_evi:.2f}")
    col3.metric("Tren", "Memburuk ↑" if trend > 0 else "Membaik ↓", delta_color="inverse" if trend > 0 else "normal")

    st.markdown(insight_box(
        f"Proyeksi menunjukkan {prov_sel} akan mengalami tren EVI yang "
        f"{'meningkat (semakin rentan)' if trend > 0 else 'menurun (semakin resilien)'} "
        f"hingga 2028 jika kondisi struktural tidak berubah secara signifikan."
    ), unsafe_allow_html=True)

    st.markdown("<br>**Kode Forecasting:**", unsafe_allow_html=True)
    st.code("""
# Contoh forecasting EVI dengan Exponential Smoothing
from statsmodels.tsa.holtwinters import ExponentialSmoothing

evi_series = df_ts[df_ts['Provinsi'] == provinsi]['EVI'].values
model = ExponentialSmoothing(evi_series, trend='add', seasonal=None)
fit = model.fit()
forecast = fit.forecast(4)  # 4 tahun ke depan
print(forecast)

# Atau dengan ARIMA
from statsmodels.tsa.arima.model import ARIMA
model = ARIMA(evi_series, order=(1,1,0))
result = model.fit()
pred = result.forecast(steps=4)
    """, language="python")
    st.markdown(placeholder_box("TEMPAT MENEMPELKAN KODE FORECASTING ANDA"), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: REKOMENDASI KEBIJAKAN
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "Rekomendasi Kebijakan":
    st.markdown(section_header("Rekomendasi Kebijakan", "Implikasi analisis untuk perencanaan pembangunan regional"), unsafe_allow_html=True)

    recs = {
        "Vulnerable": {
            "icon": "🔴",
            "title": "Vulnerable Economy Region",
            "subtitle": "NTT, Papua Pegunungan, Papua Tengah, Papua Selatan, Papua Barat",
            "color": "rec-vulnerable",
            "items": [
                ("🏫 Penguatan Human Capital", "Percepatan program Kartu Indonesia Pintar (KIP) dan peningkatan infrastruktur pendidikan dasar dan menengah di wilayah terpencil."),
                ("🌐 Digitalisasi Infrastruktur", "Prioritas pembangunan BTS dan jaringan fiber optik melalui program Palapa Ring untuk meningkatkan akses internet perdesaan."),
                ("💰 Perlindungan Sosial Adaptif", "Peningkatan cakupan Program Keluarga Harapan (PKH) dan penyesuaian besaran bantuan berbasis CPI lokal."),
                ("🏗️ Konektivitas & Logistik", "Percepatan pembangunan infrastruktur transportasi (jalan, pelabuhan) untuk mengurangi biaya logistik dan membuka akses pasar."),
                ("🌾 Diversifikasi Ekonomi Lokal", "Pengembangan agribisnis berbasis komoditas unggulan lokal dengan pendampingan offtaker dan akses pembiayaan UMKM."),
            ]
        },
        "Transitional": {
            "icon": "🟡",
            "title": "Transitional Economy Region",
            "subtitle": "30 Provinsi — Sumatra, Jawa non-core, Kalimantan, Sulawesi, Maluku",
            "color": "rec-transitional",
            "items": [
                ("💡 Akselerasi Digitalisasi UMKM", "Program pendampingan adopsi platform digital dan e-commerce untuk UMKM, didukung pelatihan literasi digital."),
                ("🏭 Penguatan Industri Manufaktur", "Insentif fiskal untuk investasi industri padat karya sebagai strategi penyerapan tenaga kerja dan reduksi TPT."),
                ("📊 Peningkatan Kualitas Layanan Publik", "Reformasi tata kelola dan peningkatan efisiensi belanja daerah untuk memperkuat layanan dasar (kesehatan, pendidikan)."),
                ("🤝 Kemitraan Pemerintah-Swasta", "Pengembangan skema PPP untuk pembiayaan infrastruktur dan kawasan industri strategis."),
                ("📈 Penguatan Sistem Perlindungan Sosial", "Integrasi data DTKS untuk memastikan akurasi targeting bantuan sosial bagi kelompok rentan."),
            ]
        },
        "Resilient": {
            "icon": "🟢",
            "title": "Resilient Economy Region",
            "subtitle": "DKI Jakarta, DI Yogyakarta, Bali",
            "color": "rec-resilient",
            "items": [
                ("🚀 Inovasi Ekonomi Digital", "Pengembangan ekosistem startup, fintech, dan ekonomi digital berbasis riset dan inovasi sebagai engine pertumbuhan baru."),
                ("🧪 Penguatan R&D & Perguruan Tinggi", "Kolaborasi triple helix (pemerintah-industri-universitas) untuk mendorong inovasi dan produktivitas."),
                ("🌍 Integrasi Ekonomi Global", "Fasilitasi akses ke rantai pasok global dan perjanjian perdagangan bilateral/multilateral."),
                ("♻️ Ekonomi Berkelanjutan", "Transisi menuju ekonomi rendah karbon dan pengembangan green economy sebagai competitive advantage jangka panjang."),
                ("🔗 Spill-over ke Daerah Sekitar", "Program transmisi pengetahuan dan investasi ke daerah penyangga untuk mengurangi disparitas inter-regional."),
            ]
        }
    }

    for cat, info in recs.items():
        st.markdown(f"""
        <div class="rec-card {info['color']}" style="margin-bottom:1.5rem;">
            <div style="display:flex;align-items:center;gap:0.8rem;margin-bottom:1rem;">
                <span style="font-size:2rem;">{info['icon']}</span>
                <div>
                    <h3 style="margin:0;font-size:1.2rem;">{info['title']}</h3>
                    <p style="margin:0;font-size:0.82rem;opacity:0.8;">{info['subtitle']}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        with st.expander(f"Lihat {len(info['items'])} Rekomendasi Kebijakan →"):
            for title, desc in info["items"]:
                st.markdown(f"**{title}**")
                st.write(desc)
                st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: AI INSIGHT
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "AI Insight":
    st.markdown(section_header("Smart Province Insight", "Analisis otomatis berbasis profil data tiap provinsi"), unsafe_allow_html=True)
    st.markdown("""<div class="info-card" style="margin-bottom:1rem;">
        <p style="margin:0;font-size:0.88rem;color:#475569;">
        Pilih provinsi untuk mendapatkan profil analitik lengkap — generated secara otomatis
        dari data BPS berbasis rule-based insight engine.
        </p>
    </div>""", unsafe_allow_html=True)

    prov_sel = st.selectbox("Pilih Provinsi:", df["Provinsi"].sort_values().tolist(), key="ai_prov")
    row = df[df["Provinsi"] == prov_sel].iloc[0]

    col1, col2 = st.columns([2, 3])
    with col1:
        badge = cluster_badge(row["cluster_label"])
        st.markdown(f"""
        <div class="info-card info-card-accent">
            <h3 style="margin:0 0 0.4rem;">{prov_sel.title()}</h3>
            {badge}
            <hr style="border-color:#EEF2F7;margin:0.8rem 0;"/>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;font-size:0.85rem;">
                <div><span style="color:#94A3B8;">EVI Score</span><br><strong>{row['EVI']:.2f}</strong></div>
                <div><span style="color:#94A3B8;">IPM</span><br><strong>{row['IPM']:.2f}</strong></div>
                <div><span style="color:#94A3B8;">Kemiskinan</span><br><strong>{row['kemiskinan']:.2f}%</strong></div>
                <div><span style="color:#94A3B8;">Akses Internet</span><br><strong>{row['akses_internet']:.2f}%</strong></div>
                <div><span style="color:#94A3B8;">Lama Sekolah</span><br><strong>{row['lama_sekolah']:.2f} thn</strong></div>
                <div><span style="color:#94A3B8;">Pengangguran</span><br><strong>{row['pengangguran']:.2f}%</strong></div>
                <div><span style="color:#94A3B8;">AHH</span><br><strong>{row['AHH']:.2f} thn</strong></div>
                <div><span style="color:#94A3B8;">Pengeluaran/Kapita</span><br><strong>Rp{row['pengeluaran_per_kapita']:,}</strong></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Radar chart — normalize to 0–10
        nat_max = df[FEATURES].max()
        nat_min = df[FEATURES].min()
        def norm(v, col, invert=False):
            mn, mx = nat_min[col], nat_max[col]
            n = (v - mn) / (mx - mn + 1e-9) * 10
            return 10 - n if invert else n

        radar_vals = [
            norm(row["lama_sekolah"], "lama_sekolah"),
            norm(row["IPM"], "IPM"),
            norm(row["pengeluaran_per_kapita"], "pengeluaran_per_kapita"),
            norm(row["AHH"], "AHH"),
            norm(row["akses_internet"], "akses_internet"),
            norm(row["kemiskinan"], "kemiskinan", invert=True),
            norm(row["pengangguran"], "pengangguran", invert=True),
        ]
        radar_cats = ["Lama Sekolah","IPM","Pengeluaran","AHH","Internet","Anti-Kemiskinan","Anti-Pengangguran"]
        st.plotly_chart(radar_chart(prov_sel.title(), radar_vals, radar_cats), use_container_width=True)

    # Auto-generated insight
    def gen_insight(row):
        label = row["cluster_label"]
        prov = row["Provinsi"].title()
        lines = []
        if label == "Vulnerable":
            lines.append(f"**{prov}** termasuk dalam kategori <span class='badge-vulnerable'>Vulnerable</span> dengan skor EVI **{row['EVI']:.2f}**.")
            if row["kemiskinan"] > 20:
                lines.append(f"Tingkat kemiskinan yang sangat tinggi (**{row['kemiskinan']:.1f}%**) menjadi faktor dominan kerentanan ekonomi wilayah ini.")
            if row["akses_internet"] < 40:
                lines.append(f"Akses internet yang terbatas (**{row['akses_internet']:.1f}%**) menghambat konektivitas digital dan akses terhadap layanan ekonomi modern.")
            if row["lama_sekolah"] < 8:
                lines.append(f"Rata-rata lama sekolah **{row['lama_sekolah']:.1f} tahun** mengindikasikan keterbatasan human capital jangka panjang.")
            lines.append("**Rekomendasi:** Prioritas penguatan perlindungan sosial, infrastruktur digital, dan akselerasi pendidikan dasar.")
        elif label == "Resilient":
            lines.append(f"**{prov}** termasuk dalam kategori <span class='badge-resilient'>Resilient</span> dengan skor EVI **{row['EVI']:.2f}**.")
            lines.append(f"IPM tinggi (**{row['IPM']:.2f}**) dan akses internet luas (**{row['akses_internet']:.1f}%**) menjadi fondasi ketahanan ekonomi.")
            lines.append("**Rekomendasi:** Fokus pada inovasi ekonomi digital, R&D, dan peran sebagai katalisator pembangunan regional.")
        else:
            lines.append(f"**{prov}** termasuk dalam kategori <span class='badge-transitional'>Transitional</span> dengan skor EVI **{row['EVI']:.2f}**.")
            if row["pengangguran"] > 6:
                lines.append(f"Tingkat pengangguran **{row['pengangguran']:.1f}%** menunjukkan tekanan pasar kerja yang perlu perhatian.")
            lines.append(f"Dengan IPM **{row['IPM']:.2f}** dan akses internet **{row['akses_internet']:.1f}%**, wilayah ini berada dalam fase transisi yang kritis.")
            lines.append("**Rekomendasi:** Penguatan digitalisasi UMKM, investasi industri padat karya, dan peningkatan kualitas layanan publik.")
        return " ".join(lines)

    st.markdown(f"""
    <div class="insight-box" style="margin-top:1rem;">
        <p style="font-size:0.95rem;line-height:1.75;">
        🤖 <strong>Auto-Generated Insight:</strong><br><br>
        {gen_insight(row).replace("**", "<strong>").replace("**", "</strong>")}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Comparison
    st.markdown(section_header("Perbandingan dengan Rata-rata Nasional", ""), unsafe_allow_html=True)
    nat_avg = df[FEATURES].mean()
    compare = pd.DataFrame({
        "Indikator": [FEATURE_LABELS[f] for f in FEATURES],
        prov_sel.title(): [row[f] for f in FEATURES],
        "Rata-rata Nasional": [nat_avg[f] for f in FEATURES],
    })
    compare = compare.set_index("Indikator")
    compare["Selisih"] = (compare[prov_sel.title()] - compare["Rata-rata Nasional"]).round(2)
    st.dataframe(compare.round(2), use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="margin-top:4rem;padding:1.5rem 2rem;background:#0B1F3A;border-radius:16px;
            display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;">
    <div>
        <p style="font-size:1rem;font-weight:800;color:#FFFFFF;margin:0;">REVA-ID</p>
        <p style="font-size:0.75rem;color:#64748B;margin:0;">Regional Economic Vulnerability Analytic · Indonesia</p>
    </div>
    <div style="font-size:0.78rem;color:#475569;text-align:center;">
        © 2026 Sahda Huwaidah Estiningtyas. <br>
        All Rights Reserved.
    </div>
    <div style="font-size:0.78rem;color:#475569;text-align:right;">
        Integrasi Principal Component Analysis dan K-Means Clustering<br>
        Pemetaan Kerentanan Ekonomi Regional Indonesia yang Berkelanjutan
    </div>
</div>
""", unsafe_allow_html=True)
