# ubmetrostation

# 🚇 Metro Station.py

Bu proje, **BFS (Breadth-First Search) ve A* (A-Star) algoritmalarını kullanarak metro hatları arasında en kısa rotayı ve en az aktarmayı bulan bir sistemdir**. Kullanıcılar belirli bir başlangıç ve varış istasyonu girerek **en verimli güzergahı** öğrenebilirler.

---

## 🚀 Kullanılan Kütüphaneler

Bu projede aşağıdaki Python kütüphaneleri kullanılmıştır:

### 🔹 `heapq` Kütüphanesi
heapq, Python'da min-heap (küçükten büyüğe sıralı yığın) ve öncelikli kuyruk oluşturmak için kullanılan bir modüldür. A* algoritması gibi en düşük maliyetli elemanı hızlıca bulmak gereken durumlarda kullanılır.
### 🔹 `collections` Kütüphanesi
collections, Python'un gelişmiş veri yapıları sağlamasına yardımcı olan bir kütüphanedir. BFS algoritmasında **deque** kullanarak verimli FIFO kuyruğu oluşturabiliriz.

## BFS (Genişlik Öncelikli Arama)
bir graf veya ağacın düğümlerini seviyelere göre katman katman ziyaret eden ve en kısa yolu bulmak için kullanılan bir arama algoritmasıdır.

💡 Çalışma Mantığı:
1-Başlangıç düğümünü (istasyon) kuyruğa ekle.
2-Kuyruktaki ilk düğümü çıkar ve ziyaret et.
3-Bu düğümün komşularını (bağlantılı istasyonları) kuyruğa ekle (daha önce eklenmemişse).
4-Kuyruk boşalana kadar 2. ve 3. adımları tekrarla.

   A -- B -- D
   |    |
   C    E -- F

Üstte görülen yol üzerinde algoritmayı çalıştırırsak 
1️⃣ A istasyonundan başla, kuyruğa ekle.                       KUYRUK[A]
2️⃣ A’nın komşularını (B ve C) kuyruğa ekle.                   KUYRUK[B,C]
3️⃣ B'yi ziyaret et, komşularını (D ve E) kuyruğa ekle.        KUYRUK[C,D,E]
4️⃣ C’yi ziyaret et. (Yeni komşusu yok.)                       KUYRUK[D,E]
5️⃣ D’yi ziyaret et. (Yeni komşusu yok.)                       KUYRUK[E]
6️⃣ E’yi ziyaret et, komşusu F’yi kuyruğa ekle.                KUYRUK[F]
7️⃣ F’yi ziyaret et, hedefe ulaşıldı! ✅                        

## A* (A-Star) ##
en kısa yolu bulmak için kullanılan akıllı bir arama algoritmasıdır.

A* algoritması iki maliyet fonksiyonunu kullanarak en iyi yolu belirler:
g(n): Başlangıç noktasından şu anki düğüme kadar olan gerçek maliyet (geçilen mesafe).
h(n): Şu anki düğümden hedefe olan tahmini maliyet (heuristic).

Toplam maliyet formülü:  f(n)=g(n)+h(n)
A her zaman en düşüK f(n) değerine sahip yolu takip eder.

   A --(2)-- B --(3)-- D
   |         |
  (1)       (2)                         
   |         |
   C --(4)-- E --(1)-- F
Tahmini h değerleri:A: 4, B: 3, C: 4, D: 6, E: 1, F: 0
Yukarıdaki şekilde hedefimiz A noktasından F Noktasına en kısa rotayı bulmak bunun için A* algoritmasını kullanacağız.

A'dan başlıyoruz.

A'nın komşuları B (g=2) ve C (g=1) eklenir.
f(B) = 2 + 3 = 5
f(C) = 1 + 4 = 5

B en düşük f değeri olduğu için seçilir.

B’nin komşuları D (g=5) ve E (g=4) eklenir.
f(D) = 5 + 3 = 8
f(E) = 4 + 1 = 5
E en düşük f değeri olduğu için seçilir.

E’nin komşusu F (hedef) eklenir.
f(F) = 5 + 0 = 5 (hedef bulundu)
F istasyonuna ulaştık. Yol tamamlandı! 
En kısa yol = ['A', 'B', 'E', 'F'] 


## BFS ve A* kullanma nedenimiz ##


BFS, genişlik öncelikli bir arama algoritmasıdır ve en kısa yol bulmada oldukça etkilidir,
BFS, tüm komşuları seviyelere göre kontrol eder ve ilk kez hedefe ulaştığında en kısa yolu bulur.
En az aktarma yaparak hedefe ulaşılmasını sağlar. Özellikle metro hatları gibi birbirine bağlı çok sayıda istasyon olduğunda, BFS doğru seçimdir.

