from .step_0_landingpage import render as step_0
from .step_1_demographics import render as step_1
from .step_2_practical import render as step_2
from .step_3_lifestyle import render as step_3
from .step_4_personality import render as step_4
from .step_5_values import render as step_5
from .step_6_matches import render as step_6

STEP_REGISTRY = {
    0: step_0,
    1: step_1,
    2: step_2,
    3: step_3,
    4: step_4,
    5: step_5,
    6: step_6,
}
