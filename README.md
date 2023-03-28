本工具用于检测SSRF类型漏洞



## Test Environment ##

>CentOS 7.9
>
>Python 3.8.11



## Tree ##

	SSRF
	.
	├── result
	│   ├── payload
	│   │   ├──	payload_info			# 包含原始payload的info对象
	│   │   └──	payload_origin			# 原始的payload
	│   └── request_log					# 利用生成的info对象（包含payload）发送请求的日										志，成功或失败的信息
	├── test
	│   ├── example.py					# 利用Flask框架编写的含有SSRF漏洞的网站
	│   ├── all_request_template.txt	# GET、POST请求的模板，用于测试
	│   └── test.py						# 测试功能
	├── ip.py							# 生成各种形式的payload，其中all_payload是对										外生成payload的方法
	├── detection.py					# 检测SSRF类型漏洞
	├── main.py							# 主程序，待完成“批量处理爬虫得到的BurpSuite格式										求”的功能



## Deploy ##

	



## Config ##

```
```