A (A-Star) algoritması, BFS'ye kıyasla daha akıllıca bir yaklaşım sunar ve özellikle daha büyük ve karmaşık grafiklerde daha etkili sonuçlar verir.Hem mevcut yolu (g(n)) hem de hedefe olan tahmin edilen mesafeyi (h(n)) kullanarak en hızlı yolu bulur. Bu sayede, çok daha verimli bir arama yapar.
Heuristic (tahmin) kullanımı, belirli bir hedefe ulaşmada algoritmanın yönlendirilmeye yardımcı olur, böylece gereksiz yollar ve aramalar azaltılır.


## Örnek Kullanım ve Test Sonuçları 
Projeme kattığım yeniliklerden bahsetmem gerekirse ben istasyon adlarını kullanıcıdan istiyorum.eğer o istasyon aktarma durağı ise birden fazla kez durak ismi mevcut demektir(örneğin Kızılay,Demetevler,Gar) bu yüzden kullanıcıya tekrar sorarak istasyonun hangi hatta olduğunu teyit ettiriyorum.Böylece rota süresini daha doğru hesaplıyor.

Başlangıç istasyonu adını girin: Kızılay
❌ 'kızılay' adıyla birden fazla istasyon bulundu. Lütfen hangi istasyonu seçmek istediğinizi belirtin:
  1. Kızılay (K1)
  2. Kızılay (M2)
Seçiminizi yapın (1, 2, ...): 2
Hedef istasyonu adını girin: aşti

🔍 En az aktarmalı rota hesaplanıyor...
✅ En az aktarmalı rota: Kızılay , M2) -> aşti , M1)

⏳ En hızlı rota hesaplanıyor...
✅ En hızlı rota (5 dakika): Kızılay , M2) -> aşti , M1)
**************************************************************************************************************************

Örneğin bu örnekte Kızılay-Demetevler rotasının süresi hesaplanırken yakın olan demetevler(K3) istasyonunun değil kullanıcının istediği diğer istasyon olan T2 istasyonunun süresini hesaplıyor.

Başlangıç istasyonu adını girin: kızılay
❌ 'kızılay' adıyla birden fazla istasyon bulundu. Lütfen hangi istasyonu seçmek istediğinizi belirtin:
  1. Kızılay (K1)
  2. Kızılay (M2)
Seçiminizi yapın (1, 2, ...): 1
Hedef istasyonu adını girin: demetevler
❌ 'demetevler' adıyla birden fazla istasyon bulundu. Lütfen hangi istasyonu seçmek istediğinizi belirtin:
  1. Demetevler (K3)
  2. Demetevler (T2)
Seçiminizi yapın (1, 2, ...): 2

🔍 En az aktarmalı rota hesaplanıyor...
✅ En az aktarmalı rota: Kızılay , K1) -> Ulus , K2) -> Demetevler , K3) -> Demetevler , T2)

⏳ En hızlı rota hesaplanıyor...
✅ En hızlı rota (13 dakika): Kızılay , K1) -> Ulus , K2) -> Demetevler , K3) -> Demetevler , T2)
**********************************************************************************************

Projemin diğer özelliği de istasyon isimleri veritababnında küçük harfle kaydedilmesine rağmen ,büyük küçük harf duyarlılığı etkisiz duruma getirilmiştir.

Başlangıç istasyonu adını girin: GAR
❌ 'gar' adıyla birden fazla istasyon bulundu. Lütfen hangi istasyonu seçmek istediğinizi belirtin:
  1. Gar (M4)
  2. Gar (T3)
Seçiminizi yapın (1, 2, ...): 2
Hedef istasyonu adını girin: ULUS

🔍 En az aktarmalı rota hesaplanıyor...
✅ En az aktarmalı rota: Gar , T3) -> Demetevler , T2) -> Demetevler , K3) -> Ulus , K2)

⏳ En hızlı rota hesaplanıyor...
✅ En hızlı rota (15 dakika): Gar , T3) -> Gar , M4) -> Sıhhiye , M3) -> Kızılay , M2) -> Kızılay , K1) -> Ulus , K2)

## Projeyi Geliştirme Fikirleri

-Kullanıcı Dostu Bir Arayüz Geliştirme
 flask veya django kullanılarak bir web sitesi oluşturulabilir böylece kaliteli kullanıcı deneyimi sunar

-Multi-Modal Ulaşım Entegrasyonu
 Metro dışında otobüs, tramvay veya bisiklet gibi ulaşım araçları da dahil ederek karma bir ulaşım rotası oluşturulabilir.(google maps 
 gibi)

 -Kalabalık istasyonları tespit etme 
 Kullanıcı belirli bir saatte yola çıkmak istediğinde, yapay zekayla kalabalık seviyesini tahmin eden veya gercek yogunluk verilerine 
 göre,hangi istasyonun daha az kalabalık olacagına dair öneri sunan bir sistem tasarlanabilir.



