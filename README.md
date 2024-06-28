# eds-plus
自动填写新致软件公司的 eds 日志

## build

```
pyinstaller -n eds-plus -F .\src\eds-plus\main.py

pyinstaller --clean --hidden-import=Pillow -n eds-plus -F .\src\eds-plus\main.py