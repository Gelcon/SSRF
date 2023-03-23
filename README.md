本工具用于检测SSRF类型漏洞



## Test Environment ##

>CentOS 7
>
>Python 3.8.11

## Tree ##

	SSRF
	.
	├── test
	│   ├── example.py			# 利用Flask框架编写的含有SSRF漏洞的网站
	│   ├── requestx.txt		# BurpSuite格式的请求案例
	│   └── test.py				# 测试功能
	├── tool
	│   ├── ip.py				# 生成各种形式的payload，其中all_payload是对外生成payload的方法
	│   ├── detection.py		# 检测SSRF类型漏洞
	├── main.py					# 主程序

## Deploy ##

	脚本放置在任意目录中
	1）$ python main.py			# 运行主程序



## Config ##

配置参数：SSRF_payload.py

	# 修改扫描或访问的ip地址
	ip = '127.0.0.1'
	# 添加访问的域名白名单，通常会用于绕过服务端域名白名单的限制
	domain = 'www.baidu.com'

