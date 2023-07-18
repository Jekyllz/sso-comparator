ServiceNow SSO Error finder - to support users without the navigation hassle.
# SSO Comparator!
```

   _____ _____  ____     ______ ____   __  ___ ____   ___     ____   ___   ______ ____   ____ 
  / ___// ___/ / __ \   / ____// __ \ /  |/  // __ \ /   |   / __ \ /   | /_  __// __ \ / __ \
  \__ \ \__ \ / / / /  / /    / / / // /|_/ // /_/ // /| |  / /_/ // /| |  / /  / / / // /_/ /
 ___/ /___/ // /_/ /  / /___ / /_/ // /  / // ____// ___ | / _, _// ___ | / /  / /_/ // _, _/ 
/____//____/ \____/   \____/ \____//_/  /_//_/    /_/  |_|/_/ |_|/_/  |_|/_/   \____//_/ |_|  
                                                                                                                                                        
Automatic SSO Log Scanning!
```
Current Functions below of this program:

* Check sso debugging enabled on instance provided - glide.authenticate.multisso.debug within sys_properties

* Validate provided user timezone for searching logs - returns the sys_user record time_zone

* Read system logs (syslog) and filter out saml logs for errors

* Try to work with error logs to determine filter to validate error with KB error table
https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB0759250

* Read IDP Identity provider table and prompt user for options.


(currently this only determines if the user has NAMEID issues - more to come soon)

Required python modules 
    pysnc -- ServiceNowClient --> An Official ServiceNow Github python package
    Further Docs here: https://servicenow.github.io/PySNC/user/getting_started.html



Install: <br>
    <code>pip install pysnc</code><br>
    <code>git clone </code><br>
    <code>cd sso-comparator</code><br>
    <code>python comparator.py</code>
    

Program is set to search for the last 30 minutes for errors. You can change the Encoded Query just by copying from the servicenow "copy query" option within the trail.
<code>gr.add_encoded_query(source=MultiSSOv2^ORsource=SAML2^ORsource=MULTISSO_OIDC_SOURCE^ORsource=com.glide.ui.ServletErrorListener^sys_created_on>javascript:gs.beginningOfLast30Minutes()^messageNOT LIKEThreadPoolExecutor^messageNOT LIKEUADownloader-gcf_download:^messageNOT LIKEPKI^messageNOT LIKEError accessing descriptor^messageNOT LIKECMDBDataManagerScriptable^messageNOT LIKEsn_orchestration_api_v1^messageNOT LIKEUADownloader-table_pkg_override^messageNOT LIKEJava^messageNOT LIKELDAP")</code>


You can change the search filter from within servicenow instance browser to copy query <br>
<code>gr.add_encoded_query("messageLIKEsso")</code>

![comparatorgif](https://github.com/Jekyllz/sso-comparator/assets/24834166/7d1364a9-2987-445e-8c4c-2cc884e18ae8)



Ktinter is maby a future project at this point as end users will greatly benefit from a GUI interface. And will reach a wider audience. 
The issue is trying to keep Comparator within default built in python modules but this may be impossible to avoid.

SSO Errors to validate from
https://support.servicenow.com/kb?id=kb_article_view&sysparm_article=KB0759250


