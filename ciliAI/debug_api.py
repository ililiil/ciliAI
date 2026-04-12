import os
import json
from volcengine.visual.VisualService import VisualService
from dotenv import load_dotenv

load_dotenv()

VOLC_AK = os.getenv('VOLC_AK')
VOLC_SK = os.getenv('VOLC_SK')

visual_service = VisualService()
visual_service.set_ak(VOLC_AK)
visual_service.set_sk(VOLC_SK)

params = {
    "req_key": "jimeng_t2i_v40",
    "prompt": "一只可爱的小猫",
    "width": 1024,
    "height": 1024,
    "model_version": "v4.0"
}

print("Params:", params)
try:
    res = visual_service.common_json_handler("CVSync2AsyncSubmitTask", params)
    print("Response:", res)
except Exception as e:
    print("Exception:", str(e))
