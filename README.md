本工具用于检测SSRF类型漏洞



## Test Environment ##

>Centos 7
>
>Python 3.8

## Tree ##

	SSRF
	.
	├── test
	│   └── Test.py				# 测试功能
	├── tool
	│   ├── ip.py				# 生成各种形式的ip转换格式
	│   ├── Burp2Requests.py	# 处理BurpSuite格式的请求
	├── main.py					# 主程序

## Deploy ##

	脚本放置在任意目录中
	1）$ python SRF_payload.py 尝试运行并生成关于127.0.0.1的payload



## Config ##

配置参数：SSRF_payload.py

	# 修改扫描或访问的ip地址
	ip = '127.0.0.1'
	# 添加访问的域名白名单，通常会用于绕过服务端域名白名单的限制
	domain = 'www.baidu.com'

