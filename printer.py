import random
from collections import deque

class Queue:
    def __init__(self):
        self.items = deque() #queue için deque kullanımı.

    def enqueue(self, item):
        self.items.append(item) #item'i queue'nin sonuna(sağa) ekler.
        #print(f"Enqueued {item} to the queue.")

    def dequeue(self):
        if not self.is_empty():
            removed_item = self.items.popleft() #queue'nin başındaki(soldaki) elamanı çıkarır ve döndürür.
            #print(f"Dequeued {removed_item} from the queue.")
            return removed_item
        else:
            print("Queue is empty, can not dequeue!")
            return None
        
    def peek(self):
        if not self.is_empty():
            #print(f"Front of queue is {self.items[0]}")
            return self.items[0] #Queue'nin başındaki elemanı döndürecek.
        else:
            print("Queue is empty, nothing to peek!")
            return None
        
    def is_empty(self):
        return len(self.items) == 0 #queue boş mu?
    
    def size(self):
        #print(f"Queue size is {len(self.items)}")
        return len(self.items) #queue'deki eleman sayısını döndürecek.

class Printer:
    def __init__(self, ppm):
        self.page_rate = ppm #sayfa başına dakika (ppm - pager per minute-)
        self.current_task = None #yazıcının mevcut görevi
        self.time_remaining = 0 #yazıcının mevcut görevi için kalan süresi(BAŞLANGIÇTA 0 )

    def tick(self):
        #Yazıcı 1 saniye çalıştırıldığında çağırılır
        if self.current_task is not None:
            self.time_remaining = self.time_remaining - 1 #1 saniye geçti
            if self.time_remaining <= 0:
                self.current_task = None #Görev tamamlandı yazıcı boşta 
    
    def busy(self):
        #Yazıcı boş mu kontrol et
        return self.current_task is not None  #Eğer yazıcı çalışıyor ise True döndür.
    
    def start_next(self, new_task):
        #Yazıcıya yeni görev başlat.
        self.current_task = new_task #Yeni görev atandı
        self.time_remaining = new_task.get_pages() * 60 / self.page_rate #Sayfa sayısına göre zama hesapla

class Task: #Baskı
    def __init__(self, time):
        self.timestamp = time #Görev zamanı(ne zaman geldi)
        self.pages = random.randrange(1, 21) #Rastgele sayfa sayısı (1-20 arası)

    def get_stamp(self):#Görevin zaman damgasını al
        return self.timestamp #zaman damgasını döndür
    
    def get_pages(self):
        #Görevin sayfa sayısını al
        return self.pages#sayfa sayısını döndür
    
    def wait_time(self, current_time):
        #görevin bekleme süresini hesapla
        return current_time - self.timestamp #Bekleme süresi = şimdiki zaman - görev zamanı
    
def simulation(num_seconds, pages_per_minute):
    lab_printer = Printer(pages_per_minute) #Yazıcı nesnesini oluştur(sayfa başına dakika hızını ayarla)
    print_queue = Queue() #Yazıcı için bir görev kuyruğu oluştur.
    waiting_times = [] #Bekleme sürelerinin listeleri

    for current_second in range(num_seconds):
        #Her saniye (num_seconds kadar) simülasyon devam eder
        if new_print_task(): #eğer yeni bir baski görevi eklenecekse
            task = Task(current_second) #yeni bir görev oluştur, mevcut zamanı task'ın zaman damgası olarak kullan.
            print_queue.enqueue(task) #yeni task'ı kuyrukta sıraya ekle.

        #eğeryazıcı boşsa ve kuyrukta görev varsa; yazıcıya görev ver
        if (not lab_printer.busy()) and (not print_queue.is_empty()):
            nexttask = print_queue.dequeue() #kuyruğun başındaki görevi al(en soldaki alınıyo yani)
            waiting_times.append(nexttask.wait_time(current_second)) #task'ın bekleme süresini hesapla ve listeye ekle
            lab_printer.start_next(nexttask) #yazıcıyı task'ı basmaya başlat

        lab_printer.tick() #Yazıcıyı 1 saniye çalıştır (basma işlemi simüle edilir.)

    #ortalama bekleme süresi hesaplanır:
    average_wait = sum(waiting_times) / len(waiting_times) if waiting_times else 0 # eğer bekleme süresi varsa ortalama hesapla.
    #ortalama bekleme süresi ve kuyruktaki görevler yazdırılır.
    print("Average Wait %6.2f secs %3d tasks remaining" % (average_wait , print_queue.size())) 

def new_print_task():
    num = random.randrange(1, 181)
    return num == 180 #eğer sayı 180 ise , yeni bir baskı görevi oluşturulacak

for i in range(10):#simülasyonu 10 kez çalıştır
    simulation(3600, 10) #3600 saniye (1 saat) boyunca, dakikada 10 sayfa hızımda yazıcıyı çalıştır.
    