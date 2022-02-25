проект по генерации изображений:
https://github.com/apchenstu/sofgan
<hr>

  
Коды ошибок 
instagram 

https://developer.mozilla.org/ru/docs/Web/HTTP/Status/429
<hr>

Видос на middleware 2,23
<hr>
https://gbcdn.mrgcdn.ru/uploads/record/79599/attachment/b7dfb41da15f95a007e3a7bb4c329f3b.mp4

 


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
        
