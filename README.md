# 介绍

`SecScan` 是一款集漏洞探测、端口扫描、指纹识别为一体的工具，拥有多样化的漏洞检测方法，支持对目标自动化进行 **端口扫描**->**指纹识别**->**服务口令探测**->**漏洞探测** 流程，旨在帮助用户/红队选手快速发现漏洞风险，提升漏洞管理效率。

如果你有好的建议欢迎在 [林乐天的个人博客](https://www.birdy02.com/secscript) 中留言🙂。

## 核心亮点

### 1. 强大的漏洞检测能力

支持自动漏洞检测、批量漏洞检测，多任务并发检测，多样化的漏洞检测方法帮助你快速发现资产的脆弱点，自动生成检测报告，并以 Excel 格式记录检测结果，便于后续分析与管理。工具目前支持三种检测方法：

- **自动检测**：指定一个url或包含url的文件，识别CMS并自动调用poc进行漏洞检测。
- **全部检测**：不识别CMS，调用poc进行全量漏洞检测。
- **选择式检测**：按照程序选择方法选择单个或全部漏洞对单个或多个资产进行检测。
- **指定poc文件**：对单个或多个资产进行检测。

### 2. 综合端口扫描

综合网络扫描模块，方便一键自动化、全方位安全检测，支持端口扫描、常见服务的爆破、web指纹识别、web漏洞扫描。

1. **信息收集**
    - 开放端口扫描
    - 端口服务探测

2.  **口令爆破**
    - 服务口令爆破：ssh、smb
    - 数据库爆破：mysql、mssql、redis、oracle、...

3. **web扫描**
    - web信息扫描
    - 指纹识别 (12000+ cms、OA、框架)
    - web漏洞扫描 （根据指纹信息精准扫描漏洞，现有poc 550+）


### 3. 丰富的内置功能与接口

- **ICP 查询**：快速获取目标站点的备案信息。
- **IP 属地查询**：定位目标 IP 的地理归属。
- **站点分析**：多维度解析目标网站的关键属性，提取一些泄露的敏感信息。
- **CMS 识别**：精准识别网站所使用到的技术和框架。
- **DNS 解析**：轻松掌握域名解析情况。

### 3. 高性能主程序

主程序基于 Golang 开发，具备卓越的性能与稳定性，可通过 JSON 格式返回检测结果，便于多种场景下的集成与调用。

### 4. 灵活的开发扩展

支持 Python + Golang 联合驱动，提供更大的开发自由度和自定义空间，满足不同用户的个性化需求。

[一些python开发工具示例](https://www.birdy02.com/docs/secscan/scripts)

## 适用场景

`SecScan` 为网络安全从业者提供了一站式的检测与分析解决方案，广泛应用于漏洞排查、安全评估、信息资产分析等工作中，为提升网络安全工作效率和准确性提供有力支持。

# 注意
- 程序功能分别由本地方法和远程API组成的，ICP、IP属地功能需要登录后使用。
- 漏洞检测需要登录后初始化下载或更新POC。

如果您觉得 `SecScan` 项目对您有所帮助，或者您喜欢我的项目，请在 [GitHub](https://github.com/birdy02-com/SecScan) 上给我一个 ⭐️。您的支持是我持续改进和增加新功能的动力！感谢您的支持！

# WeChat交流群
![dcc95a30eae958ab3610b01b145fdb6](https://github.com/user-attachments/assets/b9c8a7bd-5fcf-4a14-8b0c-b03038eed80a)



