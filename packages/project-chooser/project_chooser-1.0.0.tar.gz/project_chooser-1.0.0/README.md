# Project Chooser

[![PyPI version](https://badge.fury.io/py/project-chooser.svg)](https://badge.fury.io/py/project-chooser)
[![Python versions](https://img.shields.io/pypi/pyversions/project-chooser.svg)](https://pypi.org/project/project-chooser/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A sophisticated, AI-enhanced recommendation engine designed for academic project allocation in higher education institutions. This system employs advanced algorithmic approaches including Bayesian inference and niche discovery to optimise student-project matching.

## Features

- **🧠 Bayesian Inference Engine**: Smart question selection to minimize cognitive load during preference elicitation
- **🔍 Niche Discovery Algorithm**: Identifies uncommon yet potentially suitable projects through cross-domain analysis
- **⚡ Adaptive Questioning**: Dynamically adjusts strategy based on user responses to maximize information gain
- **📊 Multi-dimensional Scoring**: Combines preference matching, novelty detection, and practical constraints
- **📈 Statistical Analysis**: Comprehensive analytical reports on project distribution and allocation patterns
- **⚙️ Configurable Parameters**: Fine-tune scoring weights and algorithmic parameters for your institution

## Quick Start

### Installation

Install from PyPI using pip:

```bash
pip install project-chooser
```

Or using Poetry:

```bash
poetry add project-chooser
```

### Basic Usage

1. **Interactive Recommendation** (recommended for new users):

   ```bash
   project-chooser recommend --interactive
   ```

2. **Batch Processing** with a JSON file:

   ```bash
   project-chooser recommend --input preferences.json --output recommendations.json
   ```

3. **Data Validation**:

   ```bash
   project-chooser validate projects.json
   ```

4. **Generate Analysis Report**:

   ```bash
   project-chooser analyse projects.json --output analysis_report.json
   ```

## Project Data Format

Create a `projects.json` file with your project data:

```json
{
  "projects": [
    {
      "id": "PROJ001",
      "title": "Machine Learning in Climate Modeling",
      "description": "Apply ML techniques to climate data analysis",
      "degree": "Computer Science",
      "year": 4,
      "supervisor": "Dr. Smith",
      "topics": ["machine learning", "climate science", "data analysis"],
      "skills_required": ["Python", "TensorFlow", "Statistics"],
      "difficulty": "Hard",
      "group_size": "Individual"
    }
  ]
}
```

## Algorithm Details

### Bayesian Inference Engine

The system uses information-theoretic question selection to minimize the number of questions needed to understand user preferences, reducing cognitive load while maximizing information gain.

### Niche Discovery

Advanced algorithms identify projects that may not be obvious matches but could be excellent fits based on:

- Cross-domain skill transfer potential
- Novelty scoring mechanisms  
- Hidden preference pattern recognition

### Scoring System

Multi-dimensional scoring considers:

- Direct preference matching
- Skill requirement alignment
- Supervisor preferences
- Workload and difficulty matching
- Diversity and exploration factors

## Development Setup

For contributors and advanced users:

```bash
# Clone the repository
git clone https://github.com/unkokaeru/project-chooser.git
cd project-chooser

# Install with Poetry (recommended)
poetry install --with dev
poetry shell

# Or install with pip
pip install -e ".[dev]"
```

## Configuration

The system can be configured through environment variables or config files:

```bash
export PROJECT_CHOOSER_DEBUG=true
export PROJECT_CHOOSER_MAX_QUESTIONS=10
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Run the test suite (`poetry run pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENCE) file for details.

## Support

- 📚 [Documentation](https://github.com/unkokaeru/project-chooser/wiki)
- 🐛 [Issue Tracker](https://github.com/unkokaeru/project-chooser/issues)
- 💬 [Discussions](https://github.com/unkokaeru/project-chooser/discussions)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

---

**Made with ❤️ for academic institutions worldwide**
