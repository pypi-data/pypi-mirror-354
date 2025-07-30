# osonkod/__init__.py

__version__ = "0.1.0"

# Standart funksiyalar
chiqar = print
kirish = input
uzunligi = len
oraligi = range
matn = str
butun = int
haqiqiy = float
royxat = list
lugat = dict
sanoq = enumerate
filtrlash = filter
xaritlash = map
ajrat = str.split
birlashtir = str.join
sarala = sorted
teskari = reversed
maxi = max
mini = min
yigindi = sum
any_qiymat = any
hech_biri = all
yordam = help
tipi = type
isinstance_mi = isinstance
dirlar = dir

# Mantiqiy qiymatlar
rost = True
yolgon = False
hech_narsa = None

# Fayl ishlash
fayl_och = open

# Modullar import: o‘zgartirib import qilish
import_qil = __import__

# Dekorator yordamchisi
def funksiya(*args, **kwargs):
    def owrap(fn):
        return fn
    return owrap if not args else args[0]
