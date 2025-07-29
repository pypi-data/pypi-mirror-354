from abstract_flask import *
from ..imports import *
response_bp,logger = get_bp('response_bp',__name__,
                            url_prefix=URL_PREFIX,
                            static_folder=RESPONSE_DIR)
@response_bp.route('/response',methods=["POST","GET"])
def ReSpOnSe():
    data = parse_and_spec_vars(flask_request,['response'])
    response = data.get('response')
    safe_dump_to_file(data=response,file_path=RESPONSE_FILE_PATH)
