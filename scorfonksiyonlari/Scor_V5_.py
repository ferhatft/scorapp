
from rapor.models import ScorRapor, ScorSayım
from sayim.models import TerminalSayim 
from departmanlar.models import Departmanlar
import pandas as pd


"""
analizler | scorfonksiyonları adı altında yeri değiştirilecek.

"""

def rapor_calistir(ham_veri, sorgu_list_, sorgu_ref_, rapor):
    sorgu_list_ = sorgu_list_.rename(columns={"sorgu_no": "Sorgu_No", "kontrol": "Kontrol", "ref_grup": "Ref_Grup", "kategori": "Kategori", "check": "Check"})
    sorgu_ref_ = sorgu_ref_.rename(columns={"sorgu_no": "Sorgu_No", "ref": "Ref", "ekipman_parca_kodu": "Ekipman Parca Kodu", "parca_tanimi": "Parça Tanımı", "grup_tanimi": "Grup Tanımı", "kategori": "Kategori"})
    is_rapor_envanter = False
    is_sayim_sonrasi = False
    rapor_saha_no = ""
    rapor_saha_kodu = ""
    rapor_department_code = ""
    data_fix = pd.DataFrame()
    girdiler = []
    # Excel okuma ile Analiz satırlarını birleştiriyoruz. 1. Bölüm Excel Okuma ve Değişkenleri alma
    data = ham_veri

    sorgu_ref = sorgu_ref_.reset_index()
    sorgu_list = sorgu_list_.reset_index()
    for col in data.columns:

        if "Saha No" == col:  # Discovery Envanter Dosyası

            data_fix = pd.DataFrame(data[['Saha No', 'Saha Kodu', 'Ekipman Seri No', 'Ekipman Parca Kodu', 'Parca Tanimi',
                                    'Department Code', 'Quantity']])
            data_fix = data_fix.rename(columns={'Ekipman Seri No': 'Seri', 'Department Code': 'Region'}, inplace=False)
            break

        elif "sayim" == col:
            is_sayim_sonrasi = True
            data_fix = pd.DataFrame(data[['saha_no', 'saha_kodu', 'ekipman_seri_no', 'ekipman_parca_kodu', 'parca_tanimi',
                                    'department_code', 'sayim']])
            data_fix = data_fix.rename(
                columns={"saha_no": "Saha No", "saha_kodu": "Saha Kodu", "ekipman_seri_no": "Ekipman Seri No",
                                    "ekipman_parca_kodu": "Ekipman Parca Kodu", "parca_tanimi": "Parca Tanimi",
                                    'department_code': 'Region', "sayim": "Quantity"}, inplace=False)
            break

        elif "Kullanıcı" == col:  # Sayım Sonuç Raporu
            is_rapor_envanter = True
            data_fix = pd.DataFrame(data[['Lokasyon Kodu', 'Kullanıcı', 'Kalem Kodu', 'Kalem Tanımı', 'Varlık Seri No',
                                    'Zimmet Departmanı', 'Miktar', 'Sayım Fark', 'Transfer Edilen Adet', 'Durum', 'Statü',
                                                                        'Sistemde Bulunduğu Yer']])

            data_fix = data_fix.rename(columns={'Lokasyon Kodu': 'Saha No', 'Kullanıcı': 'Saha Kodu', 'Varlık Seri No': 'Ekipman Seri No',
                                                'Kalem Kodu': 'Ekipman Parca Kodu', 'Kalem Tanımı': 'Parca Tanimi',
                                                'Zimmet Departmanı': 'Region', 'Miktar': 'Quantity', 'Sayım Fark': 'Sayım_Fark',
                                                'Transfer Edilen Adet': 'Transfer_Adet', 'Durum': 'Sonuç', 'Statü': 'Durum',
                                                'Sistemde Bulunduğu Yer': 'Lokasyon'}, inplace=False)

            break
        elif "Kullanici" == col:  # ERP Sayım raporu
            is_rapor_envanter = True
            data_fix = pd.DataFrame(data[
                                        ['Lokasyon Kodu', 'Kullanici', 'Kalem Kodu', 'Kalem Tanimi', 'Varlik Seri No', 'Miktar',
                                            'Sayim Fark', 'Transfer Edilen Adet', 'Durum', 'Statü', 'Sistemde Bulundugu Yer',
                                            'Zimmet Departmani']])
            data_fix = data_fix.rename(columns={'Lokasyon Kodu': 'Saha No', 'Kullanici': 'Saha Kodu', 'Varlik Seri No': 'Ekipman Seri No',
                                                'Kalem Kodu': 'Ekipman Parca Kodu', 'Kalem Tanimi': 'Parca Tanimi',
                                                'Zimmet Departmani': 'Region', 'Miktar': 'Quantity', 'Sayim Fark': 'Sayim_Fark',
                                                'Transfer Edilen Adet': 'Transfer_Adet', 'Durum': 'Sonuç',
                                                'Statü': 'Durum', 'Sistemde Bulundugu Yer': 'Lokasyon'
                                                }, inplace=False)
            break

    basla_X = data_fix.drop_duplicates(subset=["Saha No", "Saha Kodu", "Region"])
    basla = pd.DataFrame(basla_X[["Saha No", "Saha Kodu", "Region"]])

    for h in basla.index[0:1]:
        # Envanter dosyasında saha_no ve ID bilgileri alınır
        Saha_Nox = (basla.iloc[h, 0])
        Saha_Kodu = (basla.iloc[h, 1])
        Region = (basla.iloc[h, 2])
        data_fix_1 = pd.DataFrame(data_fix[data_fix['Saha No'] == Saha_Nox])

        for i in sorgu_list.index[0:]:
            Sorgu_Nox = (sorgu_list.iloc[i, 1])
            Kontrol = (sorgu_list.iloc[i, 2])
            Ref_Grup = (sorgu_list.iloc[i, 3])
            Kategori = (sorgu_list.iloc[i, 4])
            Check = (sorgu_list.iloc[i, 5])

        # Referans listesinde ki sorgu satırları tabloya alınır
            sorgu_fix_1 = pd.DataFrame(sorgu_ref[sorgu_ref['Sorgu_No'] == Sorgu_Nox])

    # Envanter ile Referans sorgu tabloları birleştirilir.
            grupby_data = (pd.merge(data_fix_1, sorgu_fix_1, how="inner"))

    # Birleştirilen tabloları da ki referans parç kodlarına göre malzeme toplamları yapılır.
            Ref_Kon = grupby_data.groupby(by=['Ref']).sum()['Quantity'].reset_index()

            Ref_1 = 0
            Ref_2 = 0
            Ref_3 = 0
            Ref_4 = 0
            Ref_5 = 0
            Ref_6 = 0
            Ref_01 = 0
            Sonuc = "Kontrol"

        # Birleştirilen tabloda ki genel toplamaların Referans ve toplamların değerleri ayrıştırılır.
            for z in Ref_Kon.index[0:]:
                Ref_x = (Ref_Kon.iloc[z, 0])
                Ref_y = (Ref_Kon.iloc[z, 1])
        # Çıktıda ki Referans bilgileri hangi referanslara yazılacağı tespit edilir.
                if Ref_x == 'Ref_1':
                    Ref_1 = Ref_y
                elif Ref_x == 'Ref_2':
                    Ref_2 = Ref_y
                elif Ref_x == 'Ref_3':
                    Ref_3 = Ref_y
                elif Ref_x == 'Ref_4':
                    Ref_4 = Ref_y
                elif Ref_x == 'Ref_5':
                    Ref_5 = Ref_y
                elif Ref_x == 'Ref_6':
                    Ref_6 = Ref_y
                elif Ref_x == 'Ref_01':
                    Ref_01 = Ref_y

            if Ref_1 + Ref_2 + Ref_3 + Ref_4 + Ref_5 + Ref_6 == 0:
                continue

        # Excel okuma ile Analiz satırlarını birleştiriyoruz. 2. Bölüm Değişkenler ile analiz ve rapor souşturma

            elif Check == "Analiz_1":  # Uyumsuz
                Ref_Mix = (Ref_1 * (Ref_2 + Ref_3))
                if Ref_Mix == 0:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "İncele"

            elif Check == "Analiz_2":  # Uyumsuz
                Ref_Min = (Ref_1 + Ref_2 + Ref_3 + Ref_4)
                Ref_Max = (Ref_1 * Ref_2 * Ref_3 * Ref_4 * Ref_6)
                if Ref_Min == 0:
                    continue
                if not 0 < Ref_Max < 2:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_3":
                Ref_Min = (Ref_2 + Ref_3 + Ref_4 + Ref_5 + Ref_6)
                if Ref_1 != Ref_Min:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_4":  # Uyumsuz
                Ref_Min = (Ref_2 + Ref_3 + Ref_4 + Ref_5 + Ref_6)
                Ref_Max = (Ref_2 * 4) + (Ref_3 * 4) + (Ref_4 * 4) + (Ref_5 * 6) + (Ref_6 * 8)
                if not Ref_Min <= Ref_1 <= Ref_Max:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_5":  # Uyumsuz
                Ref_Min = (Ref_1 * 2)
                Ref_Max = (Ref_2 + Ref_3 + Ref_4 + Ref_5 + Ref_6)
                if not Ref_1 <= Ref_Max <= Ref_Min:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_6":  # Uyumsuz
                Ref_Mix = (Ref_1 + Ref_2)
                Ref_Min = (Ref_3 + Ref_4 + Ref_6)
                Ref_Max = (Ref_3 * 2) + (Ref_4 * 2) + (Ref_5 + Ref_6)
                if Ref_Min <= Ref_Mix <= Ref_Max:
                    Sonuc = "Uyumlu"
                else:
                    Sonuc = "Uyumsuz"

            elif Check == "Analiz_7":  # Uyumsuz
                Ref_Mix = (Ref_2 + Ref_3 + Ref_4 + Ref_5 + Ref_6)
                Ref_Min = (Ref_2 + Ref_3 + Ref_4 + Ref_5)
                Ref_Max = ((Ref_2 * 6) + (Ref_3 * 6) + (Ref_4 * 6) + (Ref_5 * 6))
                if Ref_Mix == 0:
                    continue
                if not Ref_Min <= Ref_1 <= Ref_Max:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_8":  # Uyumsuz
                Ref_Min = (Ref_2 + Ref_3 + Ref_4 + Ref_5 + Ref_6)
                if Ref_1 == 0:
                    continue
                elif not Ref_1 <= Ref_Min:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_9":  # Uyumsuz
                Ref_Mix = (Ref_1 + Ref_2)
                Ref_Min = (Ref_3 + Ref_4 + Ref_5)
                Ref_Max = ((Ref_3 * 4) + (Ref_4 * 4) + (Ref_5 * 4))
                if Ref_Mix == 0:
                    continue
                if not Ref_Min <= Ref_Mix <= Ref_Max:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_10":  # Uyumsuz
                Ref_Min = (Ref_2 + Ref_3)
                Ref_Mix = (Ref_1 * 3)
                Ref_Max = (Ref_1 * 2)

                if Ref_2 != 0 and Ref_3 != 0:
                    if not Ref_1 <= Ref_Min <= Ref_Mix:
                        Sonuc = "Uyumsuz"
                    else:
                        Sonuc = 'Uyumlu'

                elif Ref_2 == 0 and Ref_3 != 0:
                    if not Ref_1 == Ref_3:
                        Sonuc = "Uyumsuz"
                    else:
                        Sonuc = 'Uyumlu'

                elif Ref_2 != 0 and Ref_3 == 0:
                    if not Ref_1 <= Ref_2 <= Ref_Max:
                        Sonuc = "Uyumsuz"
                    else:
                        Sonuc = 'Uyumlu'
                elif Ref_Min == 0:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_11":  # Uyumsuz
                Ref_Max = (((Ref_2 * 2) + (Ref_3 * 4) + (Ref_4 * 2) + Ref_5) - Ref_6)
                if Ref_2 == 0:
                    continue
                elif not Ref_1 == Ref_Max:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_12":  # Uyumsuz
                Ref_Max = ((Ref_2 * 2) + (Ref_3 * 2) + (Ref_4 * 2) + (Ref_5 * 2))
                if not Ref_1 == Ref_Max:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_13":  # Uyumsuz
                Ref_Max = (Ref_1 * 2)
                if not Ref_1 <= Ref_2 <= Ref_Max:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_14":  # Uyumsuz
                Ref_Min = (Ref_2 + Ref_3 + Ref_4 + Ref_5)
                Ref_Max = (Ref_1 * 16)

                if Ref_1 == 0:
                    continue

                elif Ref_1 != 0 and Ref_Min != 0:
                    if Ref_1 <= Ref_Min <= Ref_Max:
                        Sonuc = "Uyumlu"
                    else:
                        Sonuc = "Uyumsuz"

            elif Check == "Analiz_15":  # Uyumsuz
                Ref_Min = (Ref_2 + Ref_3 + Ref_4 + Ref_5)
                Ref_Max = ((Ref_2 * 2) + (Ref_3 * 5) + (Ref_4 * 18))
                if not Ref_Min <= Ref_1 <= Ref_Max:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_16":  # Uyumsuz
                Ref_Min = (Ref_2 + Ref_3 + Ref_4)
                Ref_Max = ((Ref_2 * 2) + (Ref_3 * 4) + (Ref_4 * 8))
                if not Ref_Min <= Ref_1 <= Ref_Max:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_17":  # Akü - Kablo kontrolü 1-(1+4 or 1-2) + 6201
                Ref_Mca = (Ref_1 * Ref_2)
                Ref_Mta = (Ref_1 + Ref_2)
                Ref_Min = ((Ref_2 - 3) + (Ref_3 * 6))
                Ref_Max = ((Ref_2 + 5) + (Ref_3 * 8))

                if Ref_Mca == 0 and Ref_Mta == 0:
                    continue

                if Ref_Mca == 0 and Ref_Mta > 0:
                    Sonuc = "Uyumsuz"
                elif not Ref_Min <= Ref_1 <= Ref_Max:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_18":  #
                    Sonuc = "Bilgi"

            elif Check == "Analiz_19":  #
                if not Ref_1 == Ref_2 and not Ref_3 != 0:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_20":  #
                Ref_Mix = (Ref_1 * Ref_2)
                if not Ref_01 == 0:
                    if Ref_Mix == 0:
                        Sonuc = "Uyumsuz"
                    else:
                        Sonuc = "İncele"
                else:
                    continue

            elif Check == "Analiz_21":  #
                Ref_Dat = (Ref_3 + Ref_4 + Ref_5)
                Ref_Dat_max = (Ref_3 + Ref_4 + Ref_5)

                if Ref_6 > 0:  # 6201 PDU ve SCU arasında 2 adet Power, SAU ile SCU ve PDU arasında 1'ere adet data kablosu kullanılır.
                    Ref_01 = 2
                    Ref_Dat_max = (Ref_3 + Ref_4 + Ref_5 + Ref_01)

                Ref_Pow = (Ref_3 + Ref_4 + Ref_5 + Ref_6 + Ref_01)

                if not Ref_1 == Ref_Pow or not Ref_Dat <= Ref_2 <= Ref_Dat_max:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_22":
                Ref_Min = (Ref_4 + Ref_5 + Ref_6)
                if Ref_1 != Ref_2 or Ref_3 != Ref_Min:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_23":  #
                Ref_Min = (Ref_2 + (Ref_3 / 2))
                if not Ref_1 == Ref_Min:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_24":  #
                Ref_Min = ((Ref_2 + Ref_3) * 4) - (Ref_4 * 4)
                if not Ref_1 == Ref_Min:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_25":
                if Ref_1 != Ref_2:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_26":
                Ref_Min = Ref_1 * Ref_2 * Ref_3
                if Ref_01 > 0:
                    if Ref_Min == 0:
                        Sonuc = "Uyumsuz"
                    else:
                        Sonuc = "Uyumlu"
                else:
                    continue

            elif Check == "Analiz_27":
                Ref_Min = (Ref_2 + Ref_3 + Ref_4 + Ref_5)
                Ref_Max = ((Ref_2 * 4) + (Ref_3 * 8) + (Ref_4 * 4) + (Ref_5 * 4))
                if not Ref_Min <= Ref_1 <= Ref_Max:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_28":
                Ref_Min = (Ref_1 + Ref_2)
                Ref_Max = ((Ref_3 * 2) + (Ref_4 * 4) + (Ref_5 * 20))
                if Ref_Min == 0:
                    continue
                elif not Ref_Min <= Ref_Max:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_29":
                Ref_Min = (Ref_2 + Ref_3 + Ref_4 + Ref_5 + Ref_6)
                Ref_Max = (Ref_2 * 1) + ((Ref_3 * 2) + (Ref_4 * 10) + (Ref_5 * 6) + (Ref_6 * 5))
                if not Ref_Min <= Ref_1 <= Ref_Max:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_30":
                Ref_Min = (Ref_1 + Ref_2 + Ref_3)
                Ref_Max = (Ref_4 + Ref_5 + Ref_6)
                if not Ref_Min == Ref_Max:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_31":  #
                Ref_Max = (Ref_3 * 2)
                Ref_Mix = (Ref_1 + Ref_2 + Ref_3 + Ref_4 + Ref_5)

                if Ref_Mix == 0:
                    continue

                elif Ref_6 != 0 and Ref_Mix != 0:
                    if Ref_2 != Ref_6 or Ref_2 != Ref_5:
                        Sonuc = "Uyumsuz"
                    else:
                        Sonuc = "Uyumlu"

                elif Ref_6 == 0:
                    if Ref_1 != Ref_2 or Ref_1 != Ref_5 or Ref_Max != Ref_4:
                        Sonuc = "Uyumsuz"
                    else:
                        Sonuc = "Uyumlu"

            elif Check == "Analiz_32":
                if Ref_1 + Ref_3 != Ref_2 + Ref_4:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_33":
                Ref_Min = (Ref_1 * 2)
                if Ref_1 == 0:
                    continue
                elif not Ref_1 == Ref_2 and not Ref_Min <= Ref_3:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_34":
                if Ref_01 == 0:
                    continue
                else:
                    Sonuc = "İncele"

            elif Check == "Analiz_35":
                for g in range(0, 10000, 4):
                    if g == Ref_1:
                        Sonuc = "Uyumlu"
                        break
                    elif g > Ref_1:
                        Sonuc = "Uyumsuz"

            elif Check == "Analiz_36":
                if Ref_1 * Ref_2 == 0:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "İncele"

            elif Check == "Analiz_37":
                for g in range(0, 10000, 4):
                    if g == Ref_1:
                        Sonuc = "Uyumlu"
                        break
                    elif g > Ref_1:
                        Sonuc = "Uyumsuz"

            elif Check == "Analiz_38":
                for g in range(0, 10000, 6):
                    if g == Ref_1:
                        Sonuc = "Uyumlu"
                        break
                    elif g > Ref_1:
                        Sonuc = "Uyumsuz"

            elif Check == "Analiz_39":
                Ref_Min = (Ref_3 + Ref_4)
                if not Ref_1 != 0:
                    continue
                elif not Ref_1 <= Ref_2 and not Ref_1 <= Ref_Min:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_40":
                Ref_Min = ((Ref_1 + Ref_2 + Ref_3 + Ref_4) * Ref_5)
                Ref_Max = ((Ref_1 + Ref_2 + Ref_3 + Ref_4) * Ref_6)
                Ref_Mix = (Ref_5 * Ref_6)
                if Ref_Min == 0 or Ref_Max == 0 or Ref_Mix == 0:
                    Sonuc = "Uyumlu"
                else:
                    Sonuc = "Uyumsuz"

            elif Check == "Analiz_41":
                if Ref_2 != 0:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_42":
                Ref_Min = (Ref_2 + Ref_3 + Ref_4 + Ref_5 + Ref_6)
                Ref_Max = (Ref_1 * 2)
                if not Ref_1 <= Ref_Min <= Ref_Max:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_43":
                Ref_Min = (Ref_2 + Ref_3 + Ref_4)
                if not Ref_Min == Ref_1:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_44":
                Ref_Min = (Ref_2 + Ref_3)
                if Ref_1 == 0:
                    continue
                if not Ref_1 <= Ref_Min:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_45":
                if Ref_1 == 0 or Ref_2 == 0:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "İncele"

            elif Check == "Analiz_46":
                Ref_Min = (Ref_1 + Ref_2)
                Ref_Max = (Ref_1 + (Ref_2 * 2))
                if not Ref_Min <= Ref_3 <= Ref_Max:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_47":
                Ref_Min = (Ref_2 + Ref_3 + Ref_4)
                if Ref_1 == 0:
                    continue

                elif Ref_1 != 0 and Ref_Min == 0:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_48":
                Ref_Min = (Ref_2 * 2)

                if Ref_Min == Ref_1:
                    Sonuc = "Uyumlu"
                else:
                    Sonuc = "Uyumsuz"

            elif Check == "Analiz_49":
                Ref_Min = (Ref_2 + Ref_3 + Ref_4 + Ref_5 + Ref_6)

                if Ref_Min <= Ref_1:
                    Sonuc = "Uyumlu"
                else:
                    Sonuc = "Uyumsuz"

            elif Check == "Analiz_50":  # Uyumsuz
                Ref_Min = (Ref_1 + Ref_2 + Ref_3)
                Ref_Max = (Ref_1 + Ref_2 + Ref_3 + Ref_5 + Ref_6)
                if Ref_Min == 0:
                    continue
                if not 0 < Ref_Max <= 5:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_51":  # Uyumsuz
                Ref_Min = (Ref_1 * 2)
                if Ref_Min != Ref_2:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_52":  # Uyumsuz
                Ref_Mix = (Ref_1 + Ref_3 + Ref_4 + Ref_5)

                if Ref_Mix != 4 or Ref_2 == 0:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_53":  # Uyumsuz

                if Ref_1 == 0:
                    continue
                elif not Ref_1 <= Ref_2 <= Ref_1 * 12:
                    Sonuc = "Uyumsuz"
                elif not Ref_2 <= Ref_3 <= Ref_2 * 2:
                    Sonuc = "Uyumsuz"
                elif not Ref_1 <= Ref_4 <= Ref_1 * 2:
                    Sonuc = "Uyumsuz"
                elif Ref_5 != Ref_1:
                    Sonuc = "Uyumsuz"
                elif Ref_6 != Ref_1:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_54":  # Uyumsuz
                if Ref_1 == 0:
                    continue

                elif not 0 <= Ref_2 <= (Ref_1 * 6):
                    Sonuc = "Uyumsuz"
                elif Ref_3 != Ref_1:
                    Sonuc = "Uyumsuz"
                elif not Ref_4 == Ref_1:
                    Sonuc = "Uyumsuz"
                elif Ref_5 != Ref_1:
                    Sonuc = "Uyumsuz"
                elif Ref_6 != (Ref_1 * 2):
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_55":  # Uyumsuz
                if Ref_1 == 0:
                    continue
                elif not 1 <= Ref_2 <= (Ref_1 * 3):
                    Sonuc = "Uyumsuz"
                elif Ref_3 != Ref_1:
                    Sonuc = "Uyumsuz"
                elif Ref_4 != Ref_1:
                    Sonuc = "Uyumsuz"
                elif Ref_5 != Ref_1:
                    Sonuc = "Uyumsuz"
                elif Ref_6 != Ref_1:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_56":
                if Ref_1 != Ref_2:
                    Sonuc = "Uyumsuz"
                elif not Ref_2 != Ref_3:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_57":  # Uyumsuz
                if Ref_1 == 0:
                    continue

                elif not Ref_2 == Ref_1:
                    Sonuc = "Uyumsuz"
                elif not 1 <= Ref_3 <= (Ref_1 * 6):
                    Sonuc = "Uyumsuz"
                elif Ref_4 != Ref_1:
                    Sonuc = "Uyumsuz"
                elif Ref_5 != Ref_1:
                    Sonuc = "Uyumsuz"
                elif Ref_6 != Ref_1:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_58":  # Uyumsuz
                if Ref_1 == 0:
                    continue

                elif Ref_2 != Ref_1:
                    Sonuc = "Uyumsuz"
                elif not 1 <= Ref_3 <= (Ref_1 * 6):
                    Sonuc = "Uyumsuz"
                elif Ref_4 != Ref_1:
                    Sonuc = "Uyumsuz"
                elif Ref_5 != (Ref_1 * 3):
                    Sonuc = "Uyumsuz"
                elif Ref_6 != Ref_1:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_59":  # Uyumsuz
                if Ref_1 == 0:
                    continue
                elif Ref_2 != Ref_1:
                    Sonuc = "Uyumsuz"
                elif not Ref_1 <= Ref_3 <= (Ref_1 * 6):
                    Sonuc = "Uyumsuz"
                elif Ref_4 != Ref_1:
                    Sonuc = "Uyumsuz"
                elif not Ref_1 <= Ref_5 <= (Ref_1 * 3):
                    Sonuc = "Uyumsuz"
                elif not Ref_1 <= Ref_6 == (Ref_1 * 4):
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_60":  # Uyumsuz
                if Ref_2 != Ref_1:
                        Sonuc = "Uyumsuz"
                elif Ref_1 != 0:
                    if not Ref_1 <= Ref_3 <= (Ref_1 * 3):
                        Sonuc = "Uyumsuz"
                    Sonuc = "Uyumlu"
                elif Ref_6 != 0:
                    if not Ref_6 <= Ref_3 <= (Ref_6 * 3):
                        Sonuc = "Uyumsuz"
                    Sonuc = "Uyumlu"
                elif Ref_4 != Ref_6:
                    Sonuc = "Uyumsuz"
                elif Ref_5 != Ref_6:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_61":  # Uyumsuz
                Ref_Max = (Ref_2 + Ref_3 + Ref_4 + Ref_5 + Ref_6)
                if Ref_1 == 0:
                    continue
                elif Ref_Max == 0:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_62":
                if Ref_1 != Ref_2 or Ref_3 < 1:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_63":
                if Ref_1 != Ref_2 or Ref_3 == 0 or Ref_1 != Ref_4:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            rapor_saha_no = Saha_Nox
            rapor_saha_kodu = Saha_Kodu
            rapor_department_code = Region

            if is_rapor_envanter:
                if str(Saha_Nox) != str(rapor.child.saha_no):
                    raise Exception("Kontrol Raporuyla Kontrol Edilen Raporun Saha No'su Aynı Değil!")
            girdi = ScorRapor(saha_no=Saha_Nox, saha_kod=Saha_Kodu, ref_1=Ref_1, ref_2=Ref_2, ref_3=Ref_3, ref_4=Ref_4, ref_5=Ref_5, ref_6=Ref_6, ref_grup=Ref_Grup, sonuc=Sonuc, kontrol=Kontrol, kategori=Kategori, sorgu_no=Sorgu_Nox, rapor=rapor)

            if is_sayim_sonrasi:
                girdi.is_sayim_sonrasi = True

            girdi.save()
            girdiler.append(girdi)

