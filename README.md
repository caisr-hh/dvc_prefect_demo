# ML tooling tutorial: DVC + Prefect demo

This is part of the [ML Tooling Tutorial](https://github.com/caisr-hh/ml_tooling_tutorial).

Content

- A simple ML pipeline
    - `mltoy/` code base
    - `data/raw/iris.csv` tiny dataset
    - `params.yaml` YAML config for the 
- Documents
    - `docs/dvc_walkthrough.md` (and pdf) the walkthrough slide deck
    - `docs/dvc_walkthrough_extension_slides.md` (and pdf) a set of broader and deeper tips as an extension to walkthrough

## Install dependencies

Follow dependency management instructions [here](https://github.com/caisr-hh/ml_tooling_tutorial).

## Run the pipeline (bare-bone)

```bash
python -m mltoy.cli run-all # run the whole pipeline without DVC
python -m mltoy.cli prepare
python -m mltoy.cli train
python -m mltoy.cli evaluate
```

## Walkthrough

See `docs/dvc_walkthrough_slides.pdf`

See also `docs/dvc_walkthrough_extension_slides.pdf` for more ...

<details>
<summary>Generate slides from markdown</summary>

```bash
cd docs/

pandoc \
    dvc_walkthrough.md -o dvc_walkthrough_slides.pdf \
	-t beamer \
	-f markdown+raw_tex \
	--slide-level=3 \
	--variable aspectratio=169 \
	--variable fontsize=10pt \
    --variable theme=metropolis \
    --highlight-style=tango \
	-H beamer_preamble.tex

pandoc \
    dvc_walkthrough_extension.md -o dvc_walkthrough_extension_slides.pdf \
	-t beamer \
	-f markdown+raw_tex \
	--slide-level=3 \
	--variable aspectratio=169 \
	--variable fontsize=10pt \
    --variable theme=metropolis \
    --highlight-style=tango \
	-H beamer_preamble.tex
```
</details>


## Note

Portions of this code/project were developed with the assistance of ChatGPT (a product of OpenAI).