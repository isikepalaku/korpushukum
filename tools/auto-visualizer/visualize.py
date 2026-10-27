#!/usr/bin/env python3
"""
Auto Data Summarizer & Visualizer for Tabular Data (CSV, Excel).
Generates comprehensive statistical summaries and automatic charts (matplotlib/seaborn).
Optimized for headless server execution without DISPLAY.
"""

import os
import sys
import argparse
from pathlib import Path

# Force headless matplotlib backend before importing pyplot
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Styling configuration
sns.set_theme(style="darkgrid")
plt.rcParams.update({
    "figure.autolayout": True,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
})

def analyze_and_visualize(file_path: str, out_dir: str = None) -> dict:
    src = Path(file_path).resolve()
    if not src.is_file():
        raise FileNotFoundError(f"File tidak ditemukan: {src}")

    # Determine out_dir
    if out_dir is None:
        target_dir = src.parent / f"{src.stem}_charts"
    else:
        target_dir = Path(out_dir).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    # Load file
    ext = src.suffix.lower()
    if ext == ".csv":
        # Try comma, then semicolon
        try:
            df = pd.read_csv(src)
        except Exception:
            df = pd.read_csv(src, sep=";")
    elif ext in (".xlsx", ".xls"):
        df = pd.read_excel(src)
    else:
        raise ValueError(f"Format {ext} tidak didukung (harus .csv / .xlsx / .xls)")

    total_rows, total_cols = df.shape
    cols = list(df.columns)
    
    # Identify column categories
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category", "string"]).columns.tolist()
    
    # Identify date candidates
    date_cols = []
    for col in cat_cols:
        col_lower = col.lower()
        if any(k in col_lower for k in ("tgl", "tanggal", "date", "waktu", "time", "created")):
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce")
                date_cols.append(col)
            except Exception:
                pass
    # Update cat_cols after date extraction
    cat_cols = [c for c in cat_cols if c not in date_cols]

    generated_charts = []

    # 1. Plot Distribution / Histogram for Numeric Columns (Up to 3 numeric cols)
    for col in num_cols[:3]:
        valid_series = df[col].dropna()
        if len(valid_series) > 1 and valid_series.nunique() > 1:
            fig, ax = plt.subplots(figsize=(7, 4.5))
            sns.histplot(valid_series, kde=True, ax=ax, color="#0ea5e9")
            ax.set_title(f"Distribusi Data: {col}", fontweight="bold")
            chart_path = target_dir / f"dist_{col}.png"
            fig.savefig(chart_path, dpi=120)
            plt.close(fig)
            generated_charts.append(str(chart_path))

    # 2. Plot Top Categories (Up to 2 categorical cols with <= 20 unique values)
    for col in cat_cols[:2]:
        val_counts = df[col].value_counts().head(10)
        if len(val_counts) > 1:
            fig, ax = plt.subplots(figsize=(8, 4.5))
            sns.barplot(x=val_counts.values, y=val_counts.index.astype(str), hue=val_counts.index.astype(str), legend=False, ax=ax, palette="mako")
            ax.set_title(f"Top Frekuensi: {col}", fontweight="bold")
            ax.set_xlabel("Jumlah Frekuensi")
            chart_path = target_dir / f"bar_{col}.png"
            fig.savefig(chart_path, dpi=120)
            plt.close(fig)
            generated_charts.append(str(chart_path))

    # 3. Correlation Heatmap (If >= 2 numeric columns)
    if len(num_cols) >= 2:
        corr = df[num_cols].corr()
        if not corr.empty and not corr.isna().all().all():
            fig, ax = plt.subplots(figsize=(6, 5))
            sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax, cbar=True)
            ax.set_title("Korelasi Antar Kolom Numerik", fontweight="bold")
            chart_path = target_dir / "correlation_heatmap.png"
            fig.savefig(chart_path, dpi=120)
            plt.close(fig)
            generated_charts.append(str(chart_path))

    # 4. Time Series Trend (If date col found)
    if date_cols and num_cols:
        d_col = date_cols[0]
        v_col = num_cols[0]
        ts_df = df[[d_col, v_col]].dropna().sort_values(by=d_col)
        if len(ts_df) > 3:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(ts_df[d_col], ts_df[v_col], marker="o", markersize=3, color="#10b981", linewidth=1.5)
            ax.set_title(f"Tren Waktu: {v_col} vs {d_col}", fontweight="bold")
            fig.autofmt_xdate()
            chart_path = target_dir / f"trend_{v_col}.png"
            fig.savefig(chart_path, dpi=120)
            plt.close(fig)
            generated_charts.append(str(chart_path))

    # Summary statistics
    summary = {
        "source_file": str(src),
        "rows": total_rows,
        "cols": total_cols,
        "numeric_columns": num_cols,
        "categorical_columns": cat_cols,
        "date_columns": date_cols,
        "null_counts": df.isnull().sum().to_dict(),
        "charts": generated_charts,
    }
    return summary

def main():
    parser = argparse.ArgumentParser(description="Auto CSV & Data Visualizer")
    parser.add_argument("file", help="Path file CSV atau Excel")
    parser.add_argument("--out", "-o", help="Direktori output gambar (default: <file_stem>_charts/)")
    args = parser.parse_args()

    res = analyze_and_visualize(args.file, args.out)
    print(f"=== RINGKASAN DATA: {Path(args.file).name} ===")
    print(f"Dimensi: {res['rows']} baris x {res['cols']} kolom")
    print(f"Kolom Numerik ({len(res['numeric_columns'])}): {', '.join(res['numeric_columns']) if res['numeric_columns'] else '-'}")
    print(f"Kolom Kategori ({len(res['categorical_columns'])}): {', '.join(res['categorical_columns'][:5]) if res['categorical_columns'] else '-'}")
    print(f"\nGrafik Terbuat ({len(res['charts'])}):")
    for c in res['charts']:
        print(f"- {c}")

if __name__ == "__main__":
    main()
