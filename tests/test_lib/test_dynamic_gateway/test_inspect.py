from grpc_gateway.dynamic_gateway.inspect import get_service_option_from_grpc_desc, get_service_option_from_message
from tests.test_lib.util import gen_demo_module


def test_get_service_option_from_grpc_desc() -> None:
    desc_1 = 'test: {"group": "demo", "author": ["so1n", "huluwa"], "tag": [["tag1", "tag_desc"], ["tag2", ""]]}'
    desc_2 = 'test: {"desc": "demo desc", "summary": "demo summary", "url": "/api/demo"}'
    desc_3 = 'test: {"enable": false, "http_method": "get"}'

    desc = "\n".join([desc_1, desc_2, desc_3])
    # test error prefix
    grpc_server_option_model_list_by_desc = get_service_option_from_grpc_desc(desc, "", "aaa")
    assert len(grpc_server_option_model_list_by_desc) == 0

    # test desc
    grpc_server_option_model_list_by_desc = get_service_option_from_grpc_desc(desc, "", "test")
    # test service desc
    grpc_server_option_model_list_by_sdesc = get_service_option_from_grpc_desc("", desc, "test")
    for item in [grpc_server_option_model_list_by_desc, grpc_server_option_model_list_by_sdesc]:
        assert len(item) == 1
        assert item[0].group == "demo"
        assert item[0].author == ("so1n", "huluwa")
        assert item[0].tag == [("tag1", "tag_desc"), ("tag2", "")]
        assert item[0].desc == "demo desc"
        assert item[0].summary == "demo summary"
        assert item[0].url == "/api/demo"
        assert item[0].enable is False
        assert item[0].http_method == "GET"

    # test additional_bindings
    desc = (
        desc
        + "\n"
        + 'test: {"enable": true, "additional_bindings": {"group": "demo1", "enable": false, "url": "/api/boom"}}'
    )
    grpc_server_option_model_list_by_desc = get_service_option_from_grpc_desc(desc, "", "test")
    assert len(grpc_server_option_model_list_by_desc) == 2
    assert grpc_server_option_model_list_by_desc[0].group == "demo"
    assert grpc_server_option_model_list_by_desc[0].author == ("so1n", "huluwa")
    assert grpc_server_option_model_list_by_desc[0].tag == [("tag1", "tag_desc"), ("tag2", "")]
    assert grpc_server_option_model_list_by_desc[0].desc == "demo desc"
    assert grpc_server_option_model_list_by_desc[0].summary == "demo summary"
    assert grpc_server_option_model_list_by_desc[0].url == "/api/demo"
    assert grpc_server_option_model_list_by_desc[0].http_method == "GET"
    assert grpc_server_option_model_list_by_desc[0].enable is True

    assert grpc_server_option_model_list_by_desc[1].group == "demo1"
    assert grpc_server_option_model_list_by_desc[1].url == "/api/boom"


def test_get_service_option_from_message() -> None:
    grpc_service_option_model_list = get_service_option_from_message(
        gen_demo_module.DemoRequest, gen_demo_module.DemoResult, gen_demo_module
    )
    assert len(grpc_service_option_model_list) == 1
    grpc_service_option_model_list[0].author = ("so1n",)
    grpc_service_option_model_list[0].tag = [("demo_tag", "test protobuf tag")]
    grpc_service_option_model_list[0].group = "demo"
    grpc_service_option_model_list[0].desc = "This is a desc"
    grpc_service_option_model_list[0].summary = "This is a summary"
    grpc_service_option_model_list[0].url = "/demo/dynamic-gateway"
