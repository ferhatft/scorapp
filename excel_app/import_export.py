import os

import pandas
import xlsxwriter
from django.db.models.query_utils import Q
from django.utils import timezone
from envanter.models import Envanter
from parcakodlari.models import Parcakodu
from scor.settings import BASE_DIR
from sorgu.models import SorguReferanslari, Sorgular
from excel_app.models import  TemporaryExcelFiles
from eht.models import Envanter_Tarihcesi


class ImportExcel:
    """ Excel dosyalarından veri tabanına bilgi atmak amacıyla yazılan class """
    def __init__(self,file):

        self.file = file


        self.file_object = TemporaryExcelFiles.objects.create(file=self.file)
        self.file_object.save()


        self.file_object = self.file_object.file
        excel_file = TemporaryExcelFiles.objects.get(file=self.file_object)
        base = BASE_DIR
        media_url = excel_file.file.url.lstrip('/')

        excel_file = os.path.join(base,media_url)

        start_read = timezone.now()#süre ölçümü

        if 'xlsx' in excel_file:
            read_file = pandas.read_excel(excel_file,engine="openpyxl")
        elif "xls" in excel_file:
            read_file = pandas.read_excel(excel_file)
        elif 'csv' in excel_file:
            read_file = pandas.read_csv(excel_file)
        else:
            return "FileError"

        finish_read = timezone.now()

        total_read = finish_read-start_read
        print("Toplam okuma süresi: ",total_read.total_seconds())


        start_cevir = timezone.now()
        self.dict_data = read_file.to_dict(orient="records")
        finish_cevir = timezone.now()

        total_cevir = finish_cevir - start_cevir

        print("Toplam Sözlüğe çevirme süresi: ",total_cevir.total_seconds())

    def import_parca_kodu(self):
        """
            Parça kodu veri tabanına verileri import etme

        """
        try:
            #Ekipman.objects.all().delete()
            ekipman_listesi = []

            departman = self.dict_data[0]["Department Code"]
            Envanter.objects.filter(department=departman).delete()

            start_bulk = timezone.now()
            for data in self.dict_data:
                ekipman = Envanter(
                        saha_no=data["Saha No"],
                        saha_kodu=data["Saha Kodu"],
                        saha_tipi=data["Saha Tipi"],
                        yer_tipi=data["Ana Yer Tipi"],
                        ekipman_seri_no=data["Ekipman Seri No"],
                        ekipman_parca_kodu=data['Ekipman Parca Kodu'],
                        parca_tanimi=data["Parca Tanimi"],
                        kurulumu_tarihi = data['Sahaya Kurulum Tarihi'],
                        department=data['Department Code'],
                        quantity=data["Quantity"],
                        ustekipman = data['Ustekipman'],
                        )
                ekipman_listesi.append(ekipman)

            #departmen olayının ne olduğunu tam olarak öğren
                if len(ekipman_listesi) > 5000:#toplu kayıt yerine her 5binde bir kayıt edeceğiz.
                    Envanter.objects.bulk_create(ekipman_listesi,batch_size=10000)
                    ekipman_listesi = []

            Envanter.objects.bulk_create(ekipman_listesi,batch_size=9999)

            finish_bulk = timezone.now()

            total_bulk = finish_bulk - start_bulk

            print("Toplam Bulk Süresi: ",total_bulk.total_seconds())
        except:
            return "KeyError"
        finally:
            self.file_object.delete()

    def import_ekipman_hareketi_sarf(self):
        """
            Envanter Parça kodu Hareket Tarihçesi veri tabanına verileri import etme
        """
        try:
            hareket_list = []
            #sÃ¶zlÃ¼k yapsÄ±nda dolaÅŸÄ±p verileri teker teker yazdÄ±rma
            bulk_start = timezone.now()
            #Envanter_Tarihcesi.objects.all().delete()
            for data in self.dict_data:
                try:
                    hareket_line = Envanter_Tarihcesi(
                        islem_no = data['Islem No'],
                        islem_tarihi = data['Islem Tarihi'],
                        parca_kodu = data['Kalem Kodu'],
                        parca_tanimi = data['Kalem Adi'],
                        islem_miktari = data['Islem Miktari'],
                        olcum_birimi = data['Olcum Birimi'],
                        kaynak_yeri = data['Kaynak Stok Yeri'],
                        transfer_yeri = data['Transfer Stok Yeri'],
                        islem_tipi = data['Islem Tipi'],
                        form_no = data['Form No'],
                        kaynak_departman = data['Kaynak Departman'],
                        hedef_departman = data['Hedef Departman'],
                        hedef_lokasyon = data['Hedef Lokasyon'],
                        kullanici_adi = data['Kullanici Adi'],

                        )
                except:
                    return "KeyError"

                hareket_list.append(hareket_line)

                if len(hareket_list) > 5000:
                    Envanter_Tarihcesi.objects.bulk_create(hareket_list,batch_size=9999)
                    hareket_list = []
            Envanter_Tarihcesi.objects.bulk_create(hareket_list,batch_size=9999)

            bulk_finish = timezone.now()

            total_bulk = bulk_finish - bulk_start

            print("Total Bulk: ",total_bulk)
        except:
            return "KeyError"
        finally:
            self.file_object.delete()


    def import_ekipman_hareketi_seri(self):
        """
            Envanter Parça kodu Hareket Tarihçesi veri tabanına verileri import etme
        """
        try:
            hareket_list = []
            #sÃ¶zlÃ¼k yapsÄ±nda dolaÅŸÄ±p verileri teker teker yazdÄ±rma
            bulk_start = timezone.now()
            #Envanter_Tarihcesi.objects.all().delete()
            for data in self.dict_data:
                try:
                    hareket_line = Envanter_Tarihcesi(
                        islem_no = data['Islem No'],
                        islem_tarihi = data['Islem Tarihi'],
                        parca_kodu = data['Kalem Kodu'],
                        parca_tanimi = data['Kalem Adi'],
                        islem_miktari = data['Islem Miktari'],
                        olcum_birimi = data['Olcum Birimi'],
                        kaynak_yeri = data['Kaynak Stok Yeri'],
                        transfer_yeri = data['Transfer Stok Yeri'],
                        islem_tipi = data['Islem Tipi'],
                        form_no = data['Form No'],
                        kaynak_departman = data['Kaynak Departman'],
                        hedef_departman = data['Hedef Departman'],
                        hedef_lokasyon = data['Hedef Lokasyon'],
                        kullanici_adi = data['Kullanici Adi'],
                        seri_no = data['Seri Numarasi']
                        )
                except:
                    return "KeyError"

                hareket_list.append(hareket_line)

                if len(hareket_list) > 5000:
                    Envanter_Tarihcesi.objects.bulk_create(hareket_list,batch_size=9999)
                    hareket_list = []
            Envanter_Tarihcesi.objects.bulk_create(hareket_list,batch_size=9999)

            bulk_finish = timezone.now()

            total_bulk = bulk_finish - bulk_start

            print("Total Bulk: ",total_bulk)
        except:
            return "KeyError"
        finally:
            self.file_object.delete()


    def parca_listesi_kategorileri(self):

        try:

            for data in self.dict_data:
                parca_kodu = data['Ekipman Parca Kodu']
                ana_kategori = data['Ana Kategori']
                alt_kategori = data['Alt Kategori']
                ana_ekipman = data['Ana Ekipman']
                alt_ekipman = data['Alt Ekipman']
                try:
                    #bulk update uygula
                    parca = Parcakodu.objects.get(parca_kodu=parca_kodu)
                    parca.ana_kategori = ana_kategori
                    parca.alt_kategori = alt_kategori
                    parca.ana_ekipman = ana_ekipman
                    parca.alt_ekipman = alt_ekipman
                    parca.save()
                except Parcakodu.DoesNotExist:
                    continue
        except:
            return "KeyError"
        finally:
            self.file_object.delete()


    def import_sorgu_ref(self):

        try:

            ref_list = []

            #sÃ¶zlÃ¼k yapsÄ±nda dolaÅŸÄ±p verileri teker teker yazdÄ±rma
            bulk_start = timezone.now()
            SorguReferanslari.objects.all().delete()
            for data in self.dict_data:
                hareket_line = SorguReferanslari(
                    sorgu_no = data['sorgu_no'],
                    ref = data['ref'],
                    parca_kodu = data['parca_kodu'],
                    parca_tanimi = data['parca_tanimi'],
                    grup_tanimi = data['grup_tanimi'],
                    rapor_tanimi = data['rapor_tanimi'],
                    ref_grup = data['ref_grup'],
                    kategori = data['kategori'],
                    analiz_no = data['analiz_no']

                    )
                ref_list.append(hareket_line)

                if len(ref_list) > 5000:
                    SorguReferanslari.objects.bulk_create(ref_list,batch_size=9999)
                    ref_list = []
            SorguReferanslari.objects.bulk_create(ref_list,batch_size=9999)

            bulk_finish = timezone.now()

            total_bulk = bulk_finish - bulk_start

            print("Total Bulk: ",total_bulk)
        except:
            return "KeyError"
        finally:
            self.file_object.delete()


    def import_sorgu_no(self):

        try:
            sorgu_list = []

            bulk_start = timezone.now()
            Sorgular.objects.all().delete()
            for data in self.dict_data:
                hareket_line = Sorgular(
                    sorgu_no = data['sorgu_no'],
                    kontrol = data['kontrol'],
                    ref_grup = data['ref_grup'],
                    kategori = data['kategori'],
                    analiz_no = data['analiz_no']

                    )
                sorgu_list.append(hareket_line)

                if len(sorgu_list) > 5000:
                    Sorgular.objects.bulk_create(sorgu_list,batch_size=9999)
                    sorgu_list = []

            Sorgular.objects.bulk_create(sorgu_list,batch_size=9999)

            bulk_finish = timezone.now()

            total_bulk = bulk_finish - bulk_start

            print("Total Bulk: ",total_bulk)
        except:
            return "KeyError"
        finally:
            self.file_object.delete()




