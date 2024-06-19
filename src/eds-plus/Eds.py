from Args import Args
import datetime
import calendar

class Eds:
    def __init__(self):
        self.code = 0
        self.msg = None

    def response(self, code, msg):
        self.code = code
        self.msg = msg

    def run(self, playwright, args: Args):
        chromium = playwright.chromium # or "firefox" or "webkit".
        browser = chromium.launch(
            headless = args.headless,
            slow_mo = 200
        )
        page = browser.new_page()
        page.goto(args.url)

        page.on("dialog", self.handle_dialog)

        self.handle_login(page, args.user, args.password)

        # 获取当前年份和月份
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        curr_day = now.day

        # 填写当月日志
        self.write_eds(page, year, month, args)

        # 若当前月底日期 - 当前日期 <= 5，继续填写下月日志
        total_days = calendar.monthrange(year, month)[1]
        if (total_days - curr_day <= 5):
            month = self.get_next_month(month)
            if (month == 1):
                year = year + 1

            # 填写下月日志
            self.write_eds(page, year, month, args)

        # other actions...
        browser.close()
        self.response(200, "执行成功")

    def handle_login(self, page, name, password):
        page.locator("input#UserId").fill(name)
        page.locator("input#UserPassword").fill(password)
        page.locator("button#btnSubmit").click()

    def handle_dialog(self, dialog):
        print(f"dialog msg: {dialog.message}")
        if (dialog.message == "用户名或密码错误"):
            self.response(400, "用户名或密码错误")
            print("程序终止...请检查用户名密码是否正确")
            dialog.page.context.browser.close()
        else:
            code = 200 if dialog.message == "不能填写7天后的日志" else 500
            self.response(code, dialog.message)
            dialog.accept()
            print(f"程序终止...{dialog.message}")
            dialog.page.context.browser.close()

    def write_eds(self, page, year, month, args):
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

    def get_next_month(self, month):
        if (month == 12):
            return 1
        else:
            return month + 1