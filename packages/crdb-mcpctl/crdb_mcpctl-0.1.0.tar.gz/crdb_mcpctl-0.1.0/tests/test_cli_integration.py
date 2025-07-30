import subprocess

def test_real_list_contexts():
    result = subprocess.run(["crdb-mcpctl", "list", "contexts"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "contexts" in result.stdout
