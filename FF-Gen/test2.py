
import sys
import ruamel.yaml as yaml

yaml_str = """\
dic:
  - A: var1    # need to get these strings quoted
  - B: var2
  - C: var3
  - D: var4
  - E: 3       # leave this alone
"""

# the scalar emitter from emitter.py
def process_scalar(self):
    if self.analysis is None:
        self.analysis = self.analyze_scalar(self.event.value)
    if self.style is None:
        self.style = self.choose_scalar_style()
    split = (not self.simple_key_context)
    # VVVVVVVVVVVVVVVVVVVV added
    if split:  # not a key
        is_string = True
        if self.event.value and self.event.value[0].isdigit():
            is_string = False
        # insert extra tests for scalars that should not be ?
        if is_string:
            self.style = "'"
    # ^^^^^^^^^^^^^^^^^^^^
    # if self.analysis.multiline and split    \
    #         and (not self.style or self.style in '\'\"'):
    #     self.write_indent()
    if self.style == '"':
        self.write_double_quoted(self.analysis.scalar, split)
    elif self.style == '\'':
        self.write_single_quoted(self.analysis.scalar, split)
    elif self.style == '>':
        self.write_folded(self.analysis.scalar)
    elif self.style == '|':
        self.write_literal(self.analysis.scalar)
    else:
        self.write_plain(self.analysis.scalar, split)
    self.analysis = None
    self.style = None
    if self.event.comment:
        self.write_post_comment(self.event)

data = yaml.load(yaml_str, Loader=yaml.RoundTripLoader)
dd = yaml.RoundTripDumper
dd.process_scalar = process_scalar
yaml.dump(data, sys.stdout, Dumper=dd)
