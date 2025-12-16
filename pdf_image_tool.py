import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
from pathlib import Path

# 功能1：图片 → PDF
import img2pdf
from natsort import natsorted

# 功能2：PDF → PNG（使用 PyMuPDF / fitz）
import fitz  # PyMuPDF


def images_to_pdf(image_folder, output_pdf):
    image_files = [
        os.path.join(image_folder, f)
        for f in natsorted(os.listdir(image_folder))
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif'))
    ]
    if not image_files:
        raise ValueError("文件夹中没有支持的图片！")
    with open(output_pdf, "wb") as f:
        f.write(img2pdf.convert(image_files))


def pdf_to_images(pdf_path, output_folder, zoom=200):
    os.makedirs(output_folder, exist_ok=True)
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        raise RuntimeError(f"无法打开 PDF 文件：{e}")

    for pg in range(doc.page_count):
        page = doc[pg]
        mat = fitz.Matrix(zoom / 100.0, zoom / 100.0)  # zoom=200 表示 2x 分辨率
        pix = page.get_pixmap(matrix=mat, alpha=False)  # 不带透明通道
        out_path = os.path.join(output_folder, f"page_{pg + 1:03d}.png")
        pix.save(out_path)
    doc.close()


class App:
    def __init__(self, root):
        self.root = root
        root.title("PDF ↔ 图片 转换工具")
        root.geometry("520x260")
        root.resizable(False, False)

        tk.Label(root, text="多功能文档转换器", font=("Arial", 16, "bold")).pack(pady=12)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame, text="📁 图片转 PDF", command=self.run_images_to_pdf,
            width=22, height=2, font=("Arial", 11)
        ).grid(row=0, column=0, padx=12, pady=8)

        tk.Button(
            btn_frame, text="📄 PDF 转 PNG 图片", command=self.run_pdf_to_images,
            width=22, height=2, font=("Arial", 11)
        ).grid(row=0, column=1, padx=12, pady=8)

        self.status_var = tk.StringVar(value="就绪")
        tk.Label(root, textvariable=self.status_var, fg="gray", font=("Arial", 10)).pack(pady=5)

        tk.Label(
            root,
            text="输出文件将保存在原文件/文件夹所在目录",
            fg="gray",
            font=("Arial", 9)
        ).pack(side=tk.BOTTOM, pady=8)

    def set_status(self, msg):
        self.status_var.set(msg)
        self.root.update()

    def run_in_thread(self, func):
        self.set_status("处理中，请稍候...")
        threading.Thread(target=func, daemon=True).start()

    def run_images_to_pdf(self):
        folder = filedialog.askdirectory(title="选择包含图片的文件夹")
        if not folder:
            return
        output_pdf = os.path.join(folder, "output_images.pdf")
        self.run_in_thread(lambda: self._do_images_to_pdf(folder, output_pdf))

    def _do_images_to_pdf(self, folder, output_pdf):
        try:
            images_to_pdf(folder, output_pdf)
            self.set_status("✅ 图片转 PDF 成功！")
            messagebox.showinfo("成功", f"PDF 已生成：\n{output_pdf}")
        except Exception as e:
            self.set_status("❌ 转换失败")
            messagebox.showerror("错误", str(e))

    def run_pdf_to_images(self):
        pdf_file = filedialog.askopenfilename(
            title="选择 PDF 文件",
            filetypes=[("PDF 文件", "*.pdf")]
        )
        if not pdf_file:
            return
        output_folder = os.path.join(os.path.dirname(pdf_file), Path(pdf_file).stem + "_images")
        self.run_in_thread(lambda: self._do_pdf_to_images(pdf_file, output_folder))

    def _do_pdf_to_images(self, pdf_path, output_folder):
        try:
            pdf_to_images(pdf_path, output_folder, zoom=200)
            self.set_status("✅ PDF 转图片成功！")
            messagebox.showinfo("成功", f"图片已保存至：\n{output_folder}")
        except Exception as e:
            self.set_status("❌ 转换失败")
            messagebox.showerror("错误", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()