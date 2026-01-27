from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Display.SimpleGui import init_display
import time
import os
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = r"<local-path>"

def load_step_file(file_path):
    # STEP dosyasını okuyucuya yükle
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(file_path)
    
    if status == IFSelect_RetDone:
        # İlk aktarılan şekli al
        step_reader.TransferRoots()
        shape = step_reader.OneShape()
        return shape
    else:
        raise ValueError("STEP dosyası okunamadı.")

def main():
    # STEP dosyasının yolunu belirtin
    step_file = "<local-path>"  # Buraya kendi STEP dosyanızın yolunu girin
    
    # STEP dosyasını yükle
    shape = load_step_file(step_file)
    
    # Görüntüleme penceresini başlat
    display, start_display, add_menu, add_function_to_menu = init_display()
    
    # Şekli görüntüle
    display.DisplayShape(shape, update=True)
    start_display()
    
    # Görüntüleme penceresini başlat
if __name__ == "__main__":
    main()
