from codefabric.types.enums import Technologies

ProjectInitializationCommands: dict[str, str] = {
    Technologies.NodeJS.value: "npm init -y",
    Technologies.PYTHON_UV.value: "uv init",
    Technologies.PYTHON.value: "python3 -m venv .venv",
    Technologies.NEXTJS_TAILWIND_TYPESCRIPT.value: """npx create-next-app@latest . --typescript --tailwind --eslint --src-dir --no-app --import-alias "@/*" --yes""",
}

PackageInstallationCommands: dict[str, str] = {
    Technologies.NodeJS.value: "npm install {packages}",
    Technologies.PYTHON_UV.value: "uv add {packages}",
    Technologies.PYTHON.value: ".venv/bin/python -m pip install {packages}",
    Technologies.NEXTJS_TAILWIND_TYPESCRIPT.value: "npm install {packages}",
}