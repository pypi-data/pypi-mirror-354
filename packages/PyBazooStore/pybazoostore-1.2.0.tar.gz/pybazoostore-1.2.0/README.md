![BazooStore](https://webapp.bazoostore.ir/assets/Untitled-DgdTq2A6.png)


# PyBazooStore

بسم الله الرحمن الرحیم
کتابخانه غیررسمی جستجوی ربات در سرویس بازواستور





## دریافت برترین بات ها
```python

from PyBazooStore import BazooStore
bazo = BazooStore()
print(bazo.GetBestBots())
```


## دریافت بات های جدید
```python

from PyBazooStore import BazooStore
bazo = BazooStore()
print(bazo.GetNewBots())
```


## دریافت چند بات تصادفی
```python

from PyBazooStore import BazooStore
bazo = BazooStore()
print(bazo.GetRandomBots())
```


## جستجوی بات ها
```python

from PyBazooStore import BazooStore
from PyBazooStore.enums.searched_by import Searched_by


bazo = BazooStore()

#جستجو بر اساس نام بات
print(bazo.SearchBots(
    "Name Bot",
    Searched_by.NAME
))


#جستجو بر اساس توضیحات بات
print(bazo.SearchBots(
    "Caption Bot",
    Searched_by.CAPTION
))
```




نوشته شده با ❤️ توسط محمدرضا