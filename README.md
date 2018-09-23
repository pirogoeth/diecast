# diecast

Diecast is a dependency injection framework for Python.

It aims to be very simple to use, with an extremely simple API.

## Usage

To start with diecast, install it with `pip`:

    pip install -e git+https://github.com/pirogoeth/diecast.git#egg=diecast

### Component Registry

Diecast has a global registry that can be used. Otherwise, you can easily build a new registry:

    from diecast.registry import ComponentRegistry
    my_registry = ComponentRegistry()

### Injectors

Injectors must be created to inject dependencies into functions.  You can build an injector using `make_injector`:

    from diecast.inject import make_injector

    # If you're using the global registry
    from diecast.registry import get_registry
    my_registry = get_registry()

    inject = make_injector(my_registry)

### Injecting Components

After creating an injector, you can use it to decorate any function you want your components to be injected to:

    @inject
    def my_function(item: MyComponent) -> Any:
        return do_something(item)

    my_function()

When calling an injected function, you can either omit the arguments you expect to be injected
OR you can replace the injected arguments with `...` as a placeholder.

    @inject
    def my_function2(item: MyComponent, doer_cb: Callable[[Any], [Any]]) -> Any:
        return doer_cb(do_something(item))

    my_function2(..., lambda item: mutate(item))
    # is roughly equivalent to:
    my_function2(lambda item: mutate(item))

### Creating Components

Diecast has a simple `Component` interface for building injectable components:

    from diecast.component import Component

    class MyComponent(Component):

        @classmethod
        def init(cls: Type[Component]) -> 'MyComponent':
            return MyComponent()

### Registering Components

After defining your component(s), add your component to the registry:

    my_registry.add(
        # `cls` is the type we will be injecting
        cls=MyComponent,
        # `init` is a callable which will create the instance of `cls`
        # <Component>.init is the default initializer and does not need to be explicitly set
        init=MyComponent.init,
        # `init` will *only* be called once and the instance will be stored
        persist=True,
    )

Or, if you are using the global registry, you can use this shortcut:

    from diecast.registry import register_component

    register_component(
        # `cls` is the type we will be injecting
        cls=MyComponent,
        # `init` is a callable which will create the instance of `cls`
        # <Component>.init is the default initializer and does not need to be explicitly set
        init=MyComponent.init,
        # `init` will *only* be called once and the instance will be stored
        persist=True,
        # `registry` defaults to the global registry
        # set it to your registry if you so desire
        registry=my_registry,
    )

### Getting Component Instances

You can fetch component instances easily by subscripting the registry:

    instance = my_registry[MyComponent]

If the component was registered with `persist=True`, the subscript will return the
persisted component instance.

If there is not a persisted instance, the subscript will return a new instance
of the component.

## Examples

Some more practical usage examples are include in the [examples directory](/examples/).

## Contributing

Pull requests are welcomed and encouraged.  Feel free to ask questions via the issue tracker or anywhere else (such as [Gitter](https://gitter.im/pirogoeth)).

If you're submitting a PR, please install [`pre-commit`](https://github.com/pre-commit/pre-commit) and install the local git pre-commit hook to run style checks.

Any contributions will be greatly appreciated <3.

## License

Licensed under MIT. See [LICENSE](/LICENSE) for details.
