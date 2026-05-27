# GSSAPI stub for impacket compatibility
# This is a minimal implementation for basic SMB operations

GSS_C_NO_FLAGS = 0
GSS_C_REPLAY_FLAG = 1
GSS_C_SEQUENCE_FLAG = 2
GSS_C_CONF_FLAG = 4
GSS_C_INTEG_FLAG = 8
GSS_C_DCE_STYLE = 1024
GSS_C_MUTUAL_FLAG = 1

class CheckSumField:
    def __init__(self, *args, **kwargs):
        pass

class KRB5_AP_REQ:
    def __init__(self, *args, **kwargs):
        pass