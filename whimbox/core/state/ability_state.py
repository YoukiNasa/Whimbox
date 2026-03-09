from enum import Enum, auto

class CombatState(Enum):
    READY = auto()      # 可用
    COOLDOWN = auto()   # 冷却中
    DISABLED = auto()   # 被禁用（沉默/封印）

class MovementState(Enum):
    GROUNDED = auto()
    JUMPING = auto()
    GLIDING = auto()
    DASHING = auto()    # 冲刺中（无敌帧）



class AbilityState:
    def __init__(self):
        pass