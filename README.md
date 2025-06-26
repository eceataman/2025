Kamera Hareketi Tespit Sistemi
ATP Core Talent 2025 Yarışması için Gelişmiş Bilgisayarla Görü Sistem Çözümü

📋 Genel Bakış
Bu proje, sahnedeki nesne hareketlerinden kameranın kendine ait önemli hareketlerini (pan, tilt, kayma gibi) ayırt edebilen gelişmiş bir kamera hareketi algılama sistemi sunar. Sistem, birden fazla bilgisayarla görme algoritmasını birlikte kullanarak sağlam ve doğru tespit sağlar.
![Ekran görüntüsü 2025-06-26 171038](https://github.com/user-attachments/assets/ea700f53-1af9-4d47-a716-c1aa30684f1d)


🎯 Öne Çıkan Özellikler
Çoklu Algoritma Kullanımı: ORB eşleşmesi, optik akış ve kare farkı yöntemleri

Video ve Görsel Desteği: MP4, AVI, MOV, WebM videolar ve JPG, PNG görsel dizileri

Gerçek Zamanlı Analiz: Etkileşimli web arayüzü ve güven skorları

Kamera vs Nesne Hareketi Ayırımı: Gelişmiş algoritmalar ile ayrım

Güçlü Performans: RANSAC ile aykırı değer temizliği, algoritma birleştirme

🔬 Teknik Yaklaşım

1. Özellik Eşleme Algoritması (Ana Yöntem)
   ORB Anahtar Nokta Algılama: Her karede 1000’e kadar özellik noktası çıkarır

Brute Force Eşleşme: Hamming mesafesiyle çapraz eşleşme

RANSAC Homografi: Kamera dönüşümünü tahmin eder, aykırıları eler

Dönüşüm Analizi: Homografiyi çeviri, döndürme ve ölçeklemeye ayırır

python
Kopyala
Düzenle

# Kamera hareketi için eşik değerler:

- Çeviri: > 20 piksel
- Dönme: > 5 derece
- Ölçek değişimi: > %10

2. Optik Akış Algoritması (İkincil)
   Lucas-Kanade Takibi: Piramit tabanlı akış izleme

Global Hareket Analizi: Baskın hareket yönünü tespit eder

Hareket Tutarlılığı: Vektör hizasını ölçer

3. Kare Farkı Yöntemi (Yedekleme)
   Gelişmiş Piksel Farkı: Önemli piksel yüzdesiyle kombine skor

Performans Optimizasyonu: Büyük görüntülerde otomatik yeniden boyutlandırma

4. Algoritma Birleştirme (Fusion)
   Sonuçlar ağırlıklı oylama ile birleştirilir:

Özellik Eşleme: 1.5x ağırlık (öncelikli)

Optik Akış: 1.2x ağırlık (orta öncelik)

Kare Farkı: 1.0x ağırlık (yedek yöntem)

🚀 Başlarken
Gereksinimler
Python 3.8 veya üstü

pip paket yöneticisi

Kurulum
Projeyi klonlayın:

bash
Kopyala
Düzenle
git clone <repo-linkinizi-yapıştırın>
cd camera-movement-detection
Gerekli kütüphaneleri yükleyin:

bash
Kopyala
Düzenle
pip install -r requirements.txt
Uygulamayı başlatın:

bash
Kopyala
Düzenle
streamlit run app.py
Tarayıcıyı açın:
http://localhost:8501 adresine gidin

💻 Kullanım Rehberi
Girdi Seçenekleri
📁 Video Dosyası
Desteklenen formatlar: MP4, AVI, MOV, MKV, WebM

Otomatik kare çıkarımı (maks. 100 kare)

Gerçek zamanlı video bilgisi gösterimi

🖼️ Görsel Dizisi
Destek: JPG, JPEG, PNG, BMP, TIFF

Birden fazla görseli sıralı şekilde yükleyin

RGBA → RGB dönüşümü otomatik yapılır

Algılama Yöntemleri
Otomatik Mod (Tavsiye Edilen): Tüm algoritmaları birleştirerek en iyi sonucu verir

Özellik Eşleme: ORB + RANSAC homografi

Optik Akış: Lucas-Kanade hareket takibi

Kare Farkı: Piksel tabanlı basit algılama

Ayarlar
Eşik (Threshold): Hassasiyet kontrolü (10–200, varsayılan: 50)

Yöntem Seçimi: Algoritma belirleme

Detaylı Analiz: Kare bazında güven skoru gösterimi

🧠 Algoritma Detayları
Kamera vs Nesne Hareketi
Ayrımı şu yollarla yapar:

Global Hareket Tutarlılığı: Kamera hareketi tüm kareyi etkiler

Özellik Noktası Dağılımı: Kamera hareketi noktalarda tutarlı dönüşüm oluşturur

Homografi Analizi: Anlamlı homografi sadece kamera hareketinde çıkar

Hareket Vektörü Hizası: Kamera hareketi hizalı vektörler üretir

Performans Özellikleri
Algoritma Doğruluk Hız Yanlış Pozitif En İyi Kullanım
Özellik Eşleme Yüksek Orta Düşük Doku içeren sahneler
Optik Akış Orta Hızlı Orta Hareket takibi
Kare Farkı Düşük Çok Hızlı Yüksek Yedekleme amaçlı

🔧 Zorluklar ve Çözümler
🔸 1. Büyük Nesnelerden Yanlış Pozitifler
✔ Çözüm: Global hareket analizi + homografi geçerliliği ile ayrım yapıldı

🔸 2. Işık Değişiklikleri
✔ Çözüm: Piksel yerine ORB gibi özellik tabanlı yöntemler kullanıldı

🔸 3. Yüksek Çözünürlükte Performans Sorunu
✔ Çözüm: Genişliği 640px’e indirerek işlem hızı artırıldı

🔸 4. En İyi Algoritmanın Seçimi
✔ Çözüm: Ağırlıklı algoritma birleştirme sistemi ile en iyi karar otomatik veriliyor

📊 Teknik Özellikler
Gerekli Paketler:
shell
Kopyala
Düzenle
streamlit>=1.28.0 # Web arayüz
opencv-python>=4.8.0 # Görü işleme
numpy>=1.24.0 # Sayısal hesaplama
Pillow>=9.5.0 # Görsel işlemleri
🎯 Sonuçlar ve Örnekler
Algılama Başarı Oranları
Kamera Pan/Tilt: %95+

Kamera Kayma: %90+

Sadece Nesne Hareketi: <%5 yanlış pozitif

Örnek JSON Çıktı:
json
Kopyala
Düzenle
{
"movement_detected": true,
"confidence": 0.87,
"method": "feature_matching",
"details": {
"matches_found": 234,
"inliers": 189,
"inlier_ratio": 0.81,
"translation": 45.2,
"rotation": 12.3,
"scale_change": 0.05
}
}
📁 Proje Yapısı
bash
Kopyala
Düzenle
camera-movement-detection/
├── app.py # Streamlit arayüzü
├── movement_detector.py # Algılama algoritmaları
├── requirements.txt # Gereken kütüphaneler
├── README.md # Bu dökümantasyon
├── LICENSE # Apache 2.0 lisansı
└── sample_video/  
 └── shaking_timed_panning_output.mp4 # Test videosu
🔮 Gelecek Geliştirmeler
GPU Desteği: CUDA ile daha hızlı işlem

3B Hareket Analizi: Kameranın uzayda dönme tespiti

Makine Öğrenmesi: Derin öğrenme ile sınıflandırma

Gerçek Zamanlı İşlem: Anlık kamera görüntüsünü analiz etme
