from src.add_dependency import BenchmarkTask, get_func_calls
from dacite import from_dict

if __name__ == "__main__":
    task_data = {
        "task_id": "data/repos/base-4.20.0.0/src/Data/List/NonEmpty.hs--take",
        "signature": "take :: Int -> NonEmpty a -> [a]",
        "code": "take n = List.take n . toList",
        "poly_type": "Parametric",
    }

    task = from_dict(data_class=BenchmarkTask, data=task_data)
    calls = get_func_calls(task)
    assert len(calls) == 4
