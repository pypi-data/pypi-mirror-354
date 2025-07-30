# Transqlate

**Transqlate** is a production-ready, schema-aware natural language to SQL command-line assistant powered by a fine-tuned Phi-4 Mini language model.
It enables both technical and non-technical users to generate complex, accurate SQL queries over arbitrary relational databases—simply by typing English instructions.

---

## Key Features

* **Natural Language to SQL**: Translate plain English questions into executable, context-aware SQL queries.
* **Schema-Aware Retrieval (RAG)**: Automatically extracts and injects relevant schema information, scaling to large and complex databases.
* **Interactive CLI**: User-friendly terminal interface with support for query generation, schema exploration, safe execution, and dynamic database switching.
* **Safe Query Execution**: Built-in guardrails prevent accidental schema/data changes; all data-altering queries require explicit user confirmation.
* **Plug-and-Play**: Pip-installable, works on any system with Python 3.8+. No GPU required for inference.
* **Database Support**: Compatible with SQLite, PostgreSQL, MySQL, MSSQL, and Oracle databases.

---

## Installation

```bash
pip install transqlate
```

---

## Usage

### Start the interactive CLI:

```bash
transqlate --interactive
```

### Generate SQL for a specific question:

```bash
transqlate -q "List all customers who made purchases in March." --db-path path/to/database.db
```

### Explore schema or change connections:

```
:show schema         # Display current database schema
:change connection   # Switch to a new database on the fly
```

---

## License

MIT License

---

## Author

[Shaurya Sethi](https://huggingface.co/Shaurya-Sethi)
Email: [shauryaswapansethi@gmail.com](mailto:shauryaswapansethi@gmail.com)

---

**For full documentation, model details, and source code, visit the [GitHub repository](https://github.com/Shaurya-Sethi/transqlate-phi4) or [Hugging Face model page](https://huggingface.co/Shaurya-Sethi/transqlate-phi4).**