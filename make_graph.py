# Forecasting Mini-Course Sales
# Playground Series - Season 3, Episode 19
# https://www.kaggle.com/competitions/playground-series-s3e19/overview
# 専用グラフ関数

import numpy as np
import pandas as pd
from bokeh.layouts import gridplot
from bokeh.models import DataRange1d, LinearAxis    # 2軸用
from bokeh.plotting import figure, save, output_file
from bokeh.palettes import d3

TOOLS = "pan,wheel_zoom,box_zoom,reset,save"


def make_trend(df, t_column, c_column, w, h, title):
    """c_column毎に色分けトレンド生成"""
    num_c = df[c_column].nunique() if df[c_column].nunique() > 2 else 3
    c = d3['Category10'][num_c]
    p = figure(title=title, x_axis_type="datetime", height=h, width=w, tools=TOOLS,
               x_axis_label="date", y_axis_label=t_column)
    for i, col in enumerate(df[c_column].unique()):
        df_tmp = df[df[c_column]==col][["date", t_column]]
        p.line("date", t_column, source=df_tmp, line_color=c[i], legend_label=col)
    p.legend.click_policy = "hide"
    return p


def save_file(plots, num_cols, filename, title):
    """ファイルに保存"""
    output_file(filename, title=title)
    save(gridplot(plots, ncols=num_cols))


def trends(df, target="num_sold", width=1200, height=300, filename="graph.html", title="trend"):
    """1カラムのトレンド作成"""
    plots = []
    for prod in df["product"].unique():
        for store in df["store"].unique():
            df_buf = df[(df["product"]==prod) & (df["store"]==store)].drop(columns=["product", "store"])
            df_buf = df_buf.sort_values("date").reset_index(drop=True)
            p = make_trend(df_buf, target, "country", width, height, f"{prod[14:]} ({store})")
            plots.append(p)

    save_file(plots, 1, filename, title)


# def check_feature(df, feat, country="Canada", store="Kaggle Learn",
#                   width=1200, height=300, filename="graph_feat.html", title="feature"):
def check_feature(df, feat, country="Canada", store="Kaggle Learn",
                  width=1200, height=300):
    """特徴量の確認 (ざっくり周期的に店舗の差は無いので、1店舗指定。ついでに国も)"""
    t_column = "num_sold"
    df_buf = df[(df["store"]==store) & (df["country"]==country)].drop(columns=["store", "country"])
    c = d3['Category10'][3]    # 数は3以上
    plots = []
    for prod in df_buf["product"].unique():
        df_prod = df_buf[(df_buf["product"]==prod)].drop(columns=["product"]).sort_values("date").reset_index(drop=True)
        p = figure(title=f"{prod[14:]} ({store}, {country})", x_axis_type="datetime", height=height, width=width, tools=TOOLS,
                   x_axis_label="date", y_axis_label=t_column)
        y_range_name = "secondary_axis"
        p.add_layout(LinearAxis(y_range_name=y_range_name, axis_label=feat), "right")
        t_line = p.line("date", t_column, source=df_prod, line_color=c[0], legend_label=t_column)
        f_line = p.line("date", feat, source=df_prod, line_color=c[1], legend_label=feat, y_range_name=y_range_name)
        p.y_range.renderers = [t_line]
        p.extra_y_ranges = {y_range_name: DataRange1d(renderers=[f_line])}
        # p.legend.click_policy = "hide"
        plots.append(p)

    # save_file(plots, 1, filename, title)
    # 呼び出し元で操作 show(gridplot(plots, ncols=1))
    return plots
