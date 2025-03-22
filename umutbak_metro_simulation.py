from collections import deque
from typing import List, Tuple, Optional
import heapq


# bir metro istasyonunu temsil eden sınıf oluşturuyoruz.
class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx             # İstasyonun benzersiz bir kimlik numarası veya kodu.
        self.ad = ad               # İstasyonun adı
        self.hat = hat             # İstasyonun ait olduğu metro hattı (örneğin, "M1", "M2").
        self.komsular = []         # İstasyona bağlı komşu istasyonların listesini tutan bir yapı.

    def komsu_ekle(self, diger_istasyon, sure: int):        #diger_istasyon: Komşu istasyon nesnesi.
                                                            #sure: Mevcut istasyondan komşu istasyona gitme süresi (dakika cinsinden olabilir).
        self.komsular.append((diger_istasyon, sure))        #bir istasyonun hangi istasyonlarla bağlantılı olduğu ve bu bağlantıların ne kadar sürdüğünü saklar.

#Bu sınıf metro sistemindeki istasyonları ve bunların bağlantılarını saklamak için bir graf yapısı oluşturur.
class MetroAgi:
    #istasyon ID'lerini, değer olarak istasyon nesnelerini , metro bağlantısını ve sürelerini sözlük olarak saklar
    def __init__(self):
        self.istasyonlar = {}  # İstasyon ID'leri ve nesneleri
        self.baglanti = {}  # Bağlantılar ve süreler

    #Eğer aynı ID'ye sahip bir istasyon zaten varsa, uyarı vererek işlemi iptal eder.
    def istasyon_ekle(self, istasyon_id, ad, hat):
        if istasyon_id in self.istasyonlar:
            print(f"⚠️ Uyarı: {istasyon_id} zaten mevcut!")
            return

        #Istasyon sınıfından yeni bir nesne oluşturur ve self.istasyonlar sözlüğüne ekler.
        self.istasyonlar[istasyon_id] = Istasyon(istasyon_id, ad, hat)

    #İki istasyon arasına bağlantı ekler (örneğin Kızılay ↔ Ulus).
    def baglanti_ekle(self, istasyon1, istasyon2, sure):
        #Eğer istasyon1 veya istasyon2 daha önce eklenmemişse hata mesajı verir ve işlemi iptal eder.
        if istasyon1 not in self.istasyonlar or istasyon2 not in self.istasyonlar:
            print(f"❌ Hata: {istasyon1} veya {istasyon2} istasyonu bulunamadı!")
            return

        #iki yönlü bağlantının Oluşturulması
        self.istasyonlar[istasyon1].komsu_ekle(self.istasyonlar[istasyon2], sure)
        self.istasyonlar[istasyon2].komsu_ekle(self.istasyonlar[istasyon1], sure)


    #BFS Yİ TANIMLAMA
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        #Eğer başlangıç veya hedef istasyonu metro ağına eklenmemişse, hata mesajı verir ve None döndürerek işlemi sonlandırır.
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            print("❌ Başlangıç veya hedef istasyonu metro ağında bulunmuyor.")
            return None

        #Başlangıç ve hedef istasyon nesnelerini al
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

        #BFS için kuyruk (deque) oluştur
        kuyruk = deque([(baslangic, [baslangic])])  #BFS için kuyruk oluşturulur, başlangıç noktası eklenir.
        ziyaret_edildi = set()                      #Ziyaret edilen istasyonları takip etmek için bir küme oluşturulur.
        ziyaret_edildi.add(baslangic)               #Başlangıç istasyonunu ziyaret_edildi listesine ekleme

        while kuyruk:                                  # Kuyruk boşalana kadar devam eder.
            mevcut_istasyon, rota = kuyruk.popleft()   # Kuyruğun başındaki istasyonu ve rotayı alır.
            if mevcut_istasyon == hedef:               # Hedef istasyona ulaştıysak rotayı döndürür.

                return rota

            # 5. Mevcut istasyonun komşularını kontrol et
            for komsu, _ in mevcut_istasyon.komsular:    # Eğer bu komşu daha önce ziyaret edilmediyse
                if komsu not in ziyaret_edildi:          # Ziyaret edildi olarak işaretle
                    ziyaret_edildi.add(komsu)            # Yeni rotayı oluştur
                    yeni_rota = rota + [komsu]           # Kuyruğa ekle
                    kuyruk.append((komsu, yeni_rota))


        print("❌ Hedef istasyona ulaşan bir yol bulunamadı.")
        return None  # Hiçbir rota bulunamadı


    #A* algoritmasıyla en hızlı rotayı bulma
    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:  #Optional parametresi İstasyon nesnelerinden oluşan bir listeyi (rota) ve süreyi tuple cinsinden döndürür
        # Eğer başlangıç veya hedef istasyonu metro ağına eklenmemişse, hata mesajı verir ve None döndürerek işlemi sonlandırır
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

        baslangic = self.istasyonlar[baslangic_id]   #baslangic değişkeni istasyon nesnesi olarak atanır.
        hedef = self.istasyonlar[hedef_id]           #hedef değişkeni istasyon nesnesi olarak atanır
        ziyaret_edildi = {}                          #Daha önce ziyaret edilen istasyonları ve en kısa sürede ulaşma sürelerini saklayan bir sözlük

        pq = [(0, id(baslangic), baslangic, [baslangic])]
        #(toplam_sure, id(mevcut_istasyon), mevcut_istasyon, rota) seklinde pq da saklanır.
        #toplam_sure: Şu ana kadar geçen toplam süre
        #id(mevcut_istasyon): Heapq öncelik sıralamasında çakışmaları önlemek için istasyonun ID'si
        #mevcut_istasyon: Şu an bulunduğumuz istasyon
        #rota: Şu ana kadar izlenen yol


        #A Algoritmasını Çalıştırma
        while pq:
            toplam_sure, _, mevcut_istasyon, rota = heapq.heappop(pq)   #Heapq (öncelik kuyruğu) en düşük toplam_sure değerine sahip olanı alır.
            if mevcut_istasyon == hedef:                                 #Eğer şu an bulunduğumuz istasyon hedef istasyonsa, bulunan en hızlı rotayı ve toplam süreyi döndür.
                return rota, toplam_sure

            #Eğer bu istasyona daha önce daha kısa sürede ulaşıldıysa, tekrar ziyaret edilmez
            if mevcut_istasyon in ziyaret_edildi and ziyaret_edildi[mevcut_istasyon] <= toplam_sure:
                continue

            #Bu istasyona en kısa sürede nasıl ulaşıldığını kaydediyoruz.
            ziyaret_edildi[mevcut_istasyon] = toplam_sure

            #Komşu İstasyonları Kuyruğa Ekleme
            for komsu, sure in mevcut_istasyon.komsular:
                yeni_sure = toplam_sure + sure
                yeni_rota = rota + [komsu]
                heapq.heappush(pq, (yeni_sure, id(komsu), komsu, yeni_rota))

        print("❌ Hedef istasyona ulaşan bir yol bulunamadı.")
        return None

    #Kullanıcının girdiği istasyon adına karşılık gelen istasyon kimliğini (ID) döndürmek.
    def istasyon_adindan_id_bul(self, ad: str) -> Optional[str]:
        """Girilen istasyon adına karşılık gelen ID'yi bulur (Büyük/küçük harf duyarsız)."""
        ad = ad.strip().lower()  # Kullanıcıdan alınan addaki boşluklar temizlenir ve küçük harfe dönüştürülür.
        eslesen_istasyonlar = [
            istasyon for istasyon in self.istasyonlar.values() if istasyon.ad.lower() == ad
        ] #Mevcut istasyonlar arasında, kullanıcının girdiği ad ile eşleşen istasyonları bulur.

        if len(eslesen_istasyonlar) == 1:
            return eslesen_istasyonlar[0].idx  # Eğer yalnızca bir eşleşme varsa, onu döndürür.

        elif len(eslesen_istasyonlar) > 1:
            # Eğer birden fazla eşleşme varsa, kullanıcıya seçenekler sunulur.(kızılay ve gar gibi aktarma istasyonları)
            print(
                f"❌ '{ad}' adıyla birden fazla istasyon bulundu. Lütfen hangi istasyonu seçmek istediğinizi belirtin:")
            for i, istasyon in enumerate(eslesen_istasyonlar, start=1):
                print(f"  {i}. {istasyon.ad} ({istasyon.idx})")

            # Kullanıcıdan seçim alma
            while True:                   #Kullanıcı seçim yapana kadar döngü devam eder (while True).
                try:
                    secim = int(input("Seçiminizi yapın (1, 2, ...): "))
                    if 1 <= secim <= len(eslesen_istasyonlar):         #kaç tane eşlesen istasyon varsa o kadar secenek sunar (1,2,3,4....)
                        return eslesen_istasyonlar[secim - 1].idx
                    else:
                        print("❌ Geçersiz seçim. Lütfen listeden geçerli bir seçenek giriniz.")
                except ValueError:
                    print("❌ Lütfen geçerli bir sayı giriniz.")

        # Eğer hiç eşleşme yoksa
        print(f"❌ '{ad}' istasyonu bulunamadı. Mevcut istasyonlar şunlardır:")
        for istasyon in self.istasyonlar.values():
            print(f"  - {istasyon.ad} ({istasyon.idx})")
        return None


