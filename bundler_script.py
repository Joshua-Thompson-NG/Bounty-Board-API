from pathlib import Path


def bundle_code(target_dir: str = "app", output_file: str = "project_submission.txt"):
    root = Path(target_dir)
    output_path = Path(output_file)

    if not root.exists():
        print(
            f"Error: Directory '{target_dir}' not found. Run this from your project root!"
        )
        return

    # Find all .py files and sort them for a clean, predictable order
    py_files = sorted(root.rglob("*.py"))

    with output_path.open("w", encoding="utf-8") as out:
        out.write("# ==========================================\n")
        out.write(f"# PROJECT BUNDLE ({len(py_files)} files)\n")
        out.write("# ==========================================\n\n")

        for file_path in py_files:
            # Skip __pycache__ just in case
            if "__pycache__" in file_path.parts:
                continue

            content = file_path.read_text(encoding="utf-8").strip()
            out.write(f"{'=' * 60}\n")
            out.write(f"FILE: {file_path.as_posix()}\n")
            out.write(f"{'=' * 60}\n")
            if content:
                out.write(f"{content}\n\n")
            else:
                out.write("# [Empty File]\n\n")

    print(f"Success! Bundled {len(py_files)} files into '{output_file}'.")


if __name__ == "__main__":
    bundle_code()
