import tkinter as tk
from .stationarity import delete_trend_season
from .smoothing import SMA, EMA, LWMA
import matplotlib.pyplot as plt

def choice_determ_class(s):
    root = tk.Tk()
    root.title("Подтверждение удаления тренда")

    def on_yes():
        root.result = "yes"
        root.destroy()

    def on_no():
        root.result = "no"
        root.destroy()

    text_widget = tk.Text(root, wrap=tk.WORD, height=10, width=100)
    text_widget.pack(padx=10, pady=10)

    multiline_text = (
        f"Данный ВР - {s}.\n"
        "Необходимо провести процесс удаления тренда по следующим причинам:\n"
        "1. Наличие адекватной модели временных рядов наблюдений, описывающих поведение системы, является необходимым условием для проведения анализа.\n"
        "2. Если в процессе возможны изменения свойств, то для успешного прогнозирования и мониторинга, после построения модели на интервале без изменений, необходимо регулярно проверять её адекватность по мере поступления новых данных.\n"
        "3. Мощность тестов на проверку типа процесса значительно снижается при наличии изменений в процессах.\n"
        "Провести процесс удаления тренда?"
    )
    text_widget.insert(tk.END, multiline_text)
    text_widget.config(state=tk.DISABLED)

    yes_button = tk.Button(root, text="Да", command=on_yes)
    yes_button.pack(side=tk.LEFT, padx=10, pady=10)

    no_button = tk.Button(root, text="Нет", command=on_no)
    no_button.pack(side=tk.RIGHT, padx=10, pady=10)

    root.mainloop()
    return getattr(root, 'result', None)

def handle_choice_determ_class(choice, df, f):
    if choice == "yes":
        result = delete_trend_season(f, df)
    else:
        result = df
    return result

def choice_ma():
    root = tk.Tk()
    root.title("Выбор метода сглаживания")

    def on_sma():
        root.result = "sma"
        root.destroy()

    def on_ema():
        root.result = "ema"
        root.destroy()

    def on_lwma():
        root.result = "lwma"
        root.destroy()

    tk.Label(root, text="Выберите метод сглаживания:").pack(padx=10, pady=10)

    tk.Button(root, text="SMA", command=on_sma).pack(side="left", padx=5, pady=5)
    tk.Button(root, text="EMA", command=on_ema).pack(side="left", padx=5, pady=5)
    tk.Button(root, text="LWMA", command=on_lwma).pack(side="left", padx=5, pady=5)

    root.mainloop()
    return getattr(root, 'result', None)

def handle_choice_ma(choice, df):
    if choice == "sma":
        result = SMA(df)
    elif choice == "ema":
        result = EMA(df)
    elif choice == "lwma":
        result = LWMA(df)
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
