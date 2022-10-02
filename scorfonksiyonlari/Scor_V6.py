import datetime

import pandas as pd
from rapor.models import GlobalSayimRapor
from sorgu.models import SorguReferanslari, Sorgular

from envanter.models import Envanter


def rapor_calistir_V6():

    start = datetime.datetime.today()

    sorgu_list = pd.DataFrame(Sorgular.objects.all().values("sorgu_no", "kontrol", "ref_grup", "kategori", "check"))
    sorgu_ref = pd.DataFrame(SorguReferanslari.objects.all().values("sorgu_no", "ref", "ekipman_parca_kodu"))
 
    """
        XXX = Envanter.objects.in_bulk().exclude(yer_tipi="CN SAHA").all().values("saha_no","saha_kodu","department_code").distinct()
    print(XXX)"""

    all_saha_list = pd.DataFrame(Envanter.objects.exclude(yer_tipi="CN SAHA").all().values("saha_no","saha_kodu","department_code","yer_tipi").distinct())
    print(all_saha_list)

    for saha in all_saha_list.to_dict(orient="records"):
        Saha_Nox = saha["saha_no"]
        Saha_Kodu = saha["saha_kodu"]
        Departman = saha["department_code"]
        print(Saha_Nox + " " + Saha_Kodu + " " + Departman)
        
        saha_envanter = pd.DataFrame(Envanter.objects.filter(saha_no=Saha_Nox).values())

        referans_envanter = pd.merge(sorgu_ref, saha_envanter, how="inner")
        referans_sorgu = pd.merge(sorgu_list, referans_envanter, how="inner")
        referans_sorgu = referans_sorgu.drop_duplicates(subset=["sorgu_no"])

        for sorgu in referans_sorgu.to_dict(orient="records"):
            Sorgu_Nox = sorgu["sorgu_no"]
            Kontrol = sorgu["kontrol"]
            Ref_Grup = sorgu["ref_grup"]
            Kategori = sorgu["kategori"]
            Check = sorgu["check"]
        # Referans listesinde ki sorgu satırları tabloya alınır
            saha_sorgu_referans = pd.DataFrame(sorgu_ref[sorgu_ref['sorgu_no'] == Sorgu_Nox])

    # Envanter ile Referans sorgu tabloları birleştirilir.
            grupby_data = pd.merge(saha_envanter, saha_sorgu_referans, how="inner")

    # Birleştirilen tabloları da ki referans parç kodlarına göre malzeme toplamları yapılır.
            Ref_Kon = grupby_data.groupby(by=['ref']).sum()['quantity'].reset_index()

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

      
            girdi = GlobalSayimRapor(saha_no=Saha_Nox, saha_kod=Saha_Kodu, ref_1=Ref_1, ref_2=Ref_2, ref_3=Ref_3, ref_4=Ref_4, ref_5=Ref_5, ref_6=Ref_6, ref_grup=Ref_Grup, sonuc=Sonuc, kontrol=Kontrol, kategori=Kategori, sorgu_no=Sorgu_Nox,department_code=Departman)
            girdi.save()
            
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
    stop = datetime.datetime.today()
    time = stop - start
    print(time)

    return
