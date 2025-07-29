from __future__ import annotations

import contextlib
import inspect
import logging
import re
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, get_type_hints, Literal

from griffe import Docstring, DocstringSectionKind  # type: ignore
from pydantic import BaseModel, Field, create_model  # type: ignore


@dataclass
class FuncSchema:
    """Captured schema for a Python function."""

    name: str
    description: str | None
    params_pydantic_model: type[BaseModel]
    params_json_schema: Dict[str, Any]
    signature: inspect.Signature

    def to_call_args(self, data: BaseModel) -> tuple[list[Any], dict[str, Any]]:
        positional_args: list[Any] = []
        keyword_args: dict[str, Any] = {}
        for name, param in self.signature.parameters.items():
            value = getattr(data, name, None)
            if (
                param.kind == param.POSITIONAL_ONLY
                or param.kind == param.POSITIONAL_OR_KEYWORD
            ):
                positional_args.append(value)
            elif param.kind == param.KEYWORD_ONLY:
                keyword_args[name] = value
        return positional_args, keyword_args


DocstringStyle = Literal["google", "numpy", "sphinx"]


def _detect_docstring_style(doc: str) -> DocstringStyle:
    scores: dict[DocstringStyle, int] = {"sphinx": 0, "numpy": 0, "google": 0}

    sphinx_patterns = [r"^:param\s", r"^:type\s", r"^:return:", r"^:rtype:"]
    for pattern in sphinx_patterns:
        if re.search(pattern, doc, re.MULTILINE):
            scores["sphinx"] += 1

    numpy_patterns = [
        r"^Parameters\s*\n\s*-{3,}",
        r"^Returns\s*\n\s*-{3,}",
        r"^Yields\s*\n\s*-{3,}",
    ]
    for pattern in numpy_patterns:
        if re.search(pattern, doc, re.MULTILINE):
            scores["numpy"] += 1

    google_patterns = [r"^(Args|Arguments):", r"^(Returns):", r"^(Raises):"]
    for pattern in google_patterns:
        if re.search(pattern, doc, re.MULTILINE):
            scores["google"] += 1

    max_score = max(scores.values())
    if max_score == 0:
        return "google"

    styles: list[DocstringStyle] = ["sphinx", "numpy", "google"]
    for style in styles:
        if scores[style] == max_score:
            return style
    return "google"


@contextlib.contextmanager
def _suppress_griffe_logging():
    logger = logging.getLogger("griffe")
    previous_level = logger.getEffectiveLevel()
    logger.setLevel(logging.ERROR)
    try:
        yield
    finally:
        logger.setLevel(previous_level)


@dataclass
class FuncDocumentation:
    name: str
    description: str | None
    param_descriptions: Dict[str, str] | None


def generate_func_documentation(
    func: Callable[..., Any], style: DocstringStyle | None = None
) -> FuncDocumentation:
    name = func.__name__
    doc = inspect.getdoc(func)
    if not doc:
        return FuncDocumentation(name=name, description=None, param_descriptions=None)

    with _suppress_griffe_logging():
        docstring = Docstring(
            doc, lineno=1, parser=style or _detect_docstring_style(doc)
        )
        parsed = docstring.parse()

    description: str | None = next(
        (
            section.value
            for section in parsed
            if section.kind == DocstringSectionKind.text
        ),
        None,
    )

    param_descriptions: Dict[str, str] = {
        param.name: param.description
        for section in parsed
        if section.kind == DocstringSectionKind.parameters
        for param in section.value
    }

    return FuncDocumentation(
        name=name,
        description=description,
        param_descriptions=param_descriptions or None,
    )


@dataclass
class FunctionTool:
    """Representation of a local function tool."""

    func: Callable[..., Any]
    name: str
    description: str
    params_json_schema: Dict[str, Any]
    params_model: type[BaseModel]

    def run(self, **kwargs: Any) -> Any:
        """Execute the wrapped function after validating arguments."""
        data = self.params_model(**kwargs)
        args, kw = [], {}
        for name, param in inspect.signature(self.func).parameters.items():
            if param.kind in (param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD):
                args.append(getattr(data, name))
            elif param.kind == param.KEYWORD_ONLY:
                kw[name] = getattr(data, name)
        return self.func(*args, **kw)


def function_schema(
    func: Callable[..., Any],
    *,
    docstring_style: DocstringStyle | None = None,
    name_override: str | None = None,
    description_override: str | None = None,
    use_docstring_info: bool = True,
) -> FuncSchema:
    if use_docstring_info:
        doc_info = generate_func_documentation(func, docstring_style)
        param_descs = doc_info.param_descriptions or {}
    else:
        doc_info = None
        param_descs = {}

    func_name = name_override or doc_info.name if doc_info else func.__name__

    sig = inspect.signature(func)
    type_hints = get_type_hints(func)

    fields: Dict[str, Any] = {}

    for name, param in sig.parameters.items():
        if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
            continue
        ann = type_hints.get(name, param.annotation)
        if ann == inspect._empty:
            ann = Any
        field_desc = param_descs.get(name)
        if param.default is inspect._empty:
            fields[name] = (ann, Field(..., description=field_desc))
        else:
            fields[name] = (ann, Field(default=param.default, description=field_desc))

    model = create_model(f"{func_name}_args", __base__=BaseModel, **fields)
    schema = model.model_json_schema()

    return FuncSchema(
        name=func_name,
        description=description_override or doc_info.description if doc_info else None,
        params_pydantic_model=model,
        params_json_schema=schema,
        signature=sig,
    )


def function_tool(
    func: Optional[Callable[..., Any]] = None,
    *,
    name_override: Optional[str] = None,
    description_override: Optional[str] = None,
) -> FunctionTool | Callable[[Callable[..., Any]], FunctionTool]:
    """Decorator to create a :class:`FunctionTool` from a function."""

    def _create(f: Callable[..., Any]) -> FunctionTool:
        schema = function_schema(
            f,
            docstring_style=None,
            name_override=name_override,
            description_override=description_override,
        )
        return FunctionTool(
            func=f,
            name=schema.name,
            description=schema.description or "",
            params_json_schema=schema.params_json_schema,
            params_model=schema.params_pydantic_model,
        )

    if func is not None:
        return _create(func)

    def decorator(f: Callable[..., Any]) -> FunctionTool:
        return _create(f)

    return decorator
