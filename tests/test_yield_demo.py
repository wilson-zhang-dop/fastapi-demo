"""Demo: how yield works in pytest fixtures."""

import pytest

# 用一个列表记录 fixture 的执行顺序，方便观察
execution_log: list[str] = []


@pytest.fixture
def db_connection():
    """模拟数据库连接的 fixture."""
    execution_log.clear()

    # ── Setup: yield 之前 ──
    execution_log.append("1. 打开数据库连接")
    connection = {"status": "open", "data": []}

    yield connection  # ← 把 connection 交给测试函数

    # ── Teardown: yield 之后（无论测试成功/失败都执行）──
    connection["status"] = "closed"
    execution_log.append("3. 关闭数据库连接")


def test_yield_setup_and_teardown(db_connection):
    """验证 yield 之前的 setup 代码已执行."""
    # 此时 setup 已完成
    assert db_connection["status"] == "open"
    assert execution_log == ["1. 打开数据库连接"]

    # 模拟业务操作
    db_connection["data"].append("test_record")
    execution_log.append("2. 测试函数执行中")


def test_teardown_was_executed():
    """验证上一个测试结束后，yield 之后的 teardown 代码已执行.

    注意：pytest 按顺序执行同文件的测试，所以这个测试能看到
    上一个测试的 fixture teardown 结果。
    """
    assert execution_log == [
        "1. 打开数据库连接",
        "2. 测试函数执行中",
        "3. 关闭数据库连接",  # ← 证明 yield 之后的代码执行了
    ]


# ─── 嵌套 fixture 演示 yield 的执行顺序 ───


nested_log: list[str] = []


@pytest.fixture
def outer():
    nested_log.clear()
    nested_log.append("outer-setup")
    yield "outer_value"
    nested_log.append("outer-teardown")


@pytest.fixture
def inner(outer):
    nested_log.append("inner-setup")
    yield f"{outer}+inner_value"
    nested_log.append("inner-teardown")


def test_nested_fixture_order(inner):
    """嵌套 fixture 的执行顺序: 外层setup → 内层setup → 测试 → 内层teardown → 外层teardown."""
    assert inner == "outer_value+inner_value"
    nested_log.append("test-running")


def test_nested_teardown_order():
    """验证嵌套 teardown 顺序：内层先清理，外层后清理（栈顺序）."""
    assert nested_log == [
        "outer-setup",
        "inner-setup",
        "test-running",
        "inner-teardown",   # ← 内层先 teardown
        "outer-teardown",   # ← 外层后 teardown
    ]
