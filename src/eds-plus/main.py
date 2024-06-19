import flet as ft
from playwright.sync_api import sync_playwright
from Args import Args
from Eds import Eds

def main(page: ft.Page):
    def exec_button_click(e):
        if (len(text_user.value) == 0):
            text_user.focus()
            snack_bar = ft.SnackBar(ft.Text(f"请输入用户名"), open=True)
            page.overlay.append(snack_bar)
            page.update()
            return
        
        if (len(text_password.value) == 0):
            text_password.focus()
            snack_bar = ft.SnackBar(ft.Text(f"请输入密码"), open=True)
            page.overlay.append(snack_bar)
            page.update()
            return

        exec_button.text = "正在处理，请稍后"
        exec_button.disabled = True
        page.update()

        eds = Eds()
        try: 
            with sync_playwright() as playwright:
                eds.run(playwright, args)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            
        if (eds.code == 200):
            snack_bar = ft.SnackBar(ft.Text(f"自动填写日志完成: {eds.msg}"), open=True)
            page.overlay.append(snack_bar)
            page.update()
        else:
            snack_bar = ft.SnackBar(ft.Text(f"自动填写日志失败: {eds.msg}"), open=True)
            page.overlay.append(snack_bar)
            page.update()

        exec_button.disabled = False
        exec_button.text = "开始自动填写 EDS 日志"
        page.update()
        
    def text_url_change(e):
        args.url = text_url.value

    def text_user_change(e):
        args.user = text_user.value

    def text_password_change(e):
        args.password = text_password.value

    def text_msg_change(e):
        args.msg = text_msg.value

    def checkbox_headless_change(e):
        args.headless = not checkbox_headless.value

    args = Args()
    page.title = "自动填写 EDS"
    page.window.min_width = 400
    page.window.min_height = 400
    page.window.width = 400
    page.window.height = 400
    page.update()

    text_url = ft.TextField(label="EDS 地址", hint_text="请输入 EDS 地址", value="http://eds.newtouch.cn:8081/eds3/", on_change=text_url_change)
    text_user = ft.TextField(label="用户名", hint_text="请输入用户名", value="", on_change=text_user_change)
    text_password = ft.TextField(label="密码", hint_text="请输入密码", password=True, can_reveal_password=True, value="", on_change=text_password_change)
    text_msg = ft.TextField(label="EDS 日志内容", hint_text="请输入日志内容", value="代码开发", on_change=text_msg_change)
    checkbox_headless = ft.Checkbox(label="显示执行过程", value=False, on_change=checkbox_headless_change)
    exec_button = ft.FilledButton("开始自动填写 EDS 日志", disabled=False, on_click=exec_button_click)

    page.add(text_url)
    page.add(text_user)
    page.add(text_password)
    page.add(text_msg)
    page.add(checkbox_headless)
    page.add(
        ft.Container(
            content=exec_button,
            alignment=ft.alignment.center
        )
    )

ft.app(main)
