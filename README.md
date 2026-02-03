# WiFi Camera Guard (Python)

Bu proje, WiFi sinyal gücünü (RSSI) izleyip kamera görüntüsünün üzerine durum bilgisini yazan basit bir örnektir.
Gerçek donanım/ortam koşullarında RSSI düşüşleri **engel** veya **mesafe artışı** gibi durumları
kabaca işaret edebilir. Bu nedenle proje, **WiFi dalgalarını algılama** fikrini Python tarafında
örnekler ve kameradan kendinizi görmenizi sağlayacak bir arayüz sunar.

> Not: WiFi sinyalleriyle "görmek" doğrudan mümkün değildir. Bu örnek, **RSSI değişimini** izleyerek
> “engel olabilir” gibi bir uyarı üretir. Daha ileri seviye WiFi görüntüleme (WiFi sensing)
> için özel donanım ve sinyal işleme gerekir.

## Özellikler
- Kamera görüntüsü üzerine RSSI ve “engel olabilir” uyarısı yazar.
- Linux üzerinde `iw` komutu ile RSSI okur.
- `iw` yoksa veya arayüz seçilmezse otomatik **simülasyon** moduna düşer.

## Kurulum

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Çalıştırma

```bash
python -m wifi_camera_guard.app --iface wlan0
```

`--iface` verilmezse simülasyon modu aktif olur.

## İpuçları
- Linux için `iw` paketinin kurulu olması gerekir.
- Kamera erişimi yoksa uygulama hata verip çıkar.

## Klasör Yapısı
```
src/
  wifi_camera_guard/
    app.py
    wifi_reader.py
    overlay.py
```
