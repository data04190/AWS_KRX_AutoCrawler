# EC2 Setting

<br>

- AWS CLI 설치

```shell
$ curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
$ unzip awscliv2.zip
$ sudo ./aws/install
```

- AWS EC2 인스턴스 내 파일을 S3 파일 업로드
```shell
$ aws s3 cp [source파일명] s3://[destination버킷명]/[destination파일명] 
```

- AWS EC2 인스턴스 내 파일을 S3 파일 다운로드
```
$ aws s3 cp s3://[source버킷명]/[source파일명] [destination파일명] 
```

<hr>

- EC2 시간대 한국 시간으로 변경
```shell
$ sudo timedatectl set-timezone Asia/Seoul  #Asia/Seoul 기준으로 시간 변경.
$ date    #변경된 시간 확인
```

- sh 스크립트의 권한 변경
```shell
$ chmod 755 [filename].sh
```

- cronbtab -e 설정
```shell
SHELL = /bin/bash
PATH = [$PATH]

30 23 * * 1,2,3,4,5 /home/ubuntu/crawling_fullcode.sh   #평일 23:30분에 fullcode_update.py 실행 후 s3 자동 업로드
```


