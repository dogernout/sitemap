# sitemap
Sitemap creater from main site link. Visits all found links and adds them to the sitemap.

Возможен как интерактивный запуск, так и через консоль. В консоли необходимо аргументом программы указать ссылку в формате http://*/ или https://*/.

Результаты занесены в таблицу ниже:
![image](https://user-images.githubusercontent.com/26380064/173118612-a630c04b-661c-4bb5-8f60-4a62cc9a23cd.png)

Также была реализация данной программы с помощью построения небинарного
дерева. Обход производился в ширину с помощью очереди. К сожалению,
многопоточность реализовать пока что не вышло. Рисование дерева
происходило с помощью модуля graphviz (строил дополнительно дерево
Digraph).

Выводы: на некоторых сайтах невозможно извлечь ссылки на внутренние страницы, так как они не указываются в теге <a>.
