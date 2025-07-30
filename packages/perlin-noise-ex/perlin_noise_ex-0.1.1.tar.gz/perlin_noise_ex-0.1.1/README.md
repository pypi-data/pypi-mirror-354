# perlin_noise_dhex

Python implementation of Perlin noise generator by Exityx (DH - DataHandler)

## Installation

```bash
pip install perlin_noise_dhex
```

## Usage

```python
from perlin_noise_dhex import CreateNewPerlinNoise

# Create noise generator
noise = CreateNewPerlinNoise(seed=20, octave=2, amp=7, period=24)

matrix = noise.createPerlin()

noise.showGraph(matrix)

```

## License

MIT