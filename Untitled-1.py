"""
Kitap Takip Uygulaması

Amaç: Kitap ekleme, silme, arama, durum güncelleme, sadece okunmamışları listeleme
ve okunan kitapları 1-5 arası puanlama işlevlerini gerçekleştiren konsol uygulaması.
"""

import json
import os

VERI_DOSYASI = "kutuphane_verisi.json"

def kitaplari_yukle():
    print("Kitap Takip Uygulaması Başlatıldı.")
    if not os.path.exists(VERI_DOSYASI):
        return []
    try:
        with open(VERI_DOSYASI, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        print("Veri dosyası okunurken bir hata oluştu.")
        return []

def kitaplari_kaydet(kitaplar):
    try:
        with open(VERI_DOSYASI, "w", encoding="utf-8") as f:
            json.dump(kitaplar, f, ensure_ascii=False, indent=4)
    except:
        print("Veriler kaydedilirken bir hata meydana geldi.")

def kitaplari_listele(kitaplar):
    if not kitaplar:
        print("Kütüphanenizde henüz kitap bulunmuyor.")
        return False
    
    print("\nMevcut Kitaplarınız:")
    for i, k in enumerate(kitaplar, 1):
        durum = "Okundu" if k["okundu"] else "Okunmadı"
        puan = k.get("puan", 0)
        puan_str = f" - Puan: {puan}/5" if puan > 0 else ""
        print(f"{i}. {k['baslik']} ({k['yazar']}) -> [{durum}{puan_str}]")
    return True

def okunmamislari_listele(kitaplar):
    okunmamislar = [k for k in kitaplar if not k["okundu"]]
    if not okunmamislar:
        print("\nOkunmamış kitap bulunmuyor. Tüm kitapları okumuşsunuz!")
        return
    
    print("\nSadece Okunmamış Kitaplar:")
    for i, k in enumerate(okunmamislar, 1):
        print(f"{i}. {k['baslik']} ({k['yazar']})")

def kitap_ekle(kitaplar):
    baslik = input("\nKitap Adı: ").strip()
    yazar = input("Yazarı: ").strip()
    
    if not baslik or not yazar:
        print("Hata: Kitap adı veya yazar alanı boş bırakılamaz.")
        return
        
    kitaplar.append({
        "baslik": baslik,
        "yazar": yazar,
        "okundu": False,
        "puan": 0
    })
    print(f"'{baslik}' başarıyla kütüphaneye eklendi.")
    kitaplari_kaydet(kitaplar)

def durum_guncelle(kitaplar):
    if not kitaplari_listele(kitaplar):
        return
        
    try:
        secim = int(input("\nDurumunu değiştirmek istediğiniz kitap numarası: "))
        if secim < 1 or secim > len(kitaplar):
            print("Geçersiz numara seçtiniz.")
            return
            
        hedef_kitap = kitaplar[secim - 1]
        hedef_kitap["okundu"] = not hedef_kitap["okundu"]
        
        if not hedef_kitap["okundu"]:
            hedef_kitap["puan"] = 0
            
        yeni_durum = "Okundu" if hedef_kitap["okundu"] else "Okunmadı"
        print(f"'{hedef_kitap['baslik']}' durumu '{yeni_durum}' olarak güncellendi.")
        kitaplari_kaydet(kitaplar)
    except ValueError:
        print("Lütfen geçerli bir sayı girin.")

def kitaba_puan_ver(kitaplar):
    # Ana listeden SADECE okundu olanları filtreleyip geçici bir listeye alıyoruz
    okunanlar = [k for k in kitaplar if k["okundu"]]
    
    if not okunanlar:
        print("\nPuan verilebilecek okunan kitap bulunamadı. Önce durum güncelleyin.")
        return
        
    print("\nPuan Verebileceğiniz Okunan Kitaplar:")
    for i, k in enumerate(okunanlar, 1):
        mevcut = f" (Mevcut Puan: {k['puan']}/5)" if k.get("puan", 0) > 0 else ""
        print(f"{i}. {k['baslik']} - {k['yazar']}{mevcut}")
        
    try:
        secim = int(input("\nPuan vermek istediğiniz kitabın numarası: "))
        if secim < 1 or secim > len(okunanlar):
            print("Geçersiz seçim.")
            return
            
        puan = int(input("Puanınız (1-5 arası): "))
        if puan < 1 or puan > 5:
            print("Hata: Puan 1 ile 5 arasında olmalıdır.")
            return
            
        okunanlar[secim - 1]["puan"] = puan
        print(f"Kitaba {puan}/5 puanı verildi.")
        kitaplari_kaydet(kitaplar)
    except ValueError:
        print("Lütfen sadece sayı girin.")

def kitap_ara(kitaplar):
    if not kitaplar:
        print("Kütüphane boş olduğundan arama yapılamaz.")
        return
        
    terim = input("\nAranacak kitap adı veya yazar: ").strip().lower()
    if not terim:
        print("Arama alanı boş bırakılamaz.")
        return
        
    sonuclar = [k for k in kitaplar if terim in k["baslik"].lower() or terim in k["yazar"].lower()]
    
    if not sonuclar:
        print("Aramanızla eşleşen bir kitap bulunamadı.")
        return
        
    print(f"\nBulunan Sonuçlar ({len(sonuclar)} kitap):")
    for k in sonuclar:
        durum = "Okundu" if k["okundu"] else "Okunmadı"
        puan = f" | Puan: {k['puan']}/5" if k.get("puan", 0) > 0 else ""
        print(f"- {k['baslik']} ({k['yazar']}) [{durum}{puan}]")

def kitap_sil(kitaplar):
    if not kitaplari_listele(kitaplar):
        return
        
    try:
        secim = int(input("\nSilmek istediğiniz kitap numarası: "))
        if secim < 1 or secim > len(kitaplar):
            print("Geçersiz numara.")
            return
            
        silinen = kitaplar.pop(secim - 1)
        print(f"'{silinen['baslik']}' kütüphaneden silindi.")
        kitaplari_kaydet(kitaplar)
    except ValueError:
        print("Lütfen bir sayı girin.")

def ana_menu():
    kitaplar = kitaplari_yukle()
    
    while True:
        toplam = len(kitaplar)
        okunan = sum(1 for k in kitaplar if k["okundu"])
        
        print(f"\n--- MENÜ (Toplam Kitap: {toplam} | Okunan: {okunan}) ---")
        print("1. Tüm Kitapları Listele")
        print("2. Sadece Okunmamış Kitapları Listele")
        print("3. Yeni Kitap Ekle")
        print("4. Okundu / Okunmadı Yap")
        print("5. Okunan Kitaba Puan Ver (1-5)")
        print("6. Kitap Ara")
        print("7. Kitap Sil")
        print("8. Çıkış")
        
        secim = input("\nSeçiminiz (1-8): ").strip()
        
        if secim == "1":
            kitaplari_listele(kitaplar)
        elif secim == "2":
            okunmamislari_listele(kitaplar)
        elif secim == "3":
            kitap_ekle(kitaplar)
        elif secim == "4":
            durum_guncelle(kitaplar)
        elif secim == "5":
            kitaba_puan_ver(kitaplar)
        elif secim == "6":
            kitap_ara(kitaplar)
        elif secim == "7":
            kitap_sil(kitaplar)
        elif secim == "8":
            print("Sistemden çıkılıyor. İyi okumalar!")
            break
        else:
            print("Geçersiz seçim, lütfen 1-8 arası bir numara girin.")

if __name__ == "__main__":
    ana_menu()