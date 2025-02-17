import multiprocessing
import subprocess

def run_script(poc_arg):
    result = subprocess.run(['python', 'datasets_from_PoC.py', '--poc', poc_arg],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
    # Check the return code
    if result.returncode == 0:
        print(f"Success for poc: {poc_arg}")
    else:
        print(f"Failed for poc: {poc_arg} with return code: {result.returncode}")

pocs = [
    # 'ABY0111',
    ##'ALB0331',
    # 'ALB1101',
    ##'APS0111',
    # 'ARA2201',
    # 'ARG1101',
    # 'ARI1101',
'ARI1102', 'ASB0661', 'ASY0111', 'ATI2201', 'AVI2201', 'BAL0331', 'BDE0111',
'BEN2201', 'BEN2202', 'BLN0331', 'BOB1101', 'BPD1101', 'BPE0331', 'BPE0551',
'BPE2201', 'BPT1101', 'BRB0331', 'BRK0331', 'BRY0661', 'BWK1101', 'CBG0111',
'CLH0111', 'CML0331', 'COL0111', 'COL0661', 'CPK0111', 'CPK0331', 'CST0331',
'CUL0331', 'CUL0661', 'CYD0331', 'CYD2201', 'DOB0331', 'DOB0661', 'DVK0111',
'EDG0331', 'EDN0331', 'FHL0331', 'FKN0331', 'GFD0331', 'GLN0331', 'GLN0332',
'GOR0331', 'GYM0661', 'GYT0331', 'HAM0111', 'HAM0331', 'HAM0551', 'HAM2201',
'HAY0111', 'HAY0331', 'HAY1101', 'HAY2201', 'HEN0331', 'HEN2201', 'HEP0331',
'HIN0331', 'HKK0661', 'HLY0331', 'HLY2201', 'HOB1101', 'HOR0331', 'HOR0661',
'HRP2201', 'HTI0331', 'HTI1101', 'HUI0331', 'HWA0331', 'HWA0332', 'HWA1101',
'HWA1102', 'HWB0331', 'HWB1101', 'HWB2201', 'INV0331', 'INV2201', 'INV2202',
'ISL0331', 'ISL0661', 'ISL2201', 'JRD1101', 'KAI0111', 'KAW0111', 'KAW0112',
'KAW1101', 'KAW2201', 'KBY0661', 'KBY0662', 'KIK0111', 'KIK2201', 'KIN0111',
'KIN0112', 'KIN0113', 'KIN0331', 'KMO0331', 'KOE1101', 'KPA1101', 'KPO1101',
'KPU0661', 'KUM0661', 'KWA0111', 'LFD1101', 'LFD1102', 'LTN0331', 'LTN2201',
'MAN2201', 'MAT1101', 'MCH0111', 'MDN1101', 'MDN2201', 'MGM0331', 'MHO0331',
# 'MKE1101', 'MLG0111', 'MLG0331', 'MNG0331', 'MNG1101', 'MNI0111', 'MPE1101',
# 'MST0331', 'MTI2201', 'MTM0331', 'MTN0331', 'MTO0331', 'MTR0331', 'NAP2201',
# 'NAP2202', 'NMA0331', 'NPK0331', 'NSY0331', 'NWD0661', 'OAM0331', 'OHA2201',
# 'OHB2201', 'OHC2201', 'OHK2201', 'OKI2201', 'OKN0111', 'ONG0331', 'OPK0331',
# 'ORO1101', 'ORO1102', 'OTA0221', 'OTA2201', 'OTI0111', 'OWH0111', 'PAK0331',
# 'PAO1101', 'PEN0221', 'PEN0251', 'PEN0331', 'PEN1101', 'PNI0331', 'PPI2201',
# 'PRM0331', 'RDF0331', 'RDF2201', 'RFN1101', 'RFN1102', 'ROS0221', 'ROS1101',
# 'ROT0111', 'ROT0331', 'ROT1101', 'ROX1101', 'ROX2201', 'RPO2201', 'SBK0661',
# 'SDN0331', 'SFD0331', 'SFD2201', 'STK0331', 'STK0661', 'STK2201', 'STU0111',
# 'SVL0331', 'SWN0251', 'SWN2201', 'TAB2201', 'TAK0331', 'TGA0111', 'TGA0331',
# 'THI2201', 'TIM0111', 'TKA0111', 'TKA0331', 'TKB2201', 'TKR0331', 'TKU0331',
# 'TKU2201', 'TMI0331', 'TMK0331', 'TMN0551', 'TMU0111', 'TMU1101', 'TNG0111',
# 'TNG0551', 'TRK0111', 'TRK2201', 'TUI1101', 'TWC2201', 'TWH0331', 'TWI2201',
# 'TWZ0331', 'UHT0331', 'WAI0111', 'WAI0501', 'WDV0111', 'WDV1101', 'WEL0331',
# 'WGN0331', 'WHI0111', 'WHI2201', 'WHU0331', 'WIL0331', 'WIR0331', 'WKM2201',
# 'WKO0331', 'WPA2201', 'WPR0331', 'WPR0661', 'WPW0331', 'WRD0331', 'WRK0331',
# 'WRK2201', 'WTK0111', 'WTK0331', 'WTK2201', 'WTU0331', 'WVY0111', 'WVY1101',
# 'WWD1102', 'WWD1103'
]
if __name__ == "__main__":



    # Create a list to hold the process objects
    processes = []

    for poc in pocs:
        # Create a Process object
        process = multiprocessing.Process(target=run_script, args=(poc,))
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()
