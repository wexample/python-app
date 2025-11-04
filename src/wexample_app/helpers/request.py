def request_build_id() -> str:
    import os
    from datetime import datetime

    return f"{datetime.now().strftime('%Y%m%d-%H%M%S-%f')}-{os.getpid()}"