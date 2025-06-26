**ATP Core Talent 2025 - Kamera Hareketi Tespit Sistemi**

📋 **Genel Bakış**
Bu proje, sahnedeki nesne hareketlerinden kameranın kendine ait önemli hareketlerini (pan, tilt, kayma gibi) ayırt edebilen gelişmiş bir kamera hareketi algılama sistemi sunar. Sistem, birden fazla bilgisayarla görme algoritmasını birlikte kullanarak sağlam ve doğru tespit sağlar.
![Ekran görüntüsü 2025-06-26 171038](https://github.com/user-attachments/assets/ea700f53-1af9-4d47-a716-c1aa30684f1d)
Sistem hem video dosyaları hem de görsel dizileri ile çalışabilir:

🎞️ Video Desteği: .mp4, .avi, .mov, .webm gibi yaygın video formatları desteklenir. Yüklenen video otomatik olarak karelere ayrılır ve analiz edilir.

🖼️ Görsel Dizisi: Zaman sıralı .jpg, .png gibi görseller yüklenerek analiz gerçekleştirilebilir.

Kullanıcı arayüzünde bu medya dosyaları kolayca sürüklenip bırakılarak sisteme aktarılabilir. Arayüz, yükleme sonrası önizleme ve detaylı analiz sonuçlarını da sunar.
![foto2](https://github.com/user-attachments/assets/94826c8a-8f55-421a-b40f-5c7ce15bd561)

Yukarıdaki ekran görüntüsü, bu işlevin canlı bir örneğini sunar. Kullanıcı bir video yükledikten sonra:
Uygulama videoyu karelere böler, her karede kamera hareketi olup olmadığını analiz eder, hareket tespit edilen kareleri işaretler, kullanıcının seçtiği algoritmaya göre analiz detaylarını gösterir.

🎯 **Öne Çıkan Özellikler**
Çoklu Algoritma Kullanımı: ORB eşleşmesi, optik akış ve kare farkı yöntemleri

Video ve Görsel Desteği: MP4, AVI, MOV, WebM videolar ve JPG, PNG görsel dizileri

Gerçek Zamanlı Analiz: Etkileşimli web arayüzü ve güven skorları

Kamera vs Nesne Hareketi Ayırımı: Gelişmiş algoritmalar ile ayrım

Güçlü Performans: RANSAC ile aykırı değer temizliği, algoritma birleştirme

🔬 **Teknik Yaklaşım**

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

## 🚀 **Başlarken**

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
   **Kullanım Kılavuzu**
Girdi Seçenekleri
📁 Video Dosyaları
Desteklenen formatlar: MP4, AVI, MOV, MKV, WebM

Otomatik kare çıkarımı (performans için en fazla 100 kare)

Gerçek zamanlı video bilgisi gösterimi

🖼️**Görsel Dizileri**
Desteklenen formatlar: JPG, JPEG, PNG, BMP, TIFF

Görselleri kronolojik sırayla yükleyin

Otomatik RGBA'dan RGB'ye dönüşüm

**Tespit Yöntemleri**
Otomatik Mod (Önerilen): En yüksek doğruluk için tüm algoritmaları birleştirir

Özellik Eşleştirme: ORB anahtar noktaları ve homografi kullanır

Optik Akış: Lucas-Kanade akış takibini kullanır

Kare Farkı: Temel piksel tabanlı hareket tespiti

Parametreler
Eşik Değeri (Threshold): Hassasiyet kontrolü (10-200, varsayılan: 50)

Yöntem Seçimi: Kullanılacak tespit algoritmasını belirleyin

Analiz Detayı: Kare bazlı güven skoru görüntülemesi

🧠**Algoritma Detayları**
Kamera Hareketi vs Nesne Hareketi
Sistem, kamera hareketi ile sahnedeki nesne hareketini aşağıdaki şekilde ayırt eder:

Global Hareket Tutarlılığı: Kamera hareketi tüm çerçeveyi homojen şekilde etkiler

Özellik Noktası Dağılımı: Kamera hareketi tüm anahtar noktalar arasında tutarlı dönüşüm gösterir

Homografi Analizi: Geçerli kamera hareketi anlamlı homografi matrisleri üretir

Hareket Vektörü Hizalaması: Kamera hareketi hizalanmış hareket vektörleri oluşturur

📊 **Teknik Özellikler**
Bağımlılıklar
streamlit>=1.28.0    # Web arayüzü
opencv-python>=4.8.0 # Görüntü işleme
numpy>=1.24.0        # Sayısal hesaplama
Pillow>=9.5.0        # Görsel işleme


