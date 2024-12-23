
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Control/Monad/Fail.hs--fail-Maybe

# poly_type
Parametric

# signature
```haskell
fail :: String -> Maybe a
```   

# code
```haskell
fail x = Nothing
```

# dependencies
## 0
```haskell
data Maybe a = Nothing | Just a
```
## 1
```haskell
x :: String
```