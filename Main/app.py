# https://github.com/ZBGoztas/Ansys_Macro.git
from OCC.Core.BRepGProp import brepgprop_VolumeProperties,brepgprop_SurfaceProperties,brepgprop_LinearProperties
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.GProp import GProp_GProps
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_EDGE
from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.GCPnts import GCPnts_AbscissaPoint
from OCC.Core.BRep import BRep_Tool
from OCC.Core.BRepCheck import BRepCheck_Analyzer
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Display.SimpleGui import init_display
import subprocess
from PyQt5.QtWidgets import *  
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
# AII
import joblib
from sklearn.multioutput import MultiOutputRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import pandas as pd
##########################
from ansys.mechanical.core import launch_mechanical, App, find_mechanical, global_variables
import textwrap
##################################
import threading
import time
import sys
import csv
import os
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "<local-path>"
os.environ["QT_QPA_PLATFORM"] = "windows"


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 750)
        
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Ana Layout - Tüm arayüzü kapsayan dikey düzen
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.mainLayout.setSpacing(10)

        # --- Bölüm 1: Geometrik Özellikler ---
        self.groupBox_Geo = QGroupBox(self.centralwidget)
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_Geo)
        
        self.label_15 = QLabel(self.groupBox_Geo)
        font = QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_15.setFont(font)
        self.label_15.setAlignment(Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.verticalLayout_4.addWidget(self.label_15)
        
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_2 = QHBoxLayout()
        
        self.verticalLayout = QVBoxLayout()
        # Etiketler
        self.label_hacim = QLabel(self.groupBox_Geo)
        self.label_hacim.setFont(font)
        self.label_hacim.setObjectName("label_hacim")
        self.verticalLayout.addWidget(self.label_hacim)
        
        self.label_YuzeyAlani = QLabel(self.groupBox_Geo)
        self.label_YuzeyAlani.setFont(font)
        self.label_YuzeyAlani.setObjectName("label_YuzeyAlani")
        self.verticalLayout.addWidget(self.label_YuzeyAlani)
        
        self.label_KarmasiklikKatSaysi = QLabel(self.groupBox_Geo)
        self.label_KarmasiklikKatSaysi.setFont(font)
        self.label_KarmasiklikKatSaysi.setObjectName("label_KarmasiklikKatSaysi")
        self.verticalLayout.addWidget(self.label_KarmasiklikKatSaysi)
        
        self.label_MinCap = QLabel(self.groupBox_Geo)
        self.label_MinCap.setFont(font)
        self.label_MinCap.setObjectName("label_MinCap")
        self.verticalLayout.addWidget(self.label_MinCap)
        
        self.label_MaksCap = QLabel(self.groupBox_Geo)
        self.label_MaksCap.setFont(font)
        self.label_MaksCap.setObjectName("label_MaksCap")
        self.verticalLayout.addWidget(self.label_MaksCap)
        
        self.label_KisaKenar = QLabel(self.groupBox_Geo)
        self.label_KisaKenar.setFont(font)
        self.label_KisaKenar.setObjectName("label_KisaKenar")
        self.verticalLayout.addWidget(self.label_KisaKenar)
        
        self.label_UzunKenar = QLabel(self.groupBox_Geo)
        self.label_UzunKenar.setFont(font)
        self.label_UzunKenar.setObjectName("label_UzunKenar")
        self.verticalLayout.addWidget(self.label_UzunKenar)
        
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        
        self.verticalLayout_2 = QVBoxLayout()
        # Sonuçlar
        self.label_Hacim_Sonuc = QLabel(self.groupBox_Geo)
        self.label_Hacim_Sonuc.setFont(font)
        self.label_Hacim_Sonuc.setObjectName("label_Hacim_Sonuc")
        self.verticalLayout_2.addWidget(self.label_Hacim_Sonuc)
        
        self.label_YuzeyAlani_Sonuc = QLabel(self.groupBox_Geo)
        self.label_YuzeyAlani_Sonuc.setFont(font)
        self.label_YuzeyAlani_Sonuc.setObjectName("label_YuzeyAlani_Sonuc")
        self.verticalLayout_2.addWidget(self.label_YuzeyAlani_Sonuc)
        
        self.label_Karmasiklik_Sonuc = QLabel(self.groupBox_Geo)
        self.label_Karmasiklik_Sonuc.setFont(font)
        self.label_Karmasiklik_Sonuc.setObjectName("label_Karmasiklik_Sonuc")
        self.verticalLayout_2.addWidget(self.label_Karmasiklik_Sonuc)
        
        self.label_MinCap_Sonuc = QLabel(self.groupBox_Geo)
        self.label_MinCap_Sonuc.setFont(font)
        self.label_MinCap_Sonuc.setObjectName("label_MinCap_Sonuc")
        self.verticalLayout_2.addWidget(self.label_MinCap_Sonuc)
        
        self.label_MaksCap_Sonuc = QLabel(self.groupBox_Geo)
        self.label_MaksCap_Sonuc.setFont(font)
        self.label_MaksCap_Sonuc.setObjectName("label_MaksCap_Sonuc")
        self.verticalLayout_2.addWidget(self.label_MaksCap_Sonuc)
        
        self.label_KisaKenar_Sonuc = QLabel(self.groupBox_Geo)
        self.label_KisaKenar_Sonuc.setFont(font)
        self.label_KisaKenar_Sonuc.setObjectName("label_KisaKenar_Sonuc")
        self.verticalLayout_2.addWidget(self.label_KisaKenar_Sonuc)
        
        self.label_UzunKenar_Sonuc = QLabel(self.groupBox_Geo)
        self.label_UzunKenar_Sonuc.setFont(font)
        self.label_UzunKenar_Sonuc.setObjectName("label_UzunKenar_Sonuc")
        self.verticalLayout_2.addWidget(self.label_UzunKenar_Sonuc)
        
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        
        self.verticalLayout_3 = QVBoxLayout()
        self.pushButton_DosyaSec = QPushButton(self.groupBox_Geo, clicked= lambda : threading.Thread(target=self.dosyaSec()).start())
        self.pushButton_DosyaSec.setFont(font)
        self.pushButton_DosyaSec.setObjectName("pushButton_DosyaSec")
        self.verticalLayout_3.addWidget(self.pushButton_DosyaSec)
        
        self.pushButton_DosyaGoruntule = QPushButton(self.groupBox_Geo, clicked = lambda : threading.Thread(target=self.OpenStep()).start())
        self.pushButton_DosyaGoruntule.setFont(font)
        self.pushButton_DosyaGoruntule.setFocusPolicy(Qt.StrongFocus)
        self.pushButton_DosyaGoruntule.setObjectName("pushButton_DosyaGoruntule")
        self.pushButton_DosyaGoruntule.setEnabled(False)
        self.verticalLayout_3.addWidget(self.pushButton_DosyaGoruntule)
        
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        
        self.mainLayout.addWidget(self.groupBox_Geo)
        
        # --- Bölüm 2: Hesaplama ---
        self.groupBox_Calc = QGroupBox(self.centralwidget)
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox_Calc)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        
        self.pushButton_MeshAyarlariniHesapla = QPushButton(self.groupBox_Calc, clicked   = lambda : threading.Thread(target=self.meshAyarlarininBelirlenmesi()).start())
        self.pushButton_MeshAyarlariniHesapla.setObjectName("pushButton_MeshAyarlariniHesapla")
        self.horizontalLayout_4.addWidget(self.pushButton_MeshAyarlariniHesapla)
        
        self.progressBar = QProgressBar(self.groupBox_Calc)
        self.progressBar.setFont(font)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_4.addWidget(self.progressBar)
        
        self.mainLayout.addWidget(self.groupBox_Calc)
        
        # --- Bölüm 3: Mesh Parametreleri ---
        self.groupBox_Mesh = QGroupBox(self.centralwidget)
        self.horizontalLayout_7 = QHBoxLayout(self.groupBox_Mesh)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        
        self.label_ElementSize = QLabel(self.groupBox_Mesh)
        self.label_ElementSize.setFont(font)
        self.label_ElementSize.setObjectName("label_ElementSize")
        self.verticalLayout_5.addWidget(self.label_ElementSize)
        
        self.label_GrowRate = QLabel(self.groupBox_Mesh)
        self.label_GrowRate.setFont(font)
        self.label_GrowRate.setObjectName("label_GrowRate")
        self.verticalLayout_5.addWidget(self.label_GrowRate)
        
        self.label_DefatureTolerance = QLabel(self.groupBox_Mesh)
        self.label_DefatureTolerance.setFont(font)
        self.label_DefatureTolerance.setObjectName("label_DefatureTolerance")
        self.verticalLayout_5.addWidget(self.label_DefatureTolerance)
        
        self.label_MinSIze = QLabel(self.groupBox_Mesh)
        self.label_MinSIze.setFont(font)
        self.label_MinSIze.setObjectName("label_MinSIze")
        self.verticalLayout_5.addWidget(self.label_MinSIze)
        
        self.label_ProimityMinSize = QLabel(self.groupBox_Mesh)
        self.label_ProimityMinSize.setFont(font)
        self.label_ProimityMinSize.setObjectName("label_ProimityMinSize")
        self.verticalLayout_5.addWidget(self.label_ProimityMinSize)
        
        self.label_Angle = QLabel(self.groupBox_Mesh)
        self.label_Angle.setFont(font)
        self.label_Angle.setObjectName("label_Angle")
        self.verticalLayout_5.addWidget(self.label_Angle)
        
        self.horizontalLayout_5.addLayout(self.verticalLayout_5)
        
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.lineEdit_ElementSize = QLineEdit(self.groupBox_Mesh)
        self.lineEdit_ElementSize.setObjectName("lineEdit_ElementSize")
        self.verticalLayout_6.addWidget(self.lineEdit_ElementSize)
        
        self.lineEdit_GrowRate = QLineEdit(self.groupBox_Mesh)
        self.lineEdit_GrowRate.setObjectName("lineEdit_GrowRate")
        self.verticalLayout_6.addWidget(self.lineEdit_GrowRate)
        
        self.lineEdit_DefeatureTolerance = QLineEdit(self.groupBox_Mesh)
        self.lineEdit_DefeatureTolerance.setObjectName("lineEdit_DefeatureTolerance")
        self.verticalLayout_6.addWidget(self.lineEdit_DefeatureTolerance)
        
        self.lineEdit_MinSize = QLineEdit(self.groupBox_Mesh)
        self.lineEdit_MinSize.setObjectName("lineEdit_MinSize")
        self.verticalLayout_6.addWidget(self.lineEdit_MinSize)
        
        self.lineEdit_ProximityMinSize = QLineEdit(self.groupBox_Mesh)
        self.lineEdit_ProximityMinSize.setObjectName("lineEdit_ProximityMinSize")
        self.verticalLayout_6.addWidget(self.lineEdit_ProximityMinSize)
        
        self.lineEdit_Angle = QLineEdit(self.groupBox_Mesh)
        self.lineEdit_Angle.setObjectName("lineEdit_Angle")
        self.verticalLayout_6.addWidget(self.lineEdit_Angle)
        
        self.horizontalLayout_5.addLayout(self.verticalLayout_6)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_5)
        
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.pushButton_StartMesh = QPushButton(self.groupBox_Mesh, clicked = lambda : threading.Thread(target=self.startMeshing()).start())
        self.pushButton_StartMesh.setFont(font)
        self.pushButton_StartMesh.setObjectName("pushButton_StartMesh")
        self.verticalLayout_7.addWidget(self.pushButton_StartMesh)
        
        self.pushButton_MeshQualityR = QPushButton(self.groupBox_Mesh, clicked = lambda : threading.Thread(target=self.meshKalitesiniTahminEt()).start())
        self.pushButton_MeshQualityR.setFont(font)
        self.pushButton_MeshQualityR.setObjectName("pushButton_MeshQualityR")
        self.verticalLayout_7.addWidget(self.pushButton_MeshQualityR)
        
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_MeshQuality = QLabel(self.groupBox_Mesh)
        self.label_MeshQuality.setFont(font)
        self.label_MeshQuality.setObjectName("label_MeshQuality")
        self.horizontalLayout_6.addWidget(self.label_MeshQuality)
        
        self.label_MeshQulityResult = QLabel(self.groupBox_Mesh)
        self.label_MeshQulityResult.setFont(font)
        self.label_MeshQulityResult.setObjectName("label_MeshQulityResult")
        self.horizontalLayout_6.addWidget(self.label_MeshQulityResult)
        
        self.verticalLayout_7.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7.addLayout(self.verticalLayout_7)
        
        self.mainLayout.addWidget(self.groupBox_Mesh)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ZBGG Mesh"))
        self.label_15.setText(_translate("MainWindow", "GEOMETRİK ÖZELLİKLER"))
        self.label_hacim.setText(_translate("MainWindow", "Hacim :"))
        self.label_YuzeyAlani.setText(_translate("MainWindow", "Yüzey Alanı :"))
        self.label_KarmasiklikKatSaysi.setText(_translate("MainWindow", "Karmaşıklık Katsayısı : "))
        self.label_MinCap.setText(_translate("MainWindow", "Min Çap :"))
        self.label_MaksCap.setText(_translate("MainWindow", "Maks Çap :"))
        self.label_KisaKenar.setText(_translate("MainWindow", "Kısa Kenar :"))
        self.label_UzunKenar.setText(_translate("MainWindow", "Uzun Kenar :"))
        self.label_Hacim_Sonuc.setText(_translate("MainWindow", ""))
        self.label_YuzeyAlani_Sonuc.setText(_translate("MainWindow", ""))
        self.label_Karmasiklik_Sonuc.setText(_translate("MainWindow", ""))
        self.label_MinCap_Sonuc.setText(_translate("MainWindow", ""))
        self.label_MaksCap_Sonuc.setText(_translate("MainWindow", ""))
        self.label_KisaKenar_Sonuc.setText(_translate("MainWindow", ""))
        self.label_UzunKenar_Sonuc.setText(_translate("MainWindow", ""))
        self.pushButton_DosyaSec.setText(_translate("MainWindow", "Step Dosyasını Seç"))
        self.pushButton_DosyaGoruntule.setText(_translate("MainWindow", "Dosyayı Görüntüle"))
        self.pushButton_MeshAyarlariniHesapla.setText(_translate("MainWindow", "Mesh Ayarlarını Hesapla"))
        self.label_ElementSize.setText(_translate("MainWindow", "Element Size :"))
        self.label_GrowRate.setText(_translate("MainWindow", "Grow Rate :"))
        self.label_DefatureTolerance.setText(_translate("MainWindow", "Defeature Tolerance :"))
        self.label_MinSIze.setText(_translate("MainWindow", "Min Size :"))
        self.label_ProimityMinSize.setText(_translate("MainWindow", "Proximity Minimum Size :"))
        self.label_Angle.setText(_translate("MainWindow", "Curvature Normal Angle :"))
        self.pushButton_StartMesh.setText(_translate("MainWindow", "Start Mesh"))
        self.pushButton_MeshQualityR.setText(_translate("MainWindow", "Mesh Kalitesini Tahmin Et"))
        self.label_MeshQuality.setText(_translate("MainWindow", "Ortalama Mesh Kalitesi :"))
        self.label_MeshQulityResult.setText(_translate("MainWindow", ""))

    def dosyaSec(self):
        options = QFileDialog.Options()
        self.file_path, _ = QFileDialog.getOpenFileName(
            parent=None,  # Ana pencereyi geçmek isterseniz self.MainWindow yerine None geçebilirsiniz
            caption="STEP/STP Dosyası Seç",
            directory="",  # Varsayılan dizin
            filter="STEP/STP Files (*.step *.stp);;All Files (*)",
            options=options
        )
        if self.file_path:
            print(self.file_path)
            self.goemetrikOzellikler(self.file_path)

    def goemetrikOzellikler(self,Step_path):

        step_reader = STEPControl_Reader()
        status = step_reader.ReadFile(Step_path)


        step_reader.TransferRoots()
        self.shape = step_reader.OneShape()
        analyzer = BRepCheck_Analyzer(self.shape)
        
        # HACIM HESAPLMA
        props = GProp_GProps()
        brepgprop_VolumeProperties(self.shape, props)
        volume = round(props.Mass(),4)

        # YUZEY ALANI HESAPLAMA
        brepgprop_SurfaceProperties(self.shape,props)
        surfaceArea = round(props.Mass(),4) 
        
        # KARMASIKLIK KAT SAYISI
        complicated = round(volume / surfaceArea,4)

        edge_lengths = []

        # EN BUYUK VE EN KUCUK RADIUSU BULMA
        edge_explorer = TopExp_Explorer(self.shape, TopAbs_EDGE)
        min_radius = float('inf')  # Başlangıçta en küçük radyusu sonsuz olarak ayarla
        max_radius = float('-inf') # Başlangıçta en büyük radyusu negatif sonsuz olarak ayarla
        while edge_explorer.More():
            edge = edge_explorer.Current()
            
            # Kenarın eğrisi
            curve = BRepAdaptor_Curve(edge)
            curve_type = curve.GetType()
            
            # KENAR UZUNLUGUNU HESAPLA
            props = GProp_GProps()
            brepgprop_LinearProperties(edge, props)
            length = props.Mass()  # Lineer özellikler için 'Mass' uzunluğa karşılık gelir
            length = round(length,4)
            if length != 0:
                edge_lengths.append(length)
            

            if curve_type == 1 :  # Dairesel yay (Circle)
                circle = curve.Circle()
                radius = circle.Radius()
                radius = round(radius,4)
                # En küçük radyusu güncelle
                if radius < min_radius :
                    min_radius = radius

                # En büyük radyusu güncelle
                if radius > max_radius :
                    max_radius = radius

            
            edge_explorer.Next()
        max_length = max(edge_lengths)
        min_length = min(edge_lengths)
        self.label_Hacim_Sonuc.setText(str(volume) + " mm\u00B3") 
        self.label_YuzeyAlani_Sonuc.setText(str(surfaceArea) + " mm\u00B2") 
        self.label_Karmasiklik_Sonuc.setText(str(complicated)) 
        self.label_MinCap_Sonuc.setText(str(min_radius) + " mm") 
        self.label_MaksCap_Sonuc.setText(str(max_radius) + " mm") 
        self.label_KisaKenar_Sonuc.setText(str(min_length) + " mm") 
        self.label_UzunKenar_Sonuc.setText(str(max_length) + " mm") 
        self.pushButton_DosyaGoruntule.setEnabled(True)
    
    def OpenStep(self):
        # Conda ve ortam yolu
        conda_path = r"<local-path>"
        env_name = "ansys"

        # Python script ve STEP dosyasının yolları
        script_path = r"<local-path>"
        file_path = self.file_path

        # Komutu çalıştır
        subprocess.run(
            f'cmd.exe /c "{conda_path} && conda activate {env_name} && python \"{script_path}\" \"{file_path}\""',
            shell=True
        )

    def meshAyarlarininBelirlenmesi(self):
        hacim_str = self.label_Hacim_Sonuc.text().replace(" mm³", "").strip()
        yuzey_str = self.label_YuzeyAlani_Sonuc.text().replace(" mm²", "").strip()
        karmasiklik_str = self.label_Karmasiklik_Sonuc.text().strip()

        mincap_str = self.label_MinCap_Sonuc.text().replace(" mm", "").strip()
        maxcap_str = self.label_MaksCap_Sonuc.text().replace(" mm", "").strip()
        kisa_str = self.label_KisaKenar_Sonuc.text().replace(" mm", "").strip()
        uzun_str = self.label_UzunKenar_Sonuc.text().replace(" mm", "").strip()

        # Numerik dönüşümler (float olarak okuyoruz; eğer tam sayı ise de float sorunsuz çalışır)
        hacim_val = float(hacim_str) if hacim_str else 0.0
        yuzey_val = float(yuzey_str) if yuzey_str else 0.0
        karmasiklik_val = float(karmasiklik_str) if karmasiklik_str else 0.0
        mincap_val = float(mincap_str) if mincap_str else 0.0
        maxcap_val = float(maxcap_str) if maxcap_str else 0.0
        kisa_val = float(kisa_str) if kisa_str else 0.0
        uzun_val = float(uzun_str) if uzun_str else 0.0

        
        new_data = pd.DataFrame({
                'Hacim': [hacim_val],
                'YuzeyAlani': [yuzey_val],
                'Karmasiklik': [karmasiklik_val],
                'MinCap': [mincap_val],
                'MaxCap': [maxcap_val],
                'KisaEdge': [kisa_val],
                'UzunEdge': [uzun_val]
            })
        model_path = r'<local-path>'
        loaded_model = joblib.load(model_path)
        y_pred_new = loaded_model.predict(new_data)
        # hedef_degiskenler = [
        #     "MeshElementSize",
        #     "MeshGrowRate",
        #     "meshDefeatureTolerance",
        #     "MeshMinSize",
        #     "meshProximityMinimumSize",
        #     "meshCurvatureNormalAngle",
        #     "MeshAverage",
        #     "MeshStandardDeviation"
        # ]

        # Tahmin sonuçlarını GUI'ye yaz
        self.lineEdit_ElementSize.setText(str(y_pred_new[0][0]))

        self.lineEdit_GrowRate.setText(str(y_pred_new[0][1]))

        self.lineEdit_DefeatureTolerance.setText(str(y_pred_new[0][2]))

        self.lineEdit_MinSize.setText(str(y_pred_new[0][3]))

        self.lineEdit_ProximityMinSize.setText(str(y_pred_new[0][4]))

        self.lineEdit_Angle.setText(str(y_pred_new[0][5]))

        self.label_MeshQulityResult.setText(str(y_pred_new[0][6]))

    def meshKalitesiniTahminEt(self):
        hacim_str = self.label_Hacim_Sonuc.text().replace(" mm³", "").strip()
        yuzey_str = self.label_YuzeyAlani_Sonuc.text().replace(" mm²", "").strip()
        karmasiklik_str = self.label_Karmasiklik_Sonuc.text().strip()
        mincap_str = self.label_MinCap_Sonuc.text().replace(" mm", "").strip()
        maxcap_str = self.label_MaksCap_Sonuc.text().replace(" mm", "").strip()
        kisa_str = self.label_KisaKenar_Sonuc.text().replace(" mm", "").strip()
        uzun_str = self.label_UzunKenar_Sonuc.text().replace(" mm", "").strip()


        # Numerik dönüşümler (float olarak okuyoruz; eğer tam sayı ise de float sorunsuz çalışır)
        hacim_val = float(hacim_str) if hacim_str else 0.0
        yuzey_val = float(yuzey_str) if yuzey_str else 0.0
        karmasiklik_val = float(karmasiklik_str) if karmasiklik_str else 0.0
        mincap_val = float(mincap_str) if mincap_str else 0.0
        maxcap_val = float(maxcap_str) if maxcap_str else 0.0
        kisa_val = float(kisa_str) if kisa_str else 0.0
        uzun_val = float(uzun_str) if uzun_str else 0.0
        MeshElementSize = float(self.lineEdit_ElementSize.text().strip()) if self.lineEdit_ElementSize.text().strip() else 0.0
        MeshGrowRate = float(self.lineEdit_GrowRate.text().strip()) if self.lineEdit_GrowRate.text().strip() else 0.0
        meshDefeatureTolerance = float(self.lineEdit_DefeatureTolerance.text().strip()) if self.lineEdit_DefeatureTolerance.text().strip() else 0.0
        MeshMinSize = float(self.lineEdit_MinSize.text().strip()) if self.lineEdit_MinSize.text().strip() else 0.0
        meshProximityMinimumSize = float(self.lineEdit_ProximityMinSize.text().strip()) if self.lineEdit_ProximityMinSize.text().strip() else 0.0
        meshCurvatureNormalAngle = float(self.lineEdit_Angle.text().strip()) if self.lineEdit_Angle.text().strip() else 0.0

        new_data = pd.DataFrame({
                'Hacim': [hacim_val],
                'YuzeyAlani': [yuzey_val],
                'Karmasiklik': [karmasiklik_val],
                'MinCap': [mincap_val],


                
                'MaxCap': [maxcap_val],
                'KisaEdge': [kisa_val],
                'UzunEdge': [uzun_val],
                'MeshElementSize': [MeshElementSize],
                'MeshGrowRate': [MeshGrowRate],
                'meshDefeatureTolerance': [meshDefeatureTolerance],
                'MeshMinSize': [MeshMinSize],
                'meshProximityMinimumSize': [meshProximityMinimumSize],
                'meshCurvatureNormalAngle': [meshCurvatureNormalAngle],
            })
        model_path = r'<local-path>'
        loaded_model = joblib.load(model_path)
        y_pred_new = loaded_model.predict(new_data)
        # hedef_degiskenler = [
        #     "MeshElementSize",
        #     "MeshGrowRate",
        #     "meshDefeatureTolerance",
        #     "MeshMinSize",
        #     "meshProximityMinimumSize",
        #     "meshCurvatureNormalAngle",
        #     "MeshAverage",
        #     "MeshStandardDeviation"
        # ]

        # Tahmin sonuçlarını GUI'ye yaz


        self.label_MeshQulityResult.setText(str(y_pred_new[0][0]))

    def startMeshing(self):
        mechanical = launch_mechanical(
            exec_file=None,
            batch=False,
            start_instance=True,
            log_file='INFO',
            log_mechanical='pymechanical_log.txt',
            verbose_mechanical=True
        )
        time.sleep(3)  # Mechanical'ın tamamen açılması için bekleme süresi

        script_GeometryImport = textwrap.dedent(f"""
            geomImport = Model.GeometryImportGroup.AddGeometryImport()
            # Format of Geometry file
            geomImport_format = Ansys.Mechanical.DataModel.Enums.GeometryImportPreference.Format.Automatic

            # Preferences for Geometry file
            geomImport_preferences = Ansys.ACT.Mechanical.Utilities.GeometryImportPreferences()

            geomImport.Import(r'{self.file_path}', geomImport_format, geomImport_preferences)
        """)
        mechanical.run_python_script(script_GeometryImport)
        MeshElementSize = float(self.lineEdit_ElementSize.text().strip()) if self.lineEdit_ElementSize.text().strip() else 0.0
        MeshGrowRate = float(self.lineEdit_GrowRate.text().strip()) if self.lineEdit_GrowRate.text().strip() else 0.0
        meshDefeatureTolerance = float(self.lineEdit_DefeatureTolerance.text().strip()) if self.lineEdit_DefeatureTolerance.text().strip() else 0.0
        MeshMinSize = float(self.lineEdit_MinSize.text().strip()) if self.lineEdit_MinSize.text().strip() else 0.0
        meshProximityMinimumSize = float(self.lineEdit_ProximityMinSize.text().strip()) if self.lineEdit_ProximityMinSize.text().strip() else 0.0
        meshCurvatureNormalAngle = float(self.lineEdit_Angle.text().strip()) if self.lineEdit_Angle.text().strip() else 0.0
        script_Mesh = textwrap.dedent(f"""
                                        mesh = Model.Mesh
                                        mesh.ElementSize = Quantity({MeshElementSize}, "mm")
                                        mesh.UseAdaptiveSizing = False
                                        mesh.GrowthRateSF = {MeshGrowRate}
                                        mesh.AutomaticMeshBasedDefeaturing = 1
                                        mesh.DefeatureTolerance = Quantity({meshDefeatureTolerance}, "mm")
                                        mesh.CaptureCurvature = True
                                        mesh.MinimumSize = Quantity({MeshMinSize}, "mm")
                                        mesh.CurvatureNormalAngle = Quantity({meshCurvatureNormalAngle}, "deg")
                                        mesh.CaptureProximity = True
                                        mesh.ProximityMinimumSize = Quantity({meshProximityMinimumSize}, "mm")
                                        mesh.GenerateMesh()
                                    """)
        mechanical.run_python_script(script_Mesh)
        script_Wait = textwrap.dedent("""
            import time
            input("Mesh işlemi tamamlandı. Ansys Mechanical'ı kapatmak için Enter tuşuna basın...")
        """)
        mechanical.run_python_script(script_Wait)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
