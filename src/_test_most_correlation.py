from Network.MostCorrelation._ga_selector import GACorrelationQsubsetSelector
from Network._quantum_chips import *

selector = GACorrelationQsubsetSelector(IBM_5Q_Yorktown())

# Run MostCorrelation selector with time budget 10 seconds
selector.run(time_budget=10)

# Get Result
results = selector.get_result()

print(results)
