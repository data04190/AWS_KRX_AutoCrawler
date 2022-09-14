

## 한국거래소(KRX) 주가데이터 수집 자동화 시스템 

<br>
<img width=650 alt="image" src="https://user-images.githubusercontent.com/77683645/180650832-b78c339c-ba92-4359-8aff-5ce38cf67f69.png">
<hr>
<br>

### EC2 Instance
 - <b>Amazon Machine Image (AMI)</b> : `Amazon Linux 2 AMI (HVM)`
 - <b>Instance type</b> : `t2.micro`
 - <b>Auto-assign Public IP</b> : This setting should be enabled
 - Only allows the following traffic : 
     + <b>Type</b> : `SSH` 
     + <b>Port</b> : `22`
     + <b>Source</b> : `Your IP address`
 
