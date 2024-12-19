
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Either.hs--either

# poly_type
Parametric

# signature
```haskell
f1 :: (a -> c) -> (b -> c) -> T1 a b -> c
```   

# code
```haskell
f1 _ g (T2 y)    =  g y
f1 f _ (T3 x)     =  f x
```

# dependencies

## 0
```haskell
data T1 a b = T2 a | T3 b
```
## 1
```haskell
T2 :: a -> T1 a b
```
## 2
```haskell
T3 :: b -> T1 a b
```