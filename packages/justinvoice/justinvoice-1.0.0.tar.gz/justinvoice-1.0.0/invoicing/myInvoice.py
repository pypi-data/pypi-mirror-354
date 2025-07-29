import os

import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path


def generate(invoices_path, pdfs_path, image_path, product_id, product_name,
             amount_purchased, price_per_unit, total_price):
    """
    This function converts invoice exel files into pdf files

    :param invoices_path:
    :param pdfs_path:
    :param image_path:
    :param product_id:
    :param product_name:
    :param amount_purchased:
    :param price_per_unit:
    :param total_price:
    :return:
    """
    filepaths = glob.glob(f"{invoices_path}/*.xlsx")  # 读取invoices目录中所有以 “ .xlsx ” 结尾的文件路径，并存入列表

    for filepath in filepaths:
        pdf = FPDF(orientation="P", unit="mm", format="A4")  # 生成PDF文件
        pdf.add_page()
        filename = Path(filepath).stem  # 提取Excel文件名
        invoice_nr = filename.split("-")[0]  # 提取出文件名中的数字
        date = filename.split("-")[1]  # 提取出文件名中的日期
        pdf.set_font(family="Times", style="B", size=16)
        pdf.cell(w=50, h=8, txt=f"Invoice nr.{invoice_nr}", ln=1)
        pdf.cell(w=50, h=8, txt=f"Date {date}", ln=1)

        df = pd.read_excel(filepath, sheet_name="Sheet 1")  # 读取每个Excel文件

        columns = list(df.columns)
        pdf.set_font(family="Times", size=10, style="B")
        pdf.cell(w=30, h=8, txt=columns[0].replace("_", " "), border=1)
        pdf.cell(w=70, h=8, txt=columns[1].replace("_", " "), border=1)
        pdf.cell(w=30, h=8, txt=columns[2].replace("_", " "), border=1)
        pdf.cell(w=30, h=8, txt=columns[3].replace("_", " "), border=1)
        pdf.cell(w=30, h=8, txt=columns[4].replace("_", " "), border=1, ln=1)

        for index, row in df.iterrows():
            pdf.set_font(family="Times", size=10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(w=30, h=8, txt=str(row[product_id]), border=1)
            pdf.cell(w=70, h=8, txt=row[product_name], border=1)
            pdf.cell(w=30, h=8, txt=str(row[amount_purchased]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[price_per_unit]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[total_price]), border=1, ln=1)

        total_sum = df[total_price].sum()
        pdf.set_font(family="Times", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=70, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt=str(total_sum), border=1, ln=1)

        pdf.set_font(family="Times", size=10, style="B")
        pdf.cell(w=30, h=8, txt=f"The total price is {total_sum}", ln=1)
        pdf.set_font(family="Times", size=14, style="B")
        pdf.cell(w=25, h=8, txt="PythonHow")
        pdf.image(image_path, w=10)

        if not os.path.exists(pdfs_path):
            os.makedirs(pdfs_path)
            pdf.output(f"{pdfs_path}/{filename}.pdf")
        else:
            pdf.output(f"{pdfs_path}/{filename}.pdf")
