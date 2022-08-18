
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке.
    duration вставляется в часах
    distance вставляется в км
    speed вставляется в км/ч"""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки.
    duration вставляется в часах"""
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError()

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
    """Тренировка: бег.
    duration вставляется в часах
    distance вставляется в км
    speed вставляется в км/ч"""
    COEFF_CALORIE_1 = 18
    COEFF_CALORIE_2 = 20
    duration: float
    distance: float
    speed: float

    def get_spent_calories(self):
        return ((
            self.COEFF_CALORIE_1
            * self.get_mean_speed()
            - self.COEFF_CALORIE_2)
            * self.weight / self.M_IN_KM
            * self.duration * 60
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба.
    вставляется в часах
    distance вставляется в км
    speed вставляется в км/ч"""
    COEFF_CALORIE_1 = 0.035
    COEFF_CALORIE_2 = 0.029
    COEFF_CALORIE_3 = 2
    duration: float
    """вставляется в часах"""
    distance: float
    """вставляется в км"""
    speed: float
    """вставляется в км/ч"""

    def __init__(
            self, action: int,
            duration: float,
            weight: float,
            height: float
    ) -> None:
        super().__init__(
            action,
            duration,
            weight
        )
        self.height = height

    def get_spent_calories(self) -> float:
        return (((
            self.COEFF_CALORIE_1 * self.weight)
            + (self.get_mean_speed()
                ** self.COEFF_CALORIE_3
                // self.height)
            * self.COEFF_CALORIE_2
            * self.weight)
            * self.duration * 60
        )


class Swimming(Training):
    """Тренировка: плавание.
    вставляется в часах
    distance вставляется в км
    speed вставляется в км/ч"""
    LEN_STEP = 1.38
    COEFF_CALORIE_1 = 1.1
    COEFF_CALORIE_2 = 2
    duration: float
    distance: float
    speed: float

    def __init__(
            self, action: int,
            duration: float,
            weight: float,
            length_pool: int,
            count_pool: int
    ) -> None:
        super().__init__(
            action,
            duration,
            weight
        )
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((
            self.get_mean_speed()
            + self.COEFF_CALORIE_1)
            * self.COEFF_CALORIE_2 * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_dict: dict[str, Training] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    try:
        return workout_type_dict[workout_type](*data)
    except KeyError:
        print("Не вышло в районе read_package")


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
