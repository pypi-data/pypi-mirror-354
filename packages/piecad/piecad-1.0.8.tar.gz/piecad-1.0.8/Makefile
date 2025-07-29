
all: test documents

documents:
	black piecad/*.py tests/*.py doc_examples/*.example examples/*.py
	rm -rf docs/*
	pdoc3 --html piecad --force
	(cd doc_examples; ./mk_doc_examples)
	(cd examples; ./mk_examples_list >README.md)
	mv html/piecad/* docs
	rm -rf html

test:
	pytest tests --benchmark-disable

benchmark:
	pytest tests --benchmark-only

savebenchmark:
	(read -p "Benchmark Name: " -r NAME ; pytest tests --benchmark-only --benchmark-save=`date +%F`"$${NAME}" --benchmark-name=short)

clean:
	rm -f examples/*.obj
