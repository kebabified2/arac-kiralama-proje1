# Araç Kiralama Sistemi

Basit, tek‐dosyalık bir Python + Tkinter projesi. Araç ekleme, müşteri ekleme, kiralama/teslim alma ve araç sorgulama işlevlerini içerir.

---
## Kurulum
```bash
# 1) Repoyu klonlayın
cd Desktop
git clone https://github.com/kebabified2/arac-kiralama-proje1/edit/main/README.md

# 2) Çalıştır
python arac_kiralama_gui.py
```
> Tkinter, Python’ın standart kütüphanesindedir; ek bağımlılık yoktur.

---
## Dosya Yapısı
| Dosya               | Açıklama |
|--------------------|----------|
| `arac_kiralama.py` | İş mantığı: araç, müşteri ve kiralama sınıfları |
| `arac_kiralama_gui.py`           | Tkinter arayüzü (butonlar & listeler) |

---
## Kullanım
Uygulama açıldığında iki liste ve sağda butonlar görürsünüz.

| Buton       | İşlev |
|-------------|-------|
| **Araç Ekle**   | ID & model girerek araç ekler |
| **Müşteri Ekle** | ID, ad, soyad girerek müşteri ekler |
| **Kirala**      | Soldan araç, sağdan müşteri seç → kiralar |
| **Teslim Al**    | Aynı seçimle kiralamayı sonlandırır |
| **Sorgu**       | Sadece araç seç; kiralayanı veya “müsait” durumunu gösterir |
| **Çıkış**       | Programı kapatır |

> Listelerde mavi satır seçili demektir. **Kirala/Teslim Al** için iki seçim gerekir; **Sorgu** sadece araç seçimine bakar.

# Ekstra
* Pickle aracılığıyla kaydetme özelliği mevcuttur.

---
## Lisans
MIT

