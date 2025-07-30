# Muxify: Multiplex Stdout



```bash
pip install muxify
```


```python
import time
from muxify import Muxify

mux = Muxify(2, flush_interval=0.01)
i = 0
while True:
    if i % 5 == 0:
        print(f"Update {i} to tile0", file=mux[0])
    print(f"Update {i} to tile1", file=mux[1])
    time.sleep(0.01)
    i += 1
```


If `muxify` causes high CPU load in the VS code terminal you should try to disable GPU acceleration: Go to `Preferences` => `Settings` => Search for `terminal GPU acceleration` => `off`