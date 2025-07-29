"""
Core data operations for FP-Ops that provide ergonomic data handling
without expanding the DSL significantly.
"""
from __future__ import annotations
from typing import Any, Dict, List, Callable, TypeVar, Union, Tuple, Optional, cast, Type, overload, Protocol, runtime_checkable
from dataclasses import is_dataclass
from functools import reduce
from fp_ops import operation, Operation

"""
Note: These functions return Operations (not values) to enable better composition.
This allows us to build transformation pipelines before having data:

    # Define transformations independently of data
    extract_user_email = pipe(
        get("user"),
        get("contact.email", "unknown")
    )
    
    # Apply to different data sources later
    email1 = await extract_user_email(response1)
    emails = await map(extract_user_email)(user_list)

This separation of "what to do" from "what to do it with" is the key
to functional composition and reusability.
"""


def get(path: str, default: Any = None) -> Operation[[Any], Any]:
    """
    Access nested data using dot notation or dict keys.
    Configured with a path and an optional default value.
    The returned operation takes the data object as input.
    
    Examples:
        # Assuming 'data' is the dict or object to access
        # name_op = get("user.name")
        # user_name = await name_op.execute(data)
        
        # price_op = get("items.0.price", 0.0) # With default
        # item_price = await price_op.execute(data)

        # Can be used in 'build' or 'pipe':
        # pipe(
        #   get_data_source_op,
        #   get("user.profile.email", "notfound@example.com")
        # )
    """
    def _get_inner(data: Any) -> Any:
        if not path:  # path and default are from the outer scope
            return data
            
        parts = path.replace('[', '.').replace(']', '').split('.')
        current = data
        
        for part in parts:
            if current is None:
                return default
                
            # Try dict access first
            if isinstance(current, dict):
                current = current.get(part, None)
            # Then try numeric index for sequences
            elif isinstance(current, (list, tuple)) and part.isdigit():
                idx = int(part)
                current = current[idx] if 0 <= idx < len(current) else None
            # Finally try attribute access
            elif hasattr(current, part):
                current = getattr(current, part)
            else:
                return default
                
        return current if current is not None else default

    return operation(_get_inner)


async def _resolve_operation(op: "Operation", data: Any, **kwargs: Any) -> Any:
    """
    Execute *op* and, if the successful result is itself an Operation,
    keep executing until we obtain a real value (or hit an error).
    """
    current: "Operation | None" = op

    while isinstance(current, Operation):
        res = await current.execute(data, **kwargs)
        if not res.is_ok():
            return None

        value = res.default_value(None)
        if isinstance(value, Operation):
            current = value                     # loop again
        else:
            return value                        # final concrete value

    return None                                 # should not reach here




T = TypeVar('T')
R = TypeVar('R')



# Protocol for Pydantic v2 models
@runtime_checkable
class PydanticV2Model(Protocol):
    @classmethod
    def model_validate(cls, obj: Any) -> Any: ...

# Protocol for Pydantic v1 models
@runtime_checkable
class PydanticV1Model(Protocol):
    @classmethod
    def parse_obj(cls, obj: Any) -> Any: ...

@overload
def build(schema: Dict[str, Any]) -> Operation[[Any], Dict[str, Any]]:
    ...

@overload
def build(schema: Dict[str, Any], model: Type[T]) -> Operation[[Any], T]:
    ...

