import subprocess

def test_mypy_clean():
    """Testa se o código está limpo de erros de tipagem (mypy)."""
    result = subprocess.run(
        ["python", "-m", "mypy", "my_data_lib"], capture_output=True, text=True
    )
    assert result.returncode == 0, f"mypy errors:\n{result.stdout}\n{result.stderr}"