
from dataclasses import dataclass, asdict

min_in_hour = 60


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
    text = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.text.format(**asdict(self))


class Training:
    """Базовый класс тренировки.
    duration вставляется в часах"""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000

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
        raise NotImplementedError(f'{"Обязательно нужно "}'
                                  f"переопределить при наследовании")

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
    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self):
        return ((
            self.COEFF_CALORIE_1
            * self.get_mean_speed()
            - self.COEFF_CALORIE_2)
            * self.weight / self.M_IN_KM
            * self.duration * min_in_hour
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба.
    duration вставляется в часах
    distance вставляется в км
    speed вставляется в км/ч"""
    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029
    COEFF_CALORIE_3: float = 2

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
            * self.duration * min_in_hour
        )


class Swimming(Training):
    """Тренировка: плавание.
    вставляется в часах
    distance вставляется в км
    speed вставляется в км/ч"""
    LEN_STEP: float = 1.38
    COEFF_CALORIE_1: float = 1.1
    COEFF_CALORIE_2: float = 2

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
        raise KeyError("Твое сообщение об ошибке")


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
