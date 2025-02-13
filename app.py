import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from supabase import create_client, Client
from streamlit_js_eval import streamlit_js_eval
import pytz
import time
import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
#bilgiler
#supabase 
url = "https://ezyhoocwfrocaqsehler.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV6eWhvb2N3ZnJvY2Fxc2VobGVyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjcyOTkzOTUsImV4cCI6MjA0Mjg3NTM5NX0.3A2pCuleW0RnGIlCaM5pALWw8fB_KW_y2-qsIJ1_FJI"
supabase_DB = "FatihDB"
#kargo kullanıcı adı şifre ve kargo kodu
kullanici_Adi = "kombingiyim@yesilkar.com"
sifre = "Fatih123."
sube_kodu ="SL"

# Supabase Client oluştur
supabase: Client = create_client(url, key)

turkey_tz = pytz.timezone('Europe/Istanbul')
tarih = datetime.now(turkey_tz).strftime("%Y-%m-%d %H:%M:%S")
yukleme_tarihi= datetime.now(turkey_tz).strftime("%Y-%m-%d")



data = supabase.table(supabase_DB).select("*").eq("siparis_durumu", "1").order("id",desc=False).execute()  
veri = pd.DataFrame(data.data) 
tab11, tab22 ,tab33,tab44 = st.tabs(["Sipariş", "SİL","KARGO TAKİP","GEÇMİŞ KARGOLAR"]  )
with tab11:

    action = st.selectbox(
                "Seçenekler",
                [
                    "Yeni Sipariş",
                    "Sipariş Güncelle Veya Sil",
                    "Siparişleri Göster",
                    "Sipariş Sil",
                ],
            )
    if action == "Yeni Sipariş":
                with st.form(key="siparis_form"):
                    bilgiler = st.text_area(label="ADRESLER*",value="",placeholder="Siparişi Buraya Yapıştır")
                    st.markdown("**Zorunlu*")
                    dugme= st.form_submit_button(label="Siparişi Kaydet")
                    
        
                    lines = bilgiler.title().split('\n')
                    iller = {'Adana': ['Aladağ', 'Ceyhan', 'Çukurova', 'Feke', 'İmamoğlu', 'Karaisalı', 'Karataş', 'Kozan', 'Pozantı', 'Saimbeyli', 'Sarıçam', 'Seyhan', 'Tufanbeyli', 'Yumurtalık', 'Yüreğir'], 
'Adıyaman': ['Besni', 'Çelikhan', 'Gerger', 'Gölbaşı', 'Kahta', 'Merkez', 'Samsat', 'Sincik', 'Tut'], 
'Afyonkarahisar': ['Başmakçı', 'Bayat', 'Bolvadin', 'Çay', 'Çobanlar', 'Dazkırı', 'Dinar', 'Emirdağ', 'Evciler', 'Hocalar', 'İhsaniye', 'İscehisar', 'Kızılören', 'Merkez', 'Sandıklı', 'Sinanpaşa', 'Sultandağı', 'Şuhut'], 
'Ağrı': ['Diyadin', 'Doğubayazıt', 'Eleşkirt', 'Hamur', 'Merkez', 'Patnos', 'Taşlıçay', 'Tutak'], 
'Amasya': ['Göynücek', 'Gümüşhacıköy', 'Hamamözü', 'Merkez', 'Merzifon', 'Suluova', 'Taşova'], 
'Ankara': ['Akyurt', 'Altındağ', 'Ayaş', 'Bala', 'Beypazarı', 'Çamlıdere', 'Çankaya', 'Çubuk', 'Elmadağ', 'Etimesgut', 'Evren', 'Gölbaşı', 'Güdül', 'Haymana', 'Kahramankazan', 'Kalecik', 'Keçiören', 'Kızılcahamam', 'Mamak', 'Nallıhan', 'Polatlı', 'Pursaklar', 'Sincan', 'Şereflikoçhisar', 'Yenimahalle'], 
'Antalya': ['Akseki', 'Aksu', 'Alanya', 'Demre', 'Döşemealtı', 'Elmalı', 'Finike', 'Gazipaşa', 'Gündoğmuş', 'İbradı', 'Kaş', 'Kemer', 'Kepez', 'Konyaaltı', 'Korkuteli', 'Kumluca', 'Manavgat', 'Muratpaşa', 'Serik'], 
'Artvin': ['Ardanuç', 'Arhavi', 'Borçka', 'Hopa', 'Merkez', 'Murgul', 'Şavşat', 'Yusufeli'], 
'Aydın': ['Bozdoğan', 'Buharkent', 'Çine', 'Didim', 'Efeler', 'Germencik', 'İncirliova', 'Karacasu', 'Karpuzlu', 'Koçarlı', 'Köşk', 'Kuşadası', 'Kuyucak', 'Nazilli', 'Söke', 'Sultanhisar', 'Yenipazar'], 
'Balıkesir': ['Altıeylül', 'Ayvalık', 'Balya', 'Bandırma', 'Bigadiç', 'Burhaniye', 'Dursunbey', 'Edremit', 'Erdek', 'Gömeç', 'Gönen', 'Havran', 'İvrindi', 'Karesi', 'Kepsut', 'Manyas', 'Marmara', 'Savaştepe', 'Sındırgı', 'Susurluk'],
'Bilecik': ['Bozüyük', 'Gölpazarı', 'İnhisar', 'Merkez', 'Osmaneli', 'Pazaryeri', 'Söğüt', 'Yenipazar'], 
'Bingöl': ['Adaklı', 'Genç', 'Karlıova', 'Kiğı', 'Merkez', 'Solhan', 'Yayladere', 'Yedisu'], 
'Bitlis': ['Adilcevaz', 'Ahlat', 'Güroymak', 'Hizan', 'Merkez', 'Mutki', 'Tatvan'], 
'Bolu': ['Dörtdivan', 'Gerede', 'Göynük', 'Kıbrıscık', 'Mengen', 'Merkez', 'Mudurnu', 'Seben', 'Yeniçağa'], 
'Burdur': ['Ağlasun', 'Altınyayla', 'Bucak', 'Çavdır', 'Çeltikçi', 'Gölhisar', 'Karamanlı', 'Kemer', 'Merkez', 'Tefenni', 'Yeşilova'], 
'Bursa': ['Büyükorhan', 'Gemlik', 'Gürsu', 'Harmancık', 'İnegöl', 'İznik', 'Karacabey', 'Keles', 'Kestel', 'Mudanya', 'Mustafakemalpaşa', 'Nilüfer', 'Orhaneli', 'Orhangazi', 'Osmangazi', 'Yenişehir', 'Yıldırım'], 
'Çanakkale': ['Ayvacık', 'Bayramiç', 'Biga', 'Bozcaada', 'Çan', 'Eceabat', 'Ezine', 'Gelibolu', 'Gökçeada', 'Lapseki', 'Merkez', 'Yenice'], 
'Çankırı': ['Atkaracalar', 'Bayramören', 'Çerkeş', 'Eldivan', 'Ilgaz', 'Kızılırmak', 'Korgun', 'Kurşunlu', 'Merkez', 'Orta', 'Şabanözü', 'Yapraklı'], 
'Çorum': ['Alaca', 'Bayat', 'Boğazkale', 'Dodurga', 'İskilip', 'Kargı', 'Laçin', 'Mecitözü', 'Merkez', 'Oğuzlar', 'Ortaköy', 'Osmancık', 'Sungurlu', 'Uğurludağ'],
'Denizli': ['Acıpayam', 'Babadağ', 'Baklan', 'Bekilli', 'Beyağaç', 'Bozkurt', 'Buldan', 'Çal', 'Çameli', 'Çardak', 'Çivril', 'Güney', 'Honaz', 'Kale', 'Merkezefendi', 'Pamukkale', 'Sarayköy', 'Serinhisar', 'Tavas'],
'Diyarbakır': ['Bağlar', 'Bismil', 'Çermik', 'Çınar', 'Çüngüş', 'Dicle', 'Eğil', 'Ergani', 'Hani', 'Hazro', 'Kayapınar', 'Kocaköy', 'Kulp', 'Lice', 'Silvan', 'Sur', 'Yenişehir'], 
'Edirne': ['Enez', 'Havsa', 'İpsala', 'Keşan', 'Lalapaşa', 'Meriç', 'Merkez', 'Süloğlu', 'Uzunköprü'], 
'Elazığ': ['Ağın', 'Alacakaya', 'Arıcak', 'Baskil', 'Karakoçan', 'Keban', 'Kovancılar', 'Maden', 'Merkez', 'Palu', 'Sivrice'], 
'Erzincan': ['Çayırlı', 'İliç', 'Kemah', 'Kemaliye', 'Merkez', 'Otlukbeli', 'Refahiye', 'Tercan', 'Üzümlü'], 
'Erzurum': ['Aşkale', 'Aziziye', 'Çat', 'Hınıs', 'Horasan', 'İspir', 'Karaçoban', 'Karayazı', 'Köprüköy', 'Narman', 'Oltu', 'Olur', 'Palandöken', 'Pasinler', 'Pazaryolu', 'Şenkaya', 'Tekman', 'Tortum', 'Uzundere', 'Yakutiye'],
'Eskişehir': ['Alpu', 'Beylikova', 'Çifteler', 'Günyüzü', 'Han', 'İnönü', 'Mahmudiye', 'Mihalgazi', 'Mihalıççık', 'Odunpazarı', 'Sarıcakaya', 'Seyitgazi', 'Sivrihisar', 'Tepebaşı'], 
'Gaziantep': ['Araban', 'İslahiye', 'Karkamış', 'Nizip', 'Nurdağı', 'Oğuzeli', 'Şahinbey', 'Şehitkamil', 'Yavuzeli'], 
'Giresun': ['Alucra', 'Bulancak', 'Çamoluk', 'Çanakçı', 'Dereli', 'Doğankent', 'Espiye', 'Eynesil', 'Görele', 'Güce', 'Keşap', 'Merkez', 'Piraziz', 'Şebinkarahisar', 'Tirebolu', 'Yağlıdere'],
'Gümüşhane': ['Kelkit', 'Köse', 'Kürtün', 'Merkez', 'Şiran', 'Torul'], 
'Hakkari': ['Çukurca', 'Merkez', 'Şemdinli', 'Yüksekova'], 
'Hatay': ['Altınözü', 'Antakya', 'Arsuz', 'Belen', 'Defne', 'Dörtyol', 'Erzin', 'Hassa', 'İskenderun', 'Kırıkhan', 'Kumlu', 'Payas', 'Reyhanlı', 'Samandağ', 'Yayladağı'], 
'Isparta': ['Aksu', 'Atabey', 'Eğirdir', 'Gelendost', 'Gönen', 'Keçiborlu', 'Merkez', 'Senirkent', 'Sütçüler', 'Şarkikaraağaç', 'Uluborlu', 'Yalvaç', 'Yenişarbademli'], 
'Mersin': ['Akdeniz', 'Anamur', 'Aydıncık', 'Bozyazı', 'Çamlıyayla', 'Erdemli', 'Gülnar', 'Mezitli', 'Mut', 'Silifke', 'Tarsus', 'Toroslar', 'Yenişehir'], 
'İstanbul': ['Adalar', 'Arnavutköy', 'Ataşehir', 'Avcılar', 'Bağcılar', 'Bahçelievler', 'Bakırköy', 'Başakşehir', 'Bayrampaşa', 'Beşiktaş', 'Beykoz', 'Beylikdüzü', 'Beyoğlu', 'Büyükçekmece', 'Çatalca', 'Çekmeköy', 'Esenler', 'Esenyurt', 'Eyüp', 'Fatih', 'Gaziosmanpaşa', 'Güngören', 'Kadıköy', 'Kağıthane', 'Kartal', 'Küçükçekmece', 'Maltepe', 'Pendik', 'Sancaktepe', 'Sarıyer', 'Silivri', 'Sultanbeyli', 'Sultangazi', 'Şile', 'Şişli', 'Tuzla', 'Ümraniye', 'Üsküdar', 'Zeytinburnu'], 
'İzmir': ['Aliağa', 'Balçova', 'Bayındır', 'Bayraklı', 'Bergama', 'Beydağ', 'Bornova', 'Buca', 'Çeşme', 'Çiğli', 'Dikili', 'Foça', 'Gaziemir', 'Güzelbahçe', 'Karabağlar', 'Karaburun', 'Karşıyaka', 'Kemalpaşa', 'Kınık', 'Kiraz', 'Konak', 'Menderes', 'Menemen', 'Narlıdere', 'Ödemiş', 'Seferihisar', 'Selçuk', 'Tire', 'Torbalı', 'Urla'], 
'Kars': ['Akyaka', 'Arpaçay', 'Digor', 'Kağızman', 'Merkez', 'Sarıkamış', 'Selim', 'Susuz'], 
'Kastamonu': ['Abana', 'Ağlı', 'Araç', 'Azdavay', 'Bozkurt', 'Cide', 'Çatalzeytin', 'Daday', 'Devrekani', 'Doğanyurt', 'Hanönü', 'İhsangazi', 'İnebolu', 'Küre', 'Merkez', 'Pınarbaşı', 'Seydiler', 'Şenpazar', 'Taşköprü', 'Tosya'], 
'Kayseri': ['Akkışla', 'Bünyan', 'Develi', 'Felahiye', 'Hacılar', 'İncesu', 'Kocasinan', 'Melikgazi', 'Özvatan', 'Pınarbaşı', 'Sarıoğlan', 'Sarız', 'Talas', 'Tomarza', 'Yahyalı', 'Yeşilhisar'], 
'Kırklareli': ['Babaeski', 'Demirköy', 'Kofçaz', 'Lüleburgaz', 'Merkez', 'Pehlivanköy', 'Pınarhisar', 'Vize'], 
'Kırşehir': ['Akçakent', 'Akpınar', 'Boztepe', 'Çiçekdağı', 'Kaman', 'Merkez', 'Mucur'], 
'Kocaeli': ['Başiskele', 'Çayırova', 'Darıca', 'Derince', 'Dilovası', 'Gebze', 'Gölcük', 'İzmit', 'Kandıra', 'Karamürsel', 'Kartepe', 'Körfez'], 
'Konya': ['Ahırlı', 'Akören', 'Akşehir', 'Altınekin', 'Beyşehir', 'Bozkır', 'Cihanbeyli', 'Çeltik', 'Çumra', 'Derbent', 'Derebucak', 'Doğanhisar', 'Emirgazi', 'Ereğli', 'Güneysınır', 'Hadim', 'Halkapınar', 'Hüyük', 'Ilgın', 'Kadınhanı', 'Karapınar', 'Karatay', 'Kulu', 'Meram', 'Sarayönü', 'Selçuklu', 'Seydişehir', 'Taşkent', 'Tuzlukçu', 'Yalıhüyük', 'Yunak'], 
'Kütahya': ['Altıntaş', 'Aslanapa', 'Çavdarhisar', 'Domaniç', 'Dumlupınar', 'Emet', 'Gediz', 'Hisarcık', 'Merkez', 'Pazarlar', 'Simav', 'Şaphane', 'Tavşanlı'], 
'Malatya': ['Akçadağ', 'Arapgir', 'Arguvan', 'Battalgazi', 'Darende', 'Doğanşehir', 'Doğanyol', 'Hekimhan', 'Kale', 'Kuluncak', 'Pütürge', 'Yazıhan', 'Yeşilyurt'], 
'Manisa': ['Ahmetli', 'Akhisar', 'Alaşehir', 'Demirci', 'Gölmarmara', 'Gördes', 'Kırkağaç', 'Köprübaşı', 'Kula', 'Salihli', 'Sarıgöl', 'Saruhanlı', 'Selendi', 'Soma', 'Şehzadeler', 'Turgutlu', 'Yunusemre'], 
'Kahramanmaraş': ['Afşin', 'Andırın', 'Çağlayancerit', 'Dulkadiroğlu', 'Ekinözü', 'Elbistan', 'Göksun', 'Nurhak', 'Onikişubat', 'Pazarcık', 'Türkoğlu'], 
'Mardin': ['Artuklu', 'Dargeçit', 'Derik', 'Kızıltepe', 'Mazıdağı', 'Midyat', 'Nusaybin', 'Ömerli', 'Savur', 'Yeşilli'], 
'Muğla': ['Bodrum', 'Dalaman', 'Datça', 'Fethiye', 'Kavaklıdere', 'Köyceğiz', 'Marmaris', 'Menteşe', 'Milas', 'Ortaca', 'Seydikemer', 'Ula', 'Yatağan'], 
'Muş': ['Bulanık', 'Hasköy', 'Korkut', 'Malazgirt', 'Merkez', 'Varto'], 
'Nevşehir': ['Acıgöl', 'Avanos', 'Derinkuyu', 'Gülşehir', 'Hacıbektaş', 'Kozaklı', 'Merkez', 'Ürgüp'], 
'Niğde': ['Altunhisar', 'Bor', 'Çamardı', 'Çiftlik', 'Merkez', 'Ulukışla'], 
'Ordu': ['Akkuş', 'Altınordu', 'Aybastı', 'Çamaş', 'Çatalpınar', 'Çaybaşı', 'Fatsa', 'Gölköy', 'Gülyalı', 'Gürgentepe', 'İkizce', 'Kabadüz', 'Kabataş', 'Korgan', 'Kumru', 'Mesudiye', 'Perşembe', 'Ulubey', 'Ünye'], 
'Rize': ['Ardeşen', 'Çamlıhemşin', 'Çayeli', 'Derepazarı', 'Fındıklı', 'Güneysu', 'Hemşin', 'İkizdere', 'İyidere', 'Kalkandere', 'Merkez', 'Pazar'], 
'Sakarya': ['Adapazarı', 'Akyazı', 'Arifiye', 'Erenler', 'Ferizli', 'Geyve', 'Hendek', 'Karapürçek', 'Karasu', 'Kaynarca', 'Kocaali', 'Pamukova', 'Sapanca', 'Serdivan', 'Söğütlü', 'Taraklı'], 
'Samsun': ['Alaçam', 'Asarcık', 'Atakum', 'Ayvacık', 'Bafra', 'Canik', 'Çarşamba', 'Havza', 'İlkadım', 'Kavak', 'Ladik', 'Salıpazarı', 'Tekkeköy', 'Terme', 'Vezirköprü', 'Yakakent'], 
'Siirt': ['Baykan', 'Eruh', 'Kurtalan', 'Merkez', 'Pervari', 'Şirvan', 'Tillo'], 
'Sinop': ['Ayancık', 'Boyabat', 'Dikmen', 'Durağan', 'Erfelek', 'Gerze', 'Merkez', 'Saraydüzü', 'Türkeli'], 
'Sivas': ['Akıncılar', 'Altınyayla', 'Divriği', 'Doğanşar', 'Gemerek', 'Gölova', 'Gürün', 'Hafik', 'İmranlı', 'Kangal', 'Koyulhisar', 'Merkez', 'Suşehri', 'Şarkışla', 'Ulaş', 'Yıldızeli', 'Zara'], 
'Tekirdağ': ['Çerkezköy', 'Çorlu', 'Ergene', 'Hayrabolu', 'Kapaklı', 'Malkara', 'Marmaraereğlisi', 'Muratlı', 'Saray', 'Süleymanpaşa', 'Şarköy'], 
'Tokat': ['Almus', 'Artova', 'Başçiftlik', 'Erbaa', 'Merkez', 'Niksar', 'Pazar', 'Reşadiye', 'Sulusaray', 'Turhal', 'Yeşilyurt', 'Zile'], 
'Trabzon': ['Akçaabat', 'Araklı', 'Arsin', 'Beşikdüzü', 'Çarşıbaşı', 'Çaykara', 'Dernekpazarı', 'Düzköy', 'Hayrat', 'Köprübaşı', 'Maçka', 'Of', 'Ortahisar', 'Sürmene', 'Şalpazarı', 'Tonya', 'Vakfıkebir', 'Yomra'], 
'Tunceli': ['Çemişgezek', 'Hozat', 'Mazgirt', 'Merkez', 'Nazımiye', 'Ovacık', 'Pertek', 'Pülümür'], 
'Şanlıurfa': ['Akçakale', 'Birecik', 'Bozova', 'Ceylanpınar', 'Eyyübiye', 'Halfeti', 'Haliliye', 'Harran', 'Hilvan', 'Karaköprü', 'Siverek', 'Suruç', 'Viranşehir'], 
'Uşak': ['Banaz', 'Eşme', 'Karahallı', 'Merkez', 'Sivaslı', 'Ulubey'], 
'Van': ['Bahçesaray', 'Başkale', 'Çaldıran', 'Çatak', 'Edremit', 'Erciş', 'Gevaş', 'Gürpınar', 'İpekyolu', 'Muradiye', 'Özalp', 'Saray', 'Tuşba'], 
'Yozgat': ['Akdağmadeni', 'Aydıncık', 'Boğazlıyan', 'Çandır', 'Çayıralan', 'Çekerek', 'Kadışehri', 'Merkez', 'Saraykent', 'Sarıkaya', 'Sorgun', 'Şefaatli', 'Yenifakılı', 'Yerköy'], 
'Zonguldak': ['Alaplı', 'Çaycuma', 'Devrek', 'Ereğli', 'Gökçebey', 'Kilimli', 'Kozlu', 'Merkez'], 
'Aksaray': ['Ağaçören', 'Eskil', 'Gülağaç', 'Güzelyurt', 'Merkez', 'Ortaköy', 'Sarıyahşi'], 
'Bayburt': ['Aydıntepe', 'Demirözü', 'Merkez'], 
'Karaman': ['Ayrancı', 'Başyayla', 'Ermenek', 'Kazımkarabekir', 'Merkez', 'Sarıveliler'], 
'Kırıkkale': ['Bahşili', 'Balışeyh', 'Çelebi', 'Delice', 'Karakeçili', 'Keskin', 'Merkez', 'Sulakyurt', 'Yahşihan'], 
'Batman': ['Beşiri', 'Gercüş', 'Hasankeyf', 'Kozluk', 'Merkez', 'Sason'], 
'Şırnak': ['Beytüşşebap', 'Cizre', 'Güçlükonak', 'İdil', 'Merkez', 'Silopi', 'Uludere'], 
'Bartın': ['Amasra', 'Kurucaşile', 'Merkez', 'Ulus'], 
'Ardahan': ['Çıldır', 'Damal','Göle', 'Hanak', 'Merkez', 'Posof'], 
'Iğdır': ['Aralık', 'Karakoyunlu', 'Merkez', 'Tuzluca'], 
'Yalova': ['Altınova', 'Armutlu', 'Çınarcık', 'Çiftlikköy', 'Merkez', 'Termal'], 
'Karabük': ['Eflani', 'Eskipazar', 'Merkez', 'Ovacık', 'Safranbolu', 'Yenice'], 
'Kilis': ['Elbeyli', 'Merkez', 'Musabeyli', 'Polateli'], 
'Osmaniye': ['Bahçe', 'Düziçi', 'Hasanbeyli', 'Kadirli', 'Merkez', 'Sumbas', 'Toprakkale'], 
'Düzce': ['Akçakoca', 'Cumayeri', 'Çilimli', 'Gölyaka', 'Gümüşova', 'Kaynaşlı', 'Merkez', 'Yığılca']}
                    if len(lines) >= 6:
                            isim_soyisim = lines[0]
                            adres_bilgisi = lines[1]
                            ilce_il = lines[2].split()
                            
                            if len(ilce_il) == 2:
                                ilce = ilce_il[0]
                                il = ilce_il[1]
                                telefon = lines[3]
                                ucret = lines[4]
                                urun_bilgisi = '\n'.join(lines[6:])
        
                                   
                            elif len(ilce_il) == 1:
                                ilce = ilce_il[0]
                                il = lines[3].split()
                                il = il[0]
                                telefon = lines[4]
                                ucret = lines[5]
                                urun_bilgisi = '\n'.join(lines[7:])
        
                            telefon = telefon.replace(" ", "")

                            if il[0] == "I":
                                    il = "İ" + il[1:]
                            il = il.replace("i̇","i")      
                            # Girişlerin kontrolü
                            if il in iller:
                                if ilce[0] == "I":
                                    ilce = "İ" + ilce[1:]
                                ilce = ilce.replace("i̇","i")


                               
                        
                            if il not in iller:
                                    # Eğer şehir listede yoksa, 3. ve 4. satırları değiştir
                                  ilce, il = il, ilce
                        
                        
                            ilce_il = lines[2]
                            if il not in iller:
                               st.warning('İL DOĞRU DEĞİL KONTROL ET', icon="🚨" )  
                               st.warning("ilde bu yazıyor " + il)     
                               st.stop()
                            if ilce not in iller[il]: 
                               st.warning('İLÇE DOĞRU DEĞİL KONTROL ET', icon="🚨" )  
                               st.warning("ilçede bu yazıyor " + ilce)     
                               st.stop() 
                            if len(telefon) == 11:
                                        pass       
                            else:
                                        st.warning('Telefon Numarası Hatalı '+ telefon ,icon="🚨")
                                        st.stop() 
                                        
                    if dugme:
                        if not bilgiler:
                            st.write("bilgiler Eksik")
                            st.stop()
                        else:
                            bilgilr = {'tarih': tarih ,
                                    "İSİM SOYİSİM": isim_soyisim,
                                    "İLÇE": ilce,
                                    "İL": il,
                                    "ADRES": adres_bilgisi,
                                    "TELEFON": telefon,
                                    "ŞUBE KOD": sube_kodu,
                                    "MÜŞTERİ NO": "",
                                    "TUTAR": ucret,
                                    "ÜRÜN": urun_bilgisi,
                                    "MİKTAR": "1",
                                    "GRAM": "800",
                                    "GTÜRÜ": "2",
                                    "ÜCRETTÜRÜ": "6",
                                    "EK HİZMET": " ",
                                    "KDV": "8",
                                    "SİP NO": telefon,
                                    "ÇIKIŞ NO": "",
                                    "SATICI": "",
                                    "HATTAR": "",
                                    "FATTAR": "",
                                    "EN": "10",
                                    "BOY": "15",
                                    "YÜKSEKLİK": "10",
                                    "siparis_durumu": "1",
                                       
                                }
                            
                            response = supabase.table(supabase_DB).insert(bilgilr).execute()
                            st.success("Sipariş Kaydedildi")
                            streamlit_js_eval(js_expressions="parent.window.location.reload()")
                st.divider()     

                
    if action == "Sipariş Güncelle Veya Sil":
        st.text("BİRDEN FAZLA İŞARETLYİP SİLERSEN \nİŞARETLENENLER SİLİR DİKKAT ET")
        if veri.empty:
          st.warning("Şuan Siparişin yok")
        else: 
         isimler = veri[["İSİM SOYİSİM","id","ADRES","İL","İLÇE","TELEFON","TUTAR","ÜRÜN"]].sort_values(by="İSİM SOYİSİM")
         for index, row in isimler.iterrows():
            isim = row["İSİM SOYİSİM"]
            id = row["id"]
            adres = row["ADRES"]
            ilce = row["İLÇE"]
            il = row["İL"]
            telefon = row["TELEFON"]
            tutar = row["TUTAR"]
            urun = row["ÜRÜN"]

               
            if st.checkbox(f"{isim}", key=f"{id}"):        
                st.text(f"ID: {id}")
                isim_soy = st.text_input("İsim", value=f"{isim}",key=f"{id}+2")
                adres = st.text_area("adres", value=f"{adres}",key=f"{id}+3")
                il =st.text_input("il",value=f"{il}",key=f"{id}+6")
                ilce =st.text_input("ilce",value=f"{ilce}",key=f"{id}+4")
                telefon = st.text_input("telefon",value=f"{telefon}",key=f"{id}+5")
                tutar = st.text_input("Tutar",value=f"{tutar}",key=f"{id}+1") 
                urun = st.text_area("Ürün",value=f"{urun}",key=f"{id}+7") 
                col111, col222 = st.columns(2)
                with col111:
                    if st.button("Güncelle", key=f"{id}+221"):                            
                        response = supabase.table(supabase_DB).update({"İSİM SOYİSİM": isim_soy,"ADRES": adres,"İL":il,"İLÇE":ilce,"TELEFON":telefon,"SİP NO": telefon,"TUTAR":tutar,"ÜRÜN":urun}).eq("id", id).execute()                        
                        st.success("Güncelleme başarılı.")
                        st.rerun()
                    if st.button("SİL",key=f"{id}+32"):
                      response = supabase.table(supabase_DB).delete().eq("id", id).execute()                     
                      st.warning("Güncellendi") 
                        
                st.divider()
            #response = supabase.table('countries').delete().eq('id', 1).execute()

    if action == "Sipariş Sil":
        st.title("KANDIRDIM")

    if action == "Siparişleri Göster":
       if veri.empty:
        st.warning("Şuan Siparişin yok")
       else :        
        st.dataframe(veri[["İSİM SOYİSİM","ADRES","İL","İLÇE","TELEFON","TUTAR","ÜRÜN"]])

