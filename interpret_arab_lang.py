import sys
import json
import math
from datetime import datetime

def interpret_arab_lang(file_path):
    if not file_path.endswith('.arab'):
        print("Unsupported file type. Please use '.arab' files.")
        return

    variables = {}
    json_data = {}

    def process_line(line):
        line = line.strip()

        if not line or line.startswith("#"):
            return

        # Handle variable assignment
        if "=" in line:
            var, value = map(str.strip, line.split("=", 1))
            if value.startswith('"') and value.endswith('"'):
                value = value.strip('"')
            elif value.lower() in ["true", "false"]:
                value = value.lower() == "true"
            elif value.isdigit():
                value = int(value)
            elif value.replace('.', '', 1).isdigit():
                value = float(value)
            variables[var] = value
            return

        # Handle JSON string assignment
        if line.startswith("json_string"):
            _, json_string = line.split("=", 1)
            json_string = json_string.strip().strip('"')
            try:
                global json_data
                json_data = json.loads(json_string)
            except json.JSONDecodeError:
                print("Error: Invalid JSON format.")
            return

        # Handle JSON extraction
        if line.startswith("json_data"):
            _, key = line.split("=", 1)
            key = key.strip().strip('"')
            if key in json_data:
                variables['json_value'] = json_data[key]
            else:
                print(f"Error: Key '{key}' not found in JSON data.")
            return

        # Handle basic arithmetic operations
        if "ضرب" in line:
            _, var, num = map(str.strip, line.split("ضرب", 1)[1].split(maxsplit=1))
            if var in variables:
                variables[var] *= int(num)
            return

        if "جمع" in line:
            _, var1, var2 = map(str.strip, line.split("جمع", 1)[1].split(maxsplit=1))
            if var1 in variables and var2 in variables:
                variables['temp'] = variables[var1] + variables[var2]
            return

        # Handle print command
        if line.startswith("طباعة"):
            content = line.split("طباعة", 1)[1].strip()
            resolved_content = resolve_expression(content)
            print(resolved_content)
            return

        # Handle function definitions
        if line.startswith("تعريف"):
            _, func_definition = line.split("تعريف", 1)
            func_name, params = func_definition.split("(", 1)
            params, body = params.split(")", 1)
            func_name = func_name.strip()
            params = [p.strip() for p in params.split(",")]
            body = body.strip()
            variables[f"function_{func_name}"] = (params, body)
            return

        # Handle function calls
        if line.startswith("استدعاء"):
            _, call = line.split("استدعاء", 1)
            func_name, args = call.split("(", 1)
            args, _ = args.split(")", 1)
            func_name = func_name.strip()
            args = [arg.strip() for arg in args.split(",")]
            params, body = variables.get(f"function_{func_name}", ([], ""))
            if len(args) != len(params):
                print(f"Error: Incorrect number of arguments for function '{func_name}'.")
                return
            local_vars = {}
            for param, arg in zip(params, args):
                local_vars[param] = eval_expression(arg)
            process_lines(body.split("\n"))
            for param in params:
                variables[param] = local_vars[param]
            return

        # Handle JSON functions
        if line.startswith("طول"):
            _, text = line.split("طول", 1)
            text = text.strip().strip('"')
            length = len(text)
            variables['length'] = length
            return

        if line.startswith("جزء"):
            _, text, start, end = line.split("جزء", 1)[1].split("إلى", 1)
            start, end = map(int, [start.strip(), end.strip()])
            text = text.strip().strip('"')
            substring = text[start:end]
            variables['substring'] = substring
            return

        if line.startswith("جذر"):
            _, number = line.split("جذر", 1)
            number = float(number.strip())
            result = math.sqrt(number)
            variables['result'] = result
            return

        if line.startswith("وقت_الآن"):
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            variables['current_time'] = now
            return

        # Handle love Easter egg
        if line.startswith("حب"):
            value = line.split("=", 1)[1].strip()
            if value.lower() in ["true", "false"]:
                print("الحب ليس صحيحا أو خاطئا")
            return

        # Handle Zen of arab-lang Easter egg
        if line.startswith("هذا"):
            value = line.split("=", 1)[1].strip()
            if value.lower() == "zen":
                print(zen_of_arab_lang)
            return

        # Unsupported command
        print(f"Error: Unrecognized command '{line}'")

    def process_lines(lines):
        for line in lines:
            process_line(line)

    def resolve_expression(expr):
        for var in variables:
            expr = expr.replace(var, str(variables[var]))
        return expr

    def eval_expression(expr):
        try:
            return eval(resolve_expression(expr))
        except Exception as e:
            print(f"Error evaluating expression '{expr}': {e}")
            return None

    zen_of_arab_lang = """
    1. البساطة أفضل من التعقيد.
    2. وضوح أفضل من الغموض.
    3. الجمال أفضل من القبح.
    4. الصدق أفضل من التكرار.
    5. يجب أن يكون لديك وضوح في الأخطاء.
    6. يجب أن تكون الحلول صالحة وسهلة الفهم.
    7. لن يكتب البرنامج بشكل صحيح على الرغم من أنه يعمل.
    8. يجب أن تكون الأكواد ذات مغزى وفهم.
    9. لا تترك الأخطاء لتصبح مشكلة.
    10. الطابع البسيط يعزز من الجودة.
    """

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    process_lines(lines)

# Main entry point
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python interpret_arab_lang.py <file.arab>")
        sys.exit(1)

    file_path = sys.argv[1]
    interpret_arab_lang(file_path)
