import sys

class JPLInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.program_started = False
        self.program_name = ""

    def display(self, message):
        for var, value in self.variables.items():
            message = message.replace(var, str(value))
        print(message)

    def define_variable(self, name, value):
        self.variables[name] = value

    def input_variable(self, prompt):
        value = input(prompt)
        self.variables['input'] = value

    def define_function(self, name, params, body):
        self.functions[name] = (params, body)

    def call_function(self, name, args):
        if name not in self.functions:
            raise SyntaxError(f"Function {name} not defined")
        params, body = self.functions[name]
        if len(params) != len(args):
            raise SyntaxError(f"Function {name} expects {len(params)} arguments, got {len(args)}")
        
        # Save current variables
        old_vars = self.variables.copy()
        
        # Set up function's local variables
        self.variables.update(dict(zip(params, args)))
        
        # Execute function body
        for line in body:
            self.execute_line(line)
        
        # Restore old variables
        self.variables = old_vars

    def execute_line(self, line):
        line = line.strip()
        if not line or line.startswith('#'):  # Ignore empty lines and comments
            return
        if line.startswith("START"):
            parts = line.split()
            self.program_name = parts[1][1:]  # Remove the asterisk
            if line.endswith("{"):
                self.program_started = True
            else:
                raise SyntaxError("START command must be followed by '{'")
        elif line.startswith("} END"):
            parts = line.split()
            end_program_name = parts[2][1:]  # Remove the asterisk
            if end_program_name != self.program_name:
                raise SyntaxError(f"Program end name '{end_program_name}' does not match start name '{self.program_name}'")
            self.program_started = False
            self.program_name = ""
        elif not self.program_started:
            raise SyntaxError("Program must start with a START command")
        elif line.startswith("DEFINE FUNCTION"):
            parts = line[len("DEFINE FUNCTION "):].strip().split("(")
            name = parts[0].strip()
            params = parts[1].split(")")[0].strip().split(", ")
            body = []
            # Read function body
            line = input()
            while line.strip() != "}":
                body.append(line.strip())
                line = input()
            self.define_function(name, params, body)
        elif line.startswith("CALL"):
            parts = line[len("CALL "):].strip().split("(")
            name = parts[0].strip()
            args = parts[1].split(")")[0].strip().split(", ")
            self.call_function(name, args)
        elif line.startswith("DISPLAY"):
            message = line[8:].strip()
            self.display(message)
        elif line.startswith("DEFINE"):
            parts = line.split()
            name = parts[1]
            value = ' '.join(parts[2:])
            self.define_variable(name, value)
        elif line.startswith("INPUT"):
            prompt = line[6:].strip()
            self.input_variable(prompt)
            

        else:
            raise SyntaxError("Unknown command: {}".format(line))

    def run_file(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                self.execute_line(line.strip())
        if self.program_started:
            raise SyntaxError("Program ended without END command")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python compiler.py <filename.jpl/jake>")
        sys.exit(1)

    filename = sys.argv[1]

    if not (filename.endswith('.jpl') or filename.endswith('.jake')):
        print("Error: Only .jpl and .jake files are supported")
        sys.exit(1)

    interpreter = JPLInterpreter()
    interpreter.run_file(filename)
