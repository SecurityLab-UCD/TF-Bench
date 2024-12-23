
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Either.hs--either

# poly_type
Parametric

# signature
```haskell
either :: (a -> c) -> (b -> c) -> Either a b -> c
```   

# code
```haskell
either _ g (Right y)    =  g y
either f _ (Left x)     =  f x
```

# dependencies

## 0
```haskell
data Either a b = Left a | Right b
```
## 1
```haskell
Left :: a -> Either a b
```
## 2
```haskell
Right :: b -> Either a b
```