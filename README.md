# Konveyör Sıralı Çalışma

Beckhoff TwinCAT 3 üzerinde başlatma, durdurma, ürün sensörü ve parti sayacı
mantığını öğreten küçük bir endüstriyel otomasyon projesi. Aynı kontrol mantığı
Python simülasyonuyla donanım olmadan denenebilir.

> Bu proje eğitim ve simülasyon amaçlıdır.

## Neler öğreneceksiniz?

- Başlat/durdur kilitlemesi kurma
- `R_TRIG` ile sensörün yükselen kenarını yakalama
- Ürünleri yalnızca konveyör çalışırken sayma
- Parti hedefine ulaşınca konveyörü kontrollü durdurma
- PLC mantığını Python testleriyle doğrulama

## Hızlı başlangıç

Python 3.11 veya daha yeni bir sürümle:

```bash
python3 src/main.py
python3 -m unittest discover -s tests -v
```

Örnek çıktı:

```text
Konveyör başlatıldı.
Ürün algılandı: 1/5
Ürün algılandı: 2/5
Ürün algılandı: 3/5
Ürün algılandı: 4/5
Ürün algılandı: 5/5
Parti tamamlandı, konveyör durdu.
```

## TwinCAT 3'e aktarma

1. TwinCAT XAE içinde **TwinCAT Project → Add New Item → Standard PLC Project**
   ile bir PLC projesi oluşturun.
2. `PLC` altındaki `MAIN` programını açın.
3. [`plc/MAIN.st`](plc/MAIN.st) içeriğini `MAIN` programına aktarın.
4. Projeyi derleyin ve simülasyon hedefinde oturum açın.
5. `bStart`, `bStop`, `bProductSensor` ve `bResetCount` değişkenlerini Watch
   penceresinden değiştirerek senaryoyu gözlemleyin.

Beckhoff'un resmî başlangıç rehberi:
[TwinCAT 3 PLC tanıtımı](https://infosys.beckhoff.com/content/1033/tc3_system/2525041803.html)

## Değişkenler

| Değişken | Tür | Yön | Açıklama |
|---|---|---|---|
| `bStart` | `BOOL` | Giriş | Konveyörü başlatır |
| `bStop` | `BOOL` | Giriş | Konveyörü öncelikli olarak durdurur |
| `bProductSensor` | `BOOL` | Giriş | Ürün algılama sensörünün sembolik değeri |
| `bResetCount` | `BOOL` | Giriş | Konveyör duruyken sayacı sıfırlar |
| `bMotor` | `BOOL` | Çıkış | Konveyör motor komutu |
| `bRunning` | `BOOL` | Durum | Sıralı kontrolün çalışma durumu |
| `nProductCount` | `UINT` | Durum | Sayılan ürün adedi |
| `nBatchTarget` | `UINT` | Ayar | Partide istenen ürün sayısı |
| `bBatchComplete` | `BOOL` | Çıkış | Parti hedefinin tamamlandığını bildirir |

Değişkenler semboliktir; örnekte doğrudan fiziksel I/O adresi kullanılmaz.

## Öğrenci deneyleri

1. `nBatchTarget` değerini 5, 10 ve 20 yaparak durma anını karşılaştırın.
2. Konveyör duruyken sensörü tetikleyin ve sayacın değişmediğini doğrulayın.
3. Sensörü uzun süre `TRUE` tutun; `R_TRIG` sayesinde yalnızca bir ürün
   sayıldığını gözlemleyin.
4. Parti tamamlandıktan sonra yeniden başlatma ve sıfırlama sırasını deneyin.
5. Bir sıkışma sensörü ve zaman aşımı alarmı ekleyerek projeyi geliştirin.

## Güvenlik ve sınırlamalar

Bu örnek gerçek bir makinenin emniyet fonksiyonu değildir. Fiziksel konveyörde
kullanılmadan önce risk analizi, acil duruş ve koruyucu donanım doğrulaması,
elektriksel kilitlemeler, saha testleri ve yetkin uzman incelemesi gerekir.
Standart PLC kodu sertifikalı emniyet PLC'sinin veya emniyet rölesinin yerine
geçmez.

Python simülasyonu gerçek zaman davranışını, EtherCAT haberleşmesini, motor
sürücüsünü ve fiziksel sensör arızalarını modellemez.

## Lisans

MIT
