## Template In Python :

Remaking the (in)famous 'template' of C++ in Python.<br/>


## Motivation :

While template are well known in the programming community for adding layers of
complexity in a language.<br/>
I think that it has its use cases besides generics.

In C++, template's parameters can be of many kinds (integer, type, ...) which
enable us to simulate partial with a more explicit syntax in my opinion.<br/>
Because, unlike with partials, we can make a better distinction between
parameters of the function and fixed variables influencing it.

> [!Note]
> Here is some vocabulary :<br/>
> &emsp; **\-** a **function template** define a family of functions with the
> same core implementation but that need more context to be fully initialised.<br/>
> &emsp; **\-** a **class template** is the same as a function template but for
> classes. <br/>
>
> The context needed to be fully initialised is what I call **template's arguments**.

Here is an example of function template in Python :<br>
```Python
@template['switcher': dict]
def convertTo(name: str) :
    return switcher[name]

MIME_TYPES: dict = ...
FILE_EXTENSIONS: dict = ...

print(convertTo[MIME_TYPES]("markdown"))      # --> text/markdown
print(convertTo[FILE_EXTENSIONS]("markdown")) # --> .md

#We can also asign them to variables :
converTo_MIMETypes = convertTo[MIME_TYPES]
convertTo_FileExtensions = convertTo[FILE_EXTENSIONS]
```

Moreover, it extends the notion of partial to classes.<br/>
**...**

## Implementation :

The main concern was to reproduce the C++ syntax while being able to manipulate
the templated function/class.<br/>
That's why I choose to make it as a decorator.<br/>

> [!Tip]
> I could also have implemented it as a context manager but it would have
> differed to much from the C++ syntax.

### Now, how to build a function template ?

- The first step is to be able to take template's arguments while still being able
to take function's arguments at the same time.<br/>
An easy way to achieve that would be to make the function template callable and
taking as arguments the template's arguments then returning
the builded function.<br/>
However I wouldn't be able to make function template partially initialisable,
which is a feature that I plan to implement too even if I don't think it's possible
in C++.<br/>
Therefore I need the function template to implement `__getitem__`.

- The second step is to build the function with the template's arguments passed.<br/>
An easy way would be to declare global variables with the name of the parameters
and the arguments passed as values.<br/>
But it would make those names non-reusable which is unintuitive when coming from
C++.<br/>
Therefore I need to declare those variable inside a scope that I am calling the
**template's scope**.<br/>

### And how to build a class template ?

Well I don't currently know.