#Kullanıcının girdiği başlangıç ve hedef istasyonları arasında en az aktarmalı ve en kısa yolu bulmak
def kullanici_icin_rota_bul(metro: MetroAgi):        #Metro ağı nesnesi (İstasyonlar ve bağlantıları içeren veri yapısı).
    # Başlangıç istasyonunun seçimi
    while True:
        baslangic_ad = input("\nBaşlangıç istasyonu adını girin: ")
        baslangic_id = metro.istasyon_adindan_id_bul(baslangic_ad)
        if baslangic_id:
            break  # Geçerli bir istasyon bulundu, döngüyü sonlandır
        else:
            print(f"❌ '{baslangic_ad}' istasyonu bulunamadı. Lütfen geçerli bir istasyon giriniz.")

    # Hedef istasyonunun seçimi
    while True:
        hedef_ad = input("Hedef istasyonu adını girin: ")
        hedef_id = metro.istasyon_adindan_id_bul(hedef_ad)
        if hedef_id:
            break  # Geçerli bir istasyon bulundu, döngüyü sonlandır
        else:
            print(f"❌ '{hedef_ad}' istasyonu bulunamadı. Lütfen geçerli bir istasyon giriniz.")

    # Seçilen istasyonlar ile rotayı hesaplamak
    print("\n🔍 En az aktarmalı rota hesaplanıyor...")
    rota = metro.en_az_aktarma_bul(baslangic_id, hedef_id)   #BFS kullanarak en az aktarmalı rotayı buluyor
    if rota:
        print("✅ En az aktarmalı rota:", " -> ".join(f"{i.ad} , {i.idx})" for i in rota))
    else:
        print("❌ En az aktarmalı rota bulunamadı.")

    print("\n⏳ En hızlı rota hesaplanıyor...")
    sonuc = metro.en_hizli_rota_bul(baslangic_id, hedef_id)    #A* kullanarak en kısa süreli rotayı buluyor
    if sonuc:
        rota, sure = sonuc
        print(f"✅ En hızlı rota ({sure} dakika):", " -> ".join(f"{i.ad} , {i.idx})" for i in rota))
    else:
        print("❌ En hızlı rota bulunamadı.")