with tab22:
        st.title ("Sipariş Silme Ekranı")
        st.text("DİKKAT SİPARİŞLERİ YAZDIRDIĞINDAN EMİN OL")
        if st.button("Siparisleri SİL"):
            response = (supabase.table(supabase_DB).update({'yazdirma_tarihi': yukleme_tarihi}).eq("siparis_durumu", "1").execute())
            response = (supabase.table(supabase_DB).update({"siparis_durumu": "2"}).eq("siparis_durumu", "1").execute())
            st.warning("Silindi") 
            st.rerun()

tab12, tab21 = st.tabs(["Tab1", "SİPARİŞ SAYISI"] )
with tab21:
    st.text(f"Sipariş Sayısı: {len(veri)}")


st.divider()


with tab33:
        st.title ("KARGO TAKİP ETME EKRANI")    
        st.image("aras.jpg",caption='ARAS KARGO KARGO TAKİP')


            # Giriş linki ve istek başlıkları
        login_link = "https://webpostman.yesilkarkargo.com/user/login"
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0'
            }

            # Giriş isteği yap
        login_response = requests.get(login_link, headers=headers)

            # BeautifulSoup ile HTML'i ayrıştır
        bs = BS(login_response.content, 'html5lib')

            # Giriş form verileri ve token değerini al
        form_data = {
                "token": bs.find('input', attrs={'name': 'token'})['value'],
                "return_url": "/",
                "email": kullanici_Adi,
                "password": sifre
            }


        
        takip = st.text_input("Takip Kodu - Yada Telefon",placeholder='buraya yapıştır').strip()
        takip = "".join(takip.split())
        if len(takip) == 13:



            if takip:
                headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0'}
                url1 = f"https://kargotakip.araskargo.com.tr/mainpage.aspx?code={takip}"
                
                response = requests.get(url1,headers=headers)
                
                # HTML içeriğini BeautifulSoup kullanarak analiz edin
                soup = BS(response.content,"html5lib")
                
                link_veri = soup.findAll("a")
                for a_tag in link_veri:
                    href_attribute = a_tag['href']
                    if "CargoInfoWaybillAndDelivered.aspx" in href_attribute:
                        link_veri=(f"https://kargotakip.araskargo.com.tr/{href_attribute}")
                        
                    if "CargoInfoTransactionAndRedirection.aspx" in href_attribute:
                        cıktı_sonuc=(f"https://kargotakip.araskargo.com.tr/{href_attribute}")    
                            
                bilgiler =[]

                response=requests.get(link_veri)
                soup=BS(response.text,"html5lib")
                cıkıs_sube = soup.find("span",{"id":"cikis_subesi"}).text
                teslimat_sube = soup.find("span",{"id":"varis_subesi"}).text
                gonderim_Tarihi = soup.find("span",{"id":"cikis_tarihi"}).text
                son_durum = soup.find("span",{"id":"Son_Durum"}).text
                alici_adi = soup.find("span",{"id":"alici_adi_soyadi"}).text
                gonderi_tip = soup.find("span",{"id":"LabelGonTipi"}).text
                bilgiler.append({"Alıcı Adı":alici_adi,"Çıkış Şube":cıkıs_sube,"Teslimat Şubesi":teslimat_sube,"Gönderim Tarihi":gonderim_Tarihi,"Kargo Son durum":son_durum,"Gönderi tip":gonderi_tip  })
                response=requests.get(cıktı_sonuc)
                soup=BS(response.text,"html5lib")
                tablo = soup.find("table").findAll("tr")


                if son_durum == "TESLİM EDİLDİ" and gonderi_tip == "NORMAL" :
                    st.markdown("<h1 style='color: green; font-size: 36px;'>KARGONUZ TESLİM EDİLDİ</h1>", unsafe_allow_html=True)

                elif son_durum == "YOLDA" :
                    st.markdown("<h1 style='color: blue; font-size: 36px;'>KARGONUZ YOLDADIR EN KISA SÜREDE SİZE GELECEK</h1>", unsafe_allow_html=True)    

                elif gonderi_tip == "İADE" :
                    st.markdown("<h1 style='color: red; font-size: 36px;'>KARGONUZ İADE EDİLMİŞTİR GERİ DÖNÜYOR</h1>", unsafe_allow_html=True)
                        
                elif son_durum == "TESLİMATTA" and gonderi_tip == "NORMAL" :
                    st.markdown("<h1 style='color: green; font-size: 36px;'>KARGONUZ DAĞITIMA ÇIKMIŞ BUGÜN GELEBİLİR</h1>", unsafe_allow_html=True) 
                        
                else:
                    
                    st.markdown("<h1 style='color: orange; font-size: 25px;'>KARGONUZ ARAS KARGO ŞUBESİNDE EN KISA SÜREDE ALMANIZ GEREKİYOR</h1>", unsafe_allow_html=True)
                    st.markdown(f"<h1 style='color: red; font-size: 36px;'>ARAS KARGO {teslimat_sube} ŞUBESİ</h1>", unsafe_allow_html=True)      


                st.dataframe(bilgiler)
                for td in tablo[0:2]:
                    ts = (td.text)
                    st.text(ts)              
        elif len(takip) == 11:
            if takip:
                tarih_baslangic = datetime.now()
                oncesi_15_gun = tarih_baslangic - timedelta(days=15)
                tarih_bitis = datetime.now().strftime("%d.%m.%Y")
                tarih_baslangic = oncesi_15_gun.strftime("%d.%m.%Y")
                
                giris = requests.post(login_link, headers=headers, data=form_data,cookies=login_response.cookies)
                kullanici = BS(giris.content, "html.parser")
                cookie = login_response.cookies
                cargo_link = f"https://webpostman.yesilkarkargo.com/cargo/?alim_start={tarih_baslangic}&alim_end={tarih_bitis}&durums=-1&teslim_start=&teslim_end=&barkod=&isim=&soyisim=&seh_kod=0&ilce=&sipno={takip}&telno=&d_trbkod=0&d_subekod=0&btnSubmit=btnSubmit"
                cargo_response = requests.get(cargo_link, cookies=cookie)
                cargo_bs = BS(cargo_response.content, "html5lib")
                tablo = cargo_bs.find("table", {"id": "generalTables"}).find("tbody").find_all("tr")
                liste = []
                st.title("GÖNDERİLEN KARGOLAR")
                for satir in tablo:
                    sütunlar = satir.find_all("td")
                    veriler = [sütun.get_text(strip=True) for sütun in sütunlar]
                    liste.append({"TAKİP KODU":veriler[4], 
                    "İSİM SOYİSİM":veriler[5],
                    "TELEFON NU":"0"+veriler[19],
                    "SONUÇ":veriler[9],
                    "KARGO ŞUBESİ":veriler[10],
                    "ÜCRET":veriler[13]+" TL" ,
                    "siparis_takip": veriler[18] })
                    
                       
                
                
                df = pd.DataFrame(liste)
                def arama(telefon_numarasi):
                    sonuc = df[df["siparis_takip"] == telefon_numarasi]
                    if not sonuc.empty:
                        takip_kodu = sonuc.iloc[0]["TAKİP KODU"]
                        return takip_kodu
                        
                    else:
                        st.warning("Telefon Numarası bulunamadı.")
                
                takip_kodu = arama(takip)
                headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0'}
                url1 = f"https://kargotakip.araskargo.com.tr/mainpage.aspx?code={takip_kodu}"
                
                
                response = requests.get(url1,headers=headers)
                
                # HTML içeriğini BeautifulSoup kullanarak analiz edin
                soup = BS(response.content,"html5lib")
                
                link_veri = soup.findAll("a")
                for a_tag in link_veri:
                    href_attribute = a_tag['href']
                    if "CargoInfoWaybillAndDelivered.aspx" in href_attribute:
                        link_veri=(f"https://kargotakip.araskargo.com.tr/{href_attribute}")
                        
                    if "CargoInfoTransactionAndRedirection.aspx" in href_attribute:
                        cıktı_sonuc=(f"https://kargotakip.araskargo.com.tr/{href_attribute}")    
                            
                bilgiler =[]

                response=requests.get(link_veri)
                soup=BS(response.text,"html5lib")
                cıkıs_sube = soup.find("span",{"id":"cikis_subesi"}).text
                teslimat_sube = soup.find("span",{"id":"varis_subesi"}).text
                gonderim_Tarihi = soup.find("span",{"id":"cikis_tarihi"}).text
                son_durum = soup.find("span",{"id":"Son_Durum"}).text
                alici_adi = soup.find("span",{"id":"alici_adi_soyadi"}).text
                gonderi_tip = soup.find("span",{"id":"LabelGonTipi"}).text
                bilgiler.append({"Alıcı Adı":alici_adi,"Çıkış Şube":cıkıs_sube,"Teslimat Şubesi":teslimat_sube,"Gönderim Tarihi":gonderim_Tarihi,"Kargo Son durum":son_durum,"Gönderi tip":gonderi_tip  })
                response=requests.get(cıktı_sonuc)
                soup=BS(response.text,"html5lib")
                tablo = soup.find("table").findAll("tr")


                if son_durum == "TESLİM EDİLDİ" and gonderi_tip == "NORMAL" :
                    st.markdown("<h1 style='color: green; font-size: 36px;'>KARGONUZ TESLİM EDİLDİ</h1>", unsafe_allow_html=True)

                elif son_durum == "YOLDA" :
                    st.markdown("<h1 style='color: blue; font-size: 36px;'>KARGONUZ YOLDADIR EN KISA SÜREDE SİZE GELECEK</h1>", unsafe_allow_html=True)    

                elif gonderi_tip == "İADE" :
                    st.markdown("<h1 style='color: red; font-size: 36px;'>KARGONUZ İADE EDİLMİŞTİR GERİ DÖNÜYOR</h1>", unsafe_allow_html=True)
                        
                elif son_durum == "TESLİMATTA" and gonderi_tip == "NORMAL" :
                    st.markdown("<h1 style='color: green; font-size: 36px;'>KARGONUZ DAĞITIMA ÇIKMIŞ BUGÜN GELEBİLİR</h1>", unsafe_allow_html=True) 
                        
                else:
                    
                    st.markdown("<h1 style='color: orange; font-size: 25px;'>KARGONUZ ARAS KARGO ŞUBESİNDE EN KISA SÜREDE ALMANIZ GEREKİYOR</h1>", unsafe_allow_html=True)
                    st.markdown(f"<h1 style='color: red; font-size: 36px;'>ARAS KARGO {teslimat_sube} ŞUBESİ</h1>", unsafe_allow_html=True)      

                st.text(f"TAKİP KODU : {takip_kodu}")
                st.dataframe(bilgiler)
                for td in tablo[0:2]:
                    ts = (td.text)
                    st.text(ts)               
