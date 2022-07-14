-------------------------------------------------------------
  ##### обнаружение текста с фотографий
https://nuancesprog.ru/p/15535/

https://pythobyte.com/how-to-extract-text-from-images-ocr-in-python-using-opencv-and-easyocr-5f137827/

https://www.youtube.com/watch?v=UPjTYorn59g

                
     
-------------------------------------------------------------

Сайт бесплатных СМС   
https://sms-reg.com/free.html#79633429553
Scg Snt
inst_711@mail.ru
fZDUuTyBwmpSeRtvacRd

  
  
https://receive-smss.com/sms/79366199804/
wb+


         
     
### Base_Python
Многопоточность
https://yandex.ru/video/preview/?text=как%20делается%20многопоточность%20на%20питоне&path=wizard&parent-reqid=1640162334377802-1905046146888544096-man1-0611-man-l7-balancer-8080-BAL-2164&wiz_type=vital&filmId=17914322162035187423
  
     
   
Документация Скрапи
https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#std-setting-RETRY_TIMES
    
Pluging  
     
https://github.com/scrapy-plugins
<hr>
  
    
проект по генерации изображений:
https://github.com/apchenstu/sofgan
<hr>
   
     
Коды ошибок 
instagram 

https://developer.mozilla.org/ru/docs/Web/HTTP/Status/429
<hr>
   
Видос на middleware 2,23
https://gbcdn.mrgcdn.ru/uploads/record/79599/attachment/b7dfb41da15f95a007e3a7bb4c329f3b.mp4
<hr>
  

   
Ссылка на реализацию прокси внутри скрапи
https://github.com/scrapy-plugins/scrapy-zyte-smartproxy




# Parser
Добрый день! Медленно не торопясь собираем) А вообще идеальный вариант - будет реализовать middleware с остановкой работы паука на час, если получаем 429 ошибку. Пример здесь: https://stackoverflow.com/questions/43630434/how-to-handle-a-429-too-many-requests-response-in-scrapy
Stack Overflow
.   

08/02/22
А ну это нормально)) 5-6 тысяч это еще неплохой результат. Бывает через пару сотен уже блокировку вытаскивает) Блокирует как? на время, или прям надо зайти в аккаунт и ввести код проверки, чтобы разблокировать?Если просто на вермя, то здесь можно попробовать реализовать middleware по образцу из статьи: https://stackoverflow.com/questions/43630434/how-to-handle-a-429-too-many-requests-response-in-scrapy
Stack Overflow
How to handle a 429 Too Many Requests response in Scrapy?
I'm trying to run a scraper of which the output log ends as follows:

2017-04-25 20:22:22 [scrapy.spidermiddlewares.httperror] INFO: Ignoring response...



Да, можно через middleware реализовать. Там главное условие задать по какому у вас будет уходить в паузу. Заведите в классе паука параметр, который будет хранить в себе количество собранных item'ов ну или который сохранит время старта работы паука (смотря по какому критерию будете делать паузу) А затем создайте middleware:


![image](https://user-images.githubusercontent.com/82442469/153016945-8c71316c-1874-453a-abfd-fb3608bf582e.png)


 



from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from time import sleep


class SleepRetryMiddleware(RetryMiddleware):
    def __init__(self, settings):
        RetryMiddleware.__init__(self, settings)

    def process_response(self, request, response, spider):
        if spider.count_items % 1000 == 0:  # Причина паузы
            sleep(120)  # few minutes
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return super(SleepRetryMiddleware, self).process_response(request, response, spider)
        
        
        Там правда в reason можно укзаать другую причину в виде строки) Это я из стнадартной реализации взял - пауза по статус коду
        
