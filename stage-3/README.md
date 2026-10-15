# Конфигурационное управление — вариант 10 — этап 3

Исполнитель: **Исламова Камилла Тимуровна**, ИКБО-62-25.

## Реализовано
Загрузка VFS из CSV в память; команды ls/cd пока заглушки.

## Запуск
```bash
python3 -m src.main
```
С параметрами:
```bash
python3 -m src.main --vfs data/deep.csv --prompt "kamilla$" --script examples/stage4.txt
```

## Тестирование
```bash
python3 -m unittest discover -s tests -v
```
