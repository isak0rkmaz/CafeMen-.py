import tkinter as tk
from tkinter import messagebox

# --- Menü Tanımlama ---
MENU = {
    "latte": 150.00,
    "espresso": 120.00,
    "americano": 125.50,
    "capuccino": 125.50,
    "filtre kahve": 80.00,
    "tiramisu": 120.00,
    "cheesecake": 150.00,
    "su": 5.00,
}

class CafePOSApp:
    def __init__(self, master):
        self.master = master
        master.title("☕ Cafe Yazar Kasa Sistemi (Tkinter)")
        master.geometry("800x600") # Pencere boyutunu ayarla
        master.configure(bg="#f5f5dc") # Açık bej arka plan

        # --- Sepet Veri Yapısı ---
        # Format: {"urun_adi": miktar}
        self.sepet = {}

        # Sol Kısım: Menü ve Sepet Listesi
        self.sol_cerceve = tk.Frame(master, padx=10, pady=10, bg="#ffffff", bd=2, relief=tk.GROOVE)
        self.sol_cerceve.pack(side=tk.LEFT, fill=tk.Y)

        # Sağ Kısım: Hesap Özeti ve İşlemler
        self.sag_cerceve = tk.Frame(master, padx=10, pady=10, bg="#e0e0e0", bd=2, relief=tk.RAISED)
        self.sag_cerceve.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 1. Menü Alanı (Scrollable)
        self.menuyu_hazirla()

        # 2. Sepet Görüntüleme Alanı
        self.sepet_liste_etiketi = tk.Label(self.sol_cerceve, text="🛒 Mevcut Sepet", font=("Helvetica", 12, "bold"), bg="#ffffff")
        self.sepet_liste_etiketi.pack(pady=(10, 5))
        
        self.sepet_listesi = tk.Listbox(self.sol_cerceve, width=30, height=10, font=("Courier", 10))
        self.sepet_listesi.pack(pady=5)
        
        # 3. Hesap Özeti Alanı (Sağ Bölüm)
        self.hesap_ozeti_hazirla()
        
        # Başlangıçta sepeti güncelle
        self.sepeti_guncelle_gui()

    def menuyu_hazirla(self):
        """Menüdeki ürünleri buton olarak hazırlar."""
        menu_etiket = tk.Label(self.sol_cerceve, text="☕ Cafe Menüsü", font=("Helvetica", 14, "bold"), bg="#ffffff")
        menu_etiket.pack(pady=5)

        # Menü öğelerini tutacak çerçeve
        menu_cerceve = tk.Frame(self.sol_cerceve, bg="#ffffff")
        menu_cerceve.pack(pady=5, padx=5)

        row = 0
        col = 0
        for urun, fiyat in MENU.items():
            # Buton metni: Ürün Adı (Fiyat TL)
            btn_text = f"{urun.capitalize()}\n({fiyat:.2f} TL)"
            
            # Lambda kullanarak butona tıklandığında ürünü sepete ekleme
            btn = tk.Button(menu_cerceve, 
                            text=btn_text, 
                            command=lambda u=urun: self.sepete_urun_ekle(u),
                            width=15, 
                            height=3, 
                            bg="#add8e6", # Açık mavi
                            font=("Helvetica", 10, "bold"))
            
            btn.grid(row=row, column=col, padx=5, pady=5)
            
            col += 1
            if col > 2: # Her satırda 3 buton
                col = 0
                row += 1

    def hesap_ozeti_hazirla(self):
        """Sağ taraftaki toplam tutar gösterimlerini ve ödeme butonunu hazırlar."""
        
        etiket = tk.Label(self.sag_cerceve, text="💰 HESAP ÖZETİ", font=("Helvetica", 16, "bold"), bg="#e0e0e0", fg="#333333")
        etiket.pack(pady=(10, 20))

        # Toplamlar için değişkenler
        self.kdv_haric_var = tk.StringVar(value="0.00 TL")
        self.kdv_var = tk.StringVar(value="0.00 TL")
        self.genel_toplam_var = tk.StringVar(value="0.00 TL")

        # KDV Hariç
        tk.Label(self.sag_cerceve, text="KDV Hariç Tutar:", font=("Helvetica", 12), bg="#e0e0e0").pack(pady=5)
        tk.Label(self.sag_cerceve, textvariable=self.kdv_haric_var, font=("Helvetica", 14, "bold"), bg="#ffffff", fg="#00008b", width=20).pack(pady=5, padx=20)
        
        # KDV
        tk.Label(self.sag_cerceve, text="KDV (%20):", font=("Helvetica", 12), bg="#e0e0e0").pack(pady=5)
        tk.Label(self.sag_cerceve, textvariable=self.kdv_var, font=("Helvetica", 14, "bold"), bg="#ffffff", fg="#ff4500", width=20).pack(pady=5, padx=20)
        
        # Genel Toplam
        tk.Label(self.sag_cerceve, text="GENEL TOPLAM:", font=("Helvetica", 14), bg="#e0e0e0").pack(pady=(20, 5))
        tk.Label(self.sag_cerceve, textvariable=self.genel_toplam_var, font=("Helvetica", 18, "bold"), bg="#3cb371", fg="white", width=15).pack(pady=5, padx=20)

        # Ödeme Butonu
        tk.Button(self.sag_cerceve, 
                  text="💳 ÖDEME YAP", 
                  command=self.odeme_penceresi_ac,
                  bg="#ffc107", # Sarı
                  fg="#333333",
                  font=("Helvetica", 16, "bold"),
                  width=15, 
                  height=2).pack(pady=30)
        
        # Sepeti Temizle Butonu
        tk.Button(self.sag_cerceve, 
                  text="🗑️ Sepeti Temizle", 
                  command=self.sepeti_temizle,
                  bg="#dc3545", # Kırmızı
                  fg="white",
                  font=("Helvetica", 10)).pack(pady=5)


    def sepete_urun_ekle(self, urun_adi):
        """Seçilen ürünü sepete ekler ve GUI'yi günceller."""
        # Varsayılan olarak 1 adet ekle
        self.sepet[urun_adi] = self.sepet.get(urun_adi, 0) + 1
        messagebox.showinfo("Ürün Eklendi", f"Sepete 1 adet {urun_adi.capitalize()} eklendi.")
        self.sepeti_guncelle_gui()

    def sepeti_guncelle_gui(self):
        """Sepet Listbox'ını ve Hesap Özeti etiketlerini günceller."""
        self.sepet_listesi.delete(0, tk.END) # Listeyi temizle
        toplam_tutar = 0.0

        for urun, miktar in self.sepet.items():
            fiyat = MENU[urun]
            tutar = fiyat * miktar
            toplam_tutar += tutar
            
            # Listbox'a ekle: Ürün - Miktar - Tutar
            self.sepet_listesi.insert(tk.END, f"{urun.capitalize():<12} x{miktar:<3} {tutar:.2f} TL")

        # Toplam tutarları hesapla
        kdv_orani = 0.20
        kdv_tutari = toplam_tutar * kdv_orani
        kdv_haric_tutar = toplam_tutar - kdv_tutari

        # String değişkenleri güncelle
        self.kdv_haric_var.set(f"{kdv_haric_tutar:.2f} TL")
        self.kdv_var.set(f"{kdv_tutari:.2f} TL")
        self.genel_toplam_var.set(f"{toplam_tutar:.2f} TL")
        
        self.toplam_tutar = toplam_tutar # Ödeme için global değişkeni güncelle

    def sepeti_temizle(self):
        """Sepeti sıfırlar ve GUI'yi günceller."""
        if not self.sepet:
            messagebox.showinfo("Uyarı", "Sepet zaten boş.")
            return

        cevap = messagebox.askyesno("Sepeti Temizle", "Sepeti sıfırlamak istediğinizden emin misiniz?")
        if cevap:
            self.sepet.clear()
            self.sepeti_guncelle_gui()
            messagebox.showinfo("Başarılı", "Sepet temizlendi.")

    def odeme_penceresi_ac(self):
        """Ödeme işlemini gerçekleştirmek için yeni bir pencere açar."""
        if self.toplam_tutar == 0.0:
            messagebox.showerror("Hata", "Ödeme yapmak için sepette ürün olmalıdır.")
            return

        # Yeni bir TopLevel penceresi oluştur
        odeme_penceresi = tk.Toplevel(self.master)
        odeme_penceresi.title("Ödeme İşlemi")
        odeme_penceresi.geometry("350x200")
        odeme_penceresi.configure(bg="#f0f0f0")
        
        # Ödenecek tutarı göster
        tk.Label(odeme_penceresi, 
                 text=f"TOPLAM TUTAR: {self.toplam_tutar:.2f} TL", 
                 font=("Helvetica", 14, "bold"), 
                 bg="#f0f0f0", 
                 fg="#006400").pack(pady=10)

        # Müşteri Girişi Alanı
        tk.Label(odeme_penceresi, text="Müşteri Ödemesi (TL):", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=5)
        odenen_tutar_giris = tk.Entry(odeme_penceresi, font=("Helvetica", 12), width=15)
        odenen_tutar_giris.focus_set()
        odenen_tutar_giris.pack(pady=5)

        def odemeyi_gerceklestir():
            """Ödeme butonuna tıklandığında çalışır."""
            try:
                odenen_tutar = float(odenen_tutar_giris.get())
                if odenen_tutar < self.toplam_tutar:
                    messagebox.showerror("Hata", "Ödenen tutar, toplam tutardan az olamaz.")
                    return

                para_ustu = odenen_tutar - self.toplam_tutar
                
                # Başarılı mesajı ve fiş
                messagebox.showinfo("Ödeme Başarılı", 
                                    f"Ödenen: {odenen_tutar:.2f} TL\n"
                                    f"Para Üstü: {para_ustu:.2f} TL\n\n"
                                    "Fiş Yazdırılıyor...")
                
                # İşlem bitti, sepeti sıfırla ve pencereyi kapat
                self.sepet.clear()
                self.sepeti_guncelle_gui()
                odeme_penceresi.destroy()

            except ValueError:
                messagebox.showerror("Hata", "Geçerli bir sayı girin.")
            except Exception as e:
                messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

        # Onay Butonu
        tk.Button(odeme_penceresi, 
                  text="Ödemeyi Onayla", 
                  command=odemeyi_gerceklestir, 
                  bg="#28a745", 
                  fg="white", 
                  font=("Helvetica", 12, "bold")).pack(pady=10)

# --- Uygulamayı Başlatma ---
if __name__ == "__main__":
    root = tk.Tk()
    app = CafePOSApp(root)
    root.mainloop()