import sys
import os

# Qt platform plugin yolunu (PyQt) tanımlıyoruz (importlardan önce ayarlamak önemli)
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = r"<local-path>"

from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Display.SimpleGui import init_display

def load_step_file(file_path):
    """Verilen path'teki STEP dosyasını okuyup shape döndürür."""
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(file_path)
    if status == IFSelect_RetDone:
        step_reader.TransferRoots()
        shape = step_reader.OneShape()
        return shape
    else:
        raise ValueError("STEP dosyası okunamadı veya geçersiz dosya yolu.")

def main():
    # Komut satırından bir argüman bekliyoruz (STEP dosyası yolu)
    if len(sys.argv) != 2:
        print("Kullanım: python OpenStep.py <step_dosyası_yolu>")
        sys.exit(1)
    
    step_file = sys.argv[1]  # STEP dosyasının yolunu aldık
    
    # STEP dosyasını yükle
    shape = load_step_file(step_file)
    
    # PythonOCC görselleştirme fonksiyonlarını başlat
    display, start_display, add_menu, add_function_to_menu = init_display()
    # Şekli çizdir
    display.DisplayShape(shape, update=True)
    # Modeli ekrana sığdır
    display.FitAll()
    # Görselleştirme penceresini başlat (bloklayıcı döngü)
    start_display()

if __name__ == "__main__":
    main()
