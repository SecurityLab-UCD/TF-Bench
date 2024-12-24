
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Maybe.hs--maybe

# poly_type
Parametric

# signature
```haskell
maybe :: b -> (a -> b) -> Maybe a -> b
```   

# code
```haskell
maybe _ f (Just x) = f x
maybe n _ Nothing  = n
```

# dependencies
## 0
```haskell
data Maybe a = Nothing | Just a
```
## 1
```haskell
Just :: a -> Maybe a
```
## 2
```haskell
Nothing :: Maybe a
```
