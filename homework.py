from typing import Dict
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> None:
        info_about_training = asdict(self)
        return (f'Тип тренировки: {info_about_training["training_type"]}; '
                f'Длительность: {info_about_training["duration"]:.3f} ч.; '
                f'Дистанция: {info_about_training["distance"]:.3f} км; '
                f'Ср. скорость: {info_about_training["speed"]:.3f} км/ч; '
                f'Потрачено ккал: {info_about_training["calories"]:.3f}.'
                )


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: float = 1000
    LEN_STEP: float = 0.65
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance: float = self.get_distance()
        mean_speed: float = distance / self.duration
        return mean_speed

    def get_spent_calories(self) -> NotImplementedError:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(training_type=type(self).__name__,
                                   duration=self.duration,
                                   distance=self.get_distance(),
                                   speed=self.get_mean_speed(),
                                   calories=self.get_spent_calories(),
                                   )
        return info_message


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_cal_1: float = 18
        coeff_cal_2: float = 20
        mean_speed: float = self.get_mean_speed()
        duration_in_min: float = self.duration * self.MIN_IN_HOUR
        spent_calories: float = ((coeff_cal_1 * mean_speed - coeff_cal_2)
                                 * self.weight
                                 / self.M_IN_KM
                                 * duration_in_min
                                 )
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WEIGHT_MULTIPLIER_1: float = 0.035
    WEIGHT_MULTIPLIER_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight,
                         )
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mean_speed: float = self.get_mean_speed()
        duration_in_min: float = self.duration * self.MIN_IN_HOUR
        spent_calories: float = ((self.WEIGHT_MULTIPLIER_1 * self.weight
                                 + (mean_speed ** 2 // self.height)
                                 * self.WEIGHT_MULTIPLIER_2 * self.weight)
                                 * duration_in_min
                                 )
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CAL_SHIFT: float = 1.1
    CAL_MULTIPLIER: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight,
                         )
        self.length_pool: float = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = (self.length_pool * self.count_pool
                             / self.M_IN_KM / self.duration
                             )
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories: float = ((self.get_mean_speed()
                                 + self.CAL_SHIFT)
                                 * self.CAL_MULTIPLIER * self.weight
                                 )
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_dict: Dict[str, Training] = {'RUN': Running,
                                              'WLK': SportsWalking,
                                              'SWM': Swimming,
                                              }
    class_object: Training = workout_type_dict[workout_type](*data)
    return class_object


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    """Точка входа в программу."""
    packages: list = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
