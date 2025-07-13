import sys
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python fix_autostring.py <file_path>")
    sys.exit(1)

file_path = Path(sys.argv[1])
if not file_path.exists():
    print(f"File not found: {file_path}")
    sys.exit(1)

text = file_path.read_text()

# Ganti AutoString jadi String
fixed = text.replace("sqlmodel.sql.sqltypes.AutoString", "sa.String")

# Tambah import sa kalau belum ada
if "import sqlalchemy as sa" not in fixed:
    fixed = "import sqlalchemy as sa\n" + fixed

file_path.write_text(fixed)
print(f"✔ Patched AutoString in: {file_path}")
