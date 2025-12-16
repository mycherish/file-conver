# file-conver
文件格式转换工具

## 说明
- 2025年12月16日 23:26:25

    > PDF 转 PNG，图片转 PDF

## 如何使用
1. 终端使用
    ```bash
    # 1. 创建虚拟环境（只需一次）
    uv venv

    # 2. 安装依赖（无需 activate！）
    uv pip install PyMuPDF img2pdf natsort

    # 3. 运行脚本（无需 activate！）
    uv run python images_to_pdf.py
    ```

2. releases 中下载可执行程序