# Parça Kodlarını Rapora eklenecek <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<

            # parca_kod_list = grupby_data.groupby(by=['Ekipman Parca Kodu', 'Parca Tanimi', 'Ref']).sum()['Quantity'].reset_index()
            # Ref_1 = 0
            # Ref_2 = 0
            # Ref_3 = 0
            # Ref_4 = 0
            # Ref_5 = 0
            # Ref_6 = 0
            # # Birleştirilen tabloda ki genel toplamaların Referans ve toplamların değerleri ayrıştırılır.
            # for f in parca_kod_list.index[0:]:
            #     Ref_Grup = (parca_kod_list.iloc[f, 0])
            #     Kontrol = (parca_kod_list.iloc[f, 1])
            #     Ref_x = (parca_kod_list.iloc[f, 2])
            #     Ref_y = (parca_kod_list.iloc[f, 3])
            #     # Çıktıda ki Referans bilgileri hangi referanslara yazılacağı tespit edilir.
            #     if Ref_x == 'Ref_1':
            #         Ref_1 = Ref_y
            #     elif Ref_x == 'Ref_2':
            #         Ref_2 = Ref_y
            #     elif Ref_x == 'Ref_3':
            #         Ref_3 = Ref_y
            #     elif Ref_x == 'Ref_4':
            #         Ref_4 = Ref_y
            #     elif Ref_x == 'Ref_5':
            #         Ref_5 = Ref_y
            #     elif Ref_x == 'Ref_6':
            #         Ref_6 = Ref_y
            #     df2 = pd.DataFrame({"Saha_No": [Saha_No], "Saha_Kodu": [Saha_Kodu], "1-": [Ref_1], "2-": [Ref_2], "3-": [Ref_3], "4-": [Ref_4], "5-": [Ref_5], "6-": [Ref_6], "Ref_Grup": [Ref_Grup], "Sonuc": [Sonuc], "Kontrol": [Kontrol], "Kategori": [Kategori], "Sorgu_No": [Sorgu_No], "Bilgi": [Ref_x]})
            #     df = df.append(df2)
            #     Ref_1 = 0
            #     Ref_2 = 0
            #     Ref_3 = 0
            #     Ref_4 = 0
            #     Ref_5 = 0
            #     Ref_6 = 0
