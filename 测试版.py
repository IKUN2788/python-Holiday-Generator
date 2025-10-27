import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import calendar
import requests
import json
import threading
import chinese_calendar

class HolidayStatisticsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("节假日统计器")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # 存储节假日数据
        self.holiday_data = {}
        
        # 初始化当前年月
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        
        # 创建界面
        self.create_widgets()
        
        # 异步加载节假日数据
        self.load_holiday_data_thread()
    
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="节假日统计器", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 15))
        
        # 年份选择
        ttk.Label(main_frame, text="选择年份:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        self.year_var = tk.StringVar()
        self.year_combo = ttk.Combobox(main_frame, textvariable=self.year_var, width=8)
        self.year_combo['values'] = [str(year) for year in range(2020, 2031)]
        self.year_combo.set(str(self.current_year))
        self.year_combo.grid(row=1, column=1, sticky=tk.W, padx=(0, 15))
        
        # 月份选择
        ttk.Label(main_frame, text="选择月份:").grid(row=1, column=2, sticky=tk.W, padx=(0, 5))
        self.month_var = tk.StringVar()
        self.month_combo = ttk.Combobox(main_frame, textvariable=self.month_var, width=8)
        self.month_combo['values'] = [f"{month:02d}" for month in range(1, 13)]
        self.month_combo.set(f"{self.current_month:02d}")
        self.month_combo.grid(row=1, column=3, sticky=tk.W, padx=(0, 15))
        
        # 查询按钮
        self.query_btn = ttk.Button(main_frame, text="生成日历", command=self.generate_calendar)
        self.query_btn.grid(row=1, column=4, padx=(15, 0))
        
        # 日历显示区域
        self.calendar_frame = ttk.Frame(main_frame, relief="solid", borderwidth=1)
        self.calendar_frame.grid(row=2, column=0, columnspan=5, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(15, 0))
        self.calendar_frame.columnconfigure(0, weight=1)
        self.calendar_frame.rowconfigure(0, weight=1)
        
        # 汇总信息区域
        self.summary_frame = ttk.LabelFrame(main_frame, text="月份汇总", padding="10")
        self.summary_frame.grid(row=3, column=0, columnspan=5, sticky=(tk.W, tk.E), pady=(15, 0))
        
        # 状态栏
        self.status_var = tk.StringVar(value="准备就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief="sunken")
        status_bar.grid(row=4, column=0, columnspan=5, sticky=(tk.W, tk.E), pady=(15, 0))
    
    def load_holiday_data_thread(self):
        """在新线程中加载节假日数据"""
        self.status_var.set("正在加载节假日数据...")
        thread = threading.Thread(target=self.load_holiday_data)
        thread.daemon = True
        thread.start()
    
    def load_holiday_data(self):
        """加载节假日数据（模拟数据，实际应用中可接入API）"""
        try:
            # 这里使用模拟数据，实际应用中可以从API获取
            # 示例：使用公开的节假日API或本地数据文件
            self.holiday_data = self.get_simulated_holiday_data()
            
            # 模拟加载延迟
            import time
            time.sleep(1)
            
            self.root.after(0, lambda: self.status_var.set("节假日数据加载完成"))
            
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"节假日数据加载失败: {str(e)}"))
    
    def get_simulated_holiday_data(self):
        """获取模拟的节假日数据"""
        # 这里提供一些示例节假日数据
        # 实际应用中应该从可靠的API获取
        holidays = {
            "2024": {
                "01": {"01": "元旦", "27": "春节调休", "28": "春节调休"},
                "02": {"10": "春节", "11": "春节", "12": "春节", "13": "春节", "14": "春节", "15": "春节", "16": "春节", "17": "春节"},
                "04": {"04": "清明节", "05": "清明节", "06": "清明节"},
                "05": {"01": "劳动节", "02": "劳动节", "03": "劳动节", "04": "劳动节", "05": "劳动节"},
                "06": {"10": "端午节"},
                "09": {"15": "中秋节", "16": "中秋节", "17": "中秋节"},
                "10": {"01": "国庆节", "02": "国庆节", "03": "国庆节", "04": "国庆节", "05": "国庆节", "06": "国庆节", "07": "国庆节"}
            },
            "2023": {
                "01": {"01": "元旦", "21": "春节", "22": "春节", "23": "春节", "24": "春节", "25": "春节", "26": "春节", "27": "春节"},
                "04": {"05": "清明节"},
                "05": {"01": "劳动节"},
                "06": {"22": "端午节", "23": "端午节", "24": "端午节"},
                "09": {"29": "中秋节"},
                "10": {"01": "国庆节", "02": "国庆节", "03": "国庆节", "04": "国庆节", "05": "国庆节", "06": "国庆节"}
            }
        }
        return holidays
    
    def generate_calendar(self):
        """生成日历"""
        try:
            year = int(self.year_var.get())
            month = int(self.month_var.get())
            
            if not (2020 <= year <= 2030) or not (1 <= month <= 12):
                messagebox.showerror("错误", "请选择有效的年份和月份")
                return
            
            self.status_var.set("正在生成日历...")
            self.display_calendar(year, month)
            self.display_summary(year, month)
            self.status_var.set("日历生成完成")
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的年份和月份")
    
    def display_calendar(self, year, month):
        """显示日历"""
        # 清空日历区域
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        
        # 创建日历画布
        canvas = tk.Canvas(self.calendar_frame, bg="white")
        scrollbar = ttk.Scrollbar(self.calendar_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.calendar_frame.columnconfigure(0, weight=1)
        self.calendar_frame.rowconfigure(0, weight=1)
        
        # 获取月份的第一天和总天数
        cal = calendar.monthcalendar(year, month)
        month_name = calendar.month_name[month]
        
        # 显示月份标题
        title_label = ttk.Label(scrollable_frame, text=f"{year}年 {month_name}", 
                               font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=7, pady=(0, 10))
        
        # 显示星期标题
        weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        for i, day in enumerate(weekdays):
            day_label = ttk.Label(scrollable_frame, text=day, font=("Arial", 10, "bold"))
            day_label.grid(row=1, column=i, padx=2, pady=2, ipadx=10, ipady=5)
        
        # 显示日期
        row = 2
        for week in cal:
            for col, day in enumerate(week):
                if day == 0:
                    # 空日期
                    frame = ttk.Frame(scrollable_frame, width=80, height=60)
                    frame.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
                    frame.grid_propagate(False)
                else:
                    # 有效日期
                    self.create_day_widget(scrollable_frame, year, month, day, row, col)
            row += 1
        
        # 配置网格权重
        for i in range(7):
            scrollable_frame.columnconfigure(i, weight=1)
    
    def create_day_widget(self, parent, year, month, day, row, col):
        """创建日期小部件"""
        date_obj = datetime(year, month, day)
        
        # 使用chinese_calendar判断日期类型
        is_workday = self.is_workday(year, month, day)
        is_holiday, holiday_name = self.is_holiday(year, month, day)
        is_weekend = date_obj.weekday() >= 5  # 5=周六, 6=周日
        
        # 创建日期框架
        frame = ttk.Frame(parent, relief="solid", borderwidth=1)
        frame.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
        frame.grid_propagate(False)
        frame.configure(width=80, height=60)
        
        # 设置背景颜色和类型标识
        if is_holiday:
            bg_color = "#FFB6C1"  # 节假日 - 浅红色
            type_text = "假"
            type_color = "red"
        elif is_workday:
            if is_weekend:
                # 调休工作日（周末上班）
                bg_color = "#FFF8DC"  # 调休工作日 - 浅黄色
                type_text = "班"
                type_color = "orange"
            else:
                # 正常工作日
                bg_color = "#F0F8FF"  # 工作日 - 浅蓝色
                type_text = "工"
                type_color = "blue"
        else:
            # 周末休息日
            bg_color = "#FFE4E1"  # 周末 - 浅粉色
            type_text = "休"
            type_color = "purple"
        
        # 使用Canvas来设置背景色
        canvas = tk.Canvas(frame, bg=bg_color, highlightthickness=0)
        canvas.place(relwidth=1, relheight=1)
        
        # 日期标签
        day_label = tk.Label(canvas, text=str(day), bg=bg_color, 
                            font=("Arial", 12, "bold"))
        day_label.place(relx=0.1, rely=0.1)
        
        # 节假日名称
        if is_holiday and holiday_name:
            holiday_label = tk.Label(canvas, text=holiday_name, bg=bg_color,
                                   font=("Arial", 7), fg="red", wraplength=60)
            holiday_label.place(relx=0.1, rely=0.5)
        
        # 日期类型标识
        type_label = tk.Label(canvas, text=type_text, bg=bg_color,
                            font=("Arial", 8, "bold"), fg=type_color)
        type_label.place(relx=0.7, rely=0.1)
    
    def is_holiday(self, year, month, day):
        """判断是否为节假日"""
        try:
            date_obj = datetime(year, month, day).date()
            
            # 使用chinese_calendar判断是否为节假日
            if chinese_calendar.is_holiday(date_obj):
                # 获取节假日名称
                holiday_name = chinese_calendar.get_holiday_detail(date_obj)
                if holiday_name:
                    return True, holiday_name[0]  # 返回节假日名称
                else:
                    return True, "节假日"
            
            return False, ""
        except Exception as e:
            # 如果chinese_calendar出错，回退到原有逻辑
            year_str = str(year)
            month_str = f"{month:02d}"
            day_str = f"{day:02d}"
            
            try:
                if (year_str in self.holiday_data and 
                    month_str in self.holiday_data[year_str] and 
                    day_str in self.holiday_data[year_str][month_str]):
                    return True, self.holiday_data[year_str][month_str][day_str]
            except:
                pass
            
            return False, ""
    
    def is_workday(self, year, month, day):
        """判断是否为工作日（使用chinese_calendar）"""
        try:
            date_obj = datetime(year, month, day).date()
            return chinese_calendar.is_workday(date_obj)
        except:
            # 回退逻辑：非周末且非节假日
            date_obj = datetime(year, month, day)
            is_weekend = date_obj.weekday() >= 5
            is_holiday, _ = self.is_holiday(year, month, day)
            return not (is_weekend or is_holiday)
    
    def display_summary(self, year, month):
        """显示汇总信息"""
        # 清空汇总区域
        for widget in self.summary_frame.winfo_children():
            widget.destroy()
        
        # 计算各种天数
        total_days = calendar.monthrange(year, month)[1]
        workdays = 0
        weekend_rest = 0
        holidays = 0
        weekend_work = 0  # 调休工作日（周末上班）
        
        for day in range(1, total_days + 1):
            date_obj = datetime(year, month, day)
            is_weekend = date_obj.weekday() >= 5
            is_workday = self.is_workday(year, month, day)
            is_holiday, _ = self.is_holiday(year, month, day)
            
            if is_holiday:
                holidays += 1
            elif is_workday:
                if is_weekend:
                    weekend_work += 1  # 周末调休上班
                else:
                    workdays += 1  # 正常工作日
            else:
                weekend_rest += 1  # 周末休息
        
        # 显示汇总信息
        summary_text = (f"总天数: {total_days}天 | "
                       f"工作日: {workdays}天 | "
                       f"周末休息: {weekend_rest}天 | "
                       f"节假日: {holidays}天")
        
        if weekend_work > 0:
            summary_text += f" | 调休上班: {weekend_work}天"
        
        summary_label = ttk.Label(self.summary_frame, text=summary_text, 
                                 font=("Arial", 11))
        summary_label.grid(row=0, column=0, sticky=tk.W)
        
        # 额外信息
        month_name = calendar.month_name[month]
        extra_info = ttk.Label(self.summary_frame, 
                              text=f"{year}年{month_name} - 蓝色:工作日 粉色:周末 红色:节假日 黄色:调休上班",
                              font=("Arial", 9), foreground="gray")
        extra_info.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))

def main():
    root = tk.Tk()
    app = HolidayStatisticsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()