#tarihe göre listeleme kargoları 



            # Giriş isteği yap
        tarih_baslangic = st.date_input(label="BAŞLANGIÇ TARİH")
        if tarih_baslangic:
            tarih_baslangic = (tarih_baslangic.strftime("%d.%m.%Y"))
        tarih_bitis = st.date_input(label="BİTİŞ TARİH")
        if tarih_bitis:
            tarih_bitis = (tarih_bitis.strftime("%d.%m.%Y"))    
            
        if st.button("ŞUBEDE BEKLEYEN KARGOLARI LİSTELE"):    
            giris = requests.post(login_link, headers=headers, data=form_data,cookies=login_response.cookies)
            kullanici = BS(giris.content, "html.parser")
            cookie = login_response.cookies
            cargo_link = f"https://webpostman.yesilkarkargo.com/cargo/?alim_start={tarih_baslangic}&alim_end={tarih_bitis}&durums=-1&teslim_start=&teslim_end=&barkod=&isim=&soyisim=&seh_kod=0&ilce=&sipno=&telno=&d_trbkod=0&d_subekod=0&btnSubmit=btnSubmit"
            
            cargo_response = requests.get(cargo_link, cookies=cookie)
            cargo_bs = BS(cargo_response.content, "html5lib")
            tablo = cargo_bs.find("table", {"id": "generalTables"}).find("tbody").find_all("tr")
            liste = []
            st.title("ŞUBEDE BEKLEYEN KARGOLAR")
            for satir in tablo:
                sütunlar = satir.find_all("td")
                veriler = [sütun.get_text(strip=True) for sütun in sütunlar]
                if veriler[9] == "Teslim" or veriler[9] == "Paketleme" or veriler[8] == "İade" or veriler[9] == "Yolda" or veriler[9] == "Çıkış Şubesinde":
                    continue

                liste.append({"TAKİP KODU":veriler[4], 
                  "İSİM SOYİSİM":veriler[5],
                  "TELEFON NU":veriler[19],
                  "SONUÇ":veriler[9],
                  "KARGO ŞUBESİ":veriler[11],
                  "ÜCRET":veriler[14]+" TL"  })   
                
        
            db = st.dataframe(liste)
            sayı = len(liste)

            st.markdown(f"<h1 style='color: green; font-size: 36px;'>Aras Kargo Şubesinde  {sayı} Adet kargo bekliyor</h1>", unsafe_allow_html=True)

        if st.button(f"{tarih_baslangic} - {tarih_bitis} ARASI ÇIKMIŞ KARGOLARI LİSTELE"):
            giris = requests.post(login_link, headers=headers, data=form_data,cookies=login_response.cookies)
            kullanici = BS(giris.content, "html.parser")
            cookie = login_response.cookies
            cargo_link = f"https://webpostman.yesilkarkargo.com/cargo/?alim_start={tarih_baslangic}&alim_end={tarih_bitis}&durums=-1&teslim_start=&teslim_end=&barkod=&isim=&soyisim=&seh_kod=0&ilce=&sipno=&telno=&d_trbkod=0&d_subekod=0&btnSubmit=btnSubmit"
            
            cargo_response = requests.get(cargo_link, cookies=cookie)
            cargo_bs = BS(cargo_response.content, "html5lib")
            tablo = cargo_bs.find("table", {"id": "generalTables"}).find("tbody").find_all("tr")
            liste = []
            st.title("GÖNDERİLEN KARGOLAR")
            for satir in tablo:
                sütunlar = satir.find_all("td")
                veriler = [sütun.get_text(strip=True) for sütun in sütunlar]
                liste.append({"TAKİP KODU":veriler[4], 
                  "İSİM SOYİSİM":veriler[5],
                  "TELEFON NU":veriler[18],
                  "SONUÇ":veriler[9],
                  "KARGO ŞUBESİ":veriler[10],
                  "ÜCRET":veriler[13]+" TL"  })

            db = st.dataframe(liste) 
            sayı = len(liste)
            
            st.markdown(f"<h1 style='color: green; font-size: 36px;'>GÖNDERİLEN KARGO {sayı} </h1>", unsafe_allow_html=True)

