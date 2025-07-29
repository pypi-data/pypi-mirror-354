
from __future__ import annotations
from relationalai.early_access.metamodel import types, factory as f

# Rel Annotations as IR Relations (to be used in IR Annotations)

# output in arrow
arrow = f.relation("arrow", [])
arrow_annotation = f.annotation(arrow, [])

# do not output diagnostics for this error
no_diagnostics = f.relation("no_diagnostics", [f.field("code", types.Symbol)])

# do not inline this definition
no_inline = f.relation("no_inline", [])
no_inline_annotation = f.annotation(no_inline, [])

# indicates to the rel engine that this relation is a function
function = f.relation("function", [])
function_annotation = f.annotation(function, [])