if __name__ == "__main__":     #Bu ifade, Python programlarının ana giriş noktası olarak kullanılır.
                               # Amacı, bir Python dosyasının doğrudan çalıştırıldığında mı yoksa başka bir modüle dahil edildiğinde mi olduğunu belirlemektir.


    metro = MetroAgi()      # Metro ağı için bir nesne (MetroAgi) oluşturur.
                            # Bu nesne, istasyonları ve bağlantıları tutacak.

    # İstasyonlar ekleme
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "osb", "Kırmızı Hat")
    metro.istasyon_ekle("M1", "aşti", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
                               
    # Bağlantılar ekleme
    metro.baglanti_ekle("K1", "K2", 4)
    metro.baglanti_ekle("K2", "K3", 6)
    metro.baglanti_ekle("K3", "K4", 8)
    metro.baglanti_ekle("M1", "M2", 5)
    metro.baglanti_ekle("M2", "M3", 3)
    metro.baglanti_ekle("M3", "M4", 4)
    metro.baglanti_ekle("T1", "T2", 7)
    metro.baglanti_ekle("T2", "T3", 9)
    metro.baglanti_ekle("T3", "T4", 5)
    metro.baglanti_ekle("K1", "M2", 2)
    metro.baglanti_ekle("K3", "T2", 3)
    metro.baglanti_ekle("M4", "T3", 2)

    # Kullanıcıdan rota hesaplama isteği
    kullanici_icin_rota_bul(metro)
