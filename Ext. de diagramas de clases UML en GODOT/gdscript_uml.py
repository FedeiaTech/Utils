import os
import re

def parse_project_for_methods(project_path):
    class_methods = {}
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith('.gd'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    class_name_match = re.search(r'class_name\s+([\w\d_]+)', content)
                    class_name = class_name_match.group(1) if class_name_match else os.path.basename(file_path).replace('.gd', '')
                    methods = re.findall(r'func\s+([\w\d_]+)', content)
                    class_methods[class_name] = set(methods)
    return class_methods

def parse_gdscript_files(project_path, all_class_methods):
    parsed_classes = []
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith('.gd'):
                file_path = os.path.join(root, file)
                info = {
                    'name': None,
                    'extends': None,
                    'signals': [],
                    'attributes': [], # Nuevo: contendrá el nombre y tipo
                    'methods': [],   # Nuevo: contendrá el nombre, parámetros y tipo de retorno
                    'dependencies': set()
                }
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                class_name_match = re.search(r'class_name\s+([\w\d_]+)', content)
                info['name'] = class_name_match.group(1) if class_name_match else os.path.basename(file).replace('.gd', '')
                extends_match = re.search(r'extends\s+([\w\d_]+)', content)
                info['extends'] = extends_match.group(1) if extends_match else None
                info['signals'] = re.findall(r'signal\s+([\w\d_]+)', content)
                
                # Búsqueda de atributos (variables) con visibilidad y tipo
                attributes_matches = re.finditer(r'(?:@export\s+)?var\s+([\w\d_]+)(?::\s*([\w\d_]+))?', content)
                for match in attributes_matches:
                    visibility = "-" if match.group(1).startswith('_') else "+"
                    export = "<<exported>>" if "@export" in match.group(0) else ""
                    attr_type = match.group(2) if match.group(2) else "any"
                    info['attributes'].append(f"{visibility} {match.group(1)} : {attr_type} {export}".strip())
                
                # Búsqueda de métodos (funciones) con visibilidad, parámetros y tipo de retorno
                methods_matches = re.finditer(r'func\s+([\w\d_]+)\s*\((.*?)\)(?:\s*->\s*([\w\d_]+))?', content)
                for match in methods_matches:
                    visibility = "-" if match.group(1).startswith('_') else "+"
                    params = match.group(2) if match.group(2) else ""
                    return_type = f" : {match.group(3)}" if match.group(3) else ""
                    info['methods'].append(f"{visibility} {match.group(1)}({params}){return_type}".strip())
                
                # Detección de dependencias (lógica anterior)
                potential_calls = re.findall(r'(\w+)\s*\.\s*(\w+)', content)
                for var, method in potential_calls:
                    if var in all_class_methods and method in all_class_methods[var]:
                        info['dependencies'].add(var)
                
                parsed_classes.append(info)
    return parsed_classes

def generate_plantuml(parsed_classes):
    class_diagram_lines = ["@startuml\n"]
    class_names = {cls['name'] for cls in parsed_classes}
    for cls in parsed_classes:
        class_diagram_lines.append(f"class {cls['name']} {{\n")
        
        for attr in cls['attributes']:
            class_diagram_lines.append(f"  {attr}\n")
        
        if cls['signals']:
            class_diagram_lines.append("  --\n")
            for sig in cls['signals']:
                class_diagram_lines.append(f"  + {sig} () <<signal>>\n")
        
        if cls['methods']:
            class_diagram_lines.append("  --\n")
            for method in cls['methods']:
                class_diagram_lines.append(f"  {method}\n")

        class_diagram_lines.append("}\n")
    class_diagram_lines.append("\n")

    for cls in parsed_classes:
        if cls['extends'] and cls['extends'] in class_names:
            class_diagram_lines.append(f"{cls['extends']} <|-- {cls['name']}\n")
        for dep in sorted(list(cls['dependencies'])):
            if dep != cls['name'] and dep in class_names:
                class_diagram_lines.append(f"{cls['name']} .> {dep} : usa\n")

    class_diagram_lines.append("\n@enduml")
    return "".join(class_diagram_lines)

if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.abspath(__file__))
    all_class_methods = parse_project_for_methods(current_directory)
    parsed_data = parse_gdscript_files(current_directory, all_class_methods)
    uml_code = generate_plantuml(parsed_data)
    output_path = os.path.join(current_directory, "diagrama.puml")
    with open(output_path, "w", encoding='utf-8') as f:
        f.write(uml_code)
    print(f"Diagrama generado exitosamente en: {output_path}")