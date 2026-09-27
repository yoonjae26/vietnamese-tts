import importlib.util

# Module cần thư viện tùy chọn: bỏ qua khi thu thập doctest nếu môi trường không có thư viện đó.
OPTIONAL = {
    "src/vitts/translit/*": "torch",
    "src/vitts/server.py": "fastapi",
    "src/vitts/synthesizer.py": "numpy",
}
collect_ignore_glob = [path for path, dep in OPTIONAL.items() if importlib.util.find_spec(dep) is None]
