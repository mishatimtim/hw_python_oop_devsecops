class InfoMessage:
    """Информационное сообщение о тренировке."""
    pass


class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 M_IN_KM: int,
                 LEN_STEP: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.M_IN_KM = 1000
        self.LEN_STEP = 0.65

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance: float = self.get_distance(self)
        mean_speed: float = distance / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_cal_1 = 18
        coeff_cal_2 = 20
        mean_speed: float = self.get_mean_speed(self)
        spent_calories: float = (((coeff_cal_1 * mean_speed - coeff_cal_2)
                                 * self.weight)
                                 / (self.M_IN_KM * self.duration))
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 M_IN_KM: int,
                 LEN_STEP: float
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight,
                         M_IN_KM,
                         LEN_STEP
                         )
        self.height = height
        


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    pass


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    pass


def main(training: Training) -> None:
    """Главная функция."""
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
