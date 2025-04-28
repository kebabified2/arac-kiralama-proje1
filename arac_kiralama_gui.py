import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from arac_kiralama import Kiralama


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Araç Kiralama")
        self.geometry("620x300")
        self.minsize(620, 300)

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TButton", padding=6)
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 11, "bold"))

        self.sys = Kiralama.load()

        # --- Containers ----------------------------------------------------
        frm_lists = ttk.Frame(self)
        frm_lists.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        frm_buttons = ttk.Frame(self)
        frm_buttons.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ns")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Car list ------------------------------------------------------
        ttk.Label(frm_lists, text="Araçlar", style="Header.TLabel").grid(row=0, column=0, sticky="w")
        self.lbx_car = tk.Listbox(frm_lists, height=12, exportselection=False)
        scr_car = ttk.Scrollbar(frm_lists, orient="vertical", command=self.lbx_car.yview)
        self.lbx_car.config(yscrollcommand=scr_car.set)
        self.lbx_car.grid(row=1, column=0, sticky="nsew")
        scr_car.grid(row=1, column=1, sticky="ns", padx=(2, 0))

        # --- Customer list -------------------------------------------------
        ttk.Label(frm_lists, text="Müşteriler", style="Header.TLabel").grid(row=0, column=2, sticky="w", padx=(20, 0))
        self.lbx_cust = tk.Listbox(frm_lists, height=12, exportselection=False)
        scr_cust = ttk.Scrollbar(frm_lists, orient="vertical", command=self.lbx_cust.yview)
        self.lbx_cust.config(yscrollcommand=scr_cust.set)
        self.lbx_cust.grid(row=1, column=2, sticky="nsew", padx=(20, 0))
        scr_cust.grid(row=1, column=3, sticky="ns", padx=(2, 0))

        frm_lists.grid_columnconfigure(0, weight=1)
        frm_lists.grid_columnconfigure(2, weight=1)
        frm_lists.grid_rowconfigure(1, weight=1)

        # --- Buttons -------------------------------------------------------
        btn_cfg = (
            ("Araç Ekle", self.add_car),
            ("Müşteri Ekle", self.add_cust),
            ("Kirala", self.rent),
            ("Teslim Al", self.return_car),
            ("Sorgu", self.query),
            ("Çıkış", self.close),
        )
        for i, (txt, cmd) in enumerate(btn_cfg):
            ttk.Button(frm_buttons, text=txt, command=cmd).grid(row=i, column=0, pady=4, sticky="ew")

        frm_buttons.grid_columnconfigure(0, weight=1)

        self.protocol("WM_DELETE_WINDOW", self.close)
        self.refresh()

    # --- Helpers ----------------------------------------------------------
    def ask_int(self, title):
        val = simpledialog.askstring(title, f"{title} girin:", parent=self)
        return int(val) if val else None

    def ask_str(self, title):
        return simpledialog.askstring(title, f"{title} girin:", parent=self)

    def selected(self, lbx):
        return lbx.get(lbx.curselection()) if lbx.curselection() else None

    def refresh(self):
        self.lbx_car.delete(0, tk.END)
        self.lbx_cust.delete(0, tk.END)
        for a in self.sys.araclar.values():
            s = "(Kirada)" if a.kiralama_durumu else "(Müsait)"
            self.lbx_car.insert(tk.END, f"{a.arac_id} - {a.model} {s}")
        for m in self.sys.musteriler.values():
            self.lbx_cust.insert(tk.END, f"{m.musteri_id} - {m.ad} {m.soyad}")

    def _commit(self):
        self.sys.save()
        self.refresh()

    # --- Actions ----------------------------------------------------------
    def add_car(self):
        i = self.ask_int("Araç ID")
        model = self.ask_str("Model")
        if i is None or not model:
            return
        try:
            self.sys.arac_ekle(i, model)
            self._commit()
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
            self._commit()
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
            self._commit()
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
            self._commit()
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

    def close(self):
        self.sys.save()
        self.destroy()


if __name__ == "__main__":
    App().mainloop()
