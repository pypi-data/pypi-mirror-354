test:
	uv run pytest tests/ -v -s

.PHONY: test

generate-schema:
	rm -rf src/nebu/chatx/openai.py
	uv run datamodel-codegen --input ./spec/openai.yaml --input-file-type openapi --output ./src/nebu/chatx/openai.py --output-model-type pydantic_v2.BaseModel --snake-case-field --use-union-operator --reuse-model --target-python-version 3.11 --use-double-quotes --field-constraints 

.PHONY: generate-schema