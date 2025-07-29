# 🏥 ProbableDoctor

[![PyPI version](https://badge.fury.io/py/probabledoctor.svg)](https://badge.fury.io/py/probabledoctor)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Enhanced Medical Professional Name Parser** with advanced multi-credential support.

ProbableDoctor is an enhanced Python library for parsing medical professional names with proper handling of multiple comma-separated credentials and titles. Built on top of the robust `probablepeople` library, it provides specialized parsing for healthcare professionals.

## ✨ Key Features

- **🎓 Multi-Credential Parsing**: Properly handles multiple credentials like "MD, PhD, FACP"
- **👨‍⚕️ Medical Titles**: Recognizes medical prefixes and professional titles
- **📋 Structured Output**: Returns parsed components as dictionaries for easy processing
- **🔄 Backwards Compatible**: Works with existing `probablepeople` code
- **🎯 High Accuracy**: Uses advanced NLP and machine learning

## 🚀 Quick Start

### Installation

```bash
pip install probabledoctor
```

### Basic Usage

```python
import probabledoctor

# Parse a medical professional's name
result, name_type = probabledoctor.tag("Dr. Sarah Johnson MD, PhD, FACP")

print(result)
# Output: {
#     'PrefixOther': 'Dr.',
#     'GivenName': 'Sarah', 
#     'Surname': 'Johnson',
#     'SuffixOther': 'MD, PhD, FACP'
# }

print(f"Name type: {name_type}")
# Output: Name type: Person
```

### CLI Usage

```bash
# Parse and tag a name
probabledoctor "Dr. Jane Doe MD" --tag

# Parse without tagging
probabledoctor "Dr. Jane Doe MD"

# Use specific model type
probabledoctor "Smith Medical Corp" --type company --tag
```

## 📊 Examples

### Multiple Credentials

```python
import probabledoctor

names = [
    "Taylor Anne Jordan ATC, LAT",
    "Dr. Sarah Johnson MD, PhD, FACP", 
    "Michael Smith RN, BSN, CEN",
    "David Wilson PhD, MD"
]

for name in names:
    result, name_type = probabledoctor.tag(name)
    credentials = result.get('SuffixOther', '')
    full_name = f"{result.get('GivenName', '')} {result.get('Surname', '')}"
    
    print(f"👤 {full_name}")
    print(f"🎓 Credentials: {credentials}")
    print(f"📋 Type: {name_type}")
    print()
```

Output:

```text
👤 Taylor Jordan
🎓 Credentials: ATC, LAT
📋 Type: Person

👤 Sarah Johnson  
🎓 Credentials: MD, PhD, FACP
📋 Type: Person

👤 Michael Smith
🎓 Credentials: RN, BSN, CEN
📋 Type: Person

👤 David Wilson
🎓 Credentials: PhD, MD
📋 Type: Person
```

### Backwards Compatibility

ProbableDoctor maintains full compatibility with `probablepeople`:

```python
import probabledoctor as pp

# Use standard probablepeople functions
result = pp.parse("John Smith")
tagged = pp.tag("Dr. Jane Doe MD")
```

## 🏗️ What's Enhanced?

| Feature | probablepeople | probabledoctor |
|---------|---------------|----------------|
| Basic name parsing | ✅ | ✅ |
| Single credentials | ✅ | ✅ |
| Multiple credentials | ❌ Returns as string | ✅ Returns as string |
| Medical titles | ⚠️ Limited | ✅ Enhanced |
| Complex credentials | ❌ "MD, PhD, FACP" | ✅ "MD, PhD, FACP" |

## ⚠️ Known Limitations

- **Parsing of trailing initials**: In some cases, names with a trailing initial (e.g., "John Doe A") might have the initial misclassified. For example, running `probabledoctor "Kashani Jamshid A" --tag` may currently identify "A" as `SuffixOther` instead of a `MiddleInitial` or as part of the main name components. This is related to the intricacies of the statistical model used for parsing. Efforts to improve accuracy for these patterns are ongoing.

## 🎯 Use Cases

- **Healthcare Systems**: Parse doctor names from databases
- **Medical Records**: Extract credentials from patient records  
- **Research**: Analyze medical professional credentials
- **HR Systems**: Process healthcare worker information
- **Compliance**: Verify medical professional credentials

## 📚 Advanced Usage

### Custom Model Types

```python
# Use different parsing models
result = probabledoctor.tag("Dr. Smith", type="person")
result = probabledoctor.tag("Smith Medical Corp", type="company")
```

## Integration with Existing Code

```python
# Drop-in replacement for probablepeople
import probabledoctor as pp

# Your existing probablepeople code works unchanged
names = ["John Smith", "Dr. Jane Doe MD"]
for name in names:
    parsed = pp.parse(name)
    tagged = pp.tag(name)
```

## Requirements

- Python 3.9+
- python-crfsuite>=0.7
- probableparsing
- doublemetaphone

## Installation from Source

```bash
git clone https://github.com/atk81-candor/probabledoctor
cd probabledoctor
pip install -e .
```

## Running Tests

```bash
pytest tests/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🆘 Support

- 📖 [Documentation](https://github.com/atk81-candor/probabledoctor#readme)
- 🐛 [Issue Tracker](https://github.com/atk81-candor/probabledoctor/issues)
- 💬 [Discussions](https://github.com/atk81-candor/probabledoctor/discussions)

## 🙏 Acknowledgments

Built on top of the excellent [probablepeople](https://github.com/datamade/probablepeople) library by DataMade.

---

### Made with ❤️ for the healthcare community
