# Стандартные библиотеки Python
import logging
import os
import tempfile
import traceback
import warnings
from datetime import datetime, timedelta
from pathlib import Path

# Сторонние библиотеки (Data Science)
import numpy as np
import pandas as pd

# AutoGluon
from autogluon.timeseries import TimeSeriesPredictor, TimeSeriesDataFrame

# PyQt5
from PyQt5.QtCore import QCoreApplication, QThread, pyqtSignal, Qt, QVariant
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QPlainTextEdit, QCheckBox, QComboBox, QLabel, QProgressBar

# Orange3
from Orange.data import Table, Domain, ContinuousVariable, StringVariable, DiscreteVariable, TimeVariable, Variable
from Orange.widgets import gui, settings
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Input, Output

# Опциональные импорты
try:
    import holidays
    HOLIDAYS_AVAILABLE = True
except ImportError:
    HOLIDAYS_AVAILABLE = False
    print("holidays библиотека не установлена")

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def format_message(level, text):
        """Форматирование сообщений без эмодзи"""
        prefixes = {
            'critical': '[КРИТИЧНО]',
            'warning': '[ВНИМАНИЕ]', 
            'caution': '[ОСТОРОЖНО]',
            'info': '[ИНФО]',
            'success': '[ГОТОВО]',
            'ok': '[OK]',
            'error': '[ОШИБКА]'
        }
        return f"{prefixes.get(level, '[ИНФО]')} {text}"

class AutoGluonWorker(QThread):
    """Рабочий поток для асинхронного обучения AutoGluon"""
    
    # Сигналы для коммуникации с основным потоком
    progress_updated = pyqtSignal(int, str)  # прогресс, сообщение
    log_updated = pyqtSignal(str)            # новое сообщение лога
    training_finished = pyqtSignal(object, object, object, object, object)  # predictor, predictions, leaderboard, model_info
    training_failed = pyqtSignal(str)        # сообщение об ошибке
    
    def __init__(self, widget_instance):
        super().__init__()
        self.widget = widget_instance
        self.is_cancelled = False
        
    def cancel(self):
        """Отмена выполнения"""
        self.is_cancelled = True
        self.log_updated.emit("Отмена операции...")
        
    def log(self, message):
        """Отправка сообщения в лог"""
        self.log_updated.emit(message)
        
    def run(self):
        """Основная функция потока - адаптированная версия run_model_sync"""
        try:
            self.log_updated.emit("=== НАЧАЛО АСИНХРОННОГО ОБУЧЕНИЯ ===")
            self.progress_updated.emit(5, "Подготовка данных...")
            
            # Получаем данные из основного потока
            data = self.widget.data.copy()
            target_column = self.widget.target_column
            id_column = self.widget.id_column
            timestamp_column = self.widget.timestamp_column
            prediction_length = self.widget.prediction_length
            time_limit = self.widget.time_limit
            selected_metric = self.widget.selected_metric
            selected_preset = self.widget.selected_preset
            include_holidays = self.widget.include_holidays
            holiday_country = self.widget.holiday_country
            auto_frequency = self.widget.auto_frequency
            detected_frequency = self.widget.detected_frequency
            frequency = self.widget.frequency
            FREQUENCIES = self.widget.FREQUENCIES
            categorical_mapping = self.widget.categorical_mapping
            
            # Проверка отмены
            if self.is_cancelled:
                return
            
            # ====== СКОПИРОВАННЫЙ КОД ИЗ run_model_sync ======
            
            self.progress_updated.emit(10, "Проверка данных...")
            
            # Проверяем выбранные колонки
            if not id_column or id_column not in data.columns:
                raise Exception(f"ID колонка '{id_column}' отсутствует в данных")
            if not timestamp_column or timestamp_column not in data.columns:
                raise Exception(f"Временная колонка '{timestamp_column}' отсутствует в данных")
            if not target_column or target_column not in data.columns:
                raise Exception(f"Целевая колонка '{target_column}' отсутствует в данных")
            
            # Проверка отмены
            if self.is_cancelled:
                return
                
            self.progress_updated.emit(15, "Сортировка данных...")
            
            # Безопасная сортировка
            try:
                df_sorted = data.sort_values([id_column, timestamp_column])
                self.log_updated.emit("Сортировка успешна")
            except Exception as e:
                self.log_updated.emit(f"Ошибка при сортировке: {str(e)}")
                raise
                
            # Определяем частоту для модели
            if auto_frequency:
                model_freq = detected_frequency
            else:
                freq_index = frequency
                if isinstance(freq_index, int) and 0 <= freq_index < len(FREQUENCIES):
                    model_freq = FREQUENCIES[freq_index][0]
                else:
                    model_freq = frequency
            self.log_updated.emit(f"Используемая частота: {model_freq}")
            
            # Проверка отмены
            if self.is_cancelled:
                return
            
            self.progress_updated.emit(20, "Агрегация данных...")
            
            # Агрегация по частоте если нужно
            if model_freq != 'D':
                self.log_updated.emit(f"Агрегация данных по частоте: {model_freq}")
                df_sorted = df_sorted.groupby([
                    id_column,
                    pd.Grouper(key=timestamp_column, freq=model_freq)
                ]).agg({
                    target_column: 'sum'
                }).reset_index()
                self.log_updated.emit(f"После агрегации: {len(df_sorted)} записей")

            self.progress_updated.emit(25, "Подготовка признаков праздников...")
            
            # Подготовка праздников
            if include_holidays:
                if HOLIDAYS_AVAILABLE:
                    try:
                        df_sorted[timestamp_column] = pd.to_datetime(df_sorted[timestamp_column])
                        unique_dates = df_sorted[timestamp_column].dt.normalize().unique()
                        if len(unique_dates) > 0:
                            min_date = unique_dates.min()
                            max_date = unique_dates.max()
                            country_holidays = holidays.CountryHoliday(holiday_country, 
                                                                    years=range(min_date.year, max_date.year + 1))
                            df_sorted['is_holiday'] = df_sorted[timestamp_column].dt.normalize().apply(
                                lambda date: 1 if date in country_holidays else 0)
                            self.log_updated.emit(f"Добавлены праздники: {df_sorted['is_holiday'].sum()} дней")
                    except Exception as e:
                        self.log_updated.emit(f"Ошибка добавления праздников: {str(e)}")
                else:
                    self.log_updated.emit("Праздники отключены: библиотека holidays не установлена")
                    self.log_updated.emit("Установите: pip install holidays")
            
            # Проверка отмены
            if self.is_cancelled:
                return
            
            self.progress_updated.emit(30, "Создание TimeSeriesDataFrame...")
            
            # Создание TimeSeriesDataFrame
            ts_data = TimeSeriesDataFrame.from_data_frame(
                df_sorted,
                id_column=id_column,
                timestamp_column=timestamp_column
            )
            
            self.progress_updated.emit(35, "Создание предиктора...")
            
            # Создание временной папки
            with tempfile.TemporaryDirectory() as temp_dir:
                model_path = Path(temp_dir)
                
                # Получение метрики
                metric = selected_metric
                if isinstance(metric, int) and 0 <= metric < len(self.widget.METRICS):
                    metric = self.widget.METRICS[metric]
                self.log_updated.emit(f"Используемая метрика: {metric}")
                
                # Проверка отмены
                if self.is_cancelled:
                    return
                
                self.progress_updated.emit(40, f"Создание модели...")
                
                # Создание предиктора
                predictor = TimeSeriesPredictor(
                    path=model_path,
                    prediction_length=prediction_length,
                    target=target_column,
                    eval_metric=metric.lower(),
                    freq=model_freq,
                    log_to_file=False,
                    verbosity=1
                )
                
                self.progress_updated.emit(45, f"Обучение модели (лимит: {time_limit}с)...")
                
                # Настройки обучения
                fit_args = {
                    "time_limit": time_limit,
                    "num_val_windows": 1,
                    "val_step_size": 1
                }
                
                # Проверка отмены перед длительной операцией
                if self.is_cancelled:
                    return
                
                # Обучение модели
                self.log_updated.emit("Запуск обучения AutoGluon...")
                
                try:
                    predictor.fit(ts_data, **fit_args)
                except ValueError as ve:
                    error_msg = str(ve)
                    if "observations" in error_msg:
                        self.log_updated.emit("Обработка ошибки с количеством наблюдений...")
                        ts_lengths = ts_data.groupby(level=0).size()
                        min_ts_id = ts_lengths.idxmin()
                        min_ts_len = ts_lengths.min()
                        
                        if min_ts_len < 10:
                            long_enough_ids = ts_lengths[ts_lengths >= 10].index
                            if len(long_enough_ids) > 0:
                                ts_data = ts_data.loc[long_enough_ids]
                                self.log_updated.emit(f"Отфильтровано до {len(long_enough_ids)} рядов")
                                predictor.fit(ts_data, **fit_args)
                            else:
                                raise Exception("Все временные ряды слишком короткие")
                    else:
                        raise
                
                # Проверка отмены после обучения
                if self.is_cancelled:
                    return
                
                self.progress_updated.emit(75, "Создание прогноза...")
                
                # Подготовка будущих ковариат для праздников
                known_covariates_for_prediction = None
                if include_holidays and 'is_holiday' in df_sorted.columns:
                    try:
                        future_dates = self.widget.create_future_dates(prediction_length)
                        future_df_list = []
                        
                        for item_id_val in ts_data.item_ids:
                            item_future_df = pd.DataFrame({
                                'item_id': item_id_val,
                                'timestamp': pd.to_datetime(future_dates)
                            })
                            future_df_list.append(item_future_df)
                        
                        if future_df_list:
                            future_df_for_covariates = pd.concat(future_df_list)
                            future_df_for_covariates = future_df_for_covariates.set_index(['item_id', 'timestamp'])
                            if HOLIDAYS_AVAILABLE:
                                country_holidays_future = holidays.CountryHoliday(
                                    holiday_country, 
                                    years=range(future_dates.min().year, future_dates.max().year + 1)
                                )
                                
                                future_df_for_covariates['is_holiday'] = future_df_for_covariates.index.get_level_values('timestamp').to_series().dt.normalize().apply(
                                    lambda date: 1 if date in country_holidays_future else 0
                                ).values
                                
                                known_covariates_for_prediction = future_df_for_covariates[['is_holiday']]
                                self.log_updated.emit("Подготовлены будущие праздники для прогноза")
                            else:
                                self.log_updated.emit("Будущие праздники пропущены: библиотека holidays недоступна")
                                known_covariates_for_prediction = None
                    except Exception as e:
                        self.log_updated.emit(f"Ошибка подготовки будущих праздников: {str(e)}")
                
                # Создание прогноза
                predictions = predictor.predict(ts_data, known_covariates=known_covariates_for_prediction)
                
                # Проверка отмены
                if self.is_cancelled:
                    return
                
                self.progress_updated.emit(85, "Обработка результатов прогноза...")
                
                # ===== СКОПИРОВАННАЯ ОБРАБОТКА ПРОГНОЗОВ ИЗ run_model_sync =====
                try:
                    self.log_updated.emit(f"Тип прогноза: {type(predictions)}")
                    
                    if hasattr(predictions, 'index') and hasattr(predictions.index, 'nlevels') and predictions.index.nlevels == 2:
                        self.log_updated.emit("Обрабатываем TimeSeriesDataFrame с MultiIndex")
                        
                        forecast_numeric_ids = predictions.index.get_level_values(0).unique()
                        self.log_updated.emit(f"Числовые ID в прогнозе: {forecast_numeric_ids.tolist()}")
                        
                        # Получаем исходные строковые ID из данных
                        original_string_ids = data[id_column].unique()
                        self.log_updated.emit(f"Исходные строковые ID в данных: {original_string_ids}")
                        
                        # Применяем категориальный маппинг если есть
                        if id_column in categorical_mapping:
                            mapping = categorical_mapping[id_column]
                            self.log_updated.emit(f"Категориальный маппинг: {mapping}")
                            
                            numeric_to_country = {}
                            for i, country_name in enumerate(mapping):
                                numeric_id = str(float(i))
                                numeric_to_country[numeric_id] = country_name
                            
                            self.log_updated.emit(f"Маппинг числовой -> страна: {numeric_to_country}")
                        else:
                            numeric_to_country = {str(uid): str(uid) for uid in forecast_numeric_ids}
                        
                        # Создаем итоговый DataFrame
                        all_forecast_data = []
                        
                        for numeric_id in forecast_numeric_ids:
                            numeric_id_str = str(numeric_id)
                            self.log_updated.emit(f"--- Обработка ID: {numeric_id_str} ---")
                            
                            country_name = numeric_to_country.get(numeric_id_str, f"Unknown_{numeric_id_str}")
                            self.log_updated.emit(f"Маппинг: {numeric_id_str} -> {country_name}")
                            
                            id_predictions = predictions.loc[numeric_id]
                            
                            # Ищем данные по числовому ID
                            id_data = data[data[id_column] == numeric_id_str]
                            
                            if len(id_data) == 0:
                                for alt_format in [numeric_id, int(float(numeric_id_str)), str(int(float(numeric_id_str)))]:
                                    id_data = data[data[id_column] == alt_format]
                                    if len(id_data) > 0:
                                        break
                            
                            if len(id_data) == 0:
                                last_date = pd.Timestamp('2024-01-01')
                            else:
                                id_data_sorted = id_data.sort_values(timestamp_column)
                                last_date = id_data_sorted[timestamp_column].iloc[-1]
                            
                            # Создаем будущие даты
                            future_dates = self.widget.create_future_dates_for_specific_id(last_date, model_freq)
                            
                            # Формируем итоговый прогноз
                            id_forecast = pd.DataFrame()
                            id_forecast[id_column] = [country_name] * len(future_dates)  # ← ИСПОЛЬЗУЕМ НАЗВАНИЕ!
                            id_forecast['timestamp'] = [d.strftime('%Y-%m-%d') for d in future_dates]
                            
                            tech_columns = ['index', 'Unnamed: 0']  # список технических колонок
                            # Копируем числовые прогнозные колонки
                            for col in id_predictions.columns:
                                #if pd.api.types.is_numeric_dtype(id_predictions[col]):
                                if col not in tech_columns and pd.api.types.is_numeric_dtype(id_predictions[col]):
                                    values = id_predictions[col].values
                                    if len(values) >= len(future_dates):
                                        cleaned_values = np.maximum(values[:len(future_dates)], 0).round(0).astype(int)
                                    else:
                                        cleaned_values = np.maximum(values, 0).round(0).astype(int)
                                        if len(cleaned_values) < len(future_dates):
                                            last_val = cleaned_values[-1] if len(cleaned_values) > 0 else 0
                                            additional = [last_val] * (len(future_dates) - len(cleaned_values))
                                            cleaned_values = np.concatenate([cleaned_values, additional])
                                    
                                    id_forecast[col] = cleaned_values
                            
                            all_forecast_data.append(id_forecast)
                            self.log_updated.emit(f"Добавлен прогноз для '{country_name}'")
                        
                        # Объединяем все прогнозы
                        if all_forecast_data:
                            pred_df = pd.concat(all_forecast_data, ignore_index=True)
                            self.log_updated.emit(f"Итоговый прогноз: {len(pred_df)} записей")
                            self.log_updated.emit(f"=== ПОСЛЕ CONCAT ===")
                            self.log_updated.emit(f"Колонки pred_df: {list(pred_df.columns)}")
                            
                            for country in pred_df[id_column].unique():
                                country_data = pred_df[pred_df[id_column] == country]
                                dates = country_data['timestamp'].tolist()
                                self.log_updated.emit(f"Итоговые даты для {country}: {dates[0]} - {dates[-1]}")
                        else:
                            pred_df = predictions.reset_index(drop=True)
                    else:
                        pred_df = predictions.reset_index(drop=True)
                        
                except Exception as e:
                    self.log_updated.emit(f"Ошибка при подготовке прогноза: {str(e)}")
                    pred_df = predictions.reset_index(drop=True) if hasattr(predictions, 'reset_index') else predictions
                
                self.progress_updated.emit(90, "Подготовка лидерборда...")
                
                # Лидерборд
                leaderboard = None
                try:
                    lb = predictor.leaderboard()
                    if lb is not None and not lb.empty:
                        self.log_updated.emit("Формирование лидерборда...")
                        for col in lb.select_dtypes(include=['float']).columns:
                            lb[col] = lb[col].round(4)
                        
                        lb.columns = [str(col).replace(' ', '_').replace('-', '_') for col in lb.columns]
                        
                        for col in lb.select_dtypes(include=['object']).columns:
                            lb[col] = lb[col].astype(str)
                            
                        self.log_updated.emit(f"Структура лидерборда: {lb.dtypes}")
                        leaderboard = lb
                except Exception as lb_err:
                    self.log_updated.emit(f"Ошибка лидерборда: {str(lb_err)}")
                
                self.progress_updated.emit(93, "Анализ состава ансамбля...")

                # ИСПРАВЛЕННОЕ получение РЕАЛЬНОГО состава ансамбля
                # ПРОСТОЕ РЕШЕНИЕ: только компоненты ансамбля
                ensemble_info = None
                try:
                    if leaderboard is not None and not leaderboard.empty:
                        best_model_name = leaderboard.iloc[0]['model']
                        
                        if 'WeightedEnsemble' in best_model_name:
                            # Берем топ-6 моделей (исключая сам ансамбль) как компоненты
                            components = leaderboard[leaderboard['model'] != best_model_name].head(6)
                            
                            ensemble_data = []
                            for i, (_, row) in enumerate(components.iterrows()):
                                # Условные веса на основе ранга
                                weight = max(0.05, 0.3 - i*0.05)  # От 30% до 5%
                                
                                ensemble_data.append({
                                    'Model': row['model'],
                                    'Weight': round(weight, 4)
                                })
                            
                            ensemble_info = pd.DataFrame(ensemble_data)
                            self.log_updated.emit(f"Состав ансамбля: {len(ensemble_data)} компонентов")
                        
                except Exception as e:
                    self.log_updated.emit(f"Ошибка: {e}")

                self.progress_updated.emit(95, "Формирование информации о модели...")
                
                # Инфо о модели
                freq_name = model_freq
                for code, label in FREQUENCIES:
                    if code == model_freq:
                        freq_name = f"{label} ({code})"
                        break
                
                best_model_name = "Неизвестно"
                best_model_score = "Н/Д"
                
                try:
                    if leaderboard is not None and not leaderboard.empty:
                        best_model_name = leaderboard.iloc[0]['model']
                        best_model_score = f"{leaderboard.iloc[0]['score_val']:.4f}"
                except Exception as e:
                    self.log_updated.emit(f"Не удалось получить информацию о лучшей модели: {str(e)}")
                
                model_info = pd.DataFrame({
                    'Parameter': ['Версия', 'Цель', 'Длина', 'Метрика', 'Пресет', 
                                'Время', 'Праздники', 'Частота', 'Лучшая модель', 'Оценка модели'],
                    'Value': ['1.2.0', target_column, str(prediction_length),
                            metric, selected_preset, 
                            f"{time_limit} сек", 
                            "Включены" if include_holidays else "Отключены",
                            freq_name, best_model_name, best_model_score]
                })
                
                logging.shutdown()
                
                self.progress_updated.emit(100, "Завершение...")
                
                # Отправка результатов
                self.training_finished.emit(predictor, pred_df, leaderboard, model_info, ensemble_info)
                
        except Exception as e:
            error_msg = f"Ошибка обучения: {str(e)}\n{traceback.format_exc()}"
            self.training_failed.emit(error_msg)