# Parça Kodlarını Rapora eklenecek <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<

#     return Region
#
#
# def exportexcel(Region):
#     print(Region)
#
#     global df
#     global data_fix
#
# #    print(data_fix)
#
#     print(Region)

    if not is_sayim_sonrasi:
        for i in data_fix.index[0:]:
            saha_no = (data_fix.iloc[i, 0])
            saha_kod = (data_fix.iloc[i, 1])
            ekipman_seri_no = (data_fix.iloc[i, 2])
            ekipman_parca_kodu = (data_fix.iloc[i, 3])
            parca_tanimi = (data_fix.iloc[i, 4])
            department_code = (data_fix.iloc[i, 5])
            quantity = (data_fix.iloc[i, 6])

            rapor_saha_kodu = saha_kod
            rapor_saha_no = saha_no
            rapor_department_code = department_code

            sayim_girdi = ScorSayım(saha_no=saha_no, saha_kodu=saha_kod, ekipman_seri_no=ekipman_seri_no, ekipman_parca_kodu=ekipman_parca_kodu, parca_tanimi=parca_tanimi, department_code=department_code, quantity=quantity, aciklama="", sayim=quantity, rapor=rapor)
            sayim_girdi.save()

    if is_rapor_envanter:
        for i in data_fix.index[0:]:
            Saha_No = (data_fix.iloc[i, 0])
            User = (data_fix.iloc[i, 1])
            Seri_No = (data_fix.iloc[i, 4])
            Parca_Kodu = (data_fix.iloc[i, 2])
            Parca_Tanimi = (data_fix.iloc[i, 3])
            Bolge = (data_fix.iloc[i, 5])
            Miktar = (data_fix.iloc[i, 6])
            Sayim_Fark = (data_fix.iloc[i, 7])
            Transfer_Adet = (data_fix.iloc[i, 8])
            Sonuc = (data_fix.iloc[i, 9])
            Durum = (data_fix.iloc[i, 10])
            Lokasyon = (data_fix.iloc[i, 11])
            Lokasyon = str(Lokasyon).replace(".0", "")
            rapor_envanter_girdi = TerminalSayim(saha_no=Saha_No, user=User, seri_no=Seri_No, parca_kodu=Parca_Kodu, parca_tanimi=Parca_Tanimi, bolge=Bolge, miktar=Miktar, sayim_fark=Sayim_Fark, transfer_adet=Transfer_Adet, durum=Durum, sonuc=Sonuc, lokasyon=Lokasyon, rapor=rapor)

            rapor_department_code = Bolge
            rapor_envanter_girdi.save()
            rapor_saha_no = Saha_No
            rapor_saha_kodu = User

    rapor.saha_no = rapor_saha_no
    rapor.saha_kod = rapor_saha_kodu
    rapor.department_code = Departmanlar.objects.get(code=rapor_department_code)
    rapor.save()

    return girdiler
