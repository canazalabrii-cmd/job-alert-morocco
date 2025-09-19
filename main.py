import requests
from bs4 import BeautifulSoup
import time

# معلومات البوت
BOT_TOKEN = "8289814129:AAGhJL_DjLl104OwK1RsxZ90DiNP6hynqGc"
CHAT_ID = "198842533"

# إرسال رسالة على تيليجرام
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("خطأ في إرسال الرسالة:", e)

# البحث في Indeed
def search_indeed():
    jobs = []
    try:
        url = "https://ma.indeed.com/jobs"
        params = {'q': 'محاسب', 'l': 'الرباط'}
        response = requests.get(url, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for job in soup.find_all('h2', class_='jobTitle')[:5]:
            title_elem = job.find('a')
            if title_elem:
                title = title_elem.get_text(strip=True)
                link = "https://ma.indeed.com" + title_elem.get('href', '#')
                jobs.append(f"📌 <b>{title}</b>\n🔗 <a href='{link}'>عرض الوظيفة</a>\n")
    except Exception as e:
        print("خطأ في Indeed:", e)
    return jobs

# البحث في Emploi.ma
def search_emploi_ma():
    jobs = []
    try:
        url = "https://www.emploi.ma/recherche-jobs-maroc"
        params = {'keyword': 'محاسب', 'location': 'الرباط'}
        response = requests.get(url, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for job in soup.find_all('div', class_='job-title')[:5]:
            title_elem = job.find('a')
            if title_elem:
                title = title_elem.get_text(strip=True)
                link = "https://www.emploi.ma" + title_elem.get('href', '#')
                jobs.append(f"📌 <b>{title}</b>\n🔗 <a href='{link}'>عرض الوظيفة</a>\n")
    except Exception as e:
        print("خطأ في Emploi.ma:", e)
    return jobs

# البرنامج الرئيسي
def job_alert():
    print("جاري البحث عن فرص العمل...")
    indeed_jobs = search_indeed()
    emploi_jobs = search_emploi_ma()
    all_jobs = indeed_jobs + emploi_jobs

    if all_jobs:
        message = "💼 <b>فرص عمل جديدة في مجال المحاسبة:</b>\n\n" + "\n".join(all_jobs)
        send_telegram_message(message)
        print("تم إرسال التنبيهات")
    else:
        send_telegram_message("❌ لا توجد فرص عمل جديدة حالياً.")
        print("لا توجد فرص عمل")

# لتشغيل البرنامج مرة واحدة للاختبار
if __name__ == "__main__":
    job_alert()
