"""Konveyör sıralı çalışma mantığının donanımsız Python simülasyonu."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ConveyorState(str, Enum):
    """Konveyörün kullanıcıya gösterilen durumları."""

    IDLE = "beklemede"
    RUNNING = "çalışıyor"
    BATCH_COMPLETE = "parti_tamamlandı"


@dataclass
class Conveyor:
    """Başlat/durdur ve yükselen kenar sayımı yapan küçük konveyör modeli."""

    batch_target: int = 10
    product_count: int = 0
    state: ConveyorState = ConveyorState.IDLE
    _sensor_was_active: bool = False

    def __post_init__(self) -> None:
        if self.batch_target <= 0:
            raise ValueError("Parti hedefi sıfırdan büyük olmalıdır.")

    @property
    def motor_on(self) -> bool:
        """Motor komutunu mevcut durumdan üret."""

        return self.state is ConveyorState.RUNNING

    def start(self) -> bool:
        """Parti tamamlanmamışsa konveyörü çalıştır."""

        if self.state is ConveyorState.BATCH_COMPLETE:
            return False
        self.state = ConveyorState.RUNNING
        return True

    def stop(self) -> None:
        """Konveyörü durdur; sayaç değerini koru."""

        if self.state is ConveyorState.RUNNING:
            self.state = ConveyorState.IDLE

    def reset(self) -> bool:
        """Yalnızca motor duruyken sayacı ve parti durumunu sıfırla."""

        if self.motor_on:
            return False
        self.product_count = 0
        self.state = ConveyorState.IDLE
        self._sensor_was_active = False
        return True

    def set_sensor(self, active: bool) -> bool:
        """Sensörün yükselen kenarında bir ürün say; sayıldıysa True döndür."""

        rising_edge = active and not self._sensor_was_active
        self._sensor_was_active = active

        if not rising_edge or not self.motor_on:
            return False

        self.product_count += 1
        if self.product_count >= self.batch_target:
            self.state = ConveyorState.BATCH_COMPLETE
        return True


def run_demo() -> None:
    """Beş ürünlük tekrarlanabilir bir konsol demosu çalıştır."""

    conveyor = Conveyor(batch_target=5)
    conveyor.start()
    print("Konveyör başlatıldı.")

    while conveyor.motor_on:
        conveyor.set_sensor(False)
        if conveyor.set_sensor(True):
            print(f"Ürün algılandı: {conveyor.product_count}/{conveyor.batch_target}")

    print("Parti tamamlandı, konveyör durdu.")


if __name__ == "__main__":
    run_demo()
