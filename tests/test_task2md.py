import pytest
from hypothesis import given, strategies as st
from src.common import BenchmarkTask, md2task, task2md


# Strategy for generating BenchmarkTask instances
@st.composite
def benchmark_task_strategy(draw):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    task_id = draw(st.text(alphabet=alphabet, min_size=1))
    poly_type = draw(st.text(alphabet=alphabet, min_size=1))
    signature = draw(st.text(alphabet=alphabet, min_size=1))
    code = draw(st.text(alphabet=alphabet, min_size=1))
    dependencies = draw(st.lists(st.text(alphabet=alphabet, min_size=1)))
    return BenchmarkTask(task_id, poly_type, signature, code, dependencies)


@given(benchmark_task_strategy())
def test_md2task(task):
    md = task2md(task)
    new_task = md2task(md)
    assert new_task.task_id == task.task_id
    assert new_task.poly_type == task.poly_type
    assert new_task.signature == task.signature
    assert new_task.code == task.code
    assert new_task.dependencies == task.dependencies


@given(benchmark_task_strategy())
def test_roundtrip_task2md_md2task(task):
    md = task2md(task)
    new_task = md2task(md)
    assert new_task == task


@given(benchmark_task_strategy())
def test_roundtrip_md2task_task2md(task):
    md = task2md(task)
    new_task = md2task(md)
    new_md = task2md(new_task)
    assert new_md == md


if __name__ == "__main__":
    test_roundtrip_md2task_task2md()
    test_roundtrip_task2md_md2task()
