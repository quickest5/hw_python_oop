from turtle import distance


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type,
                 duration,
                 distance,
                 speed,
                 calories) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        self.message = f'Тип тренировки: {self.training_type};'
        f'Длительность: {round(self.duration, 3)} ч.;'
        f'Дистанция: {round(self.distance, 3)} км;'
        f'Ср. скорость: {round(self.speed, 3)} км/ч;'
        f'Потрачено ккал: {round(self.calories, 3)}.'
        return self.message


class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.LEN_STEP = 0.65
        self.M_IN_KM = 1000
        pass

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        self.training_distance = self.action * self.LEN_STEP / self.M_IN_KM
        return self.training_distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        self.training_mean_speed = self.get_distance() / self.duration
        return self.training_mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        self.training_info = InfoMessage()
        return self.training_info


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self):
        self.coeff_calorie_1 = 18
        self.coeff_calorie_2 = 20
        self.spent_calories = ((self.coeff_calorie_1
                               * Training.get_mean_speed()
                               - self.coeff_calorie_2)
                               * Training.weight / ((Training.duration) / 60))
        return self.spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
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
        self.coeff_calorie_1 = 0.035
        self.coeff_calorie_2 = 0.029
        self.spent_calories = (((self.coeff_calorie_1 * self.weight)
                                + (Training.get_mean_speed()**2 // self.height)
                                * self.coeff_calorie_2
                                * self.weight) * ((self.duration) / 60))
        return self.spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action,
                         duration,
                         length_pool,
                         count_pool)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.LEN_STEP = 1.38

    def get_mean_speed(self):
        self.training_mean_speed = (self.length_pool * self.count_pool
                                    / self.M_IN_KM / self.duration)
        return self.training_mean_speed

    def get_spent_calories(self) -> float:
        self.coeff_calorie_1 = 1.1
        self.coeff_calorie_2 = 2
        self.spent_calories = (Swimming.get_mean_speed() + self.coeff_calorie_1
                               * self.coeff_calorie_2 * self.weight)
        return self.spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_dict: dict[str, Training] = {'SWM': Swimming, 'RUN': Running,
                                              'WLK': SportsWalking}
    return workout_type_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = Training.show_training_info()
    print(str(info.get_message()))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
