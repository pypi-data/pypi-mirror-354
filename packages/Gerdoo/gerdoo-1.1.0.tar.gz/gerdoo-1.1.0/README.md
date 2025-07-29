![موتور جستجوی گردو](https://gerdoo.me/static/commons/img/logo.c179f12989b4.svg)



# Gerdoo

این کتابخانه مخصوص استفاده برای موتور جستجوی **گردو** طراحی شده است


برای ساخت یک یک شیء از سرچ کننده گردو این کار را انجام دهید :
```python

import Gerdoo from Gerdoo

gerdoo = Gerdoo("Query")
```

## امکانات
- جستجوی کلی
- جستجوی تصویر
- جستجوی ویدیو
- جستجوی اخبار
- دریافت پیشنهادات برای جستجو




## جستجوی کلی

```python

import Gerdoo from Gerdoo

gerdoo = Gerdoo("Query")
print(gerdoo.search())
```


## جستجوی تصاویر

```python

import Gerdoo from Gerdoo

gerdoo = Gerdoo("Query")
print(gerdoo.search_image())
```


## جستجوی ویدیو ها

```python

import Gerdoo from Gerdoo

gerdoo = Gerdoo("Query")
print(gerdoo.search_video())
```


## جستجوی اخبار

```python

import Gerdoo from Gerdoo

gerdoo = Gerdoo("Query")
print(gerdoo.search_news())
```


## دریافت پیشنهادات برای جستجو

```python

import Gerdoo from Gerdoo

gerdoo = Gerdoo("Query")
print(gerdoo.GetSuggestions())
```


### لینک ها
- [نویسنده](https://apicode.pythonanywhere.com/)
- [موتور جستجوی گردو](https://gerdoo.me/)