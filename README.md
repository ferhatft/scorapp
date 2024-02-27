# Scor Rapor Uygulaması

Bu Django tabanlı proje, bakım raporları oluşturmayı ve yönetmeyi amaçlamaktadır. Ayrıca kullanıcı yetkilendirme, kullanıcı kaydı, şifre sıfırlama gibi temel kullanıcı yönetimi işlevlerini de içerir.

## Özellikler

- Kullanıcı kaydı oluşturma ve oturum açma işlevleri.
- Bakım raporlarını oluşturma, düzenleme ve onaylama yetenekleri.
- Parça kodu görüntüleme ve envanter listesi gibi envanter yönetimi işlevleri.
- Raporların e-posta ile gönderilmesi özelliği.
- Raporların görüntülenmesi ve düzenlenmesi için özel izinler.

## Başlarken

1. Projeyi bilgisayarınıza klonlayın.
2. Sanal bir ortam oluşturun ve bağımlılıkları yüklemek için `pip install -r requirements.txt` komutunu çalıştırın.
3. Veritabanını oluşturmak için `python manage.py migrate` komutunu çalıştırın.
4. Yönetici kullanıcı oluşturmak için `python manage.py createsuperuser` komutunu çalıştırın.
5. Sunucuyu başlatmak için `python manage.py runserver` komutunu çalıştırın.
6. Tarayıcınızda `http://localhost:8000` adresine giderek uygulamayı görüntüleyebilirsiniz.
