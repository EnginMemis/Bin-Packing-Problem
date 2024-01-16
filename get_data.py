from shapes import Rectangle

def readFile():
    index = 0
    rectangles = []
    dosya_yolu = "Data/C7_3"
    try:
        with open(dosya_yolu, 'r') as dosya:
            data = dosya.readlines()
            for i in range(len(data)):
                data[i] = data[i].split('\n')[0]
            count = int(data[0])
            bin_width = int(data[1].split()[0])
            bin_height = int(data[1].split()[1])

            for i in range(2, count + 2):
                width = int(data[i].split()[0])
                height = int(data[i].split()[1])
                rectangles.append(Rectangle(width, height, index))
                index += 1
        return bin_width, bin_height, rectangles
    except FileNotFoundError:
        print("Belirtilen dosya bulunamadı.")
    except Exception as e:
        print("Dosya okuma sırasında bir hata oluştu:", str(e))
