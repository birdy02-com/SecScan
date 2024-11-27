# -*- coding: utf-8 -*-
import json
import time

from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import subprocess, os
from docx.shared import RGBColor
from datetime import datetime
from docx import Document


class Function:
    @classmethod
    def timer(cls) -> str:  # 时间
        now = datetime.now()
        year = f'{now.year:02}'
        month = f'{now.month:02}'
        day = f'{now.day:02}'
        hour = f'{now.hour:02}'
        minute = f'{now.minute:02}'
        second = f'{now.second:02}'
        return f"{year}年{month}月{day}日{hour}时{minute}分{second}秒"

    @classmethod
    def _row_tit(cls, doc, text: str):
        line = doc.add_paragraph()
        tit = line.add_run(f'{text}：')
        tit.bold = True
        tit.font.color.rgb = RGBColor(0, 51, 102)  # 使用RGB颜色
        return line

    @classmethod
    def write_docx(cls, v: dict, _url: str, out_file: str) -> str:
        doc = Document()
        # 标题
        heading = doc.add_heading('漏洞报告', 0)
        heading.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        t = doc.add_paragraph('生成时间：' + cls.timer())
        t.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT
        cls._row_tit(doc, "漏洞名称").add_run(v['vName'])
        cls._row_tit(doc, "漏洞URL").add_run(_url)
        cls._row_tit(doc, "是否存在漏洞").add_run('是' if v['isVul'] else '否')
        cls._row_tit(doc, "影响产品").add_run(v['product'])
        cls._row_tit(doc, "影响版本").add_run(v['version'])
        cls._row_tit(doc, "危险等级").add_run(v['level'])
        if v['vId']:
            cls._row_tit(doc, "漏洞编号")
            for n, i in enumerate(v['vId']):
                doc.add_paragraph(str(n + 1) + '：' + i)

        cls._row_tit(doc, "漏洞描述").add_run(v['vDesc'])
        cls._row_tit(doc, "参考链接").add_run(v['link'])
        if v['fix']:
            cls._row_tit(doc, "修复建议")
            for n, i in enumerate(v['fix']):
                doc.add_paragraph(str(n + 1) + '：' + i)
        doc.add_paragraph('')
        doc.add_paragraph('')
        request = v['request']
        cls._row_tit(doc, ">> 请求")
        cls._row_tit(doc, "URL").add_run(request['url'])
        cls._row_tit(doc, "请求方法").add_run(request['method'])
        cls._row_tit(doc, "请求头")
        table = doc.add_table(rows=1, cols=1)
        for row_index, row in enumerate(table.rows):
            for col_index, cell in enumerate(row.cells):
                hed, text = request['header'], ''
                for i in hed: text += i + ': ' + hed[i] + '\n'
                cell.text = text.rstrip('\n')
        if request['body']:
            cls._row_tit(doc, "请求体")
            table = doc.add_table(rows=1, cols=1)
            for row_index, row in enumerate(table.rows):
                for col_index, cell in enumerate(row.cells): cell.text = request['body']
        doc.add_paragraph('')
        doc.add_paragraph('')
        response = v['response']
        cls._row_tit(doc, ">> 响应")
        cls._row_tit(doc, "URL").add_run(response['url'])
        cls._row_tit(doc, "状态码").add_run(str(response['code']))
        cls._row_tit(doc, "响应头")
        table = doc.add_table(rows=1, cols=1)
        for row_index, row in enumerate(table.rows):
            for col_index, cell in enumerate(row.cells):
                hed, text = response['header'], ''
                for i in hed: text += i + ': ' + hed[i] + '\n'
                cell.text = text.rstrip('\n')
        cls._row_tit(doc, "响应体")
        table = doc.add_table(rows=1, cols=1)
        for row_index, row in enumerate(table.rows):
            for col_index, cell in enumerate(row.cells): cell.text = response['body']
        doc.save(os.path.join("output", out_file, v['vName'].replace("/", '') + '.docx'))
        return v['vName'] + '.docx'


def exploit(_poc, _url: str):
    process = subprocess.Popen(
        [
            r"C:\Users\b0bef\Documents\Golang\secScript\EXE\secScript.exe",
            "-vul",
            "api",
            "-poc",
            _poc,
            "-vUrl",
            _url
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf-8'  # 指定正确的编码
    )
    stdout, _ = process.communicate()
    return json.loads(stdout)


poc = r"C:\Users\b0bef\Documents\Golang\secScript\EXE\vul\OA\致远OA\致远OA A6 createMysql.jsp 数据库敏感信息泄露-1.yaml"
url = "https://api.birdy02.com"
# 调用 Go 程序
res = exploit(poc, url)
path = os.path.join("output",str(int(time.time())))
if not os.path.exists(path): os.makedirs(path)
Function.write_docx(res, url, str(int(time.time())))
