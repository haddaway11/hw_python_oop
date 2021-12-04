class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str, duration: float, distance: float, speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')

   # show_training_info()


class Training:
    """Базовый класс тренировки."""
    TRAINING_TYPE = ''
    M_IN_KM = 1000
    LEN_STEP = 0.65  

    def __init__(self,
                 action: int, #количество совершённых действий
                 duration: float,  #prodolzitelnost
                 weight: float,   #massa
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
        speed = self.get_distance()/self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""       
        infomes = InfoMessage(self.__class__.__name__, self.duration, self.get_distance(), self.get_mean_speed(), self.get_spent_calories())
        return infomes



class Running(Training):
    """Тренировка: бег."""
    TRAINING_TYPE = 'RUN'

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        spentcal = (coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2) * self.weight / self.M_IN_KM * self.duration*60
        return spentcal


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    TRAINING_TYPE = 'WLK'
    def __init__(self,
                 action: int,      #количество совершённых действий
                 duration: float,  #prodolzitelnost
                 weight: float,    #massa
                 height: float,    #рост
                 ) -> None:
        # наследуем функциональность конструктора из класса-родителя
        super().__init__(action, duration, weight)
        # добавляем новую функциональность: свойство height
        self.height = height
    
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_3 = 0.035
        coeff_calorie_4 = 0.029
        spentcal = (coeff_calorie_3 * self.weight + (self.get_mean_speed()**2 // self.height) * coeff_calorie_4 * self.weight) * self.duration*60
        return spentcal


class Swimming(Training):
    """Тренировка: плавание."""
    TRAINING_TYPE = 'SWM'
    def __init__(self,
                 action: int,      #количество совершённых действий
                 duration: float,  #prodolzitelnost
                 weight: float,    #massa
                 length_pool: float,   #длина бассейна в метрах
                 count_pool: float,    #сколько раз пользователь переплыл бассейн
                 ) -> None:
        # наследуем функциональность конструктора из класса-родителя
        super().__init__(action, duration, weight)
        # добавляем новую функциональность: свойство length_pool, count_pool
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.length_pool*self.count_pool/self.M_IN_KM/self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_5 = 1.1
        spentcal = (self.get_mean_speed() + coeff_calorie_5) * 2 * self.weight
        return spentcal

    def get_distance(self) -> float:

        """Получить дистанцию в км."""
        M_IN_KM = 1000
        LEN_STEP = 1.38              
        distance = self.action * LEN_STEP / M_IN_KM
        return distance

def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return type[workout_type](*data)
    


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
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

