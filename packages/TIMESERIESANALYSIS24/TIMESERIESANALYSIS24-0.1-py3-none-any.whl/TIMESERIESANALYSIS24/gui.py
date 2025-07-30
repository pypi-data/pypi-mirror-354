import tkinter as tk
import matplotlib.pyplot as plt
from .stationarity import Stationarity
from .smoothing import Smoothing

class GUI:
    def __init__(self):
        self.root = None

    def choice_determ_class(self, s):
        self.root = tk.Tk()
        self.root.title("Подтверждение удаления тренда")

        def on_yes():
            self.root.result = "yes"
            self.root.destroy()

        def on_no():
            self.root.result = "no"
            self.root.destroy()

        text_widget = tk.Text(self.root, wrap=tk.WORD, height=10, width=100)
        text_widget.pack(padx=10, pady=10)

        multiline_text = (
            f"Данный ВР - {s}.\n"
            "Необходимо провести процесс удаления тренда по следующим причинам:\n"
            "1. Наличие адекватной модели временных рядов наблюдений, описывающих поведение системы, является необходимым условием для проведения анализа.\n"
            "2. Если в процессе возможны изменения свойств, то для успешного прогнозирования и мониторинга, после построения модели на интервале без изменений, необходимо регулярно проверять её адекватность по мере поступления новых данных.\n"
            "3. Мощность тестов на проверку типа процесса значительно снижается при наличии изменений в процессах.\n"
            "Провести процесс удаления тренда?\n"
        )
        text_widget.insert(tk.END, multiline_text)
        text_widget.config(state=tk.DISABLED)

        tk.Button(self.root, text="Да", command=on_yes).pack(side=tk.LEFT, padx=10, pady=10)
        tk.Button(self.root, text="Нет", command=on_no).pack(side=tk.RIGHT, padx=10, pady=10)

        self.root.mainloop()
        return getattr(self.root, 'result', None)

    def handle_choice_determ_class(self, choice, df, f):
        if choice == "yes":
            stationarity = Stationarity(df)
            result = stationarity.delete_trend_season(f)
        else:
            result = df
        return result

    def choice_ma(self):
        self.root = tk.Tk()
        self.root.title("Выбор метода сглаживания")

        def on_sma():
            self.root.result = "sma"
            self.root.destroy()

        def on_ema():
            self.root.result = "ema"
            self.root.destroy()

        def on_lwma():
            self.root.result = "lwma"
            self.root.destroy()

        tk.Label(self.root, text="Выберите метод сглаживания:").pack(padx=10, pady=10)
        tk.Button(self.root, text="SMA", command=on_sma).pack(side="left", padx=5, pady=5)
        tk.Button(self.root, text="EMA", command=on_ema).pack(side="left", padx=5, pady=5)
        tk.Button(self.root, text="LWMA", command=on_lwma).pack(side="left", padx=5, pady=5)

        self.root.mainloop()
        return getattr(self.root, 'result', None)

    def handle_choice_ma(self, choice, df):
        smoothing = Smoothing(df)
        if choice == "sma":
            result = smoothing.sma()
        elif choice == "ema":
            result = smoothing.ema()
        elif choice == "lwma":
            result = smoothing.lwma()
        else:
            result = df

        plt.plot(df, label='Исходный ВР')
        plt.plot(result, label='Сглаженный ВР', linestyle='--')
        plt.legend()
        plt.xlabel('Дата')
        plt.ylabel('Температура')
        plt.grid()
        plt.show()

        return result
