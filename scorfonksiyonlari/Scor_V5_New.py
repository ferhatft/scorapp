import pandas as pd
from departmanlar.models import Departmanlar
from rapor.models import ScorRapor, ScorSayım
from sayim.models import TerminalSayim


def rapor_calistir_new(ham_veri, sorgu_list_, sorgu_ref_, rapor):
    
    is_rapor_envanter = False
    is_sayim_sonrasi = False
    rapor_saha_no = ""
    rapor_saha_kodu = ""
    rapor_department_code = ""
    data_fix = pd.DataFrame()
    basla = pd.DataFrame()
    girdiler = []
    # Excel okuma ile Analiz satırlarını birleştiriyoruz. 1. Bölüm Excel Okuma ve Değişkenleri alma
    data = pd.DataFrame(ham_veri)



    sorgu_ref = sorgu_ref_.reset_index()
    sorgu_list = sorgu_list_.reset_index()
    
    basla_X = data.drop_duplicates(subset=["saha_no", "saha_kodu", "department_code"])
    
    basla = pd.DataFrame(basla_X[["saha_no", "saha_kodu", "department_code"]])
    data_fix = data

    for h in basla.index[0:1]:
        # Envanter dosyasında saha_no ve ID bilgileri alınır
        Saha_Nox = (basla.iloc[h, 0])
        Saha_Kodu = (basla.iloc[h, 1])
        Department = (basla.iloc[h, 2])
        print(Saha_Nox)
        data_fix_1 = pd.DataFrame(data_fix[data_fix['saha_no'] == Saha_Nox])
        print("data_fix_1",data_fix_1)

        for i in sorgu_list.index[0:]:
            Sorgu_Nox = (sorgu_list.iloc[i, 1])
            Kontrol = (sorgu_list.iloc[i, 2])
            Ref_Grup = (sorgu_list.iloc[i, 3])
            Kategori = (sorgu_list.iloc[i, 4])
            Check = (sorgu_list.iloc[i, 5])
            print(Sorgu_Nox)
        # Referans listesinde ki sorgu satırları tabloya alınır
            sorgu_fix_1 = pd.DataFrame(sorgu_ref[sorgu_ref['sorgu_no'] == Sorgu_Nox])
            print("sorgu_fix_1",sorgu_fix_1)
    # Envanter ile Referans sorgu tabloları birleştirilir.
            grupby_data = pd.merge(data_fix_1, sorgu_fix_1, how="inner")
            print("GroupBy Dataas: ",grupby_data)
    # Birleştirilen tabloları da ki referans parç kodlarına göre malzeme toplamları yapılır.
            Ref_Kon = grupby_data.groupby(by=['ref']).sum()['quantity'].reset_index()

            Ref_1 = 0
            Ref_2 = 0
            Ref_3 = 0
            Ref_4 = 0
            Ref_5 = 0
            Ref_6 = 0
            Ref_01 = 0
            Bilgi = ""
            Sonuc = "Kontrol"
        #Birleştirilen tabloda ki genel toplamaların Referans ve toplamların değerleri ayrıştırılır.
            for z in Ref_Kon.index[0:]:
                Ref_x = (Ref_Kon.iloc[z, 0])
                Ref_y = (Ref_Kon.iloc[z, 1])
        #Çıktıda ki Referans bilgileri hangi referanslara yazılacağı tespit edilir.
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
                Ref_Mix = (Ref_1 * Ref_2)
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
                Ref_Min = (Ref_2 + Ref_3 + Ref_4 + Ref_5)
                Ref_Max = ((Ref_2 * 4) + (Ref_3 * 4) + (Ref_4 * 4) + (Ref_5 * 6))
                if not Ref_Min <= Ref_1 <= Ref_Max:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_5":  # Uyumsuz
                Ref_Min = (Ref_1 * 2)
                Ref_Max = (Ref_2 + Ref_3 + Ref_4 + Ref_5 + Ref_6)
                if not Ref_Min == Ref_Max:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_6":  # Uyumsuz
                Ref_Mix = (Ref_1 + Ref_2)
                Ref_Min = (Ref_3 + Ref_4 + Ref_6)
                Ref_Max = (Ref_3 * 2) + (Ref_4 * 2) + Ref_6
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

            elif Check in "Analiz_13":  # Uyumsuz
                Ref_Max = (Ref_1 * 2)
                if not Ref_1 <= Ref_2 <= Ref_Max:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_14":  # Uyumsuz
                Ref_Min = (Ref_2 + Ref_3 + Ref_4 + Ref_5)
                Ref_Max = (Ref_1 * 16)

                if Ref_1 != 0 or Ref_2 != 0:
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
                Ref_Min = (Ref_2 + Ref_3)
                Ref_Max = ((Ref_2 * 2) + (Ref_3 * 4))
                if not Ref_Min <= Ref_1 <= Ref_Max:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_17":  # Akü - Kablo kontrolü 1-(1+4 or 1-2) + 6201
                Ref_Mca = (Ref_1 * Ref_2)
                Ref_Mta = (Ref_1 + Ref_2)
                Ref_Min = ((Ref_2 - 3) + (Ref_3 * 6))
                Ref_Max = ((Ref_2 + 3) + (Ref_3 * 8))

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

            elif Check in "Analiz_19":  #
                if not Ref_1 == Ref_2 and Ref_3 != 0:
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
                if Ref_6 > 0:  # 6201 PDU ve SCU arasında 2 adet Power, SAU ile SCU ve PDU arasında 1'ere adet data kablosu kullanılır.
                    Ref_01 = 2

                Ref_Pow = (Ref_3 + Ref_4 + Ref_5 + Ref_6 + Ref_01)
                Ref_Dat = (Ref_3 + Ref_4 + Ref_5 + Ref_01)

                if Ref_1 != Ref_Pow or Ref_2 != Ref_Dat:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_22":
                Ref_Min = (Ref_4 + Ref_5 + Ref_6)
                Ref_Max = ((Ref_4 * 2) + (Ref_5 * 4) + (Ref_6 * 6))
                if not Ref_1 == Ref_2 and Ref_3 == Ref_Min:
                    Sonuc = "Uyumsuz"
                elif not Ref_Min <= Ref_2 <= Ref_Max:
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
                Ref_Min = ((Ref_2 + Ref_3 + Ref_4 + Ref_5 + Ref_6) * 4)
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
                Ref_Mix = ( Ref_1 + Ref_2 + Ref_3 + Ref_4 + Ref_5)
                if Ref_6 > 0 and Ref_Mix > 0:
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
                elif not Ref_1 == Ref_2 and Ref_Min <= Ref_3:
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
                for g in range(0, 10000, 8):
                    if g == Ref_1:
                        Sonuc = "Uyumlu"
                        break
                    elif g > Ref_1:
                        Sonuc = "Uyumsuz"

            elif Check == "Analiz_38":
                for g in range(0, 10000, 12):
                    if g == Ref_1:
                        Sonuc = "Uyumlu"
                        break
                    elif g > Ref_1:
                        Sonuc = "Uyumsuz"

            elif Check == "Analiz_39":
                Ref_Min = (Ref_3 + Ref_4)
                if not Ref_1 != 0:
                    continue
                elif not Ref_1 <= Ref_2 and Ref_1 <= Ref_Min:
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

            elif Check in "Analiz_45":
                if Ref_1 == 0 or Ref_2 == 0:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Bilgi"

            elif Check == "Analiz_46":
                Ref_Min = (Ref_1 + Ref_2)
                Ref_Max = (Ref_1 + (Ref_2 * 2))
                if not Ref_Min <= Ref_3 <= Ref_Max:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check in "Analiz_47":
                Ref_Min = (Ref_2 + Ref_3 + Ref_4)
                if Ref_1 != 0 and Ref_Min == 0:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Bilgi"

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
                Ref_Max = (Ref_1 * Ref_2 * Ref_3 * Ref_6)
                if Ref_Min == 0:
                    continue
                if not 0 < Ref_Max <= 4:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"

            elif Check == "Analiz_51":  # Uyumsuz
                Ref_Min = (Ref_1 * 2)
                Ref_Max = (Ref_1 * 4)
                if not Ref_Min <= Ref_2 <= Ref_Max:
                    Sonuc = "Uyumsuz"
                else:
                    Sonuc = "Uyumlu"




            rapor_saha_no = Saha_Nox
            rapor_saha_kodu = Saha_Kodu
            rapor_department_code = Department

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

    return girdiler