with tab44:
    gecmis_kargo = st.date_input("Tarih Seç",key="saat1")
    gecmis_kargo_bitis = st.date_input("Tarih Seç")
    if gecmis_kargo:
            gecmis_kargo_baslangic = (gecmis_kargo.strftime("%Y-%m-%d")) 
             
    if gecmis_kargo_bitis:
             gecmis_kargo_bitis = (gecmis_kargo_bitis.strftime("%Y-%m-%d"))      
    if st.button("Siparisleri Getir"):            
            #data = supabase.table(supabase_DB).select("*").eq("yazdirma_tarihi", gecmis_kargo_baslangic).execute()
            data = supabase.table(supabase_DB).select("*").gte("yazdirma_tarihi", gecmis_kargo).lte("yazdirma_tarihi", gecmis_kargo_bitis).order("tarih",desc=False).execute()

            data = pd.DataFrame(data.data) 
            if data.empty:
                st.warning("Bu Tarihte Siparişin yok",icon="⚠️")
                
            else : 
                st.dataframe(data[["tarih","yazdirma_tarihi","İSİM SOYİSİM","ADRES","İL","İLÇE","TELEFON","TUTAR","ÜRÜN"]])
                sayı = len(data)            
                st.markdown(f"<h1 style='color: green; font-size: 36px;'>YAZDIRILAN SİPARİŞ SAYISI :  {sayı} </h1>", unsafe_allow_html=True)
