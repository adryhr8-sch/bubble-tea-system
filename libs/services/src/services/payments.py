from core.interfaces import IPaymentProcessor
from core.exceptions import PaymentRejectedError


class CardPaymentProcessor(IPaymentProcessor):
    def __init__(self, reject_payment: bool = False):
        self._reject_payment = reject_payment

    def process_payment(self, amount: float) -> bool:
        if self._reject_payment:
            raise PaymentRejectedError("Pago con tarjeta rechazado")
        return True


class CashPaymentProcessor(IPaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        return True  # Siempre pendiente / aprobado en efectivo
