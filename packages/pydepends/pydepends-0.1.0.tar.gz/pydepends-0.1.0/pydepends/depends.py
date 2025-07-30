# Copyright 2024 Eric Cardozo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You can obtain a copy of the License at:
# 
#     http://www.apache.org/licenses/LICENSE-2.0
#
# This software is distributed "AS IS," without warranties or conditions.
# See the License for specific terms.
#
# For inquiries, visit: mr-mapache.github.io/py-msgbus/ 

from typing import Generator, AsyncGenerator 
from inspect import signature, iscoroutinefunction, isasyncgenfunction
from contextlib import ExitStack, AsyncExitStack, contextmanager, asynccontextmanager
from collections.abc import Callable
from functools import wraps

class Provider:
    def __init__(self):
        self.dependency_overrides = dict()
    
    def override(self, dependency: Callable, override: Callable):
        self.dependency_overrides[dependency] = override

class Dependency:
    def __init__(self, callable: Callable):
        self.callable = callable


async def async_resolve(function: Callable, provider: Provider, *args, **kwargs):
    parameters = signature(function).parameters
    bounded = signature(function).bind_partial(*args, **kwargs)
    exit_stack = AsyncExitStack()
    
    for name, parameter in parameters.items():
        if name not in bounded.arguments and isinstance(parameter.default, Dependency):
            dependency = parameter.default.callable
            if dependency in provider.dependency_overrides:
                dependency = provider.dependency_overrides[dependency]
            
            if iscoroutinefunction(dependency) or isasyncgenfunction(dependency):
                dep_args, dep_stack = await async_resolve(dependency, provider)
                async with dep_stack:
                    if isasyncgenfunction(dependency):
                        gen = dependency(*dep_args.args, **dep_args.kwargs)
                        bounded.arguments[name] = await exit_stack.enter_async_context(_async_managed_dependency(gen))
                    else:
                        bounded.arguments[name] = await dependency(*dep_args.args, **dep_args.kwargs)
            else:
                dep_args, dep_stack = resolve(dependency, provider)
                with dep_stack:
                    dep_instance = dependency(*dep_args.args, **dep_args.kwargs)
                    if isinstance(dep_instance, Generator):
                        bounded.arguments[name] = exit_stack.enter_context(_managed_dependency(dep_instance))
                    else:
                        bounded.arguments[name] = dep_instance
    
    return bounded, exit_stack


def resolve(function: Callable, provider: Provider, *args, **kwargs):
    parameters = signature(function).parameters
    bounded = signature(function).bind_partial(*args, **kwargs)
    exit_stack = ExitStack()
    
    for name, parameter in parameters.items():
        if name not in bounded.arguments and isinstance(parameter.default, Dependency):
            dependency = parameter.default.callable
            if dependency in provider.dependency_overrides:
                dependency = provider.dependency_overrides[dependency]
            
            if iscoroutinefunction(dependency) or isasyncgenfunction(dependency):
                raise RuntimeError(f"Cannot resolve async dependency {dependency.__name__} in sync context")
            
            dep_args, dep_stack = resolve(dependency, provider)
            with dep_stack:
                dep_instance = dependency(*dep_args.args, **dep_args.kwargs)
                if isinstance(dep_instance, Generator):
                    bounded.arguments[name] = exit_stack.enter_context(_managed_dependency(dep_instance))
                else:
                    bounded.arguments[name] = dep_instance
    
    return bounded, exit_stack





@contextmanager
def _managed_dependency(generator: Generator):
    try:
        value = next(generator)
        yield value
    finally:
        try:
            next(generator, None)
        except StopIteration:
            pass




@asynccontextmanager
async def _async_managed_dependency(generator: AsyncGenerator):
    try:
        value = await generator.__anext__()
        yield value
    finally:
        try:
            await generator.aclose()
        except StopAsyncIteration:
            pass
        except RuntimeError as e:
            if "cannot reuse already awaited" not in str(e):
                raise


def Depends(callable: Callable):
    return Dependency(callable)

def inject(provider: Provider):
    def decorator(function: Callable):
        if iscoroutinefunction(function) or isasyncgenfunction(function):
            @wraps(function)
            async def async_wrapper(*args, **kwargs):
                bounded, exit_stack = await async_resolve(function, provider, *args, **kwargs)
                async with exit_stack:
                    return await function(*bounded.args, **bounded.kwargs)
            return async_wrapper
        else:
            @wraps(function)
            def sync_wrapper(*args, **kwargs):
                bounded, exit_stack = resolve(function, provider, *args, **kwargs)
                with exit_stack:
                    return function(*bounded.args, **bounded.kwargs)
            return sync_wrapper
    return decorator