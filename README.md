Kamera Hareketi Tespit Sistemi
ATP Core Talent 2025 Yarışması için Gelişmiş Bilgisayarla Görü Sistem Çözümü

📋 Genel Bakış
Bu proje, sahnedeki nesne hareketlerinden kameranın kendine ait önemli hareketlerini (pan, tilt, kayma gibi) ayırt edebilen gelişmiş bir kamera hareketi algılama sistemi sunar. Sistem, birden fazla bilgisayarla görme algoritmasını birlikte kullanarak sağlam ve doğru tespit sağlar.
![Ekran görüntüsü 2025-06-26 171038](https://github.com/user-attachments/assets/ea700f53-1af9-4d47-a716-c1aa30684f1d)
Sistem hem video dosyaları hem de görsel dizileri ile çalışabilir:

🎞️ Video Desteği: .mp4, .avi, .mov, .webm gibi yaygın video formatları desteklenir. Yüklenen video otomatik olarak karelere ayrılır ve analiz edilir.

🖼️ Görsel Dizisi: Zaman sıralı .jpg, .png gibi görseller yüklenerek analiz gerçekleştirilebilir.

Kullanıcı arayüzünde bu medya dosyaları kolayca sürüklenip bırakılarak sisteme aktarılabilir. Arayüz, yükleme sonrası önizleme ve detaylı analiz sonuçlarını da sunar.
![foto2](https://github.com/user-attachments/assets/94826c8a-8f55-421a-b40f-5c7ce15bd561)

Yukarıdaki ekran görüntüsü, bu işlevin canlı bir örneğini sunar. Kullanıcı bir video yükledikten sonra:
Uygulama videoyu karelere böler, her karede kamera hareketi olup olmadığını analiz eder, hareket tespit edilen kareleri işaretler, kullanıcının seçtiği algoritmaya göre analiz detaylarını gösterir.

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

## 🚀 **Getting Started**

### **Prerequisites**

- Python 3.8 or higher
- pip package manager

### **Başlarken**

1. **Depoyu klonlayın:**

```bash
git clone <your-repo-url>
cd camera-movement-detection
```

2. **Bağımlılıkları yükleyin:**

```bash
pip install -r requirements.txt
```

3. **Uygulamayı çalıştırın:**

```bash
streamlit run app.py
```

4. **Tarayıcınızı açın:**
   Navigate to `http://localhost:8501`

