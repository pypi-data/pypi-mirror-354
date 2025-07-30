import base64
import binascii
from .exceptions import DataError


class ELLEEntry:

    def __init__(self, name: str, flags: tuple[str, ...] | None, value: bytes):
        self.name = name
        self.flags = flags
        self.value = value

    def __str__(self):
        return f'ElleEntry:\n    name: {self.name}\n    flags: {self.flags}\n    value: {self.value}'

    def __repr__(self):
        return f'ElleEntry(name={self.name}, flags={self.flags}, value={self.value})'

    def __iter__(self):
        yield self.name
        yield self.flags
        yield self.value


class ELLEFile:

    def __init__(self, elle_file_path: str | None = None, *, data_name: str = None, values: tuple[ELLEEntry, ...] = ()):

        if elle_file_path:
            with open(elle_file_path, 'r') as elle_file:
                file = elle_decode(elle_file.read())
                self.data_name, self.values = (file.data_name, file.values)
        else:
            self.data_name = data_name
            self.values = values

    def find_entry_with_name(self, name: str) -> ELLEEntry | None:
        return next((v for v in self.values if v.name == name), None)

    def save_file(self, file_name: str):
        with open(file_name, 'w') as elle_file:
            elle_file.write(elle_encode(self.data_name, self.values))

    def set_data_name(self, data_name: str):
        self.data_name = data_name

    def add_entry(self, entry: ELLEEntry):
        self.values = self.values + (entry,)

    def __str__(self):
        return elle_encode(self.data_name, self.values)

    def __repr__(self):
        return f"ELLEFile(data_name={self.data_name!r}, values={self.values!r})"


def elle_encode(data_type: str, entries: tuple[ELLEEntry, ...]) -> str:

    lines = [f'|{data_type}|']

    used_names = []
    for entry in entries:

        if entry.name in used_names:
            raise DataError(f"Duplicate name '{entry.name}'")

        if not entry.name or not entry.value:
            raise DataError("Missing or malformed data")

        if '$' in entry.name:
            raise DataError("'$' is not allowed")

        if '\n' in entry.name:
            raise DataError("Line break is not allowed")

        lines.append(f"{entry.name}${','.join(entry.flags)}${base64.b64encode(entry.value).decode('utf-8')}")
        used_names.append(entry.name)

    lines.append(f'|/{data_type}|')

    return '\n'.join(lines)

def elle_decode(encoded: str) -> ELLEFile:
    lines = encoded.strip().split('\n')

    if not lines or not lines[0].startswith('|') or not lines[-1].startswith('|/'):
        raise DataError("Malformed data: missing headers")

    type_name = lines[0][1:-1]
    end_tag = f'|/{type_name}|'
    if lines[-1] != end_tag:
        raise DataError(f"End tag '{lines[-1]}' does not match start tag '{type_name}'")

    entries = []
    for line in lines[1:-1]:
        if '$' not in line:
            raise DataError(f"Malformed line (missing $): {line}")
        split = line.split('$', 2)

        if len(split) != 3:
            raise DataError(f"No flags entry: {line}")

        n, f, v = split
        f = tuple(f.split(','))

        try:
            entries.append(ELLEEntry(name=n, flags=f, value=base64.b64decode(v, validate=True)))

        except binascii.Error:
            raise DataError(f"Invalid base64: {line}")

    return ELLEFile(data_name=type_name, values=tuple(entries))
