# Copyright (C) 2024 Robert Wiese - All Rights Reserved.
"""Bind Skeleton module creation positions."""

from enum import Enum
import logging
import os

from Core import core_paths as cpath

from .ue_skeleton_names import EpicBasicSkeleton

# Main paths
MAIN_PATHS = cpath.core_paths()

LOG = logging.getLogger(os.path.basename(__file__))


class BindModulePositions(Enum):
    """All Basic Proxy Epic skeleton module positions and names."""

    SPINE = [
        {
            "name": f"{EpicBasicSkeleton.PELVIS.value}_BPX",
            "position": [1.643580311187394e-21, 98.69322204589844, 2.379462480545044],
        },
        {
            "name": f"{EpicBasicSkeleton.SPINE_01.value}_BPX",
            "position": [
                -1.7832174288568996e-16,
                101.16019024789955,
                2.224139488180419,
            ],
        },
        {
            "name": f"{EpicBasicSkeleton.SPINE_02.value}_BPX",
            "position": [
                4.9741612745095165e-14,
                106.00695481004972,
                3.4006447420858263,
            ],
        },
        {
            "name": f"{EpicBasicSkeleton.SPINE_03.value}_BPX",
            "position": [
                1.4642356796334186e-13,
                113.57889298970535,
                4.3061018464324095,
            ],
        },
        {
            "name": f"{EpicBasicSkeleton.SPINE_04.value}_BPX",
            "position": [3.282475457360187e-13, 122.41347909854565, 3.765427228372718],
        },
        {
            "name": f"{EpicBasicSkeleton.SPINE_05.value}_BPX",
            "position": [
                1.3061600671016637e-12,
                139.53107210402257,
                0.13299659558299748,
            ],
        },
        {
            "name": f"{EpicBasicSkeleton.NECK_01.value}_BPX",
            "position": [
                -3.2471021361400834e-07,
                151.17530081006927,
                -2.3929106340808186,
            ],
        },
        {
            "name": f"{EpicBasicSkeleton.NECK_02.value}_BPX",
            "position": [
                -4.690114967465231e-07,
                156.87662845153253,
                -1.087634786711889,
            ],
        },
        {
            "name": f"{EpicBasicSkeleton.HEAD.value}_BPX",
            "position": [-6.117792488000871e-07, 162.5031186225401, 0.1382347057676141],
        },
        {
            "name": f"{EpicBasicSkeleton.HEAD.value}_end_BPX",
            "position": [-6.117792488000871e-07, 170, 0.1382347057676141],
        },
    ]

    LEG_R = [
        {
            "name": f"{EpicBasicSkeleton.THIGH_R.value}_BPX",
            "position": [-11.154600143432617, 95.47183800799418, 2.650410794338726],
        },
        {
            "name": f"{EpicBasicSkeleton.CALF_R.value}_BPX",
            "position": [-13.06266341081274, 49.769644354111605, 1.6972013187687498],
        },
        {
            "name": f"{EpicBasicSkeleton.FOOT_R.value}_BPX",
            "position": [-14.684454703037137, 8.128632002731706, 0.04133908448391477],
        },
        {
            "name": f"{EpicBasicSkeleton.BALL_R.value}_BPX",
            "position": [-16.628285385457833, 1.1650361601554513, 13.31601367473364],
        },
    ]
    LEG_L = [
        {
            "name": f"{EpicBasicSkeleton.THIGH_L.value}_BPX",
            "position": [11.154600143432617, 95.47183800799418, 2.650410794338726],
        },
        {
            "name": f"{EpicBasicSkeleton.CALF_L.value}_BPX",
            "position": [13.06266341081274, 49.769644354111605, 1.6972013187687498],
        },
        {
            "name": f"{EpicBasicSkeleton.FOOT_L.value}_BPX",
            "position": [14.684454703037137, 8.128632002731706, 0.04133908448391477],
        },
        {
            "name": f"{EpicBasicSkeleton.BALL_L.value}_BPX",
            "position": [16.628285385457833, 1.1650361601554513, 13.31601367473364],
        },
    ]
    ARM_R = [
        {
            "name": f"{EpicBasicSkeleton.CLAVICLE_R.value}_BPX",
            "position": [-0.9313597065185146, 145.01594928690463, -2.085085825332809],
        },
        {
            "name": f"{EpicBasicSkeleton.UPPERARM_R.value}_BPX",
            "position": [-16.055299298278133, 142.83668643778142, -2.5078371108592425],
        },
        {
            "name": f"{EpicBasicSkeleton.LOWERARM_R.value}_BPX",
            "position": [-32.39559255192758, 121.24203352583643, -1.7643836358888279],
        },
        {
            "name": f"{EpicBasicSkeleton.HAND_R.value}_BPX",
            "position": [-45.47026773109977, 105.44405027532662, 14.373582317269056],
        },
        {
            "name": f"{EpicBasicSkeleton.HAND_R.value}_end_BPX",
            "position": [-53.99953079223633, 95.1382369995117, 24.90118408203125],
        },
    ]
    ARM_L = [
        {
            "name": f"{EpicBasicSkeleton.CLAVICLE_L.value}_BPX",
            "position": [0.9313597065185146, 145.01594928690463, -2.085085825332809],
        },
        {
            "name": f"{EpicBasicSkeleton.UPPERARM_L.value}_BPX",
            "position": [16.055299298278133, 142.83668643778142, -2.5078371108592425],
        },
        {
            "name": f"{EpicBasicSkeleton.LOWERARM_L.value}_BPX",
            "position": [32.39559255192758, 121.24203352583643, -1.7643836358888279],
        },
        {
            "name": f"{EpicBasicSkeleton.HAND_L.value}_BPX",
            "position": [45.47026773109977, 105.44405027532662, 14.373582317269056],
        },
        {
            "name": f"{EpicBasicSkeleton.HAND_L.value}_end_BPX",
            "position": [53.99953079223633, 95.1382369995117, 24.90118408203125],
        },
    ]
    THUMB_R = [
        {
            "name": f"{EpicBasicSkeleton.THUMB_01_R.value}_BPX",
            "position": [-43.83117490166582, 103.68327017152465, 17.22749930255447],
        },
        {
            "name": f"{EpicBasicSkeleton.THUMB_02_R.value}_BPX",
            "position": [-42.76928054297963, 101.00742689008851, 20.855958254577008],
        },
        {
            "name": f"{EpicBasicSkeleton.THUMB_03_R.value}_BPX",
            "position": [-42.81722991346148, 98.867452998824, 22.518941720709375],
        },
        {
            "name": f"{EpicBasicSkeleton.THUMB_03_R.value}_end_BPX",
            "position": [-42.88468551635743, 95.85678863525392, 24.85854148864744],
        },
    ]
    THUMB_L = [
        {
            "name": f"{EpicBasicSkeleton.THUMB_01_L.value}_BPX",
            "position": [43.83117490166582, 103.68327017152465, 17.22749930255447],
        },
        {
            "name": f"{EpicBasicSkeleton.THUMB_02_L.value}_BPX",
            "position": [42.76928054297963, 101.00742689008851, 20.855958254577008],
        },
        {
            "name": f"{EpicBasicSkeleton.THUMB_03_L.value}_BPX",
            "position": [42.81722991346148, 98.867452998824, 22.518941720709375],
        },
        {
            "name": f"{EpicBasicSkeleton.THUMB_03_L.value}_end_BPX",
            "position": [42.88468551635743, 95.85678863525392, 24.85854148864744],
        },
    ]
    INDEX_R = [
        {
            "name": f"{EpicBasicSkeleton.INDEX_METACARPAL_R.value}_BPX",
            "position": [-45.527577938198505, 103.48450324973776, 17.880841995899154],
        },
        {
            "name": f"{EpicBasicSkeleton.INDEX_01_R.value}_BPX",
            "position": [-47.47545090255724, 99.93535958728009, 21.419272800380487],
        },
        {
            "name": f"{EpicBasicSkeleton.INDEX_02_R.value}_BPX",
            "position": [-48.54431229312727, 95.94226516851205, 23.355205451665665],
        },
        {
            "name": f"{EpicBasicSkeleton.INDEX_03_R.value}_BPX",
            "position": [-48.73853787968011, 93.58926210801593, 24.135071301023494],
        },
        {
            "name": f"{EpicBasicSkeleton.INDEX_03_R.value}_end_BPX",
            "position": [-49.050613403320305, 90.95372009277347, 24.895338058471676],
        },
    ]
    INDEX_L = [
        {
            "name": f"{EpicBasicSkeleton.INDEX_METACARPAL_L.value}_BPX",
            "position": [45.527577938198505, 103.48450324973776, 17.880841995899154],
        },
        {
            "name": f"{EpicBasicSkeleton.INDEX_01_L.value}_BPX",
            "position": [47.47545090255724, 99.93535958728009, 21.419272800380487],
        },
        {
            "name": f"{EpicBasicSkeleton.INDEX_02_L.value}_BPX",
            "position": [48.54431229312727, 95.94226516851205, 23.355205451665665],
        },
        {
            "name": f"{EpicBasicSkeleton.INDEX_03_L.value}_BPX",
            "position": [48.73853787968011, 93.58926210801593, 24.135071301023494],
        },
        {
            "name": f"{EpicBasicSkeleton.INDEX_03_L.value}_end_BPX",
            "position": [49.050613403320305, 90.95372009277347, 24.895338058471676],
        },
    ]
    MIDDLE_R = [
        {
            "name": f"{EpicBasicSkeleton.MIDDLE_METACARPAL_R.value}_BPX",
            "position": [-46.46967530051343, 103.30456568519665, 16.441092857060816],
        },
        {
            "name": f"{EpicBasicSkeleton.MIDDLE_01_R.value}_BPX",
            "position": [-49.12984023576821, 99.59544277817325, 19.616878008312],
        },
        {
            "name": f"{EpicBasicSkeleton.MIDDLE_02_R.value}_BPX",
            "position": [-50.08279744962752, 95.12958019915996, 21.44747971472549],
        },
        {
            "name": f"{EpicBasicSkeleton.MIDDLE_03_R.value}_BPX",
            "position": [-49.782683232290076, 92.32423294357424, 22.127085196863387],
        },
        {
            "name": f"{EpicBasicSkeleton.MIDDLE_03_R.value}_end_BPX",
            "position": [-49.045574188232436, 89.67755126953125, 22.542404174804684],
        },
    ]
    MIDDLE_L = [
        {
            "name": f"{EpicBasicSkeleton.MIDDLE_METACARPAL_L.value}_BPX",
            "position": [46.46967530051343, 103.30456568519665, 16.441092857060816],
        },
        {
            "name": f"{EpicBasicSkeleton.MIDDLE_01_L.value}_BPX",
            "position": [49.12984023576821, 99.59544277817325, 19.616878008312],
        },
        {
            "name": f"{EpicBasicSkeleton.MIDDLE_02_L.value}_BPX",
            "position": [50.08279744962752, 95.12958019915996, 21.44747971472549],
        },
        {
            "name": f"{EpicBasicSkeleton.MIDDLE_03_L.value}_BPX",
            "position": [49.782683232290076, 92.32423294357424, 22.127085196863387],
        },
        {
            "name": f"{EpicBasicSkeleton.MIDDLE_03_L.value}_end_BPX",
            "position": [49.045574188232436, 89.67755126953125, 22.542404174804684],
        },
    ]
    RING_R = [
        {
            "name": f"{EpicBasicSkeleton.RING_METACARPAL_R.value}_BPX",
            "position": [-47.01426575079376, 102.86414404160303, 15.500264747364422],
        },
        {
            "name": f"{EpicBasicSkeleton.RING_01_R.value}_BPX",
            "position": [-49.63500671307859, 99.06614491772264, 17.40672428725838],
        },
        {
            "name": f"{EpicBasicSkeleton.RING_02_R.value}_BPX",
            "position": [-50.701640316925904, 95.22064848655776, 18.87258736219148],
        },
        {
            "name": f"{EpicBasicSkeleton.RING_03_R.value}_BPX",
            "position": [-50.09748546210722, 92.12805940608125, 19.60402556866898],
        },
        {
            "name": f"{EpicBasicSkeleton.RING_03_R.value}_end_BPX",
            "position": [-49.31956100463867, 89.83547973632812, 19.916154861450188],
        },
    ]
    RING_L = [
        {
            "name": f"{EpicBasicSkeleton.RING_METACARPAL_L.value}_BPX",
            "position": [47.01426575079376, 102.86414404160303, 15.500264747364422],
        },
        {
            "name": f"{EpicBasicSkeleton.RING_01_L.value}_BPX",
            "position": [49.63500671307859, 99.06614491772264, 17.40672428725838],
        },
        {
            "name": f"{EpicBasicSkeleton.RING_02_L.value}_BPX",
            "position": [50.701640316925904, 95.22064848655776, 18.87258736219148],
        },
        {
            "name": f"{EpicBasicSkeleton.RING_03_L.value}_BPX",
            "position": [50.09748546210722, 92.12805940608125, 19.60402556866898],
        },
        {
            "name": f"{EpicBasicSkeleton.RING_03_L.value}_end_BPX",
            "position": [49.31956100463867, 89.83547973632812, 19.916154861450188],
        },
    ]
    PINKY_R = [
        {
            "name": f"{EpicBasicSkeleton.PINKY_METACARPAL_R.value}_BPX",
            "position": [-47.45343239879253, 102.49076981423546, 14.507948775645323],
        },
        {
            "name": f"{EpicBasicSkeleton.PINKY_01_R.value}_BPX",
            "position": [-49.48743400299146, 98.33252849809222, 15.419480774199565],
        },
        {
            "name": f"{EpicBasicSkeleton.PINKY_02_R.value}_BPX",
            "position": [-50.175729150139404, 95.5940193930298, 16.0503434475637],
        },
        {
            "name": f"{EpicBasicSkeleton.PINKY_03_R.value}_BPX",
            "position": [-49.97290693112249, 93.85143234976987, 16.41338087175558],
        },
        {
            "name": f"{EpicBasicSkeleton.PINKY_03_R.value}_end_BPX",
            "position": [-49.29690551757812, 91.43212890625, 16.858219146728512],
        },
    ]
    PINKY_L = [
        {
            "name": f"{EpicBasicSkeleton.PINKY_METACARPAL_L.value}_BPX",
            "position": [47.45343239879253, 102.49076981423546, 14.507948775645323],
        },
        {
            "name": f"{EpicBasicSkeleton.PINKY_01_L.value}_BPX",
            "position": [49.48743400299146, 98.33252849809222, 15.419480774199565],
        },
        {
            "name": f"{EpicBasicSkeleton.PINKY_02_L.value}_BPX",
            "position": [50.175729150139404, 95.5940193930298, 16.0503434475637],
        },
        {
            "name": f"{EpicBasicSkeleton.PINKY_03_L.value}_BPX",
            "position": [49.97290693112249, 93.85143234976987, 16.41338087175558],
        },
        {
            "name": f"{EpicBasicSkeleton.PINKY_03_L.value}_end_BPX",
            "position": [49.29690551757812, 91.43212890625, 16.858219146728512],
        },
    ]


