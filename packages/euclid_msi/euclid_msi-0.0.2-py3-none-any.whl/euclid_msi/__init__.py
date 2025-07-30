from . import preprocessing as preprocessing
from . import embedding as embedding
from . import clustering as clustering
from . import postprocessing as postprocessing
from . import euclid_casecontrol as euclid_casecontrol
from . import plotting as plotting

__all__ = ["preprocessing", "embedding", "clustering", "postprocessing", "euclid_casecontrol", "plotting"]
__version__ = "0.0.1b"

#TO PUBLISH
#pip install twine
#twine upload dist/*