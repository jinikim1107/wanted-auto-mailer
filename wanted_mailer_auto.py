import smtplib
import json
import os
import sys
from email.mime.text import MIMEText
from datetime import datetime

def send_notification_email():
    try:
        # 1단계: GitHub Secrets에서 SMTP 정보 가져오기
        smtp_server = os.environ.get('SMTP_SERVER')
        smtp_port = int(os.environ.get('SMTP_PORT'))
        sender_email = os.environ.get('SMTP_USERNAME')
        sender_password = os.environ.get('SMTP_PASSWORD')

        if not all([smtp_server, smtp_port, sender_email, sender_password]):
            raise ValueError("SMTP 설정에 필요한 Secret 값이 하나 이상 없습니다.")

        # 2단계: config.json 파일 읽기
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)

        recipient_email = config['email']
        location = ', '.join(config['location'])
        year = config['year']
        jobs = ', '.join(config['jobs'])

        # 3단계: 이메일 내용 생성
        subject = f"🚀 [{location}] 지역 채용 정보 자동화 알림"
        body = f"""안녕하세요. 요청하신 채용 정보 자동화 알림입니다.
- 검색 지역: {location}
- 요구 경력: {year}년 이상
- 관심 직무: {jobs}
"""
        
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # 4단계: 이메일 발송
        print("SMTP 서버에 연결하여 로그인을 시도합니다...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        print(f"✅ 메일 발송 성공: {recipient_email}")

    except Exception as e:
        # 🚨 여기가 핵심! 오류 발생 시 워크플로우를 '실패' 처리합니다.
        print("❌ 이메일 발송 중 오류가 발생했습니다.")
        print("---!!! 진짜 오류 메시지 !!!---")
        print(e)
        print("---------------------------")
        sys.exit(1) # 워크플로우를 강제로 실패시킴

if __name__ == "__main__":
    send_notification_email()


