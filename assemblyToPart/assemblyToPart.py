from OCC.Core.STEPControl import STEPControl_Reader, STEPControl_Writer, STEPControl_AsIs
from OCC.Core.TopoDS import TopoDS_Compound, TopoDS_Shape
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_SOLID
from OCC.Core.IFSelect import IFSelect_RetDone
import os

# STEP dosyasını okuyarak bir STEPControl_Reader nesnesi döndürür
def read_step_file(file_path):
    reader = STEPControl_Reader()  # STEP dosyasını okuyacak nesneyi oluştur
    status = reader.ReadFile(file_path)  # Dosyayı yükle ve okuma durumunu kontrol et
    if status != IFSelect_RetDone:  # Eğer okuma başarısızsa
        print("STEP dosyası okunamadı.")  # Hata mesajı ver
        return None  # İşlemi sonlandır
    reader.TransferRoot()  # Dosya içeriğini bellek yapısına aktar
    return reader  # Reader nesnesini döndür

# STEP dosyasındaki montajdan parçaları ayırır
def extract_parts_from_assembly(assembly_shape):
    parts = []  # Parçaların saklanacağı liste
    explorer = TopExp_Explorer(assembly_shape, TopAbs_SOLID)  # Montajdaki solid türdeki şekilleri keşfet
    while explorer.More():  # Keşfedilecek şekiller olduğu sürece
        parts.append(explorer.Current())  # Şu anki şekli listeye ekle
        explorer.Next()  # Sonraki şekle geç
    return parts  # Tüm parçaları döndür

# Bir parçayı STEP dosyası olarak kaydeder
def save_part_as_step(part_shape, output_file):
    writer = STEPControl_Writer()  # STEP dosyasını yazmak için writer nesnesi oluştur
    writer.Transfer(part_shape, STEPControl_AsIs)  # Şekli olduğu gibi yazma için transfer et
    status = writer.Write(output_file)  # STEP dosyasını yaz ve durumu kontrol et
    if status == IFSelect_RetDone:  # Eğer yazma başarılıysa
        print(f"Parça başarıyla {output_file} olarak kaydedildi.")  # Başarı mesajı yazdır
    else:
        print(f"Parça kaydedilemedi: {output_file}")  # Hata mesajı yazdır

# Ana işlem akışı
def process_assembly(input_step_file):
    # STEP dosyasını oku
    reader = read_step_file(input_step_file)  # STEP dosyasını oku ve bir reader nesnesi al
    name1 = os.path.splitext(os.path.basename(input_step_file))[0].replace(' ', '')
    if reader is None:  # Eğer dosya okunamadıysa
        return  # İşlemi sonlandır

    # Montajın root şekli
    assembly_shape = reader.Shape()  # Montajın ana şekli (root shape)

    # Parçaları ayıkla
    parts = extract_parts_from_assembly(assembly_shape)  # Montajdaki parçaları ayıkla
    os.makedirs(name1, exist_ok=True)
    # Her bir parçayı ayrı STEP dosyasına kaydet
    for idx, part in enumerate(parts):  # Her bir parçayı sırayla işle
        output_file = f"{name1}/parca_{idx + 1}.step"  # Çıkış dosyasını isimlendir (örneğin: parca_1.step)
        save_part_as_step(part, output_file)  # Parçayı STEP dosyasına kaydet

# Ana işlem akışını başlat

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Split every STEP assembly in a folder into single-part STEP files.")
    parser.add_argument("assembly_dir", help="Folder containing STEP assembly files")
    args = parser.parse_args()
    for file_0 in sorted(os.listdir(args.assembly_dir)):
        if file_0.lower().endswith((".step", ".stp")):
            process_assembly(os.path.join(args.assembly_dir, file_0))

print('Bitti')