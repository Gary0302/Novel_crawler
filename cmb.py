import os
from ebooklib import epub
from bs4 import BeautifulSoup
import shutil

def cmb(name, output_path, book_title):
    # 獲取資料夾名稱作為書名

    # 創建 EPUB 實例
    book = epub.EpubBook()

    # 設置 EPUB 書籍的基本資訊
    book.set_identifier(f'id_{book_title}')
    book.set_title(book_title)
    book.set_language('zh')
    book.add_author('Gary')  # 設置作者

    # 添加一個封面
    cover = epub.EpubItem(uid="cover", file_name="cover.xhtml", media_type="application/xhtml+xml", content=f"<html><body><h1>{book_title}</h1></body></html>")
    book.add_item(cover)

    # 讀取資料夾中的所有 .txt 文件並排序
    txt_files = [os.path.join(name, f) for f in os.listdir(name) if f.endswith('.txt')]
    
    # 修改排序邏輯，忽略無法匹配數字的文件
    txt_files.sort(key=lambda x: int(''.join(filter(str.isdigit, os.path.basename(x)))))

    # 遍歷每個 txt 文件並創建對應的 EPUB 頁面
    for txt_file in txt_files:
        with open(txt_file, 'r', encoding='utf-8') as file:
            content = file.read()

        # 生成頁面標題為 txt 文件名
        a = str(os.path.basename(txt_file).split("_")[1])
        page_title = a.split(".")[0]

        # 把換行符轉換成 <br> 標籤
        content_with_br = content.replace('\n', '<br>')

        # 創建 HTML 頁面
        page_content = f"<html><body><h1>{page_title}</h1><p>{content_with_br}</p></body></html>"
        soup = BeautifulSoup(page_content, 'html.parser')

        # 創建 EPUB 頁面
        chapter = epub.EpubHtml(title=page_title, file_name=f'{page_title}.xhtml', lang='zh')
        chapter.content = str(soup)

        # 將頁面添加到書籍中
        book.add_item(chapter)

        # 添加到目錄和 spine
        book.toc.append(chapter)
        book.spine.append(chapter)

    # 添加 CSS 文件
    style = """
    body {
        font-family: "Arial", sans-serif;
        line-height: 1.5;
        margin: 20px;
    }

    h1 {
        font-size: 24px;
        text-align: center;
    }

    p {
        font-size: 14px;
        text-align: justify;
    }
    """
    css_item = epub.EpubItem(uid="style", file_name="styles.css", media_type="text/css", content=style)
    book.add_item(css_item)

    # 定義導航
    book.add_item(epub.EpubNav())

    # 儲存 EPUB 文件
    output_file = os.path.join(output_path, f"{book_title}.epub")
    epub.write_epub(output_file, book)
    print(f"EPUB 文件已經生成: {output_file}")

    shutil.rmtree("./tmp")
