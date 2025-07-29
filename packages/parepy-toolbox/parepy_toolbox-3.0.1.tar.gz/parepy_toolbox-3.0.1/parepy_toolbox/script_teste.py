import os
import subprocess

source_folder = '.'
output_folder = 'docs_md'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

modules = [
    f[:-3] for f in os.listdir(source_folder)
    if f.endswith('.py') and f != '__init__.py' and f != 'script_teste.py'
]

yml_template = """\
loader:
  type: python
  search_path: ["{search_path}"]
  modules: ["{module}"]

renderer:
  type: markdown
  filename: "{output_file}"
"""

for module in modules:
    print(f'Gerando documentação para módulo {module}...')
    yml_filename = f'pydoc_{module}.yml'
    output_file = os.path.join(output_folder, f'{module}.md').replace("\\", "/")

    yml_content = yml_template.format(
        search_path=source_folder,
        module=module,
        output_file=output_file
    )

    # Salva o arquivo YAML temporário
    with open(yml_filename, 'w', encoding='utf-8') as f:
        f.write(yml_content)

    print(f'YAML para {module}:\n{yml_content}\n---\n')

    # Executa o pydoc-markdown com o YAML criado
    result = subprocess.run(['pydoc-markdown', yml_filename], capture_output=True, text=True)

    if result.returncode == 0:
        print(f'Documentação gerada com sucesso: {output_file}\n')
    else:
        print(f'Erro ao gerar documentação para {module}:')
        print(result.stderr)
        print()

    # Remove o YAML temporário
    os.remove(yml_filename)
