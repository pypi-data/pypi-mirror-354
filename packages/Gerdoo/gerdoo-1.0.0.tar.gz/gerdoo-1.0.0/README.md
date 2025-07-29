# Gerdoo

این کتابخانه مخصوص استفاده برای موتور جستجوی **گردو** طراحی شده است


برای ساخت یک یک شیء از سرچ کننده گردو این کار را انجام دهید :
```python

import Gerdoo from SearchGerdoo

gerdoo = SearchGerdoo("Query")
```



### جستجوی کلی

```python

import Gerdoo from SearchGerdoo

gerdoo = SearchGerdoo("Query")
print(gerdoo.search())
```


### جستجوی تصاویر

```python

import Gerdoo from SearchGerdoo

gerdoo = SearchGerdoo("Query")
print(gerdoo.search_image())
```


### جستجوی ویدیو ها

```python

import Gerdoo from SearchGerdoo

gerdoo = SearchGerdoo("Query")
print(gerdoo.search_video())
```


### جستجوی اخبار

```python

import Gerdoo from SearchGerdoo

gerdoo = SearchGerdoo("Query")
print(gerdoo.search_news())
```


### دریافت پیشنهادات برای جستجو

```python

import Gerdoo from SearchGerdoo

gerdoo = SearchGerdoo("Query")
print(gerdoo.GetSuggestions())
```