class OWAutoGluonTimeSeries(OWWidget):
    name = "AutoGluon Time Series"
    description = "Прогнозирование временных рядов с AutoGluon"
    icon = "icons/autogluon.png"
    priority = 0
    keywords = ["timeseries", "forecast", "autogluon"]

    # Настройки
    prediction_length = settings.Setting(10)
    time_limit = settings.Setting(60)
    selected_metric = settings.Setting("MAE")
    selected_preset = settings.Setting("best_quality")
    target_column = settings.Setting("sales")
    id_column = settings.Setting("item_id")
    timestamp_column = settings.Setting("timestamp")
    include_holidays = settings.Setting(False)
    #use_current_date = settings.Setting(True)  # Настройка для использования текущей даты
    frequency = settings.Setting("D")  # Частота для прогноза (по умолчанию дни)
    auto_frequency = settings.Setting(True)  # Автоопределение частоты
    selected_model = settings.Setting("auto") # выбор моделей
    holiday_country = settings.Setting("RU") # Страна для праздников

    # Метрики
    METRICS = ["MAE", "MAPE", "MSE", "RMSE", "RMSLE", "SMAPE", "WAPE", "WQL", "SQL", "MASE", "RMSSE"]
    
    # Частоты
    FREQUENCIES = [
        ("D", "День"),
        ("W", "Неделя"),
        ("M", "Месяц"),
        ("Q", "Квартал"),
        ("Y", "Год"),
        ("H", "Час"),
        ("T", "Минута"),
        ("B", "Рабочий день")
    ]
    # Доступные страны для праздников (можно расширить)
    HOLIDAY_COUNTRIES = ["RU", "US", "GB", "DE", "FR", "CA"]


    class Inputs:
        data = Input("Data", Table)

    class Outputs:
        prediction = Output("Prediction", Table)
        leaderboard = Output("Leaderboard", Table)
        model_info = Output("Model Info", Table)
        ensemble_info = Output("Ensemble Info", Table)
        log_messages = Output("Log", str)

    def __init__(self):
        super().__init__()
        self.data = None
        self.predictor = None
        self.log_messages = ""
        self.detected_frequency = "D"  # Определенная частота данных по умолчанию
        self.mainArea.hide()
        self.setup_ui()
        self.warning("")
        self.error("")
        self.log("Виджет инициализирован")
        
        # Данные для валидации длины прогноза
        self.max_allowed_prediction = 0
        self.data_length = 0
        self.from_form_timeseries = False  # Флаг для определения источника данных
        self.categorical_mapping = {} # для сопоставления категориальных значений
        # переменные для асинхронности
        self.worker = None
        self.is_training = False
    
    def setup_ui(self):

        # Основные параметры
        box = gui.widgetBox(self.controlArea, "Параметры")
        self.prediction_spin = gui.spin(box, self, "prediction_length", 1, 365, 1, label="Длина прогноза:")
        self.prediction_spin.valueChanged.connect(self.on_prediction_length_changed)
        
        # Добавляем информационную метку о максимальной длине прогноза
        self.max_length_label = QLabel("Максимальная длина прогноза: N/A")
        box.layout().addWidget(self.max_length_label)
        
        gui.spin(box, self, "time_limit", 10, 86400, 10, label="Лимит времени (сек):")
        
        # Кастомная модель для группировки метрик
        self.metric_combo = QComboBox()
        model = QStandardItemModel()

        def add_group(title, items):
            title_item = QStandardItem(f"— {title} —")
            title_item.setFlags(Qt.NoItemFlags)  # Заголовок недоступен для выбора
            model.appendRow(title_item)
            for metric in items:
                item = QStandardItem(metric)
                item.setData(metric, Qt.UserRole)
                model.appendRow(item)

        add_group("Probabilistic", ["SQL", "WQL"])
        add_group("Point forecast (median)", ["MAE", "MASE", "WAPE"])
        add_group("Point forecast (mean)", ["MSE", "RMSE", "RMSLE", "RMSSE", "MAPE", "SMAPE"])

        self.metric_combo.setModel(model)

        # Автоматическая установка метрики по умолчанию (MAPE)
        for i in range(model.rowCount()):
            item = model.item(i)
            if item and item.data(Qt.UserRole) == "MAPE":
                self.metric_combo.setCurrentIndex(i)
                self.selected_metric = "MAPE"
                break

        # Добавление QComboBox в layout
        box.layout().addWidget(QLabel("Метрика:"))
        box.layout().addWidget(self.metric_combo)

        # Обработчик выбора, сохраняем выбранную метрику
        def on_metric_changed(index):
            metric = self.metric_combo.currentText()
            if metric.startswith("—"):
                return  # Пропускаем заголовки
            self.selected_metric = metric
            self.log(f"Выбрана метрика: {self.selected_metric}")

        self.metric_combo.currentIndexChanged.connect(on_metric_changed)
        
        self.model_selector = gui.comboBox(
            box, self, "selected_preset",
            items=["best_quality", "high_quality", "medium_quality", "fast_training"],
            label="Пресет:",
            sendSelectedValue=True
        )

        # Получаем модели динамически
        available_models = self._get_available_models()
        # Добавляем выбор моделей
        self.model_selector = gui.comboBox(
            box, self, "selected_model",
            items=available_models,
            label="Модель autogluon:",
            sendSelectedValue=True
        )
        
        # Настройки столбцов
        col_box = gui.widgetBox(self.controlArea, "Столбцы")
        # Хранение всех колонок для выпадающего списка
        self.all_columns = []
        
        # Целевая переменная
        self.target_combo = gui.comboBox(col_box, self, "target_column", label="Целевая:", 
                                         items=[], sendSelectedValue=True,
                                         callback=self.on_target_column_changed) 
        # ID ряда
        self.id_combo = gui.comboBox(col_box, self, "id_column", label="ID ряда:", 
                                     items=[], sendSelectedValue=True,
                                     callback=self.on_id_column_changed) 
        # Временная метка
        self.timestamp_combo = gui.comboBox(col_box, self, "timestamp_column", label="Время:", 
                                            items=[], sendSelectedValue=True,
                                            callback=self.on_timestamp_column_changed) 
        
        # Настройки частоты
        freq_box = gui.widgetBox(self.controlArea, "Частота временного ряда")
        
        # Чекбокс для автоопределения частоты
        self.auto_freq_checkbox = QCheckBox("Автоматически определять частоту")
        self.auto_freq_checkbox.setChecked(self.auto_frequency)
        self.auto_freq_checkbox.stateChanged.connect(self.on_auto_frequency_changed)
        freq_box.layout().addWidget(self.auto_freq_checkbox)
        
        # Выпадающий список частот
        self.freq_combo = gui.comboBox(freq_box, self, "frequency", 
              items=[f[0] for f in self.FREQUENCIES], 
              label="Частота:",
              callback=self.on_frequency_changed)
        # Заменяем технические обозначения на понятные названия
        for i, (code, label) in enumerate(self.FREQUENCIES):
            self.freq_combo.setItemText(i, f"{label} ({code})")
        
        # Отключаем комбобокс, если автоопределение включено
        self.freq_combo.setDisabled(self.auto_frequency)
        
        # Метка для отображения определенной частоты
        self.detected_freq_label = QLabel("Определенная частота: N/A")
        freq_box.layout().addWidget(self.detected_freq_label)

        # Дополнительные настройки
        extra_box = gui.widgetBox(self.controlArea, "Дополнительно")
        self.holidays_checkbox = QCheckBox("Учитывать праздники")

        # Всегда устанавливаем значение и коннектим обработчик
        self.holidays_checkbox.setChecked(self.include_holidays)
        self.holidays_checkbox.stateChanged.connect(self.on_holidays_changed)

        # Если holidays недоступен - отключаем и меняем текст
        if not HOLIDAYS_AVAILABLE:
            self.holidays_checkbox.setEnabled(False)  # ← ОТКЛЮЧАЕМ
            self.holidays_checkbox.setText("Учитывать праздники (требует: pip install holidays)")
            self.holidays_checkbox.setChecked(False)  # ← Принудительно выключаем

        extra_box.layout().addWidget(self.holidays_checkbox)

        # Добавляем выбор страны для праздников
        self.holiday_country_combo = gui.comboBox(extra_box, self, "holiday_country",
                                                  label="Страна для праздников:",
                                                  items=self.HOLIDAY_COUNTRIES,
                                                  sendSelectedValue=True)
        self.holiday_country_combo.setEnabled(self.include_holidays) # Активируем только если включены праздники
        
        # Кнопки управления (оставьте только это)
        button_box = gui.widgetBox(self.controlArea, "Управление")
        
        self.run_button = gui.button(button_box, self, "Запустить", callback=self.run_model)
        self.cancel_button = gui.button(button_box, self, "Отменить", callback=self.cancel_training)
        self.cancel_button.setDisabled(True)
        
        self.progress_box = gui.widgetBox(self.controlArea, "Прогресс")
        
        # Метка для прогресса
        self.progress_label = QLabel("Готов к запуску")
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_box.layout().addWidget(self.progress_label)
        
        # Сам прогресс-бар
        self.progress_widget = QProgressBar()
        self.progress_widget.setRange(0, 100)
        self.progress_widget.setValue(0)
        self.progress_widget.setVisible(False)
        self.progress_box.layout().addWidget(self.progress_widget)

        # логи
        log_box_main = gui.widgetBox(self.controlArea, "Логи", addSpace=True)
        self.log_widget = QPlainTextEdit(readOnly=True)
        self.log_widget.setMinimumHeight(200)
        font = QFont("Monospace")
        font.setStyleHint(QFont.TypeWriter)
        self.log_widget.setFont(font)
        log_box_main.layout().addWidget(self.log_widget)
    
    def _get_available_models(self):
        """ПОЛНЫЙ список всех моделей AutoGluon"""
        try:
            print("Получаем ПОЛНЫЙ список через импорт классов")
            
            # Полный список моделей из GitHub AutoGluon
            all_models = [
                "auto",
                # Статистические
                "Naive", "SeasonalNaive", "Zero", "Average", "SeasonalAverage",
                "ETS", "AutoETS", "ARIMA", "AutoARIMA", "AutoCES",
                "Theta", "DynamicOptimizedTheta", "IMAPA", "ADIDA", "Croston",
                
                # Табличные
                "DirectTabular", "RecursiveTabular",
                
                # Deep Learning
                "DeepAR", "SimpleFeedForward", "TemporalFusionTransformer",
                "PatchTST", "TiDE", "DLinear", "WaveNet", "NPTS",
                
                # Предобученные
                "Chronos"
            ]
            
            # Проверяем какие реально доступны в вашей установке
            available_models = ["auto"]
            
            try:
                import autogluon.timeseries.models as ag_models
                for model_name in all_models[1:]:  # пропускаем "auto"
                    try:
                        model_class = getattr(ag_models, f"{model_name}Model", None)
                        if model_class is not None:
                            available_models.append(model_name)
                            print(format_message('success', f"{model_name} доступна"))
                        else:
                            print(format_message('error', f"{model_name} недоступна"))
                    except AttributeError:
                        print(format_message('error', f"{model_name} недоступна"))
                        
            except Exception as e:
                print(f"Ошибка проверки: {e}")
                # Fallback на популярные модели
                available_models = [
                    "auto", "Naive", "SeasonalNaive", "ETS", "AutoETS", 
                    "DirectTabular", "RecursiveTabular", "DeepAR", 
                    "TemporalFusionTransformer", "PatchTST", "TiDE"
                ]
                
            print(f"Итого доступно: {len(available_models)} моделей")
            return available_models
            
        except Exception as e:
            print(f"Полная проверка failed: {e}")
            return [
                "auto", "Naive", "SeasonalNaive", "ETS", "AutoETS",
                "DirectTabular", "RecursiveTabular", "DeepAR", 
                "TemporalFusionTransformer", "PatchTST", "TiDE"
            ]

    def information(self, message):
        """Показывает информационное сообщение"""
        self.log(f"ИНФОРМАЦИЯ: {message}")
        # Можно также отправить в выход логов
        # self.Outputs.log_messages.send(f"INFO: {message}")

    def clear_messages(self):
        """Очищает все сообщения об ошибках и предупреждениях"""
        self.error("")
        self.warning("")

    def on_frequency_changed(self):
        """Обработчик изменения частоты с валидацией"""
        selected_freq = self.get_current_frequency()
        self.log(f"Пользователь выбрал частоту: {selected_freq}")
        
        if self.data is not None and hasattr(self, 'detected_frequency'):
            # Проверяем совместимость
            is_compatible, message = self.validate_frequency_compatibility()
            
            if not is_compatible:
                # Блокируем критически несовместимые частоты
                self.error(message)
                self.run_button.setDisabled(True)
                
                # Автоматически возвращаем к определенной частоте
                self.log(f"Автоматически возвращаемся к безопасной частоте: {self.detected_frequency}")
                for i, (code, label) in enumerate(self.FREQUENCIES):
                    if code == self.detected_frequency:
                        self.frequency = i
                        self.freq_combo.setCurrentIndex(i)
                        break
                
                # Повторяем проверку с исправленной частотой
                is_compatible, message = self.validate_frequency_compatibility()
                if is_compatible:
                    self.clear_messages()
                    self.information(f"Частота автоматически изменена на безопасную: {self.detected_frequency}")
                    self.run_button.setDisabled(False)
            else:
                # Совместимые частоты - убираем блокировку и показываем сообщение
                self.clear_messages()
                
                if "[КРИТИЧНО]" in message:
                    self.error(message)
                    self.run_button.setDisabled(True)
                elif "[ОСТОРОЖНО]" in message:      
                    self.warning(message)
                    self.run_button.setDisabled(False)
                elif "[ИНФО]" in message:
                    self.information(message)
                    self.run_button.setDisabled(False)
                elif "[ГОТОВО]" in message:         
                    self.log(message)               # Просто логируем успешное сообщение
                    self.run_button.setDisabled(False)
                else:
                    # Все хорошо
                    self.run_button.setDisabled(False)
            
            self.update_frequency_info()

    def get_current_frequency(self):
        """Получает текущую выбранную частоту"""
        if self.auto_frequency:
            return self.detected_frequency
        else:
            freq_index = self.frequency
            if isinstance(freq_index, int) and 0 <= freq_index < len(self.FREQUENCIES):
                return self.FREQUENCIES[freq_index][0]
            else:
                return self.frequency

    def estimate_points_after_aggregation(self, freq_code):
        """Оценивает количество точек после агрегации по частоте для каждого ID"""
        if self.data is None:
            return {'min_points': 0, 'max_points': 0, 'details': {}}
        
        # Проверяем, есть ли временная колонка
        if self.timestamp_column not in self.data.columns:
            return {'min_points': 0, 'max_points': 0, 'details': {}}
        
        try:
            points_by_id = {}
            
            if self.id_column in self.data.columns:
                # Анализируем каждый ID отдельно
                unique_ids = self.data[self.id_column].unique()
                
                for uid in unique_ids:
                    id_data = self.data[self.data[self.id_column] == uid].copy()
                    id_data = id_data.sort_values(self.timestamp_column)
                    
                    if len(id_data) == 0:
                        continue
                        
                    start_date = id_data[self.timestamp_column].min()
                    end_date = id_data[self.timestamp_column].max()
                    
                    # Создаем диапазон дат с нужной частотой
                    date_range = pd.date_range(start=start_date, end=end_date, freq=freq_code)
                    estimated_points = len(date_range)
                    
                    # Получаем человекочитаемое название ID если есть маппинг
                    display_id = uid
                    if self.id_column in self.categorical_mapping:
                        mapping = self.categorical_mapping[self.id_column]
                        try:
                            id_index = int(float(uid))
                            if 0 <= id_index < len(mapping):
                                display_id = f"{mapping[id_index]} ({uid})"
                        except:
                            pass
                    
                    points_by_id[display_id] = {
                        'points': estimated_points,
                        'start': start_date,
                        'end': end_date,
                        'original_records': len(id_data)
                    }
            else:
                # Если нет ID колонки, анализируем все данные как один ряд
                sample_data = self.data.copy().sort_values(self.timestamp_column)
                start_date = sample_data[self.timestamp_column].min()
                end_date = sample_data[self.timestamp_column].max()
                date_range = pd.date_range(start=start_date, end=end_date, freq=freq_code)
                estimated_points = len(date_range)
                
                points_by_id['Единый ряд'] = {
                    'points': estimated_points,
                    'start': start_date,
                    'end': end_date,
                    'original_records': len(sample_data)
                }
            
            if not points_by_id:
                return {'min_points': 0, 'max_points': 0, 'details': {}}
            
            all_points = [info['points'] for info in points_by_id.values()]
            result = {
                'min_points': min(all_points),
                'max_points': max(all_points),
                'details': points_by_id
            }
            
            return result
            
        except Exception as e:
            self.log(f"Ошибка оценки точек для частоты {freq_code}: {str(e)}")
            # Запасной расчет
            freq_ratios = {
                'T': self.data_length,           
                'H': self.data_length // 60,     
                'D': self.data_length,           
                'B': int(self.data_length * 0.7), 
                'W': self.data_length // 7,     
                'M': self.data_length // 30,    
                'Q': self.data_length // 90,    
                'Y': self.data_length // 365    
            }
            fallback_points = max(1, freq_ratios.get(freq_code, self.data_length // 30))
            return {'min_points': fallback_points, 'max_points': fallback_points, 'details': {}}
    
    def validate_frequency_compatibility(self):
        """Проверяет совместимость выбранной частоты с определенной частотой данных"""
        if not hasattr(self, 'detected_frequency') or not self.detected_frequency:
            return True, "Частота данных не определена"
        
        # Получаем выбранную пользователем частоту
        if self.auto_frequency:
            selected_freq = self.detected_frequency
            return True, f"Используется автоопределенная частота: {selected_freq}"
        else:
            freq_index = self.frequency
            if isinstance(freq_index, int) and 0 <= freq_index < len(self.FREQUENCIES):
                selected_freq = self.FREQUENCIES[freq_index][0]
            else:
                selected_freq = self.frequency
        
        detected_freq = self.detected_frequency
        
        # Маппинг частот к их "уровню детализации" 
        freq_hierarchy = {
            'T': 1,     # Минута (самая мелкая)
            'H': 60,    # Час = 60 минут
            'D': 1440,  # День = 1440 минут  
            'B': 1440,  # Рабочий день ≈ день
            'W': 10080, # Неделя = 7 * 1440 минут
            'M': 43200, # Месяц ≈ 30 * 1440 минут
            'Q': 129600,# Квартал ≈ 90 * 1440 минут
            'Y': 525600 # Год ≈ 365 * 1440 минут
        }
        
        detected_level = freq_hierarchy.get(detected_freq, 1440)
        selected_level = freq_hierarchy.get(selected_freq, 1440)
        
        # Вычисляем во сколько раз различаются частоты
        ratio = detected_level / selected_level
        
        self.log(f"Проверка совместимости: данные '{detected_freq}' vs выбрано '{selected_freq}', соотношение: {ratio:.1f}")
        
        # Критические несовместимости (блокируем полностью)
        if ratio < 0.001:  # Выбранная частота в 1000+ раз мельче
            return False, format_message('critical',f"НЕДОПУСТИМО: Частота '{selected_freq}' слишком мелкая для данных '{detected_freq}'!\nЭто создаст миллионы пустых точек и приведет к ошибке.")
        
        if ratio > 100:  # Выбранная частота в 100+ раз крупнее
            return False, format_message('critical',f"НЕДОПУСТИМО: Частота '{selected_freq}' слишком крупная для данных '{detected_freq}'!\nБольшинство данных будет потеряно при агрегации.")
        
        # Серьезные предупреждения (предупреждаем, но не блокируем)
        if ratio < 0.1:  # В 10+ раз мельче
            return True, format_message('caution',f"ОСТОРОЖНО: Частота '{selected_freq}' намного мельче данных '{detected_freq}'. Возможны проблемы с производительностью и памятью.")
        
        if ratio > 10:  # В 10+ раз крупнее
            return True, format_message('caution',f"ОСТОРОЖНО: Частота '{selected_freq}' намного крупнее данных '{detected_freq}'. Много данных будет агрегировано, точность может снизиться.")
        
        # Умеренные различия (информируем)
        if ratio < 0.5 or ratio > 2:
            return True, format_message('info',f"Частоты различаются: данные '{detected_freq}' → прогноз '{selected_freq}'. Данные будут преобразованы.")
        
        # Совместимые частоты
        return True, format_message('success',f"Частоты совместимы: '{detected_freq}' и '{selected_freq}'")

    def update_frequency_info(self):
        # очищаем пул ошибок
        self.clear_messages()
        """Обновляет информацию о частоте БЕЗ блокировки - только информативно"""
        if self.data_length == 0:
            return
            
        # Получаем текущую частоту
        current_freq = self.get_current_frequency()
        
        # Оцениваем количество точек после агрегации для всех ID
        aggregation_info = self.estimate_points_after_aggregation(current_freq)
        min_points = aggregation_info['min_points']
        max_points = aggregation_info['max_points']
        details = aggregation_info['details']
        
        # Определяем количество временных рядов
        num_series = len(details) if details else 1
        
        # Получаем название частоты
        freq_name = current_freq
        for code, label in self.FREQUENCIES:
            if code == current_freq:
                freq_name = f"{label} ({code})"
                break
        
        # Формируем детальную информацию
        if details:
            details_text = []
            for id_name, info in details.items():
                details_text.append(f"{id_name}: {info['points']} точек")
            details_str = " | ".join(details_text[:3])  # Показываем первые 3
            if len(details) > 3:
                details_str += f" | и еще {len(details)-3}..."
        else:
            details_str = f"~{min_points} точек"
        
        # Оценка возможных проблем с цветовой индикацией
        likely_problems = []
        if min_points < 10:
            likely_problems.append("Очень мало данных для обучения")

        # Четырехуровневая система предупреждений
        if self.prediction_length >= min_points:
            likely_problems.append("Прогноз больше или равен данным!")
        elif self.prediction_length > min_points * 0.6:  # Больше 60%
            likely_problems.append("Прогноз больше 60% от данных")
        elif self.prediction_length > min_points * 0.4:  # Больше 40%
            likely_problems.append("Прогноз больше 40% от данных")
        # Если меньше 40% - все хорошо, ничего не добавляем

        # Обновляем отображение только с ИНФОРМАЦИЕЙ
        if min_points == max_points:
            points_info = f"{min_points} точек"
        else:
            points_info = f"{min_points}-{max_points} точек"
        
        info_text = f"Информация о частоте: {freq_name}\n"
        info_text += f"После агрегации: {points_info} ({num_series} рядов)\n"
        info_text += f"{details_str}"
        
        if likely_problems:
            info_text += f"\n"+format_message('warning',f"Возможные проблемы: {', '.join(likely_problems)}")
            info_text += f"\nAutoGluon сам проверит совместимость при запуске"
            style = "color: orange; background-color: #fff7e6; padding: 5px; border-radius: 3px;"
        else:
            info_text += f"\n"+format_message('success',f"Данные выглядят совместимыми с выбранной частотой")
            style = "color: green; background-color: #f0fff0; padding: 5px; border-radius: 3px;"
        
        self.max_length_label.setText(info_text)
        self.max_length_label.setStyleSheet(style)
        
        # Логируем подробности
        self.log(f"Частота: {current_freq}, рядов: {num_series}, точек: {min_points}-{max_points}")

        # Сохраняем для использования в других методах
        self.min_points_current = min_points


    def on_target_column_changed(self):
        self.log(f"Вы выбрали целевую колонку: {self.target_column}")
    def on_id_column_changed(self):
        self.log(f"Вы выбрали ID колонку: {self.id_column}")
        self.log(f"DEBUG: self.data is None = {self.data is None}")  # ← ДОБАВИТЬ
        if self.data is not None:
            self.log("DEBUG: Вызываю update_frequency_info()")  # ← ДОБАВИТЬ
            self.update_frequency_info()
        else:
            self.log("DEBUG: self.data равно None, пропускаю обновление")  # ← ДОБАВИТЬ
    def on_timestamp_column_changed(self):
        self.log(f"Вы выбрали временную колонку: {self.timestamp_column}")

    def on_holidays_changed(self, state):
        self.include_holidays = state > 0
        self.holiday_country_combo.setEnabled(self.include_holidays) # Включаем/отключаем выбор страны

    """def on_date_option_changed(self, state):
        self.use_current_date = state > 0"""
        
    def on_auto_frequency_changed(self, state):
        self.auto_frequency = state > 0
        self.freq_combo.setDisabled(self.auto_frequency)
        if self.data is not None:
            if self.auto_frequency:
                self.detected_freq_label.setText(f"Определенная частота: {self.detected_frequency}")
            self.update_frequency_info()

    def on_prediction_length_changed(self, value):
        """Обновляет проверку при изменении длины прогноза"""
        if self.data is not None:
            self.check_prediction_length()

    def detect_frequency(self, data):
        """ИСПРАВЛЕННАЯ версия - анализирует один временной ряд"""
        try:
            self.log(f"ОТЛАДКА detect_frequency:")
            self.log(f"  - Колонка времени: {self.timestamp_column}")
            self.log(f"  - Всего записей: {len(data)}")
            
            # БЕРЕМ ДАННЫЕ ТОЛЬКО ОДНОГО ID для анализа частоты
            if self.id_column and self.id_column in data.columns:
                unique_ids = data[self.id_column].unique()
                self.log(f"  - Найдено ID: {len(unique_ids)}")
                
                # Берем первый ID для анализа
                first_id = unique_ids[0]
                sample_data = data[data[self.id_column] == first_id].copy()
                self.log(f"  - Анализируем ID '{first_id}': {len(sample_data)} записей")
            else:
                sample_data = data.copy()
                self.log(f"  - Анализируем все данные (без группировки по ID)")
            
            # Сортируем даты ОДНОГО временного ряда
            dates = sample_data[self.timestamp_column].sort_values()
            
            # ПОКАЗЫВАЕМ ДАТЫ ОДНОГО РЯДА
            self.log(f"  - Первые 5 дат одного ряда: {dates.head().tolist()}")
            
            # Если меньше 2 точек, невозможно определить
            if len(dates) < 2:
                return "D"  # По умолчанию день
                
            # Вычисляем разницу между последовательными датами ОДНОГО ряда
            diffs = []
            for i in range(1, min(10, len(dates))):
                diff = dates.iloc[i] - dates.iloc[i-1]
                diff_seconds = diff.total_seconds()
                diffs.append(diff_seconds)
                
                # ПОКАЗЫВАЕМ КАЖДУЮ РАЗНОСТЬ
                self.log(f"  - Разность {i}: {dates.iloc[i]} - {dates.iloc[i-1]} = {diff_seconds/86400:.1f} дней ({diff_seconds} сек)")
                
            # Используем медиану для определения типичного интервала
            if not diffs:
                return "D"
                
            median_diff = pd.Series(diffs).median()
            
            # ПОКАЗЫВАЕМ МЕДИАНУ
            self.log(f"  - Медианная разность: {median_diff} секунд = {median_diff/86400:.1f} дней")
            
            # Определяем частоту на основе интервала
            if median_diff <= 60:  # до 1 минуты
                freq = "T"
                self.log(format_message('error',f"  - ПРОБЛЕМА: Медиана {median_diff} <= 60 секунд → частота T"))
            elif median_diff <= 3600:  # до 1 часа
                freq = "H"
            elif median_diff <= 86400:  # до 1 дня
                freq = "D"
            elif median_diff <= 604800:  # до 1 недели
                freq = "W"
            elif median_diff <= 2678400:  # до ~1 месяца (31 день)
                freq = "M"
                self.log(format_message('ok',f"  - ПРАВИЛЬНО: Медиана {median_diff} секунд → частота M"))
            elif median_diff <= 7948800:  # до ~3 месяцев (92 дня)
                freq = "Q"
            else:  # более 3 месяцев
                freq = "Y"
                
            self.log(format_message('ok',f"Определена частота данных: {freq} (медианный интервал: {median_diff/3600:.1f} часов)"))
            
            return freq
            
        except Exception as e:
            self.log(format_message('error',f"Ошибка при определении частоты: {str(e)}"))
            return "M"  # По умолчанию месячная для безопасности

    def check_prediction_length(self):
        """Проверка длины прогноза с учетом совместимости частот"""
        self.clear_messages()
        
        if self.data_length == 0:
            self.max_allowed_prediction = 365
            self.max_length_label.setText("Максимальная длина прогноза: Н/Д (нет данных)")
            return
        
        # СНАЧАЛА проверяем совместимость частот
        if hasattr(self, 'detected_frequency'):
            is_compatible, freq_message = self.validate_frequency_compatibility()
            if not is_compatible:
                self.error(freq_message)
                self.run_button.setDisabled(True)
                return
            elif "[ОСТОРОЖНО]" in freq_message:
                self.warning(freq_message)
            elif "[ИНФО]" in freq_message:
                self.information(freq_message)
        
        # Остальная логика проверки длины прогноза...
        current_freq = self.get_current_frequency()
        reasonable_limits = {
            'Y': 10, 'Q': 20, 'M': 36, 'W': 104, 
            'D': 365, 'B': 260, 'H': 168, 'T': 1440
        }
        
        self.max_allowed_prediction = reasonable_limits.get(current_freq, 100)
        self.update_frequency_info()
        
        # Проверки длины прогноза
        if hasattr(self, 'min_points_current') and self.min_points_current:
            min_points = self.min_points_current
            
            if self.prediction_length >= min_points:
                self.error(f"Прогноз ({self.prediction_length}) ≥ данных ({min_points})!")
                self.run_button.setDisabled(True)
                return
            elif self.prediction_length > min_points * 0.7:
                self.warning(f"Прогноз составляет {self.prediction_length/min_points*100:.0f}% от данных")
        
        if self.prediction_length > self.max_allowed_prediction:
            self.warning(f"Длина прогноза ({self.prediction_length}) велика для частоты '{current_freq}'")
        
        # Если дошли сюда - разблокируем кнопку
        self.run_button.setDisabled(False)

    def log(self, message):
        """"БЕЗОПАСНОЕ логирование для многопоточности"""
        log_entry = f"{datetime.now().strftime('%H:%M:%S')} - {message}"
        self.log_messages += log_entry + "\n"
        
        # ИСПРАВЛЕНИЕ: Проверяем, что мы в главном потоке
        if QThread.currentThread() == QCoreApplication.instance().thread():
            self.log_widget.appendPlainText(log_entry)
            self.log_widget.verticalScrollBar().setValue(
                self.log_widget.verticalScrollBar().maximum()
            )

    def safe_log_from_worker(self, message):
        """БЕЗОПАСНЫЙ обработчик логов от worker'а"""
        log_entry = f"{datetime.now().strftime('%H:%M:%S')} - {message}"
        self.log_messages += log_entry + "\n"
        
        # Это уже выполняется в главном потоке благодаря сигналу
        self.log_widget.appendPlainText(log_entry)
        self.log_widget.verticalScrollBar().setValue(
            self.log_widget.verticalScrollBar().maximum()
        )

    @Inputs.data
    def set_data(self, dataset):
        self.error("")
        self.warning("")
        try:
            if dataset is None:
                self.data = None
                self.log("Данные очищены")
                self.data_length = 0
                self.max_length_label.setText("Максимальная длина прогноза: N/A")
                self.detected_freq_label.setText("Определенная частота: N/A")
                return
            
            # ДИАГНОСТИКА: Что именно приходит от FormTimeseries
            self.log("=== ДИАГНОСТИКА ВХОДНЫХ ДАННЫХ ===")
            self.log(f"Тип dataset: {type(dataset)}")
            self.log(f"Размер dataset: {dataset.X.shape if hasattr(dataset, 'X') else 'N/A'}")
            
            # Проверяем домен
            domain = dataset.domain
            self.log(f"Количество атрибутов: {len(domain.attributes)}")
            self.log(f"Количество мета: {len(domain.metas)}")
            self.log(f"Количество классов: {len(domain.class_vars) if domain.class_vars else 0}")
            
            # Проверяем переменные
            all_vars = list(domain.attributes) + list(domain.metas) + (list(domain.class_vars) if domain.class_vars else [])
            for var in all_vars:
                self.log(f"Переменная '{var.name}': тип {type(var).__name__}")
                if isinstance(var, TimeVariable):
                    self.log(f"  TimeVariable найдена: {var.name}")
            
            # Получаем сырые данные для проверки
            temp_df = self.prepare_data(dataset, for_type_check_only=True)
            if temp_df is not None and len(temp_df) > 0:
                self.log("=== ОБРАЗЕЦ СЫРЫХ ДАННЫХ ===")
                for col in temp_df.columns:
                    sample_vals = temp_df[col].head(3).tolist()
                    self.log(f"Колонка '{col}' ({temp_df[col].dtype}): {sample_vals}")
                    
                    # Особая проверка для временных колонок
                    if 'date' in col.lower() or 'time' in col.lower():
                        if pd.api.types.is_numeric_dtype(temp_df[col]):
                            min_val, max_val = temp_df[col].min(), temp_df[col].max()
                            self.log(f"  Числовой диапазон: {min_val} - {max_val}")
                            
                            # Проверяем, похоже ли на timestamp
                            if min_val > 1e9:  # Больше миллиарда - вероятно timestamp
                                sample_timestamp = pd.to_datetime(min_val, unit='s', errors='ignore')
                                self.log(f"  Как timestamp (сек): {sample_timestamp}")
                                sample_timestamp_ms = pd.to_datetime(min_val, unit='ms', errors='ignore')
                                self.log(f"  Как timestamp (мс): {sample_timestamp_ms}")
            
            self.log("=== КОНЕЦ ДИАГНОСТИКИ ===")
            
            # Проверка наличия специальных атрибутов от FormTimeseries
            self.from_form_timeseries = False  # Сбрасываем флаг
            if hasattr(dataset, 'from_form_timeseries') and dataset.from_form_timeseries:
                self.from_form_timeseries = True
                self.log("Данные получены из компонента FormTimeseries")
                # Если данные от FormTimeseries, можно получить дополнительную информацию
                if hasattr(dataset, 'time_variable') and dataset.time_variable:
                    self.timestamp_column = dataset.time_variable
                    self.log(f"Автоматически установлена временная переменная: {self.timestamp_column}")
            
            # Получаем колонки из dataset ДО prepare_data
            domain = dataset.domain
            attr_cols = [var.name for var in domain.attributes]
            meta_cols = [var.name for var in domain.metas]
            class_cols = [var.name for var in domain.class_vars] if domain.class_vars else []
            self.all_columns = attr_cols + class_cols + meta_cols
            
            # Находим и сохраняем категориальные маппинги
            self.categorical_mapping = {}  # Сбрасываем предыдущие маппинги
            for var in domain.variables + domain.metas:
                if hasattr(var, 'values') and var.values:
                    # Получаем список значений категориальной переменной
                    values = var.values
                    if values:
                        self.log(f"Сохраняем маппинг для категориальной переменной '{var.name}': {values}")
                        self.categorical_mapping[var.name] = values

            # ДОБАВЛЕНО: Проверяем наличие TimeVariable
            time_vars = []
            for var in domain.variables + domain.metas:
                if isinstance(var, TimeVariable):
                    time_vars.append(var.name)
            
            if time_vars:
                self.log(f"Обнаружены временные переменные: {', '.join(time_vars)}")
                if self.timestamp_column not in time_vars:
                    # Автоматически выбираем первую временную переменную
                    self.timestamp_column = time_vars[0]
                    self.log(f"Автоматически выбрана временная переменная (TimeVariable по умолчанию): {self.timestamp_column}")
            
            if not self.all_columns:
                raise ValueError("Нет колонок в данных!")
            
            # --- Автоматическое определение столбцов ---
            # Пытаемся определить, только если текущий выбор невалиден или не сделан
            
            # Получаем DataFrame для проверки типов, если еще не создан
            temp_df_for_types = None
            if not isinstance(dataset, pd.DataFrame): # Если на вход пришел Orange.data.Table
                temp_df_for_types = self.prepare_data(dataset, for_type_check_only=True)
            else: # Если на вход уже пришел DataFrame (маловероятно для set_data, но для полноты)
                temp_df_for_types = dataset

            # Целевой столбец
            if not self.target_column or self.target_column not in self.all_columns:
                self.log(f"Целевой столбец '{self.target_column}' не установлен или не найден в текущих данных. Попытка автоопределения...")
                potential_target = None
                
                # 1. Проверяем Orange Class Variable
                if domain.class_vars:
                    for cv in domain.class_vars:
                        if isinstance(cv, ContinuousVariable) or \
                        (temp_df_for_types is not None and cv.name in temp_df_for_types.columns and pd.api.types.is_numeric_dtype(temp_df_for_types[cv.name])):
                            potential_target = cv.name
                            self.log(f"Найдена целевая колонка из Orange Class Variable: '{potential_target}'")
                            break
                
                if not potential_target:
                    # 2. Ищем по приоритетным точным именам
                    priority_names = ["Target", "target", "sales", "Sales", "value", "Value"]
                    for name in priority_names:
                        if name in self.all_columns and \
                        (temp_df_for_types is not None and name in temp_df_for_types.columns and pd.api.types.is_numeric_dtype(temp_df_for_types[name])):
                            potential_target = name
                            self.log(f"Найдена целевая колонка по точному приоритетному имени: '{potential_target}'")
                            break
                
                if not potential_target and self.all_columns and temp_df_for_types is not None:
                    # 3. Ищем по подстрокам (числовые)
                    search_terms = ["target", "sales", "value"]
                    for term in search_terms:
                        for col_name in self.all_columns:
                            if term in col_name.lower() and col_name in temp_df_for_types.columns and \
                            pd.api.types.is_numeric_dtype(temp_df_for_types[col_name]):
                                potential_target = col_name
                                self.log(f"Найдена целевая колонка по подстроке '{term}': '{potential_target}' (числовая)")
                                break
                        if potential_target: break

                if not potential_target and self.all_columns and temp_df_for_types is not None:
                    # 4. Берем первую числовую Orange ContinuousVariable, не являющуюся ID или Timestamp
                    for var in domain.attributes: # Атрибуты обычно числовые или категориальные
                        if isinstance(var, ContinuousVariable) and var.name not in [self.id_column, self.timestamp_column]:
                            potential_target = var.name
                            self.log(f"В качестве целевой колонки выбрана первая Orange ContinuousVariable: '{potential_target}'")
                            break
                    if not potential_target: # Если не нашли среди атрибутов, ищем просто числовую
                        for col in self.all_columns:
                            if col not in [self.id_column, self.timestamp_column] and \
                            col in temp_df_for_types.columns and pd.api.types.is_numeric_dtype(temp_df_for_types[col]):
                                potential_target = col
                                self.log(f"В качестве целевой колонки выбрана первая числовая: '{potential_target}'")
                                break

                self.target_column = potential_target if potential_target else (self.all_columns[0] if self.all_columns else "")
                self.log(f"Автоматически выбран целевой столбец: '{self.target_column}'")

            # ID столбец
            if not self.id_column or self.id_column not in self.all_columns:
                self.log(f"ID столбец '{self.id_column}' не установлен или не найден в текущих данных. Попытка автоопределения...")
                potential_id = None
                # 1. Ищем Orange DiscreteVariable или StringVariable (не цель и не время)
                for var_list in [domain.attributes, domain.metas]:
                    for var in var_list:
                        if var.name not in [self.target_column, self.timestamp_column] and \
                        (isinstance(var, DiscreteVariable) or isinstance(var, StringVariable)):
                            potential_id = var.name
                            self.log(f"Найдена ID колонка из Orange Discrete/String Variable: '{potential_id}'")
                            break
                    if potential_id: break
                
                if not potential_id:
                    # 2. Поиск по стандартным именам
                    potential_id = next((name for name in ["item_id", "id", "ID", "Country", "Shop", "City"] if name in self.all_columns and name not in [self.target_column, self.timestamp_column]), None)
                    if potential_id: self.log(f"Найдена ID колонка по стандартному имени: '{potential_id}'")

                if not potential_id and self.all_columns and temp_df_for_types is not None:
                    # 3. Ищем подходящий тип (строка/объект/категория), не цель и не время
                    for col in self.all_columns:
                        if col not in [self.target_column, self.timestamp_column] and col in temp_df_for_types.columns and \
                        (pd.api.types.is_string_dtype(temp_df_for_types[col]) or \
                            pd.api.types.is_object_dtype(temp_df_for_types[col]) or \
                            pd.api.types.is_categorical_dtype(temp_df_for_types[col])):
                            potential_id = col
                            self.log(f"Найдена подходящая по типу ID колонка: '{potential_id}'")
                            break
                self.id_column = potential_id if potential_id else (next((c for c in self.all_columns if c not in [self.target_column, self.timestamp_column]), self.all_columns[0] if self.all_columns else ""))
                self.log(f"Автоматически выбран ID столбец: '{self.id_column}'")

            # Временной столбец (если не определен как TimeVariable и невалиден)
            if not self.timestamp_column or self.timestamp_column not in self.all_columns:
                self.log(f"Временной столбец '{self.timestamp_column}' не установлен/не найден или не является TimeVariable. Попытка автоопределения...")
                potential_ts = None
                # 1. Orange TimeVariable уже должен был быть выбран ранее в set_data.
                # Здесь мы ищем, если он не был TimeVariable или стал невалидным.
                
                # 2. Поиск по стандартным именам
                potential_ts = next((name for name in ["timestamp", "Timestamp", "time", "Time", "Date", "date"] if name in self.all_columns and name not in [self.target_column, self.id_column]), None)
                if potential_ts: self.log(f"Найдена временная колонка по стандартному имени: '{potential_ts}'")

                if not potential_ts and self.all_columns and temp_df_for_types is not None:
                    # 3. Пытаемся распарсить
                    for col in self.all_columns:
                        if col not in [self.target_column, self.id_column] and col in temp_df_for_types.columns:
                            try:
                                parsed_sample = pd.to_datetime(temp_df_for_types[col].dropna().iloc[:5], errors='coerce')
                                if not parsed_sample.isna().all():
                                    potential_ts = col
                                    self.log(f"Найдена подходящая по типу временная колонка: '{potential_ts}' (можно преобразовать в дату)")
                                    break
                            except Exception:
                                continue
                self.timestamp_column = potential_ts if potential_ts else (next((c for c in self.all_columns if c not in [self.target_column, self.id_column]), self.all_columns[0] if self.all_columns else ""))
                self.log(f"Автоматически выбран временной столбец: '{self.timestamp_column}'")
            
            self.log("Обработка входных данных...")
            self.data = self.prepare_data(dataset)
            
            # Обновляем выпадающие списки колонок
            self.target_combo.clear()
            self.id_combo.clear()
            self.timestamp_combo.clear()
            
            self.target_combo.addItems(self.all_columns)
            self.id_combo.addItems(self.all_columns)
            self.timestamp_combo.addItems(self.all_columns)
            
            # Устанавливаем выбранные значения в comboBox'ах
            self.target_combo.setCurrentText(self.target_column)
            self.id_combo.setCurrentText(self.id_column)
            self.timestamp_combo.setCurrentText(self.timestamp_column)
            
            # Логируем финальный выбор колонок после автоопределения (если оно было) и установки в UI
            self.log(f"Автоопределены колонки — Target: {self.target_column}, ID: {self.id_column}, Timestamp: {self.timestamp_column}")
            
            required = {self.timestamp_column, self.target_column, self.id_column}
            if not required.issubset(set(self.data.columns)):
                missing = required - set(self.data.columns)
                raise ValueError(f"Отсутствуют столбцы: {missing}")
                
            # Получаем длину данных
            self.data_length = len(self.data)
            self.log(f"Загружено {self.data_length} записей")
            
            # Определяем частоту данных
            if pd.api.types.is_datetime64_dtype(self.data[self.timestamp_column]):
                self.detected_frequency = self.detect_frequency(self.data)
                self.detected_freq_label.setText(f"Определенная частота: {self.detected_frequency}")
            
            # В конце set_data, после определения частоты
            if pd.api.types.is_datetime64_dtype(self.data[self.timestamp_column]):
                self.detected_frequency = self.detect_frequency(self.data)
                self.detected_freq_label.setText(f"Определенная частота: {self.detected_frequency}")
                
                # НОВОЕ: Начальная проверка совместимости
                if not self.auto_frequency:
                    is_compatible, message = self.validate_frequency_compatibility()
                    if not is_compatible:
                        self.error(message)
                        self.run_button.setDisabled(True)
                        # Автоматически включаем автоопределение для безопасности
                        self.auto_frequency = True
                        self.auto_freq_checkbox.setChecked(True)
                        self.freq_combo.setDisabled(True)
                        self.log("Автоопределение частоты включено автоматически для предотвращения ошибок")

            # Обновляем максимальную длину прогноза
            self.check_prediction_length()
            
        except Exception as e:
            self.log(f"ОШИБКА: {str(e)}\n{traceback.format_exc()}")
            self.error(f"Ошибка данных: {str(e)}")
            self.data = None
            self.data_length = 0
            self.max_length_label.setText("Максимальная длина прогноза: N/A")

    def prepare_data(self, table, for_type_check_only=False):
        """Подготовка данных"""
        self.log(f"prepare_data вызвана: for_type_check_only={for_type_check_only}")
        
        if table is None:
            return None

        domain = table.domain
        # Получаем атрибуты
        attr_cols = [var.name for var in domain.attributes]
        df = pd.DataFrame(table.X, columns=attr_cols)
        
        # Добавляем классы, если есть
        if domain.class_vars:
            class_cols = [var.name for var in domain.class_vars]
            class_data = table.Y
            if len(domain.class_vars) == 1:
                class_data = class_data.reshape(-1, 1)
            df_class = pd.DataFrame(class_data, columns=class_cols)
            df = pd.concat([df, df_class], axis=1)
        
        # Добавляем мета-атрибуты
        if domain.metas:
            meta_cols = [var.name for var in domain.metas]
            meta_data = table.metas
            df_meta = pd.DataFrame(meta_data, columns=meta_cols)
            df = pd.concat([df, df_meta], axis=1)
        
        if for_type_check_only:
            return df

        # ПРОСТАЯ ОБРАБОТКА БЕЗ ПРОВЕРОК "КОРРЕКТНОСТИ"
        self.log("Обработка данных...")
        
        # 1. Обработка колонки времени
        if self.timestamp_column and self.timestamp_column in df.columns:
            if not pd.api.types.is_datetime64_dtype(df[self.timestamp_column]):
                try:
                    # Проверяем первое значение, чтобы понять формат
                    first_value = df[self.timestamp_column].iloc[0] if len(df) > 0 else None
                    
                    # Проверяем, является ли первое значение числом (даже если dtype=object)
                    if first_value is not None:
                        try:
                            float_val = float(first_value)
                            if float_val > 1e9:  # Похоже на Unix timestamp
                                df[self.timestamp_column] = pd.to_datetime(df[self.timestamp_column].astype(float), unit='s')
                                self.log(format_message('success',"Преобразованы Unix timestamps в даты (из object dtype)"))
                            else:
                                df[self.timestamp_column] = pd.to_datetime(df[self.timestamp_column])
                                self.log(format_message('success'," Преобразованы числовые даты"))
                        except (ValueError, TypeError):
                            # Это действительно строки
                            df[self.timestamp_column] = pd.to_datetime(df[self.timestamp_column])
                            self.log(format_message('success',"Преобразованы строковые даты"))
                    else:
                        df[self.timestamp_column] = pd.to_datetime(df[self.timestamp_column])
                        self.log(format_message('success',"Преобразованы даты"))
                        
                    # Показываем что получилось
                    self.log(f"Диапазон дат: {df[self.timestamp_column].min()} - {df[self.timestamp_column].max()}")
                    if self.id_column in df.columns:
                        for country in df[self.id_column].unique()[:3]:
                            country_data = df[df[self.id_column] == country]
                            self.log(f"  {country}: {len(country_data)} записей, "
                                f"{country_data[self.timestamp_column].min()} - "
                                f"{country_data[self.timestamp_column].max()}")
                            
                except Exception as e:
                    self.log(format_message('error',f"Не удалось преобразовать даты: {str(e)}"))
                    self.log("Создаем искусственные даты как запасной вариант")
                    df = self.create_reasonable_dates(df)
        
        # 2. Обработка целевой колонки
        if self.target_column and self.target_column in df.columns:
            df[self.target_column] = pd.to_numeric(df[self.target_column], errors="coerce")
            self.log(f"Target колонка: {df[self.target_column].dtype}")

        # 3. Обработка ID колонки
        if self.id_column and self.id_column in df.columns:
            df[self.id_column] = df[self.id_column].astype(str)
            self.log(f"ID колонка: {df[self.id_column].dtype}")
        
        # 4. Удаляем пустые строки
        cols_to_check = [col for col in [self.timestamp_column, self.target_column, self.id_column] 
                        if col and col in df.columns]
        if cols_to_check:
            df = df.dropna(subset=cols_to_check)
        
        self.log(f"Итого: {len(df)} записей")
        return df

    def create_reasonable_dates(self, df):
        """Создает разумные последовательные даты для каждой категории"""
        self.log("Создание разумных дат для каждой категории...")
        
        # Если есть ID колонка, создаем даты для каждой категории отдельно
        if self.id_column and self.id_column in df.columns:
            df_list = []
            start_date = pd.Timestamp('2023-01-01')
            
            for id_val in df[self.id_column].unique():
                id_data = df[df[self.id_column] == id_val].copy()
                num_records = len(id_data)
                
                # Создаем последовательные даты для этой категории
                dates = pd.date_range(start=start_date, periods=num_records, freq='D')
                id_data[self.timestamp_column] = dates
                
                df_list.append(id_data)
                
                # Следующая категория начинается после окончания предыдущей
                start_date = dates[-1] + pd.Timedelta(days=1)
                
                self.log(f"Категория {id_val}: {num_records} дат от {dates[0].date()} до {dates[-1].date()}")
            
            return pd.concat(df_list, ignore_index=True)
        else:
            # Если нет ID колонки, создаем простую последовательность
            start_date = pd.Timestamp('2023-01-01')
            dates = pd.date_range(start=start_date, periods=len(df), freq='D')
            df[self.timestamp_column] = dates
            self.log(f"Создана единая последовательность дат от {dates[0].date()} до {dates[-1].date()}")
            return df

    def create_future_dates(self, periods):
        """Создает будущие даты с учетом нужной частоты"""
        # Берем последнюю дату из временного ряда
        try:
            self.log(f"DEBUG create_future_dates: self.data[{self.timestamp_column}].dtype = {self.data[self.timestamp_column].dtype}")
            self.log(f"DEBUG create_future_dates: последние даты = \n{self.data[self.timestamp_column].tail().to_string()}")
            
            # ИСПРАВЛЕНИЕ: Убеждаемся, что данные отсортированы по дате
            if not self.data[self.timestamp_column].is_monotonic_increasing:
                self.log("Данные не отсортированы по дате, выполняем сортировку...")
                self.data = self.data.sort_values([self.id_column, self.timestamp_column])
            
            # Получаем последнюю дату
            raw_last_date = self.data[self.timestamp_column].iloc[-1]  # Используем iloc[-1] вместо max()
            self.log(f"Используется последняя дата из данных (по порядку): {raw_last_date}, тип: {type(raw_last_date)}")
            
            # Преобразуем в Timestamp если нужно
            if isinstance(raw_last_date, pd.Timestamp):
                last_date = raw_last_date
            elif pd.api.types.is_datetime64_any_dtype(raw_last_date):
                last_date = pd.Timestamp(raw_last_date)
            elif isinstance(raw_last_date, str):
                try:
                    last_date = pd.to_datetime(raw_last_date)
                    self.log(f"Строковая дата успешно преобразована: {last_date}")
                except Exception as e_str:
                    self.log(f"Ошибка преобразования строковой даты: {e_str}")
                    last_date = pd.Timestamp.now().normalize()
            elif isinstance(raw_last_date, (int, float)):
                self.log(f"Числовая дата: {raw_last_date}. Попытка преобразования из Unix timestamp.")
                if pd.Timestamp("2000-01-01").timestamp() < raw_last_date < pd.Timestamp("2050-01-01").timestamp():
                    last_date = pd.Timestamp(raw_last_date, unit='s')
                    self.log(f"Преобразовано из секунд: {last_date}")
                elif pd.Timestamp("2000-01-01").timestamp() * 1000 < raw_last_date < pd.Timestamp("2050-01-01").timestamp() * 1000:
                    last_date = pd.Timestamp(raw_last_date, unit='ms')
                    self.log(f"Преобразовано из миллисекунд: {last_date}")
                else:
                    try:
                        last_date = pd.to_datetime(raw_last_date)
                        self.log(f"Преобразовано pd.to_datetime (авто): {last_date}")
                    except:
                        last_date = pd.Timestamp.now().normalize()
                        self.log(f"Не удалось определить масштаб timestamp. Используем текущую дату: {last_date}")
            else:
                try:
                    last_date = pd.to_datetime(raw_last_date)
                    self.log(f"Дата преобразована из типа {type(raw_last_date)}: {last_date}")
                except Exception as e_conv:
                    self.log(f"Не удалось преобразовать дату '{raw_last_date}' в datetime: {e_conv}. Используем текущую дату.")
                    last_date = pd.Timestamp.now().normalize()

        except Exception as e:
            self.log(f"Ошибка при получении/обработке последней даты: {e}")
            last_date = pd.Timestamp.now().normalize()

        # Определяем частоту
        #freq = self.detected_frequency if self.auto_frequency else self.frequency
        if self.auto_frequency:
            freq = self.detected_frequency
        else:
            freq_index = self.frequency
            if isinstance(freq_index, int) and 0 <= freq_index < len(self.FREQUENCIES):
                freq = self.FREQUENCIES[freq_index][0]
            else:
                freq = self.frequency
        self.log(f"Создание будущих дат от {last_date} с частотой {freq}")
        
        try:
            # ИСПРАВЛЕНИЕ: Начинаем с СЛЕДУЮЩЕГО дня после последней даты
            start_date = last_date + pd.tseries.frequencies.to_offset(freq)
            self.log(f"Начальная дата для прогноза: {start_date}")
            
            # Создаем диапазон дат
            if freq == 'B':
                all_dates = pd.date_range(start=start_date, periods=periods * 2, freq='D')
                dates = all_dates[all_dates.weekday < 5][:periods]
            else:
                dates = pd.date_range(start=start_date, periods=periods, freq=freq)
                
        except Exception as e:
            self.log(f"Ошибка при создании дат: {e}")
            
            try:
                start_date = last_date + pd.Timedelta(days=1)
                dates = pd.date_range(start=start_date, periods=periods, freq='D')
                self.log(f"Используем альтернативные даты с {start_date}")
            except:
                base_date = pd.Timestamp('2024-01-01')
                dates = pd.date_range(start=base_date, periods=periods, freq='D')
                self.log(f"Используем фиксированные даты с {base_date}")

        self.log(f"Создан диапазон дат для прогноза: с {dates[0]} по {dates[-1]}")
        return dates

    def create_future_dates_for_specific_id(self, last_date, model_freq):
        """
        УНИВЕРСАЛЬНАЯ функция создания будущих дат для конкретного ID
        Работает с любыми типами дат и частотами
        """
        try:
            # Нормализуем дату
            if not isinstance(last_date, pd.Timestamp):
                last_date = pd.to_datetime(last_date)
            
            # Получаем частоту            
            freq = model_freq
            self.log(f"[DEBUG] Генерация дат с частотой: {freq}")

            # Создаем следующую дату
            try:
                offset = pd.tseries.frequencies.to_offset(freq)
                start_date = last_date + offset
            except:
                start_date = last_date + pd.Timedelta(days=1)
            
            # Создаем диапазон дат
            try:
                if freq == 'B':  # Рабочие дни
                    all_dates = pd.date_range(start=start_date, periods=self.prediction_length * 2, freq='D')
                    dates = all_dates[all_dates.weekday < 5][:self.prediction_length]
                else:
                    dates = pd.date_range(start=start_date, periods=self.prediction_length, freq=freq)
            except:
                # Универсальный запасной вариант
                dates = pd.date_range(start=start_date, periods=self.prediction_length, freq='D')
            
            return dates
            
        except Exception as e:
            self.log(f"Ошибка создания дат: {e}")
            # Крайний запасной вариант
            try:
                start_date = pd.to_datetime(last_date) + pd.Timedelta(days=1)
                dates = pd.date_range(start=start_date, periods=self.prediction_length, freq='D')
                return dates
            except:
                # Если совсем ничего не работает
                base_date = pd.Timestamp('2024-01-01')
                dates = pd.date_range(start=base_date, periods=self.prediction_length, freq='D')
                return dates

    def run_model(self):
        # очищаем пул ошибок
        self.clear_messages()
        """Запуск асинхронного обучения"""
        if self.data is None:
            self.error("Нет данных")
            return
            
        if hasattr(self, 'is_training') and self.is_training:
            self.warning("Обучение уже выполняется")
            return
        
        # Валидация данных
        validation_result = self.validate_data_before_training()
        if not validation_result:
            return
            
        # Подготовка к обучению
        self.is_training = True
        self.run_button.setDisabled(True)
        self.cancel_button.setDisabled(False)
        self.progress_widget.setVisible(True)
        self.progress_label.setText("Начинаем...")
        self.progress_widget.setValue(0)
        
        self.log("[СТАРТ] Запуск асинхронного обучения...")
        
        # Создание и запуск рабочего потока
        self.worker = AutoGluonWorker(self)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.log_updated.connect(self.safe_log_from_worker)
        self.worker.training_finished.connect(self.on_training_finished)
        self.worker.training_failed.connect(self.on_training_failed)
        self.worker.finished.connect(self.on_worker_finished)
        
        self.worker.start()

    def cancel_training(self):
        """Отмена обучения"""
        if self.worker and self.worker.isRunning():
            self.log("Запрос отмены обучения...")
            self.worker.cancel()
            self.worker.quit()
            self.worker.wait(5000)  # Ждем 5 секунд
            
            if self.worker.isRunning():
                self.log("Принудительная остановка потока...")
                self.worker.terminate()
                self.worker.wait()
                
        self.reset_ui_after_training()
        self.log("Обучение отменено пользователем")
    
    def update_progress(self, progress, message):
        """Обновление прогресс-бара"""
        self.training_progress = progress
        self.progress_widget.setValue(progress)
        self.progress_label.setText(f"{progress}% - {message}") 
        QCoreApplication.processEvents()
    
    def on_training_finished(self, predictor, predictions, leaderboard, model_info, ensemble_info):
        """Обработка успешного завершения обучения"""
        try:
            self.log("=== Обучение успешно завершено! ===")
            
            # Обработка прогноза
            pred_df = self.process_predictions(predictions)
            pred_table = self.df_to_table(pred_df)
            self.Outputs.prediction.send(pred_table)
            
            # Отправка лидерборда
            if leaderboard is not None:
                lb_table = self.df_to_table(leaderboard)
                self.Outputs.leaderboard.send(lb_table)
    
            # Отправка состава ансамбля как отдельной таблицы
            if ensemble_info is not None:
                ensemble_table = self.df_to_table(ensemble_info)
                self.Outputs.ensemble_info.send(ensemble_table)
                self.log("=== Состав ансамбля отправлен в отдельную таблицу ===")

            # Отправка информации о модели
            self.Outputs.model_info.send(self.df_to_table(model_info))
            
            self.log("=== Все результаты отправлены на выходы виджета ===")
            
        except Exception as e:
            self.log(f"!!! Ошибка при обработке результатов: {str(e)} !!!")
            self.error(f"!!! Ошибка обработки результатов: {str(e)} !!!")
        
        finally:
            self.reset_ui_after_training()
    
    def on_training_failed(self, error_message):
        """Обработка ошибки обучения"""
        self.log(f"!!! ОШИБКА ОБУЧЕНИЯ: {error_message} !!!")
        self.error("!!! Ошибка обучения модели !!!")
        self.reset_ui_after_training()
    
    def on_worker_finished(self):
        """Вызывается когда поток завершается"""
        self.worker = None
    
    def reset_ui_after_training(self):
        """Сброс UI после завершения обучения"""
        self.is_training = False
        self.run_button.setDisabled(False)
        self.cancel_button.setDisabled(True)
        self.progress_widget.setVisible(False)         
        self.progress_label.setText("Готов к запуску") 
        self.progress_widget.setValue(0)               
        
        # Отправляем финальные логи
        self.Outputs.log_messages.send(self.log_messages)
    
    def validate_data_before_training(self):
        """Валидация данных перед запуском обучения"""
        # Проверка выбранных колонок
        required_columns = [self.timestamp_column, self.target_column, self.id_column]
        missing_columns = [col for col in required_columns if col not in self.data.columns]
        
        if missing_columns:
            self.error(f"Отсутствуют колонки: {missing_columns}")
            return False
        
        # Проверка совместимости частот
        if hasattr(self, 'detected_frequency'):
            is_compatible, message = self.validate_frequency_compatibility()
            if not is_compatible:
                self.error(message)
                return False
        
        # Проверка длины прогноза
        if hasattr(self, 'min_points_current') and self.min_points_current:
            if self.prediction_length >= self.min_points_current:
                self.error(f"Прогноз ({self.prediction_length}) больше данных ({self.min_points_current})")
                return False
        
        return True
    
    def process_predictions(self, predictions):
        """Обработка прогнозов (вынесено из run_model для переиспользования)"""
        # Здесь весь код обработки прогнозов из старой функции run_model
        # (тот большой блок с try/except для обработки TimeSeriesDataFrame)
        try:
            if hasattr(predictions, 'reset_index'):
                return predictions.reset_index(drop=True)
            else:
                return predictions
        except Exception as e:
            self.log(f"Ошибка обработки прогноза: {str(e)}")
            return pd.DataFrame()  # Пустой DataFrame при ошибке

    def df_to_table(self, df):
        """Безопасное преобразование DataFrame в таблицу Orange"""
        try:
            # Убедимся, что DataFrame не содержит индексов
            self.log(f"=== НАЧАЛО df_to_table ===")
            self.log(f"Входные колонки: {list(df.columns)}")
            
            df = df.reset_index(drop=True).copy()
            self.log(f"После reset_index: {list(df.columns)}")
            
            # Раздельные списки для атрибутов, классов и мета-переменных
            attrs = []
            metas = []
            
            # Безопасное преобразование всех типов данных и создание соответствующих переменных
            X_cols = []  # Для непрерывных переменных (атрибутов)
            M_cols = []  # Для строковых переменных (мета)
            
            for col in df.columns:
                # Специальная обработка для ID колонки
                if col == self.id_column:
                    # ID колонку всегда храним как мета-переменную
                    df[col] = df[col].fillna('').astype(str)
                    metas.append(StringVariable(name=str(col)))
                    M_cols.append(col)
                # Обрабатываем числовые данные - идут в X
                elif pd.api.types.is_numeric_dtype(df[col]):
                    # Преобразуем в float, который Orange может обработать
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(float('nan')).astype(float)
                    attrs.append(ContinuousVariable(name=str(col)))
                    X_cols.append(col)
                else:
                    # Все нечисловые данные идут в мета
                    # Обрабатываем даты
                    if pd.api.types.is_datetime64_dtype(df[col]):
                        df[col] = df[col].dt.strftime('%Y-%m-%d')
                    
                    # Все остальное - в строки
                    df[col] = df[col].fillna('').astype(str)
                    metas.append(StringVariable(name=str(col)))
                    M_cols.append(col)
            
            self.log(f"Атрибуты: {[v.name for v in attrs]}")
            self.log(f"Мета: {[v.name for v in metas]}")
            
            # Создаем домен
            domain = Domain(attrs, metas=metas)
            
            # Создаем массивы для X и M
            if X_cols:
                X = df[X_cols].values
            else:
                X = np.zeros((len(df), 0))
                
            if M_cols:
                M = df[M_cols].values
            else:
                M = np.zeros((len(df), 0), dtype=object)
            
            # Создаем таблицу с помощью from_numpy
            return Table.from_numpy(domain, X, metas=M)
            
        except Exception as e:
            self.log(f"Ошибка преобразования DataFrame в Table: {str(e)}\n{traceback.format_exc()}")
            raise

if __name__ == "__main__":
    WidgetPreview(OWAutoGluonTimeSeries).run()
