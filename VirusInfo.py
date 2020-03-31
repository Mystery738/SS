import requests, os, random, getpass
from bs4 import BeautifulSoup
from time import localtime, strftime
from colorama import Fore

import smtplib as root
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

url = ''
headers_useragents = list ()

def clear ():
	if os.name == 'nt':
		_ = os.system ('cls')
	else:
		_ = os.system ('clear')

def useragent_list():
	global headers_useragents
	headers_useragents.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3')
	headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
	headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)')
	headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1')
	headers_useragents.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1')
	headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)')
	headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)')
	headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)')
	headers_useragents.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)')
	headers_useragents.append('Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)')
	headers_useragents.append('Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)')
	headers_useragents.append('Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51')
	return(headers_useragents)
	
def randomString(size):
	out_str = ''
	for i in range(0, size):
		a = random.randint(65, 90)
		out_str += chr(a)
	return(out_str)

def initHeaders():
	useragent_list()
	global headers_useragents
	headers = {
				'User-Agent': random.choice(headers_useragents),
				'Cache-Control': 'no-cache',
				'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
				'Referer': 'http://www.google.com/?q=' + randomString(random.randint(5,10)),
				'Keep-Alive': str(random.randint(110,120)),
				'Connection': 'keep-alive'
				}

	return headers

def sent_main (url, textToUser, login, password):
		msg = MIMEMultipart()

		msg['Subject'] = 'Приветствую! Вот актуальная информация по короновирусу.'
		msg['From'] = login
		body = textToUser

		msg.attach (MIMEText(body, 'plain'))

		server = root.SMTP_SSL (url, 465 )
		server.login (login, password)

		server.sendmail (login, login, msg.as_string() )
		print (Fore.GREEN + 'Сообщение успешно отправлено!')	

def get_page_data (url):
	headers = initHeaders()
	req = requests.get (url, headers = headers)
	soup = BeautifulSoup (req.text, 'lxml')

	coronovirus = soup.findAll ('div', {'id' : 'maincounter-wrap'})

	cases = coronovirus[0].find ('div', {'class' : 'maincounter-number'}).find ('span')
	death = coronovirus[1].find ('div', {'class' : 'maincounter-number'}).find ('span')
	recovered = coronovirus[2].find ('div', {'class' : 'maincounter-number'}).find ('span') 

	return 'Информация по миру:' + '\nЗафиксировано случаев -> ' + cases.text + '\nУмерло -> ' + death.text + '\nВылечилось -> ' + recovered.text

def main ():
	
	print ('''
Наш телеграмчик: @Termuxtop
 ▌ ▐·▪  ▄▄▄  ▄• ▄▌.▄▄ · ▪   ▐ ▄ ·▄▄▄      
▪█·█▌██ ▀▄ █·█▪██▌▐█ ▀. ██ •█▌▐█▐▄▄·▪     
▐█▐█•▐█·▐▀▀▄ █▌▐█▌▄▀▀▀█▄▐█·▐█▐▐▌██▪  ▄█▀▄ 
 ███ ▐█▌▐█•█▌▐█▄█▌▐█▄▪▐█▐█▌██▐█▌██▌.▐█▌.▐▌
. ▀  ▀▀▀.▀  ▀ ▀▀▀  ▀▀▀▀ ▀▀▀▀▀ █▪▀▀▀  ▀█▄▀▪
[1] -> Отправка актуальной информации на Mail
[2] -> Отправка актуальной информации на Yandex
		''')

	task = input ('Выберите задачу: ')

	if task == '1':
		url = 'smtp.mail.ru'
	elif task == '2':
		url = 'smtp.yandex.ru'
	else:
		print ('Неправильный номер')

	timePush = input ('Во сколько отправлять: ')
	login = input ('Введите почту для отправки: ')
	password = getpass.getpass ('Пароль: ')

	print ('Ждите отправки и не закрывайте консоль!')

	while True:
		if strftime("%H:%M:%S", localtime()) == timePush:
			textToUser = get_page_data ('https://www.worldometers.info/coronavirus/')
			sent_main (url, textToUser, login, password)

if __name__ == '__main__':
	clear ()
	main ()