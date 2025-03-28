# Document Translation Agent: Agentic translation using reflection workflow

This is a Python demonstration of a reflection agentic workflow for machine translation. The main steps are:
1. Use Marker to perform OCR on the input document and obtain a markdown file;
2. Prompt an LLM to translate a text from `source_language` to `target_language`;
3. Have the LLM reflect on the translation to come up with constructive suggestions for improving it;
4. Use the suggestions to improve the translation.

## Customizability

By using an LLM as the heart of the translation engine, this system is highly steerable. For example, by changing the prompts, it is easier using this workflow than a traditional machine translation (MT) system to:
- Modify the output's style, such as formal/informal.
- Specify how to handle idioms and special terms like names, technical terms, and acronyms. For example, including a glossary in the prompt lets you make sure particular terms (such as open source, H100 or GPU) are translated consistently.
- Specify specific regional use of the language, or specific dialects, to serve a target audience. For example, Spanish spoken in Latin America is different from Spanish spoken in Spain; French spoken in Canada is different from how it is spoken in France.

**This is not mature software**, and is the result of Andrew playing around with translations on weekends the past few months, plus collaborators (Joaquin Dominguez, Nedelina Teneva, John Santerre) helping refactor the code.

According to our evaluations using BLEU score on traditional translation datasets, this workflow is sometimes competitive with, but also sometimes worse than, leading commercial offerings. However, we’ve also occasionally gotten fantastic results (superior to commercial offerings) with this approach. We think this is just a starting point for agentic translations, and that this is a promising direction for translation, with significant headroom for further improvement, which is why we’re releasing this demonstration to encourage more discussion, experimentation, research and open-source contributions.

If agentic translations can generate better results than traditional architectures (such as an end-to-end transformer that inputs a text and directly outputs a translation) -- which are often faster/cheaper to run than our approach here -- this also provides a mechanism to automatically generate training data (parallel text corpora) that can be used to further train and improve traditional algorithms. (See also [this article in The Batch](https://www.deeplearning.ai/the-batch/building-models-that-learn-from-themselves/) on using LLMs to generate training data.)

Comments and suggestions for how to improve this are very welcome!


## Getting Started

To get started, follow these steps:

### Installation:
- The Poetry package manager is required for installation. [Poetry Installation](https://python-poetry.org/docs/#installation) Depending on your environment, this might work:

```bash
pip intsall marker-pdf[full]
pip install poetry
```

- A .env file with a OPENAI_API_KEY is required to run the workflow. See the .env.sample file as an example.
```bash
git clone https://github.com/gbull25/document-translation.git
cd translation-agent
poetry install
poetry shell # activates virtual environment
```
### Usage:

```python
import translation_agent as ta
source_lang, target_lang, country = "English", "Spanish", "Mexico"
translation = ta.translate(source_lang, target_lang, source_text, country)
```
See examples/translate_document.py for an example script to try out.

## License

Translation Agent is released under the **MIT License**. You are free to use, modify, and distribute the code
for both commercial and non-commercial purposes.
