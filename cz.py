import requests
from bs4 import BeautifulSoup
import re
import os
import time

def CZcrawl_novel(start_url):
    
    def extract_book_title(html):
        """從 HTML 中提取書名"""
        soup = BeautifulSoup(html, "html.parser")
        title_tag = soup.find("title")
        if title_tag:
            title_text = title_tag.get_text()
            match = re.search(r'【(.*?)】', title_text)  # 提取【】中的內容
            if match:
                return match.group(1).strip()  # 返回書名
        return "未知書名"  # 如果無法提取，使用預設名稱

    def extract_book_chapter(html):
        #從 HTML 中提取章節名稱

        soup = BeautifulSoup(html, "html.parser")
        title_tag = soup.find("title")
        if title_tag:
            title_text = title_tag.get_text()
            match = re.search(r"】(.*?) \|", title_text)  # 提取【】中的內容
            if match:
                return match.group(1).strip()  #
        return None 
    

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    current_url = start_url
    chapter_number = 1
    book_title = None

    cycle = 0

    while current_url:
        try:
            response = requests.get(current_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # 提取書名（僅在第一次請求時）
            if book_title is None:
                book_title = extract_book_title(response.text)
                print(f"書名提取成功: {book_title}")

            # 提取內容

            chapter_name = extract_book_chapter(response.text)

            content_div = soup.find("div", class_="content")
            if content_div:
                chapter_text = content_div.get_text(separator="\n", strip=True)
                if chapter_name != None:
                    output_file = os.path.join("./tmp", f"{chapter_number}_{chapter_name}.txt")
                else:
                    output_file = os.path.join("./tmp", f"chapter_{chapter_number}.txt")
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(chapter_text)

                if chapter_name != None:
                    print(f"成功保存章節: {chapter_number}_{chapter_name}.txt")
                else:
                    print(f"成功保存章節: chapter_{chapter_number}.txt")
            cycle += 1
            if cycle == 3:
                print("3")
                time.sleep(1)
                print("2")
                time.sleep(1)
                print("1")
                time.sleep(1)
                cycle = 0
            # 查找下一章的鏈接
            next_page_link = soup.find("a", class_="next-chapter")
            if next_page_link and 'href' in next_page_link.attrs:
                next_url = next_page_link['href']
                current_url = "https:" + next_url if next_url.startswith("//") else next_url
                chapter_number += 1
            else:
                print("沒有找到 '下一章' 的鏈接，爬取結束。")
                current_url = None  # 結束爬取


        except Exception as e:
            print(f"處理網址 {current_url} 時發生錯誤: {e}")
            break
    return book_title



#source .venv/bin/activate