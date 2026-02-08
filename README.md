# ML tooling tutorial: DVC + Prefect demo

This is part of the [ML Tooling Tutorial](https://github.com/caisr-hh/ml_tooling_tutorial).

Content

- A simple ML pipeline
    - `mltoy/` code base
    - `data/raw/iris.csv` tiny dataset
    - `params.yaml` YAML config for the 
- Walk through slide decks
    - `docs/dvc_walkthrough.md`
    - `docs/dvc_walkthrough_extension_slides.md`
    - `docs/prefect_walkthrough.md`

## Install dependencies

Follow dependency management instructions [here](https://github.com/caisr-hh/ml_tooling_tutorial).

## Run the pipeline (bare-bone)

```bash
python -m mltoy.cli run-all # run the whole pipeline without DVC
python -m mltoy.cli prepare
python -m mltoy.cli train
python -m mltoy.cli evaluate
```

## Make targets

Try `make` to see available targets.

## Walkthrough documents

- DVC walkthrough: `docs/dvc_walkthrough_slides.pdf`
- DVC walkthrough extension: `docs/dvc_walkthrough_extension_slides.pdf` 
- Prefect walkthrough:  `docs/prefect_walkthrough.pdf`

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

pandoc \
    prefect_walkthrough.md -o prefect_walkthrough_slides.pdf \
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