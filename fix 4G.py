#$language = "python"
#$interface ="1.0"

username = "viettel"
password = "Viettel123a@"

with open("SRT.txt","r+") as f:
	lines = f.readlines()

	
command_list = ['delete policy-options policy-statement 4G_SERVICE_VRF_EXPORT term NMS_SRT_COMMUNITY',
				'delete policy-options community COMMUNITY_SRT_NMS members 7552:2005',
				'set policy-options policy-statement 4G_SERVICE_VRF_EXPORT term 4G_SRT_COMMUNITY from protocol direct',
				'set policy-options policy-statement 4G_SERVICE_VRF_EXPORT term 4G_SRT_COMMUNITY from protocol static',
				'set policy-options policy-statement 4G_SERVICE_VRF_EXPORT term 4G_SRT_COMMUNITY then local-preference 3000',
				'set policy-options policy-statement 4G_SERVICE_VRF_EXPORT term 4G_SRT_COMMUNITY then community add COMMUNITY_SRT_4G',
				'set policy-options policy-statement 4G_SERVICE_VRF_EXPORT term 4G_SRT_COMMUNITY then accept',
				'set policy-options community COMMUNITY_SRT_4G members 7552:37',
				'set policy-options community COMMUNITY_SRT_4G members 7552:800',
				'set policy-options community COMMUNITY_SRT_4G members 7552:2005',
				'set policy-options community COMMUNITY_SRT_NMS members 7552:2010',
				'rename routing-instances VRF_4G_SERVICE to VRF_4G_Service']

				
				
for line in lines:
	crt.Screen.WaitForString("~]#")
	crt.Screen.Send("ssh " + username + "@" + line + '\r')
	crt.Screen.WaitForString("(yes/no)?",1)
	crt.Screen.Send("yes" + '\r')

	crt.Screen.WaitForString("assword:",1)
	crt.Screen.Send(password + '\r')

	crt.Screen.WaitForString(">")
	crt.Screen.Send("configure" + '\r')

	for command in command_list:
		crt.Screen.WaitForString("#")
		crt.Screen.Send(command  + '\r')

	crt.Screen.WaitForString("#")
	crt.Screen.Send("show | compare | no-more" + '\r')

	crt.Screen.WaitForString("#")
	crt.Screen.Send('commit comment "fix VRF 4G"' + '\r')
	
	crt.Screen.WaitForString("#")
	crt.Screen.Send("exit" + '\r')
	crt.Screen.WaitForString(">")
	crt.Screen.Send("exit" + '\r')