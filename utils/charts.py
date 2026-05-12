import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
import numpy as np

NAVY   = "#0B1F3A"
TEAL   = "#0E7B6C"
SKY    = "#4CB8C4"
CREAM  = "#F5F4F0"
WHITE  = "#FFFFFF"
MUTED  = "#6B7A8D"
BORDER = "#DDE3EA"

CLUSTER_COLORS = {
    "Resilient":    "#1A7F4B",
    "Transitional": "#D4850A",
    "Vulnerable":   "#C0392B",
}
PLOTLY_TEMPLATE = dict(
    layout=dict(
        font=dict(family="Plus Jakarta Sans, sans-serif", color=NAVY),
        paper_bgcolor=WHITE,
        plot_bgcolor=WHITE,
        margin=dict(t=40, b=40, l=40, r=20),
        legend=dict(bgcolor=WHITE, bordercolor=BORDER, borderwidth=1, font=dict(size=12)),
    )
)

def apply_template(fig):
    fig.update_layout(**PLOTLY_TEMPLATE["layout"])
    fig.update_xaxes(showgrid=True, gridcolor="#EEF2F7", zeroline=False, linecolor=BORDER)
    fig.update_yaxes(showgrid=True, gridcolor="#EEF2F7", zeroline=False, linecolor=BORDER)
    return fig

# ── EVI Bar Chart ────────────────────────────────────────────────────────────
def evi_bar_chart(df):
    dfs = df.sort_values("EVI", ascending=True).copy()
    colors = [CLUSTER_COLORS[lbl] for lbl in dfs["cluster_label"]]
    fig = go.Figure(go.Bar(
        x=dfs["EVI"], y=dfs["Provinsi"],
        orientation="h",
        marker_color=colors,
        text=dfs["EVI"].round(2),
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "EVI: %{x:.2f}<br>"
            "<extra></extra>"
        )
    ))
    fig.update_layout(
        title="Skor Economic Vulnerability Index (EVI) per Provinsi",
        height=900,
        xaxis_title="EVI Score",
        yaxis_title="",
        yaxis=dict(autorange=True, tickfont=dict(size=11)),
    )
    return apply_template(fig)

# ── EVI Histogram ────────────────────────────────────────────────────────────
def evi_histogram(df):
    fig = go.Figure()
    for label, color in CLUSTER_COLORS.items():
        sub = df[df["cluster_label"] == label]
        fig.add_trace(go.Histogram(
            x=sub["EVI"], name=label,
            marker_color=color, opacity=0.75,
            nbinsx=10,
        ))
    fig.update_layout(
        title="Distribusi EVI per Kategori Cluster",
        barmode="overlay",
        xaxis_title="EVI Score",
        yaxis_title="Frekuensi",
        height=360,
    )
    return apply_template(fig)

# ── PCA Scatter ──────────────────────────────────────────────────────────────
def pca_scatter(df):
    fig = px.scatter(
        df, x="PC1", y="PC2",
        color="cluster_label",
        color_discrete_map=CLUSTER_COLORS,
        text="Provinsi",
        hover_data={"IPM": True, "kemiskinan": True, "akses_internet": True, "cluster_label": False},
        labels={"PC1": "PC1 — Kesejahteraan & Akses", "PC2": "PC2 — Demografi & Tekanan Sosial"},
        title="Visualisasi Cluster Provinsi (PCA Space)",
    )
    fig.update_traces(
        textposition="top center",
        textfont=dict(size=9, color=NAVY),
        marker=dict(size=11, opacity=0.85, line=dict(width=1, color=WHITE)),
    )
    fig.update_layout(
        height=500,
        legend_title_text="Kategori",
    )
    return apply_template(fig)

# ── Variance Explained ───────────────────────────────────────────────────────
def variance_chart(explained, cumulative):
    comps = [f"PC{i+1}" for i in range(len(explained))]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=comps, y=[v*100 for v in explained],
        name="Proporsi Variansi",
        marker_color=TEAL, opacity=0.85,
        yaxis="y",
    ))
    fig.add_trace(go.Scatter(
        x=comps, y=[v*100 for v in cumulative],
        name="Kumulatif",
        mode="lines+markers",
        line=dict(color="#C0392B", width=2.5),
        marker=dict(size=8),
        yaxis="y",
    ))
    fig.add_hline(y=70, line_dash="dot", line_color=MUTED,
                  annotation_text="70% threshold", annotation_position="right")
    fig.update_layout(
        title="Variance Explained oleh Komponen Utama",
        xaxis_title="Komponen Utama",
        yaxis_title="Variansi (%)",
        height=360,
        legend=dict(orientation="h", y=1.12),
    )
    return apply_template(fig)

