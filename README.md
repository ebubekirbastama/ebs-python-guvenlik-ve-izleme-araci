🛡️ EBS Python Güvenlik ve İzleme Aracı

Bu proje, Windows işletim sisteminde çalışan kullanıcıların sistemlerini daha güvenli hale getirmelerine ve işlem, dosya, servis gibi öğeleri daha kolay denetlemelerine yardımcı olmak için geliştirilmiş bir Python uygulamasıdır. Arayüzde `customtkinter` kütüphanesi kullanılmıştır ve PowerShell komutları aracılığıyla sistemsel işlemler yapılır.

📦 Proje GitHub Sayfası:
https://github.com/ebubekirbastama/ebs-python-guvenlik-ve-izleme-araci

<hr>

![EBS](https://raw.githubusercontent.com/ebubekirbastama/ebs-python-guvenlik-ve-izleme-araci/refs/heads/main/ebs%20g%C3%BCvenlik%20tool.png)

🚀 Özellikler:
-------------

🗂️ Genel Sekme:
- Gizli dosyaları listeleme
- Silinemeyen dosyaların sistem/gizli/salt-okunur niteliklerini kaldırma

⚙️ Process Sekmesi:
- Aktif işlemleri listeleme
- İşlem yolu bulma
- PID ile işlem sonlandırma
- Dosya hash (MD5) hesaplama

🚀 Başlangıç Sekmesi:
- Kullanıcı başlangıç kayıtlarını görüntüleme
- Görev zamanlayıcısındaki görevleri listeleme ya da göreve göre arama

🔍 Taramalar Sekmesi:
- Belirtilen klasördeki tüm dosyaları listeleme
- Sistem servislerini görüntüleme

🔧 Otomatik Kurulum:
--------------------
Gerekli paketler, proje ilk çalıştırıldığında sistemde yoksa otomatik olarak yüklenir. Bu sayede kullanıcılar ek işlem yapmadan doğrudan programı çalıştırabilirler.

Alternatif olarak aşağıdaki komutla da yükleyebilirsiniz:

pip install -r requirements.txt

📁 Kurulum:
-----------

1. Projeyi klonlayın:
git clone https://github.com/ebubekirbastama/ebs-python-guvenlik-ve-izleme-araci.git
cd ebs-python-guvenlik-ve-izleme-araci

2. Gerekli modülleri yükleyin (otomatik de yapılır ama manuel isterseniz):
pip install customtkinter

3. Uygulamayı çalıştırın:
python app.py

📄 Lisans:
----------
Bu proje MIT Lisansı ile lisanslanmıştır.

MIT License

Copyright (c) 2025 Ebubekir Bastama

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