class ExportExcel:
    """ Excel dosyalarını indirmek amacıyla oluşturulmuş class """

    def get_data(self,saha_num=None):
        if saha_num is None:
            all_objects = Envanter.objects.all()[:10]
        else:
            all_objects = Envanter.objects.filter(Q(saha_no=saha_num) | Q(saha_kodu=saha_num))
        return all_objects

    def generate_excel(self,saha_num=None):

        path=os.path.join(BASE_DIR,\
        'media'+os.sep+'TemporaryExcelKeeper'+\
            os.sep+'Saha_Envanter.xlsx')

        dir_path = os.path.join(BASE_DIR,\
        'media'+os.sep+'TemporaryExcelKeeper')


        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

        workbook = xlsxwriter.Workbook(path)

        worksheet = workbook.add_worksheet()
#eğer dosya yolu bulunamıyorsa yeni bir tane oluştur.
        titles = [
            'Saha No',
            'Saha Kodu',
            'Saha Tipi',
            'Ekipman Seri No',
            'Ekipman Parca Kodu',
            'Parca Tanimi',
            'Department Code',
            'Quantity',
            'Teslim Tarihi',
            'Sahaya Kurulum Tarihi',
            'Ust Ekipman',
            ]
        row = 0
        col = 0

        for title in titles:
            worksheet.write(row,col,title)
            col += 1

        if saha_num is None:
            all_data = self.get_data(saha_num=None)
        else:
            all_data = self.get_data(saha_num=saha_num)
        for data in all_data:
            row += 1
            col = 0

            saha_no = data.saha_no
            saha_kodu = data.saha_kodu
            saha_tipi = data.saha_tipi
            seri_no = data.ekipman_seri_no
            parca_kodu = data.ekipman_parca_kodu
            parca_tanimi = data.parca_tanimi
            department_code = data.department_code
            quantity = data.quantity
            teslim_tarihi = data.kurulumu_tarihi
            sahaya_kurulum_tarihi = data.kurulumu_tarihi
            ust_ekipman = data.ustekipman

            worksheet.write(row,col,saha_no)
            col += 1
            worksheet.write(row,col,saha_kodu)
            col += 1
            worksheet.write(row,col,saha_tipi)
            col += 1
            worksheet.write(row,col,seri_no)
            col += 1
            worksheet.write(row,col,parca_kodu)
            col += 1
            worksheet.write(row,col,parca_tanimi)
            col += 1
            worksheet.write(row,col,department_code)
            col += 1
            worksheet.write(row,col,quantity)
            col += 1
            worksheet.write(row,col,teslim_tarihi)
            col += 1
            worksheet.write(row,col,sahaya_kurulum_tarihi)
            col += 1
            worksheet.write(row,col,ust_ekipman)


        workbook.close()
        return path
