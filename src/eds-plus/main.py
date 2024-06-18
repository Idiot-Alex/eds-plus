import flet as ft
from playwright.sync_api import sync_playwright
import datetime
import calendar

class Args:
    # 构造函数，当创建对象时自动调用
    def __init__(self, msg="代码开发", url="http://eds.newtouch.cn:8081/eds3/"):
        # 定义对象的属性
        self.name = None
        self.password = None
        self.msg = msg
        self.url = url
        self.headless = True

def run(playwright, args: Args):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(
        headless = False,
        slow_mo = 200
    )
    page = browser.new_page()
    page.goto(args.url)

    page.on("dialog", handle_dialog)

    handle_login(page, args.name, args.password)

    # 获取当前年份和月份
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    curr_day = now.day

    # 填写当月日志
    write_eds(page, year, month, args)

    # 若当前月底日期 - 当前日期 <= 5，继续填写下月日志
    total_days = calendar.monthrange(year, month)[1]
    if (total_days - curr_day <= 5):
        month = get_next_month(month)
        if (month == 1):
            year = year + 1

        # 填写下月日志
        write_eds(page, year, month, args)

    # other actions...
    browser.close()

def handle_login(page, name, password):
    page.locator("input#UserId").fill(name)
    page.locator("input#UserPassword").fill(password)
    page.locator("button#btnSubmit").click()

def handle_dialog(dialog):
    print(f"dialog msg: {dialog.message}")
    if (dialog.message == "用户名或密码错误"):
        print("程序终止...请检查用户名密码是否正确")
        dialog.page.context.browser.close()
    else:
        dialog.accept()
        print(f"程序终止...{dialog.message}")
        dialog.page.context.browser.close()

def write_eds(page, year, month, args):
    # 获取当月总天数
    total_days = calendar.monthrange(year, month)[1]
    # 遍历每一天的日期
    for day in range(1, total_days + 1):
        dateStr = datetime.date(year, month, day).strftime("%Y-%m-%d")
        page.goto(args.url + "worklog.aspx?LogDate=" + dateStr)
        table = page.locator("table#dgWorkLogList")
        if table.count() > 0:
            print(dateStr + " EDS done....")
        else:
            page.locator("input#txtStartTime").fill("09:00")
            page.locator("input#txtEndTime").fill("12:00")
            page.locator("textarea#txtMemo").fill(args.msg)
            page.locator("input#btnSave").click()

            page.locator("input#txtStartTime").fill("13:00")
            page.locator("input#txtEndTime").fill("18:00")
            page.locator("textarea#txtMemo").fill(args.msg)
            page.locator("input#btnSave").click()
            print(dateStr + " write EDS done....")

def get_next_month(month):
    if (month == 12):
        return 1
    else:
        return month + 1


def main(page: ft.Page):
    def exec_button_click(e):
        page.snack_bar = ft.SnackBar(ft.Text(f"Hello..."))
        page.snack_bar.open = True
        page.update()
        try: 
            with sync_playwright() as playwright:
                args.name = "211859"
                args.password = "211859zx"
                run(playwright, args)
        except Exception as e:
            print(f"An error occurred: {e.message}")
        

    def checkbox_headless_change(e):
        args.headless = not checkbox_headless.value


    args = Args()
    page.title = "自动填写 EDS"
    page.window_min_width = 400
    page.window_min_height = 400
    page.window_max_width = 400
    page.window_max_height = 400
    page.update()

    text_url = ft.TextField(label="EDS 地址", hint_text="请输入 EDS 地址", value="http://eds.newtouch.cn:8081/eds3/")
    text_userName = ft.TextField(label="用户名", hint_text="请输入用户名", value="211859")
    text_password = ft.TextField(label="密码", hint_text="请输入密码", password=True, can_reveal_password=True, value="211859zx")
    text_msg = ft.TextField(label="EDS 日志内容", hint_text="请输入日志内容", value="代码开发")
    checkbox_headless = ft.Checkbox(label="显示执行过程", value=False, on_change=checkbox_headless_change)
    exec_button = ft.FilledButton("开始自动填写 EDS 日志", on_click=exec_button_click)

    page.add(text_url)
    page.add(text_userName)
    page.add(text_password)
    page.add(text_msg)
    page.add(checkbox_headless)
    page.add(
        ft.Container(
            content=exec_button,
            alignment=ft.alignment.center
        )
    )
    # try: 
    #     with sync_playwright() as playwright:
    #         args = Args('211859', '211859zx', '代码开发')
    #         run(playwright, args)
    # except Exception as e:
    #     print(f"An error occurred: {e.message}")

ft.app(main)
