from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    COEFF_CALORIE_1: int = 18  # коэфициенты для подсчета калорий
    COEFF_CALORIE_2: int = 20  # коэфициенты для подсчета калорий
    COEFF_CALORIE_3: float = 0.035  # коэфициенты для подсчета калорий
    COEFF_CALORIE_4: float = 0.029  # коэфициенты для подсчета калорий
    HOUR_IN_MIN: int = 60  # коэфициенты для подсчета калорий
    CALORIE_RATIO: float = 1.1
    CALORIE_RATIO_2: int = 2

    def __init__(self,
                 action: int,  # количество
                 duration: float,  # часы
                 weight: float,  # килограммы
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        infomes = InfoMessage(self.__class__.__name__,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories())
        return infomes


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = (         # у нас в задании в примере COEFF_CALORIE
            (self.COEFF_CALORIE_1 * self.get_mean_speed()
             - self.COEFF_CALORIE_2) * self.weight
            / self.M_IN_KM * self.duration * self.HOUR_IN_MIN
        )
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,      # количество совершённых действий
                 duration: float,  # продолжительность в часах
                 weight: float,    # масса в кг
                 height: float,    # рост в метрах
                 ) -> None:
        # наследуем функциональность конструктора из класса-родителя
        super().__init__(action, duration, weight)
        # добавляем новую функциональность: свойство height
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calorie = (
            (self.COEFF_CALORIE_3 * self.weight
             + self.get_mean_speed()**2 // self.height * self.COEFF_CALORIE_4
             * self.weight) * self.duration * self.HOUR_IN_MIN
        )
        return calorie


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38  # переопределяем для класса плавание

    def __init__(self,
                 action: int,      # количество совершённых действий
                 duration: float,  # продолжительность
                 weight: float,    # масса
                 length_pool: float,   # длина бассейна в метрах
                 count_pool: float,    # сколько раз переплыл бассейн
                 ) -> None:
        # наследуем функциональность конструктора из класса-родителя
        super().__init__(action, duration, weight)
        # добавляем новую функциональность: свойство length_pool, count_pool
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calori = (
            (self.get_mean_speed() + self.CALORIE_RATIO) * self.CALORIE_RATIO_2
            * self.weight
        )
        return calori

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    types = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type in types.keys():
        return types[workout_type](*data)
    else:
        print("Ошибка ключ не совпадает")


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
