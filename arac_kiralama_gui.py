import tkinter as tk
from tkinter import simpledialog, messagebox
from arac_kiralama import Kiralama


class App(tk.Tk):
    """Minimum arayüz – temel işlevler korunur."""

    def __init__(self):
        super().__init__()
        self.title("Araç Kiralama")
        self.geometry("500x220")
        self.resizable(False, False)
        self.sys = Kiralama()

        # Listeler
        self.lbx_car = tk.Listbox(self, width=40, exportselection=False)
        self.lbx_cust = tk.Listbox(self, width=25, exportselection=False)
        self.lbx_car.grid(row=0, column=0, rowspan=6, padx=5, pady=5)
        self.lbx_cust.grid(row=0, column=1, rowspan=6, padx=5, pady=5)

        # Butonlar
        btn_titles = (
            ("Araç Ekle", self.add_car),
            ("Müşteri Ekle", self.add_cust),
            ("Kirala", self.rent),
            ("Teslim Al", self.return_car),
            ("Sorgu", self.query),
            ("Çıkış", self.destroy),
        )
        for i, (txt, cmd) in enumerate(btn_titles):
            tk.Button(self, text=txt, command=cmd).grid(row=i, column=2, pady=3)

        self.refresh()

    # ------ Yardımcılar ------
    def ask_int(self, title):
        val = simpledialog.askstring(title, f"{title} girin:", parent=self)
        return int(val) if val else None

    def ask_str(self, title):
        return simpledialog.askstring(title, f"{title} girin:", parent=self)

    def selected(self, lbx: tk.Listbox):
        return lbx.get(lbx.curselection()) if lbx.curselection() else None

    def refresh(self):
        self.lbx_car.delete(0, tk.END)
        self.lbx_cust.delete(0, tk.END)
        for a in self.sys.araclar.values():
            s = "(Kirada)" if a.kiralama_durumu else "(Müsait)"
            self.lbx_car.insert(tk.END, f"{a.arac_id} - {a.model} {s}")
        for m in self.sys.musteriler.values():
            self.lbx_cust.insert(tk.END, f"{m.musteri_id} - {m.ad} {m.soyad}")

    # ------ İşlevler ------
    def add_car(self):
        i = self.ask_int("Araç ID")
        model = self.ask_str("Model")
        if i is None or not model:
            return
        try:
            self.sys.arac_ekle(i, model)
            self.refresh()
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def add_cust(self):
        i = self.ask_int("Müşteri ID")
        ad = self.ask_str("Ad")
        soy = self.ask_str("Soyad")
        if i is None or not (ad and soy):
            return
        try:
            self.sys.musteri_ekle(i, ad, soy)
            self.refresh()
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def rent(self):
        car = self.selected(self.lbx_car)
        cust = self.selected(self.lbx_cust)
        if not (car and cust):
            messagebox.showerror("Hata", "Araç ve müşteri seçin")
            return
        try:
            self.sys.kiralama_yap(int(car.split(" - ")[0]), int(cust.split(" - ")[0]))
            self.refresh()
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def return_car(self):
        car = self.selected(self.lbx_car)
        cust = self.selected(self.lbx_cust)
        if not (car and cust):
            messagebox.showerror("Hata", "Araç ve müşteri seçin")
            return
        try:
            self.sys.kiralama_iptal_et(int(cust.split(" - ")[0]), int(car.split(" - ")[0]))
            self.refresh()
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def query(self):
        car = self.selected(self.lbx_car)
        if not car:
            messagebox.showerror("Hata", "Araç seçin")
            return
        a_id = int(car.split(" - ")[0])
        active = next((k for k in self.sys.kiralamalar if k["arac_id"] == a_id and k["bitis"] is None), None)
        if not active:
            messagebox.showinfo("Sorgu", "Bu araç müsait")
            return
        m = self.sys.musteriler[active["musteri_id"]]
        messagebox.showinfo("Sorgu", f"Araç ID {a_id} → {m.ad} {m.soyad} (ID {m.musteri_id})")


if __name__ == "__main__":
    App().mainloop()
