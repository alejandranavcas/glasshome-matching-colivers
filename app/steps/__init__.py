from .step_0_landingpage import render as step_0
from .step_01_authentification import render as step_01
from .step_1_demographics import render as step_1
from .step_2_practical import render as step_2
from .step_3_lifestyle import render as step_3
from .step_4_personality import render as step_4
from .step_5_values import render as step_5
from .step_6_matches import render as step_6

STEP_REGISTRY = {
    0: step_0,
    1: step_01,
    2: step_1,
    3: step_2,
    4: step_3,
    5: step_4,
    6: step_5,
    7: step_6,
}
