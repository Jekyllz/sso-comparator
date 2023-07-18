from pysnc import ServiceNowClient
from getpass import getpass
import re, sys, time, os, threading
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1: 
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def __enter__(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            return False

def clearscreen():
    #Find device type and clear screen
    os.system('cls' if os.name == 'nt' else 'clear')

def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor

def welcomecomparator():
    global time
    global os
    print(bcolors.OKGREEN,'        _____ _____  ____     ______ ____   __  ___ ____   ___     ____   ___   ______ ____   ____ ')
    print('        / ___// ___/ / __ \\   / ____// __ \\ /  |/  // __ \\ /   |   / __ \\ /   | /_  __// __ \\ / __ \\')
    print('        \__ \\ \__ \\ / / / /  / /    / / / // /\_/ // /_/ // /| |  / /_/ // /| |  / /  / / / // /_/ /')
    print('       ___/ /___/ // /_/ /  / /___ / /_/ // /  / // ____// ___ | / _, _// ___ | / /  / /_/ // _, _/ ')
    print('      /____//____/ \____/   \____/ \____//_/  /_//_/    /_/  |_|/_/ |_|/_/  |_|/_/   \____//_/ |_|  ')
    print('                                                                                                    ')
    print('                                                                                                    ')
    print(bcolors.OKCYAN,'      Automatic ServiceNow Troubleshooting                                                      ',bcolors.ENDC)

    with Spinner():
        time.sleep(1.5)
        os.system('cls' if os.name == 'nt' else 'clear')

def login():
    # User Prompt for instance name and user credentials 
    global client
    global inst
    global name
    global password
    global url
    print(bcolors.OKCYAN,"Please Enter Instance Name",bcolors.ENDC)
    inst = input("(only name element not including .service-now) : ")
    name = input("ServiceNow User : ")
    password = getpass("ServiceNow Password : ")

    url='https://'+inst+'.service-now.com'
    client = ServiceNowClient(url,(name,password))
    os.system('cls' if os.name == 'nt' else 'clear')

def yesno():
    ans = 0
    answer = None 
    while answer not in ("yes", "no", "n", "y"): 
        answer = input("Enter yes or no: ") 
        if answer == "y" or answer == "yes": 
            ans = 1
            return ans
        elif answer == "n" or answer == "no": 
            ans = 0
            return ans
        else: 
            print("Please enter yes or no.") 

def get_timezone():
    global name
    global client
    global inst
    gr = client.GlideRecord('sys_user')
    queries2=("user_name="+name)
    gr.add_encoded_query(queries2)
    gr.query()
    with Spinner():
        for r in gr:
            print(bcolors.OKGREEN,"Time Zone for " + name + " is set to : ",r.time_zone,bcolors.ENDC)
            time.sleep(2)

def sso_enabled():
    global client
    global inst
    gr = client.GlideRecord('sys_properties')
    querie=("sys_name=glide.authenticate.multisso.debug")
    gr.add_encoded_query(querie)
    gr.query()
    with Spinner():
        for r in gr:
            if r.value == "false":
                print(bcolors.FAIL, "Multi SSO Is not enabled", bcolors.ENDC)
                print(bcolors.OKGREEN, "This tick box is unabled \'Enable multiple provider SSO\':", bcolors.ENDC)
                print(bcolors.OKBLUE,"\n", inst+"/now/nav/ui/classic/params/target/MultiSSOProperties.do",bcolors.ENDC)
                time.sleep(1)
            elif r.value == "true":
                print(bcolors.OKGREEN, "Multi Provider SSO enabled",bcolors.OKGREEN,"✓", bcolors.ENDC)
                time.sleep(1)

def findssologs():
#Read Syslog table for SSO Related logs
## Syslog log types are level=0 'Information', level=1 are 'warning', level=2 = 'Error'
    global client
    global inst
    global name
    global password
    global url
    gr = client.GlideRecord('syslog')
    #query to filter for last 30 minutes - and filter out unwanted system errors.
    gr.add_encoded_query("source=MultiSSOv2^ORsource=SAML2^ORsource=MULTISSO_OIDC_SOURCE^ORsource=com.glide.ui.ServletErrorListener^sys_created_on>javascript:gs.beginningOfLast30Minutes()^messageNOT LIKEThreadPoolExecutor^messageNOT LIKEUADownloader-gcf_download:^messageNOT LIKEPKI^messageNOT LIKEError accessing descriptor^messageNOT LIKECMDBDataManagerScriptable^messageNOT LIKEsn_orchestration_api_v1^messageNOT LIKEUADownloader-table_pkg_override^messageNOT LIKEJava^messageNOT LIKELDAP")
    #limited to 1000 records 
    gr.limit = 1000
    gr.query()
    for r in gr:
            #find error logs they're classed as level = 2
            if r.level=="2":
             
                #find NameID Mismatch error log
                if r.level=="2" and r.source == "com.glide.ui.ServletErrorListener" and r.message.find("Invalid User Field") != -1:
                    
                    print("\n=============Error Found=============")
                    print("Error From syslog :",bcolors.FAIL,r.sys_created_on,r.message,bcolors.ENDC)
                    print(bcolors.OKGREEN, "\nSolution: Compare the nameID response from SAML to the User_field in IDP to identify the mismatch",bcolors.ENDC)
                    for r in gr:
                        if r.message.find('SAML Request xml:<samlp:Response ID') != -1:
                            print (bcolors.OKGREEN,"\nSSO nameID found from SAML Response: ",bcolors.ENDC,re.findall('NameID.*</NameID>', str(r.message)))
                            print(bcolors.BOLD, "Which IDP Is the user attempting to login with? ",bcolors.ENDC)
                            break
                    break
            
            #find information logs they're classed as level=0
            #elif r.level=="0":

def get_idps():
    global client
    gr = client.GlideRecord('sso_properties')

    gr.add_encoded_query("active=true")
    gr.query()
    print(bcolors.BOLD, "\nWhich IDP to select? : ", bcolors.ENDC)
    I = 0
    idpdict={}
    
    for r in gr:
        I = I+1
        print( bcolors.OKGREEN ,I,bcolors.OKBLUE, r.name, bcolors.ENDC)
        idpdict[I] = {'Num': I, 'Name': r.name, 'Active': r.active, 'Sysid': r.sys_id, 'UserF': r.user_field, 'Auto': r.auto_provision, 'ssoscript':r.sso_script}

                
    #User Choice IDP
    op = int(input("Number? : "))
#    print(idpdict[(op)])
    print(bcolors.BOLD," \nSelected : ", bcolors.OKGREEN, idpdict[(op)]['Name'], bcolors.ENDC)
    print("Active            :", bcolors.OKBLUE, idpdict[(op)]['Active'], bcolors.ENDC)
    print("User Field        :", bcolors.OKBLUE, idpdict[(op)]['UserF'], bcolors.ENDC)
    #print("Auto Provisioning :", bcolors.OKBLUE, idpdict[(op)]['Auto'], bcolors.ENDC)
    #print("SSO Login Script  :", bcolors.OKBLUE, idpdict[(op)]['ssoscript'], bcolors.ENDC)

def get_sso_debug():
    
    global client
    gr = client.GlideRecord('sys_properties')
    gr.limit = 1000
    querie=("sys_name=glide.authenticate.multissov2_feature.enabled")
    gr.add_encoded_query(querie)
    gr.query()
    with Spinner():
        for r in gr:
            if r.value == "false":
                print(bcolors.FAIL, "SSO Not Enabled please enable tick box in URL below : ", bcolors.ENDC)
                print(bcolors.OKGREEN, "Please Enable debug logging for the \'multiple provider SSO integration\':", bcolors.ENDC)
                print(bcolors.OKBLUE,"\n", inst+"/now/nav/ui/classic/params/target/MultiSSOProperties.do",bcolors.ENDC)
                print("\n Once debugging SSO is enabled, please perform the test login again through SSO to gather logs. This will take 5-10Mins to reflect within the system logs")
                time.sleep(2)
            elif r.value == "true":
                print(bcolors.OKGREEN, "SSO Debugging enabled",bcolors.OKGREEN,"✓", bcolors.ENDC)
                time.sleep(2)

def get_sso_userfield():
    #glide.authenticate.multisso.login_locate.user_field
    print("create def")

clearscreen()
welcomecomparator()
login()
sso_enabled()
get_sso_debug()
get_timezone()
findssologs()
get_idps()
