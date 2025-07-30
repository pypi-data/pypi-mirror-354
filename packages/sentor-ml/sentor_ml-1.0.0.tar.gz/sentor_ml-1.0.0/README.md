# Sentor Python SDK

A Python SDK for interacting with the Sentor ML API for sentiment analysis. This SDK provides a simple and intuitive interface for sentiment analysis operations.

## Installation

```bash
pip install sentor-ml
```

## Features

- 🚀 Python 3.7+ support
- ⚡ Simple and intuitive API
- 🌍 Support for multiple languages
- 📦 Batch processing capabilities
- 🛡️ Comprehensive error handling
- 🔄 Real-time sentiment analysis

## Usage

### Basic Usage

```python
from sentor import SentorClient

# Initialize the client
client = SentorClient('your-api-key')

# Analyze sentiment
input_data = [
    {
        "doc": "Apple's new iPhone is amazing!",
        "doc_id": "1",
        "entities": [
            "Apple",
            "iPhone"
        ]
    },
    {
        "doc": "Samsung's new phone is amazing!",
        "doc_id": "2",
        "entities": [
            "Samsung",
            "phone"
        ]
    }
]
result = client.analyze(input_data)
print(result)
```

### Sample Output

```json
{
  "results": [
    {
      "doc_id": "1",
      "predicted_class": 2,
      "predicted_label": "positive",
      "probabilities": {
        "negative": 0.00010637386003509164,
        "neutral": 0.0002509312762413174,
        "positive": 0.9996427297592163
      }
    },
    {
      "doc_id": "2",
      "predicted_class": 2,
      "predicted_label": "positive",
      "probabilities": {
        "negative": 0.00010637386003509164,
        "neutral": 0.0002509312762413174,
        "positive": 0.9996427297592163
      }
    }
  ]
}
```

## API Reference

Please refer to the [Sentor ML API Documentation](https://ml.sentor.app) for more details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see the [LICENSE](LICENSE) file for details.