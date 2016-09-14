# -*- coding: cp1254 -*-
import socket,sys,os,dns.resolver,threading,time,cfscrape,re,requests

print """
------------------------------------------------
Cloudflare Ip Resolver
Coded by @hasanemrebeyy
------------------------------------------------
"""

if len(sys.argv) != 2:
    print "Target is not found. Usage: python2.7 {} [URL] (Url format: example.com)".format(sys.argv[0])
    sys.exit()
site = sys.argv[1]

main = socket.gethostbyname(site)

class End( Exception ):
    pass

print "first ip = " + main 
print "-----------------------------------------------------------------"

def mxrecord():
    myResolver = dns.resolver.Resolver() 
    myAnswers = myResolver.query(site, "MX") 
    try:
        print  "MX records listed: "

        for rdata in myAnswers: 
            print socket.gethostbyname(rdata.exchange.to_text().strip("."))

            print "-----------------------------------------------------------------"
    except:
       print "Mx records is failed. Try again please."
       print "-----------------------------------------------------------------"
       pass

def multi(item,site):
    try:
        ip = socket.gethostbyname(item + "." + site)
        print "[+] " + item + site +  ", " + ip + " found."
    except: 
        pass


def getip():
    list = open('subs').readlines()
    print("[!] Trying to site the real IP using different subdomains.")
    for item in list:
        threading.Thread(target=multi,args=(item,site)).start()
    
    print "[-]Not found ips."
    #time.sleep(5)

def info(domain):
    print "-----------------------------------------------------------------"
    scraper = cfscrape.create_scraper()  
    files = ['phpinfo.php', 'php.php', 'php-info.php', '/']
    for infofile in files:
            find= scraper.get("http://"+site + "/"+ infofile).content 
            try:          
                if "PHP Version" in find:
                    r = re.search('<tr><td class="e">SERVER_ADDR </td><td class="v">(.*) </td></tr>', find)
                    if r:
                        print "[+] Real ip = " + r.group(1)
            except:
                pass  


        	

mxrecord() 
getip()
info(site)
