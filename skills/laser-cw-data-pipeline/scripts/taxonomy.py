# -*- coding: utf-8 -*-
"""session-v1 新采集树枚举；不用于 snapshot-v2 指标编号。"""

CAMPAIGNS = ("鉴定件", "加强件")
GROUPS = ("SZSD", "YCQD")

DEVICES = {
    "SZSD": ["AD2208", "DA9726", "TLV2548", "GTH_RF4", "FREQ_COUNTER"],
    "YCQD": ["AD9245", "DA766", "AD677", "AD128", "ADG526_AD677"],
}

INDICATORS = {
    "AD2208": ["01_DynamicRange", "02_Scale", "03_Bandwidth", "04_Sfdr", "05_InlDnl",
               "06_NoiseIla", "07_NoisePico", "08_Isolation", "09_PhaseBandwidth", "10_ClockSource"],
    "DA9726": ["01_OutputVoltage", "02_Scale", "03_Noise", "04_Isolation", "05_PhaseNoise"],
    "AD9245": ["01_DynamicRange", "02_Scale", "03_Bandwidth", "04_Sfdr", "05_InlDnl",
               "06_Noise", "07_Isolation"],
    "DA766": ["01_OutputVoltage", "02_Scale", "03_Noise", "04_Isolation"],
    "AD677": ["01_FrequencyResponse", "02_Scale", "03_Noise"],
    "AD128": ["01_Bandwidth", "02_DynamicRange", "03_Noise"],
    "TLV2548": ["01_TelemetryCodes"],
    "GTH_RF4": ["01_OutputPower", "02_FreqStability"],
    "FREQ_COUNTER": ["01_ChannelCrosstalk"],
    "ADG526_AD677": ["01_TelemetryCodes"],
}

INTERFACES = {
    "AD2208": ["ADC1_JG15", "ADC2_JG17", "ADC3_JG19", "ADC5_JG22", "ADC6_JG24"],
    "DA9726": ["DAC1_JG18", "DAC2_JG20", "DAC3_JG21", "DAC4_JG23", "DAC5_JG25"],
    "AD9245": ["X1G", "X2G", "X3G", "X4G"],
    "DA766": ["X7", "X9", "X11-5", "X11-6", "X11-7", "X12G", "X77-7", "X77-8"],
    "AD677": ["X3", "X13"],
    "AD128": ["X10", "X11-1", "X11-2", "X11-3", "X11-4"],
    "TLV2548": ["SIG_IN%d" % i for i in range(1, 9)],
    "GTH_RF4": ["GTH_JG10", "RF_JG1", "RF_JG4", "RF_JG5", "RF_JG8"],
    "FREQ_COUNTER": ["CH1", "CH2", "CH3", "CH4"],
    "ADG526_AD677": ["ADDR_%02X" % i for i in range(16)],
}

# 新树内出现即报错的拼写黑名单（存量错误名）
BLACKLIST = ("ila_nosie", "nosie", "200290919", "adress")

REWORK_BOUNDARY = "2026-09-19"   # 历史批次参考；禁止仅凭日期推断实际改焊状态

INDICATOR_REMARKS = {
    "06_NoiseIla": "10~25 MHz ILA 高频噪声（报告'输入等效噪声'节）",
    "07_NoisePico": "250 kS/s PICO 1 Hz 总链路噪声（报告'输入等效噪声'节）",
    "09_PhaseBandwidth": "含 2208-9726/766 链路传输延迟与相移带宽",
    "10_ClockSource": "原'ADC&DAC时钟源稳定度测试'归并（归属待确认）",
    "01_TelemetryCodes": "遥测静态码值（TLV2548 为 SIG_IN1~8；ADG526+AD677 为 ADDR_00~0F 遍历）",
    "02_FreqStability": "秒稳/万秒稳（53100A）",
}