class BindCorrectivePositions(Enum):
    CLAVICLE_OUT_R = {
        "name": "clavicle_out_r",
        "parent": EpicBasicSkeleton.CLAVICLE_R.value,
        "position": [-12.652524893440583, 148.8910774557812, -2.2247869058227225],
    }
    CLAVICLE_SCAP_R = {
        "name": "clavicle_scap_r",
        "parent": EpicBasicSkeleton.CLAVICLE_R.value,
        "position": [-9.444724869281355, 141.38060424412575, -8.430450773618025],
    }
    UPPERARM_TWIST_01_R = {
        "name": "upperarm_twist_01_r",
        "parent": EpicBasicSkeleton.UPPERARM_R.value,
        "position": [-21.502062473604507, 135.6386446695165, -2.260020644620558],
    }
    UPPERARM_TWISTCOR_01_R = {
        "name": "upperarm_twistCor_01_r",
        "parent": "upperarm_twist_01_r",
        "position": [-21.50206247360446, 135.63864466951654, -2.2600206446205733],
    }
    UPPERARM_TRICEP_R = {
        "name": "upperarm_tricep_r",
        "parent": "upperarm_twist_02_r",
        "position": [-27.034254959727374, 127.98379345064653, -6.78579361190992],
    }
    UPPERARM_BICEP_R = {
        "name": "upperarm_bicep_r",
        "parent": "upperarm_twist_02_r",
        "position": [-27.285138844359395, 128.03778354924677, 1.2347989381797286],
    }
    UPPERARM_TWISTCOR_02_R = {
        "name": "upperarm_twistCor_02_r",
        "parent": "upperarm_twist_02_r",
        "position": [-26.948825648930892, 128.4406029012515, -2.0122041783818845],
    }
    UPPERARM_CORRECTIVEROOT_R = {
        "name": "upperarm_correctiveRoot_r",
        "parent": EpicBasicSkeleton.UPPERARM_R.value,
        "position": [-16.05529929827806, 142.83668643778128, -2.507837110859236],
    }
    UPPERARM_BCK_R = {
        "name": "upperarm_bck_r",
        "parent": "upperarm_correctiveRoot_r",
        "position": [-17.499778679822526, 141.5401132249059, -8.8197639147259],
    }
    UPPERARM_IN_R = {
        "name": "upperarm_in_r",
        "parent": "upperarm_correctiveRoot_r",
        "position": [-16.15344586710023, 135.94165061030606, -0.7541294666258793],
    }
    UPPERARM_FWD_R = {
        "name": "upperarm_fwd_r",
        "parent": "upperarm_correctiveRoot_r",
        "position": [-17.959999544146314, 140.28197778460574, 4.123558338857031],
    }
    UPPERARM_OUT_R = {
        "name": "upperarm_out_r",
        "parent": "upperarm_correctiveRoot_r",
        "position": [-20.7332545587913, 146.35323319942287, -3.1251424288992578],
    }
    LOWERARM_TWIST_02_R = {
        "name": "lowerarm_twist_02_r",
        "parent": EpicBasicSkeleton.LOWERARM_R.value,
        "position": [-36.75357331868152, 115.97626391342654, 3.6150021883514682],
    }
    LOWERARM_TWIST_01_R = {
        "name": "lowerarm_twist_01_r",
        "parent": EpicBasicSkeleton.LOWERARM_R.value,
        "position": [-41.11185064855323, 110.71020615563364, 8.99438893437988],
    }
    LOWERARM_CORRECTIVEROOT_R = {
        "name": "lowerarm_correctiveRoot_r",
        "parent": EpicBasicSkeleton.LOWERARM_R.value,
        "position": [-32.39556771536613, 121.24254633563666, -1.7643883244187488],
    }
    LOWERARM_OUT_R = {
        "name": "lowerarm_out_r",
        "parent": "lowerarm_correctiveRoot_r",
        "position": [-34.99942815972259, 121.50354620521462, -2.564228232530176],
    }
    LOWERARM_IN_R = {
        "name": "lowerarm_in_r",
        "parent": "lowerarm_correctiveRoot_r",
        "position": [-31.367901100540355, 118.63735811485074, -0.7733423681440733],
    }
    LOWERARM_FWD_R = {
        "name": "lowerarm_fwd_r",
        "parent": "lowerarm_correctiveRoot_r",
        "position": [-32.809509150232834, 121.97136510998877, 1.0244628371922346],
    }
    LOWERARM_BCK_R = {
        "name": "lowerarm_bck_r",
        "parent": "lowerarm_correctiveRoot_r",
        "position": [-33.733930483943254, 117.74077885869428, -3.5180762915464685],
    }
    WRIST_INNER_R = {
        "name": "wrist_inner_r",
        "parent": EpicBasicSkeleton.HAND_R.value,
        "position": [-43.9920357005851, 104.66063440151193, 14.006728112725293],
    }
    WRIST_OUTER_R = {
        "name": "wrist_outer_r",
        "parent": EpicBasicSkeleton.HAND_R.value,
        "position": [-46.52817834252647, 106.61027548932765, 15.056658687067522],
    }
    WEAPON_R = {
        "name": "weapon_r",
        "parent": EpicBasicSkeleton.HAND_R.value,
        "position": [-45.02346061304126, 103.61086485084313, 14.176288422974851],
    }
    CLAVICLE_PEC_R = {
        "name": "clavicle_pec_r",
        "parent": EpicBasicSkeleton.SPINE_05.value,
        "position": [-10.180403549674686, 133.4375415428856, 11.84474512683763],
    }
    SPINE_04_LATISSIMUS_R = {
        "name": "spine_04_latissimus_r",
        "parent": EpicBasicSkeleton.SPINE_05.value,
        "position": [-12.816333877211873, 130.64292582497197, -1.270466524037893],
    }
    THIGH_TWIST_01_R = {
        "name": "thigh_twist_01_r",
        "parent": "thigh_r",
        "position": [-11.790621259074346, 80.23777282160837, 2.332674289235978],
    }
    THIGH_TWISTCOR_01_R = {
        "name": "thigh_twistCor_01_r",
        "parent": "thigh_twist_01_r",
        "position": [-11.790621259074348, 80.23777282160836, 2.3326742892359746],
    }
    THIGH_TWIST_02_R = {
        "name": "thigh_twist_02_r",
        "parent": "thigh_r",
        "position": [-12.42664237471609, 65.00370763522257, 2.0149377841332257],
    }
    THIGH_TWISTCOR_02_R = {
        "name": "thigh_twistCor_02_r",
        "parent": "thigh_twist_02_r",
        "position": [-12.426642374716087, 65.00370763522263, 2.014937784133224],
    }
