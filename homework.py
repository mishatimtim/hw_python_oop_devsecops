from typing import Union


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> None:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: float = 1000
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance: float = self.get_distance()
        mean_speed: float = distance / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(training_type=self.__class__.__name__,
                                   duration=self.duration,
                                   distance=self.get_distance(),
                                   speed=self.get_mean_speed(),
                                   calories=self.get_spent_calories()
                                   )
        return info_message


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_cal_1: float = 18
        coeff_cal_2: float = 20
        mean_speed: float = self.get_mean_speed()
        duration_in_min: float = self.duration * 60
        spent_calories: float = ((coeff_cal_1 * mean_speed - coeff_cal_2)
                                 * self.weight
                                 / self.M_IN_KM * duration_in_min)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight
                         )
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_cal_1: float = 0.035
        coeff_cal_2: float = 0.029
        mean_speed: float = self.get_mean_speed()
        duration_in_min: float = self.duration * 60
        spent_calories: float = ((coeff_cal_1 * self.weight + (mean_speed
                                 ** 2 // self.height)
                                 * coeff_cal_2 * self.weight)
                                 * duration_in_min)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

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
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = (self.length_pool * self.count_pool
                             / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_cal_1: float = 1.1
        coeff_cal_2: float = 2
        spent_calories: float = ((self.get_mean_speed()
                                 + coeff_cal_1) * coeff_cal_2 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_dict: dict = {'RUN': Running,
                               'WLK': SportsWalking,
                               'SWM': Swimming
                               }
    class_object: Union[Running,
                        SportsWalking,
                        Swimming] = workout_type_dict[workout_type](*data)
    return class_object


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
