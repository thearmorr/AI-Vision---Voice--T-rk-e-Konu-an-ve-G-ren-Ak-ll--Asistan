📌 AI Görsel ve Sesli Etkileşimli Asistan
👁️ Kamerayla Gören, 🎙️ Sesle Dinleyen ve 💬 Sohbet Eden Yapay Zekâ Destekli Sistem
🧠 Proje Açıklaması
Bu proje, gerçek zamanlı görüntü işleme, sesli komut tanıma, ve yapay zekâ sohbet motorunu bir araya getirerek geliştirilen bir çok modaliteli (multi-modal) yapay zekâ asistanıdır. Sistem hem kullanıcıyı kameradan "görür", hem mikrofondan dinler, hem de doğal Türkçe dilinde sesli geri bildirim verir.

🔧 Teknik Özellikler

Özellik	Açıklama
🎥 Görüntü Tanıma	OpenCV ve MobileNet SSD kullanarak gerçek zamanlı nesne tanıma ve takip
🧍 Odak Takibi	Sesli komutlarla belirli bir insan nesnesine odaklanma (örnek: "İnsan 2'ye odaklan")
🗣️ Sesli Komut Tanıma	speech_recognition ile Türkçe konuşmaları metne çevirme
🤖 Yapay Zekâ Cevapları	Google Gemini 1.5 Flash modeli ile anlamlı, samimi, kısa yanıtlar üretme
🔊 Sesli Yanıt	gTTS ve pygame ile Türkçe yapay sesli konuşma
🧠 Kısa Süreli Hafıza	Son 10 konuşma geçmişine göre bağlamlı cevaplar
🧵 Çoklu Thread Kullanımı	Kamera ve mikrofon işlemleri aynı anda paralel çalışır
🎯 Neler Yapabilir?
Kameradaki kişileri veya nesneleri tespit eder ve etiketler.

Sesli komutla belirli kişilere "odaklanabilir" ya da takibi bırakabilir.

Kullanıcıyla kısa, samimi, Türkçe konuşmalar yapabilir.

Yanıtlarını doğal sesle geri iletir.

Görme + duyma + konuşma kabiliyetiyle etkileşimli bir AI deneyimi sunar.

💡 Örnek Kullanım Komutları
"İnsan 1'e odaklan" – Belirli bir kişiyi takip etmeye başlar.

"Takipten çık" – Takibi bırakır.

"Nasılsın kanka?" – AI dostça ve kısa bir şekilde cevap verir.

"Bugün hava nasıl?" – Chat yanıtını sesli verir.

🧰 Kullanılan Teknolojiler
Python 3.x

OpenCV + MobileNet SSD (nesne tanıma)

speech_recognition (konuşma algılama)

gTTS + pygame (sesli yanıtlar)

Google Generative AI (Gemini 1.5 Flash) (doğal dil üretimi)

Threading (video + ses aynı anda çalışması için)

⚠️ Notlar
Projeyi çalıştırmadan önce coco.names, frozen_inference_graph.pb, ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt dosyalarının aynı klasörde olması gerekir.

Google API anahtarının doğru ve geçerli olduğundan emin olun.

gTTS ve pygame modülleri sistemde kurulu olmalıdır.
