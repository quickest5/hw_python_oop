from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    """вставляется в часах"""
    distance: float
    """вставляется в км"""
    speed: float
    """вставляется в км/ч"""
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        """вставляется в часах"""
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20
    duration: float
    """вставляется в часах"""
    distance: float
    """вставляется в км"""
    speed: float
    """вставляется в км/ч"""

    def get_spent_calories(self):
        self.spent_calories = ((
            self.coeff_calorie_1
            * self.get_mean_speed()
            - self.coeff_calorie_2)
            * self.weight / self.M_IN_KM
            * self.duration * 60
        )
        return self.spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_1 = 0.035
    coeff_calorie_2 = 0.029
    coeff_calorie_3 = 2
    duration: float
    """вставляется в часах"""
    distance: float
    """вставляется в км"""
    speed: float
    """вставляется в км/ч"""

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight)
        self.height = height

    def get_spent_calories(self) -> float:
        self.spent_calories = (((self.coeff_calorie_1 * self.weight)
                               + (self.get_mean_speed()
                               ** self.coeff_calorie_3
                               // self.height)
                               * self.coeff_calorie_2
                               * self.weight)
                               * self.duration * 60)
        return self.spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    coeff_calorie_1 = 1.1
    coeff_calorie_2 = 2
    duration: float
    """вставляется в часах"""
    distance: float
    """вставляется в км"""
    speed: float
    """вставляется в км/ч"""
    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        self.training_mean_speed = (self.length_pool * self.count_pool
                                    / self.M_IN_KM / self.duration)
        return self.training_mean_speed

    def get_spent_calories(self) -> float:
        self.spent_calories = ((self.get_mean_speed()
                               + self.coeff_calorie_1)
                               * self.coeff_calorie_2 * self.weight)
        return self.spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_dict: dict[str, Training] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return workout_type_dict[workout_type](*data)


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
