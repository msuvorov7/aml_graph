# AML Graph

MVP проект для графовой аналитики в помощь AML сотрудникам банка.

# Архитектура решения

![docs/img/aml_graph_design.png](docs/img/aml_graph_design.png)

- Ежедневно на кластере производим рассчет витрин с вершинами и ребрами для графа.
Временной период установлен на 30 дней. Для каждого клиента находим данные о его 
дате регистрации, уровне риска, санкциях и других необходимых данных. В качестве ребер 
берем все транзакции (без агрегации за весь период), чтобы в UI дать аналитику возможность
просмотреть всю выписку
- Переливаем рассчитанные данные в графовую БД, чтобы иметь возможность производить
быстрый обход графа и увеличить скорость доступа к данным.
- Испоьзуем самописный Frontend & Backend, чтобы гибко реализовывать требования заказчика