def build(
    schema: Dict[str, Any], 
    model: Optional[Type[T]] = None
) -> Union[Operation[[Any], Dict[str, Any]], Operation[[Any], T]]:
    """
    Build an object from a schema. Values can be static, callables, or operations.
    
    Args:
        schema: Dictionary mapping field names to values, callables, or operations
        model: Optional model class (dataclass or Pydantic model) to instantiate
               with the built dictionary
    
    Returns:
        Operation that builds either a dictionary or an instance of the model class
    
    Examples:
        # Return a dictionary (backward compatible)
        build({
            "id": get("user_id"),
            "fullName": lambda d: f"{d['first_name']} {d['last_name']}",
            "email": get("contact.email"),
            "isActive": True
        })
        
        # Return a Pydantic model instance
        class UserProfile(BaseModel):
            id: int
            fullName: str
            email: str
            isActive: bool
            
        build({
            "id": get("user_id"),
            "fullName": lambda d: f"{d['first_name']} {d['last_name']}",
            "email": get("contact.email"),
            "isActive": True
        }, UserProfile)
        
        # Return a dataclass instance
        @dataclass
        class BookDetails:
            title: str
            price: str
            
        extract_book_details: Operation[[ElementHandle], BookDetails] = build({
            "title": GetText("h3 > a"),
            "price": GetText("p.price_color"),
        }, BookDetails)
    """
    # Quick check if any operation in schema requires context
    require_ctx = False
    ctx_type = None
    
    for value in schema.values():
        if isinstance(value, Operation):
            # Check the operation's graph for context requirements
            for spec in value._graph._nodes.values():
                if spec.require_ctx:
                    require_ctx = True
                    if spec.ctx_type:
                        ctx_type = spec.ctx_type
                    break
        if require_ctx:
            break
    
    async def _build(data: Any, **op_kwargs: Any) -> Any:  # Return Any to avoid type issues
        result: Dict[str, Any] = {}

        for key, value in schema.items():
            if isinstance(value, Operation):
                # Fully resolve chained / nested operations
                result[key] = await _resolve_operation(value, data, **op_kwargs)
            elif isinstance(value, dict):
                # Handle nested dictionaries
                nested = await build(value).execute(data, **op_kwargs)
                result[key] = nested.default_value({})
            elif callable(value) and not isinstance(value, (type, bool, int, float, str)):
                # Handle callables (but not built-in types)
                try:
                    result[key] = value(data)
                except Exception:
                    result[key] = None
            else:
                # Handle static values
                result[key] = value

        # If a model class was provided, instantiate it
        if model is not None:
            try:
                # Check if it's a Pydantic model using duck typing
                if hasattr(model, 'model_validate'):
                    # Pydantic v2
                    return model.model_validate(result)    # type: ignore[attr-defined]
                elif hasattr(model, 'parse_obj'):
                    # Pydantic v1
                    return model.parse_obj(result)         # type: ignore[attr-defined]
                elif is_dataclass(model):
                    # Standard dataclass
                    return model(**result)
                else:
                    # Try generic instantiation (works for most classes)
                    return model(**result)
            except Exception as e:
                # If model instantiation fails, you might want to handle this
                # differently based on your error handling strategy
                raise ValueError(f"Failed to instantiate {model.__name__}: {e}")
        
        return result
    
    return operation(context=require_ctx, context_type=ctx_type)(_build) # type: ignore[arg-type]

def merge(*sources: Union[Dict[str, Any],
                          Callable[[Any], Dict[str, Any]],
                          Operation[[Any], Dict[str, Any]]]
          ) -> Operation[[Any], Dict[str, Any]]:
    """
    Merge multiple dictionaries or dict-returning sources into a single dictionary.
    
    This operation combines dictionaries from various sources, with later sources
    overriding values from earlier ones when keys conflict. Sources can be:
    
    - Static dictionaries: Merged as-is
    - Operations: Executed and their dict results merged  
    - Callables: Called with input data and their dict results merged
    - Dicts containing Operations: Operations within dicts are executed
    
    Args:
        *sources: Variable number of sources that each produce a dictionary.
                 Can be static dicts, Operations returning dicts, callables
                 returning dicts, or dicts containing Operation values.
    
    Returns:
        Operation that merges all source dictionaries into one.
    
    Examples:
        # Merge static dictionaries
        merge({"a": 1}, {"b": 2}, {"a": 3})  # Result: {"a": 3, "b": 2}
        
        # Merge operations that return dicts
        merge(
            get("user.profile"),      # Operation returning dict
            get("user.settings"),     # Operation returning dict
            {"timestamp": "2024-01-01"}  # Static dict
        )
        
        # Mix static values with operations in a dict
        merge(
            get("user.contact"),
            {"name": get("user.name"), "active": True}  # Operation in dict
        )
        
        # Use callables for dynamic merging
        merge(
            lambda d: {"id": d["user_id"]},
            lambda d: {"score": len(d["items"]) * 10}
        )
    
    Notes:
        - If a source returns None or fails, it's skipped (no error propagated)
        - Operations within dictionaries are executed with the input data
        - Later sources override earlier ones for conflicting keys
        - All sources receive the same input data (not chained)
    """
    async def _merge(data: Any) -> Dict[str, Any]:
        out: Dict[str, Any] = {}

        for src in sources:
            if isinstance(src, Operation):
                res = await src.execute(data)
                update = res.default_value({}) if res.is_ok() else {}
            elif callable(src):
                update = src(data)
            else:
                update = {}
                for key, value in src.items():
                    if isinstance(value, Operation):
                        res = await value.execute(data)
                        update[key] = res.default_value(None) if res.is_ok() else None
                    else:
                        update[key] = value

            if isinstance(update, dict):
                out.update(update)

        return out
    
    return operation(_merge)


def update(update_values: Dict[str, Any]) -> Operation[[Dict[str, Any]], Dict[str, Any]]:
    """
    Update a dict with another dict (the update_values).
    The outer function takes the update_values as configuration and returns
    an inner function that takes the source dictionary.

    Example:
        # source_dict = {"a": 1, "b": 2}
        # updater = update({"b": 3, "c": 4})
        # updated_dict = await updater.execute(source_dict)
        # Result: {"a": 1, "b": 3, "c": 4}
    """
    @operation
    def _update_inner(source: Dict[str, Any]) -> Dict[str, Any]:
        return {**source, **update_values}
    return _update_inner


