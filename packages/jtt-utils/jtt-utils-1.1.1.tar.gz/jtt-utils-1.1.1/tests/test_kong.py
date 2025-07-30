from jtt_tm_utils.kong import Kong
import logging
logging.basicConfig(level=20,format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
kong = Kong()
host =None
 
kong.register_upstream_service('candytest',8000,'/candytest',host=None,custom_base_path="",auth='jwt')