# ── PCA Loadings Heatmap ─────────────────────────────────────────────────────
def loadings_heatmap(loadings_df):
    fig = go.Figure(go.Heatmap(
        z=loadings_df.values.T,
        x=loadings_df.index.tolist(),
        y=loadings_df.columns.tolist(),
        colorscale=[[0, "#C0392B"],[0.5, WHITE],[1, TEAL]],
        zmid=0,
        text=np.round(loadings_df.values.T, 3),
        texttemplate="%{text}",
        hovertemplate="%{x}<br>%{y}: %{z:.3f}<extra></extra>",
    ))
    fig.update_layout(
        title="PCA Loadings — Kontribusi Variabel ke Komponen Utama",
        height=280,
        xaxis=dict(tickangle=-35, tickfont=dict(size=10)),
        yaxis=dict(tickfont=dict(size=12)),
        margin=dict(t=50, b=100, l=60, r=20),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    return fig

# ── Correlation Heatmap ──────────────────────────────────────────────────────
def correlation_heatmap(df, features):
    corr = df[features].corr()
    short = [f.split(" ")[0] for f in features]
    fig = go.Figure(go.Heatmap(
        z=corr.values,
        x=short, y=short,
        colorscale=[[0,"#C0392B"],[0.5,WHITE],[1,TEAL]],
        zmid=0,
        text=np.round(corr.values, 2),
        texttemplate="%{text}",
        hovertemplate="x=%{x}<br>y=%{y}<br>r=%{z:.2f}<extra></extra>",
    ))
    fig.update_layout(
        title="Correlation Heatmap — Variabel Sosial-Ekonomi",
        height=420,
        margin=dict(t=50, b=50, l=80, r=20),
    )
    fig.update_xaxes(showgrid=False, tickangle=-35)
    fig.update_yaxes(showgrid=False)
    return fig

# ── Elbow Method ─────────────────────────────────────────────────────────────
def elbow_chart(inertias, k_range):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(k_range), y=inertias,
        mode="lines+markers",
        line=dict(color=TEAL, width=2.5),
        marker=dict(size=9, color=TEAL, line=dict(width=2, color=WHITE)),
        name="Inertia",
    ))
    fig.add_vline(x=3, line_dash="dot", line_color="#D4850A",
                  annotation_text="Optimal k=3", annotation_position="top")
    fig.update_layout(
        title="Elbow Method — Penentuan Jumlah Cluster Optimal",
        xaxis_title="Jumlah Cluster (k)",
        yaxis_title="Inertia (WCSS)",
        height=340,
    )
    return apply_template(fig)

# ── Silhouette Chart ──────────────────────────────────────────────────────────
def silhouette_chart(scores, k_range):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=list(k_range), y=scores,
        marker_color=[TEAL if k != 2 else "#D4850A" for k in k_range],
        opacity=0.85,
    ))
    fig.update_layout(
        title="Silhouette Score per Jumlah Cluster",
        xaxis_title="Jumlah Cluster (k)",
        yaxis_title="Silhouette Score",
        height=300,
    )
    return apply_template(fig)

# ── Variable Distribution ─────────────────────────────────────────────────────
def variable_dist(df, col, label):
    fig = go.Figure()
    for cl, color in CLUSTER_COLORS.items():
        sub = df[df["cluster_label"] == cl]
        fig.add_trace(go.Box(
            y=sub[col], name=cl, marker_color=color,
            boxmean="sd", jitter=0.4, pointpos=-1.8,
            marker=dict(size=5, opacity=0.6),
        ))
    fig.update_layout(
        title=f"Distribusi {label} per Cluster",
        yaxis_title=label,
        height=340,
        showlegend=True,
    )
    return apply_template(fig)

# ── Choropleth / Bubble (fallback, no geojson) ────────────────────────────────
def evi_bubble(df):
    fig = px.scatter(
        df.sort_values("EVI", ascending=False),
        x="Provinsi", y="EVI",
        size=df["EVI"].abs() + 1,
        color="cluster_label",
        color_discrete_map=CLUSTER_COLORS,
        hover_data={"IPM": True, "kemiskinan": True, "akses_internet": True},
        title="EVI Bubble Chart — Skor Kerentanan Ekonomi per Provinsi",
        labels={"EVI": "EVI Score", "Provinsi": ""},
    )
    fig.update_traces(marker=dict(opacity=0.80, line=dict(width=1, color=WHITE)))
    fig.update_layout(
        height=420,
        xaxis=dict(tickangle=-45, tickfont=dict(size=9.5)),
    )
    return apply_template(fig)

# ── Forecasting Line ─────────────────────────────────────────────────────────
def forecast_chart(years_hist, hist_vals, years_fc, fc_vals, prov_name):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years_hist, y=hist_vals,
        mode="lines+markers",
        name="Data Historis",
        line=dict(color=TEAL, width=2.5),
        marker=dict(size=8),
    ))
    # confidence band
    fig.add_trace(go.Scatter(
        x=years_fc + years_fc[::-1],
        y=[v+0.4 for v in fc_vals] + [v-0.4 for v in fc_vals][::-1],
        fill="toself",
        fillcolor="rgba(14,123,108,0.10)",
        line=dict(color="rgba(0,0,0,0)"),
        name="Confidence Interval",
    ))
    fig.add_trace(go.Scatter(
        x=years_fc, y=fc_vals,
        mode="lines+markers",
        name="Prediksi EVI",
        line=dict(color="#C0392B", width=2.5, dash="dash"),
        marker=dict(size=8, symbol="diamond"),
    ))
    fig.add_vline(x=2024.5, line_dash="dot", line_color=MUTED,
                  annotation_text="Forecast →", annotation_position="top left")
    fig.update_layout(
        title=f"Forecasting EVI — {prov_name}",
        xaxis_title="Tahun",
        yaxis_title="EVI Score",
        height=380,
        legend=dict(orientation="h", y=1.12),
    )
    return apply_template(fig)

# ── Radar Chart for AI Insight ────────────────────────────────────────────────
def radar_chart(prov_name, values, categories):
    fig = go.Figure(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill="toself",
        fillcolor="rgba(14,123,108,0.18)",
        line=dict(color=TEAL, width=2),
        name=prov_name,
    ))
    fig.update_layout(
        polar=dict(
            bgcolor=WHITE,
            radialaxis=dict(visible=True, range=[0, 10], tickfont=dict(size=9)),
            angularaxis=dict(tickfont=dict(size=10, color=NAVY)),
        ),
        title=f"Profil Indikator — {prov_name}",
        height=380,
        paper_bgcolor=WHITE,
        font=dict(family="Plus Jakarta Sans, sans-serif", color=NAVY),
        margin=dict(t=60, b=40, l=40, r=40),
    )
    return fig
