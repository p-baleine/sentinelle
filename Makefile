# 生成されるファイル側でパッケージのパスがおかしいときは以下参照
# https://github.com/grpc/grpc/issues/9575#issuecomment-293934506
# (そんなん分からんよ…)一応理由は以下らしい
# https://github.com/protocolbuffers/protobuf/issues/1491#issuecomment-263924909
# へー

PROTO_DEF_FILES = $(shell find protos/sentinelle -name "*.proto")
PB2_FILES =$(PROTO_DEF_FILES:protos/sentinelle/%.proto=sentinelle/%_pb2.py)
PB2_GRPC_FILES = \
$(PROTO_DEF_FILES:protos/sentinelle/%.proto=sentinelle/%_pb2_grpc.py)

all: $(PB2_FILES) $(PB2_GRPC_FILES)

sentinelle/%_pb2.py: protos/sentinelle/%.proto
	pipenv run python -m grpc_tools.protoc -I protos \
		--python_out . \
		--grpc_python_out . \
		$<

sentinelle/%_pb2_grpc.py: protos/sentinelle/%.proto
	pipenv run python -m grpc_tools.protoc -I protos \
		--python_out . \
		--grpc_python_out . \
		$<
