## Quản lý chi tiêu App

---

#### Hướng dẫn cài đặt

1. Tạo môi trường ảo: `python -m venv venv`
2. Kích hoạt môi trường ảo: `source venv/bin/activate` | ` source venv/Scripts/activate`
3. Cài đặt packages: `pip install -r requirements.txt`

   -  Export venv to file: `pip freeze > requirements.txt`

4. Chạy dự án: `uvicorn app.main:app --reload`
