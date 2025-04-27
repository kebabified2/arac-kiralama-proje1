from datetime import datetime
import os
import pickle

DATA_FILE = "kiralama.dat"  # kayıt dosyası


class Arac:
    """Araç temel modeli"""

    def __init__(self, arac_id: int, model: str):
        self.arac_id = arac_id
        self.model = model
        self.kiralama_durumu = False  # False = müsait, True = kirada

    def arac_durumu_guncelle(self, durum: bool):
        self.kiralama_durumu = durum

    def __repr__(self):
        durum = "Kirada" if self.kiralama_durumu else "Müsait"
        return f"<Arac {self.arac_id} {self.model} ({durum})>"


class Musteri:
    """Müşteri temel modeli"""

    def __init__(self, musteri_id: int, ad: str, soyad: str):
        self.musteri_id = musteri_id
        self.ad = ad
        self.soyad = soyad
        self.kiraladigi_araclar: list[int] = []

    def __repr__(self):
        return f"<Musteri {self.musteri_id} {self.ad} {self.soyad}>"


class Kiralama:
    """Kiralama işlemlerini yöneten sınıf
    save/load ile diske yazılır – pickle basitliği yeterlidir.
    """

    def __init__(self):
        self.araclar: dict[int, Arac] = {}
        self.musteriler: dict[int, Musteri] = {}
        self.kiralamalar: list[dict] = []

    # ---------- Kalıcı depolama ----------
    def save(self, path: str = DATA_FILE):
        """Nesneyi pickle ile diske yazar"""
        with open(path, "wb") as fh:
            pickle.dump(self, fh)

    @classmethod
    def load(cls, path: str = DATA_FILE):
        """Dosya varsa oku, yoksa boş sistem döndür"""
        if os.path.exists(path):
            with open(path, "rb") as fh:
                obj = pickle.load(fh)
                # sınıf adımız değişmediyse güvenli—yine de tip kontrolü yapalım
                if isinstance(obj, cls):
                    return obj
        return cls()

    # ---------- Kayıt yöntemleri ----------
    def arac_ekle(self, arac_id: int, model: str):
        if arac_id in self.araclar:
            raise ValueError("Bu araç ID zaten mevcut.")
        self.araclar[arac_id] = Arac(arac_id, model)

    def musteri_ekle(self, musteri_id: int, ad: str, soyad: str):
        if musteri_id in self.musteriler:
            raise ValueError("Bu müşteri ID zaten mevcut.")
        self.musteriler[musteri_id] = Musteri(musteri_id, ad, soyad)

    # ---------- İşlem yöntemleri ----------
    def kiralama_yap(self, musteri_id: int, arac_id: int):
        if musteri_id not in self.musteriler:
            raise KeyError("Müşteri bulunamadı.")
        if arac_id not in self.araclar:
            raise KeyError("Araç bulunamadı.")

        musteri = self.musteriler[musteri_id]
        arac = self.araclar[arac_id]
        if arac.kiralama_durumu:
            raise RuntimeError("Araç zaten kirada.")

        arac.arac_durumu_guncelle(True)
        musteri.kiraladigi_araclar.append(arac_id)
        self.kiralamalar.append({
            "musteri_id": musteri_id,
            "arac_id": arac_id,
            "baslangic": datetime.now(),
            "bitis": None
        })

    def kiralama_iptal_et(self, musteri_id: int, arac_id: int):
        arac = self.araclar.get(arac_id)
        musteri = self.musteriler.get(musteri_id)
        if not arac or not musteri:
            raise KeyError("Müşteri veya araç bulunamadı.")

        aktif = next((k for k in self.kiralamalar
                      if k["musteri_id"] == musteri_id and
                         k["arac_id"] == arac_id and
                         k["bitis"] is None), None)
        if not aktif:
            raise RuntimeError("Aktif kiralama bulunamadı.")

        arac.arac_durumu_guncelle(False)
        musteri.kiraladigi_araclar.remove(arac_id)
        aktif["bitis"] = datetime.now()

    def kiralama_bilgisi(self):
        return [{
            **k,
            "baslangic": k["baslangic"].strftime("%Y-%m-%d %H:%M:%S"),
            "bitis": k["bitis"].strftime("%Y-%m-%d %H:%M:%S") if k["bitis"] else None
        } for k in self.kiralamalar]


# ---------- Hızlı test ----------
if __name__ == "__main__":
    # daha önceki durumu yükle
    sistem = Kiralama.load()

    # test eklemeler
    if not sistem.araclar:
        sistem.arac_ekle(1, "Toyota Corolla")
        sistem.musteri_ekle(100, "Ahmet", "Yılmaz")
        sistem.kiralama_yap(100, 1)

    print("Kiralamalar:", sistem.kiralama_bilgisi())

    # çıkışta kaydet
    sistem.save()
