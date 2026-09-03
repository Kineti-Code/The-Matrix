import re

class Matrix():
    class OperationError(ValueError):
        pass

    @staticmethod
    def _validate_construction(rows: int, columns: int):
        if rows == 1 and columns == 1:
            raise ValueError("Cannot construct 1x1 matrix (js use a normal number lol)")
        if rows <= 0 or columns <= 0:
            raise ValueError("Matrix cannot have 0 rows or columns!")

    def _validate_values(self):
        if len(self.values) != self.num_rows:
            raise ValueError("Num rows not equal to parameter 'num_rows'!")
        for row in self.values:
            if len(row) != self.num_columns:
                raise ValueError("Num columns not equal to parameter 'num_columns'!")

    def __init__(self, num_rows, num_columns, values):
        self._validate_construction(num_rows, num_columns)

        self.num_rows = num_rows
        self.num_columns = num_columns
        self.values = values

        self._validate_values()

    def __str__(self):        
        return "\n".join([" ".join([f"{num:g}" for num in row]) for row in self.values])


    # Replacement - add multiple of one row to another
    # Interchange - swap two rows
    # Scale - Multiply each column in a row by a constant

    def validate_row(self, row_idx):
        if row_idx < 0 or row_idx >= len(self.values):
            raise IndexError("Index does not correspond to a valid row!")

    # 2r1 -> r1
    def scale(self, row, scalar):
        for col in range(len(self.values[row])):
            self.values[row][col] *= scalar

    # 2r1 + r2 -> r2
    def replace(self, row_from, row_to, scalar=1):
        scaled_row_from = self.values[row_from][:]

        for col in range(len(scaled_row_from)):
            scaled_row_from[col] *= scalar

        for col in range(self.num_columns):
            self.values[row_to][col] = scaled_row_from[col] + self.values[row_to][col]

    # r2 <-> r1
    def interchange(self, row1, row2):
        og_row1 = self.values[row1]

        self.values[row1] = self.values[row2]
        self.values[row2] = og_row1

    def parse_text(self, text):
        cleaned_text = text.replace(" ", "").lower()

        # Scale has no + and only ->
        # Replace has plus sign and ->
        # interchange has <->

        interchange_symbol = "<->"
        replace_symbol = "+"
        scale_symbol = "->"

        if interchange_symbol in cleaned_text:
            match = re.fullmatch(r"r(\d+)<->r(\d+)", cleaned_text)
            if not match:
                raise SyntaxError("Invalid syntax detected for interchange operation. Follow the format 'r[row_num] <-> r[row_num]'")
            
            row1 = int(match.group(1)) - 1
            row2 = int(match.group(2)) - 1

            self.interchange(row1, row2)
            print(f"Interchanged row {row1+1} with row {row2+1}")

        elif replace_symbol in cleaned_text:
            match = re.fullmatch(r"(-?\d+\.?\d*)r(\d+)\+r(\d+)->r(\d+)", cleaned_text)
            if not match:
                raise SyntaxError("Invalid syntax detected for replacement operation. Follow the format 'nr[row_num_from] + nr[row_num_to] -> r[row_num_to]' (no subtraction between rows)")
            
            scalar = float(match.group(1)) if '.' in match.group(1) else int(match.group(1))
            row_from = int(match.group(2)) - 1
            row_added_to = int(match.group(3)) - 1
            row_to = int(match.group(4)) - 1
            
            if row_added_to != row_to:
                raise self.OperationError("Row being operated on must come after the plus sign!")

            self.replace(row_from, row_to, scalar)
            print(f"Replaced row {row_to+1} with {scalar} * row {row_from+1} + row {row_to+1}")

        elif scale_symbol in cleaned_text:
            # Pattern: (scalar)r(digits) -> r(digits)
            match = re.fullmatch(r"(-?\d+\.?\d*)r(\d+)->r(\d+)", cleaned_text)
            if not match:
                raise SyntaxError("Invalid syntax detected for scaling operation. Follow the format 'nr[row_num] -> r[row_num]'!")
                
            scalar = float(match.group(1)) if '.' in match.group(1) else int(match.group(1))
            row_from = int(match.group(2)) - 1
            row_to = int(match.group(3)) - 1
            
            if row_from != row_to:
                raise self.OperationError("Scaled row must match the destination row!")
                
            self.scale(row_from, scalar)
            print(f"Scaled row {row_from+1} by {scalar}")

        else:
            raise SyntaxError("Invalid syntax detected! Valid operations are replacement, interchange, and scaling.")

