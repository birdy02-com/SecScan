# -*- coding: utf-8 -*-
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
import subprocess, os, json, time, argparse
from docx.shared import RGBColor
from datetime import datetime
from docx import Document

outPath = "output"


# 方法
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


# 文件输出
class Docx:
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
        t = doc.add_paragraph('生成时间：' + Function.timer())
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
        doc.save(os.path.join(out_file, v['vName'].replace("/", '') + '.docx'))
        return v['vName'] + '.docx'


# 漏洞检测方法
def exploit(_poc, _url: str) -> dict:
    process = subprocess.Popen(
        [
            r"secScript.exe",
            "-poc", _poc,
            "-vUrl", _url,
            "-api", "true"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf-8'  # 指定正确的编码
    )
    stdout, _ = process.communicate()
    return json.loads(stdout)


# icp查询
# 返回参考：https://apifox.com/apidoc/shared-76f1bd0e-6083-4251-91a2-e96c9bb3bce2/api-219597580
def icp(keyword: str) -> dict:
    process = subprocess.Popen(
        [
            r"secScript.exe",
            "-icp", keyword,
            "-api", "true"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf-8'  # 指定正确的编码
    )
    stdout, _ = process.communicate()
    return json.loads(stdout)


# ip属地查询
# 返回参考：https://apifox.com/apidoc/shared-76f1bd0e-6083-4251-91a2-e96c9bb3bce2/api-217943200
def ip(ipv4: str) -> dict:
    process = subprocess.Popen(
        [
            r"secScript.exe",
            "-ip", ipv4,
            "-api", "true"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf-8'  # 指定正确的编码
    )
    stdout, _ = process.communicate()
    return json.loads(stdout)


# 获取域名的A记录
# 返回参考：https://apifox.com/apidoc/shared-76f1bd0e-6083-4251-91a2-e96c9bb3bce2/api-219607563
def dns(domain: str) -> dict:
    process = subprocess.Popen(
        [
            r"secScript.exe",
            "-ns", domain,
            "-api", "true"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf-8'  # 指定正确的编码
    )
    stdout, _ = process.communicate()
    return json.loads(stdout)


def analyze_url(uri, cms: str) -> dict:
    process = subprocess.Popen(
        [
            r"secScript.exe",
            "-url", uri,
            "-api", "true",
            "-cms", "true" if cms else ""
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding='utf-8'  # 指定正确的编码
    )
    stdout, _ = process.communicate()
    return json.loads(stdout)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-poc', '--poc', help='poc文件')
    parser.add_argument('-u', '--url', help='配合漏洞检测时候（要检测的URL） | 站点分析时（要分析的url）')
    parser.add_argument('-cms', '--cms', help='配合站点分析时使用，输入值不为空')
    parser.add_argument('-out', '--out', type=bool, default=False, help='是否输出文件：(True | False)')
    parser.add_argument('-ip', '--ipv4', help='要查询属地的ipv4地址')
    parser.add_argument('-icp', '--icp', help='要查询ICP的单位名/域名/ICP号')
    parser.add_argument('-uf', '--ufile', help='指定要批量检测的url文件')
    parser.add_argument('-ns', '--dns', help='要获取A记录的域名')
    args = parser.parse_args()

    if args.poc:
        path = os.path.join(outPath, str(int(time.time())))
        if not os.path.isfile(args.poc): return print("文件不存在", args.poc)
        if args.url:
            if not args.url.startswith('http'): return print("URL错误", args.url)
            if not os.path.exists(path): os.makedirs(path)
            res = exploit(args.poc, args.url)
            if args.out:
                print(args.url, "存在漏洞" if res["isVul"] else "不存在漏洞", res["vName"])
                if res['isVul']: print("输出文件:", Docx.write_docx(res, args.url, path))
            else:
                print(res)

        elif args.ufile:
            if not os.path.isfile(args.ufile): return print("文件不存在", args.ufile)
            with open(args.ufile, 'r', encoding='utf-8') as f:
                urls = [i.strip() for i in f.read().split('\n') if i.strip() != "" and i.startswith('http')]
            if not os.path.exists(path): os.makedirs(path)
            for url in urls:
                res = exploit(args.poc, url)
                print(url, "存在漏洞" if res["isVul"] else "不存在漏洞", res["vName"])
                if res['isVul']: print("输出文件:", Docx.write_docx(res, args.url, path))

    elif args.ipv4:
        res = ip(args.ipv4)
        print(res)

    elif args.icp:
        res = icp(args.icp)
        print(res)

    elif args.dns:
        res = dns(args.dns)
        print(res)
    elif args.url:
        res = analyze_url(args.url, args.cms)
        print(res)


if __name__ == "__main__":
    main()

# poc = r"C:\Users\b0bef\Documents\Golang\secScript\EXE\vul\OA\致远OA\致远OA A6 createMysql.jsp 数据库敏感信息泄露-1.yaml"
# url = "https://api.birdy02.com"
