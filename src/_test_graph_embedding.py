from Network import GAGraphEmbeddingConstructor
from Network._quantum_chips import *

# Initial quantum chips
rigetti_16Q_Aspen = Rigetti_16Q_Aspen()
ibm_20Q_Johannesburg = IBM_20Q_Johannesburg()

# Search optimal mapping
embeding_selector = GAGraphEmbeddingConstructor(rigetti_16Q_Aspen, ibm_20Q_Johannesburg)
embeding_selector.run(time_budget=5)

# Show optimal mapping
results = embeding_selector.get_result()
print(results)
